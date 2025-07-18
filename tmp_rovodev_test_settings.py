#!/usr/bin/env python3
"""
Test script for the options dashboard functionality.
"""

import requests
import json
import time
from pathlib import Path

def test_settings_dashboard():
    """Test the settings dashboard functionality."""
    base_url = "http://localhost:5000"
    
    print("Testing ChatGPT Archive Search Settings Dashboard")
    print("=" * 50)
    
    # Test 1: Check if settings page loads
    print("1. Testing settings page accessibility...")
    try:
        response = requests.get(f"{base_url}/settings")
        if response.status_code == 200:
            print("   ✓ Settings page loads successfully")
        else:
            print(f"   ✗ Settings page failed to load (status: {response.status_code})")
            return False
    except requests.exceptions.ConnectionError:
        print("   ✗ Cannot connect to server. Make sure the app is running on localhost:5000")
        return False
    
    # Test 2: Get current settings
    print("2. Testing settings API...")
    try:
        response = requests.get(f"{base_url}/api/settings")
        if response.status_code == 200:
            settings = response.json()
            print("   ✓ Settings API working")
            print(f"   Current archive path: {settings.get('archive_path', 'Not set')}")
            print(f"   Current theme: {settings.get('theme_mode', 'auto')}")
        else:
            print(f"   ✗ Settings API failed (status: {response.status_code})")
            return False
    except Exception as e:
        print(f"   ✗ Settings API error: {e}")
        return False
    
    # Test 3: Update settings
    print("3. Testing settings update...")
    test_settings = {
        "theme_mode": "dark",
        "accent_color": "purple",
        "max_results": 50,
        "default_case_sensitive": True
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/settings",
            json=test_settings,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            print("   ✓ Settings update successful")
        else:
            result = response.json()
            print(f"   ✗ Settings update failed: {result.get('error', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"   ✗ Settings update error: {e}")
        return False
    
    # Test 4: Validate settings
    print("4. Testing settings validation...")
    invalid_settings = {
        "max_results": -1,  # Invalid value
        "custom_primary_color": "invalid_color"  # Invalid color
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/settings/validate",
            json=invalid_settings,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            result = response.json()
            if not result.get('valid', True):
                print("   ✓ Settings validation working (correctly rejected invalid settings)")
            else:
                print("   ✗ Settings validation failed (accepted invalid settings)")
                return False
        else:
            print(f"   ✗ Settings validation API failed (status: {response.status_code})")
            return False
    except Exception as e:
        print(f"   ✗ Settings validation error: {e}")
        return False
    
    # Test 5: Check JEF status
    print("5. Testing JEF integration status...")
    try:
        response = requests.get(f"{base_url}/api/jef-status")
        if response.status_code == 200:
            jef_status = response.json()
            print(f"   JEF Available: {jef_status.get('available', False)}")
            if jef_status.get('path'):
                print(f"   JEF Path: {jef_status.get('path')}")
            print("   ✓ JEF status API working")
        else:
            print(f"   ✗ JEF status API failed (status: {response.status_code})")
            return False
    except Exception as e:
        print(f"   ✗ JEF status error: {e}")
        return False
    
    # Test 6: Export settings
    print("6. Testing settings export...")
    try:
        response = requests.get(f"{base_url}/api/settings/export")
        if response.status_code == 200:
            print("   ✓ Settings export working")
            # Check if it's a valid JSON file
            try:
                exported_data = json.loads(response.text)
                if 'exported_at' in exported_data:
                    print("   ✓ Export contains expected metadata")
                else:
                    print("   ⚠ Export missing metadata")
            except json.JSONDecodeError:
                print("   ✗ Export is not valid JSON")
                return False
        else:
            print(f"   ✗ Settings export failed (status: {response.status_code})")
            return False
    except Exception as e:
        print(f"   ✗ Settings export error: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("✓ All settings dashboard tests passed!")
    print("\nYou can now:")
    print("1. Visit http://localhost:5000/settings to configure the app")
    print("2. Change the archive root folder")
    print("3. Customize colors and themes")
    print("4. Adjust search preferences")
    print("5. Configure JEF integration")
    print("6. Export/import settings")
    
    return True

def test_configuration_file():
    """Test if configuration file is created and readable."""
    print("\nTesting configuration file...")
    config_file = Path("app_settings.json")
    
    if config_file.exists():
        print("   ✓ Configuration file exists")
        try:
            with open(config_file, 'r') as f:
                config_data = json.load(f)
            print("   ✓ Configuration file is valid JSON")
            print(f"   Settings count: {len(config_data)} items")
            return True
        except Exception as e:
            print(f"   ✗ Configuration file error: {e}")
            return False
    else:
        print("   ⚠ Configuration file not found (will be created on first save)")
        return True

if __name__ == "__main__":
    print("ChatGPT Archive Search - Settings Dashboard Test")
    print("Make sure the application is running before running this test.")
    print("Start the app with: python app.py")
    print()
    
    input("Press Enter when the app is running...")
    
    success = test_settings_dashboard()
    test_configuration_file()
    
    if success:
        print("\n🎉 Settings dashboard is working correctly!")
    else:
        print("\n❌ Some tests failed. Check the output above for details.")