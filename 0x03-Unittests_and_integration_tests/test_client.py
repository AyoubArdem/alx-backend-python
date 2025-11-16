#!/usr/bin/env python3
"""
Unittests for GithubOrgClient.
Ensures documentation, correct indentation, and pycodestyle compatibility.
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import (
    org_payload,
    repos_payload,
    expected_repos,
    apache2_repos
)


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient."""

    @parameterized.expand([
        ("google", {"payload": True}),
        ("abc", {"payload": False}),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, expected_payload, mock_get_json):
        """Test the org() method."""
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, expected_payload)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    @patch("client.GithubOrgClient.org", new_callable=property)
    def test_public_repos_url(self, mock_org):
        """Test the _public_repos_url property."""
        mock_org.return_value = {"repos_url": "http://fake-url.com"}

        client = GithubOrgClient("google")
        self.assertEqual(client._public_repos_url, "http://fake-url.com")

    @patch("client.get_json")
    @patch(
        "client.GithubOrgClient._public_repos_url",
        new_callable=property
    )
    def test_public_repos(self, mock_url, mock_get_json):
        """Test public_repos() with mocked URL and JSON."""
        mock_url.return_value = "http://fake-url.com"
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]

        client = GithubOrgClient("google")
        repos = client.public_repos()

        self.assertEqual(repos, ["repo1", "repo2"])
        mock_get_json.assert_called_once_with("http://fake-url.com")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test license checking."""
        client = GithubOrgClient("google")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests with patched requests.get."""

    @classmethod
    def setUpClass(cls):
        """Start the requests.get patcher."""
        cls.get_patcher = patch("client.requests.get")
        mock_get = cls.get_patcher.start()

        def side_effect(url):
            mock_response = Mock()
            if "orgs" in url:
                mock_response.json.return_value = cls.org_payload
            else:
                mock_response.json.return_value = cls.repos_payload
            return mock_response

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the requests.get patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos() integration."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test filter by license integration."""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos("apache-2.0"),
            self.apache2_repos
        )
