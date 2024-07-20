import os
import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_s3_notifications as s3_notifications,
    aws_iam as iam,
)
from constructs import Construct
from dotenv import load_dotenv

load_dotenv()

# 環境変数からバケット名を取得
SOURCE_BUCKET = os.environ["SOURCE_BUCKET"]
TARGET_BUCKET = os.environ["TARGET_BUCKET"]


class CdkProjectStack(Stack):
    """CDK Stack class"""

    def __init__(self, scope: Construct, construct_id: str, env: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 既存のS3バケットを参照
        source_bucket = s3.Bucket.from_bucket_name(self, "ExistingSourceBucket", SOURCE_BUCKET)

        # カスタムポリシーを定義
        custom_policy = iam.Policy(
            self, "CustomPolicy",
            statements=[
                iam.PolicyStatement(
                    actions=[
                        "s3:GetObject",
                        "s3:ListBucket",
                        "s3:GetBucketNotificationConfiguration",
                        "s3:PutBucketNotificationConfiguration",
                        "s3:PutObject",
                    ],
                    effect=iam.Effect.ALLOW,
                    resources=["arn:aws:s3:::*"],
                ),
                iam.PolicyStatement(
                    actions=[
                        "logs:CreateLogGroup",
                        "logs:CreateLogStream",
                        "logs:PutLogEvents",
                    ],
                    effect=iam.Effect.ALLOW,
                    resources=[f"arn:aws:logs:{cdk.Aws.REGION}:{cdk.Aws.ACCOUNT_ID}:log-group:/aws/lambda/*"],
                ),
            ],
        )

        # IAMロールを定義し、カスタムポリシーをアタッチ
        custom_role = iam.Role(self, "CustomRole", assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"))
        custom_policy.attach_to_role(custom_role)

        # Lambda関数を定義
        default_lambda = DefaultLambda(
            self,
            "defaultHandler",
            role=custom_role,
            function_name=f"defaultHandler-{env}",
        )

        # LambdaトリガーにS3バケットを設定
        source_bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3_notifications.LambdaDestination(default_lambda),
            s3.NotificationKeyFilter(
                prefix="input/",
                suffix=".json",
            ),
        )


class DefaultLambda(_lambda.Function):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(
            scope,
            id,
            runtime=_lambda.Runtime.PYTHON_3_12,
            code=_lambda.Code.from_asset("handler"),
            handler="s3copy.handler",
            environment={
                "SOURCE_BUCKET": SOURCE_BUCKET,
                "TARGET_BUCKET": TARGET_BUCKET,
            },
            **kwargs  # 他の任意の引数を受け入れる
        )
