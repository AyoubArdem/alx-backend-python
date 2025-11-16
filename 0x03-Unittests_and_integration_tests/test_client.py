python
#!/usr/bin/env python3
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient
from parameterized import parameterized_class
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos

class TestGithubOrgClient(unittest.TestCase):
  
  @parameterized.expand([
        ("google", {"payload": True}),
        ("abc", {"payload": False})
    ])
    @patch("client.get_json")
    def test_org(self, org_name, expected_payload, mock_get_json):
             mock_get_json.return_value = expected_payload

             client = GithubOrgClient(org_name)
             result = client.org

             self.assertEqual(result, expected_payload)
             mock_get_json.assert_called_once_with (
                         f"https://api.github.com/orgs/{org_name}"
          )
   '''#############################################################################'''
   '''methode 1'''
   @parameterized.expand([
       ("google",http://fake-url-1.com),
        ("abc", http://fake-url-2.com),
   ])  
   @patch(client.org)
   def test_public_repo_url(self,org_name,expected_url,mock_get_json):
                 mock_get_json.return_value = expected_url
                 client = GithubOrgClient(org_name)
                 result = client._public_repo_url
                 self.assertEqual(result,expected_url)
     
    '''methode 2'''
    def test_public_repos_url(self):
        with patch("client.GithubOrgClient.org", 
                   new_callable=property(lambda self: {"repos_url": "http://fake-url.com"})):
            client = GithubOrgClient("google")
            self.assertEqual(client._public_repos_url, "http://fake-url.com")
    '''#############################################################################'''

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]

        with patch("client.GithubOrgClient._public_repos_url", 
                   new_callable=property(lambda self: "http://fake-url.com")):
            client = GithubOrgClient("google")
            repos = client.public_repos()

        self.assertEqual(repos, ["repo1", "repo2"])
        mock_get_json.assert_called_once()


    @parameterized.expand([
       ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
          
        client = GithubOrgClient("google")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)

    
 

@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(TestCase):

    @classmethod
    def setUpClass(cls):
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
        cls.get_patcher.stop()

    def test_public_repos(self):
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)
