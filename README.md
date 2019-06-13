# Serving On demand Machine Learning Models utilizing MLflow

A sample for on-demand serving of Machine Learning models, using [MLFlow](https://docs.azuredatabricks.net/applications/mlflow/index.html) as the lifecycle platform and [Azure Databricks](https://docs.azuredatabricks.net/getting-started/index.html) for training models and hosting MLflow.

## Architecture

The sample consists of 3 separated services, that communicate over REST APIs. The services are deployed on an Azure Kubernetes Cluster.

![Architecture Diagram](images/architecture.png)

**[Prediction Service](prediction/README.md)**

**[Training Service](training/README.md)**

**[Model Runner](model-runner/README.md)**

## How to run locally

Look at each service's readme to learn how to run it locally.

## Deployment

In this sample we are using Helm chart to deploy the application to Kubernetes.

### Pre-requisites

In order to deploy the services to Kubernetes, please make sure the following components are installed and running:

- Databricks cluster with a notebook for each training model
- MLFlow
- Kubernetes cluster and Helm configured and ready for use
- Docker images registry including the docker images of the services. **Here we assume that the docker images were built and pushed to the registry.**

### Configuration

Open the [values.yaml](deployments\values.yaml) file, and set the values of the parameters.

> For more information about each service parameters, please refer to the service's readme.

### Running Helm

After setting the values in the `values.yaml` file:

- Open the command line
- Change directory (cd) to the **deployments** directory
- Run the following command:

    ```bash
    helm install ShortLivedMLModels -f ShortLivedMLModels\values.yaml --name=demo
    ```

This will deploy the services into the Kubernetes cluster.

Please note that the Prediction service is the entry point of this application, so it is set to type `LoadBalancer`, and this will grant it a public IP address. To get this IP address, you can run the following command, and see the **EXTERNAL-IP** value in the `training-service` row.

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
