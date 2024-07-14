#!/usr/bin/env python3
"""Usage: app.py
cdk deploy --context env=dev

"""
import aws_cdk as cdk

from lib.cdk_python_stack import CdkProjectStack


app = cdk.App()

# --context {{環境}}} のパラメータを取得
env = cdk.App().node.try_get_context("env")

CdkProjectStack(
    scope=app,
    construct_id=f"cdk-python-stack-{env}",
    env=env,
)

app.synth()
