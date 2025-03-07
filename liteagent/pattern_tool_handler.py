"""
Pattern-based tool calling handler that uses XPath-like patterns to detect and extract tool calls.

This approach removes the need for a model registry and handles tool calls based on the structure
of the response instead of model-specific logic.
"""

import json
import re
import copy
import uuid
from typing import Any, Dict, List, Optional, Union, Set, Tuple
from abc import ABC, abstractmethod

from .xpath_extractor import XPathExtractor
from .utils import logger

# ABC for tool calling handlers - defined here to avoid circular imports
class ToolCallingHandlerBase(ABC):
    """Base class for tool calling handlers."""
    
    @abstractmethod
    def extract_tool_calls(self, response: Any) -> List[Dict]:
        """
        Extract tool calls from a model response.
        
        Args:
            response: The model response
            
        Returns:
            A list of tool call dictionaries
        """
        pass
        
    @abstractmethod
    def format_tools_for_model(self, tools: List[Dict]) -> Any:
        """
        Format tools for a model.
        
        Args:
            tools: A list of tool definitions
            
        Returns:
            Formatted tools in the format expected by the model
        """
        pass
        
    @abstractmethod
    def format_tool_results(self, tool_name: str, result: Any, **kwargs) -> Dict:
        """
        Format tool results for a model.
        
        Args:
            tool_name: The name of the tool
            result: The result of the tool call
            
        Returns:
            Formatted tool results in the format expected by the model
        """
        pass
        
    @abstractmethod
    def can_handle_response(self, response: Any) -> bool:
        """
        Determine if this handler can process the given response format.
        
        Args:
            response: The response to check
            
        Returns:
            bool: True if this handler can process the response, False otherwise
        """
        pass

    def _track_tool_call(self, tool_name: str, arguments: Dict):
        """Track a tool call for testing purposes."""
        # Import here to avoid circular imports
        from .tool_calling import ToolCallTracker
        ToolCallTracker.get_instance().record_call(tool_name, arguments)
    
    def _track_tool_result(self, tool_name: str, result: Any):
        """Track a tool result for testing purposes."""
        # Import here to avoid circular imports
        from .tool_calling import ToolCallTracker
        ToolCallTracker.get_instance().record_result(tool_name, result)


class ResponsePattern:
    """
    Defines a pattern for detecting and extracting tool calls from model responses.
    """
    
    def __init__(
        self,
        id: str,
        structure_checks: List[Dict[str, str]],
        extraction: Dict[str, Any],
        result_format: Dict[str, Any],
        priority: int = 0
    ):
        """
        Initialize a response pattern.
        
        Args:
            id: Unique identifier for the pattern
            structure_checks: List of checks to determine if a response matches this pattern
            extraction: Configuration for extracting tool calls
            result_format: Configuration for formatting tool results
            priority: Priority of this pattern (higher values = higher priority)
        """
        self.id = id
        self.structure_checks = structure_checks
        self.extraction = extraction
        self.result_format = result_format
        self.priority = priority


