from nginx_analysis.dataclasses import CombinedFilters, DirectiveFilter, NginxLineConfig
from tests.testcase import TestCase


class TestCombinedFilters(TestCase):
    def setUp(self) -> None:
        self.line = NginxLineConfig(
            line=1,
            directive="server_name",
            args=["example.com"],
            block=[],
        )
        self.parent_line = NginxLineConfig(
            line=1,
            directive="foo",
            args=[],
            block=[self.line],
        )

    def test_match_returns_true_if_directive_matches_line(self):
        filters = CombinedFilters(filters=[DirectiveFilter(directive="server_name")])
        self.assertTrue(filters.match(self.line))

    def test_match_returns_true_if_directive_and_value_matches_line(self):
        filters = CombinedFilters(
            filters=[DirectiveFilter(directive="server_name", value="example.com")]
        )
        self.assertTrue(filters.match(self.line))

    def test_match_returns_false_if_directive_does_not_match_line(self):
        filters = CombinedFilters(filters=[DirectiveFilter(directive="foo")])
        self.assertFalse(filters.match(self.line))

    def test_match_returns_false_if_directive_matches_but_value_doesnt(self):
        filters = CombinedFilters(
            filters=[DirectiveFilter(directive="server_name", value="foo.com")]
        )
        self.assertFalse(filters.match(self.line))

    def test_match_returns_true_if_first_filter_matches_and_second_doesnt(self):
        filters = CombinedFilters(
            filters=[
                DirectiveFilter(directive="server_name", value="example.com"),
                DirectiveFilter(directive="foo"),
            ]
        )
        self.assertTrue(filters.match(self.line))

    def test_match_returns_false_if_both_filters_dont_match(self):
        filters = CombinedFilters(
            filters=[
                DirectiveFilter(directive="server_name", value="foo.com"),
                DirectiveFilter(directive="foo"),
            ]
        )
        self.assertFalse(filters.match(self.line))

    def test_match_returns_false_if_one_filter_doesnt_match_and_operator_is_all(self):
        filters = CombinedFilters(
            operator=all,
            filters=[
                DirectiveFilter(directive="server_name", value="example.com"),
                DirectiveFilter(directive="foo"),
            ],
        )
        self.assertFalse(filters.match(self.line))

    def test_match_returns_true_if_all_filters_match_and_operator_is_all(self):
        filters = CombinedFilters(
            operator=all,
            filters=[
                DirectiveFilter(directive="server_name"),
                DirectiveFilter(directive="server_name", value="example.com"),
            ],
        )
        self.assertTrue(filters.match(self.line))

    def test_match_returns_true_if_nested_filter_matches(self):
        filters = CombinedFilters(
            filters=[
                DirectiveFilter(directive="server_name", value="example.com"),
                CombinedFilters(
                    operator=any,
                    filters=[
                        DirectiveFilter(directive="server_name"),
                        DirectiveFilter(directive="bar"),
                    ],
                ),
            ]
        )
        self.assertTrue(filters.match(self.line))

    def test_match_returns_true_with_operator_any_if_nested_filter_doesnt_match(self):
        filters = CombinedFilters(
            operator=any,
            filters=[
                DirectiveFilter(directive="server_name", value="example.com"),
                CombinedFilters(
                    operator=any,
                    filters=[
                        DirectiveFilter(directive="bar"),
                    ],
                ),
            ],
        )
        self.assertTrue(filters.match(self.line))
