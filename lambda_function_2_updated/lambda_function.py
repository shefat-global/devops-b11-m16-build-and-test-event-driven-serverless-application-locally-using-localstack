import json
import os
from datetime import datetime, timezone


def lambda_handler(event, context):
    """Updated formatter with extra file-processing information."""
    print("UPDATED Function 2 received data:")
    print(json.dumps(event))

    filename = event.get("key", "")
    _, extension = os.path.splitext(filename)

    result = {
        "message": "Module 16 processing completed successfully!",
        "bucket": event.get("bucket"),
        "filename": filename,
        "filename_uppercase": filename.upper(),
        "file_extension": extension.lower() if extension else "no extension",
        "size_bytes": event.get("size_bytes", 0),
        "upload_time": event.get("upload_time"),
        "processed_at_utc": datetime.now(timezone.utc).isoformat(),
        "deployment_version": "v2-updated",
    }

    print("UPDATED Function 2 formatted result:")
    print(json.dumps(result))

    return {
        "statusCode": 200,
        "body": result,
    }
