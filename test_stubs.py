#!/usr/bin/env python3
"""
Test script to verify that the fake-ubuntu-advantage-tools Python stubs work correctly.

This script tests that:
1. The uaclient module can be imported
2. The updates() function returns the expected structure
3. The returned object has the correct attributes
4. No exceptions are raised during normal usage

Run this after installing fake-ubuntu-advantage-tools to verify it works.
"""

import sys


def test_import():
    """Test that the uaclient module can be imported."""
    print("Testing import of uaclient.api.u.pro.packages.updates.v1...")
    try:
        import uaclient.api.u.pro.packages.updates.v1
        print("✓ Import successful")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


def test_updates_function():
    """Test that the updates() function works correctly."""
    print("\nTesting updates() function...")
    try:
        from uaclient.api.u.pro.packages.updates.v1 import updates
        result = updates()
        print("✓ updates() function callable")
        return result
    except Exception as e:
        print(f"✗ updates() failed: {e}")
        return None


def test_result_structure(result):
    """Test that the result has the expected structure."""
    print("\nTesting result structure...")
    
    if result is None:
        print("✗ Result is None")
        return False
    
    # Check for updates attribute
    if not hasattr(result, 'updates'):
        print("✗ Result missing 'updates' attribute")
        return False
    print("✓ Result has 'updates' attribute")
    
    # Check that updates is a list
    if not isinstance(result.updates, list):
        print("✗ 'updates' is not a list")
        return False
    print("✓ 'updates' is a list")
    
    # Check that list is empty (no UA updates available)
    if len(result.updates) != 0:
        print(f"⚠ 'updates' list not empty (contains {len(result.updates)} items)")
    else:
        print("✓ 'updates' list is empty (no UA packages)")
    
    return True


def test_alternative_import():
    """Test alternative import style used in some Ubuntu tools."""
    print("\nTesting alternative import style...")
    try:
        import uaclient.api.u.pro.packages.updates.v1 as ua
        result = ua.updates()
        if hasattr(result, 'updates'):
            print("✓ Alternative import style works")
            return True
        else:
            print("✗ Alternative import returned unexpected result")
            return False
    except Exception as e:
        print(f"✗ Alternative import failed: {e}")
        return False


def test_update_info_class():
    """Test that UpdateInfo class exists and can be instantiated."""
    print("\nTesting UpdateInfo class...")
    try:
        from uaclient.api.u.pro.packages.updates.v1 import UpdateInfo
        info = UpdateInfo(
            package="test-package",
            version="1.0",
            download_size=1024,
            status="pending_attach"
        )
        
        # Verify attributes
        if info.package != "test-package":
            print("✗ UpdateInfo.package incorrect")
            return False
        if info.version != "1.0":
            print("✗ UpdateInfo.version incorrect")
            return False
        if info.download_size != 1024:
            print("✗ UpdateInfo.download_size incorrect")
            return False
        if info.status != "pending_attach":
            print("✗ UpdateInfo.status incorrect")
            return False
        
        print("✓ UpdateInfo class works correctly")
        return True
    except Exception as e:
        print(f"✗ UpdateInfo test failed: {e}")
        return False




def test_status_module():
    """Test that the status module works correctly."""
    print("\nTesting status module...")
    try:
        from uaclient.api.u.pro.status import status, StatusResult
        result = status()
        
        if not hasattr(result, 'attached'):
            print("✗ StatusResult missing 'attached' attribute")
            return False
        if not hasattr(result, 'enabled_services'):
            print("✗ StatusResult missing 'enabled_services' attribute")
            return False
        
        print("✓ status module works correctly")
        return True
    except Exception as e:
        print(f"✗ status module test failed: {e}")
        return False


def test_magic_attach_initiate():
    """Test that the magic attach initiate module works correctly."""
    print("\nTesting magic attach initiate module...")
    try:
        from uaclient.api.u.pro.attach.magic.initiate.v1 import initiate, InitiateResult
        result = initiate()
        
        if not hasattr(result, 'success'):
            print("✗ InitiateResult missing 'success' attribute")
            return False
        if not hasattr(result, 'error'):
            print("✗ InitiateResult missing 'error' attribute")
            return False
        
        print("✓ magic attach initiate module works correctly")
        return True
    except Exception as e:
        print(f"✗ magic attach initiate test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Testing fake-ubuntu-advantage-tools Python stubs")
    print("=" * 60)
    
    all_passed = True
    
    # Test 1: Import
    if not test_import():
        all_passed = False
        print("\n⚠ Skipping remaining tests due to import failure")
        sys.exit(1)
    
    # Test 2: updates() function
    result = test_updates_function()
    if result is None:
        all_passed = False
    
    # Test 3: Result structure
    if result is not None:
        if not test_result_structure(result):
            all_passed = False
    
    # Test 4: Alternative import
    if not test_alternative_import():
        all_passed = False
    
    # Test 5: UpdateInfo class
    if not test_update_info_class():
        all_passed = False
    
    # Test 6: status module
    if not test_status_module():
        all_passed = False
    
    # Test 7: magic attach initiate module
    if not test_magic_attach_initiate():
        all_passed = False
    
    # Summary
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All tests passed!")
        print("\nThe fake-ubuntu-advantage-tools stubs are working correctly.")
        print("Ubuntu system tools should work without crashes or patches.")
    else:
        print("✗ Some tests failed!")
        print("\nThere may be issues with the stub implementation.")
        sys.exit(1)
    print("=" * 60)


if __name__ == "__main__":
    main()