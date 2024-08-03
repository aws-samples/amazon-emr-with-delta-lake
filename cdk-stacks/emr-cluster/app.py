#!/usr/bin/env python3
import os

import aws_cdk as cdk

from aws_cdk import (
  Stack,
  aws_ec2,
  aws_emr
)
from constructs import Construct

class EmrStack(Stack):

  def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    EMR_CLUSTER_NAME = cdk.CfnParameter(self, 'EMRClusterName',
      type='String',
      description='Amazon EMR Cluster name',
      default='deltalake-demo'
    )

    vpc_name = self.node.try_get_context("vpc_name") or "default"
    vpc = aws_ec2.Vpc.from_lookup(self, "ExistingVPC",
      is_default=True,
      vpc_name=vpc_name)

    #XXX: For creating Amazon EMR in a new VPC,
    # remove comments from the below codes and
    # comments out vpc = aws_ec2.Vpc.from_lookup(..) codes above,
    #
    # vpc = aws_ec2.Vpc(self, "EMRStackVPC",
    #   max_azs=2,
    #   gateway_endpoints={
    #     "S3": aws_ec2.GatewayVpcEndpointOptions(
    #       service=aws_ec2.GatewayVpcEndpointAwsService.S3
    #     )
    #   }
    # )

    emr_instances = aws_emr.CfnCluster.JobFlowInstancesConfigProperty(
      core_instance_group=aws_emr.CfnCluster.InstanceGroupConfigProperty(
        instance_count=2,
        instance_type="m5.xlarge",
        market="ON_DEMAND"
      ),
      ec2_subnet_id=vpc.public_subnets[0].subnet_id,
      keep_job_flow_alive_when_no_steps=True, # After last step completes: Cluster waits
      master_instance_group=aws_emr.CfnCluster.InstanceGroupConfigProperty(
        instance_count=1,
        instance_type="m5.xlarge",
        market="ON_DEMAND"
      ),
      termination_protected=False
    )

    emr_version = self.node.try_get_context("emr_version") or "emr-7.2.0"
    emr_cfn_cluster = aws_emr.CfnCluster(self, "MyEMRCluster",
      instances=emr_instances,
      # In order to use the default role for `job_flow_role`, you must have already created it using the CLI or console
      job_flow_role="EMR_EC2_DefaultRole",
      name=EMR_CLUSTER_NAME.value_as_string,
      service_role="EMR_DefaultRole_V2",
      applications=[
        aws_emr.CfnCluster.ApplicationProperty(name="Hadoop"),
        aws_emr.CfnCluster.ApplicationProperty(name="Hive"),
        aws_emr.CfnCluster.ApplicationProperty(name="JupyterHub"),
        aws_emr.CfnCluster.ApplicationProperty(name="Livy"),
        aws_emr.CfnCluster.ApplicationProperty(name="Spark"),
        aws_emr.CfnCluster.ApplicationProperty(name="JupyterEnterpriseGateway")
      ],
      bootstrap_actions=None,
      configurations=[
        aws_emr.CfnCluster.ConfigurationProperty(
          classification="delta-defaults",
          configuration_properties={
            "delta.enabled": "true"
          }),
        aws_emr.CfnCluster.ConfigurationProperty(
          classification="hive-site",
          configuration_properties={
            "hive.metastore.client.factory.class": "com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory"
          }),
        aws_emr.CfnCluster.ConfigurationProperty(
          classification="spark-hive-site",
          configuration_properties={
            "hive.metastore.client.factory.class": "com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory"
          })
      ],
      ebs_root_volume_size=32,
      log_uri="s3n://aws-logs-{account}-{region}/elasticmapreduce/".format(account=cdk.Aws.ACCOUNT_ID, region=cdk.Aws.REGION),
      release_label=emr_version,
      scale_down_behavior="TERMINATE_AT_TASK_COMPLETION",
      visible_to_all_users=True
    )


app = cdk.App()
EmrStack(app, "EmrStack", env=cdk.Environment(
  account=os.getenv('CDK_DEFAULT_ACCOUNT'),
  region=os.getenv('CDK_DEFAULT_REGION')))

app.synth()
