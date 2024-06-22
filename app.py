#!/usr/bin/env python3
import os

import aws_cdk as cdk

from aws_cdk_python.aws_cdk_python_stack import MyCdkProjectStack


app = cdk.App()
MyCdkProjectStack(
    app,
    "AwsCdkPythonStack",
)

app.synth()
