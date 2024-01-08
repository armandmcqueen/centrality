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

from centrality_controlplane_sdk.models.disk_iops_measurement import DiskIopsMeasurement

class TestDiskIopsMeasurement(unittest.TestCase):
    """DiskIopsMeasurement unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> DiskIopsMeasurement:
        """Test DiskIopsMeasurement
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `DiskIopsMeasurement`
        """
        model = DiskIopsMeasurement()
        if include_optional:
            return DiskIopsMeasurement(
                vm_id = '',
                ts = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                iops = {
                    'key' : 1.337
                    }
            )
        else:
            return DiskIopsMeasurement(
                vm_id = '',
                ts = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                iops = {
                    'key' : 1.337
                    },
        )
        """

    def testDiskIopsMeasurement(self):
        """Test DiskIopsMeasurement"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
