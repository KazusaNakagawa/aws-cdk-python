import pytest
from datetime import datetime as dt

from handler import s3copy

s3copy.CONFIG_FILE = "./handler/config.json"

class TestS3Copy:

    def test_s3copy(self, mocker, monkeypatch):
        monkeypatch.setenv("SOURCE_BUCKET", "source-bucket")
        monkeypatch.setenv("TARGET_BUCKET", "target-bucket")
        source_key = "input/test1.json"
        event = {
            "Records": [
                {
                    "s3": {
                        "bucket": {
                            "name": "source-bucket"
                        },
                        "object": {
                            "key": source_key
                        }
                    }
                }
            ]
        }
        context = {}
        mock_s3_client = mocker.patch('handler.s3copy.s3')
        mock_s3_client.copy_object.return_value = {}

        # Act
        result = s3copy.handler(event, context)

        # Assert
        dt_now = dt.now().strftime("%Y/%m/%d")
        mock_s3_client.copy_object.assert_called_once_with(
            Bucket="target-bucket",
            CopySource={
                "Bucket": "source-bucket",
                "Key": source_key
            },
            Key=f"test1_prefix/{dt_now}/{source_key}",
        )
        assert result == {'statusCode': 200, 'body': f'"Successfully copied {source_key}"'}

    def test_s3copy_not_json(self, mocker, monkeypatch):
        monkeypatch.setenv("SOURCE_BUCKET", "source-bucket")
        monkeypatch.setenv("TARGET_BUCKET", "target-bucket")
        source_key = "input/test1.txt"
        event = {
            "Records": [
                {
                    "s3": {
                        "bucket": {
                            "name": "source-bucket"
                        },
                        "object": {
                            "key": source_key
                        }
                    }
                }
            ]
        }
        context = {}
        mock_s3_client = mocker.patch('handler.s3copy.s3')
        mock_s3_client.copy_object.return_value = {}

        # Act
        result = s3copy.handler(event, context)

        # Assert
        mock_s3_client.copy_object.assert_not_called()
        assert result == {'statusCode': 200, 'body': f'"{source_key} is not a .json file. No action taken."'}
