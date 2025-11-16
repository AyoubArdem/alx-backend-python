#!/usr/bin/env python3
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test org property"""
        mock_get_json.return_value = {"payload": True}

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, {"payload": True})

    def test_public_repos_url(self):
        """Test the _public_repos_url property"""
        with patch(
            "client.GithubOrgClient.org",
            new_callable=property(lambda self: {"repos_url": "http://fake.com"})
        ):
            client = GithubOrgClient("google")
            self.assertEqual(client._public_repos_url, "http://fake.com")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos"""
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]

        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=property(lambda self: "http://fake.com")
        ):
            client = GithubOrgClient("google")
            repos = client.public_repos()

            self.assertEqual(repos, ["repo1", "repo2"])
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license"""
        client = GithubOrgClient("google")
        self.assertEqual(client.has_license(repo, license_key), expected)


class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests"""

    @classmethod
    def setUpClass(cls):
        """Start patcher"""
        cls.get_patcher = patch("client.requests.get")
        mock_get = cls.get_patcher.start()

        def side_effect(url):
            mock_response = Mock()
            if "orgs" in url:
                mock_response.json.return_value = org_payload
            else:
                mock_response.json.return_value = repos_payload
            return mock_response

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), expected_repos)

    def test_public_repos_with_license(self):
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos("apache-2.0"), apache2_repos)
