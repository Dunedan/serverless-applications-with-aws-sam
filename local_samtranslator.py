#!/usr/bin/env python2

"""Script to convert AWS SAM templates to AWS CloudFormation templates.

Expects SAM template on stdin and prints out CloudFormation template on stdout.
"""

import sys

import boto3
import yaml
from cfn_tools import dump_yaml
from samtranslator.public.translator import ManagedPolicyLoader
from samtranslator.translator.transform import transform

input_fragment = yaml.load(sys.stdin.read())
iam_client = boto3.client('iam')
transformed = transform(input_fragment, {}, ManagedPolicyLoader(iam_client))
print(dump_yaml(transformed))
