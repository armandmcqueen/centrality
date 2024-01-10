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

from centrality_controlplane_sdk.models.disk_iops import DiskIops

class TestDiskIops(unittest.TestCase):
    """DiskIops unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> DiskIops:
        """Test DiskIops
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `DiskIops`
        """
        model = DiskIops()
        if include_optional:
            return DiskIops(
                disk_name = '',
                iops = 1.337
            )
        else:
            return DiskIops(
                disk_name = '',
                iops = 1.337,
        )
        """

    def testDiskIops(self):
        """Test DiskIops"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
