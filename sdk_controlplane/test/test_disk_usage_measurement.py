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

from centrality_controlplane_sdk.models.disk_usage_measurement import DiskUsageMeasurement

class TestDiskUsageMeasurement(unittest.TestCase):
    """DiskUsageMeasurement unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> DiskUsageMeasurement:
        """Test DiskUsageMeasurement
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `DiskUsageMeasurement`
        """
        model = DiskUsageMeasurement()
        if include_optional:
            return DiskUsageMeasurement(
                vm_id = '',
                ts = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                usage = {
                    'key' : centrality_controlplane_sdk.models.disk_usage.DiskUsage(
                        used_mb = 1.337, 
                        total_mb = 1.337, )
                    }
            )
        else:
            return DiskUsageMeasurement(
                vm_id = '',
                ts = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                usage = {
                    'key' : centrality_controlplane_sdk.models.disk_usage.DiskUsage(
                        used_mb = 1.337, 
                        total_mb = 1.337, )
                    },
        )
        """

    def testDiskUsageMeasurement(self):
        """Test DiskUsageMeasurement"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
