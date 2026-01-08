import json
import os
import boto3
import pytest

LOCALSTACK_ENDPOINT_URL = os.getenv("LOCALSTACK_ENDPOINT_URL")
AWS_REGION = os.getenv("AWS_REGION")
LAMBDA_NAME = os.getenv("AWS_LAMBDA_NAME")

@pytest.fixture()
def client():
    client = boto3.client(
        "lambda", endpoint_url=LOCALSTACK_ENDPOINT_URL, region_name=AWS_REGION
    )
    return client


@pytest.fixture()
def invoke_lambda(client):
    return lambda payload: client.invoke(
        FunctionName=LAMBDA_NAME, Payload=json.dumps(payload)
    )


def test_happy_path(invoke_lambda):
    response = invoke_lambda({"x": 1, "y": 2})
    response_payload = json.loads(response["Payload"].read())

    assert response_payload["result"] == 3


def test_invalid_input_type(invoke_lambda):
    response = invoke_lambda({"x": "1", "y": 2})

    response_payload = json.loads(response["Payload"].read())

    assert response_payload["result"] == 3

    response = invoke_lambda({"x": "1", "y": "2"})
    response_payload = json.loads(response["Payload"].read())

    assert response_payload["result"] == 3

    response = invoke_lambda({"x": "1"})
    response_payload = json.loads(response["Payload"].read())

    assert response_payload["result"] == 1


def test_no_input(invoke_lambda):
    response = invoke_lambda({})
    response_payload = json.loads(response["Payload"].read())

    assert response_payload["result"] == 0


def test_invalid_input(invoke_lambda):
    response = invoke_lambda({"x": "invalid", "y": "invalid"})
    response_payload = json.loads(response["Payload"].read())

    assert response_payload["statusCode"] == 400
    assert response_payload["error"] == "invalid input"
