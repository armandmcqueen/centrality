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

from centrality_controlplane_sdk.models.info_response import InfoResponse

class TestInfoResponse(unittest.TestCase):
    """InfoResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> InfoResponse:
        """Test InfoResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `InfoResponse`
        """
        model = InfoResponse()
        if include_optional:
            return InfoResponse(
                git_commit = '',
                git_branch = '',
                git_is_dirty = True,
                deploy_time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f')
            )
        else:
            return InfoResponse(
                git_commit = '',
                git_branch = '',
                git_is_dirty = True,
                deploy_time = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
        )
        """

    def testInfoResponse(self):
        """Test InfoResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()