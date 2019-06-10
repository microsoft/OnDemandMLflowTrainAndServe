mlflow_config = {
    'api_prefix': '/api/2.0/preview/mlflow',
    'search_path': '/runs/search',
    'mlflow_experiment_id': 121212,
    'databricks_token': 'token',
    'databricks_host': 'databricks.host.com',
    'models_relative_path': 'model_path',
    'model_name': 'ModelName',
    'timeout': 10,
    "model_training_parameters": {"string_param": "string", "float_param": "float"},
    "model_prediction_parameters_translation": {"date": "ds", "productPrice": "price",
                                                "competitorPrice": "competitor_price"},
    "prediction_parameters_types": {"date": "date", "productPrice": "int",
                                    "competitorPrice": "int"},
}
service_config = {
    "appinsights_key": "APP_INSIGHTS_INSTRUMENTATION_KEY",
    "service_name": "SERVICE_NAME"
}
