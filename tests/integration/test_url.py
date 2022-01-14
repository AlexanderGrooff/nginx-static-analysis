from nginx_analysis.url import get_server_config_for_url
from tests.testcase import TestCase


class TestURLIntegration(TestCase):
    def test_specific_http_url_matches(self):
        root_config = self.get_example_root_conf()
        server_config = get_server_config_for_url("http://example.com", root_config)
        self.assertEqual(str(server_config.file), "/etc/nginx/servers/example.com.conf")
        self.assertEqual(server_config.line, 1)

    def test_specific_https_url_matches(self):
        root_config = self.get_example_root_conf()
        server_config = get_server_config_for_url("https://example.com", root_config)
        self.assertEqual(str(server_config.file), "/etc/nginx/servers/example.com.conf")
        self.assertEqual(server_config.line, 1)

    def test_port_without_listen_directive_has_no_matches(self):
        root_config = self.get_example_root_conf()
        server_config = get_server_config_for_url(
            "http://example.com:12345", root_config
        )
        self.assertIsNone(server_config)

    def test_random_servername_matches_default_server(self):
        root_config = self.get_example_root_conf()
        server_config = get_server_config_for_url(
            "http://blablablablabla.bla", root_config
        )
        self.assertEqual(
            str(server_config.file), "/etc/nginx/servers/testalex.hypernode.io.conf"
        )
        self.assertEqual(server_config.line, 1)
