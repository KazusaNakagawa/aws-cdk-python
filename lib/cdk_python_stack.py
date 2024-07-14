import os
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_s3_notifications as s3_notifications,
    aws_iam as iam,
)
from constructs import Construct
from dotenv import load_dotenv


class CdkProjectStack(Stack):
    """CDK Stack class"""
    load_dotenv()

    # 環境変数からバケット名を取得
    SOURCE_BUCKET = os.environ["SOURCE_BUCKET"]
    TARGET_BUCKET = os.environ["TARGET_BUCKET"]

    def __init__(self, scope: Construct, construct_id: str, env: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Lambda関数を定義
        s3_copy_lambda = _lambda.Function(
            self,
            "s3copyHandler",
            runtime=_lambda.Runtime.PYTHON_3_12,
            code=_lambda.Code.from_asset("handler"),
            handler="s3copy.handler",
            function_name=f"s3copyHandler-{env}",
            environment={
                "SOURCE_BUCKET": self.SOURCE_BUCKET,
                "TARGET_BUCKET": self.TARGET_BUCKET,
            },
        )

        # 既存のS3バケットを参照
        source_bucket = s3.Bucket.from_bucket_name(self, "ExistingSourceBucket", self.SOURCE_BUCKET)
        target_bucket = s3.Bucket.from_bucket_name(self, "ExistingTargetBucket", self.TARGET_BUCKET)

        # Lambda関数に必要なS3バケットへのアクセス権限を付与
        s3_copy_lambda.add_to_role_policy(
            iam.PolicyStatement(
                actions=[
                    "s3:GetObject",
                    "s3:ListBucket",
                    "s3:GetBucketNotificationConfiguration",
                    "s3:PutBucketNotificationConfiguration",
                    "s3:PutObject",
                ],
                resources=[
                    source_bucket.bucket_arn,
                    f"{source_bucket.bucket_arn}/*"
                ],
            )
        )

        # S3バケットにLambda関数へのアクセス権限を付与
        source_bucket.grant_read_write(s3_copy_lambda)
        target_bucket.grant_read_write(s3_copy_lambda)

        # LambdaトリガーにS3バケットを設定
        source_bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3_notifications.LambdaDestination(s3_copy_lambda),
            s3.NotificationKeyFilter(
                prefix="input/",
                suffix=".json"),
        )
