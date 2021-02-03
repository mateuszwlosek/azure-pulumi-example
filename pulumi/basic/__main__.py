import pulumi
import os
from pulumi_kubernetes.meta.v1 import ObjectMetaArgs
from pulumi_kubernetes.core.v1 import PersistentVolume, PersistentVolumeClaim, PersistentVolumeClaimSpecArgs, ResourceRequirementsArgs, Namespace
from pulumi_kubernetes.storage.v1 import StorageClass
from pulumi_kubernetes.helm.v2 import Chart, ChartOpts, FetchOpts

namespace_name = os.getenv('namespace_name')
mongodb_database = os.getenv('mongodb_database')
mongodb_username = os.getenv('mongodb_username')
mongodb_password = os.getenv('mongodb_password')

namespace = Namespace(
  resource_name=namespace_name,
  metadata=ObjectMetaArgs(
    name=namespace_name
  )
)

ingress_service = Chart(
  'nginx-ingress',
  config = ChartOpts(
    fetch_opts = FetchOpts(
      repo='https://kubernetes.github.io/ingress-nginx'
    ),
    chart = 'ingress-nginx',
    version = '3.21.0',
    namespace = namespace_name,
  values = {
    "controller" : {
      "replicaCount" : 1
   }
 }
))

storage_class = StorageClass(
  "storage-class",
  provisioner="kubernetes.io/azure-disk",
  reclaim_policy="Retain",
  parameters={
    "storageaccounttype":"Premium_LRS",
    "kind":"Managed"
  }
)

mongodb_volume_claim = PersistentVolumeClaim(
  "mongodb-volume-claim",
  metadata=ObjectMetaArgs(
    namespace=namespace_name
  ),
  spec=PersistentVolumeClaimSpecArgs(
    storage_class_name="managed-premium",
    access_modes=["ReadWriteOnce"],
    resources=ResourceRequirementsArgs(
      requests={
        "storage":"1Gi"
      }
    )
  )
)


mongodb_chart = Chart(
  'mongodb', 
  config=ChartOpts(
    fetch_opts = FetchOpts(
      repo='https://charts.bitnami.com/bitnami'
    ),
    chart='mongodb',
    version='10.4.0',
    namespace=namespace_name,
    values={
      "nameOverride":"mongodb",
      "labels":{
       "app":"mongodb"
      },
      "auth":{
        "database":mongodb_database,
        "username":mongodb_username,
        "password":mongodb_password
      },
     "persistence":{
       "existingClaim":mongodb_volume_claim.metadata.name
     }
   }
))
