from nginx_analysis.analysis import get_matching_lines_in_children
from nginx_analysis.dataclasses import DirectiveFilter, NginxLineConfig
from tests.testcase import TestCase


class TestFindMatchesInChildren(TestCase):
    def test_return_empty_list_if_no_children_and_no_match(self):
        line = NginxLineConfig(
            directive="return",
            args=["404"],
            line=1,
        )
        dfilter = DirectiveFilter(directive="location", value="/")
        self.assertEqual(
            get_matching_lines_in_children(line, filters=[dfilter]), ([], [])
        )
        self.assertEqual(
            get_matching_lines_in_children(line, filters=[dfilter]), ([], [])
        )

    def test_return_empty_list_if_args_dont_match(self):
        line = NginxLineConfig(
            directive="return",
            args=["404"],
            line=1,
        )
        dfilter = DirectiveFilter(directive="return", value="123")
        self.assertEqual(
            get_matching_lines_in_children(line, filters=[dfilter]), ([], [])
        )
        self.assertEqual(
            get_matching_lines_in_children(line, filters=[dfilter]), ([], [])
        )

    def test_return_line_if_direct_match(self):
        line = NginxLineConfig(
            directive="return",
            args=["404"],
            line=1,
        )
        dfilter = DirectiveFilter(directive="return", value="404")
        self.assertEqual(
            get_matching_lines_in_children(line, filters=[dfilter]), ([line], [dfilter])
        )

    def test_return_line_if_direct_match_for_one_filter(self):
        line = NginxLineConfig(
            directive="return",
            args=["404"],
            line=1,
        )
        dfilter1 = DirectiveFilter(directive="return", value="404")
        dfilter2 = DirectiveFilter(directive="return", value="405")
        self.assertEqual(
            get_matching_lines_in_children(line, filters=[dfilter1, dfilter2]),
            ([line], [dfilter1]),
        )

    def test_return_parent_and_children_if_match_child(self):
        parent = NginxLineConfig(
            directive="location",
            args=["/"],
            line=1,
        )
        line = NginxLineConfig(
            directive="return",
            args=["404"],
            line=1,
        )
        line.parent = parent
        parent.children.append(line)

        dfilter = DirectiveFilter(directive="return", value="404")
        self.assertEqual(
            get_matching_lines_in_children(parent, filters=[dfilter]),
            ([parent, line], [dfilter]),
        )

    def test_return_parent_and_children_if_match_parent(self):
        parent = NginxLineConfig(
            directive="location",
            args=["/"],
            line=1,
        )
        line = NginxLineConfig(
            directive="return",
            args=["404"],
            line=1,
        )
        line.parent = parent
        parent.children.append(line)

        dfilter = DirectiveFilter(directive="location", value="/")
        self.assertEqual(
            get_matching_lines_in_children(parent, filters=[dfilter]),
            ([parent, line], [dfilter]),
        )
