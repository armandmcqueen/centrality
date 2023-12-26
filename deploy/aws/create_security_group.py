import boto3
import typer

app = typer.Typer()


@app.command()
def create_security_group(vpc_id: str):
    ec2 = boto3.client('ec2')

    # Create Security Group
    response = ec2.create_security_group(
        Description='Security Group for specific ports',
        GroupName='MySecurityGroup',
        VpcId=vpc_id
    )
    security_group_id = response['GroupId']

    # Add Inbound Rules
    ec2.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {'IpProtocol': 'tcp',
             'FromPort': 8000,
             'ToPort': 8000,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp',
             'FromPort': 8501,
             'ToPort': 8501,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp',
             'FromPort': 5432,
             'ToPort': 5432,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp',
             'FromPort': 22,
             'ToPort': 22,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ]
    )

    print(f"Security Group Created: {security_group_id}")


if __name__ == '__main__':
    app()


