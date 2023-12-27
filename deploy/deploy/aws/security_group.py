import boto3
import typer
from deploy.aws import constants
from deploy.aws.config import AwsDeployConfig
from pathlib import Path
from rich import print
import os

app = typer.Typer()


config_file_path = Path(__file__).parent / "config.yaml"
if constants.CONFIG_PATH_OVERRIDE_ENVVAR in os.environ:
    CONFIG_FILE_PATH = Path(os.environ[constants.CONFIG_PATH_OVERRIDE_ENVVAR])
config = AwsDeployConfig.from_yaml_file(config_file_path)


@app.command(
    help=f"Create a security group for the Centrality deploy script named {constants.SECURITY_GROUP_NAME}"
)
def create():
    ec2 = boto3.client('ec2')

    # Create Security Group
    response = ec2.create_security_group(
        Description=constants.SECURITY_GROUP_DESCRIPTION,
        GroupName=constants.SECURITY_GROUP_NAME,
        VpcId=config.vpc_id,
    )
    security_group_id = response['GroupId']

    ports = [8000, 8501, 5432, 22]
    ip_permissions = [
        {'IpProtocol': 'tcp',
         'FromPort': port,
         'ToPort': port,
         'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
         } for port in ports
    ]

    # Add Inbound Rules
    ec2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=ip_permissions,
    )

    print(f"Security Group Created: {security_group_id}")
    config.security_group_id = security_group_id
    config.write_yaml(config_file_path)
    print("[green]✓ config.yaml updated")



@app.command(
    help=f"Delete the security group created by create ({constants.SECURITY_GROUP_NAME}))"
)
def delete():
    ec2 = boto3.client('ec2')
    # Delete Security Group
    response = ec2.delete_security_group(
        GroupId=config.security_group_id,
    )

    print(f"Security Group Deleted: {constants.SECURITY_GROUP_NAME}")
    config.security_group_id = ""
    config.write_yaml(config_file_path)
    print("[green]✓ config.yaml updated")


if __name__ == '__main__':
    app()


