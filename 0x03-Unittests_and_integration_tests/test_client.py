#!/usr/bin/env python3
"""some test"""
import unittest
from client import GithubOrgClient
from unittest.mock import PropertyMock, patch
from parameterized import parameterized


class TestGithubOrgClient(unittest.TestCase):
    """Test case for GithubOrgClient"""

    @parameterized.expand([
        ("google", {
            "name": "google",
            "description": "Google organization"
            }
         ),
        ("abc", {
            "name": "abc",
            "description": "ABC organization"
            }
         ),
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

    @patch("client.GithubOrgClient.org", new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Testing the GithubOrgClient._public_repos_url
        returns the correct value"""
        test_payload = {
                "repos_url": "https://api.github.com/orgs/google/repos"
                }
        mock_org.return_value = test_payload

        client = GithubOrgClient("google")
        result = client._public_repos_url

        self.assertEqual(result, "https://api.github.com/orgs/google/repos")
