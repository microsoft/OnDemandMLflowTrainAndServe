# Prediction Service

This service deals with all model serving aspects:  searching for a model run, downloading , loading and getting a prediction. 

# Prerequisite requirements

Install:
* docker with version 18.09 or up. Download and install from the following [link](https://docs.docker.com/)
* python 3.7.3 or up from the following [link](https://www.python.org/downloads/)

## Environment Variables

The project contains configuration needed for both mlflow and training service and it is sourced from env variables.
To run the service locally the following env variables have to be defined:

```bash
TRAINING_SERVICE_HOST=<Training service host>
TRAINING_SERVICE_PORT=<Training service port>
TRAINING_SERVICE_API_TRAIN_PATH=<training service api path to train and check status for models>
TRAINING_REQUESTS_TIMEOUT=<integer value for request to timeout when calling training service api>
MLFLOW_REQUESTS_TIMEOUT=<integer value for request to timeout when calling mlflow api>
SALES_MODEL_SERVICE_HOST=<Sales model serving host>
SALES_MODEL_SERVICE_PORT=<Sales model port>
PREDICTION_URL_PATH=<model handler service api path for prediction>
TRAINING_PAYLOAD_URL_PATH=<model handler service api path for recieving training payload for the model>
MODEL_SERVICE_REQUESTS_TIMEOUT=<integer value for request to timeout when calling model handler api>

```
When running the service in docker container the run will expect the following env variables to be passed.
The easy way will be to create env-file with the variables (just copy paste variables from the previous part into the file)

## Adding ML Model to requirements

In order to successfully build and run the Prediction service, there is a need to add the relevant ML Model (**.whl** file) to the build process:

1. Download the **.whl** file, and copy it to the root directory of the Prediction service (near the docker file).
1. Add the **.whl** file to the `requirements.txt` (or to `requirements-dev.txt` if needed)
    > **Note:** Instead of manually adding the .whl file to the requirements, you can run the `modify-requirements.sh` script, after copying the .whl file to the root directory, which automatically adds the .whl file to the both requirements files.

# Run on docker - local

docker build . -t {some tag name} -f ./Dockerfile_local  
detached : docker run --env-file=env-file -d {some tag name}  
interactive (recommended for debug): docker run -p 3000:5001 -it {some tag name}

# Run on docker - production

Using uWSGI and nginx for production  
docker build . -t {some tag name}  
detached : docker run --env-file=env-file -d {some tag name}  
interactive (recommended for debug): docker run -p 3000:80 -it {some tag name}

# Run on local computer

python -m venv env  
source env/bin/activate  
python -m pip install -r ./requirements.txt  
python main.py

# Setup environment for development

-   Install required packages:
    -   Go to project's root directory
    -   Install project requirements:
        ```sh
        pip3 install -r ./requirements.txt
        ```
    -   Install test and lint requirements:
        ```sh
        pip3 install -r ./requirements-dev.txt
        ```
