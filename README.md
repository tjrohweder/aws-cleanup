# AWS SAM Template for Auto-Deleting CloudFormation Stacks

## Overview
This AWS Serverless Application Model (SAM) template defines a Lambda function that automatically deletes old CloudFormation stacks based on a time-to-live (TTL) parameter. The function removes stacks that match specific naming patterns (`feat`, `rel`, `hotfix`) and exceed the defined TTL.

## Architecture
- **AWS Lambda**: The function that checks and deletes old CloudFormation stacks.
- **Amazon EventBridge**: Triggers the Lambda function.

## Requirements
- AWS CLI
- AWS SAM CLI
- Python 3.13

## Deployment instructions
1. Clone the repository
   ```bash
   git clone git@github.com:tjrohweder/aws-cleanup.git
   cd aws-cleanup
   ```
---

2. Edit the **DeleteCFNLambdaExecutionRole** located at  `template.yaml` and adjust the lambda permissions according to your needs
```bash
Action:
  - logs:CreateLogGroup
  - logs:CreateLogStream
  - logs:PutLogEvents
  - cloudformation:DeleteStack
  - cloudformation:DescribeStacks
  - cloudformation:ListStacks
Resource: "*"
```
---

3. Build the SAM application
   ```sh
   sam build
   ```
---

4. Deploy the application
   ```bash
   sam deploy --guided
   ```
---


## Environment Variables
- `ttl_minutes`: The number of minutes before a CloudFormation stack should be deleted. This is set through the `TTL` parameter in the template.
---

## Cleanup
Remove deployed resources
```bash
sam delete
```
