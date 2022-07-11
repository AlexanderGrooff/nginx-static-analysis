import re

from nginx_analysis.log import logformat_to_regex_pattern
from tests.testcase import TestCase


class TestLogformatToRegexPattern(TestCase):
    def test_empty_line_to_empty_pattern(self):
        self.assertEqual(logformat_to_regex_pattern(""), re.compile(""))

    def test_variable_to_named_regex(self):
        self.assertEqual(
            logformat_to_regex_pattern("Host: $http_host"),
            re.compile(r"Host:\ (?P<http_host>.*)"),
        )

    def test_multiple_variables_to_named_regex(self):
        self.assertEqual(
            logformat_to_regex_pattern("Host: $http_host User-Agent: $http_user_agent"),
            re.compile(
                r"Host:\ (?P<http_host>.*)\ User\-Agent:\ (?P<http_user_agent>.*)"
            ),
        )
