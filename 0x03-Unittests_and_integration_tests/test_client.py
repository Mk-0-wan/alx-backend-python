#!/usr/bin/env python3
"""some test for the client.py file"""
from parameterized import parameterized, parameterized_class
import unittest
from unittest.mock import PropertyMock, patch, Mock
from fixtures import TEST_PAYLOAD
from client import GithubOrgClient


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


@parameterized_class(
    ("org_payload",
     "repos_payload",
     "expected_repos",
     "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test case for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Set up class method to patch requests.get"""
        def get_side_effect(url):
            """Side effect function for requests.get"""
            res_mock = Mock()
            if url == "https://api.github.com/orgs/google":
                res_mock.json.side_effect = lambda: cls.org_payload
            elif url == "https://api.github.com/orgs/google/repos":
                res_mock.json.side_effect = lambda: cls.repos_payload
            else:
                res_mock.json.side_effect = lambda: None
            return res_mock

        cls.get_patcher = patch(
                'requests.get',
                side_effect=cls.get_side_effect)

        # Start the patcher
        cls.mock_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Tear down class method to stop the patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos method"""
        client = GithubOrgClient("google")
        repos = client.public_repos()
        self.assertEqual(client.org, self.org_payload)
        self.assertEqual(client.repos_payload, self.repos_payload)
        self.assertEqual(repos, self.expected_repos)
        self.mock_get.assert_called()

    def test_public_repos_with_license(self):
        """Test public_repos method with license argument"""
        client = GithubOrgClient("google")
        repos = client.public_repos()
        expected_apache_repos = client.public_repos('apache-2.0')
        expected_repos_with_license = self.apache2_repos
        self.assertEqual(expected_apache_repos, expected_repos_with_license)
        self.assertEqual(repos, self.expected_repos)
        self.mock_get.assert_called()
