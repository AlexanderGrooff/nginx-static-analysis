from nginx_analysis.log import get_nginx_logformat
from tests.testcase import TestCase


class TestGetNginxLogformat(TestCase):
    def test_return_default_logformat(self):
        ret = get_nginx_logformat()
        self.assertEqual(
            ret,
            '$remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent"',
        )
