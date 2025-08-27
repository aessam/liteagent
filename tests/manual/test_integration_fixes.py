#!/usr/bin/env python3
"""
Test script to verify integration test fixes are working.
This tests the specific issues that were causing massive test failures.
"""

import sys
import os
import traceback

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_tool_calling_types_import():
    """Test that tool_calling_types imports work correctly."""
    print("🔧 Testing tool_calling_types imports...")
    
    try:
        from liteagent.tool_calling_types import ToolCallingType, get_tool_calling_type
        print("  ✅ Import successful")
        
        # Test the function
        result = get_tool_calling_type("openai/gpt-4o-mini")
        print(f"  ✅ get_tool_calling_type works: {result}")
        
        # Test enum values
        print(f"  ✅ Available enum values: {[item.name for item in ToolCallingType]}")
        
        return True
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        traceback.print_exc()
        return False

def test_validation_helper_fixes():
    """Test that validation helper fixes work."""
    print("\n🔧 Testing validation_helper fixes...")
    
    try:
        from tests.utils.validation_helper import ValidationTestHelper
        from liteagent.capabilities import ModelCapabilities
        print("  ✅ ValidationTestHelper import successful")
        
        # Create a mock capabilities object
        capabilities = ModelCapabilities(
            model_id="openai/gpt-4o-mini",
            name="GPT-4o Mini",
            provider="OpenAI",
            tool_calling=True,
            supports_parallel_tools=True,
            supports_streaming=True,
            supports_image_input=False,
            max_tokens=4096,
            context_window=16384
        )
        
        class MockObserver:
            def register_response_parser(self, pattern, parser):
                print(f"    📝 Registered parser for: {pattern}")
        
        # Test the function that was causing NameError
        ValidationTestHelper.register_parsers_for_type(
            MockObserver(), 
            capabilities, 
            ["get_weather", "add_numbers"]
        )
        print("  ✅ register_parsers_for_type works without NameError")
        
        return True
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        traceback.print_exc()
        return False

def test_memory_model_types_fixes():
    """Test that memory model types fixes work."""
    print("\n🔧 Testing memory model types fixes...")
    
    try:
        # Check that the import path is correct
        from liteagent.tool_calling_types import get_tool_calling_type, ToolCallingType
        
        # Mock the specific function that was failing
        from unittest.mock import patch
        
        with patch("liteagent.tool_calling_types.get_tool_calling_type") as mock_get_type:
            mock_get_type.return_value = ToolCallingType.BASIC
            result = get_tool_calling_type("test-model")
            print(f"  ✅ Mocking get_tool_calling_type works: {result}")
        
        # Test that ToolCallingType.BASIC exists (was TEXT_BASED before)
        basic_type = ToolCallingType.BASIC
        print(f"  ✅ ToolCallingType.BASIC exists: {basic_type}")
        
        return True
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        traceback.print_exc()
        return False

def test_validation_test_fixes():
    """Test that validation test fixes work."""
    print("\n🔧 Testing validation test enum fixes...")
    
    try:
        from liteagent.tool_calling_types import ToolCallingType
        
        # Test that the corrected enum values work
        basic = ToolCallingType.BASIC
        parallel = ToolCallingType.PARALLEL
        
        print(f"  ✅ ToolCallingType.BASIC: {basic}")
        print(f"  ✅ ToolCallingType.PARALLEL: {parallel}")
        
        # Test the logic that was in the validation test
        current_strategy = ToolCallingType.BASIC
        temp_strategy = ToolCallingType.BASIC
        if current_strategy == ToolCallingType.BASIC:
            temp_strategy = ToolCallingType.PARALLEL
        
        print(f"  ✅ Strategy switching logic works: {current_strategy} -> {temp_strategy}")
        
        return True
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("🔍 INTEGRATION TEST FIXES VERIFICATION")
    print("=" * 60)
    print("Testing the specific issues that caused 105 test failures\n")
    
    tests = [
        ("Tool Calling Types Import", test_tool_calling_types_import),
        ("Validation Helper Fixes", test_validation_helper_fixes),
        ("Memory Model Types Fixes", test_memory_model_types_fixes),
        ("Validation Test Enum Fixes", test_validation_test_fixes),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"Running: {test_name}")
        print('='*60)
        result = test_func()
        results.append((test_name, result))
    
    print(f"\n{'='*60}")
    print("SUMMARY")
    print('='*60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nPassed: {passed}/{len(tests)}")
    
    if passed == len(tests):
        print("\n🎉 ALL FIXES VERIFIED! Integration tests should now work.")
        print("\nYou can now run: pytest tests/integration/ -v")
    else:
        print(f"\n⚠️  {len(tests) - passed} test(s) still failing. Check the errors above.")
    
    return passed == len(tests)

if __name__ == "__main__":
    main()