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

    def test_build_prediction_payload_with_model_params(self):
        model_params = {"string_param": "value", "int_param": 1}
        assert \
            self.model_handler.build_prediction_payload(model_params) == {'experiment_ids': [121212],
                                                                          'filter':
                                                                              "params.string_param = 'value' and params.int_param = 1"
                                                                          }

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
