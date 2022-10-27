from unittest import TestCase

from nginx_analysis.input import get_args


class TestGetArgs(TestCase):
    def test_parse_directive(self):
        ret = get_args(["directive", "example"])
        self.assertEqual(ret.directives, ["example"])

    def test_parse_multiple_directives(self):
        ret = get_args(["directive", "example", "example2"])
        self.assertEqual(ret.directives, ["example", "example2"])

    def test_parse_value(self):
        ret = get_args(["directive", "example", "--values", "bla"])
        self.assertEqual(ret.directives, ["example"])
        self.assertEqual(ret.values, ["bla"])

    def test_parse_two_directives_one_value(self):
        ret = get_args(["directive", "example", "example2", "--values", "bla"])
        self.assertEqual(ret.directives, ["example", "example2"])
        self.assertEqual(ret.values, ["bla"])

    def test_parse_two_directives_two_values(self):
        ret = get_args(["directive", "example", "example2", "--values", "bla", "bla2"])
        self.assertEqual(ret.directives, ["example", "example2"])
        self.assertEqual(ret.values, ["bla", "bla2"])
