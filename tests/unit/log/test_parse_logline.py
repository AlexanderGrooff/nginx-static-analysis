from nginx_analysis.log import parse_logline
from tests.testcase import TestCase


class TestParseLogline(TestCase):
    def test_default_logline_contains_http_host(self):
        logline = '66.249.65.159 - - [06/Nov/2014:19:10:38 +0600] "GET /news/53f8d72920ba2744fe873ebc.html HTTP/1.1" 404 177 "-" "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"'
        root_config = self.get_example_root_conf()
        parsed_line = parse_logline(root_config, logline)
        self.assertIsNotNone(parsed_line)
