import re

from nginx_analysis.analysis import nginx_to_regex
from tests.testcase import TestCase


class TestNginxToRegex(TestCase):
    def test_regular_string_doesnt_change(self):
        ret = nginx_to_regex("test")
        self.assertEqual(ret, "test")

    def test_wildcard_only_matches_that_directory(self):
        regex = nginx_to_regex("*.conf")
        self.assertTrue(re.match(regex, "test.conf"))
        self.assertFalse(re.match(regex, "test/test.conf"))
