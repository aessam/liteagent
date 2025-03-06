"""
Debug script to print API payloads and responses.

This script modifies the LiteLLMInterface to print detailed debug information
about API requests and responses to help diagnose issues with None responses.
"""

import os
import sys
from typing import Dict, Any, List
import json
import time

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Import required modules
from liteagent import LiteAgent
from liteagent.models import ModelInterface, LiteLLMInterface
from liteagent.observer import AgentObserver
from liteagent.tools import get_weather, add_numbers
from liteagent.tool_calling_types import ToolCallingType, get_tool_calling_type
from tests.integration.validation_observer import ValidationObserver
from tests.utils.validation_helper import ValidationTestHelper

# Create a debug proxy for the LiteLLMInterface
class DebugLiteLLMInterface(LiteLLMInterface):
    """Debug wrapper for LiteLLMInterface to print API request and response details."""
    
    def _call_api(self, kwargs: Dict) -> Any:
        """Make the API call using LiteLLM with detailed debug printing."""
        # Print the API request
        request_id = f"req_{time.time()}"
        print(f"\n=== API REQUEST {request_id} ===")
        print(f"Model: {self.model_name}")
        
        # Pretty print messages for readability
        if "messages" in kwargs:
            print("\nMessages:")
            for i, msg in enumerate(kwargs["messages"]):
                role = msg.get("role", "unknown")
                content = msg.get("content", "")
                print(f"[{i}] {role}: {content[:100]}..." if len(content) > 100 else f"[{i}] {role}: {content}")
        
        # Print tools/functions if present
        if "tools" in kwargs:
            print("\nTools:")
            print(json.dumps(kwargs["tools"], indent=2))
        elif "functions" in kwargs:
            print("\nFunctions:")
            print(json.dumps(kwargs["functions"], indent=2))
        
        # Make the actual API call
        try:
            print("\nSending request to API...")
            response = super()._call_api(kwargs)
            
            # Print the response
            print(f"\n=== API RESPONSE {request_id} ===")
            print(f"Response type: {type(response)}")
            
            if response is None:
                print("RESPONSE IS NONE!")
                return None
            
            # Print formatted response for inspection
            try:
                if hasattr(response, 'model_dump_json'):
                    print(json.dumps(json.loads(response.model_dump_json()), indent=2))
                elif hasattr(response, '__dict__'):
                    print(json.dumps(response.__dict__, indent=2, default=str))
                else:
                    print(f"Response: {response}")
            except Exception as e:
                print(f"Error formatting response: {e}")
                print(f"Raw response: {response}")
                
            return response
        except Exception as e:
            print(f"\n=== API ERROR {request_id} ===")
            print(f"Error: {e}")
            raise

# Monkey patch the LiteLLMInterface
def run_test_with_debug():
    """Run a simple test to debug API calls."""
    # Setup the test environment
    model_names = [
        "anthropic/claude-3-5-sonnet-latest",
        "groq/llama-3.1-8b-instant",
        "ollama/llama3.3", 
        "ollama/phi4"
    ]
    
    # Replace normal interface with debug interface
    from liteagent.models import LiteLLMInterface as OriginalLiteLLMInterface
    # Store the original
    original_interface = OriginalLiteLLMInterface
    # Replace with debug version
    import liteagent.models
    liteagent.models.LiteLLMInterface = DebugLiteLLMInterface
    
    for model_name in model_names:
        print(f"\n\n{'=' * 50}")
        print(f"TESTING MODEL: {model_name}")
        print(f"{'=' * 50}\n")
        
        # Set up validation observer
        validation_observer = ValidationObserver()
        tool_calling_type = get_tool_calling_type(model_name)
        validation_observer.set_validation_strategy(tool_calling_type)
        
        # Get system prompt
        system_prompt = ValidationTestHelper.get_system_prompt_for_tools(["get_weather"])
        
        # Create agent
        agent = LiteAgent(
            model=model_name,
            name=f"DebugAgent_{model_name.replace('/', '_')}",
            system_prompt=system_prompt,
            tools=[get_weather],
            observers=[validation_observer]
        )
        
        # Register parser
        ValidationTestHelper.register_parsers_for_type(
            validation_observer,
            tool_calling_type,
            ["get_weather"]
        )
        
        try:
            # Run the test
            print(f"\nAsk about weather in Tokyo...")
            response = agent.chat("What's the weather in Tokyo?")
            
            print(f"\nResponse: {response}")
            print(f"Type: {type(response)}")
            print(f"Functions called: {validation_observer.called_functions}")
            
            if response is None:
                print("MODEL RETURNED NONE RESPONSE")
            else:
                print("MODEL RETURNED VALID RESPONSE")
                
        except Exception as e:
            print(f"ERROR: {e}")
        
        print(f"\n{'=' * 50}\n")
    
    # Restore the original interface
    liteagent.models.LiteLLMInterface = original_interface

if __name__ == "__main__":
    run_test_with_debug() 