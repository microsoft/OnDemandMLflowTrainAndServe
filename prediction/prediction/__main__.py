import os
import logging
# pylint: disable=import-error
from app_config import training_service_config, mlflow_models_mapping, prediction_config
from prediction_service import PredictionService

prediction_service = PredictionService(training_service_config, mlflow_models_mapping, prediction_config)

if __name__ == '__main__':
    env = os.getenv('ENVIRONMENT')
    logging_level = os.getenv('LOG_LEVEL', logging.INFO)

    log = logging.getLogger('werkzeug')
    log.setLevel(logging_level)

    if env is None or env == 'production':
        prediction_service.run_flask_server(port=80, host='0.0.0.0')
    if env == 'local':
        prediction_service.run_flask_server(port=3000, host='0.0.0.0')
