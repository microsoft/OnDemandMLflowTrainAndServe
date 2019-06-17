# Serving On demand Machine Learning Models utilizing MLflow

This sample demonstrates the use of [Azure Databricks](https://docs.azuredatabricks.net/getting-started/index.html) and [MLflow](https://docs.azuredatabricks.net/applications/mlflow/index.html) for on-demand training and serving of Machine Learning models, hosted in Databricks notebook.

The code in this repository allows a data scientist, that created an MLflow project, to test it with different parameters and later serve the model to get its prediction results based on the trained model.

> When running this sample, we assume a notebook is already loaded in Azure Databricks, and this notebook is using MLflow to store and log the experiments. This repository holds 2 [sample notebooks](./notebooks) (based on the samples provided by MLflow) you can use to get started.

## Architecture

The solution consists of 3 services deployed on an [Azure Kubernetes Service](https://azure.microsoft.com/en-in/services/kubernetes-service/). In this sample, the services communicate over REST APIs.

![Architecture Diagram](images/architecture.png)

**[Prediction Service](prediction/README.md)** is the entry point to the solution, navigating between issuing a train model request and running a model to receive the prediction results.

**[Training Service](training/README.md)** manages the requests to Databricks - starting a cluster and running a notebook to train an ML Model.

**[Model Runner](model-runner/README.md)** serves an MLflow model to return prediction request results.

### Solution User Flow

The entry point to the solution is the Prediction Service, with the /predict POST API.
The body of the request holds the required parameters to run an ML Model.

User requests a prediction based on an ML Model stored in databricks using the /predict API:

1. If a model with the same parameters as in the request parameters is already available in the MLFlow repository, the Model Runner serves the model and will return the result
2. If the model is not available for the requested parameters:
    1. Prediction service issues a request to the Training Service to train the model.
    2. Training model returns a **run id**, used to identify the request
    3. User issues a new /predict request, specifying the **run id** in timely intervals, until a response with status **COMPLETED** is returned. This response will hold the result of the model execution.

#### API body structure sample

```json
{
    "runId": null,
    "modelType": "WINE",
    "modelParameters": {
        "alpha": 0.36,
        "l1_ratio": "0.33"
    },
    "predictionParameters": {
        "alcohol": 12.8,
        "chlorides": 0.029,
        "citric_acid": 0.48,
        "density": 0.98,
        "fixed_acidity": 6.2,
        "free_sulfur_dioxide": 29,
        "pH": 3.33,
        "residual_sugar": 1.2,
        "sulphates": 0.39,
        "total_sulfur_dioxide": 75,
        "volatile_acidity": 0.66
    }
}
```

We've prepared a few sample API requests to run in postman, using the [sample notebooks](./notebooks) in this repository.

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/adc8703fb97388e41ded)

## Deployment

The application is deployed to a Kubernetes cluster using [Helm](https://helm.sh/docs/).

### Pre-requisites

In order to deploy the services to Kubernetes, please make sure the following components are installed and running:

-   Databricks cluster with a notebook for each model required to be trained
-   MLFlow available as a service in Databricks
-   Kubernetes cluster and Helm configured and ready for use
-   Docker images registry including the docker images of the services. **Here we assume that the docker images were built and pushed to the registry.**

### Configuration

Edit the [values.yaml](deployments\values.yaml) file with the values of the parameters.

> For more information about each service parameters, please refer to the service readme file

### Running Helm

After setting the values in the `values.yaml` file:

-   Open the command line
-   Change directory (cd) to the [deployments](./deployments) directory
-   Run the following command:

    ```bash
    helm install ShortLivedMLModels -f ShortLivedMLModels\values.yaml --name=demo
    ```

This will deploy the services into the Kubernetes cluster.

Please note that the Prediction service is the entry point of this application, so it is set to type `LoadBalancer`, and this will grant it a public IP address.

#### Updating the application in Kubernetes

If there is a need to make changes to any of the values in the `values.yaml`, make the changes and run the following command:

```bash
helm upgrade demo ShortLivedMLModels --recreate-pods --reset-values --force --values ShortLivedMLModels\values.yaml
```

You can also set the values that you need to change inline, by adding `--set var1=value1,var2=value2` to the end of the command.

> More detailed information about Helm commands can be found in [Helm documentation](https://helm.sh/docs/helm/#helm-install).

## Contributing

This project welcomes contributions and suggestions. Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
