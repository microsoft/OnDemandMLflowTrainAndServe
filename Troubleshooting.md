# Troubleshooting

When requesting for a prediction you might receive back an error saying: 'No successfully finished runs were found'. This usually happens when the system cannot find a model that was successfully trained. This section will help you find the root cause for the error.

## Model Runner Service Configuration

-   Verify model runner service is up and running:

    -   On a Kubernetes cluster:

    ```bash
    kubectl get pods
    ```

    -   Locally:

    ```bash
    docker ps
    ```

-   Verify env variables configuration defined for the model runner service:

    -   MLFLOW_SERVER_API_PREFIX
    -   MLFLOW_SERVER_SEARCH_PATH
    -   MODELS_RELATIVE_PATH
    -   MLFLOW_REQUESTS_TIMEOUT
    -   MLFLOW_EXPERIMENT_MAPPING
    -   DATABRICKS_HOST
    -   DATABRICKS_TOKEN

    To check env variables values locally (on a running docker container):

    ```bash
    docker exec container_name bash -c 'echo "$ENV_VAR"'
    ```

    To check env variables on a running kubernetes pod, the following command shows the pod spec where you should review the 'env' section:

    ```bash
    kubectl get pod ${mypod} -oyaml
    ```

    You can also check from inside the pod what is in effect:

    ```bash
    kubectl exec ${mypod} -- sh -c env
    ```

    If those parameters are not defined correctly, the model service will be looking for a model in a wrong experiment/databricks etc.

## Training Service Configuration

-   Verify training service is up and running:

    -   On a Kubernetes cluster:

    ```bash
    kubectl get pods
    ```

    -   Locally:

    ```bash
    docker ps
    ```

-   Verify env variables configuration defined for the training service:

    -   DATABRICKS_WORKSPACE_URL
    -   DATABRICKS_AUTH_TOKEN
    -   DATABRICKS_CLUSTER_ID
    -   DATABRICKS_TYPE_MAPPING

    (see how to check the env variables values in the first section )
    If those parameters are not defined correctly the training service will train the model in a wrong databricks/notebook etc.

## Databricks Notebook Execution

If the MLflow notebook run has failed in Databricks, those are the common reasons:

-   Notebook parameters - verify that the parameters sent within request's json body have the same names and types in the notebook.
-   Other errors - Try running notebook manually with the same parameters sent within request's json body and see if any error occurs.
