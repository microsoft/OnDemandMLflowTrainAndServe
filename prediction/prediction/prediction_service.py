import json
from enum import Enum
from flask import Flask, request
import requests
from applicationinsights.flask.ext import AppInsights


class JobStatus(Enum):
    PENDING = 'pending'
    RUNNING = 'running'
    COMPLETED = 'completed'
    ERROR = 'error'


class PredictionService:
    def __init__(self, training_config, mlflow_models_mapping, prediction_config):
        self.training_config = training_config
        self.mlflow_models_mapping = mlflow_models_mapping
        self.training_url = training_config['host'] + ':' + str(training_config['port']) + training_config[
            'api_train_path']
        self.appinsights_key = training_config['appinsights_key']
        self.service_name = prediction_config['service_name']

    def check_training_status(self, run_id):
        try:
            training_status_response = requests.get(self.training_url + '/' + str(run_id),
                                                    timeout=self.training_config['timeout']).json()
            return TrainingResponse(run_id, training_status_response['state'], training_status_response['message'])

        except requests.exceptions.HTTPError as e:
            return TrainingResponse(None, JobStatus.ERROR.value, str(e))

        except requests.exceptions.Timeout:
            return TrainingResponse(None, JobStatus.ERROR.value, "request to training service timed out")

        except requests.exceptions.ConnectionError:
            return TrainingResponse(None, JobStatus.ERROR.value, "failed connecting to training service")

    def train_new_model(self, model_type, parameters):
        try:
            payload = {
                "modelType": model_type,
                "parameters": parameters
            }
            training_response = requests.post(self.training_url,

                                              data=json.dumps(payload),
                                              headers={
                                                  'content-type': 'application/json'},
                                              timeout=self.training_config['timeout'])
            training_parsed_response = json.loads(
                training_response.content.decode('utf-8'))
            return TrainingResponse(training_parsed_response['runId'],
                                    None,
                                    None)
        except requests.exceptions.HTTPError as e:
            return TrainingResponse(None, JobStatus.ERROR.value, str(e))
        except requests.exceptions.Timeout:
            return TrainingResponse(None, JobStatus.ERROR.value, "request to training service timed out")
        except requests.exceptions.ConnectionError:
            return TrainingResponse(None, JobStatus.ERROR.value, "failed connecting to training service")

    def get_model_url(self, model_type_name):
        return self.mlflow_models_mapping[model_type_name]['model_service_host'] + ':' + str(
            self.mlflow_models_mapping[model_type_name]['model_service_port'])

    def get_prediction(self, params, model_type):
        models_full_config = self.mlflow_models_mapping
        model_url = self.get_model_url(model_type) + models_full_config['prediction_url_path']
        model_response = requests.post(model_url, data=json.dumps(params), headers={
            'content-type': 'application/json'}, timeout=models_full_config['timeout']).json()
        return model_response

    @staticmethod
    def build_prediction_response(run_id, status, status_message, results):
        return {'runId': run_id, 'status': status, 'statusMessage': status_message, 'result': results}

    def run_flask_server(self, port, host):
        """Run the flask server."""
        app = Flask(__name__)

        if self.appinsights_key is not None and self.service_name is not None:
            app.config['APPINSIGHTS_INSTRUMENTATIONKEY'] = self.appinsights_key
            # log requests, traces and exceptions to the Application Insights service
            appinsights = AppInsights(app)
            appinsights.context.cloud.role = self.service_name

        # pylint: disable=unused-variable
        @app.route('/')
        def index():
            return 'Prediction Service is up.'

        # pylint: disable=unused-variable
        @app.route('/predict', methods=['POST'])
        def get_prediction():
            body = request.get_json()
            model_parameters = body['modelParameters']
            prediction_parameters = body['predictionParameters']
            run_id = body.get('runId')
            model_type_name = body.get('modelType')
            if run_id is not None:
                # if run_id is not None it means we have a job that we haven't got it's results/artifacts
                # check for status of that job
                training_response = self.check_training_status(run_id)
                # if it haven't completed yet return it's current status
                if training_response.status != JobStatus.COMPLETED.value:
                    response = json.dumps(
                        self.build_prediction_response(run_id, training_response.status,
                                                       training_response.status_message,
                                                       [], {}))
                else:
                    model_response = self.get_prediction(prediction_parameters, model_type_name)
                    if model_response['status'] == 'error':
                        response = json.dumps(self.build_prediction_response(run_id, JobStatus.ERROR.value,
                                                                             model_response['statusMessage'],
                                                                             [], {}))
                    else:
                        response = json.dumps(
                            self.build_prediction_response(run_id, JobStatus.COMPLETED.value,
                                                           None,
                                                           model_response['result']))
            else:
                # if the job is None
                # since the simulation service is unaware of model and prediction parameters separation
                # two options are possible: first train a new model
                # second if the change in the ui was only on prediction parameters, maybe we already trained that model
                model_response = self.get_prediction(prediction_parameters, model_type_name)
                if model_response['status'] == 'error':
                    training_response = self.train_new_model(
                        body['modelType'], model_parameters)
                    response = json.dumps(
                        self.build_prediction_response(training_response.run_id, training_response.status,
                                                       training_response.status_message,
                                                       [], {}))
                else:
                    response = json.dumps(
                        self.build_prediction_response(run_id, JobStatus.COMPLETED.value,
                                                       None,
                                                       model_response['result']))

            return response

        app.run(port=port, host=host)


class TrainingResponse:  # pylint: disable=too-few-public-methods
    def __init__(self, run_id, status, status_message):
        self.run_id = run_id
        self.status = status
        self.status_message = status_message
