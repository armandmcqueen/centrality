from common.config.config import CentralityConfig
from typing import Optional
from pydantic import model_validator


class AwsDeployConfig(CentralityConfig):
    region: str = ""
    vpc_id: str = ""
    subnet_id: str = ""
    key_pair: str = ""

    security_group_id: str = ""
    iam_role_arn: str = ""
    iam_policy_arn: str = ""

    @model_validator(mode="after")
    def validate_core_fields(self):
        for field in ["region", "vpc_id", "subnet_id", "key_pair"]:
            if not getattr(self, field):
                raise ValueError(f"Missing required field {field}")
        return self

    def validate_full_config_set(self):
        for field in self.model_fields.keys():
            if not getattr(self, field):
                raise ValueError(f"Missing required field {field}")
        return self

