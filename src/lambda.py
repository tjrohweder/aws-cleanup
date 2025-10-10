import boto3
import os
from datetime import datetime, timedelta, timezone


def delete_stacks(ttl_minutes):
    patterns = ["feat", "rel", "hotfix"]
    cfn = boto3.client("cloudformation")
    response = cfn.describe_stacks()
    now = datetime.now(timezone.utc)
    delete_threshold = now - timedelta(minutes=ttl_minutes)

    for stack in response["Stacks"]:
        stack_name = stack["StackName"]
        stack_creation_time = stack["CreationTime"]

        if stack_creation_time.tzinfo is None:
            stack_creation_time = stack_creation_time.replace(tzinfo=timezone.utc)

        if (
            any(pattern in stack_name for pattern in patterns)
            and stack_creation_time > delete_threshold
        ):
            try:
                cfn.delete_stack(StackName=stack_name)
                print(f"Deleted stack: {stack_name}")
            except Exception as e:
                print(f"Failed to delete stack: {stack_name}, Error: {str(e)}")

    return "SUCCESS"


def handler(event, context):
    ttl_minutes = int(os.environ["ttl_minutes"])
    return delete_stacks(ttl_minutes)
