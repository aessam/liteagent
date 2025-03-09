"""
Simplified pattern-based tool calling handler.

This handler uses a streamlined approach to detect and extract tool calls from
model responses based on their structure, removing the need for model-specific logic.
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
        Format a tool result for a model.
        
        Args:
            tool_name: The name of the tool
            result: The result from the tool
            **kwargs: Additional keyword arguments
            
        Returns:
            A formatted result in the format expected by the model
        """
        pass
        
    @abstractmethod
    def can_handle_response(self, response: Any) -> bool:
        """
        Determine if this handler can process the given response format.
        
        Args:
            response: The response to check
            
        Returns:
            True if this handler can process the response, False otherwise
        """
        pass

    def _track_tool_call(self, tool_name: str, arguments: Dict):
        """For tracking purposes (optional)."""
        pass
        
    def _track_tool_result(self, tool_name: str, result: Any):
        """For tracking purposes (optional)."""
        pass


class ResponsePattern:
    """Defines a pattern for detecting and extracting tool calls from model responses."""
    
    def __init__(
        self,
        id: str,
        structure_checks: List[Dict[str, str]],
        extraction: Dict[str, Any],
        result_format: Dict[str, Any],
        priority: int = 0
    ):
        """Initialize a response pattern."""
        self.id = id
        self.structure_checks = structure_checks
        self.extraction = extraction
        self.result_format = result_format
        self.priority = priority


