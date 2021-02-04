# Azure + Azure Dev Ops Pipelines + Pulumi Example

Example of [Azure AKS](https://docs.microsoft.com/en-us/azure/aks/) with [Pulumi](https://www.pulumi.com/) (in python) usage.  
Docker images stored in [Azure container registry](https://azure.microsoft.com/en-us/services/container-registry/).  
Used pipelines in [Azure Dev Ops](https://azure.microsoft.com/en-us/services/devops/).  

Used [Helm](https://helm.sh/) charts for [mongoDB](https://github.com/bitnami/charts/tree/master/bitnami/mongodb) and [NGINX Ingress](https://github.com/helm/charts/tree/master/stable/nginx-ingress).  
Includes also a simple [Spring Boot](https://spring.io/projects/spring-boot) application.  

## Spring Boot application
Created a very simple spring boot application to show rolling updates with Azure pipelines/Kubernetes and ingress usage.    
Contains three endpoints:  
* `GET /` - returns String "TEST" (Can be simply changed and when changes are pushed, the image should be updated and a new value should be returned)  
* `GET /user/` - returns list of Users in the MongoDB database  
* `POST /user?username=(username)` - creates a user with the given username  

MongoDB properties in `application.properties` are configured to use environment variables that are configured in a pipeline.  

## Pulumi
Created two Pulumi projects, which create the following resources:  
  
basic:
 - namespace
 - NGINX Ingress resources (defined in Helm) 
 - storage class
 - persistent volume claim (for MongoDB)
 - MongoDB resources (defined in helm)  
 
demo-app:
 - simple spring boot application deployment
 - service for the application
 - ingress for the application

Projects contain a lot of environment variables usage, so they can be easily configured in Azure Pipelines.  
Used v2 of Helm package as v3 has problems with Helm hooks  
https://github.com/pulumi/pulumi-kubernetes/issues/555

## Pipelines

Pulumi:  
Pipelines that executes `pulumi up`. Used for both Pulumi projects (environment variables differ)  
I used Pulumi task and Pulumi script in a console. Pulumi script was used to create a new stack if it doesn't exist. I couldn't do that in task as the Pulumi task assumes that the stack already exists. I used a Pulumi task for `pulumi up` as Pulumi in a script has problems with environment variables. Because of that, I needed to use two different env variables that Pulumi needs for authentication (PULUMI_ACCESS_TOKEN and pulumi.access.token. One is used by Pulumi task the other one is used by `pulumi login`)  
Used AzureCLI task to log in as azureSubscription parameter did not work with Pulumi task.  
  
`env` had to be defined for a script to use a secret env variable:  
```
  env:
    PULUMI_ACCESS_TOKEN: $(PULUMI_ACCESS_TOKEN)
```
  
`|| true` was used in `pulumi stack init` script to ignore errors.  
I did not use `continueOnError` as it displays a warning even that pipeline should be considered fully successful.

Docker build push rolling update:
Pipeline builds a Docker image, pushes it to Docker repository, creates image secret, and performs rolling update to update current deployment with new image (using secret created in previous step)  
Pipeline is executed on any change in the repository. Thanks to that, any changes in the spring boot application are deployed instantly when the code on the master branch changes.

## Guide

### Azure Account
[Create an Azure account or log in to an existing one](https://azure.microsoft.com/auth/signin/?loginProvider=Microsoft&redirectUri=%2Fpl-pl%2F)

#### How to use a free trial:
Go to `Subscriptions`  
![Screenshot_20210203_194509](https://user-images.githubusercontent.com/15820051/106794511-3c9d5b00-6659-11eb-9aa3-88335a4f459d.png)  
and add a new one, then select `Free Trial` offer and fill data as requested. 

### Pulumi
[Create a Pulumi account or log in into an existing one](https://app.pulumi.com/signin)  
In settings generate a new access token and save it somewhere.  
![image](https://user-images.githubusercontent.com/15820051/106800741-2a271f80-6661-11eb-837b-6b4012c596a8.png)  
[Add Pulumi Azure Pipeline task to Azure](https://marketplace.visualstudio.com/items?itemName=pulumi.build-and-release-task)  
[Install Pulumi (Optional)](https://www.pulumi.com/docs/get-started/install/)  


### Setup Kubernetes cluster
Go to `Kubernetes services` and add a new Kubernetes cluster.  
While creating the cluster, add a new resource group while clicking `Create new`.  
Go to the `Integrations` tab and create a new container registry with `Create new`.  
If you are using a free trial account, change `node count` to 1.  
All the other settings can be left as the default ones.  
![image](https://user-images.githubusercontent.com/15820051/106795693-ad914280-665a-11eb-9f3b-b151b17b0cf3.png)  
![image](https://user-images.githubusercontent.com/15820051/106796891-407eac80-665c-11eb-902a-17f8b5352be5.png)  

### Kubectl and Azure
[Install and Set Up Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)  
[Install Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-linux?pivots=apt)  
Login to Azure from CLI: `az login`  
*In case of any problems, go to Azure Active Directory, copy Tenant ID and use id while logging: az login --tenant 6f643342-abc3-226g-(...)*  
![image](https://user-images.githubusercontent.com/15820051/106805460-0070f700-6667-11eb-8611-e122a129569b.png)  
Save az credentials in kubectl config:  
`az aks get-credentials --resource-group test-resource-group --name cluster-test`  
(Replace `test-resource-group` with your resource group and `cluster-test` with your cluster name)   
   
Switch kubectl context:  
`kubectl config use-context test-cluster`  
(Replace `test-cluster` with your cluster name)

### Setup Azure DevOps
Go to [Azure dev](https://dev.azure.com/) and create a new project.  
![image](https://user-images.githubusercontent.com/15820051/106797141-876ca200-665c-11eb-8627-1557ce4900c1.png)  
Go to `Repos` and get HTTPS (or SSH) URL for the repository.  
![image](https://user-images.githubusercontent.com/15820051/106797492-f6e29180-665c-11eb-90f7-6913026993b5.png)  
Clone the repository locally, copy files from my repository and push those files.  
![image](https://user-images.githubusercontent.com/15820051/106797815-6789ae00-665d-11eb-987b-4ebf65f1dc31.png)  
Go to `Project settings`  
![image](https://user-images.githubusercontent.com/15820051/106797943-92740200-665d-11eb-980e-36ccba314a37.png)  
`Service connections` in `Pipelines`, create a `Docker Registry` and `Azure resource manager`(Service principal) connections.   
![image](https://user-images.githubusercontent.com/15820051/106798185-f0084e80-665d-11eb-9743-76457d1475ba.png)   
![image](https://user-images.githubusercontent.com/15820051/106799610-bfc1af80-665f-11eb-8400-59283287e720.png)   
Go to `Environments` and create a new one  
![image](https://user-images.githubusercontent.com/15820051/106809473-03221b00-666c-11eb-8134-509d2829f778.png)   
![image](https://user-images.githubusercontent.com/15820051/106809535-1634eb00-666c-11eb-90c4-454c1beea9d1.png)   
![image](https://user-images.githubusercontent.com/15820051/106809612-2e0c6f00-666c-11eb-97b9-11980bb403f4.png)   

### Pipelines

**Pipeline to build, push Docker image and perform rolling update of demo application**  
Go to Pipelines and create a new one.  
Select Azure Repos Git and repository created before as the place with your code.  
In `Configure` step select `Existing Azure Pipeline YAML file` and in `path` select: `/pipelines/docker-build-push-rolling-update.yml`.  

Now configure Variables  
![image](https://user-images.githubusercontent.com/15820051/106798640-89cffb80-665e-11eb-9680-1b57e3919ed0.png)  

| Name                        | Description                                                                                                                                       | Example value                                              |
|-----------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------|
| docker_registry_repository  | Docker registry repository path, generated while creating a Kubernetes cluster                                                                    | mateuszwlosektestregistry                                   |
| image_name                  | Docker image name. You can type anything                                                                                                          | test-cluster                                               |
| docker_registry_connection  | Docker registry connection created above                                                                                                          | docker-registry-service-connection                         |
| image_pull_secret           | Docker image pull secret name. Any value                                                                                             | docker-registry-image-pull-secret                          |
| kubernetes_environment      | Environment created above                                                                                                                         | test-environment                                           |
| kubernetes_service_endpoint | Service connection to Kubernetes. Should be created automatically after creating environment. Look for it in Project Settings/Service Connections | test-environment-test-cluster-demo-namespace-1612386451573 |
| namespace                   | Namespace name                                                                                                                                    | demo-namespace                                             |

Save changes (Don't execute pipeline from here as it will not be possible to select required parameters.  
Go to pipelines and execute saved pipeline, in `Stages to run` select only `Build`.   
Rename the pipeline to: `Build image, Deploy image, Perform rolling update`  

**Pipeline to create a basic infrastructure (namespace, ingress service, storage, MongoDB)**
Go to Pipelines and create a new one.  
Select Azure Repos Git and repository created before as the place with your code.  
In `Configure` step select `Existing Azure Pipeline YAML file` and in `path` select: `/pipelines/pulumi-pipeline.yml`.  

Variables:
| Name                  | Description                                                                                   | Example value                             |
|-----------------------|-----------------------------------------------------------------------------------------------|--------------------------------------|
| azure_subscription    | Azure resource manager connection created above                                               | azure-service-connection             |
| cluster_name          | Kubernetes cluster name                                                                       | test-cluster                         |
| mongodb_database      | Mongodb database name. Any value                                                  | master                               |
| mongodb_username      | Mongodb username. Any value                                                       | test                                 |
| mongodb_password      | Mongodb password. Any value                                                       | test                                 |
| namespace_name        | Namespace name. Any value                                                         | demo-namespace                       |
| pip_requirements_path | Path to requirements for pip. If repositories files were not changed value has to be the same as in the example                                       | pulumi/basic/requirements            |
| PULUMI_ACCESS_TOKEN   | Pulumi token, generated after in Pulumi settings. You can keep this value secret                                               | pul-8e8kcaj95h86g10dec4dx1f7w18s20fb2ga66894 |
| pulumi.access.token   | Same token as in PULUMI_ACCESS_TOKEN (Two env variables are needed) | pul-8e8kcaj95h86g10dec4dx1f7w18s20fb2ga66894  | 
| pulumi_directory      | Directory with Pulumi files. If repositories files were not changed value has to be the same as in the example                                         | pulumi/basic/                        |
| pulumi_stack          | Pulumi stack name. Any value                                                      | demo-stack                           |
| resources_group_name  | Resources group name. Generated when Kubernetes cluster was created.                          | test-resource-group                  | 

Save changes and run the pipeline.  
Rename the pipeline to: `Pulumi basic infrastructure up`

**Pipeline to deploy a demo application exposed outside (spring boot application, service, ingress)**  
Go to Pipelines and create a new one.  
Select Azure Repos Git and repository created before as the place with your code.   
In `Configure` step select `Existing Azure Pipeline YAML file` and in `path` select: `/pipelines/pulumi-pipeline.yml`.  

Variables: 
| Name                       | Description                                                                                                                                                                            | Example value                                  |
|----------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------|
| azure_subscription         | Azure resource manager connection created above                                                                                                                                        | azure-service-connection                  |
| cluster_name               | Kubernetes cluster name                                                                                                                                                                | test-cluster                              |
| demo_port                  | Demo application port. If application properties were not changed value has to be the same as in the example                                                                                                                                       | 8080                                      |
| docker_registry_repository | Docker registry repository path. In Azure go to container registries, select the one you want to use, and copy `Login server` value / repository image name used in env variables above | mateuszwlosektestregistry.azurecr.io/demo |
| image_pull_secret          | Docker image pull secret name. Have to be the same as in variables given above                                                                                                       | docker-registry-image-pull-secret         |
| mongodb_database           | MongoDB database name Have to be the same as in variables given above                                                                                                                 | master                                    |
| mongodb_username           | MongoDB username Have to be the same as in variables given above                                                                                                                    | test                                      |
| mongodb_password           | MongoDB password Have to be the same as in variables given above                                                                                                                   | test                                      |
| mongodb_host               | MongoDB service name. If Pulumi files were not changed value has to be the same as in the example                                                                                                                                        | mongodb                                   |
| namespace_name             | Namespace name. If Pulumi files were not changed value has to be the same as in the example                                                                                                                      | demo-namespace                            |
| pip_requirements_path      | Path to requirements for pip. If repositories files were not changed value has to be the same as in the example                                                                                                                                | pulumi/demo-app/requirements              |
| PULUMI_ACCESS_TOKEN        | Pulumi token, generated after in Pulumi setting. You can keep this value secret                                                                                                                                        | pul-8e8kcaj95h86g10dec4dx1f7w18s20fb2ga66894      |
| pulumi.access.token        | Same token as in PULUMI_ACCESS_TOKEN (Two env variables are needed)                                                                                          | pul-8e8kcaj95h86g10dec4dx1f7w18s20fb2ga66894      |
| pulumi_directory           | Directory with pulumi files. Any value                                                                                                                                  | pulumi/demo-app/                          |
| pulumi_stack               | Pulumi stack name. Any value                                                                                                                                               | demo-stack                                |
| resources_group_name       | Resources group name. Generated when Kubernetes cluster was created                                                                                                                   | test-resource-group                       |

Save changes and run the pipeline.  
Rename the pipeline to: `Pulumi demo app up`  

You can check the environment now in Azure webpage or in CLI.  

**When anything is changed in the repository, the pipeline with rolling update will be executed automatically. It's an example of how to deploy changes automatically when e.g demo application in this case is changed.**  

### Kubectl useful commands:  
Switch Kubernetes namespace: `kubectl config set-context --current --namespace=demo-namespace` (Replace `demo-namespace` with your namespace, set in environment variables above)  
Switch Kubernetes context: `kubectl config use-context cluster-test` (Replace `demo-namespace` with your context)
Check Kubernetes deployments: `kubectl get deployment`  
Check Kubernetes pods: `kubectl get pods`  
Check Kubernetes pods from all namespaces: `kubectl get pods --all-namespaces`
Check Kubernetes services: `kubectl get services`  
Describe a resource: `kubectl describe deployment mongodb`  
Check pod logs: `kubectl get logs mongodb-7c9986b5c-26bdv -f` (Replace with your pod name)  
Check YAML of a resource: `kubectl get deployment mongodb -o yaml`  
Delete a resource: `kubectl delete deployment demo` (If another resource is depending on this resource, deletion may not work)  

### Test demo application:  
Get external IP: `kubectl get services`, service: `nginx-ingress-ingress-nginx-controller`.  
Test endpoint: `curl 'http://1.2.3.4` (replace IP with your one)  
Get users endpoint: `curl 'http://1.2.3.4/user'` (replace IP with your one)  
Create users endpoint: `curl -X POST 'http://1.2.3.4/user?username=test'` (replace IP with your one) 

### Pulumi useful commands:  
Cancel ongoing Pulumi process: `pulumi cancel`  
**In case of any errors with corrupted Pulumi state**: `pulumi cancel`, `pulumi stack export | pulumi stack import`, and `pulumi refresh`  
