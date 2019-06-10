# Model Handler Service

This service deals with all model serving aspects: searching for a model run, downloading , loading and getting a prediction.

# Prerequisite requirements

Install:

-   docker with version 18.09 or up. Download and install from the following [link](https://docs.docker.com/)
-   python 3.7.3 or up from the following [link](https://www.python.org/downloads/)

## Environment Variables

To run the service the following env variables have to be defined:

```bash
MLFLOW_SERVER_API_PREFIX=<MLFlow api prefix. For example: /2.0/preview/mlflow>
MLFLOW_SERVER_SEARCH_PATH=<MLFlow runs search url path. For example: /runs/search>
MODELS_RELATIVE_PATH=<the model_path set in  mlflow.sklearn.log_model(forecast_model, "model_path")>
ENVIRONMENT=<Not Required. Possible values are: local or production. This variable will affect what port the app will run on, for local=3000/production=80  >
MLFLOW_REQUESTS_TIMEOUT=<integer value for request to timeout when calling mlflow api>
MODEL_NAME=<Model name. For example: SALES>
MODEL_TRAINING_PARAMETERS=<Model parameters required for model training. It should be a string of parameter=type separated by a comma.For example: a string productId=string,competitorId=string,outlier=float,retailer=string>
MLFLOW_EXPERIMENT_ID=<MLflow experiment id that the model runs are logged in>
DATABRICKS_HOST=<Databricks host>
DATABRICKS_TOKEN=<Databricks token>
MODEL_PREDICTION_PARAMETERS_TRANSLATION=<Prediction parameters mapping between as they recieved in json and how they are expected on the model>
PREDICTION_PARAMETERS_TYPES=<Prediction parameters types mapping. For example: "date_param_name=date,string_param_name=string">
```

MLFlow api env variables should be set following the [MLFllow Rest API documentation](https://www.mlflow.org/docs/latest/rest-api.html)

When running the service in docker container the run will expect the following env variables to be passed.
The easy way will be to create env-file with the variables (just copy paste variables from the previous part into the file)

## Build and Run locally with docker

```bash
docker build . -t model-handler-service
docker run --env-file=path/to/env-file -p 127.0.0.1:3000:3000 model-handler-service
```

## Setup environment for development

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

# Troubleshooting

If the model is not found the following message will be returned 'No successfully finished runs were found'.
To find the root cause for this error, check the following scenarios:

-   Model Handler service configuration
    -   Verify model handler service is up and running :
        -   On Kubernetes cluster:
        ```bash
        kubectl get pods
        ```
        -   Locally:
        ```bash
        docker ps
        ```
    -   on model service verify the following env variables configuration :

        -   MLFLOW_SERVER_API_PREFIX
        -   MLFLOW_SERVER_SEARCH_PATH
        -   MODELS_RELATIVE_PATH
        -   MLFLOW_REQUESTS_TIMEOUT
        -   MODEL_TRAINING_PARAMETERS
        -   MLFLOW_EXPERIMENT_MAPPING
        -   DATABRICKS_HOST
        -   DATABRICKS_TOKEN
            to check env variables values locally (on a running docker container):

        ```bash
        docker exec container_name bash -c 'echo "$ENV_VAR"'
        ```

        to check env variables on a running kubernetes pod, the following command shows what was passed,
        you can look at the pod spec (like the docker command that was used to run it):

        ```bash
        kubectl get pod ${mypod} -oyaml - look for the env: section
        ```

        to show what's in effect, you can exec into the pod:

        ```bash
        kubectl exec ${mypod} -- sh -c env
        ```

        if those parameters are not defined correctly the model service will be looking for a model in a wrong experiment/databricks and etc.
-   Training Service configuration

    -   Verify training service is up and running :
        -   On Kubernetes cluster:
        ```bash
        kubectl get pods
        ```
        -   Locally:
        ```bash
        docker ps
        ```
    -   on training service verify the following env variables configuration :
        -   DATABRICKS_WORKSPACE_URL=<Databricks Workspace URL. Example: https://westeurope.azuredatabricks.net>
        -   DATABRICKS_AUTH_TOKEN=<Authentication Token for Databricks>
        -   DATABRICKS_CLUSTER_ID=<Databricks cluster ID>
        -   DATABRICKS_TYPE_MAPPING=<Json including TYPE:NOTEBOOK_PATH, Example: "{\"MODEL\":\"/Users/user@domain.com/TYPES\"}">
        (see how to check the env variables values in the first section )
        if those parameters are not defined correctly the training service will train the model in a wrong databricks/notebook and etc.

-   Notebook
    The notebook execution can fail for multiple reasons:
    -   Notebook parameters - verify parameters sent within request's json body have the same names and types as they are set in the notebook.
    -   Data Source - the data source in the UI and databricks should be the same
    -   Other errors - Try running notebook manually with same parameters sent within request's json body and see if any error occurs
