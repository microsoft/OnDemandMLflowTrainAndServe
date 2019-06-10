from environs import Env

env = Env()

# validate env vars
env.url('DATABRICKS_HOST')

mlflow_config = {
    'api_prefix': env("MLFLOW_SERVER_API_PREFIX"),
    'search_path': env("MLFLOW_SERVER_SEARCH_PATH"),
    'mlflow_experiment_id': str(int(env.float(("MLFLOW_EXPERIMENT_ID")))),
    'databricks_token': env('DATABRICKS_TOKEN'),
    'databricks_host': env('DATABRICKS_HOST'),
    'models_relative_path': env('MODELS_RELATIVE_PATH'),
    'model_name': env('MODEL_NAME'),
    "timeout": env.int("MLFLOW_REQUESTS_TIMEOUT"),
    "model_training_parameters": env.dict("MODEL_TRAINING_PARAMETERS"),
    "model_prediction_parameters_translation": env.dict("MODEL_PREDICTION_PARAMETERS_TRANSLATION"),
    "prediction_parameters_types": env.dict("PREDICTION_PARAMETERS_TYPES")

}

service_config = {
    "appinsights_key": env("APP_INSIGHTS_INSTRUMENTATION_KEY"),
    "service_name": env("SERVICE_NAME")
}
