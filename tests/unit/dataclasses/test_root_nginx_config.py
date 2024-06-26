from tests.testcase import TestCase


class TestRootNginxConfig(TestCase):
    def test_root_config_contains_all_included_files(self):
        root_config = self.get_example_root_conf()
        self.assertListEqual(
            [c.file for c in root_config.config],
            [
                root_config.root_dir / "nginx.conf",
                root_config.root_dir / "servers/example.com.conf",
                root_config.root_dir / "servers/testalex.hypernode.io.conf",
                root_config.root_dir / "servers/verylargefile.conf",
                root_config.root_dir / "servers/include/nested.conf",
                root_config.root_dir / "relative_include/relative_include.conf",
                root_config.root_dir / "relative_include/relative_nested_include.conf",
            ],
        )
