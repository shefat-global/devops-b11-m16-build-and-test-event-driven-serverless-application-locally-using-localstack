# Module 16 - Linux/macOS Commands

```bash
pip install awscli awscli-local
cp .env.example .env
# Edit .env and insert your real LOCALSTACK_AUTH_TOKEN. Never commit .env.

docker compose up -d
docker compose ps
curl http://localhost:4566/_localstack/health

awslocal iam create-role \
  --role-name module16-lambda-role \
  --assume-role-policy-document file://iam/trust-policy.json
awslocal iam put-role-policy \
  --role-name module16-lambda-role \
  --policy-name module16-lambda-policy \
  --policy-document file://iam/lambda-policy.json

(cd lambda_function_2_initial && zip -j ../function2.zip lambda_function.py)
(cd lambda_function_1 && zip -j ../function1.zip lambda_function.py)

awslocal lambda create-function \
  --function-name file-response-formatter \
  --runtime python3.12 \
  --handler lambda_function.lambda_handler \
  --role arn:aws:iam::000000000000:role/module16-lambda-role \
  --zip-file fileb://function2.zip \
  --timeout 30
awslocal lambda wait function-active-v2 --function-name file-response-formatter

awslocal lambda create-function \
  --function-name file-event-handler \
  --runtime python3.12 \
  --handler lambda_function.lambda_handler \
  --role arn:aws:iam::000000000000:role/module16-lambda-role \
  --zip-file fileb://function1.zip \
  --timeout 30 \
  --environment 'Variables={PROCESSOR_FUNCTION=file-response-formatter,LOCALSTACK_ENDPOINT=http://localhost.localstack.cloud:4566}'
awslocal lambda wait function-active-v2 --function-name file-event-handler

awslocal s3api create-bucket --bucket module16-upload-bucket
awslocal lambda add-permission \
  --function-name file-event-handler \
  --statement-id AllowS3Invoke \
  --action lambda:InvokeFunction \
  --principal s3.amazonaws.com \
  --source-arn arn:aws:s3:::module16-upload-bucket
awslocal s3api put-bucket-notification-configuration \
  --bucket module16-upload-bucket \
  --notification-configuration file://notification.json

awslocal lambda invoke --function-name file-response-formatter --payload fileb://manual-event.json response-function2.json
cat response-function2.json

awslocal s3 cp sample.txt s3://module16-upload-bucket/sample.txt
sleep 3
awslocal logs filter-log-events --log-group-name /aws/lambda/file-event-handler
awslocal logs filter-log-events --log-group-name /aws/lambda/file-response-formatter

(cd lambda_function_2_updated && zip -j ../function2-updated.zip lambda_function.py)
awslocal lambda update-function-code --function-name file-response-formatter --zip-file fileb://function2-updated.zip
sleep 3

awslocal lambda invoke --function-name file-response-formatter --payload fileb://manual-event.json response-updated.json
cat response-updated.json
awslocal s3 cp sample-updated.csv s3://module16-upload-bucket/sample-updated.csv
sleep 3
awslocal logs filter-log-events --log-group-name /aws/lambda/file-event-handler
awslocal logs filter-log-events --log-group-name /aws/lambda/file-response-formatter
```