class PatternToolHandler(ToolCallingHandlerBase):
    """
    Simplified pattern-based tool calling handler.
    
    This handler uses patterns to detect and extract tool calls from model responses
    without requiring model-specific implementations.
    """
    
    def __init__(self):
        """Initialize the pattern-based tool handler with core patterns."""
        self.xpath_extractor = XPathExtractor()
        
        # Core patterns for extracting tool calls - simplified to essential formats
        self.patterns = [
            # OpenAI format
            ResponsePattern(
                id="openai",
                structure_checks=[
                    {"exists": "choices/*/message/tool_calls"}
                ],
                extraction={
                    "method": "xpath",
                    "tool_calls_path": "choices/*/message/tool_calls",
                    "function_name_path": "function/name",
                    "function_args_path": "function/arguments"
                },
                result_format={
                    "template": {"role": "tool", "tool_call_id": "{id}", "content": "{result}"},
                    "multiple_format": "array"
                },
                priority=100
            ),
            
            # Anthropic format
            ResponsePattern(
                id="anthropic",
                structure_checks=[
                    {"exists": "content"}
                ],
                extraction={
                    "method": "xpath",
                    "tool_calls_path": "content/type=tool_use",
                    "function_name_path": "name",
                    "function_args_path": "input"
                },
                result_format={
                    "template": {"type": "tool_result", "tool_use_id": "{id}", "content": "{result}"},
                    "multiple_format": "array"
                },
                priority=90
            ),
            
            # Text-based format (for models that use text to describe tool calls)
            ResponsePattern(
                id="text_based",
                structure_checks=[
                    {"exists": "choices/*/message/content"}
                ],
                extraction={
                    "method": "regex_json",
                    "content_path": "choices/*/message/content",
                    "pattern": r"\{[\s\S]*?\"name\"[\s\S]*?\"arguments\"[\s\S]*?\}"
                },
                result_format={
                    "template": {"role": "assistant", "content": "I used the tool and got: {result}"},
                    "multiple_format": "text"
                },
                priority=10
            )
        ]
        
        # For testing and debugging
        self.last_detected_pattern = None
    
    def detect_pattern(self, response: Any) -> Optional[ResponsePattern]:
        """Detect which pattern matches the response structure."""
        # Convert response to dict if it's not already
        response_dict = self._ensure_dict(response)
        
        # Try each pattern in order of priority
        for pattern in sorted(self.patterns, key=lambda p: p.priority, reverse=True):
            if self._check_structure(response_dict, pattern.structure_checks):
                self.last_detected_pattern = pattern
                return pattern
        
        # No pattern matched
        return None
    
    def _ensure_dict(self, response: Any) -> Dict:
        """Ensure the response is a dictionary."""
        if isinstance(response, dict):
            return response
        
        try:
            # Try to convert to dict if it's an object with a dict-like structure
            return response.__dict__ if hasattr(response, '__dict__') else {}
        except:
            # Fall back to an empty dict
            logger.warning(f"Failed to convert response to dict: {type(response)}")
            return {}
    
    def _check_structure(self, data: Dict, checks: List[Dict[str, Any]]) -> bool:
        """Check if data matches all the structural checks."""
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
                
                content = self.xpath_extractor.get_node(data, path)
                
                if pattern and (not content or not re.search(pattern, str(content))):
                    return False
        
        # All checks passed
        return True
    
    def extract_tool_calls(self, response: Any) -> List[Dict]:
        """Extract tool calls from a model response."""
        # Handle None response
        if response is None:
            return []
        
        # Convert response to dict if needed
        response_dict = self._ensure_dict(response)
        
        # Detect the pattern
        pattern = self.detect_pattern(response_dict)
        if not pattern:
            return []
        
        # Extract using the appropriate method
        extraction = pattern.extraction
        method = extraction["method"]
        
        if method == "xpath":
            return self._extract_xpath(response_dict, extraction)
        elif method == "regex":
            return self._extract_regex(response_dict, extraction)
        elif method == "regex_json":
            return self._extract_regex_json(response_dict, extraction)
        else:
            logger.warning(f"Unknown extraction method: {method}")
            return []
    
    def _extract_xpath(self, data: Dict, config: Dict) -> List[Dict]:
        """Extract tool calls using XPath-like paths."""
        tool_calls_path = config["tool_calls_path"]
        name_path = config["function_name_path"]
        args_path = config["function_args_path"]
        
        # Get all tool calls
        tool_calls = self.xpath_extractor.get_nodes(data, tool_calls_path)
        if not tool_calls:
            return []
        
        result = []
        for tc in tool_calls:
            # Extract function name
            name = self.xpath_extractor.get_node(tc, name_path)
            if not name:
                continue
                
            # Extract arguments
            args_str = self.xpath_extractor.get_node(tc, args_path)
            
            # Parse arguments
            if isinstance(args_str, str):
                try:
                    args = json.loads(args_str)
                except:
                    args = {"raw_args": args_str}
            elif isinstance(args_str, dict):
                args = args_str
            else:
                args = {}
            
            # Get ID if available, or generate one
            tc_id = self.xpath_extractor.get_node(tc, "id") or str(uuid.uuid4())
            
            # Create tool call
            result.append({
                "name": name,
                "arguments": args,
                "id": tc_id
            })
            
            # Track for debugging/testing
            self._track_tool_call(name, args)
        
        return result
    
    def _extract_regex_json(self, data: Dict, config: Dict) -> List[Dict]:
        """Extract JSON objects from text that appear to be tool calls."""
        content_path = config["content_path"]
        pattern = config["pattern"]
        
        # Extract content
        content = self.xpath_extractor.get_node(data, content_path)
        if not content:
            return []
        
        # Find all JSON-like patterns in the content
        matches = re.findall(pattern, str(content))
        result = []
        
        for idx, match in enumerate(matches):
            try:
                # Try to parse as JSON
                json_obj = json.loads(match)
                
                # Check if it has the required fields
                if "name" in json_obj:
                    # Get arguments
                    args = json_obj.get("arguments", json_obj.get("params", json_obj.get("args", {})))
                    
                    # Create tool call
                    result.append({
                        "name": json_obj["name"],
                        "arguments": args,
                        "id": json_obj.get("id", f"extracted_id_{idx}_{uuid.uuid4()}")
                    })
                    
                    # Track for testing
                    self._track_tool_call(json_obj["name"], args)
            except:
                pass
        
        return result
    
    def _extract_regex(self, data: Dict, config: Dict) -> List[Dict]:
        """Extract tool calls using regex on content."""
        content_path = config["content_path"]
        pattern = config["pattern"]
        
        # Extract content
        content = self.xpath_extractor.get_node(data, content_path)
        if not content:
            return []
        
        # Find matches
        matches = re.findall(pattern, str(content), re.DOTALL)
        result = []
        
        for idx, match in enumerate(matches):
            try:
                # Try to parse as JSON
                tool_data = json.loads(match)
                
                if "name" in tool_data:
                    result.append({
                        "name": tool_data["name"],
                        "arguments": tool_data.get("arguments", {}),
                        "id": tool_data.get("id", f"regex_id_{idx}_{uuid.uuid4()}")
                    })
                    
                    self._track_tool_call(tool_data["name"], tool_data.get("arguments", {}))
            except:
                pass
                
        return result
    
    def format_tools_for_model(self, tools: List[Dict]) -> Any:
        """Format tools for a model."""
        # Default to OpenAI format
        formatted_tools = []
        for tool in tools:
            formatted_tool = {
                "type": "function",
                "function": {
                    "name": tool.get("name", ""),
                    "description": tool.get("description", ""),
                    "parameters": tool.get("parameters", {})
                }
            }
            formatted_tools.append(formatted_tool)
        
        return formatted_tools
    
    def format_tool_results(self, tool_name: str, result: Any, **kwargs) -> Dict:
        """Format a tool result for a model."""
        tool_call_id = kwargs.get("tool_call_id", str(uuid.uuid4()))
        
        # Format for most models (OpenAI)
        return {
            "role": "tool",
            "tool_call_id": tool_call_id,
            "content": str(result) if result is not None else ""
        }
    
    def can_handle_response(self, response: Any) -> bool:
        """Check if this handler can process the response."""
        pattern = self.detect_pattern(response)
        return pattern is not None 