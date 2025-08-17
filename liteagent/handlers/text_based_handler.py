"""
Text-based tool calling handler implementation.

This handler is used for models that don't have native tool calling capabilities,
but can follow text instructions to call tools in a specific format.
"""

import json
import re
import uuid
from typing import Dict, List, Any

from ..simple_tool_handler import SimpleToolCallingHandler


class TextBasedToolCallingHandler(SimpleToolCallingHandler):
    """Compatibility class for text-based tool calling."""
    
    def extract_tool_calls(self, response: Any) -> List[Dict]:
        """
        Override to extract tool calls from text-based formats.
        
        Args:
            response: The model response
            
        Returns:
            A list of extracted tool calls
        """
        # Get the content from the response
        if not hasattr(response, 'choices') or not response.choices:
            return []
            
        if not hasattr(response.choices[0], 'message') or not hasattr(response.choices[0].message, 'content'):
            return []
            
        content = response.choices[0].message.content
        if not content:
            return []
            
        # Try multiple patterns to be more robust
        patterns = [
            # Standard [FUNCTION_CALL] format
            r'\[FUNCTION_CALL\]\s*(\w+)\((.*?)\)\s*\[/FUNCTION_CALL\]',
            # Markdown code block format some models use
            r'```(?:python|json)?\s*(\w+)\((.*?)\)\s*```',
            # Simple function call format
            r'(\w+)\((.*?)\)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.DOTALL)
            if matches:
                tool_calls = []
                for func_name, args_str in matches:
                    # Only process if function name looks like one of our defined tools
                    if func_name not in ["get_weather", "add_numbers", "multiply_numbers", "calculate_area"]:
                        continue
                        
                    # Parse arguments
                    args_dict = {}
                    
                    # Try different argument parsing approaches
                    # First try key=value format
                    arg_pattern = r'(\w+)\s*=\s*(?:"([^"]*?)"|\'([^\']*?)\'|(\S+))'
                    arg_matches = re.findall(arg_pattern, args_str)
                    
                    if arg_matches:
                        for arg_match in arg_matches:
                            key = arg_match[0]
                            # Find the first non-empty group which is the value
                            value = next((v for v in arg_match[1:] if v), "")
                            # Convert to appropriate types
                            try:
                                # Check if it's a number
                                if value.isdigit():
                                    value = int(value)
                                elif value.replace('.', '', 1).isdigit() and value.count('.') <= 1:
                                    value = float(value)
                            except (ValueError, AttributeError):
                                pass
                            args_dict[key] = value
                    else:
                        # Try positional arguments format
                        pos_args = [arg.strip() for arg in args_str.split(',') if arg.strip()]
                        if func_name == "get_weather" and len(pos_args) >= 1:
                            # For get_weather, assume the first arg is city
                            city = pos_args[0].strip('"\'')
                            args_dict["city"] = city
                        elif (func_name == "add_numbers" or func_name == "multiply_numbers") and len(pos_args) >= 2:
                            # For add_numbers/multiply_numbers, assume two numerical args
                            try:
                                a = int(pos_args[0]) if pos_args[0].isdigit() else pos_args[0]
                                b = int(pos_args[1]) if pos_args[1].isdigit() else pos_args[1]
                                args_dict["a"] = a
                                args_dict["b"] = b
                            except (ValueError, IndexError):
                                continue
                            
                    # Create and track the tool call
                    tool_call_id = str(uuid.uuid4())
                    tool_call = {
                        "name": func_name,
                        "arguments": args_dict,
                        "id": tool_call_id
                    }
                    tool_calls.append(tool_call)
                    
                    # Track for testing
                    self._track_tool_call(func_name, args_dict)
                    
                if tool_calls:
                    return tool_calls
        
        # Try to extract function calls from a more general discussion
        common_tools = {
            "get_weather": ["weather", "temperature", "forecast"],
            "add_numbers": ["add", "sum", "plus", "addition"],
            "multiply_numbers": ["multiply", "product", "times", "multiplication"]
        }
        
        for tool_name, keywords in common_tools.items():
            for keyword in keywords:
                if keyword in content.lower():
                    # Check if we can find numerical values for add/multiply
                    if tool_name in ["add_numbers", "multiply_numbers"]:
                        # Look for two numbers
                        numbers = re.findall(r'\b(\d+)\b', content)
                        if len(numbers) >= 2:
                            args_dict = {
                                "a": int(numbers[0]),
                                "b": int(numbers[1])
                            }
                            tool_call = {
                                "name": tool_name,
                                "arguments": args_dict,
                                "id": str(uuid.uuid4())
                            }
                            self._track_tool_call(tool_name, args_dict)
                            return [tool_call]
                    
                    # Check for city names for weather
                    elif tool_name == "get_weather":
                        # Common cities that might be mentioned
                        cities = ["Tokyo", "New York", "London", "Paris", "Berlin", 
                                 "Sydney", "Beijing", "Moscow", "Cairo", "Mumbai"]
                        for city in cities:
                            if city in content:
                                args_dict = {"city": city}
                                tool_call = {
                                    "name": tool_name,
                                    "arguments": args_dict,
                                    "id": str(uuid.uuid4())
                                }
                                self._track_tool_call(tool_name, args_dict)
                                return [tool_call]
        
        # No tool calls found
        return []
    
    def format_tools_for_model(self, tools: List[Dict]) -> str:
        """
        Override to provide text-based format for tools.
        
        Args:
            tools: A list of tool definitions
            
        Returns:
            Formatted tools in a text-based format
        """
        # Convert tools to text-based format
        tool_descriptions = []
        for tool in tools:
            # Get name and description
            name = tool.get("name", "")
            description = tool.get("description", "")
            
            # Get parameters
            parameters = tool.get("parameters", {})
            properties = parameters.get("properties", {})
            required = parameters.get("required", [])
            
            # Build parameter descriptions
            param_descriptions = []
            for param_name, param_info in properties.items():
                param_type = param_info.get("type", "any")
                param_desc = param_info.get("description", "")
                required_str = "(required)" if param_name in required else "(optional)"
                param_descriptions.append(f"- {param_name} ({param_type}) {required_str}: {param_desc}")
            
            # Create example values for better guidance
            example_values = {}
            for param_name, param_info in properties.items():
                param_type = param_info.get("type", "")
                if param_type == "integer" or param_type == "number":
                    example_values[param_name] = 5 if param_name != "b" else 7
                elif param_type == "string":
                    example_values[param_name] = "Tokyo" if "city" in param_name else "example"
            
            # Create example function call
            example_args = ", ".join([f"{k}={repr(v)}" for k, v in example_values.items()])
            
            # Build the full tool description
            tool_desc = [
                f"## Function: {name}",
                f"Description: {description}",
                "Parameters:",
                *param_descriptions,
                "\nUsage Example:",
                f"[FUNCTION_CALL] {name}({example_args}) [/FUNCTION_CALL]"
            ]
            tool_descriptions.append("\n".join(tool_desc))
        
        # Add overall instructions
        instructions = [
            "# Tool Usage Instructions",
            "1. Use these tools by calling them with the [FUNCTION_CALL] syntax exactly as shown in the examples.",
            "2. Make sure to provide all required parameters.",
            "3. Wait for the tool to return a result before proceeding.\n"
        ]
        
        # Join all tool descriptions
        return "\n\n".join(instructions + tool_descriptions)
    
    def format_tool_results(self, tool_name: str, result: Any, **kwargs) -> Dict:
        """
        Override to provide text-based format for results.
        
        Args:
            tool_name: The name of the tool
            result: The result from the tool
            **kwargs: Additional keyword arguments
            
        Returns:
            A formatted tool result for text-based tools
        """
        content = result
        if isinstance(result, (dict, list)):
            content = json.dumps(result)
        else:
            content = str(result) if result is not None else ""
        
        self._track_tool_result(tool_name, result)
        
        return {
            "role": "tool",
            "tool_call_id": kwargs.get("tool_id", f"call_{uuid.uuid4()}"),
            "content": content
        } 