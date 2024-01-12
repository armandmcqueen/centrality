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

from centrality_controlplane_sdk.models.disk_throughput_measurement import DiskThroughputMeasurement

class TestDiskThroughputMeasurement(unittest.TestCase):
    """DiskThroughputMeasurement unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> DiskThroughputMeasurement:
        """Test DiskThroughputMeasurement
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `DiskThroughputMeasurement`
        """
        model = DiskThroughputMeasurement()
        if include_optional:
            return DiskThroughputMeasurement(
                machine_id = '',
                ts = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                throughput = [
                    centrality_controlplane_sdk.models.disk_throughput.DiskThroughput(
                        disk_name = '', 
                        read_mbps = 1.337, 
                        write_mbps = 1.337, )
                    ]
            )
        else:
            return DiskThroughputMeasurement(
                machine_id = '',
                ts = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                throughput = [
                    centrality_controlplane_sdk.models.disk_throughput.DiskThroughput(
                        disk_name = '', 
                        read_mbps = 1.337, 
                        write_mbps = 1.337, )
                    ],
        )
        """

    def testDiskThroughputMeasurement(self):
        """Test DiskThroughputMeasurement"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
