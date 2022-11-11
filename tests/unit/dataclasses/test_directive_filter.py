from nginx_analysis.analysis import get_line_at_linenr
from nginx_analysis.dataclasses import DirectiveFilter
from tests.testcase import TestCase


class TestDirectiveFilter(TestCase):
    def setUp(self) -> None:
        nginx_config = """http {
    server {
        server_name example.com;
        location / {}
        location /foo {
            return 201;
        }
    }
    server {
        server_name alex.com;
        location /bar {}
        location / {
            return 403;
        }
    }
}
"""
        self.root_config = self.load_nginx_config(nginx_config)

    def test_match_server_name(self):
        filter = DirectiveFilter(directive="server_name", value="example.com")
        line = get_line_at_linenr(self.root_config, 3)
        self.assertEqual(filter.match(line), True)
