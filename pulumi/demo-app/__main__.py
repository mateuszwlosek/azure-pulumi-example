import pulumi
import os
from pulumi_kubernetes.apps.v1 import Deployment, DeploymentSpecArgs
from pulumi_kubernetes.meta.v1 import LabelSelectorArgs, ObjectMetaArgs
from pulumi_kubernetes.core.v1 import ContainerArgs, PodSpecArgs, PodTemplateSpecArgs, Service, ServiceSpecArgs, ServicePortArgs, LocalObjectReferenceArgs, EnvVarArgs
from pulumi_kubernetes.networking.v1beta1 import Ingress, IngressSpecArgs, IngressRuleArgs, HTTPIngressRuleValueArgs, HTTPIngressPathArgs, IngressBackendArgs

namespace_name = os.getenv('namespace_name')
docker_registry_repository = os.getenv('docker_registry_repository')
image_pull_secret = os.getenv('image_pull_secret')
demo_port = os.getenv('demo_port')
mongodb_host = os.getenv('mongodb_host')
mongodb_port = os.getenv('mongodb_port')
mongodb_username = os.getenv('mongodb_username')
mongodb_password = os.getenv('mongodb_password')
mongodb_database = os.getenv('mongodb_database')

deployment_demo = Deployment(
    "demo",
    metadata=ObjectMetaArgs(
      name="demo",
      namespace=namespace_name
    ),
    spec=DeploymentSpecArgs(
        selector=LabelSelectorArgs(
          match_labels={
            "app":"demo"
          }
        ),
        replicas=1,
        template=PodTemplateSpecArgs(
            metadata=ObjectMetaArgs(
              labels={
                "app":"demo"
              }
            ),
            spec=PodSpecArgs(
              containers=[ContainerArgs(
                name="demo", 
                image=docker_registry_repository + ':latest',
                env=[EnvVarArgs(
                  name='mongodb_host',
                  value=mongodb_host
                ),EnvVarArgs(
                  name='mongodb_port',
                  value=mongodb_port
                ),EnvVarArgs(
                  name='mongodb_username',
                  value=mongodb_username
                ),EnvVarArgs(
                  name='mongodb_password',
                  value=mongodb_password
                ),EnvVarArgs(
                  name='mongodb_database',
                  value=mongodb_database
                )]
              )], 
              image_pull_secrets=[LocalObjectReferenceArgs(
                name=image_pull_secret
              )]
            )
        )
    ))

demo_service = Service(
 "demo",
 metadata=ObjectMetaArgs(
   name="demo",
   namespace=namespace_name
 ),
 spec=ServiceSpecArgs(
   selector={
     "app": "demo"
   },
   ports=[ServicePortArgs(
     port=int(demo_port)
   )],
   type="ClusterIP"
 )
)

ingress = Ingress(
  "ingress",
  metadata=ObjectMetaArgs(
    namespace=namespace_name,
    annotations={
      "kubernetes.io/ingress.class":"nginx",
      "nginx.ingress.kubernetes.io/ssl-redirect":"false",
      "nginx.ingress.kubernetes.io/use-regex":"true",
      "nginx.ingress.kubernetes.io/rewrite-target":"/$1"
    }
  ),
  spec = IngressSpecArgs(
    rules = [IngressRuleArgs(
        http = HTTPIngressRuleValueArgs(
            paths = [HTTPIngressPathArgs(
                backend = IngressBackendArgs(
                    service_name = "demo",
                    service_port = int(demo_port)
                ),
                path = "/(.*)"
            )]
        )
    )]
  )
)

