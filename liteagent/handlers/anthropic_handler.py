"""
Anthropic-specific tool calling handler implementation.
"""

import json
import uuid
import copy
from typing import Dict, List, Any

from ..pattern_tool_handler import PatternToolHandler

class AnthropicToolCallingHandler(PatternToolHandler):
    """Compatibility class for Anthropic-style tool calling."""
    
    def extract_tool_calls(self, response: Any) -> List[Dict]:
        """
        Override to handle mock objects in tests and raw API responses.
        
        Args:
            response: The model response
            
        Returns:
            A list of extracted tool calls
        """
        # Special case for Anthropic mock objects in tests
        if hasattr(response, 'content') and isinstance(response.content, list):
            tool_calls = []
            for item in response.content:
                if hasattr(item, 'type') and item.type == 'tool_use':
                    tool_call_data = {
                        "name": item.name if hasattr(item, 'name') else "unknown",
                        "arguments": item.input if hasattr(item, 'input') else {},
                        "id": item.id if hasattr(item, 'id') else str(uuid.uuid4())
                    }
                    tool_calls.append(tool_call_data)
                    self._track_tool_call(tool_call_data["name"], tool_call_data["arguments"])
            return tool_calls
        
        # Check for direct Claude API format
        if hasattr(response, 'type') and response.type == 'message':
            if hasattr(response, 'content') and isinstance(response.content, list):
                tool_calls = []
                for block in response.content:
                    if hasattr(block, 'type') and block.type == 'tool_use':
                        if hasattr(block, 'name') and hasattr(block, 'input'):
                            tool_call_data = {
                                "name": block.name,
                                "arguments": block.input,
                                "id": block.id if hasattr(block, 'id') else str(uuid.uuid4())
                            }
                            tool_calls.append(tool_call_data)
                            self._track_tool_call(tool_call_data["name"], tool_call_data["arguments"])
                return tool_calls
        
        # Handle LiteLLM wrapped responses
        if hasattr(response, 'choices') and response.choices:
            if hasattr(response.choices[0], 'message'):
                message = response.choices[0].message
                
                # Try to extract tool calls from message.tool_calls
                if hasattr(message, 'tool_calls') and message.tool_calls:
                    tool_calls = []
                    for tc in message.tool_calls:
                        if hasattr(tc, 'function'):
                            args = tc.function.arguments
                            if isinstance(args, str):
                                try:
                                    args = json.loads(args)
                                except:
                                    args = {}
                            
                            tool_call_data = {
                                "name": tc.function.name,
                                "arguments": args,
                                "id": tc.id if hasattr(tc, 'id') else str(uuid.uuid4())
                            }
                            tool_calls.append(tool_call_data)
                            self._track_tool_call(tool_call_data["name"], tool_call_data["arguments"])
                    return tool_calls
                
                # Try to extract from content blocks
                if hasattr(message, 'content') and isinstance(message.content, list):
                    tool_calls = []
                    for block in message.content:
                        if hasattr(block, 'type') and block.type == 'tool_use':
                            if hasattr(block, 'name') and hasattr(block, 'input'):
                                tool_call_data = {
                                    "name": block.name,
                                    "arguments": block.input,
                                    "id": block.id if hasattr(block, 'id') else str(uuid.uuid4())
                                }
                                tool_calls.append(tool_call_data)
                                self._track_tool_call(tool_call_data["name"], tool_call_data["arguments"])
                    return tool_calls
        
        # Fall back to pattern-based handling for real responses
        return super().extract_tool_calls(response)
        
    def format_tools_for_model(self, tools: List[Dict]) -> List[Dict]:
        """
        Override to provide Anthropic-specific tool format.
        
        Args:
            tools: A list of tool definitions
            
        Returns:
            Formatted tools for Anthropic
        """
        anthropic_tools = []
        
        for tool in tools:
            parameters = tool.get("parameters", {})
            
            # Convert properties from OpenAI format to Anthropic format
            parameters_schema = self._convert_parameters_to_schema(parameters)
            
            # Add detailed descriptions to help Claude understand how to use the tool
            description = tool.get("description", "")
            name = tool.get("name", "")
            
            # Create Anthropic-compliant tool definition
            anthropic_tool = {
                "name": name,
                "description": description,
                "input_schema": parameters_schema
            }
            
            anthropic_tools.append(anthropic_tool)
            
        return anthropic_tools
        
    def _convert_parameters_to_schema(self, parameters: Dict) -> Dict:
        """
        Convert OpenAI-style parameters to Anthropic input_schema.
        
        Args:
            parameters: The parameters in OpenAI format
            
        Returns:
            Parameters in Anthropic format
        """
        # Start with a basic schema
        schema = {
            "type": "object",
            "properties": {},
            "required": parameters.get("required", [])
        }
        
        # Copy properties
        if "properties" in parameters:
            properties = {}
            for prop_name, prop_data in parameters["properties"].items():
                # Create a deep copy to avoid modifying the original
                prop_copy = copy.deepcopy(prop_data)
                
                # Make sure all properties have a description
                if "description" not in prop_copy:
                    prop_copy["description"] = f"The {prop_name} parameter"
                    
                properties[prop_name] = prop_copy
                
            schema["properties"] = properties
            
        return schema
        
    def format_tool_results(self, tool_name: str, result: Any, **kwargs) -> Dict:
        """
        Override to match Anthropic format for tool results.
        
        Args:
            tool_name: The name of the tool
            result: The result from the tool
            **kwargs: Additional keyword arguments
            
        Returns:
            A formatted tool result for Anthropic
        """
        # Format content as string or JSON as appropriate
        content = result
        if isinstance(result, (dict, list)):
            # For structured data, use JSON string
            content = json.dumps(result)
        else:
            # Otherwise convert to string
            content = str(result) if result is not None else ""
        
        # Track for testing
        self._track_tool_result(tool_name, result)
        
        # Format according to Anthropic's expectations for tool results
        tool_id = kwargs.get("tool_id", f"call_{uuid.uuid4()}")
        
        return {
            "role": "tool",
            "tool_call_id": tool_id,
            "content": content,
            "name": tool_name  # Anthropic format includes the name
        } 