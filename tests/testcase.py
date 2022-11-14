from tempfile import NamedTemporaryFile
from unittest import TestCase as BaseTestCase
from unittest.mock import Mock, mock_open, patch

from nginx_analysis.analysis import parse_config
from nginx_analysis.dataclasses import RootNginxConfig


class TestCase(BaseTestCase):
    def set_up_patch(self, topatch, themock=None, **kwargs) -> Mock:
        """
        Patch a function or class
        :param topatch: string The class to patch
        :param themock: optional object to use as mock
        :return: mocked object
        """
        if themock is None:
            themock = Mock(**kwargs)

        patcher = patch(topatch, themock)
        self.addCleanup(patcher.stop)
        return patcher.start()

    def set_up_mock_open(self, read_value=""):
        return self.set_up_patch("builtins.open", mock_open(read_data=read_value))

    def get_example_root_conf(self, file="/etc/nginx/nginx.conf") -> RootNginxConfig:
        return parse_config(file)

    def load_nginx_config(self, config: str) -> RootNginxConfig:
        # Load config in a temporary file
        with NamedTemporaryFile() as f:
            f.write(config.encode())
            f.flush()
            return parse_config(f.name)
