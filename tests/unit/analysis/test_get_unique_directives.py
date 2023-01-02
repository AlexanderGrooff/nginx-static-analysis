from nginx_analysis.analysis import get_unique_directives
from tests.testcase import TestCase


class TestGetUniqueDirectives(TestCase):
    maxDiff = None

    def test_get_unique_directives(self):
        root_config = self.get_example_root_conf()
        self.assertListEqual(
            sorted(get_unique_directives(root_config)),
            [
                "default_type",
                "events",
                "gzip",
                "gzip_disable",
                "gzip_min_length",
                "gzip_proxied",
                "gzip_types",
                "http",
                "include",
                "index",
                "keepalive_timeout",
                "limit_conn_status",
                "limit_req_log_level",
                "limit_req_status",
                "listen",
                "location",
                "map_hash_bucket_size",
                "pid",
                "proxy_pass",
                "return",
                "sendfile",
                "server",
                "server_name",
                "server_names_hash_bucket_size",
                "server_tokens",
                "tcp_nodelay",
                "tcp_nopush",
                "types_hash_max_size",
                "user",
                "worker_connections",
                "worker_processes",
            ],
        )
