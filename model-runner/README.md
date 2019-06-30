# Model Runner Service

This service is responsible of all model serving aspects: searching for a model run, downloading, loading and getting a prediction.

## Prerequisite Requirements

-   docker with version 18.09 or up. Download and install from the following [link](https://docs.docker.com/)
-   python 3.7.3 or up from the following [link](https://www.python.org/downloads/)

### Environment Variables

To run the service the following env variables have to be defined:

```conf
MLFLOW_SERVER_API_PREFIX=<MLFlow api prefix. For example: /2.0/preview/mlflow>
MLFLOW_SERVER_SEARCH_PATH=<MLFlow runs search url path. For example: /runs/search>
MODELS_RELATIVE_PATH=<the model_path set in  mlflow.sklearn.log_model(forecast_model, "model_path")>
PORT=<Optional. This variable will affect what port the app will run on, for local=3000/production=80  >
MLFLOW_REQUESTS_TIMEOUT=<integer value for request to timeout when calling mlflow api>
MODEL_NAME=<Model name. For example: wine>
MLFLOW_EXPERIMENT_ID=<MLflow experiment id that the model runs are logged in>
DATABRICKS_HOST=<Databricks host>
DATABRICKS_TOKEN=<Databricks token>
```

MLflow api env variables should also be set according to the [MLflow Rest API documentation](https://www.mlflow.org/docs/latest/rest-api.html)

When running the service in a docker container, it is expected that the above env variables will be available.
The easiest way to do this will be to create env-file with the variables (just copy paste variables from the previous part into the file).

## Build and Run with Docker

```bash
docker build . -t model-runner-service
docker run --env-file=path/to/env-file -p 127.0.0.1:3000:3000 model-runner-service
```

## Setup Environment for Development

Install required packages:

-   Go to project's root directory
-   Install project requirements:

    ```sh
    pip3 install -r ./requirements.txt
    ```

-   Install additional development requirements:

    ```sh
    pip3 install -r ./requirements-dev.txt
    ```
