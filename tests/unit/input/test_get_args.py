from unittest import TestCase

from nginx_analysis.input import get_args


class TestGetArgs(TestCase):
    def test_parse_directive(self):
        ret = get_args(["-d", "example"])
        self.assertEqual(ret.directives, ["example"])

    def test_parse_multiple_directives(self):
        ret = get_args(["-d", "example", "-d", "example2"])
        self.assertEqual(ret.directives, ["example", "example2"])

    def test_parse_filter(self):
        ret = get_args(["-f", "example=bla"])
        self.assertEqual(ret.filters, ["example=bla"])

    def test_parse_multiple_filters(self):
        ret = get_args(["-f", "example=bla", "-f", "example2=bla2"])
        self.assertEqual(ret.filters, ["example=bla", "example2=bla2"])
