import json
import os
from pathlib import Path
import tempfile

from config_manager import ConfigManager


def test_load_default_settings():
    cfg = ConfigManager(config_file="nonexistent.json")
    defaults = cfg._load_default_settings()
    assert "archive_path" in defaults
    assert defaults["theme_mode"] == "auto"


def test_save_and_load_settings(tmp_path):
    cfg_file = tmp_path / "settings.json"
    cfg = ConfigManager(config_file=str(cfg_file))
    cfg.set("archive_path", str(tmp_path))
    assert cfg.save_settings()

    new_cfg = ConfigManager(config_file=str(cfg_file))
    assert new_cfg.get("archive_path") == str(tmp_path)


def test_validation_errors(tmp_path):
    cfg = ConfigManager(config_file=str(tmp_path / "settings.json"))
    cfg.set("archive_path", str(tmp_path / "doesnotexist"))
    errors = cfg.validate_settings()
    assert "archive_path" in errors
