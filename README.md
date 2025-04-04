# AWS SAM Template for Auto-Deleting CloudFormation Stacks

## Overview
This AWS Serverless Application Model (SAM) template defines a Lambda function that automatically deletes old CloudFormation stacks based on a time-to-live (TTL) parameter. The function is scheduled to run every 5 minutes and removes stacks that match specific naming patterns (`feat`, `rel`, `hotfix`) and exceed the defined TTL.

## Architecture
- **AWS Lambda**: The function that checks and deletes old CloudFormation stacks.
- **Amazon EventBridge (CloudWatch Events)**: Triggers the Lambda function every 5 minutes.
- **IAM Role**: Grants the necessary permissions to the Lambda function to manage CloudFormation stacks and write logs.

## Prerequisites
- AWS CLI installed and configured
- AWS SAM CLI installed
- Python 3.13 installed

## Deployment Instructions
1. Clone the repository:
   ```sh
   git clone <repository-url>
   cd <repository-folder>
   ```
2. Build the SAM application:
   ```sh
   sam build
   ```
3. Deploy the application:
   ```sh
   sam deploy --guided
   ```
   Follow the prompts to configure parameters such as TTL.

## Environment Variables
- `ttl_minutes`: The number of minutes before a CloudFormation stack should be deleted. This is set through the `TTL` parameter in the template.

## Lambda Function Code
The Lambda function is located in `lambda_function/lambda_function.py` and is responsible for:
- Listing all CloudFormation stacks.
- Filtering stacks based on naming patterns and age.
- Deleting stacks older than the defined TTL.

## Cleanup
To remove the deployed resources, run:
```sh
sam delete
```

