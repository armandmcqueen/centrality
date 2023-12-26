import boto3
import json

def create_iam_role():
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
        RoleName='EC2SelfTerminationRole',
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
        PolicyName='EC2TerminateSelfPolicy',
        PolicyDocument=json.dumps(policy)
    )
    policy_arn = policy['Policy']['Arn']

    # Attach the policy to the role
    iam.attach_role_policy(
        RoleName='EC2SelfTerminationRole',
        PolicyArn=policy_arn
    )

    print(f"IAM Role Created: {role_arn}")

    # Create an instance profile
    profile_name = 'EC2SelfTerminationInstanceProfile'  # Instance profile name
    iam.create_instance_profile(
        InstanceProfileName=profile_name
    )

    # Add the role to the instance profile
    role_name = 'EC2SelfTerminationRole'  # The name of the IAM role you created
    iam.add_role_to_instance_profile(
        InstanceProfileName=profile_name,
        RoleName=role_name
    )

def delete_all_created_resources():
    iam = boto3.client('iam')

    # Delete the policy
    iam.delete_policy(
        PolicyArn='arn:aws:iam::664043321167:policy/EC2TerminateSelfPolicy'
    )

    # Detach the policy from the role
    iam.detach_role_policy(
        RoleName='EC2SelfTerminationRole',
        PolicyArn='arn:aws:iam::664043321167:policy/EC2TerminateSelfPolicy'
    )

    # Delete the role
    iam.delete_role(
        RoleName='EC2SelfTerminationRole'
    )

    # Delete the instance profile
    iam.delete_instance_profile(
        InstanceProfileName='EC2SelfTerminationInstanceProfile'
    )

create_iam_role()