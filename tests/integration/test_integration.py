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
