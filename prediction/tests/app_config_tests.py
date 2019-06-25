training_service_config = {
    "host": 'http://training-host',
    "port": '3001',
    "api_train_path": '/train',
    "timeout": 1000,
    "appinsights_key": "APP_INSIGHTS_INSTRUMENTATION_KEY",
    "service_name": "model-handler"
}

mlflow_models_mapping = {
    'model-type': {
        'model_service_host': 'http://model-handler-host',
        'model_service_port': '3002',
    },
    'prediction_url_path': '/predict',
    'training_payload_url_path': '/training_payload',
    "timeout": 1000

}

service_config = {
    "service_name": "SERVICE_NAME"
}
