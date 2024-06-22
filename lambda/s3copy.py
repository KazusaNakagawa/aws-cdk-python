import json
import boto3
import os

s3 = boto3.client("s3")


def handler(event, context):
    # 環境変数からバケット名を取得
    source_bucket = os.environ["SOURCE_BUCKET"]
    target_bucket = os.environ["TARGET_BUCKET"]

    # イベントからS3オブジェクト情報を取得
    source_key = event["Records"][0]["s3"]["object"]["key"]

    if source_key.endswith(".json"):
        try:
            copy_source = {"Bucket": source_bucket, "Key": source_key}
            s3.copy_object(CopySource=copy_source, Bucket=target_bucket, Key=source_key)
            print(f"Successfully copied {source_key} from {source_bucket} to {target_bucket}")
            return {"statusCode": 200, "body": json.dumps(f"Successfully copied {source_key}")}
        except Exception as e:
            print(e)
            print(f"Error copying {source_key} from {source_bucket} to {target_bucket}")
            return {"statusCode": 500, "body": json.dumps(f"Error copying {source_key}")}
    else:
        print(f"{source_key} is not a .json file. No action taken.")
        return {"statusCode": 200, "body": json.dumps(f"{source_key} is not a .json file. No action taken.")}
