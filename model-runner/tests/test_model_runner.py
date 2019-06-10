from unittest import mock
import unittest
import json
from datetime import datetime
import app_config_tests

from model_runner.model_runner import ModelRunner


class ModelRunnerTest(unittest.TestCase):
    model_handler = ModelRunner(app_config_tests.mlflow_config, app_config_tests.service_config)
    mlflow_tracking_server_erl = model_handler.mlflow_api_url
    run_id = "SomeRunID"

    # def test_build_prediction_payload_when_no_model_params(self):
    #     params = {"param": "value"}
    #     assert self.model_handler.build_prediction_payload(params) == \
    #            {'experiment_ids': [121212],
    #             'anded_expressions': []}
    #
    # def test_build_prediction_payload_with_model_params(self):
    #     model_params = {}
    #     for param in self.model_handler.model_parameters:
    #         if self.model_handler.model_parameters_types[param] == 'float':
    #             # should be converted later to float
    #             model_params[param] = 1
    #         else:
    #             model_params[param] = 'param'
    #     assert \
    #         self.model_handler.build_prediction_payload(model_params) == {'experiment_ids': [121212],
    #                                                                       'anded_expressions': [
    #                                                                           {'parameter': {'key': 'string_param',
    #                                                                                          'string': {
    #                                                                                              'comparator': '=',
    #                                                                                              'value': 'param'}}},
    #                                                                           {'parameter': {'key': 'float_param',
    #                                                                                          'string': {
    #                                                                                              'comparator': '=',
    #                                                                                              'value': 1.0}}}]
    #                                                                       }
    #
    # def test_build_training_payload(self):
    #     parameters = {}
    #     # empty parameters shouldn't fail and pass as empty
    #     assert self.model_handler.build_training_payload(parameters) == {'modelType': 'ModelName', 'parameters': {}}
    #     # all model parameters should be in the payload and non model parameters should be excluded
    #     parameters = {"string_param": "string", "float_param": 1.0, 'non_model_training_param': 'some_value'}
    #     assert self.model_handler.build_training_payload(parameters) == {'modelType': 'ModelName',
    #                                                                      'parameters': {"string_param": "string",
    #                                                                                     "float_param": 1.0}}

    def test_get_prediction_parameters_for_date(self):
        prediction_params = {'date': '2019-05-01T12:20:09.925Z'}
        assert self.model_handler.get_prediction_parameters(prediction_params) == {
            'ds': datetime.fromisoformat(prediction_params['date'][:-1])}

    def test_get_prediction_parameters_for_productPrice(self):
        prediction_params = {'productPrice': 17.17}
        assert self.model_handler.get_prediction_parameters(prediction_params) == {'price':
                                                                                       prediction_params[
                                                                                           'productPrice']}

    def test_get_prediction_parameters_for_competitorPrice(self):
        prediction_params = {'competitorPrice': 17.17}
        assert self.model_handler.get_prediction_parameters(prediction_params) == {'competitor_price':
                                                                                       prediction_params[
                                                                                           'competitorPrice']}

    def mocked_mlflow_search_models_response(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
                self.content = json.dumps(self.json_data).encode("utf-8")

        if args[0] == 'databricks.host.com/api/2.0/preview/mlflow/runs/search':
            return MockResponse({
                "runs": [
                    {
                        "info": {
                            "run_uuid": "4",
                            "experiment_id": 1559542257869193,
                            "name": "",
                            "source_type": "LOCAL",
                            "source_name": "/source/name",
                            "user_id": "user@id.com",
                            "status": "FAILED",
                            "start_time": 1557399917600,
                            "end_time": 1557399945380,
                            "source_version": "",
                            "entry_point_name": "",
                            "artifact_uri": "dbfs:/databricks/mlflow/1559542257869193/0c5b2accf22c4bb287b5ca62b051b018/artifacts",
                            "lifecycle_stage": "active"
                        },
                        "data": {
                            "params": [
                                {
                                    "key": "string_param",
                                    "value": "value"
                                },
                                {
                                    "key": "float_param",
                                    "value": 2.5
                                }
                            ],
                            "tags": [
                            ]
                        }
                    },
                    {
                        "info": {
                            "run_uuid": "3",
                            "experiment_id": 1559542257869193,
                            "name": "",
                            "source_type": "LOCAL",
                            "source_name": "/source/name",
                            "user_id": "user@id.com",
                            "status": "FINISHED",
                            "start_time": 1557399917589,
                            "end_time": 1557399945371,
                            "source_version": "",
                            "entry_point_name": "",
                            "artifact_uri": "dbfs:/databricks/mlflow/1559542257869193/0c5b2accf22c4bb287b5ca62b051b018/artifacts",
                            "lifecycle_stage": "active"
                        },
                        "data": {
                            "params": [
                                {
                                    "key": "string_param",
                                    "value": "value"
                                },
                                {
                                    "key": "float_param",
                                    "value": 2.5
                                }
                            ],
                            "tags": [
                            ]
                        }
                    },
                    {
                        "info": {
                            "run_uuid": "2",
                            "experiment_id": 1559542257869193,
                            "name": "",
                            "source_type": "NOTEBOOK",
                            "source_name": "/notebook/path",
                            "user_id": "user@id.com",
                            "status": "FAILED",
                            "start_time": 1557054235768,
                            "end_time": 1557054325551,
                            "source_version": "",
                            "entry_point_name": "",
                            "artifact_uri": "dbfs:/databricks/mlflow/1559542257869193/0f6d60bae2054404aa9570f4f2c15378/artifacts",
                            "lifecycle_stage": "active"
                        },
                        "data": {
                            "tags": [
                            ]
                        }
                    },
                    {
                        "info": {
                            "run_uuid": "1",
                            "experiment_id": 1559542257869193,
                            "name": "",
                            "source_type": "LOCAL",
                            "source_name": "/source/name",
                            "user_id": "user@id.com",
                            "status": "FINISHED",
                            "start_time": 1557383609723,
                            "end_time": 1557383633706,
                            "source_version": "",
                            "entry_point_name": "",
                            "artifact_uri": "dbfs:/databricks/mlflow/1559542257869193/1537396aa51340a79ee280bbae9af9cf/artifacts",
                            "lifecycle_stage": "active"
                        },
                        "data": {
                            "params": [
                                {
                                    "key": "string_param",
                                    "value": "value"
                                },
                                {
                                    "key": "float_param",
                                    "value": 2.5
                                }
                            ],
                            "tags": [
                            ]
                        }
                    }]}, 200)

        return MockResponse(None, 404)

    @mock.patch('requests.post', side_effect=mocked_mlflow_search_models_response)
    def test_search_model(self, mock_post):
        parameters = {"string_param": "value", "float_param": 2.5}
        # it should return the latest run
        assert self.model_handler.search_model(parameters)['info']['run_uuid'] == '4'


if __name__ == '__main__':
    unittest.main()
