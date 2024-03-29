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

from centrality_controlplane_sdk.models.network_throughput_measurement import NetworkThroughputMeasurement

class TestNetworkThroughputMeasurement(unittest.TestCase):
    """NetworkThroughputMeasurement unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> NetworkThroughputMeasurement:
        """Test NetworkThroughputMeasurement
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `NetworkThroughputMeasurement`
        """
        model = NetworkThroughputMeasurement()
        if include_optional:
            return NetworkThroughputMeasurement(
                machine_id = '',
                ts = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                per_interface = [
                    centrality_controlplane_sdk.models.throughput.Throughput(
                        interface_name = '', 
                        sent_mbps = 1.337, 
                        recv_mbps = 1.337, )
                    ],
                total = centrality_controlplane_sdk.models.throughput.Throughput(
                    interface_name = '', 
                    sent_mbps = 1.337, 
                    recv_mbps = 1.337, )
            )
        else:
            return NetworkThroughputMeasurement(
                machine_id = '',
                ts = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                per_interface = [
                    centrality_controlplane_sdk.models.throughput.Throughput(
                        interface_name = '', 
                        sent_mbps = 1.337, 
                        recv_mbps = 1.337, )
                    ],
                total = centrality_controlplane_sdk.models.throughput.Throughput(
                    interface_name = '', 
                    sent_mbps = 1.337, 
                    recv_mbps = 1.337, ),
        )
        """

    def testNetworkThroughputMeasurement(self):
        """Test NetworkThroughputMeasurement"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
