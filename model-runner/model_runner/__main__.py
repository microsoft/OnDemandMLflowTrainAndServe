import logging
# pylint: disable-msg=F0401
# pylint: disable=no-name-in-module
from app_config import mlflow_config, service_config
from model_runner import ModelRunner

model_handler = ModelRunner(mlflow_config, service_config)

if __name__ == '__main__':
    logging_level = service_config['log_level']

    log = logging.getLogger('werkzeug')
    log.setLevel(logging_level)

    model_handler.run_flask_server(port=service_config['port'], host='0.0.0.0')
