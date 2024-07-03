#!/usr/bin/env python3
"""some test"""
import unittest
from client import GithubOrgClient
from unittest.mock import PropertyMock, patch
from fixtures import (
        org_payload,
        repos_payload,
        expected_repos,
        apache2_repos
        )
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

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos returns the correct value"""
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = test_payload
        test_url = "https://api.github.com/orgs/google/repos"

        with patch(
                'client.GithubOrgClient._public_repos_url',
                new_callable=PropertyMock) as mock_repos_url:
            mock_repos_url.return_value = test_url

            client = GithubOrgClient("google")
            result = client.public_repos()

            # Check that public_repos returns
            # the correct list of repository names
            self.assertEqual(result, ["repo1", "repo2", "repo3"])

            # Ensure the mocked property and get_json were called once
            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(test_url)


class TestGithubOrgClient(unittest.TestCase):
    """Test case for GithubOrgClient"""

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({"license": {"key": "my_license"}}, "other_license", False),
        ({}, "my_license", False),
        ({"license": None}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected_result):
        """Test GithubOrgClient.has_license returns the correct value"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected_result)


@parameterized_class([
    {"org_payload": org_payload,
     "repos_payload": repos_payload,
     "expected_repos": expected_repos,
     "apache2_repos": apache2_repos}
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test case for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Set up class method to patch requests.get"""
        cls.get_patcher = patch('requests.get')

        # Start the patcher
        cls.mock_get = cls.get_patcher.start()

        # Set up the side effect for the mock
        cls.mock_get.side_effect = cls.get_side_effect

    @classmethod
    def tearDownClass(cls):
        """Tear down class method to stop the patcher"""
        cls.get_patcher.stop()

    @classmethod
    def get_side_effect(cls, url):
        """Side effect function for requests.get"""
        if url == "https://api.github.com/orgs/google":
            return Mock(status_code=200, json=lambda: cls.org_payload)
        elif url == "https://api.github.com/orgs/google/repos":
            return Mock(status_code=200, json=lambda: cls.repos_payload)
        return Mock(status_code=404)

    def test_public_repos(self):
        """Test public_repos method"""
        client = GithubOrgClient("google")
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)
