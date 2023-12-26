import boto3
import json
import typer
from rich import print
from deploy.aws.config import AwsDeployConfig
from deploy.aws import constants
from pathlib import Path
import os

app = typer.Typer()


CONFIG_FILE_PATH = Path(__file__).parent / "config.yaml"
if constants.CONFIG_PATH_OVERRIDE_ENVVAR in os.environ:
    CONFIG_FILE_PATH = Path(os.environ[constants.CONFIG_PATH_OVERRIDE_ENVVAR])
config = AwsDeployConfig.from_yaml_file(CONFIG_FILE_PATH)


@app.command(
    help=f"Create an IAM policy, role, and instance profile for EC2 instances to terminate themselves"
)
def create():
    iam = boto3.client('iam')

    # Define the trust relationship
    trust_relationship = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "ec2.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }

    # Create the role
    role = iam.create_role(
        RoleName=constants.IAM_ROLE_NAME,
        AssumeRolePolicyDocument=json.dumps(trust_relationship)
    )
    role_arn = role['Role']['Arn']

    # Define the policy
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "ec2:DescribeInstances",
                    "ec2:TerminateInstances"
                ],
                "Resource": "*"
            }
        ]
    }

    # Create the policy
    policy = iam.create_policy(
        PolicyName=constants.IAM_POLICY_NAME,
        PolicyDocument=json.dumps(policy)
    )
    policy_arn = policy['Policy']['Arn']
    print(f"IAM Policy Created: [blue bold]{policy_arn}")

    # Attach the policy to the role
    iam.attach_role_policy(
        RoleName=constants.IAM_ROLE_NAME,
        PolicyArn=policy_arn
    )
    print(f"IAM Role Created: [blue bold]{role_arn}")

    # Create an instance profile
    # Don't save arn because deletion happens by name
    iam.create_instance_profile(
        InstanceProfileName=constants.IAM_PROFILE_NAME
    )

    iam.add_role_to_instance_profile(
        InstanceProfileName=constants.IAM_PROFILE_NAME,
        RoleName=constants.IAM_ROLE_NAME,
    )
    print(f"IAM Instance Profile Created: [blue bold]{constants.IAM_PROFILE_NAME}")

    config.iam_role_arn = role_arn
    config.iam_policy_arn = policy_arn
    config.write_yaml(CONFIG_FILE_PATH)
    print("[green]✓ config.yaml updated")


@app.command(
    help=f"Delete the IAM policy, role, and instance profile created by create_iam_role"
)
def delete():
    iam = boto3.client('iam')

    # Detach the policy from the role
    iam.detach_role_policy(
        RoleName=constants.IAM_ROLE_NAME,
        PolicyArn=config.iam_policy_arn
    )

    # Delete the policy
    iam.delete_policy(
        PolicyArn=config.iam_policy_arn
    )
    print(f"IAM Policy Deleted: [red bold]{config.iam_policy_arn}")

    # Detach role from instance profile
    iam.remove_role_from_instance_profile(
        InstanceProfileName=constants.IAM_PROFILE_NAME,
        RoleName=constants.IAM_ROLE_NAME,
    )

    # Delete the role
    iam.delete_role(
        RoleName=constants.IAM_ROLE_NAME,
    )
    print(f"IAM Role Deleted: [red bold]{config.iam_role_arn}")

    # Delete the instance profile
    iam.delete_instance_profile(
        InstanceProfileName=constants.IAM_PROFILE_NAME,
    )
    print(f"IAM Instance Profile Deleted: [red bold]{constants.IAM_PROFILE_NAME}")

    config.iam_role_arn = ""
    config.iam_policy_arn = ""
    config.write_yaml(CONFIG_FILE_PATH)
    print("[green]✓ config.yaml updated")


if __name__ == '__main__':
    app()