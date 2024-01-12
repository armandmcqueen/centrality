# coding: utf-8

"""
    centrality-controlplane

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 0.0.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest
import datetime

from centrality_controlplane_sdk.models.gpu_memory_measurement import GpuMemoryMeasurement

class TestGpuMemoryMeasurement(unittest.TestCase):
    """GpuMemoryMeasurement unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> GpuMemoryMeasurement:
        """Test GpuMemoryMeasurement
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `GpuMemoryMeasurement`
        """
        model = GpuMemoryMeasurement()
        if include_optional:
            return GpuMemoryMeasurement(
                machine_id = '',
                ts = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                memory = [
                    centrality_controlplane_sdk.models.gpu_memory.GpuMemory(
                        used_mb = 1.337, 
                        total_mb = 1.337, )
                    ]
            )
        else:
            return GpuMemoryMeasurement(
                machine_id = '',
                ts = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                memory = [
                    centrality_controlplane_sdk.models.gpu_memory.GpuMemory(
                        used_mb = 1.337, 
                        total_mb = 1.337, )
                    ],
        )
        """

    def testGpuMemoryMeasurement(self):
        """Test GpuMemoryMeasurement"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
