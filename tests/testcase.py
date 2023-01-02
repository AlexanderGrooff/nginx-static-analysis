import os
from glob import glob
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory
from unittest import TestCase as BaseTestCase
from unittest.mock import Mock, mock_open, patch

from nginx_analysis.analysis import parse_config
from nginx_analysis.dataclasses import RootNginxConfig

PROJECT_DIR = Path(__file__).parent.parent


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
        # Copy the example config to a temporary directory so
        # that we can rename /etc/nginx to the temporary directory
        # in the Nginx config files
        with TemporaryDirectory() as tmpdir:
            # Copy all files in the example config to the temporary directory
            for path in glob(f"{PROJECT_DIR}/example_nginx/**", recursive=True):
                rel_path = path.split(f"{PROJECT_DIR}/example_nginx/")[1]
                tempfile_path = f"{tmpdir}/{rel_path}"
                if os.path.isdir(path):
                    # Create the child tempdir
                    os.makedirs(tempfile_path, exist_ok=True)
                    continue

                with open(path) as f:
                    with open(tempfile_path, "w") as g:
                        print(f"Copy {path} to {tempfile_path} from relpath {rel_path}")
                        contents = f.read()
                        contents = contents.replace("/etc/nginx", tmpdir)
                        g.write(contents)

            # Load the config from the tmpdir
            return parse_config(f"{tmpdir}/nginx.conf")

    def load_nginx_config(self, config: str) -> RootNginxConfig:
        # Load config in a temporary file
        with NamedTemporaryFile() as f:
            f.write(config.encode())
            f.flush()
            return parse_config(f.name)
