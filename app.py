#!/usr/bin/env python3
import os

import aws_cdk as cdk

from lib.aws_cdk_python_stack import MyCdkProjectStack


app = cdk.App()
MyCdkProjectStack(
    app,
    "AwsCdkPythonStack",
)

app.synth()
