import requests
import unittest
from unittest import mock
import json
from app_config_tests import training_service_config, mlflow_models_mapping, prediction_config
from prediction.prediction_service import PredictionService, TrainingResponse, JobStatus


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code
        self.content = json.dumps(self.json_data).encode("utf-8")

    def json(self):
        return self.json_data


class PredictionServiceTest(unittest.TestCase):
    prediction_service = PredictionService(training_service_config, mlflow_models_mapping, prediction_config)

    # test check_training_status function
    def mocked_failed_training_response(*args, **kwargs):
        if args[0] == 'http://training-host:3001/train/run_id':
            raise requests.exceptions.ConnectionError
        return MockResponse(None, 404)

    def mocked_success_training_response(*args, **kwargs):
        if args[0] == 'http://training-host:3001/train/run_id':
            return MockResponse({'state': 'completed', 'message': None}, 200)
        return MockResponse(None, 404)

    @mock.patch('requests.get', side_effect=mocked_failed_training_response)
    def test_check_training_status_failure(self, mock):
        assert self.prediction_service.check_training_status("run_id").status == JobStatus.ERROR.value

    @mock.patch('requests.get', side_effect=mocked_success_training_response)
    def test_check_training_status_success(self, mock):
        run_id = "run_id"
        assert self.prediction_service.check_training_status(run_id).run_id == run_id
        assert self.prediction_service.check_training_status(run_id).status == JobStatus.COMPLETED.value
        assert self.prediction_service.check_training_status(run_id).status_message is None


    # test get_prediction function
    def mocked_prediction_response(*args, **kwargs):
        if args[0] == 'http://model-handler-host:3002/predict':
            return MockResponse( {'status': JobStatus.COMPLETED.value,
                                                                        'statusMessage': None, "result": [
                {
                    "date": "2017-04-29T00:00:00.000000",
                    "salesVolume": 101.89271519246286
                },
                {
                    "date": "2017-05-01T00:00:00.000000",
                    "salesVolume": 102.02099330778664
                },
                {
                    "date": "2017-05-02T00:00:00.000000",
                    "salesVolume": 111.72246771092415
                }], "probability": {
                "binsEdges": [
                    116990.02301757515,
                    124455.5402428202,
                    131921.05746806526,
                    139386.57469331034
                ],
                "probabilities": [
                    0.05,
                    0.74,
                    0.21
                ]
            }}, 200)
        return MockResponse(None, 404)

    # it should return only the relevant parameters
    @mock.patch('requests.post', side_effect=mocked_prediction_response)
    def test_get_prediction(self, mock):
        assert self.prediction_service.get_prediction({'param1': 'value'},
                                                      'model-type') == {'status': JobStatus.COMPLETED.value,
                                                                        'statusMessage': None, "result": [
                {
                    "date": "2017-04-29T00:00:00.000000",
                    "salesVolume": 101.89271519246286
                },
                {
                    "date": "2017-05-01T00:00:00.000000",
                    "salesVolume": 102.02099330778664
                },
                {
                    "date": "2017-05-02T00:00:00.000000",
                    "salesVolume": 111.72246771092415
                }], "probability": {
                "binsEdges": [
                    116990.02301757515,
                    124455.5402428202,
                    131921.05746806526,
                    139386.57469331034
                ],
                "probabilities": [
                    0.05,
                    0.74,
                    0.21
                ]
            }}
