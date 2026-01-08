import pandas as pd
from io import BytesIO


def generate_output_key(input_key: str):
    input_key_no_extension = input_key
    if ".json" in input_key:
        input_key_no_extension = input_key.replace(".json", "")
    return f"{input_key_no_extension}.parquet"


def store_data(s3_client, bucket: str, key: str, data: pd.DataFrame) -> None:
    buffer = BytesIO()
    data.to_parquet(buffer, index=False, engine='pyarrow')
    buffer.seek(0)
    s3_client.put_object(Bucket=bucket, Key=key, Body=buffer.getvalue())
