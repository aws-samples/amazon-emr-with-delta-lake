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

    if str(os.environ.get('USE_DEFAULT_VPC', 'false')).lower() == 'true':
      vpc_name = self.node.try_get_context('vpc_name') or "default"
      vpc = aws_ec2.Vpc.from_lookup(self, 'ExistingVPC',
        is_default=True,
        vpc_name=vpc_name
      )
    else:
      # XXX: To use more than 2 AZs, be sure to specify the account and region on your stack.
      # XXX: https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_ec2/Vpc.html
      vpc = aws_ec2.Vpc(self, "EMRStackVPC",
        max_azs=2,
        gateway_endpoints={
          "S3": aws_ec2.GatewayVpcEndpointOptions(
            service=aws_ec2.GatewayVpcEndpointAwsService.S3
          )
        }
      )

    emr_instances = aws_emr.CfnCluster.JobFlowInstancesConfigProperty(
      # additional_master_security_groups=[], # A list of additional Amazon EC2 security group IDs for the master node.
      # additional_slave_security_groups=[], # A list of additional Amazon EC2 security group IDs for the core and task nodes.
      core_instance_group=aws_emr.CfnCluster.InstanceGroupConfigProperty(
        instance_count=3,
        instance_type="m5.2xlarge",
        market="ON_DEMAND"
      ),
      # ec2_subnet_id=vpc.public_subnets[0].subnet_id,
      ec2_subnet_id=vpc.private_subnets[0].subnet_id,
      keep_job_flow_alive_when_no_steps=True, # After last step completes: Cluster waits
      master_instance_group=aws_emr.CfnCluster.InstanceGroupConfigProperty(
        instance_count=1,
        instance_type="m5.xlarge",
        market="ON_DEMAND"
      ),
      termination_protected=False
    )

    emr_cluster_name = self.node.try_get_context("emr_cluster_name") or "deltalake-demo"
    emr_version = self.node.try_get_context("emr_version") or "emr-7.8.0"
    emr_cfn_cluster = aws_emr.CfnCluster(self, "MyEMRCluster",
      instances=emr_instances,
      # In order to use the default role for `job_flow_role`, you must have already created it using the CLI or console
      job_flow_role="EMR_EC2_DefaultRole",
      name=emr_cluster_name,
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

    cdk.CfnOutput(self, 'EmrCluserName', value=emr_cfn_cluster.name)
    cdk.CfnOutput(self, 'EmrVersion', value=emr_cfn_cluster.release_label)


app = cdk.App()
EmrStack(app, "EmrStack", env=cdk.Environment(
  account=os.getenv('CDK_DEFAULT_ACCOUNT'),
  region=os.getenv('CDK_DEFAULT_REGION')))

app.synth()
