import boto3

from rich import print
from typing import Optional
import time
import typer
from deploy.aws.config import AwsDeployConfig
from deploy.aws import constants
from pathlib import Path
import requests
from rich.console import Console
import subprocess
import os

CONFIG_FILE_PATH = Path(__file__).parent / "config.yaml"
if constants.CONFIG_PATH_OVERRIDE_ENVVAR in os.environ:
    CONFIG_FILE_PATH = Path(os.environ[constants.CONFIG_PATH_OVERRIDE_ENVVAR])
config = AwsDeployConfig.from_yaml_file(CONFIG_FILE_PATH)


app = typer.Typer()


def get_log_lines(host: str) -> list[str]:
    """Get all non-empty lines from /var/log/cloud-init-output.log"""
    out = subprocess.check_output(
        f"ssh ubuntu@{host} cat /var/log/cloud-init-output.log",
        shell=True,
        stderr=subprocess.DEVNULL,
    )
    lines = out.decode("utf-8").splitlines()
    return [line for line in lines if line.strip() != ""]


def _launch(
    instance_type: str,
    checkout: str,
    ttl_secs: int,
    wait: bool,
    idempotency_token: Optional[str] = None,
):
    """
    Launch an instance with the specified checkout (branch, tag, or commit hash). Will launch the instance,
    set the cloud-init script to checkout code and download docker compose, and then terminate itself after
    ttl_secs. If wait is True, will wait for the instance to be running and the API healthcheck to pass, while
    tailing the cloud-init logs.
    """
    # Validate config
    print()
    print("Checking config fully set...")
    try:
        config.validate_full_config_set()
    except ValueError as e:
        print(e)
        print(
            "Not all config values are set. Did you create the security group and IAM resources?"
        )
        return
    print("[green]✓[/green] Config fully set")
    print()

    # Get appropriate AMI for architecture
    if instance_type not in constants.INSTANCE_TO_AMI:
        raise ValueError(
            f"Instance type {instance_type} architecture not currently known (add it to "
            "INSTANCE_TO_AMI in constants.py)"
        )
    ami = constants.INSTANCE_TO_AMI[instance_type]
    if ami != constants.AMI_ARM:
        raise NotImplementedError(
            "Only ARM instances are currently supported because the cloud-init "
            "script hardcodes downloading the ARM docker-compose binary. This is "
            "easy to fix, but just needs someone to test out a non-ARM instance "
            "and update the script to be correct."
        )

    ec2 = boto3.resource("ec2")
    iam = boto3.client("iam")

    # Get the instance profile ARN since we only save the Name. TODO: Check if we can just use name?
    instance_profile = iam.get_instance_profile(
        InstanceProfileName=constants.IAM_PROFILE_NAME
    )
    instance_profile_arn = instance_profile["InstanceProfile"]["Arn"]

    instances_name = "centrality-deploy"
    if idempotency_token is not None:
        instances_name += f"-{idempotency_token}"

    tags = [
        {
            "Key": "Name",
            "Value": instances_name,
        },
        {
            "Key": constants.MANAGEMENT_TAG_KEY,
            "Value": constants.MANAGEMENT_TAG_VALUE,
        },
    ]
    if idempotency_token is not None:
        tags.append(
            {
                "Key": constants.IDEMPOTENCY_TAG_KEY,
                "Value": idempotency_token,
            }
        )

    instances = ec2.create_instances(
        TagSpecifications=[
            {"ResourceType": "instance", "Tags": tags},
        ],
        ImageId=ami,
        MinCount=1,
        MaxCount=1,
        InstanceType=instance_type,
        KeyName=config.key_pair,
        IamInstanceProfile={
            "Arn": instance_profile_arn,
        },
        InstanceInitiatedShutdownBehavior="terminate",
        NetworkInterfaces=[
            {
                "AssociatePublicIpAddress": True,
                "DeviceIndex": 0,
                "Groups": [
                    config.security_group_id,
                ],
                "SubnetId": config.subnet_id,
            },
        ],
        UserData=f"""#!/bin/bash
        
                    # Install repo
                    git clone https://github.com/armandmcqueen/centrality
                    cd centrality
                    git checkout {checkout}
                    
                    
                    # Set up docker
                    sudo apt-get update
                    sudo apt-get install -y docker.io
                    sudo curl -L \
                    "https://github.com/docker/compose/releases/download/v2.23.3/docker-compose-linux-armv7" \
                    -o /usr/local/bin/docker-compose
                    sudo chmod +x /usr/local/bin/docker-compose
                    echo "alias docker-compose='sudo docker-compose'" >> ~/.bashrc
                    sudo docker-compose up -d
                    
                    touch /home/ubuntu/cloud-init-done
                    echo "Sleeping for {ttl_secs} seconds..."
                    sleep {ttl_secs}
                    sudo apt-get update && sudo apt-get install -y awscli
                    aws ec2 terminate-instances --region {config.region} --instance-ids $(curl http://169.254.169.254/latest/meta-data/instance-id)
                  """,
    )
    instance = instances[0]

    console = Console()
    print(f"Launched instance: {instance.id}")
    url = f"https://console.aws.amazon.com/ec2/v2/home?region={config.region}#Instances:instanceId={instance.id}"
    console.print(
        f"EC2 Instance Console Link: [link={url}]{url}[/link]", style="bold blue"
    )

    if wait:
        print()
        print("Waiting for instance to be running...")
        instance.wait_until_running()
        instance.load()
        print()
        print("[green bold]Instance is running!")
        print("Startup logs can be found at [pink bold]/var/log/cloud-init-output.log")
        print()
        print(
            "The instance is available for SSH, but the cloud-init is probably still running"
        )
        print(
            f"[bright_black]ssh ubuntu@{instance.public_dns_name} tail -f /var/log/cloud-init-output.log"
        )
        print(f"[bright_black]ssh ubuntu@{instance.public_dns_name}")
        print()

        health_check_url = f"http://{instance.public_dns_name}:8000/healthz"
        start_time = time.time()
        logs = []
        log_index = 0
        print(
            "[blue bold]Waiting for cloud-init to finish and API healthcheck to pass "
            "(this can take some time)..."
        )
        print("Tailing logs:")
        while True:
            try:
                logs = get_log_lines(instance.public_dns_name)
            except Exception:
                pass

            logs_to_print = logs[log_index:]
            for log in logs_to_print:
                out = f"[#a570bc]/var/log/cloud-init-output.log[/#a570bc] | {log}]"
                print(out)
                log_index += 1

            if time.time() - start_time > constants.INSTANCE_HEALTHCHECK_PATIENCE_SECS:
                raise TimeoutError(
                    f"Healthcheck not reachable after {constants.INSTANCE_HEALTHCHECK_PATIENCE_SECS} seconds"
                )
            try:
                r = requests.get(health_check_url, timeout=0.5)
                if r.status_code == 200:
                    print()
                    print(
                        f"[green]Healthcheck passed after {round(time.time() - start_time, 2)} seconds!"
                    )
                    print(f"UI available at: http://{instance.public_dns_name}:8501")
                    break

            except requests.exceptions.ConnectionError:
                pass
            except Exception as e:
                print()
                print(e)
                raise e


