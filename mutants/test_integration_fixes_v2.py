#!/usr/bin/env python3
"""
Test script to verify integration test fixes v2 are working.
This tests the specific ToolCallingType object attribute issues.
"""

import sys
import os
import traceback

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_register_parsers_for_type_with_correct_signature():
    """Test that register_parsers_for_type works with ToolCallingType."""
    print("🔧 Testing register_parsers_for_type with correct signature...")
    
    try:
        from tests.utils.validation_helper import ValidationTestHelper
        from liteagent.tool_calling_types import ToolCallingType
        print("  ✅ Imports successful")
        
        class MockObserver:
            def register_response_parser(self, pattern, parser):
                print(f"    📝 Registered parser for: {pattern}")
        
        # Test the function with ToolCallingType (what the tests actually pass)
        ValidationTestHelper.register_parsers_for_type(
            MockObserver(), 
            ToolCallingType.BASIC,  # This is what tests pass, not ModelCapabilities
            ["get_weather", "add_numbers"]
        )
        print("  ✅ register_parsers_for_type works with ToolCallingType.BASIC")
        
        # Test with different enum values
        ValidationTestHelper.register_parsers_for_type(
            MockObserver(), 
            ToolCallingType.PARALLEL,
            ["calculate_area"]
        )
        print("  ✅ register_parsers_for_type works with ToolCallingType.PARALLEL")
        
        return True
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        traceback.print_exc()
        return False

def test_memory_model_types_model_name():
    """Test that the memory test model name is now correct."""
    print("\n🔧 Testing memory model types model name fix...")
    
    try:
        # Test that the model name format is recognized
        from liteagent.providers.factory import ProviderFactory
        
        # This should work now
        provider_name = ProviderFactory.get_provider_name("mistral/open-mistral")
        print(f"  ✅ Provider for 'mistral/open-mistral': {provider_name}")
        
        # Test that the old format fails (confirming our fix was needed)
        try:
            provider_name_old = ProviderFactory.get_provider_name("open-mistral")
            print(f"  ⚠️  Old format 'open-mistral' unexpectedly works: {provider_name_old}")
        except Exception as e:
            print(f"  ✅ Old format 'open-mistral' correctly fails: {type(e).__name__}")
        
        return True
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        traceback.print_exc()
        return False

def test_integration_test_imports():
    """Test that the integration test imports work."""
    print("\n🔧 Testing integration test imports...")
    
    try:
        # Test imports that were failing
        from liteagent.tool_calling_types import ToolCallingType, get_tool_calling_type
        from tests.utils.validation_helper import ValidationTestHelper
        print("  ✅ All imports successful")
        
        # Test that the enum values we're using exist
        basic = ToolCallingType.BASIC
        parallel = ToolCallingType.PARALLEL
        none = ToolCallingType.NONE
        advanced = ToolCallingType.ADVANCED
        
        print(f"  ✅ Available enum values work: {[basic.name, parallel.name, none.name, advanced.name]}")
        
        # Test that the function works
        result = get_tool_calling_type("openai/gpt-4o-mini")
        print(f"  ✅ get_tool_calling_type works: {result}")
        
        return True
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        traceback.print_exc()
        return False

def test_mock_validation_observer_scenario():
    """Test a typical integration test scenario."""
    print("\n🔧 Testing typical integration test scenario...")
    
    try:
        from liteagent.tool_calling_types import ToolCallingType, get_tool_calling_type
        from tests.utils.validation_helper import ValidationTestHelper
        
        # Mock the validation observer as the real tests do
        class MockValidationObserver:
            def __init__(self):
                self.validation_strategy = None
                self.parsers = []
                
            def set_validation_strategy(self, strategy):
                self.validation_strategy = strategy
                print(f"    📋 Set validation strategy: {strategy}")
                
            def register_response_parser(self, pattern, parser):
                self.parsers.append((pattern, parser))
                print(f"    📝 Registered parser: {pattern}")
        
        # Simulate what the integration tests do
        model = "openai/gpt-4o-mini"
        tool_names = ["get_weather", "add_numbers"]
        
        validation_observer = MockValidationObserver()
        
        # Step 1: Get tool calling type (what tests do)
        tool_calling_type = get_tool_calling_type(model)
        print(f"  📊 Tool calling type for {model}: {tool_calling_type}")
        
        # Step 2: Set validation strategy 
        validation_observer.set_validation_strategy(tool_calling_type)
        
        # Step 3: Register parsers (this was failing before)
        ValidationTestHelper.register_parsers_for_type(
            validation_observer, 
            tool_calling_type,  # This is the correct type now
            tool_names
        )
        
        print(f"  ✅ Full integration test scenario works! Registered {len(validation_observer.parsers)} parsers")
        return True
        
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("🔍 INTEGRATION TEST FIXES V2 VERIFICATION")
    print("=" * 60)
    print("Testing fixes for AttributeError: 'ToolCallingType' object has no attribute 'model_id'\n")
    
    tests = [
        ("Register Parsers Function Signature", test_register_parsers_for_type_with_correct_signature),
        ("Memory Model Types Model Name", test_memory_model_types_model_name),
        ("Integration Test Imports", test_integration_test_imports),
        ("Full Integration Test Scenario", test_mock_validation_observer_scenario),
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
        print("\n🎉 ALL V2 FIXES VERIFIED! Integration tests should now work.")
        print("\nThe AttributeError: 'ToolCallingType' object has no attribute 'model_id' should be fixed.")
        print("\nYou can now run: pytest tests/integration/ -v")
    else:
        print(f"\n⚠️  {len(tests) - passed} test(s) still failing. Check the errors above.")
    
    return passed == len(tests)

if __name__ == "__main__":
    main()