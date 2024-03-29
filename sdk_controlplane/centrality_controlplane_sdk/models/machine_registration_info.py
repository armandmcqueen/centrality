# coding: utf-8

"""
    centrality-controlplane

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 0.0.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Any, ClassVar, Dict, List, Optional
from pydantic import BaseModel, StrictInt, StrictStr
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

class MachineRegistrationInfo(BaseModel):
    """
    Information about a machine to register with the control plane.  Same as machine heartbeat, but without a few fields that are either set via URL params or automatically set server-side.
    """ # noqa: E501
    num_cpus: StrictInt
    cpu_description: StrictStr
    host_memory_mb: StrictInt
    num_gpus: StrictInt
    gpu_type: Optional[StrictStr]
    gpu_memory_mb: Optional[StrictInt]
    nvidia_driver_version: Optional[StrictStr]
    hostname: StrictStr
    __properties: ClassVar[List[str]] = ["num_cpus", "cpu_description", "host_memory_mb", "num_gpus", "gpu_type", "gpu_memory_mb", "nvidia_driver_version", "hostname"]

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True
    }


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of MachineRegistrationInfo from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        _dict = self.model_dump(
            by_alias=True,
            exclude={
            },
            exclude_none=True,
        )
        # set to None if gpu_type (nullable) is None
        # and model_fields_set contains the field
        if self.gpu_type is None and "gpu_type" in self.model_fields_set:
            _dict['gpu_type'] = None

        # set to None if gpu_memory_mb (nullable) is None
        # and model_fields_set contains the field
        if self.gpu_memory_mb is None and "gpu_memory_mb" in self.model_fields_set:
            _dict['gpu_memory_mb'] = None

        # set to None if nvidia_driver_version (nullable) is None
        # and model_fields_set contains the field
        if self.nvidia_driver_version is None and "nvidia_driver_version" in self.model_fields_set:
            _dict['nvidia_driver_version'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of MachineRegistrationInfo from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "num_cpus": obj.get("num_cpus"),
            "cpu_description": obj.get("cpu_description"),
            "host_memory_mb": obj.get("host_memory_mb"),
            "num_gpus": obj.get("num_gpus"),
            "gpu_type": obj.get("gpu_type"),
            "gpu_memory_mb": obj.get("gpu_memory_mb"),
            "nvidia_driver_version": obj.get("nvidia_driver_version"),
            "hostname": obj.get("hostname")
        })
        return _obj


