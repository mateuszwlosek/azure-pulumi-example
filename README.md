# Azure + Pulumi Example

## Guide

### Azure Account
[Create an azure account or log in into an existing one](https://azure.microsoft.com/auth/signin/?loginProvider=Microsoft&redirectUri=%2Fpl-pl%2F)

#### How to use a free trial:
Go to `Subscriptions`  
![Screenshot_20210203_194509](https://user-images.githubusercontent.com/15820051/106794511-3c9d5b00-6659-11eb-9aa3-88335a4f459d.png)  
and add a new one, then select `Free Trial` offer and fill data as requested. 

### Pulumi
[Create a pulumi account or log in into an existing one](https://app.pulumi.com/signin)  
In settings generate new access token and save it somewhere  
![image](https://user-images.githubusercontent.com/15820051/106800741-2a271f80-6661-11eb-837b-6b4012c596a8.png)
[Install Pulumi (Optional)](https://www.pulumi.com/docs/get-started/install/)

### Setup Kubernetes cluster
Go to `Kubernetes services` and add a new Kubernetes cluser.  
While creating the cluster, add a new resource group while clicking `Create new`.  
Go to the `Integrations` tab and create a new container registry with `Create new`.  
If you are using a free trial account, change `node count` to 1
All the other settings can be left as the default ones.  
![image](https://user-images.githubusercontent.com/15820051/106795693-ad914280-665a-11eb-9f3b-b151b17b0cf3.png)  
![image](https://user-images.githubusercontent.com/15820051/106796891-407eac80-665c-11eb-902a-17f8b5352be5.png)  

### Kubectl and Azure
[Install and Set Up Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
[Install Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-linux?pivots=apt)
Login to azure from CLI: `az login`  
*In case of any problems, go to Azure Active Directory, copy Tenant ID and use id while logging: az login --tenant 6f643342-abc3-226g-(...)*  
![image](https://user-images.githubusercontent.com/15820051/106805460-0070f700-6667-11eb-8611-e122a129569b.png)  
Save az credentials in kubectl config: `az aks get-credentials --resource-group test-resource-group --name cluster-test` (Replace `test-resource-group` with your resource group and `cluster-test` with your cluster name)  
Switch kubectl context: `kubectl config use-context test-cluster` (Replace `test-cluster` with your cluster name)

### Setup Azure DevOps
Go to [Azure dev](https://dev.azure.com/) and create a new project  
![image](https://user-images.githubusercontent.com/15820051/106797141-876ca200-665c-11eb-8627-1557ce4900c1.png)  
Go to `Repos` and get HTTPS (or SSH) url for the repository  
![image](https://user-images.githubusercontent.com/15820051/106797492-f6e29180-665c-11eb-90f7-6913026993b5.png)  
Clone the repository locally, copy files from my repository and push those files.  
![image](https://user-images.githubusercontent.com/15820051/106797815-6789ae00-665d-11eb-987b-4ebf65f1dc31.png)  
Go to `Project settings`  
![image](https://user-images.githubusercontent.com/15820051/106797943-92740200-665d-11eb-980e-36ccba314a37.png)  
`Service connections` in `Pipelines`, create a `Docker Registry` and `Azure resource manager`(Service principal) connections   
![image](https://user-images.githubusercontent.com/15820051/106798185-f0084e80-665d-11eb-9743-76457d1475ba.png)   
![image](https://user-images.githubusercontent.com/15820051/106799610-bfc1af80-665f-11eb-8400-59283287e720.png)   
Go to environments and create a new one  
![image](https://user-images.githubusercontent.com/15820051/106809473-03221b00-666c-11eb-8134-509d2829f778.png)   
![image](https://user-images.githubusercontent.com/15820051/106809535-1634eb00-666c-11eb-90c4-454c1beea9d1.png)   
![image](https://user-images.githubusercontent.com/15820051/106809612-2e0c6f00-666c-11eb-97b9-11980bb403f4.png)   


#### Pipelines
Go to `Pipelines` and create a new one.  
Select `Azure Repos Git` and repository created before as the place with your code. 

**Pipeline to build, push docker image and perform rolling update of demo application**  
In `Configure` step select `Existing Azure Pipeline YAML file` and in `path` select: `/pipelines/docker-build-push-rolling-update.yml`.  

Now configure Variables  
![image](https://user-images.githubusercontent.com/15820051/106798640-89cffb80-665e-11eb-9680-1b57e3919ed0.png)  

Name: docker_registry_repository  
Description: Docker registry repository path, generated while creating a kubernetes cluster  
My value: mateuszwlosektestregistry  

Name: image_name  
Description: Docker image name. You can type anything   
My value: test-cluster  

Name: docker_registry_connection  
Description: Docker registry connection created above  
My value: docker-registry-service-connection  

Name: image_pull_secret   
Description: Docker image pull secret name. You can type anything   
My value: docker-registry-image-pull-secret   

Name: kubernetes_environment  
Description: Environment created above  
My value: test-environment  

Name: kubernetes_service_endpoint  
Description: Service connection to kubernetes. Should be created automatically after creating environemnt. Look for it in Project Settings/Service Connections  
My value: test-environment-test-cluster-demo-namespace-1612386451573  

Name: namespace  
Description: Namespace name (Have to be the same as in variables given above)   
My value: demo-namespace  

Save changes (Don't execute pipeline from here as it will not be possible to select required parameters.  
Go to pipelines and execute saved pipeline, in `Stages to run` select only `Build`.   
Rename the pipeline to: Build image, Deploy image, Perform rolling update  

**Pipeline to create a basic infrastructure (namespace, ingress service, storage, mongodb)**  
In `Configure` step select `Existing Azure Pipeline YAML file` and in `path` select: `/pipelines/pulumi-pipeline.yml`.  

Variables:

Name: azure_subscription  
Description: Azure resource manager connection created above   
My value: azure-service-connection  

Name: cluster_name  
Description: Kubernetes cluster name  
My value: test-cluster  

Name: mongodb_database  
Description: Mongodb database name. You can type anything  
My value: master  

Name: mongodb_username  
Description: Mongodb username. You can type anything   
My value: test  

Name: mongodb_password  
Description: Mongodb password. You can type anything   
My value: test  

Name: namespace_name  
Description: Namespace name. You can type anything  
My value: demo-namespace  

Name: pip_requirements_path  
Description: Path to requirements for pip. Type the same value as I.  
My value: pulumi/basic/requirements  

Name: PULUMI_ACCESS_TOKEN  
Description: Pulumi token, generated after in Pulumi settings  
My value: pul-(... I won't share pulumi token)   

Name: pulumi.access.token  
Description: Same token as in the variable above (yes, two env variables are needed. I explained it above)  
My value: pul-(... I won't share pulumi token)   

Name: pulumi_directory  
Description: Directory with pulumi files. Type the same value as I  
My value: pulumi/basic/  

Name: pulumi_stack  
Description: Pulumi stack name. You can type anything  
My value: demo-stack  

Name: resources_group_name  
Description: Resources group name. Generated when kubernetes cluster was created.  
My value: test-resource-group  

Save changes and run the pipeline.  
Rename the pipeline to: Pulumi basic infrastructure up

**Pipeline to deploy a demo application exposed outside (spring boot application, service, ingress)**  
In `Configure` step select `Existing Azure Pipeline YAML file` and in `path` select: `/pipelines/pulumi-pipeline.yml`.  

Variables:  

Name: azure_subscription  
Description: Azure resource manager connection created above  
My value: azure-service-connection  

Name: cluster_name  
Description: Kubernetes cluster name  
My value: test-cluster  

Name: demo_port  
Description: Demo application port. Type the same value as I.
My value: 8080

Name: docker_registry_repository   
Description: Docker registry repository path. In azure go to container registries, select the one you want to use and copy `Login server` value / repository image name used in env variables above  
My value: mateuszwlosektestregistry.azurecr.io/demo  

Name: image_pull_secret   
Description: Docker image pull secret name. (Have to be the same as in variables given above)   
My value: docker-registry-image-pull-secret   

Name: mongodb_database   
Description: Mongodb database name (Have to be the same as in variables given above)   
My value: master  

Name: mongodb_username  
Description: Mongodb username (Have to be the same as in variables given above)   
My value: test   

Name: mongodb_password  
Description: Mongodb password (Have to be the same as in variables given above)   
My value: test   

Name: mongodb_host    
Description: Mongodb service name. Type the same value as I.  
My value: mongodb  

Name: namespace_name  
Description: Namespace name (Have to be the same as in variables given above)  
My value: demo-namespace   

Name: pip_requirements_path  
Description: Path to requirements for pip. Type the same value as I.  
My value: pulumi/demo-app/requirements   

Name: PULUMI_ACCESS_TOKEN   
Description: Pulumi token, generated after in Pulumi settings   
My value: pul-(... I won't share pulumi token)   

Name: pulumi.access.token   
Description: Same token as in the variable above (yes, two env variables are needed. I explained it above)   
My value: pul-(... I won't share pulumi token)   

Name: pulumi_directory  
Description: Directory with pulumi files. Type the same value as I  
My value: pulumi/demo-app/  

Name: pulumi_stack  
Description: Pulumi stack name. You can type anything   
My value: demo-stack  

Name: resources_group_name  
Description: Resources group name. Generated when kubernetes cluster was created.  
My value: test-resource-group  

Save changes and run the pipeline.  
Rename the pipeline to: Pulumi demo app up  

You can check the environment now in Azure UI or in CLI.  

**When anything is changed in repo, pipeline with rolling update will be executed automatically. It's an example of how to deploy changes automatically when e.g demo application in this case is changed.**  

Kubectl useful commands:  
Switch kubernetes namespace: `kubectl config set-context --current --namespace=demo-namespace` (Replace `demo-namespace` with your namespace, set in environment variables above)  
Check kubernetes deployments: `kubectl get deployment`  
Check kubernetes pods: `kubectl get pods`  
Check kubernetes services: `kubectl get services`  
Describe a resource: `kubectl describe deployment mongodb`  
Check pod logs: `kubectl get logs mongodb-7c9986b5c-26bdv -f` (Replace with your pod name)  
Check yaml of a resource: `kubectl get deployment mongodb -o yaml`  

Test demo application:  
Get external IP: `kubectl get services`, get external IP from `nginx-ingress-ingress-nginx-controller`.  
Test endpoint: `curl 'http://1.2.3.4` (replace IP with your one)  
Get users endpoint: `curl 'http://1.2.3.4/user'` (replace IP with your one)  
Create users endpoint: `curl -X POST 'http://1.2.3.4/user?username=test'` (replace IP with your one) 

Pulumi useful commands:  
Cancel ongoing pulumi process: `pulumi cancel`  
In case of any errors with corrupted pulumi state: `pulumi stack export | pulumi stack import` and `pulumi refresh`  
