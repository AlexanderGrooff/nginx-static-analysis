from nginx_analysis.analysis import filter_config
from nginx_analysis.dataclasses import DirectiveFilter, NginxLineConfig
from tests.testcase import TestCase


class TestDirectiveIntegration(TestCase):
    maxDiff = None

    def test_one_user_is_parsed(self):
        root_config = self.get_example_root_conf()
        expected_line = NginxLineConfig(
            line=1, file=root_config.root_file, directive="user", args=["app"]
        )
        user_filters = [DirectiveFilter(directive="user")]
        lines = filter_config(root_config.lines, user_filters)
        self.assertEqual(lines[0], expected_line)

    def test_two_server_names_are_parsed(self):
        root_config = self.get_example_root_conf()
        server_name_filters = [DirectiveFilter(directive="server_name")]
        lines = filter_config(root_config.lines, server_name_filters)
        expected_lines = [
            NginxLineConfig(
                line=2,
                file=root_config.root_dir / "servers/example.com.conf",
                directive="server_name",
                args=["example.com", "www.example.com"],
            ),
            NginxLineConfig(
                line=2,
                file=root_config.root_dir / "servers/testalex.hypernode.io.conf",
                directive="server_name",
                args=["testalex.hypernode.io"],
            ),
        ]
        for line in expected_lines:
            self.assertIn(line, lines)

    def test_one_server_name_is_parsed_for_the_given_value(self):
        root_config = self.get_example_root_conf()
        server_name_filters = [
            DirectiveFilter(directive="server_name", value="example.com")
        ]
        lines = filter_config(root_config.lines, server_name_filters)
        expected_lines = [
            NginxLineConfig(
                line=2,
                file=root_config.root_dir / "servers/example.com.conf",
                directive="server_name",
                args=["example.com", "www.example.com"],
            ),
        ]
        for line in expected_lines:
            self.assertIn(line, lines)

    def test_relative_include_is_caught_from_root_config_prefix(self):
        root_config = self.get_example_root_conf()
        server_name_filters = [
            DirectiveFilter(directive="server_name", value="example.com"),
            DirectiveFilter(directive="location"),
        ]
        lines = filter_config(root_config.lines, server_name_filters)
        expected_lines = [
            NginxLineConfig(
                line=14,
                file=root_config.root_dir / "servers/testalex.hypernode.io.conf",
                directive="include",
                args=["relative_include/relative_include.conf"],
            ),
            NginxLineConfig(
                line=3,
                file=root_config.root_dir / "relative_include/relative_include.conf",
                directive="include",
                args=["relative_include/relative_nested_include.conf"],
            ),
        ]
        for line in expected_lines:
            self.assertIn(line, lines)

    def test_return_line_if_no_filters(self):
        root_config = self.get_example_root_conf()
        expected_line = NginxLineConfig(
            line=1, file=root_config.root_file, directive="user", args=["app"]
        )
        user_filters = []
        lines = filter_config(root_config.lines, user_filters)
        self.assertEqual(lines[0], expected_line)