@app.command(
    help="Launch a Centrality instance with the specified checkout (branch, tag, or commit hash)"
)
def launch(
    instance_type: str,
    checkout: str = "main",
    ttl_secs: int = constants.INSTANCE_DEFAULT_TTL,
    wait: bool = True,
    idempotency_token: Optional[str] = None,
):
    delete(wait=False, idempotency_token=idempotency_token)
    print("[green bold]✓ Termination triggered for all instances")
    _launch(
        instance_type=instance_type,
        checkout=checkout,
        ttl_secs=ttl_secs,
        wait=wait,
        idempotency_token=idempotency_token,
    )


@app.command()
def delete(wait: bool = True, idempotency_token: Optional[str] = None):
    ec2 = boto3.resource("ec2")
    filters = [
        {
            "Name": "tag:" + constants.MANAGEMENT_TAG_KEY,
            "Values": [
                constants.MANAGEMENT_TAG_VALUE,
            ],
        },
    ]
    if idempotency_token is not None:
        filters.append(
            {
                "Name": f"tag:{constants.IDEMPOTENCY_TAG_KEY}",
                "Values": [
                    idempotency_token,
                ],
            }
        )
    instances = ec2.instances.filter(Filters=filters)
    print("Instances to Terminate:")
    for instance in instances:
        print(f"[red]- {instance.id}")

    print()
    print("Terminating instances...")
    for instance in instances:
        instance.terminate()
        print(f"[green]✓[/green] Termination triggered for: {instance.id}")

    if wait:
        print()
        print("Waiting for instances to terminate...")
        for instance in instances:
            instance.wait_until_terminated()
            print(f"[green]✓[/green] Instance terminated: [strike]{instance.id}")

        print()
        print("[green bold]✓ All instances terminated")


if __name__ == "__main__":
    app()
