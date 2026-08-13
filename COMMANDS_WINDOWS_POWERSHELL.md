# Module 16 - Windows PowerShell Commands

Run commands from the project folder.

## 0. Prerequisites

```powershell
pip install awscli awscli-local
Copy-Item .env.example .env
# Edit .env and insert your real LOCALSTACK_AUTH_TOKEN. Never commit .env.
```

## 1. Start LocalStack

```powershell
docker compose up -d
docker compose ps
curl.exe http://localhost:4566/_localstack/health
```

## 2. Verify IAM, S3, and Lambda APIs

```powershell
awslocal iam list-roles
awslocal s3api list-buckets
awslocal lambda list-functions
```

## 3. Create IAM Role

```powershell
awslocal iam create-role `
  --role-name module16-lambda-role `
  --assume-role-policy-document file://iam/trust-policy.json

awslocal iam put-role-policy `
  --role-name module16-lambda-role `
  --policy-name module16-lambda-policy `
  --policy-document file://iam/lambda-policy.json
```

## 4. Package Lambda Functions

```powershell
Compress-Archive -Path lambda_function_1/lambda_function.py -DestinationPath function1.zip -Force
Compress-Archive -Path lambda_function_2_initial/lambda_function.py -DestinationPath function2.zip -Force
```

## 5. Deploy Both Functions

```powershell
awslocal lambda create-function `
  --function-name file-response-formatter `
  --runtime python3.12 `
  --handler lambda_function.lambda_handler `
  --role arn:aws:iam::000000000000:role/module16-lambda-role `
  --zip-file fileb://function2.zip `
  --timeout 30

awslocal lambda wait function-active-v2 --function-name file-response-formatter

awslocal lambda create-function `
  --function-name file-event-handler `
  --runtime python3.12 `
  --handler lambda_function.lambda_handler `
  --role arn:aws:iam::000000000000:role/module16-lambda-role `
  --zip-file fileb://function1.zip `
  --timeout 30 `
  --environment "Variables={PROCESSOR_FUNCTION=file-response-formatter,LOCALSTACK_ENDPOINT=http://localhost.localstack.cloud:4566}"

awslocal lambda wait function-active-v2 --function-name file-event-handler
awslocal lambda list-functions
```

## 6. Create S3 Bucket and Configure Trigger

```powershell
awslocal s3api create-bucket --bucket module16-upload-bucket

awslocal lambda add-permission `
  --function-name file-event-handler `
  --statement-id AllowS3Invoke `
  --action lambda:InvokeFunction `
  --principal s3.amazonaws.com `
  --source-arn arn:aws:s3:::module16-upload-bucket

awslocal s3api put-bucket-notification-configuration `
  --bucket module16-upload-bucket `
  --notification-configuration file://notification.json

awslocal s3api list-buckets
awslocal s3api get-bucket-notification-configuration --bucket module16-upload-bucket
```

## 7. Test Function 2 Manually

```powershell
awslocal lambda invoke `
  --function-name file-response-formatter `
  --payload fileb://manual-event.json `
  response-function2.json

Get-Content response-function2.json
```

## 8. Test Event-Driven Workflow

```powershell
awslocal s3 cp sample.txt s3://module16-upload-bucket/sample.txt
Start-Sleep -Seconds 3
awslocal s3 ls s3://module16-upload-bucket/

awslocal logs filter-log-events --log-group-name /aws/lambda/file-event-handler
awslocal logs filter-log-events --log-group-name /aws/lambda/file-response-formatter
```

## 9. Update and Redeploy Function 2

```powershell
Compress-Archive -Path lambda_function_2_updated/lambda_function.py -DestinationPath function2-updated.zip -Force

awslocal lambda update-function-code `
  --function-name file-response-formatter `
  --zip-file fileb://function2-updated.zip

Start-Sleep -Seconds 3
awslocal lambda get-function --function-name file-response-formatter
```

## 10. Verify Updated Response

```powershell
awslocal lambda invoke `
  --function-name file-response-formatter `
  --payload fileb://manual-event.json `
  response-updated.json

Get-Content response-updated.json

awslocal s3 cp sample-updated.csv s3://module16-upload-bucket/sample-updated.csv
Start-Sleep -Seconds 3

awslocal logs filter-log-events --log-group-name /aws/lambda/file-event-handler
awslocal logs filter-log-events --log-group-name /aws/lambda/file-response-formatter
```

## 11. Final Verification

```powershell
awslocal lambda list-functions
awslocal s3 ls s3://module16-upload-bucket/
awslocal s3api get-bucket-notification-configuration --bucket module16-upload-bucket
docker compose ps
```

## Cleanup (optional, after screenshots)

```powershell
docker compose down
```
