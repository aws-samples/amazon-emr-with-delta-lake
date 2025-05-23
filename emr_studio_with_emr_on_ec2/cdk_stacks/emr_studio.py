#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab

import aws_cdk as cdk

from aws_cdk import (
  Stack,
  aws_ec2,
  aws_emr,
  aws_iam,
  aws_s3 as s3,
)
from constructs import Construct


class EmrStudioStack(Stack):

  def __init__(self, scope: Construct, construct_id: str, vpc, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    EMR_STUDIO_NAME = self.node.try_get_context("emr_studio_name") or "deltalake-demo"

    s3_bucket = s3.Bucket(self, "s3bucket",
      removal_policy=cdk.RemovalPolicy.DESTROY, #XXX: Default: cdk.RemovalPolicy.RETAIN - The bucket will be orphaned
      bucket_name=f"{EMR_STUDIO_NAME}-emr-studio-{self.region}-{self.account}")

    sg_emr_studio_workspace = aws_ec2.SecurityGroup(self, 'EmrStudioWorkspaceSG',
      vpc=vpc,
      allow_all_outbound=False,
      description='Workspace Security Group for EMR Studio',
      security_group_name=f'{EMR_STUDIO_NAME}-emr-studio-workspace'
    )
    cdk.Tags.of(sg_emr_studio_workspace).add('Name', 'emr-studio-workspace')

    sg_emr_studio_engine = aws_ec2.SecurityGroup(self, 'EmrStudioEngineSG',
      vpc=vpc,
      allow_all_outbound=True,
      description='Engine Security Group for EMR Studio',
      security_group_name=f'{EMR_STUDIO_NAME}-emr-studio-engine'
    )
    cdk.Tags.of(sg_emr_studio_engine).add('Name', 'emr-studio-engine')

    sg_emr_studio_engine.add_ingress_rule(peer=sg_emr_studio_workspace,
      connection=aws_ec2.Port.tcp(18888),
      description='Allow inbound from Workspace Security Group')

    sg_emr_studio_workspace.add_egress_rule(peer=sg_emr_studio_engine,
      connection=aws_ec2.Port.tcp(18888),
      description='Allow outbound to Engine Security Group')
    sg_emr_studio_workspace.add_egress_rule(peer=aws_ec2.Peer.any_ipv4(),
      connection=aws_ec2.Port.tcp(443),
      description='Allow HTTPS outbound')


    emr_studio_service_role_policy_doc = aws_iam.PolicyDocument()

    emr_studio_service_role_policy_doc.add_statements(aws_iam.PolicyStatement(**{
      "sid": "AllowEMRReadOnlyActions",
      "effect": aws_iam.Effect.ALLOW,
      "actions": [
        "elasticmapreduce:ListInstances",
        "elasticmapreduce:DescribeCluster",
        "elasticmapreduce:ListSteps"
      ],
      "resources": ["*"]
    }))

    emr_studio_service_role_policy_doc.add_statements(aws_iam.PolicyStatement(**{
      "sid": "AllowEC2ENIActions",
      "effect": aws_iam.Effect.ALLOW,
      "actions": [
        "ec2:CreateNetworkInterfacePermission",
        "ec2:DeleteNetworkInterface"
      ],
      "resources": ["arn:aws:ec2:*:*:network-interface/*"]
    }))

    emr_studio_service_role_policy_doc.add_statements(aws_iam.PolicyStatement(**{
      "sid": "AllowEC2ENIAttributeAction",
      "effect": aws_iam.Effect.ALLOW,
      "actions": [
        "ec2:ModifyNetworkInterfaceAttribute"
      ],
      "resources": [
        "arn:aws:ec2:*:*:instance/*",
        "arn:aws:ec2:*:*:network-interface/*",
        "arn:aws:ec2:*:*:security-group/*"
      ]
    }))

    emr_studio_service_role_policy_doc.add_statements(aws_iam.PolicyStatement(**{
      "sid": "AllowEC2SecurityGroupActions",
      "effect": aws_iam.Effect.ALLOW,
      "actions": [
        "ec2:AuthorizeSecurityGroupEgress",
        "ec2:AuthorizeSecurityGroupIngress",
        "ec2:RevokeSecurityGroupEgress",
        "ec2:RevokeSecurityGroupIngress",
        "ec2:DeleteNetworkInterfacePermission"
      ],
      "resources": [ "*" ]
    }))

    emr_studio_service_role_policy_doc.add_statements(aws_iam.PolicyStatement(**{
      "sid": "AllowDefaultEC2SecurityGroupsCreation",
      "effect": aws_iam.Effect.ALLOW,
      "actions": [
        "ec2:CreateSecurityGroup"
      ],
      "resources": [ "arn:aws:ec2:*:*:security-group/*" ]
    }))

    emr_studio_service_role_policy_doc.add_statements(aws_iam.PolicyStatement(**{
      "sid": "AllowDefaultEC2SecurityGroupsCreationInVPC",
      "effect": aws_iam.Effect.ALLOW,
      "actions": [
        "ec2:CreateSecurityGroup"
      ],
      "resources": [ "arn:aws:ec2:*:*:vpc/*" ]
    }))

    emr_studio_service_role_policy_doc.add_statements(aws_iam.PolicyStatement(**{
      "sid": "AllowAddingEMRTagsDuringDefaultSecurityGroupCreation",
      "effect": aws_iam.Effect.ALLOW,
      "actions": [
        "ec2:CreateTags"
      ],
      "resources": [ "arn:aws:ec2:*:*:security-group/*" ],
      "conditions": {
        "StringEquals": {
          "ec2:CreateAction": "CreateSecurityGroup"
        }
      }
    }))

    emr_studio_service_role_policy_doc.add_statements(aws_iam.PolicyStatement(**{
      "sid": "AllowEC2ENICreation",
      "effect": aws_iam.Effect.ALLOW,
      "actions": [
        "ec2:CreateNetworkInterface"
      ],
      "resources": [ "arn:aws:ec2:*:*:network-interface/*" ]
    }))

    emr_studio_service_role_policy_doc.add_statements(aws_iam.PolicyStatement(**{
      "sid": "AllowEC2ENICreationInSubnetAndSecurityGroup",
      "effect": aws_iam.Effect.ALLOW,
      "actions": [
        "ec2:CreateNetworkInterface"
      ],
      "resources": [
        "arn:aws:ec2:*:*:subnet/*",
        "arn:aws:ec2:*:*:security-group/*"
      ]
    }))

    emr_studio_service_role_policy_doc.add_statements(aws_iam.PolicyStatement(**{
      "sid": "AllowAddingTagsDuringEC2ENICreation",
      "effect": aws_iam.Effect.ALLOW,
      "actions": [
        "ec2:CreateTags"
      ],
      "resources": [ "arn:aws:ec2:*:*:network-interface/*" ],
      "conditions": {
        "StringEquals": {
          "ec2:CreateAction": "CreateNetworkInterface"
        }
      }
    }))

    emr_studio_service_role_policy_doc.add_statements(aws_iam.PolicyStatement(**{
      "sid": "AllowEC2ReadOnlyActions",
      "effect": aws_iam.Effect.ALLOW,
      "actions": [
        "ec2:DescribeSecurityGroups",
        "ec2:DescribeNetworkInterfaces",
        "ec2:DescribeTags",
        "ec2:DescribeInstances",
        "ec2:DescribeSubnets",
        "ec2:DescribeVpcs"
      ],
      "resources": [ "*" ]
    }))

    emr_studio_service_role_policy_doc.add_statements(aws_iam.PolicyStatement(**{
      "sid": "AllowSecretsManagerReadOnlyActions",
      "effect": aws_iam.Effect.ALLOW,
      "actions": [
        "secretsmanager:GetSecretValue"
      ],
      "resources": [ "arn:aws:secretsmanager:*:*:secret:*" ]
    }))

    emr_studio_service_role_policy_doc.add_statements(aws_iam.PolicyStatement(**{
      "sid": "AllowS3NotebookStorage",
      "effect": aws_iam.Effect.ALLOW,
      "actions": [
        "s3:Put*",
        "s3:Get*",
        "s3:GetEncryptionConfiguration",
        "s3:List*",
        "s3:Delete*"
      ],
      "resources": [ "*" ]
    }))

    emr_studio_service_role_policy_doc.add_statements(aws_iam.PolicyStatement(**{
      "sid": "KmsPermission",
      "effect": aws_iam.Effect.ALLOW,
      "actions": [
        "kms:Decrypt",
        "kms:ReEncrypt*",
        "kms:GenerateDataKey*",
        "kms:DescribeKey"
      ],
      "resources": [ "*" ]
    }))

    emr_studio_service_role = aws_iam.Role(self, 'EmrStudioServiceRole',
      role_name=f'{EMR_STUDIO_NAME}_EMRStudio_Service_Role',
      assumed_by=aws_iam.ServicePrincipal('elasticmapreduce.amazonaws.com'),
      inline_policies={
        f'{EMR_STUDIO_NAME}_EMRStudioServiceRolePolicy': emr_studio_service_role_policy_doc
      }
    )

    # http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emr-studio.html
    self.emr_studio = aws_emr.CfnStudio(self, "MyCfnEmrStudio",
      auth_mode="IAM", # [IAM, SSO]
      default_s3_location=f"s3://{s3_bucket.bucket_name}",
      engine_security_group_id=sg_emr_studio_engine.security_group_id,
      name=EMR_STUDIO_NAME,
      service_role=emr_studio_service_role.role_arn,
      subnet_ids=vpc.select_subnets(subnet_type=aws_ec2.SubnetType.PRIVATE_WITH_NAT).subnet_ids,
      vpc_id=vpc.vpc_id,
      workspace_security_group_id=sg_emr_studio_workspace.security_group_id
    )


    cdk.CfnOutput(self, 'EmrStudioName',
      value=self.emr_studio.name,
      export_name=f'{self.stack_name}-EmrStudioName')
    cdk.CfnOutput(self, 'EmrStudioUrl',
      value=self.emr_studio.attr_url,
      export_name=f'{self.stack_name}-EmrStudioUrl')
    cdk.CfnOutput(self, 'EmrStudioId',
      value=self.emr_studio.attr_studio_id,
      export_name=f'{self.stack_name}-EmrStudioId')
    cdk.CfnOutput(self, 'EmrStudioDefaultS3Location',
      value=self.emr_studio.default_s3_location,
      export_name=f'{self.stack_name}-EmrStudioDefaultS3Location')
    cdk.CfnOutput(self, 'EmrStudioEnginSecurityGroupId',
      value=self.emr_studio.engine_security_group_id,
      export_name=f'{self.stack_name}-EmrStudioEnginSecurityGroupId')
    cdk.CfnOutput(self, 'EmrStudioWSSecurityGroupId',
      value=self.emr_studio.workspace_security_group_id,
      export_name=f'{self.stack_name}-EmrStudioWSSecurityGroupId')
