import json
import os
from urllib.parse import unquote_plus

import boto3

PROCESSOR_FUNCTION = os.getenv("PROCESSOR_FUNCTION", "file-response-formatter")
LOCALSTACK_ENDPOINT = os.getenv(
    "LOCALSTACK_ENDPOINT", "http://localhost.localstack.cloud:4566"
)

lambda_client = boto3.client(
    "lambda",
    region_name="us-east-1",
    endpoint_url=LOCALSTACK_ENDPOINT,
)


def lambda_handler(event, context):
    """Triggered automatically when a new object is created in S3."""
    print("Received S3 event:")
    print(json.dumps(event))

    record = event["Records"][0]
    bucket_name = record["s3"]["bucket"]["name"]
    object_key = unquote_plus(record["s3"]["object"]["key"])
    object_size = record["s3"]["object"].get("size", 0)
    event_time = record.get("eventTime", "unknown")

    processed_data = {
        "bucket": bucket_name,
        "key": object_key,
        "size_bytes": object_size,
        "upload_time": event_time,
        "source": "S3 ObjectCreated event",
    }

    print("Function 1 processed data:")
    print(json.dumps(processed_data))

    response = lambda_client.invoke(
        FunctionName=PROCESSOR_FUNCTION,
        InvocationType="RequestResponse",
        Payload=json.dumps(processed_data).encode("utf-8"),
    )

    function2_payload = json.loads(response["Payload"].read().decode("utf-8"))

    print("Function 2 response received by Function 1:")
    print(json.dumps(function2_payload))

    return {
        "statusCode": 200,
        "message": "S3 upload event processed successfully",
        "processed_data": processed_data,
        "function2_response": function2_payload,
    }
