from tests.testcase import TestCase


class TestRootNginxConfig(TestCase):
    def test_root_config_contains_all_included_files(self):
        root_config = self.get_example_root_conf()
        self.assertEqual(
            [c.file for c in root_config.config],
            [
                root_config.root_dir / "nginx.conf",
                root_config.root_dir / "servers/example.com.conf",
                root_config.root_dir / "servers/testalex.hypernode.io.conf",
            ],
        )
