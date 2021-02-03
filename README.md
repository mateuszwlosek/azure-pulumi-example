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

### Setup Kubernetes cluster
Go to `Kubernetes services` and add a new Kubernetes cluser.  
While creating the cluster, add a new resource group while clicking `Create new`.  
Go to the `Integrations` tab and create a new container registry with `Create new`.  
If you are using a free trial account, change `node count` to 1
All the other settings can be left as the default ones.  
![image](https://user-images.githubusercontent.com/15820051/106795693-ad914280-665a-11eb-9f3b-b151b17b0cf3.png)  
![image](https://user-images.githubusercontent.com/15820051/106796891-407eac80-665c-11eb-902a-17f8b5352be5.png)  

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


#### Pipelines
Go to `Pipelines` and create a new one.  
Select `Azure Repos Git` and repository created before as the place with your code. 

**Pipeline to create a basic infrastructure (namespace, ingress service, storage, mongodb)**
In `Configure` step select `Existing Azure Pipeline YAML file` and in `path` select: `/pipelines/pulumi-pipeline.yml`.  
Now configure Variables  
![image](https://user-images.githubusercontent.com/15820051/106798640-89cffb80-665e-11eb-9680-1b57e3919ed0.png)  

Name: azure_subscription  
Description: XXX  
My value: azure-service-connection  

Name: cluster_name  
Description: Kubernetes cluster name  
My value: test-cluster  

Name: mongodb_database  
Description: Mongodb database name (you can type anything)  
My value: master  

Name: mongodb_username  
Description: Mongodb username (you can type anything)  
My value: test  

Name: mongodb_password  
Description: Mongodb password (you can type anything)  
My value: test  

Name: namespace_name  
Description: Namespace name (you can type anything)  
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
Description: Pulumi stack name (you can type anything)  
My value: demo-stack  

Name: resources_group_name  
Description: Resources group name. Generated when kubernetes cluster was created.  
My value: test-resource-group  
