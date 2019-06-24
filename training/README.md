# Training Service

Training Service is responsible to communicate with a third party service to train a new ML model.

In our case, we are using Azure Databricks. Using other third party will require an implementation change for the training service.

## Request Flows

### New Training request

New requests for training are treated with the following steps:

1. A new request (POST) for a training is coming with the following data structure in the body:

    ```json
    {
        "modelType": "MODEL",
        "parameters": {
            // Parameters key-values
        }
    }
    ```

1. Retrieve the notebook path in Databricks according to the `modelType` (which in our case is 'MODEL').
    > Note: `modelType` -> 'Databricks notebook path' mappings are described in the json value of the `DATABRICKS_TYPE_MAPPING` environment variable.
1. Start the Databricks cluster if it is in 'TERMINATED' state.
1. Send a request to the Databricks to run the notebook with the specified parameters.
1. The response from Databricks will include `runId`, and will be returned in the response json in the following structure:

    ```json
    {
        "runId": 123
    }
    ```

### Get Run Status request

1. A new request for run status is coming with `runId` in the request path. Example: `GET /123`

1. The response from Databricks will include `state` and `message`, and will be returned in the response json in the following structure:

    ```json
    {
        "state": "<Run Status>",
        "message": "<Run Message>"
    }
    ```

    - **'Run Status'** could be one of the following values: `pending`, `running` or `completed`
    - **'Run Message'** is generally empty, but will include error message if the run finishes unsuccessfully.

## Environment Variables

The service expects several environment variables to be set in order to run:

| Var                              | Required | Description                                                                                                                                |
| -------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| PORT                             | yes      | Service port. default=80                                                                                                                   |
| DATABRICKS_WORKSPACE_URL         | yes      | Databricks Workspace URL                                                                                                                   |
| DATABRICKS_AUTH_TOKEN            | yes      | Authentication Token for Databricks                                                                                                        |
| DATABRICKS_CLUSTER_ID            | yes      | Databricks cluster ID. More information can be found [here](https://docs.databricks.com/user-guide/faq/workspace-details.html#cluster-url) |
| DATABRICKS_RUN_TIMEOUT           | yes      | Run timeout for notebook runs                                                                                                              |
| DATABRICKS_TYPE_MAPPING          | yes      | Json including MODEL:NOTEBOOK_PATH mapping                                                                                                 |
| NODE_ENV                         | no       | **test** for unit testing                                                                                                                  |
| APP_INSIGHTS_INSTRUMENTATION_KEY | no       | Application Insights instrumentation key                                                                                                   |
| SERVICE_NAME                     | no       | service name for Application Insights logging                                                                                              |

### Sample environment variables

```conf
PORT=3000
DATABRICKS_WORKSPACE_URL=https://westeurope.azuredatabricks.net
DATABRICKS_AUTH_TOKEN=abcdefghi123456a123a1234a123456abc12
DATABRICKS_CLUSTER_ID=1234-123456-hurts123
DATABRICKS_RUN_TIMEOUT=3600
DATABRICKS_TYPE_MAPPING={"wine":"/shared/wine_notebook","diabetes":"/shared/diabetes_notebook"}
APP_INSIGHTS_INSTRUMENTATION_KEY=01e9c546-1234-1234-cf56-7d6b49fc053a
SERVICE_NAME=training
```

## Build and Run locally with docker

```bash
docker build . -t training-service
docker run --env-file=.env-file -p 127.0.0.1:3000:3000 training-service
```
