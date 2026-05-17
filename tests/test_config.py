import tempfile
import unittest
from pathlib import Path

from dwsearch.config import load_runtime_config, resolve_config_path


class ConfigTests(unittest.TestCase):
    def test_resolve_config_path_explicit(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            config_path = Path(tmp_dir) / "x.toml"
            config_path.write_text("[defaults]\ndefault_amount=7\n", encoding="utf-8")
            resolved = resolve_config_path(str(config_path))
            self.assertEqual(resolved, config_path)

    def test_load_runtime_config_profile_override(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            config_path = Path(tmp_dir) / "dwsearch.toml"
            config_path.write_text(
                "[defaults]\n"
                "default_engine='ahmia'\n"
                "default_amount=11\n"
                "timeout_s=20.0\n"
                "retries=2\n"
                "backoff_s=0.6\n"
                "headers_preset='random'\n"
                "concurrency=6\n"
                "\n"
                "[profiles.fast]\n"
                "default_amount=5\n"
                "timeout_s=10.0\n",
                encoding="utf-8",
            )
            cfg = load_runtime_config(str(config_path), "fast")
            self.assertEqual(cfg.profile, "fast")
            self.assertEqual(cfg.default_engine, "ahmia")
            self.assertEqual(cfg.default_amount, 5)
            self.assertEqual(cfg.timeout_s, 10.0)
            self.assertEqual(cfg.retries, 2)


if __name__ == "__main__":
    unittest.main()
