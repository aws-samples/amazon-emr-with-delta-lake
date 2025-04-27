#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab

import aws_cdk as cdk

from aws_cdk import (
  Stack,
  aws_ec2,
  aws_emr
)
from constructs import Construct


class EmrStack(Stack):

  def __init__(self, scope: Construct, construct_id: str, vpc, emr_studio, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    emr_studio_engine_sg = aws_ec2.SecurityGroup.from_security_group_id(self,
      "EMRStudioEngineSG",
      emr_studio.engine_security_group_id
    )

    emr_cluster_sg = aws_ec2.SecurityGroup(self, "EMRClusterSG",
      vpc=vpc,
      description="Security Group for EMR Cluster"
    )
    emr_cluster_sg.add_ingress_rule(
      peer=emr_studio_engine_sg,
      connection=aws_ec2.Port.tcp(18888),
      description="Allow from EMR Studio Engine Security Group"
    )

    emr_instances = aws_emr.CfnCluster.JobFlowInstancesConfigProperty(
      additional_master_security_groups=[emr_cluster_sg.security_group_id],
      additional_slave_security_groups=[emr_cluster_sg.security_group_id],
      core_instance_group=aws_emr.CfnCluster.InstanceGroupConfigProperty(
        instance_count=3,
        instance_type="m5.2xlarge",
        market="ON_DEMAND"
      ),
      ec2_subnet_id=emr_studio.subnet_ids[0],
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


    cdk.CfnOutput(self, 'EmrCluserName',
      value=emr_cfn_cluster.name,
      export_name=f'{self.stack_name}-EmrCluserName')
    cdk.CfnOutput(self, 'EmrVersion',
      value=emr_cfn_cluster.release_label,
      export_name=f'{self.stack_name}-EmrVersion')
