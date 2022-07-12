from pathlib import Path

from nginx_analysis.analysis import get_directive_matches
from nginx_analysis.dataclasses import NginxLineConfig
from tests.testcase import TestCase


class TestDirectiveIntegration(TestCase):
    maxDiff = None

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
                file=Path("/etc/nginx/servers/example.com.conf"),
                directive="server_name",
                args=["example.com", "www.example.com"],
            ),
            NginxLineConfig(
                line=2,
                file=Path("/etc/nginx/servers/testalex.hypernode.io.conf"),
                directive="server_name",
                args=["testalex.hypernode.io"],
            ),
        ]
        for line in expected_lines:
            self.assertIn(line, lines)

    def test_parent_blocks_are_set_correctly(self):
        root_config = self.get_example_root_conf()
        lines = get_directive_matches(root_config, directive_name="server_name")
        for line in lines:
            self.assertEqual(line.parent.directive, "server")
            self.assertRegex(str(line.parent.file), "/etc/nginx/servers/.*.conf")
            self.assertEqual(line.parent.parent.directive, "include")
            self.assertEqual(str(line.parent.parent.file), "/etc/nginx/nginx.conf")
            self.assertEqual(line.parent.parent.parent.directive, "http")