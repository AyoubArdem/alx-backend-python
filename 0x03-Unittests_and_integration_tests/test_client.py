from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


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
    
