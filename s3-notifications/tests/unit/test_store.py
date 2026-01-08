from io import BytesIO
import boto3
import pandas as pd
import pytest
from src.store import generate_output_key, store_data
from src.read import read_data
import moto


@pytest.fixture(scope="module")
def s3_bucket():
    with moto.mock_aws():
        s3_client = boto3.client("s3", region_name="us-east-1")
        bucket_name = "test_bucket"
        s3_client.create_bucket(Bucket=bucket_name)
        yield s3_client, bucket_name


@pytest.fixture()
def mock_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {"keyword": ["test1", "test2"], "search_volume": [100, 200], "cpc": [1.5, 2.0]}
    )


def test_key_with_json_ext():
    result = generate_output_key("test.json")
    assert result == "test.parquet"


def test_key_no_ext():
    result = generate_output_key("test")
    assert result == "test.parquet"


def test_store_data(mock_dataframe, s3_bucket):
    s3_client, bucket_name = s3_bucket
    key = "test.parquet"
    store_data(s3_client=s3_client, bucket=bucket_name, key=key, data=mock_dataframe)
    response = s3_client.get_object(Bucket=bucket_name, Key=key)

    parquet_buffer = BytesIO(response["Body"].read())
    df = pd.read_parquet(parquet_buffer, engine="pyarrow")
    pd.testing.assert_frame_equal(df, mock_dataframe)
