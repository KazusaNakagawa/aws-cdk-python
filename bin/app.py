#!/usr/bin/env python3
"""Usage: app.py
cdk deploy --context env=dev

"""
import os
import sys
import aws_cdk as cdk

# スクリプトのディレクトリを取得して、lib のパスを追加
script_dir = os.path.dirname(os.path.abspath(__file__))
lib_path = os.path.join(script_dir, "..")
sys.path.append(lib_path)

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
