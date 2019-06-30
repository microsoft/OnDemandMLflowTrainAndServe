# Prediction Service

This service routes prediction requests to the right model-runner service. If no model is available to get a prediction from, it will ask for a new training or check for status if training is in progress.

## Prerequisite Requirements

-   docker with version 18.09 or up. Download and install from the following [link](https://docs.docker.com/)
-   python 3.7.3 or up from the following [link](https://www.python.org/downloads/)

### Environment Variables

To run the service the following env variables have to be defined:

```conf
TRAINING_SERVICE_HOST=<Training service host>
TRAINING_SERVICE_PORT=<Training service port>
TRAINING_SERVICE_API_TRAIN_PATH=<training service api path to train and check status for models>
TRAINING_REQUESTS_TIMEOUT=<integer value for request to timeout when calling training service api>
MLFLOW_REQUESTS_TIMEOUT=<integer value for request to timeout when calling mlflow api>
MLFLOW_MODELS_MAPPING=<Json String representing the models mapping>
```

An Example for MLFLOW_MODELS_MAPPING env var, where wine and diabetes are modelTypes:

```json
{
    "timeout": 1000,
    "wine": {
        "model_service_port": "3003",
        "model_service_host": "http://localhost"
    },
    "diabetes": {
        "model_service_port": "3004",
        "model_service_host": "http://localhost"
    }
}
```

When running the service in a docker container, it is expected that the above env variables will be available.
The easiest way to do this will be to create env-file with the variables (just copy paste variables from the previous part into the file).

## Build and Run with Docker

```bash
docker build . -t {some tag name} -f ./Dockerfile_local
```

detached:

```bash
docker run --env-file=env-file -d {some tag name}
```

interactive (recommended for debug):

```bash
docker run --env-file=env-file -p 3000:3000 -it {some tag name}
```

## Run on a Local Machine

```bash
python -m venv env
source env/bin/activate
python -m pip install -r ./requirements.txt
python main.py
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
