#!/usr/bin/env python3
"""
Debug script for tool_calling_types import and usage issues.

This script tests the import and usage of get_tool_calling_type from 
liteagent.tool_calling_types to identify issues with integration tests.
"""

import sys
import traceback
import os

# Add the current directory to Python path to ensure imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_import_tool_calling_types():
    """Test importing the tool_calling_types module and its components."""
    print("=" * 60)
    print("1. Testing import of liteagent.tool_calling_types module")
    print("=" * 60)
    
    try:
        import liteagent.tool_calling_types as tct
        print("✓ Successfully imported liteagent.tool_calling_types")
        
        # Check what's available in the module
        print(f"✓ Available attributes: {dir(tct)}")
        
        # Test importing specific components
        from liteagent.tool_calling_types import ToolCallingType, get_tool_calling_type
        print("✓ Successfully imported ToolCallingType and get_tool_calling_type")
        
        # Check the enum values
        print(f"✓ ToolCallingType enum values: {list(ToolCallingType)}")
        print(f"✓ ToolCallingType enum values by name: {[t.name for t in ToolCallingType]}")
        print(f"✓ ToolCallingType enum values by value: {[t.value for t in ToolCallingType]}")
        
        return True, tct, ToolCallingType, get_tool_calling_type
        
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        traceback.print_exc()
        return False, None, None, None
    except Exception as e:
        print(f"✗ Unexpected error during import: {e}")
        traceback.print_exc()
        return False, None, None, None

def test_get_tool_calling_type_function(get_tool_calling_type, ToolCallingType):
    """Test the get_tool_calling_type function with sample model names."""
    print("\n" + "=" * 60)
    print("2. Testing get_tool_calling_type function")
    print("=" * 60)
    
    test_models = [
        "openai/gpt-4o-mini",
        "gpt-4o-mini", 
        "openai/gpt-4o",
        "gpt-4o",
        "anthropic/claude-3-5-sonnet-20241022",
        "claude-3-5-sonnet-20241022",
        "groq/llama-3.1-70b-versatile",
        "invalid-model-name",
        "nonexistent/model"
    ]
    
    for model in test_models:
        try:
            print(f"\nTesting model: {model}")
            result = get_tool_calling_type(model)
            print(f"  ✓ Result: {result}")
            print(f"  ✓ Result type: {type(result)}")
            print(f"  ✓ Result value: {result.value}")
            print(f"  ✓ Result name: {result.name}")
        except Exception as e:
            print(f"  ✗ Error with {model}: {e}")
            traceback.print_exc()

def test_capabilities_module():
    """Test the underlying capabilities module."""
    print("\n" + "=" * 60)
    print("3. Testing underlying capabilities module")
    print("=" * 60)
    
    try:
        from liteagent.capabilities import get_model_capabilities
        print("✓ Successfully imported get_model_capabilities")
        
        # Test with openai/gpt-4o-mini
        test_model = "openai/gpt-4o-mini"
        print(f"\nTesting capabilities for: {test_model}")
        
        capabilities = get_model_capabilities(test_model)
        print(f"✓ Capabilities result: {capabilities}")
        
        if capabilities:
            print(f"  - Model ID: {capabilities.model_id}")
            print(f"  - Name: {capabilities.name}")
            print(f"  - Provider: {capabilities.provider}")
            print(f"  - Tool calling: {capabilities.tool_calling}")
            print(f"  - Supports parallel tools: {capabilities.supports_parallel_tools}")
            print(f"  - Multimodal: {capabilities.multimodal}")
            print(f"  - Context limit: {capabilities.context_limit}")
        else:
            print("  ✗ No capabilities found for model")
            
    except Exception as e:
        print(f"✗ Error testing capabilities: {e}")
        traceback.print_exc()

def test_validation_helper_issue():
    """Test the specific issue in validation_helper.py."""
    print("\n" + "=" * 60)
    print("4. Testing validation_helper.py issue")
    print("=" * 60)
    
    try:
        from tests.utils.validation_helper import ValidationTestHelper
        print("✓ Successfully imported ValidationTestHelper")
        
        # Try to see what ToolCallingType is being used in validation_helper
        # This should fail because it's not imported
        print("\nTesting what happens when validation_helper tries to use ToolCallingType...")
        
        # This will reveal the exact error
        validation_helper = ValidationTestHelper()
        print("✓ ValidationTestHelper instantiated")
        
    except NameError as e:
        print(f"✗ NameError (expected): {e}")
        print("This confirms the issue - ToolCallingType is not imported in validation_helper.py")
    except Exception as e:
        print(f"✗ Other error: {e}")
        traceback.print_exc()

def main():
    """Main test function."""
    print("Debug Script for tool_calling_types Issues")
    print("This script will help identify why integration tests are failing")
    print("with 'NameError: name 'tool_calling_type' is not defined'")
    
    # Test 1: Import the module
    success, module, ToolCallingType, get_tool_calling_type = test_import_tool_calling_types()
    
    if not success:
        print("\n🚨 Cannot proceed - basic import failed!")
        return
    
    # Test 2: Test the function
    if get_tool_calling_type and ToolCallingType:
        test_get_tool_calling_type_function(get_tool_calling_type, ToolCallingType)
    
    # Test 3: Test capabilities
    test_capabilities_module()
    
    # Test 4: Test validation helper issue
    test_validation_helper_issue()
    
    print("\n" + "=" * 60)
    print("SUMMARY AND DIAGNOSIS")
    print("=" * 60)
    print("\nBased on this analysis, the likely issues are:")
    print("1. validation_helper.py references ToolCallingType.OPENAI and ToolCallingType.ANTHROPIC")
    print("   but these values don't exist in the current enum")
    print("2. validation_helper.py doesn't import ToolCallingType at all")
    print("3. The current ToolCallingType enum has: NONE, BASIC, PARALLEL, ADVANCED")
    print("4. Tests expect: OPENAI, ANTHROPIC, etc.")
    print("\nTo fix:")
    print("- Add missing import in validation_helper.py")
    print("- Update enum values or update code to use correct enum values")
    print("- Ensure consistent usage across all test files")

if __name__ == "__main__":
    main()