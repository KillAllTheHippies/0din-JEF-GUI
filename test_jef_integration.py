#!/usr/bin/env python3
"""
Test script to verify JEF integration works correctly.
Run this script to test the integration before starting the Flask app.
"""

import sys
import os
from pathlib import Path

def test_jef_integration():
    """Test JEF integration components"""
    print("=== JEF Integration Test ===\n")
    
    # Test 1: Check JEF path
    JEF_PATH = Path("K:/0din/0din-JEF")
    if JEF_PATH.exists():
        print(f"✓ JEF path found: {JEF_PATH}")
    else:
        print(f"✗ JEF path not found: {JEF_PATH}")
        print("  Please ensure JEF is installed at the correct location.")
        return False
    
    # Test 2: Check JEF imports
    sys.path.insert(0, str(JEF_PATH))
    try:
        from jef import tiananmen, nerve_agent, meth, harry_potter, copyrights
        print("✓ JEF modules imported successfully")
    except ImportError as e:
        print(f"✗ JEF import failed: {e}")
        print("  Please ensure JEF dependencies are installed.")
        return False
    
    # Test 3: Test basic functionality
    test_text = "This is a sample text for testing JEF analysis capabilities."
    
    try:
        # Test each analysis type
        tests = [
            ("Tiananmen", lambda: tiananmen.score(test_text)),
            ("Nerve Agent", lambda: nerve_agent.score(test_text)),
            ("Methamphetamine", lambda: meth.score(test_text)),
            ("Copyright", lambda: copyrights.score(test_text, "reference text"))
        ]
        
        for test_name, test_func in tests:
            try:
                result = test_func()
                print(f"✓ {test_name} analysis: {result}")
            except Exception as e:
                print(f"✗ {test_name} analysis failed: {e}")
                return False
                
    except Exception as e:
        print(f"✗ JEF functionality test failed: {e}")
        return False
    
    print("\n✓ All JEF integration tests passed!")
    print("The Flask app should now work with JEF integration.")
    return True

if __name__ == "__main__":
    success = test_jef_integration()
    sys.exit(0 if success else 1)