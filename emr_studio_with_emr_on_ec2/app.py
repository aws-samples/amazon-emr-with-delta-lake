#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab

import os

import aws_cdk as cdk

from cdk_stacks import (
  VpcStack,
  EmrStack,
  EmrStudioStack,
)

AWS_ENV = cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'),
  region=os.getenv('CDK_DEFAULT_REGION'))

app = cdk.App()

vpc_stack = VpcStack(app, 'DeltaLakeEMRVpc',
  env=AWS_ENV
)

emr_studio_stack = EmrStudioStack(app, 'DeltaLakeEMRStudio',
  vpc_stack.vpc,
  env=AWS_ENV
)
emr_studio_stack.add_dependency(vpc_stack)

emr_stack = EmrStack(app, 'DeltaLakeEMRCluster',
  vpc_stack.vpc,
  emr_studio_stack.emr_studio,
  env=AWS_ENV
)
emr_stack.add_dependency(emr_studio_stack)

app.synth()
