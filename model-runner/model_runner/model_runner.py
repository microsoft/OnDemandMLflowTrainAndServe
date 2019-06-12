import os
from pathlib import Path
import json
import glob
import shutil
from datetime import datetime
from enum import Enum
import mlflow
from mlflow import sklearn as model_type
import pandas
import requests
from flask import Flask, request
from applicationinsights.flask.ext import AppInsights


class JobStatus(Enum):
    PENDING = 'pending'
    RUNNING = 'running'
    COMPLETED = 'completed'
    ERROR = 'error'


class ModelRunner:

    def __init__(self, mlflow_config, service_config):
        self.mlflow_config = mlflow_config
        self.service_config = service_config
        self.mlflow_api_url = mlflow_config['databricks_host'] + mlflow_config['api_prefix']
        self.databricks_request_headers = {'content-type': 'application/json',
                                           'Authorization': 'Bearer ' + mlflow_config[
                                               'databricks_token']}
        self.models_relative_path = mlflow_config['models_relative_path']

    date_time_format = '%Y-%m-%dT%H:%M:%S.%f%z'
    mlflow_client = mlflow.tracking.MlflowClient(tracking_uri='databricks')
    mlflow.set_tracking_uri('databricks')

    def build_prediction_payload(self, params):
        experiment_ids = [self.mlflow_config['mlflow_experiment_id']]
        payload = {'experiment_ids': experiment_ids}
        parameters_data = []
        for param in params:
            if type(params[param]) in [float, int]:
                parameters_data.append("params." + param + " = " + str((params[param])))
            else:
                parameters_data.append("params." + param + " = " + repr(str(params[param])))

        payload['filter'] = " and ".join(parameters_data)
        return payload

    def search_model(self, parameters):
        latest_run = None
        search_url = self.mlflow_api_url + self.mlflow_config['search_path']
        payload = self.build_prediction_payload(parameters)
        search_models_response = requests.post(search_url, data=json.dumps(payload),
                                               headers=self.databricks_request_headers,
                                               timeout=self.mlflow_config['timeout'])
        json_result = json.loads(search_models_response.content.decode('utf-8'))

        if 'runs' in json_result:
            results = json_result['runs']
            latest_run = sorted(results, key=lambda k: k['info']['start_time'], reverse=True)[0]

        return latest_run

    def download_model(self, run_id):
        # create local path for the downloaded model
        local_output_path = self.get_model_path(run_id)

        try:
            os.makedirs(local_output_path)
        except FileExistsError:
            return local_output_path
        # next we download the model
        # since this function does not receive a local output path
        # it downloads the artifacts to a "random" directory under /var/folders/ and returns the path to it
        output_path = self.mlflow_client.download_artifacts(run_id, self.models_relative_path)
        # the next step will be to copy the files from the output_path to local_output_path
        # the reason it is done that way, is because if we have already downloaded the model
        # we can easily find it
        for filename in glob.glob(os.path.join(output_path, '**')):
            shutil.copy(filename, local_output_path)
        shutil.rmtree(output_path)
        return local_output_path

    @staticmethod
    def get_model_path(run_id):
        return str(Path.home()) + '/models/' + run_id

    def load_and_predict(self, run_id, parameters):

        model = model_type.load_model(self.get_model_path(run_id))

        model_results = model.predict(
            pandas.DataFrame(data=parameters, index=[0]))

        return model_results

    @staticmethod
    def build_prediction_response(status, status_message, results):
        return {'status': status, 'statusMessage': status_message, 'result': results}

    def run_flask_server(self, port, host):
        """Run the flask server."""
        app = Flask(__name__)

        if self.service_config['appinsights_key'] is not None and self.service_config['service_name'] is not None:
            app.config['APPINSIGHTS_INSTRUMENTATIONKEY'] = self.service_config['appinsights_key']
            # log requests, traces and exceptions to the Application Insights service
            appinsights = AppInsights(app)
            appinsights.context.cloud.role = self.service_config['service_name']

        # pylint: disable=unused-variable
        @app.route('/')
        def index():
            return self.mlflow_config['model_name'] + ' Model Runner Service is up.'

        @app.route('/predict', methods=['POST'])
        def get_prediction():
            request_body = request.get_json()
            latest_run = self.search_model(request_body['modelParameters'])
            if latest_run is None:
                response = json.dumps(
                    self.build_prediction_response("error",
                                                   'No successfully finished runs were found',
                                                   [], {}))
            else:
                self.download_model(
                    latest_run['info']['run_uuid'])
                model_result = self.load_and_predict(latest_run['info']['run_uuid'],
                                                     request_body['predictionParameters'])
                response = json.dumps(
                    self.build_prediction_response("success",
                                                   None,
                                                   model_result.tolist()))
            return response

        app.run(port=port, host=host)
