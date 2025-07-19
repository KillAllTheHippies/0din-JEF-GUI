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


def test_export_import_settings(tmp_path):
    cfg_file = tmp_path / "settings.json"
    cfg = ConfigManager(config_file=str(cfg_file))
    cfg.set("archive_path", str(tmp_path))
    cfg.save_settings()

    export_file = tmp_path / "export.json"
    assert cfg.export_settings(str(export_file))
    assert export_file.exists()

    with open(export_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert "exported_at" in data

    cfg.set("archive_path", "changed")
    assert cfg.import_settings(str(export_file))
    assert cfg.get("archive_path") == str(tmp_path)


def test_get_theme_css_variables_custom():
    cfg = ConfigManager(config_file="none.json")
    cfg.set("theme", "custom")
    cfg.set("custom_primary_color", "#ff0000")
    vars = cfg.get_theme_css_variables()
    assert vars["--accent-primary"] == "#ff0000"
    assert "--sidebar-width" in vars
