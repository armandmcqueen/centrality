import boto3
import os

from rich import print
from rich.console import Console
import time

# TODO: Move these somewhere else
KEY_PAIR = "armand-centrality"
SLEEP_TIME_SECS = 60 * 60 * 5  # 5 hours
IAM_ROLE_ARN = "arn:aws:iam::664043321167:role/EC2SelfTerminationRole"
IAM_INSTANCE_PROFILE_ARN = "arn:aws:iam::664043321167:instance-profile/EC2SelfTerminationInstanceProfile"
SECURITY_GROUP_ID = "sg-021272fb61c189da0"
ami_x64 = "ami-0c7217cdde317cfec"  # TODO: Automatically map instance type to AMI
ami_arm = "ami-05d47d29a4c2d19e1"
INSTANCE_TYPE = 'm7g.medium'
VPC_ID = "vpc-07440ec1153cb2a0b"
SUBNET_ID = "subnet-0b7e0d8e896cb2dc2"
REGION = "us-east-1"
MANAGEMENT_TAG_KEY = "ManagementTag"
MANAGEMENT_TAG_VALUE = "centrality-ttl"

def launch_instance(checkout: str):
    ec2 = boto3.resource('ec2')

    instances = ec2.create_instances(
        # add name
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'centrality-test-instance (ttl)'  # TODO: Better name
                    },
                    {
                        'Key': MANAGEMENT_TAG_KEY,
                        'Value': MANAGEMENT_TAG_VALUE,
                    },
                ]
            },
        ],

        ImageId=ami_arm,
        MinCount=1,
        MaxCount=1,
        InstanceType=INSTANCE_TYPE,
        KeyName=KEY_PAIR,
        IamInstanceProfile={
            'Arn': IAM_INSTANCE_PROFILE_ARN,
        },
        InstanceInitiatedShutdownBehavior='terminate',
        NetworkInterfaces=[
            {
                'AssociatePublicIpAddress': True,
                'DeviceIndex': 0,
                'Groups': [
                    SECURITY_GROUP_ID,
                ],
                'SubnetId': SUBNET_ID,
            },
        ],
        UserData=f'''#!/bin/bash
        
                    # Install repo
                    git clone https://github.com/armandmcqueen/centrality
                    cd centrality
                    git checkout {checkout}
                    echo "Sleeping for {SLEEP_TIME_SECS} seconds..."
                    
                    # Set up docker
                    sudo apt-get update
                    sudo apt-get install -y docker.io
                    sudo curl -L "https://github.com/docker/compose/releases/download/v2.23.3/docker-compose-linux-armv7" -o /usr/local/bin/docker-compose
                    sudo chmod +x /usr/local/bin/docker-compose
                    echo "alias docker-compose='sudo docker-compose'" >> ~/.bashrc
                    sudo docker-compose up -d
                    
                    touch /home/ubuntu/cloud-init-done
                    
                    sleep {SLEEP_TIME_SECS}
                    sudo apt-get update && sudo apt-get install -y awscli
                    aws ec2 terminate-instances --region {REGION} --instance-ids $(curl http://169.254.169.254/latest/meta-data/instance-id)
                  '''
    )
    instance = instances[0]

    console = Console()
    print(f'Launched instance: {instance.id}')
    url = f'https://console.aws.amazon.com/ec2/v2/home?region={REGION}#Instances:instanceId={instance.id}'
    console.print(f"EC2 Instance Console Link: [link={url}]{url}[/link]", style="bold blue")
    print(f'Waiting for instance to be running...')
    instance.wait_until_running()
    print()
    print("[green]Instance is running!")
    print("Startup logs can be found at /var/log/cloud-init-output.log")
    print()
    # Print link to instance dns
    #
    # print()
    instance.load()
    print("The instance is available for SSH, but the cloud-init is probably still running")
    print(f"[blue bold]ssh ubuntu@{instance.public_dns_name} tail -f /var/log/cloud-init-output.log")
    print(f"[blue bold]ssh ubuntu@{instance.public_dns_name}")

    print()
    print("Waiting for cloud-init to finish and API healthcheck to pass (this can take some time)...", end="")

    import requests
    TIMEOUT_SECS = 60 * 3
    start_time = time.time()
    while True:
        if time.time() - start_time > TIMEOUT_SECS:
            raise TimeoutError(f"Healthcheck not reachable after {TIMEOUT_SECS} seconds")

        try:
            # use requests to check if http://instance_dns:8000/healthz returns 200. The server probably isn't running yet
            # so do timeouts and retries. Add a . with no newline after each try to show progress
            # if it fails
            # if it succeeds, break
            health_check_url = f"http://{instance.public_dns_name}:8000/healthz"
            r = requests.get(health_check_url, timeout=1)
            if r.status_code == 200:
                print()
                print()
                print("[green]Healthcheck passed!")
                print(f"UI available at: http://{instance.public_dns_name}:8501")
                break

        except requests.exceptions.ConnectionError:
            print("[yellow].", end="")
            time.sleep(3)
        except Exception as e:
            print()
            print(e)
            raise e

def terminate_all_instances():
    ec2 = boto3.resource('ec2')
    instances = ec2.instances.filter(
        Filters=[
            {
                'Name': 'tag:' + MANAGEMENT_TAG_KEY,
                'Values': [
                    MANAGEMENT_TAG_VALUE,
                ]
            },
        ]
    )
    print("Instances to Terminate:")
    for instance in instances:
        print(f"[red]- {instance.id}")

    print()
    print("Terminating instances...")
    for instance in instances:
        instance.terminate()
        print(f"[green]✓ Termination triggered for: {instance.id}")


if __name__ == "__main__":
    terminate_all_instances()
    # launch_instance(checkout="preview-deployments")
