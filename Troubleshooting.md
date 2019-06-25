# Troubleshooting

This section will try to help you with a common error that is returned when asking for prediction and no successful trained model was not found.
In this case following message will be returned 'No successfully finished runs were found'.
To find the root cause for this error, check the following scenarios.

## Model Runner service configuration
-   Verify model runner service is up and running :
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
    kubectl get pod ${mypod} -oyaml
    ```
    - look for the env: section

    to show what's in effect, you can exec into the pod:

    ```bash
    kubectl exec ${mypod} -- sh -c env
    ```

    if those parameters are not defined correctly the model service will be looking for a model in a wrong experiment/databricks and etc.
## Training Service configuration

-   Verify training service is up and running :
    -   On Kubernetes cluster:
    ```bash
    kubectl get pods
    ```
    -   Locally:
    ```bash
    docker ps
    ```
-   on training service the following env variables configuration should be valid :
    -   DATABRICKS_WORKSPACE_URL=<Databricks Workspace URL. Example: https://westeurope.azuredatabricks.net>
    -   DATABRICKS_AUTH_TOKEN=<Authentication Token for Databricks>
    -   DATABRICKS_CLUSTER_ID=<Databricks cluster ID>
    -   DATABRICKS_TYPE_MAPPING=<Json including TYPE:NOTEBOOK_PATH, Example: "{\"MODEL\":\"/Users/user@domain.com/TYPES\"}">
    (see how to check the env variables values in the first section )
    if those parameters are not defined correctly the training service will train the model in a wrong databricks/notebook and etc.

## Databricks Notebook Execution
If the mlflow notebook run has failed those are the common scenarios:
-   Notebook parameters - verify parameters sent within request's json body have the same names and types as they are set in the notebook.
-   Other errors - Try running notebook manually with same parameters sent within request's json body and see if any error occurs
