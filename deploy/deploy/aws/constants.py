SECURITY_GROUP_NAME = "centrality-deploy-security-group"

IAM_ROLE_NAME = 'EC2SelfTerminationRole'
IAM_POLICY_NAME = 'EC2TerminateSelfPolicy'
IAM_PROFILE_NAME = 'EC2SelfTerminationInstanceProfile'

MANAGEMENT_TAG_KEY = "ManagementTag"
MANAGEMENT_TAG_VALUE = "centrality-deploy"

AMI_X64 = "ami-0c7217cdde317cfec"
AMI_ARM = "ami-05d47d29a4c2d19e1"

# Specify whether to use ARM or x64 AMI for each instance type.
INSTANCE_TO_AMI = {
    "m7g.medium": AMI_ARM,
    "m7g.16xlarge": AMI_ARM,
}

# Use a config file other than config.yaml in this folder.
CONFIG_PATH_OVERRIDE_ENVVAR = "AWS_DEPLOY_CONFIG_PATH"
