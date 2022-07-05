from nginx_analysis.url import get_server_configs_for_url
from tests.testcase import TestCase


class TestURLIntegration(TestCase):
    def test_specific_http_url_matches(self):
        root_config = self.get_example_root_conf()
        server_configs = get_server_configs_for_url("http://example.com", root_config)
        self.assertEqual(len(server_configs), 1)
        server_config = server_configs[0]
        self.assertEqual(str(server_config.file), "/etc/nginx/servers/example.com.conf")
        self.assertEqual(server_config.line, 1)

    def test_specific_https_url_matches(self):
        root_config = self.get_example_root_conf()
        server_configs = get_server_configs_for_url("https://example.com", root_config)
        self.assertEqual(len(server_configs), 1)
        server_config = server_configs[0]
        self.assertEqual(str(server_config.file), "/etc/nginx/servers/example.com.conf")
        self.assertEqual(server_config.line, 1)

    def test_port_without_listen_directive_has_no_matches(self):
        root_config = self.get_example_root_conf()
        server_configs = get_server_configs_for_url(
            "http://example.com:12345", root_config
        )
        self.assertEqual(server_configs, [])

    def test_random_servername_matches_default_server(self):
        root_config = self.get_example_root_conf()
        server_configs = get_server_configs_for_url(
            "http://blablablablabla.bla", root_config
        )
        self.assertEqual(len(server_configs), 1)
        server_config = server_configs[0]
        self.assertEqual(
            str(server_config.file), "/etc/nginx/servers/testalex.hypernode.io.conf"
        )
        self.assertEqual(server_config.line, 1)

    def test_url_without_scheme_matches_all_ports(self):
        root_config = self.get_example_root_conf()
        server_configs = get_server_configs_for_url("example.com", root_config)
        self.assertEqual(len(server_configs), 4)

        # Ports 80, 443, 8080, and 8443
        expected_configs = [
            ["/etc/nginx/servers/example.com.conf", 1],
            ["/etc/nginx/servers/example.com.conf", 1],
            ["/etc/nginx/servers/example.com.conf", 1],
            ["/etc/nginx/servers/example.com.conf", 1],
        ]
        for s, e in zip(server_configs, expected_configs):
            self.assertEqual(str(s.file), e[0])
            self.assertEqual(s.line, e[1])
