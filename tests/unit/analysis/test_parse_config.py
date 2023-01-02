from nginx_analysis.analysis import get_directive_matches
from tests.testcase import TestCase


class TestParseConfig(TestCase):
    def test_parent_is_set_on_include_block(self):
        root_config = self.get_example_root_conf()
        include_lines = get_directive_matches(root_config.lines, ["include"])
        self.assertGreater(len(include_lines), 0)
        for include_line in include_lines:
            self.assertEqual(include_line.directive, "include")
            self.assertGreater(len(include_line.children), 0)
            for child in include_line.children:
                self.assertEqual(child.parent, include_line)

    def test_http_has_no_parent(self):
        root_config = self.get_example_root_conf()
        http_lines = get_directive_matches(root_config.lines, ["http"])
        self.assertEqual(len(http_lines), 1)
        self.assertIsNone(http_lines[0].parent)

    def test_include_parent_is_http(self):
        root_config = self.get_example_root_conf()
        include_lines = get_directive_matches(root_config.lines, ["include"])
        self.assertGreater(len(include_lines), 0)
        for include_line in include_lines:
            self.assertEqual(include_line.parent.directive, "http")

    def test_include_has_no_block(self):
        root_config = self.get_example_root_conf()
        include_lines = get_directive_matches(root_config.lines, ["include"])
        self.assertGreater(len(include_lines), 0)
        for include_line in include_lines:
            self.assertIsNone(include_line.block)

    def test_http_has_block(self):
        root_config = self.get_example_root_conf()
        http_lines = get_directive_matches(root_config.lines, ["http"])
        self.assertEqual(len(http_lines), 1)
        self.assertIsNotNone(http_lines[0].block)

    def test_server_has_block(self):
        root_config = self.get_example_root_conf()
        server_lines = get_directive_matches(root_config.lines, ["server"])
        self.assertGreater(len(server_lines), 0)
        for server_line in server_lines:
            self.assertIsNotNone(server_line.block)

    def test_location_has_block(self):
        root_config = self.get_example_root_conf()
        location_lines = get_directive_matches(root_config.lines, ["location"])
        self.assertGreater(len(location_lines), 0)
        for location_line in location_lines:
            self.assertIsNotNone(location_line.block)
