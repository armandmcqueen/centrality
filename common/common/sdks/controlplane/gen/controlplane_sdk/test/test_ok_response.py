# coding: utf-8

"""
    centrality-controlplane

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 0.0.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from controlplane_sdk.models.ok_response import OkResponse


class TestOkResponse(unittest.TestCase):
    """OkResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> OkResponse:
        """Test OkResponse
        include_option is a boolean, when False only required
        params are included, when True both required and
        optional params are included"""
        # uncomment below to create an instance of `OkResponse`
        """
        model = OkResponse()
        if include_optional:
            return OkResponse(
                status = 'ok'
            )
        else:
            return OkResponse(
        )
        """

    def testOkResponse(self):
        """Test OkResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == "__main__":
    unittest.main()
