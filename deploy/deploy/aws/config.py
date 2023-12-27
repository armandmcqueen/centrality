from common.config.config import CentralityConfig
from pydantic import model_validator


class AwsDeployConfig(CentralityConfig):
    """
    Configuration for deploying a VM to AWS. The first set of fields must be set manually by the user.

    The second set of fields are automatically updated and saved by the creation scripts. CentralityConfig
    doesn't support optional fields, so we use an empty string to represent an unset value and then have
    some custom validation logic to ensure that all fields are set when they need to be.
    """

    # Manually set fields
    region: str = ""
    vpc_id: str = ""
    subnet_id: str = ""
    key_pair: str = ""

    # Automatically managed fields
    security_group_id: str = ""
    iam_role_arn: str = ""
    iam_policy_arn: str = ""

    @model_validator(mode="after")
    def validate_core_fields(self):
        """Check that all required fields are set"""
        for field in ["region", "vpc_id", "subnet_id", "key_pair"]:
            if not getattr(self, field):
                raise ValueError(f"Missing required field {field}")
        return self

    def validate_full_config_set(self):
        """
        Check that all fields are set. This is used when launching instances to make sure the
        IAM and security group resources were created first.
        """
        for field in self.model_fields.keys():
            val = getattr(self, field)
            if val == "":
                raise ValueError(f"Missing required field {field}")
        return self
