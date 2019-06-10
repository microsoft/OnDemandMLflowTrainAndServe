# Serving On demand Machine Learning Models utilizing MLflow

A sample for on-demand serving of Machine Learning models, using [MLFlow](https://docs.azuredatabricks.net/applications/mlflow/index.html) as the lifecycle platform and [Azure Databricks](https://docs.azuredatabricks.net/getting-started/index.html) for training models and hosting MLflow.

## Architecture

The sample consist of 3 separate services, that communicate over REST APIs. The services are deployed on an Azure Kubernetes Cluster.

![Architecture Diagram](images/architecture.png)

**[Prediction Service](prediction/README.md)**

**[Training Service](training/README.md)**

**[Model Runner](model-runner/REDAME.md)**

## How to run locally

## Deployment

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
