from nginx_analysis.dataclasses import AllFilter, DirectiveFilter
from nginx_analysis.filter import logline_to_filter
from tests.testcase import TestCase


class TestLoglineToFilters(TestCase):
    def test_server_name_is_set_as_filter(self):
        parsed_line = {"server_name": "example.com"}
        filters = logline_to_filter(parsed_line)
        self.assertEqual(
            filters,
            AllFilter(
                filters=[DirectiveFilter(directive="server_name", value="example.com")]
            ),
        )

    def test_location_is_parsed_from_request(self):
        parsed_line = {"request": "GET /foo/bar"}
        filters = logline_to_filter(parsed_line)
        self.assertEqual(
            filters,
            AllFilter(
                filters=[DirectiveFilter(directive="location", value="/foo/bar")]
            ),
        )

    def test_unknown_directive_is_ignored(self):
        parsed_line = {"foo": "bar"}
        filters = logline_to_filter(parsed_line)
        self.assertEqual(filters, AllFilter(filters=[]))
