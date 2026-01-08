import os
import boto3
from src import read_data, store_data, transform_data, generate_output_key
from src._types import Data

s3_client = boto3.client("s3")
output_bucket = os.getenv("OUTPUT_BUCKET")


def lambda_handler(event: dict, context: dict):
    if not output_bucket:
        raise ValueError("output bucket not set")

    event_name = event["Records"][0]["eventName"]
    if event_name == "ObjectCreated:Put":
        s3 = event["Records"][0]["s3"]
        src_obj_key = s3["object"]["key"]
        bucket_name = s3["bucket"]["name"]

    input_data: Data = read_data(s3_client=s3_client, bucket=bucket_name, key=src_obj_key)  # type: ignore
    transformed_data = transform_data(input_data)
    output_key = generate_output_key(src_obj_key)
    store_data(
        s3_client=s3_client, bucket=output_bucket, key=output_key, data=transformed_data
    )
