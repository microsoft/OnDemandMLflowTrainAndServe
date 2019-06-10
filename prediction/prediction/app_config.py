from environs import Env

env = Env()

training_service_config = {
    "host": env("TRAINING_SERVICE_HOST"),
    "port": env("TRAINING_SERVICE_PORT"),
    "api_train_path": env("TRAINING_SERVICE_API_TRAIN_PATH"),
    "timeout": env.int("TRAINING_REQUESTS_TIMEOUT"),
    "appinsights_key": env("APP_INSIGHTS_INSTRUMENTATION_KEY")
}

mlflow_models_mapping = {
    'SALES': {
        'model_service_host': env("SALES_MODEL_SERVICE_HOST"),
        'model_service_port': env("SALES_MODEL_SERVICE_PORT"),
    },
    'prediction_url_path': env("PREDICTION_URL_PATH"),
    'training_payload_url_path': env("TRAINING_PAYLOAD_URL_PATH"),
    "timeout": env.int("MODEL_SERVICE_REQUESTS_TIMEOUT")

}

prediction_config = {
    "service_name": env("SERVICE_NAME")
}
