from nginx_analysis.analysis import get_lines_matching_filter
from nginx_analysis.dataclasses import CombinedFilters, DirectiveFilter, NginxLineConfig
from tests.testcase import TestCase


class TestGetDirectiveValuesFromLine(TestCase):
    def test_return_empty_list_if_directive_not_found_on_line(self):
        line_config = NginxLineConfig(
            line=1,
            directive="server_name",
            args=["example.com"],
            block=[],
        )
        filters = CombinedFilters(filters=[DirectiveFilter(directive="foo")])
        ret = get_lines_matching_filter(filters, line_config)
        self.assertEqual(ret, [])

    def test_return_current_line(self):
        line_config = NginxLineConfig(
            line=1,
            directive="server_name",
            args=["example.com"],
            block=[],
        )
        filters = CombinedFilters(filters=[DirectiveFilter(directive="server_name")])
        ret = get_lines_matching_filter(filters, line_config)
        self.assertEqual(ret, [line_config])

    def test_return_nested_line(self):
        nested_line = NginxLineConfig(
            line=1,
            directive="server_name",
            args=["example.com"],
            block=[],
        )
        parent_line = NginxLineConfig(
            line=1,
            directive="foo",
            args=[],
            block=[nested_line],
        )
        filters = CombinedFilters(filters=[DirectiveFilter(directive="server_name")])
        ret = get_lines_matching_filter(filters, parent_line)
        self.assertEqual(ret, [nested_line])

    def test_return_parent_and_nested_line(self):
        nested_line = NginxLineConfig(
            line=1,
            directive="server_name",
            args=["example.com"],
            block=[],
        )
        parent_line = NginxLineConfig(
            line=1,
            directive="server_name",
            args=["parent.com"],
            block=[nested_line],
        )
        filters = CombinedFilters(filters=[DirectiveFilter(directive="server_name")])
        ret = get_lines_matching_filter(filters, parent_line)
        self.assertEqual(ret, [parent_line, nested_line])
