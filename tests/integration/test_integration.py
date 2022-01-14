from nginx_analysis.analysis import get_directive_matches
from nginx_analysis.dataclasses import NginxLineConfig
from tests.testcase import TestCase


class TestIntegration(TestCase):
    def test_one_user_is_parsed(self):
        expected_line = NginxLineConfig(
            line=1, file="/etc/nginx/nginx.conf", directive="user", args=["app"]
        )
        root_config = self.get_example_root_conf()
        lines = get_directive_matches(root_config, directive_name="user")
        self.assertEqual(lines[0], expected_line)

    def test_two_server_names_are_parsed(self):
        root_config = self.get_example_root_conf()
        lines = get_directive_matches(root_config, directive_name="server_name")
        expected_lines = [
            NginxLineConfig(
                line=2,
                file="/etc/nginx/servers/example.com.conf",
                directive="server_name",
                args=["example.com", "www.example.com"],
            ),
            NginxLineConfig(
                line=1, file="/etc/nginx/nginx.conf", directive="user", args=["app"]
            ),
        ]
        self.assertEqual(lines, expected_lines)
