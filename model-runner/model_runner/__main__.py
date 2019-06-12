import os
# pylint: disable=no-name-in-module
from app_config import mlflow_config, service_config
from model_runner import ModelRunner

model_handler = ModelRunner(mlflow_config, service_config)

if __name__ == '__main__':
    env = os.getenv('ENVIRONMENT')
    if env is None or env == 'production':
        model_handler.run_flask_server(port=3003, host='0.0.0.0')
    if env == 'local':
        model_handler.run_flask_server(port=3003, host='0.0.0.0')
