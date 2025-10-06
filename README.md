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
   ```sh
   git clone git@github.com:tjrohweder/aws-cleanup.git
   cd aws-cleanup
   ```
2. Build the SAM applications
   ```sh
   sam build
   ```
3. Deploy the application
   ```sh
   sam deploy --guided
   ```
   Follow the prompts to configure parameters such as TTL.

## Environment Variables
- `ttl_minutes`: The number of minutes before a CloudFormation stack should be deleted. This is set through the `TTL` parameter in the template.

## Cleanup
Remove the deployed resources
```sh
sam delete
```