class PatternToolHandler(ToolCallingHandlerBase):
    """
    Tool calling handler that uses configurable patterns to extract and format tool calls.
    """
    
    def __init__(self):
        """Initialize the pattern-based tool handler with predefined patterns."""
        self.xpath_extractor = XPathExtractor()
        
        # Define the patterns in order of priority (highest to lowest)
        self.patterns = [
            # OpenAI-style tool calling
            ResponsePattern(
                id="openai_style",
                structure_checks=[
                    {"exists": "choices/*/message/tool_calls"},
                    {"exists": "choices/*/message/tool_calls/*/function/name"}
                ],
                extraction={
                    "method": "xpath",
                    "tool_calls_path": "choices/*/message/tool_calls/*",
                    "function_name_path": "function/name",
                    "function_args_path": "function/arguments",
                    "tool_id_path": "id"
                },
                result_format={
                    "template": [
                        {"tool_call_id": "{tool_id}", "role": "tool", "content": "{result}"}
                    ],
                    "multiple_format": "array"
                },
                priority=100
            ),
            
            # Anthropic-style tool calling
            ResponsePattern(
                id="anthropic_style",
                structure_checks=[
                    {"exists": "content/0"},
                    {"exists": "content/*/type"}
                ],
                extraction={
                    "method": "content_filter",
                    "content_path": "content",
                    "filter_type": "tool_use"
                },
                result_format={
                    "template": [
                        {"type": "tool_result", "tool_use_id": "{tool_id}", "content": "{result}"}
                    ],
                    "multiple_format": "array"
                },
                priority=90
            ),
            
            # Tools XML tags
            ResponsePattern(
                id="xml_tools_tag",
                structure_checks=[
                    {"exists": "choices/*/message/content"},
                    {"contains": "choices/*/message/content", "pattern": "<tools>.*</tools>"}
                ],
                extraction={
                    "method": "regex",
                    "content_path": "choices/*/message/content",
                    "pattern": r"<tools>\s*(.*?)\s*</tools>",
                    "json_parse": True
                },
                result_format={
                    "template": {"role": "assistant", "content": "Results:\n{results}"},
                    "result_item_template": "- {name}: {result}",
                    "multiple_format": "text",
                    "separator": "\n"
                },
                priority=80
            ),
            
            # Markdown code blocks
            ResponsePattern(
                id="markdown_code_block",
                structure_checks=[
                    {"exists": "choices/*/message/content"},
                    {"contains": "choices/*/message/content", "pattern": "```json.*```"}
                ],
                extraction={
                    "method": "regex",
                    "content_path": "choices/*/message/content",
                    "pattern": r"```(?:json)?\s*(.*?)\s*```",
                    "json_parse": True
                },
                result_format={
                    "template": {"role": "assistant", "content": "Here are the results:\n{results}"},
                    "result_item_template": "• {name}: {result}",
                    "multiple_format": "text",
                    "separator": "\n\n"
                },
                priority=70
            ),
            
            # Ollama-style tool calling
            ResponsePattern(
                id="ollama_style",
                structure_checks=[
                    {"exists": "message/tool_calls"},
                    {"exists": "message/tool_calls/*/function/name"}
                ],
                extraction={
                    "method": "xpath",
                    "tool_calls_path": "message/tool_calls/*",
                    "function_name_path": "function/name",
                    "function_args_path": "function/arguments",
                    "tool_id_path": "id"  # May be missing, will use fallback
                },
                result_format={
                    "template": {"role": "assistant", "content": "{results}"},
                    "result_item_template": "Function {name} returned: {result}",
                    "multiple_format": "text",
                    "separator": "\n"
                },
                priority=60
            ),
            
            # Legacy OpenAI function calling
            ResponsePattern(
                id="legacy_openai",
                structure_checks=[
                    {"exists": "choices/*/message/function_call"},
                    {"exists": "choices/*/message/function_call/name"}
                ],
                extraction={
                    "method": "xpath",
                    "tool_calls_path": "choices/*/message",
                    "function_name_path": "function_call/name",
                    "function_args_path": "function_call/arguments"
                },
                result_format={
                    "template": {"role": "function", "name": "{name}", "content": "{result}"},
                    "multiple_format": "single"  # Legacy format only supports one function
                },
                priority=50
            ),
            
            # Fallback: Try to find any JSON structure that looks like a tool call
            ResponsePattern(
                id="generic_json_in_text",
                structure_checks=[
                    {"exists": "choices/*/message/content"},
                    {"contains": "choices/*/message/content", "pattern": "\\{.*name.*arguments.*\\}"}
                ],
                extraction={
                    "method": "regex_json",
                    "content_path": "choices/*/message/content",
                    "pattern": r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}",  # Non-recursive regex to find JSON objects
                    "json_validate": ["name", "arguments"]  # Fields that must exist
                },
                result_format={
                    "template": {"role": "assistant", "content": "I got these results: {results}"},
                    "result_item_template": "{result}",
                    "multiple_format": "text",
                    "separator": ", "
                },
                priority=10
            ),
            
            # Mistral medium/small format
            ResponsePattern(
                id="mistral_medium",
                structure_checks=[
                    {"exists": "choices/*/message/content"},
                    {"exists": "choices/*/message/tool_calls"}
                ],
                extraction={
                    "method": "xpath",
                    "tool_calls_path": "choices/*/message/tool_calls",
                    "function_name_path": "name",
                    "function_args_path": "arguments",
                    "tool_id_path": "id"
                },
                result_format={
                    "template": {"role": "assistant", "content": "Results: {results}"},
                    "result_item_template": "{name}: {result}",
                    "multiple_format": "text",
                    "separator": "\n"
                },
                priority=85
            ),
            
            # Groq without tool_calls
            ResponsePattern(
                id="groq_no_tools",
                structure_checks=[
                    {"exists": "choices/*/message/content"},
                    {"exists": "x_groq"}
                ],
                extraction={
                    "method": "regex_json",
                    "content_path": "choices/*/message/content",
                    "pattern": r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}",
                    "json_validate": ["name"]
                },
                result_format={
                    "template": {"role": "assistant", "content": "Results: {results}"},
                    "result_item_template": "{result}",
                    "multiple_format": "text",
                    "separator": "\n"
                },
                priority=40
            ),
            
            # Mistral medium with null tool_calls
            ResponsePattern(
                id="mistral_null_tools",
                structure_checks=[
                    {"exists": "choices/*/message/content"}
                ],
                extraction={
                    "method": "null_tools",
                    "content_path": "choices/*/message/content"
                },
                result_format={
                    "template": {"role": "assistant", "content": "{results}"},
                    "result_item_template": "{result}",
                    "multiple_format": "text",
                    "separator": "\n"
                },
                priority=5  # Very low priority as a fallback
            ),
            
            # Error responses
            ResponsePattern(
                id="error_response",
                structure_checks=[
                    {"exists": "error"}
                ],
                extraction={
                    "method": "null_tools",
                    "content_path": "error/message"
                },
                result_format={
                    "template": {"role": "assistant", "content": "Error: {results}"},
                    "result_item_template": "{result}",
                    "multiple_format": "text",
                    "separator": "\n"
                },
                priority=20
            ),
            
            # Ollama without tool_calls
            ResponsePattern(
                id="ollama_no_tools",
                structure_checks=[
                    {"exists": "message"},
                    {"exists": "model"}
                ],
                extraction={
                    "method": "null_tools",
                    "content_path": "message/content"
                },
                result_format={
                    "template": {"role": "assistant", "content": "{results}"},
                    "result_item_template": "{result}",
                    "multiple_format": "text",
                    "separator": "\n"
                },
                priority=15
            ),
            
            # Final fallback for any response
            ResponsePattern(
                id="fallback",
                structure_checks=[],  # No checks, matches anything
                extraction={
                    "method": "null_tools",
                    "content_path": ""
                },
                result_format={
                    "template": {"role": "assistant", "content": "No tool calls found"},
                    "result_item_template": "{result}",
                    "multiple_format": "text",
                    "separator": "\n"
                },
                priority=1  # Lowest priority
            ),
        ]
        
        # Sort patterns by priority (highest first)
        self.patterns.sort(key=lambda p: p.priority, reverse=True)
    
    def detect_pattern(self, response: Any) -> Optional[ResponsePattern]:
        """
        Detect which pattern matches the response structure.
        
        Args:
            response: The model response
            
        Returns:
            The matching pattern, or None if no pattern matches
        """
        # Convert response to dict if it's not already
        if not isinstance(response, dict):
            try:
                # Try to convert to dict if it's an object with a dict-like structure
                response_dict = response.__dict__ if hasattr(response, '__dict__') else {}
            except:
                # Fall back to an empty dict
                response_dict = {}
                logger.warning(f"Failed to convert response to dict: {type(response)}")
        else:
            response_dict = response
        
        # Try each pattern in order of priority
        for pattern in self.patterns:
            if self._check_structure(response_dict, pattern.structure_checks):
                logger.debug(f"Response matches pattern: {pattern.id}")
                return pattern
        
        # No pattern matched
        logger.warning("No matching response pattern found")
        return None
    
    def _check_structure(self, data: Dict, checks: List[Dict[str, Any]]) -> bool:
        """
        Check if data matches all the structural checks.
        
        Args:
            data: The data to check
            checks: List of structural checks
            
        Returns:
            True if all checks pass, False otherwise
        """
        for check in checks:
            # Check if a path exists
            if "exists" in check:
                path = check["exists"]
                if not self.xpath_extractor.path_exists(data, path):
                    return False
            
            # Check if content at path contains a pattern
            elif "contains" in check:
                path = check["contains"]
                pattern = check.get("pattern")
                value = check.get("value")
                
                content = self.xpath_extractor.get_node(data, path)
                
                if pattern:
                    # Check for regex pattern
                    if not content or not re.search(pattern, str(content)):
                        return False
                elif value:
                    # Check for exact value
                    if not content or value not in content:
                        return False
                else:
                    # Invalid check
                    return False
        
        # All checks passed
        return True
    
    def extract_tool_calls(self, response: Any) -> List[Dict]:
        """
        Extract tool calls from a model response.
        
        Args:
            response: The model response
            
        Returns:
            A list of tool call dictionaries
        """
        logger.debug(f"Extracting tool calls from response: {type(response)}")
        
        # Handle None response
        if response is None:
            logger.debug("Received None response")
            return []
        
        # Convert response to dict if it's not already
        if not isinstance(response, dict):
            try:
                # Try to convert to dict if it's an object with a dict-like structure
                response_dict = response.__dict__ if hasattr(response, '__dict__') else {}
            except:
                # Fall back to an empty dict
                response_dict = {}
                logger.warning(f"Failed to convert response to dict: {type(response)}")
        else:
            response_dict = response
        
        # Debug the response structure
        self._debug_structure(response_dict)
        
        # Detect the pattern
        pattern = self.detect_pattern(response_dict)
        if not pattern:
            logger.warning("No pattern detected for response")
            return []
        
        # Extract tool calls using the appropriate method
        extraction = pattern.extraction
        method = extraction["method"]
        
        if method == "xpath":
            return self._extract_xpath(response_dict, extraction)
        elif method == "regex":
            return self._extract_regex(response_dict, extraction)
        elif method == "regex_json":
            return self._extract_regex_json(response_dict, extraction)
        elif method == "content_filter":
            return self._extract_content_filter(response_dict, extraction)
        elif method == "null_tools":
            return self._extract_null_tools(response_dict, extraction)
        else:
            logger.warning(f"Unknown extraction method: {method}")
            return []
    
    def _extract_xpath(self, data: Dict, config: Dict) -> List[Dict]:
        """
        Extract tool calls using XPath.
        
        Args:
            data: Response data
            config: Extraction configuration
            
        Returns:
            List of extracted tool calls
        """
        tool_calls_path = config["tool_calls_path"]
        function_name_path = config["function_name_path"]
        function_args_path = config["function_args_path"]
        tool_id_path = config.get("tool_id_path")
        
        # Extract tool calls
        tool_calls = self.xpath_extractor.get_nodes(data, tool_calls_path)
        logger.debug(f"Found {len(tool_calls)} potential tool calls at path {tool_calls_path}")
        logger.debug(f"Tool calls data: {tool_calls}")
        
        result = []
        
        for idx, tc in enumerate(tool_calls):
            # Extract function name and arguments
            name = self.xpath_extractor.get_node(tc, function_name_path)
            args = self.xpath_extractor.get_node(tc, function_args_path)
            
            # Handle missing name or arguments
            if not name:
                logger.warning(f"Missing function name in tool call: {tc}")
                continue
            
            # Handle JSON string arguments
            if isinstance(args, str) and args.startswith('{'):
                try:
                    args = json.loads(args)
                except json.JSONDecodeError:
                    logger.warning(f"Failed to parse function arguments: {args}")
                    continue
            
            # Use a default ID if not provided
            if tool_id_path:
                tool_id = self.xpath_extractor.get_node(tc, tool_id_path)
            else:
                tool_id = None
                
            if not tool_id:
                tool_id = f"call_{idx}_{uuid.uuid4()}"
            
            # Add tool call to results
            result.append({
                "name": name,
                "arguments": args or {},
                "id": tool_id
            })
            
            # Track this tool call for testing
            self._track_tool_call(name, args or {})
        
        return result
    
    def _extract_regex(self, data: Dict, config: Dict) -> List[Dict]:
        """
        Extract tool calls using regex on content.
        
        Args:
            data: Response data
            config: Extraction configuration
            
        Returns:
            List of extracted tool calls
        """
        content_path = config["content_path"]
        pattern = config["pattern"]
        json_parse = config.get("json_parse", False)
        
        # Extract content
        content = self.xpath_extractor.get_node(data, content_path)
        if not content:
            logger.warning(f"Content not found at path: {content_path}")
            return []
        
        # Find matches
        matches = re.findall(pattern, str(content), re.DOTALL)
        result = []
        
        for idx, match in enumerate(matches):
            if json_parse:
                try:
                    # Try to parse as JSON
                    tool_data = json.loads(match)
                    
                    # Validate that required fields exist
                    if "name" not in tool_data:
                        logger.warning(f"Missing 'name' in tool data: {tool_data}")
                        continue
                    
                    # Get arguments
                    args = tool_data.get("arguments", {})
                    
                    # Create tool call
                    result.append({
                        "name": tool_data["name"],
                        "arguments": args,
                        "id": tool_data.get("id", f"extracted_id_{idx}_{uuid.uuid4()}")
                    })
                    
                    # Track this tool call for testing
                    self._track_tool_call(tool_data["name"], args)
                    
                except json.JSONDecodeError:
                    logger.warning(f"Failed to parse JSON from content: {match}")
            else:
                # Use raw string
                result.append({
                    "name": "unknown",
                    "arguments": match,
                    "id": f"extracted_id_{idx}_{uuid.uuid4()}"
                })
        
        return result
    
    def _extract_regex_json(self, data: Dict, config: Dict) -> List[Dict]:
        """
        Extract JSON objects from text that appear to be tool calls.
        
        Args:
            data: Response data
            config: Extraction configuration
            
        Returns:
            List of extracted tool calls
        """
        content_path = config["content_path"]
        pattern = config["pattern"]
        required_fields = config.get("json_validate", ["name"])
        
        # Extract content
        content = self.xpath_extractor.get_node(data, content_path)
        if not content:
            logger.warning(f"Content not found at path: {content_path}")
            return []
        
        # Find all JSON-like patterns in the content
        import re
        matches = re.findall(pattern, str(content))
        result = []
        
        for idx, match in enumerate(matches):
            try:
                # Try to parse as JSON
                json_obj = json.loads(match)
                
                # Check if it has the required fields
                if all(field in json_obj for field in required_fields):
                    # Get arguments (could be under different names)
                    args = json_obj.get("arguments", json_obj.get("params", json_obj.get("args", {})))
                    
                    # Create tool call
                    result.append({
                        "name": json_obj["name"],
                        "arguments": args,
                        "id": json_obj.get("id", f"extracted_id_{idx}_{uuid.uuid4()}")
                    })
                    
                    # Track this tool call for testing
                    self._track_tool_call(json_obj["name"], args)
            except (json.JSONDecodeError, TypeError):
                logger.debug(f"Failed to parse JSON from content: {match}")
        
        return result
    
    def _extract_content_filter(self, data: Dict, config: Dict) -> List[Dict]:
        """
        Extract tool calls by filtering content array items by type.
        
        Args:
            data: Response data
            config: Extraction configuration
            
        Returns:
            List of extracted tool calls
        """
        content_path = config["content_path"]
        filter_type = config["filter_type"]
        
        # Get the content array
        content = self.xpath_extractor.get_node(data, content_path)
        if not content or not isinstance(content, list):
            logger.warning(f"Content not found at path '{content_path}' or not a list")
            return []
        
        # Filter items by type
        result = []
        for idx, item in enumerate(content):
            if isinstance(item, dict) and item.get("type") == filter_type:
                # Extract tool call data
                name = item.get("name")
                args = item.get("input", {})
                tool_id = item.get("id", f"extracted_id_{idx}_{uuid.uuid4()}")
                
                if not name:
                    logger.warning(f"Missing name in tool call: {item}")
                    continue
                
                # Add tool call to results
                result.append({
                    "name": name,
                    "arguments": args,
                    "id": tool_id
                })
                
                # Track this tool call for testing
                self._track_tool_call(name, args)
        
        return result
    
    def _extract_null_tools(self, data: Dict, config: Dict) -> List[Dict]:
        """
        Handle responses with null tool_calls.
        
        Args:
            data: Response data
            config: Extraction configuration
            
        Returns:
            Empty list since there are no tool calls
        """
        # These responses don't actually have tool calls, so return an empty list
        return []
    
    def format_tools_for_model(self, tools: List[Dict]) -> Any:
        """
        Format tools for a model. This is a generic implementation that works for most models.
        
        Args:
            tools: A list of tool definitions
            
        Returns:
            Formatted tools in a generic format
        """
        # For most models, the format is the same as OpenAI
        formatted_tools = []
        for tool in tools:
            # Create a copy of the tool to avoid modifying the original
            tool_copy = tool.copy()
            
            # Add the "type" field if it doesn't exist
            if "type" not in tool_copy:
                tool_copy["type"] = "function"
            
            # Ensure the tool has a "function" property
            if "function" not in tool_copy:
                function_data = {}
                
                # Move name, description, and parameters to a function object
                for field in ["name", "description", "parameters"]:
                    if field in tool_copy:
                        function_data[field] = tool_copy.pop(field)
                
                # Add the function property
                tool_copy["function"] = function_data
            
            # Add to the formatted tools
            formatted_tools.append(tool_copy)
        
        return formatted_tools
    
    def format_tool_results(self, tool_name: str, result: Any, **kwargs) -> Dict:
        """
        Format tool results for a model.
        
        Args:
            tool_name: The name of the tool
            result: The result of the tool call
            **kwargs: Additional formatting options
            
        Returns:
            Formatted tool results
        """
        # Get tool call ID if provided
        tool_id = kwargs.get("tool_id", f"call_{uuid.uuid4()}")
        
        # Track this tool result for testing
        self._track_tool_result(tool_name, result)
        
        # Default to OpenAI format
        return {
            "tool_call_id": tool_id,
            "role": "tool",
            "content": str(result) if result is not None else ""
        }
    
    def format_multiple_tool_results(self, pattern_id: str, tool_calls: List[Dict], results: List[Any]) -> Any:
        """
        Format multiple tool results according to the pattern's result_format.
        
        Args:
            pattern_id: ID of the pattern that matched the response
            tool_calls: List of tool calls
            results: List of tool results
            
        Returns:
            Formatted tool results
        """
        # Find the pattern
        pattern = next((p for p in self.patterns if p.id == pattern_id), None)
        
        if not pattern:
            # Fallback to a simple format
            return [self.format_tool_results(tc["name"], res, tool_id=tc.get("id", f"call_{uuid.uuid4()}"))
                   for tc, res in zip(tool_calls, results)]
        
        format_config = pattern.result_format
        template = format_config["template"]
        multiple_format = format_config.get("multiple_format", "array")
        
        if multiple_format == "array":
            # Return array of formatted items (OpenAI, Anthropic style)
            formatted_results = []
            for tc, result in zip(tool_calls, results):
                item = copy.deepcopy(template[0])  # Assume template is an array with one item
                for key, value in item.items():
                    item[key] = value.replace("{tool_id}", tc.get("id", ""))
                    item[key] = item[key].replace("{result}", str(result) if result is not None else "")
                    item[key] = item[key].replace("{name}", tc.get("name", ""))
                formatted_results.append(item)
            return formatted_results
        
        elif multiple_format == "single":
            # Return the first result only (legacy function calling)
            if not tool_calls or not results:
                return None
                
            tc = tool_calls[0]
            result = results[0]
            
            # Copy the template
            formatted = copy.deepcopy(template)
            for key, value in formatted.items():
                formatted[key] = value.replace("{tool_id}", tc.get("id", ""))
                formatted[key] = formatted[key].replace("{result}", str(result) if result is not None else "")
                formatted[key] = formatted[key].replace("{name}", tc.get("name", ""))
            
            return formatted
        
        elif multiple_format == "text":
            # Return text with all results (text-based models)
            item_template = format_config.get("result_item_template", "{result}")
            separator = format_config.get("separator", "\n")
            
            formatted_items = []
            for tc, result in zip(tool_calls, results):
                item = item_template.replace("{tool_id}", tc.get("id", ""))
                item = item.replace("{result}", str(result) if result is not None else "")
                item = item.replace("{name}", tc.get("name", ""))
                formatted_items.append(item)
            
            all_results = separator.join(formatted_items)
            
            # Apply to outer template (which is usually a dict)
            formatted = copy.deepcopy(template)
            for key, value in formatted.items():
                formatted[key] = value.replace("{results}", all_results)
            
            return formatted
        
        else:
            # Unknown format, return a simple dict
            return {"results": results}
    
    def can_handle_response(self, response: Any) -> bool:
        """
        Determine if this handler can process the given response format.
        
        Args:
            response: The response to check
            
        Returns:
            True if this handler can process the response, False otherwise
        """
        # This handler can handle any response for which we can detect a pattern
        pattern = self.detect_pattern(response)
        return pattern is not None
    
    def _debug_structure(self, response: Dict):
        """
        Log detailed information about the response structure to help with debugging.
        
        Args:
            response: The response data to analyze
        """
        # Get all paths in the response
        paths = self.xpath_extractor.get_all_paths(response)
        sorted_paths = sorted(list(paths))
        
        logger.debug(f"Response structure - paths: {sorted_paths}")
        
        # Check for specific paths that might contain tool calls
        tool_paths = [
            "content/*/type", 
            "choices/*/message/tool_calls",
            "message/tool_calls"
        ]
        
        for path in tool_paths:
            try:
                data = self.xpath_extractor.get_nodes(response, path)
                logger.debug(f"Data at path '{path}': {data}")
            except:
                logger.debug(f"Error accessing path '{path}'")
                
        # Try to find tool_use types
        if "content" in response and isinstance(response["content"], list):
            for i, item in enumerate(response["content"]):
                if isinstance(item, dict) and item.get("type") == "tool_use":
                    logger.debug(f"Found tool_use at content/{i}: {item}") 