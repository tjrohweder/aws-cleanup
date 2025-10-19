import os
import logging
from datetime import datetime, timedelta, timezone

import boto3
from botocore.exceptions import ClientError

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(), format="%(levelname)s %(message)s"
)
log = logging.getLogger(__name__)


def delete_stacks(ttl_minutes: int) -> str:
    patterns: list[str] = ["feat", "rel", "hotfix"]
    cfn = boto3.client("cloudformation")
    response = cfn.describe_stacks()
    now = datetime.now(timezone.utc)
    delete_threshold = now - timedelta(minutes=ttl_minutes)

    for stack in response.get("Stacks", []):
        stack_name = stack.get("StackName", "")
        stack_creation_time = stack.get("CreationTime")

        if (
            isinstance(stack_creation_time, datetime)
            and stack_creation_time.tzinfo is None
        ):
            stack_creation_time = stack_creation_time.replace(tzinfo=timezone.utc)

        if (
            any(pattern in stack_name for pattern in patterns)
            and isinstance(stack_creation_time, datetime)
            and stack_creation_time > delete_threshold
        ):
            try:
                cfn.delete_stack(StackName=stack_name)
                log.info("Deleted stack: %s", stack_name)
            except ClientError as e:
                err = e.response.get("Error", {})
                log.error(
                    "Failed to delete stack: %s, Error: %s - %s",
                    stack_name,
                    err.get("Code", "ClientError"),
                    err.get("Message", str(e)),
                )
            except Exception as e:
                log.exception(
                    "Failed to delete stack: %s, Unexpected error: %s", stack_name, e
                )

    return "SUCCESS"


def handler(event, context):
    ttl_env = os.environ.get("ttl_minutes")
    if ttl_env is None:
        raise RuntimeError("Environment variable 'ttl_minutes' is required")

    try:
        ttl_minutes = int(ttl_env)
    except ValueError as e:
        raise ValueError("Environment variable 'ttl_minutes' must be an integer") from e

    return delete_stacks(ttl_minutes)
