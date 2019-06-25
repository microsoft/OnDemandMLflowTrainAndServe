import logging
# pylint: disable=import-error
from app_config import training_service_config, mlflow_models_mapping, service_config
from prediction_service import PredictionService

prediction_service = PredictionService(
    training_service_config, mlflow_models_mapping, service_config)

if __name__ == '__main__':
    logging_level = service_config['log_level']

    log = logging.getLogger('werkzeug')
    log.setLevel(logging_level)

    prediction_service.run_flask_server(port=service_config['port'], host='0.0.0.0')
