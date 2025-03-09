"""
Unit tests for the xpath_extractor module.

This module contains tests for XPath-like extraction functionality used in tool calling.
"""

import json
import pytest
from typing import Dict, Any, List

from liteagent.xpath_extractor import XPathExtractor, get_node_by_xpath, get_paths
from liteagent.tool_calling_detection import detect_tool_calling_format
from liteagent.tool_calling_types import ToolCallingType


# Test fixtures
@pytest.fixture
def openai_response():
    """Sample OpenAI response with tool calls."""
    return {
        "id": "chatcmpl-123",
        "object": "chat.completion",
        "created": 1677858242,
        "model": "gpt-3.5-turbo-0613",
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [
                        {
                            "id": "call_abc123",
                            "type": "function",
                            "function": {
                                "name": "get_weather",
                                "arguments": "{\"location\": \"San Francisco, CA\", \"unit\": \"celsius\"}"
                            }
                        }
                    ]
                },
                "finish_reason": "tool_calls",
                "index": 0
            }
        ]
    }


@pytest.fixture
def anthropic_response():
    """Sample Anthropic response with tool_use."""
    return {
        "id": "msg_1234567890",
        "type": "message",
        "role": "assistant",
        "model": "claude-3-opus-20240229",
        "content": [
            {
                "type": "text",
                "text": "I'll get the weather information for San Francisco."
            },
            {
                "type": "tool_use",
                "id": "tool_use_abc123",
                "name": "get_weather",
                "input": {
                    "location": "San Francisco, CA",
                    "unit": "celsius"
                }
            }
        ]
    }


class TestXPathExtractor:
    """Test cases for the XPathExtractor class."""
    
    def test_get_node_with_openai_response(self, openai_response):
        """Test extracting tool_calls from an OpenAI response."""
        # Using direct function
        tool_calls_direct = get_node_by_xpath(openai_response, 'choices/0/message/tool_calls')
        assert tool_calls_direct is not None
        assert len(tool_calls_direct) == 1
        assert tool_calls_direct[0]['function']['name'] == 'get_weather'
        
        # Using XPathExtractor class
        extractor = XPathExtractor()
        tool_calls_class = extractor.get_node(openai_response, 'choices/0/message/tool_calls')
        assert tool_calls_class is not None
        assert len(tool_calls_class) == 1
        assert tool_calls_class[0]['function']['name'] == 'get_weather'
        
        # Test with wildcard
        tool_calls_wildcard = extractor.get_node(openai_response, 'choices/*/message/tool_calls')
        assert tool_calls_wildcard is not None
        assert len(tool_calls_wildcard) == 1
        assert tool_calls_wildcard[0]['function']['name'] == 'get_weather'
    
    def test_get_node_with_anthropic_response(self, anthropic_response):
        """Test extracting tool_use from an Anthropic response."""
        # Using direct function
        tool_use_blocks = []
        for i, block in enumerate(anthropic_response['content']):
            if block['type'] == 'tool_use':
                tool_use_blocks.append(block)
        
        assert len(tool_use_blocks) == 1
        assert tool_use_blocks[0]['name'] == 'get_weather'
        
        # Using XPathExtractor class for specific block
        extractor = XPathExtractor()
        tool_use = extractor.get_node(anthropic_response, 'content/1')
        assert tool_use is not None
        assert tool_use['type'] == 'tool_use'
        assert tool_use['name'] == 'get_weather'
        
        # Test detecting any tool_use block (demonstrating current issue)
        # This is expected to fail with the current implementation!
        tool_use_wildcard = extractor.get_nodes(anthropic_response, 'content/type=tool_use')
        assert tool_use_wildcard[0]['name'] == 'get_weather'

        
    
    def test_tool_calling_detection_with_openai(self, openai_response):
        """Test that the detection logic correctly identifies OpenAI tool calls."""
        detected_type = detect_tool_calling_format(openai_response)
        assert detected_type == ToolCallingType.OPENAI
    
    def test_tool_calling_detection_with_anthropic(self, anthropic_response):
        """Test that the detection logic correctly identifies Anthropic tool use."""
        detected_type = detect_tool_calling_format(anthropic_response)
        assert detected_type == ToolCallingType.ANTHROPIC


# Run the tests directly if executed as a script
if __name__ == "__main__":
    pytest.main(["-xvs", __file__]) 