# Module 16 Assignment - Event-Driven Serverless Application with LocalStack

## Architecture

`S3 Object Upload -> Lambda 1 (file-event-handler) -> Lambda 2 (file-response-formatter) -> JSON/log output`

The first Lambda is triggered by an S3 `ObjectCreated` event. It extracts the bucket name, object key, object size, and upload event time, then invokes the second Lambda synchronously. The second Lambda formats the processed data as JSON. An updated v2 of Function 2 adds a UTC processing timestamp, file extension, uppercase filename, a custom message, and a deployment version field.

## Project Structure

```text
Module16_LocalStack_Assignment/
├── docker-compose.yml
├── .env.example
├── notification.json
├── manual-event.json
├── sample.txt
├── sample-updated.csv
├── COMMANDS_WINDOWS_POWERSHELL.md
├── COMMANDS_LINUX_MAC.md
├── iam/
│   ├── trust-policy.json
│   └── lambda-policy.json
├── lambda_function_1/
│   └── lambda_function.py
├── lambda_function_2_initial/
│   └── lambda_function.py
├── lambda_function_2_updated/
│   └── lambda_function.py
└── screenshots/
    └── README.md
```

## Important Current LocalStack Note

Current LocalStack Docker setups require an Auth Token for activation. Copy `.env.example` to `.env`, insert your own token, and never publish the `.env` file or token in GitHub. The Docker socket is mounted because modern LocalStack Lambda execution launches Lambda runtime containers through Docker.

## Recommended Workflow

1. Follow `COMMANDS_WINDOWS_POWERSHELL.md` on Windows or `COMMANDS_LINUX_MAC.md` on Linux/macOS.
2. Capture the nine required real screenshots using the names in `screenshots/README.md`.
3. Insert those screenshots into the matching placeholders in the provided assignment DOCX.
4. Upload the DOCX to Google Drive and open it with Google Docs.
5. Set sharing to **Anyone with the link -> Viewer** and submit the Google Docs link.

## Expected Updated Function 2 Fields

After redeployment, the response should include fields similar to:

```json
{
  "message": "Module 16 processing completed successfully!",
  "bucket": "module16-upload-bucket",
  "filename": "sample-updated.csv",
  "filename_uppercase": "SAMPLE-UPDATED.CSV",
  "file_extension": ".csv",
  "size_bytes": 41,
  "upload_time": "<S3 event time>",
  "processed_at_utc": "<current UTC timestamp>",
  "deployment_version": "v2-updated"
}
```

## References

- LocalStack Lambda documentation: https://docs.localstack.cloud/aws/services/lambda/
- LocalStack S3 documentation: https://docs.localstack.cloud/aws/services/s3/
- LocalStack AWS CLI / awslocal documentation: https://docs.localstack.cloud/aws/connecting/aws-cli/
- LocalStack installation: https://docs.localstack.cloud/aws/getting-started/installation/
- LocalStack Auth Token: https://docs.localstack.cloud/aws/getting-started/auth-token/
