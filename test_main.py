import json
import boto3
import pytest
from moto import mock_aws
from main import lambda_handler


@mock_aws
def test_lambda_reads_json_from_s3():

    s3 = boto3.client("s3", region_name="us-east-1")
    bucket_name = "test-bucket"
    file_key = "data.json"

    s3.create_bucket(Bucket=bucket_name)

    test_data = {"numbers": [1, 2, 3, 4, 5], "name": "test data"}
    s3.put_object(Bucket=bucket_name, Key=file_key, Body=json.dumps(test_data))

    event = {"bucket": bucket_name, "key": file_key}
    result = lambda_handler(event, {})

    assert result["statusCode"] == 200
    body = json.loads(result["body"])
    assert body["total"] == 15
    assert body["data"]["name"] == "test data"


@mock_aws
def test_lambda_file_not_found():

    s3 = boto3.client("s3", region_name="us-east-1")
    bucket_name = "test-bucket"

    s3.create_bucket(Bucket=bucket_name)

    event = {"bucket": bucket_name, "key": "nonexistent.json"}
    result = lambda_handler(event, {})

    assert result["statusCode"] == 404
    body = json.loads(result["body"])
    assert "error" in body


@mock_aws
def test_lambda_missing_parameters():

    event = {}
    result = lambda_handler(event, {})

    assert result["statusCode"] == 400
    body = json.loads(result["body"])
    assert "error" in body


@mock_aws
def test_lambda_with_nested_json():

    s3 = boto3.client("s3", region_name="us-east-1")
    bucket_name = "test-bucket"
    file_key = "nested.json"

    s3.create_bucket(Bucket=bucket_name)

    test_data = {
        "numbers": [10, 20, 30],
        "metadata": {"created_by": "test", "timestamp": "2024-01-01"},
    }
    s3.put_object(Bucket=bucket_name, Key=file_key, Body=json.dumps(test_data))

    event = {"bucket": bucket_name, "key": file_key}
    result = lambda_handler(event, {})

    assert result["statusCode"] == 200
    body = json.loads(result["body"])
    assert body["total"] == 60
