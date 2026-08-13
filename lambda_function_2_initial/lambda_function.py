import json


def lambda_handler(event, context):
    """Receives processed S3 metadata and returns a formatted JSON response."""
    print("Function 2 received data:")
    print(json.dumps(event))

    result = {
        "message": "Function 2 received processed S3 data successfully",
        "bucket": event.get("bucket"),
        "filename": event.get("key"),
        "size_bytes": event.get("size_bytes", 0),
        "upload_time": event.get("upload_time"),
    }

    print("Function 2 formatted result:")
    print(json.dumps(result))

    return {
        "statusCode": 200,
        "body": result,
    }
