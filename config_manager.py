"""
Configuration Manager for ChatGPT Archive Search Tool

Handles loading, saving, and managing application settings with
support for user preferences, theme customization, and runtime configuration.
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

class ConfigManager:
    """
    Centralized configuration management for the application.
    
    Handles user settings, application preferences, and runtime configuration
    with automatic persistence and validation.
    """
    
    def __init__(self, config_file: str = "app_settings.json"):
        """
        Initialize the configuration manager.
        
        Args:
            config_file: Path to the configuration file
        """
        self.config_file = Path(config_file)
        self.settings = self._load_default_settings()
        self.load_settings()
    
    def _load_default_settings(self) -> Dict[str, Any]:
        """
        Load default application settings.
        
        Returns:
            Dictionary containing default configuration values
        """
        return {
            # Archive settings
            "archive_path": "ChatGPT chats/ChatGPT chats",
            
            # Theme settings
            "theme_mode": "auto",  # auto, light, dark
            "accent_color": "blue",
            "custom_primary_color": "#0d6efd",
            
            # Search preferences
            "default_search_mode": "ALL",
            "max_results": 100,
            "default_case_sensitive": False,
            "enable_live_search": False,
            
            # File explorer settings
            "max_tree_depth": 3,
            "sidebar_width": 300,
            "show_hidden_files": False,
            "expand_tree_on_load": True,
            
            # JEF integration
            "jef_path": "K:/0din/0din-JEF",
            "enable_jef_integration": False,
            
            # Export settings
            "default_export_format": "csv",
            "default_path_type": "relative",
            
            # Performance settings
            "search_timeout": 30,
            "cache_size": 100,
            
            # Server settings
            "host": "0.0.0.0",
            "port": 5000,
            "debug": True,
            
            # Metadata
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "last_saved": None
        }
    
    def load_settings(self) -> bool:
        """
        Load settings from the configuration file.
        
        Returns:
            True if settings were loaded successfully, False otherwise
        """
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    saved_settings = json.load(f)
                
                # Merge with defaults to ensure all keys exist
                self.settings.update(saved_settings)
                print(f"Settings loaded from {self.config_file}")
                return True
            else:
                print(f"No configuration file found at {self.config_file}, using defaults")
                return False
        except Exception as e:
            print(f"Error loading settings: {e}")
            return False
    
    def save_settings(self) -> bool:
        """
        Save current settings to the configuration file.
        
        Returns:
            True if settings were saved successfully, False otherwise
        """
        try:
            # Update last saved timestamp
            self.settings["last_saved"] = datetime.now().isoformat()
            
            # Create backup of existing config
            if self.config_file.exists():
                backup_file = self.config_file.with_suffix('.json.backup')
                self.config_file.replace(backup_file)
            
            # Save new settings
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            
            print(f"Settings saved to {self.config_file}")
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key doesn't exist
            
        Returns:
            Configuration value or default
        """
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.
        
        Args:
            key: Configuration key
            value: Value to set
        """
        self.settings[key] = value
    
    def update(self, new_settings: Dict[str, Any]) -> None:
        """
        Update multiple configuration values.
        
        Args:
            new_settings: Dictionary of settings to update
        """
        self.settings.update(new_settings)
    
    def get_all(self) -> Dict[str, Any]:
        """
        Get all configuration settings.
        
        Returns:
            Complete settings dictionary
        """
        return self.settings.copy()
    
    def reset_to_defaults(self) -> None:
        """Reset all settings to default values."""
        self.settings = self._load_default_settings()
    
    def validate_settings(self) -> Dict[str, str]:
        """
        Validate current settings and return any errors.
        
        Returns:
            Dictionary of validation errors (empty if all valid)
        """
        errors = {}
        
        # Validate archive path
        archive_path = self.get("archive_path")
        if archive_path and not Path(archive_path).exists():
            errors["archive_path"] = "Archive path does not exist"
        
        # Validate JEF path
        jef_path = self.get("jef_path")
        if jef_path and self.get("enable_jef_integration") and not Path(jef_path).exists():
            errors["jef_path"] = "JEF path does not exist"
        
        # Validate numeric values
        numeric_settings = {
            "max_results": (1, 10000),
            "max_tree_depth": (1, 10),
            "sidebar_width": (200, 800),
            "search_timeout": (5, 300),
            "cache_size": (10, 1000),
            "port": (1, 65535)
        }
        
        for setting, (min_val, max_val) in numeric_settings.items():
            value = self.get(setting)
            if not isinstance(value, (int, float)) or not (min_val <= value <= max_val):
                errors[setting] = f"Must be a number between {min_val} and {max_val}"
        
        # Validate color format
        custom_color = self.get("custom_primary_color")
        if custom_color and not custom_color.startswith("#") or len(custom_color) != 7:
            errors["custom_primary_color"] = "Must be a valid hex color (e.g., #0d6efd)"
        
        return errors
    
    def export_settings(self, file_path: str) -> bool:
        """
        Export settings to a file.
        
        Args:
            file_path: Path to export file
            
        Returns:
            True if export was successful, False otherwise
        """
        try:
            export_data = {
                **self.settings,
                "exported_at": datetime.now().isoformat(),
                "export_version": "1.0"
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error exporting settings: {e}")
            return False
    
    def import_settings(self, file_path: str) -> bool:
        """
        Import settings from a file.
        
        Args:
            file_path: Path to import file
            
        Returns:
            True if import was successful, False otherwise
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                imported_settings = json.load(f)
            
            # Remove export metadata
            imported_settings.pop("exported_at", None)
            imported_settings.pop("export_version", None)
            
            # Validate imported settings
            temp_settings = self.settings.copy()
            self.settings.update(imported_settings)
            errors = self.validate_settings()
            
            if errors:
                # Restore original settings if validation fails
                self.settings = temp_settings
                print(f"Import failed due to validation errors: {errors}")
                return False
            
            return True
        except Exception as e:
            print(f"Error importing settings: {e}")
            return False
    
    def get_theme_css_variables(self) -> Dict[str, str]:
        """
        Get CSS variables for theme customization.
        
        Returns:
            Dictionary of CSS variable names and values
        """
        custom_color = self.get("custom_primary_color", "#0d6efd")
        accent_color = self.get("accent_color", "blue")
        
        # Color palette based on accent color
        color_palettes = {
            "blue": {"primary": "#0d6efd", "secondary": "#6610f2"},
            "purple": {"primary": "#6f42c1", "secondary": "#6610f2"},
            "green": {"primary": "#198754", "secondary": "#20c997"},
            "orange": {"primary": "#fd7e14", "secondary": "#f0ad4e"},
            "red": {"primary": "#dc3545", "secondary": "#e83e8c"},
            "teal": {"primary": "#20c997", "secondary": "#17a2b8"}
        }
        
        palette = color_palettes.get(accent_color, color_palettes["blue"])
        
        return {
            "--accent-primary": custom_color if accent_color == "custom" else palette["primary"],
            "--accent-secondary": palette["secondary"],
            "--sidebar-width": f"{self.get('sidebar_width', 300)}px"
        }

# Global configuration instance
config = ConfigManager()