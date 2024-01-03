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

from centrality_controlplane_sdk.models.cpu_measurement import CpuMeasurement

class TestCpuMeasurement(unittest.TestCase):
    """CpuMeasurement unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> CpuMeasurement:
        """Test CpuMeasurement
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `CpuMeasurement`
        """
        model = CpuMeasurement()
        if include_optional:
            return CpuMeasurement(
                vm_id = '',
                ts = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                cpu_percents = [
                    1.337
                    ]
            )
        else:
            return CpuMeasurement(
                vm_id = '',
                ts = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                cpu_percents = [
                    1.337
                    ],
        )
        """

    def testCpuMeasurement(self):
        """Test CpuMeasurement"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()