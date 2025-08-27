#!/usr/bin/env python3
"""
Targeted test to reproduce the exact NameError in validation_helper.py
"""

import sys
import traceback
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_validation_helper_specific_error():
    """Test the specific line that causes NameError in validation_helper.py."""
    print("Testing validation_helper.py specific error reproduction")
    print("=" * 60)
    
    try:
        # Import what we need
        from liteagent.tool_calling_types import ToolCallingType, get_tool_calling_type
        from tests.utils.validation_helper import ValidationTestHelper
        
        print("✓ Successfully imported ToolCallingType and ValidationTestHelper")
        
        # Create a mock validation observer (we don't need a real one for this test)
        class MockValidationObserver:
            def register_response_parser(self, pattern, parser):
                print(f"  Would register parser: {pattern}")
        
        mock_observer = MockValidationObserver()
        
        # Try to call the method that has the error
        print("\nTrying to call register_parsers_for_type with BASIC type...")
        
        # This should trigger the error because it tries to compare with ToolCallingType.OPENAI
        from liteagent.capabilities import get_model_capabilities
        capabilities = get_model_capabilities("openai/gpt-4o-mini")
        
        print(f"Got capabilities: {capabilities}")
        print(f"Calling register_parsers_for_type...")
        
        # This line should cause the NameError
        ValidationTestHelper.register_parsers_for_type(
            mock_observer, 
            capabilities,  # This is ModelCapabilities, not ToolCallingType
            ["get_weather"]
        )
        
        print("✓ No error occurred - this is unexpected!")
        
    except NameError as e:
        print(f"✗ NameError caught: {e}")
        print("This is the error we're looking for!")
        traceback.print_exc()
        
        # Let's examine the validation_helper source to see the exact issue
        print("\nLet's check what's wrong in the source...")
        import inspect
        source = inspect.getsource(ValidationTestHelper.register_parsers_for_type)
        print("Source code of register_parsers_for_type:")
        print("-" * 40)
        print(source)
        
    except Exception as e:
        print(f"✗ Other error: {e}")
        traceback.print_exc()

def test_exact_line_issue():
    """Test the exact line that references undefined variables."""
    print("\n" + "=" * 60)
    print("Testing the exact line with the undefined reference")
    print("=" * 60)
    
    try:
        # Let's try to access ToolCallingType.OPENAI directly
        from liteagent.tool_calling_types import ToolCallingType
        
        print("Available ToolCallingType values:")
        for item in ToolCallingType:
            print(f"  - {item.name}: {item.value}")
        
        print("\nTrying to access ToolCallingType.OPENAI...")
        try:
            openai_type = ToolCallingType.OPENAI
            print(f"✓ ToolCallingType.OPENAI = {openai_type}")
        except AttributeError as e:
            print(f"✗ AttributeError: {e}")
            print("This is why the comparison fails!")
        
        print("\nTrying to access ToolCallingType.ANTHROPIC...")
        try:
            anthropic_type = ToolCallingType.ANTHROPIC
            print(f"✓ ToolCallingType.ANTHROPIC = {anthropic_type}")
        except AttributeError as e:
            print(f"✗ AttributeError: {e}")
            print("This is why the comparison fails!")
            
    except Exception as e:
        print(f"✗ Error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_validation_helper_specific_error()
    test_exact_line_issue()