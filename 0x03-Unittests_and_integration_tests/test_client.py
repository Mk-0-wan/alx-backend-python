#!/usr/bin/env python3
"""some test"""
import unittest
from client import GithubOrgClient
from unittest.mock import  patch
from parameterized import parameterized



class TestGithubOrgClient(unittest.TestCase):
    """Test case for GithubOrgClient"""

    @parameterized.expand([
        ("google", {"name": "google", "description": "Google organization"}),
        ("abc", {"name": "abc", "description": "ABC organization"}),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, expected_response, mock_get_json):
        """Test GithubOrgClient.org returns the correct value"""
        mock_get_json.return_value = expected_response

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
                f"https://api.github.com/orgs/{org_name}"
                )
        self.assertEqual(result, expected_response)
