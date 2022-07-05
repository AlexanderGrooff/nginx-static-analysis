from nginx_analysis.url import get_port_for_url
from tests.testcase import TestCase


class TestGetPortForURL(TestCase):
    def test_https_port(self):
        self.assertEqual(get_port_for_url("https://example.com"), 443)

    def test_http_port(self):
        self.assertEqual(get_port_for_url("http://example.com"), 80)

    def test_no_port(self):
        self.assertIsNone(get_port_for_url("example.com"))

    def test_specific_port_without_scheme(self):
        self.assertEqual(get_port_for_url("example.com:123"), 123)

    def test_specific_port_with_http(self):
        self.assertEqual(get_port_for_url("http://example.com:123"), 123)

    def test_specific_port_with_https(self):
        self.assertEqual(get_port_for_url("https://example.com:123"), 123)
