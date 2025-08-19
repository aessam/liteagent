"""
Base provider interface for LiteAgent.

This module defines the abstract interface that all LLM providers must implement.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union
import time

from ..utils import logger


@dataclass
class ToolCall:
    """Represents a tool call from the model."""
    id: str
    name: str
    arguments: Dict[str, Any]


@dataclass 
class ProviderResponse:
    """Standardized response format across all providers."""
    content: Optional[str]
    tool_calls: List[ToolCall]
    usage: Optional[Dict[str, Any]]
    model: str
    provider: str
    raw_response: Any
    finish_reason: Optional[str] = None


class ProviderInterface(ABC):
    """Abstract base class for all LLM provider implementations."""
    
    def __init__(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize the provider interface.
        
        Args:
            model_name: Name of the model to use
            api_key: API key for the provider (if required)
            **kwargs: Provider-specific configuration
        """
        self.model_name = model_name
        self.api_key = api_key
        self.provider_name = self._get_provider_name()
        self.config = kwargs
        self._setup_client()
        
    @abstractmethod
    def _get_provider_name(self) -> str:
        """Return the name of the provider."""
        pass
        
    @abstractmethod 
    def _setup_client(self) -> None:
        """Setup the provider-specific client."""
        pass
        
    @abstractmethod
    def generate_response(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate a response from the model.
        
        Args:
            messages: List of message dictionaries
            tools: Optional list of tool definitions
            **kwargs: Additional provider-specific parameters
            
        Returns:
            ProviderResponse: Standardized response object
        """
        pass
        
    @abstractmethod
    def supports_tool_calling(self) -> bool:
        """Check if the model supports tool calling."""
        pass
        
    @abstractmethod
    def supports_parallel_tools(self) -> bool:
        """Check if the model supports parallel tool execution."""
        pass
        
    def get_max_tokens(self) -> Optional[int]:
        """Get the maximum token limit for this model."""
        # Default implementation - providers can override
        return None
        
    def get_context_window(self) -> Optional[int]:
        """Get the context window size for this model."""
        # Default implementation - providers can override  
        return None
        
    def _log_request(self, messages: List[Dict], tools: Optional[List[Dict]] = None) -> None:
        """Log the request details."""
        logger.info(f"[{self.provider_name}] Calling {self.model_name}")
        logger.info(f"[{self.provider_name}] Message count: {len(messages)}")
        if tools:
            tool_names = [tool.get('function', {}).get('name', 'unknown') for tool in tools]
            logger.info(f"[{self.provider_name}] Tools available: {tool_names}")
        else:
            logger.info(f"[{self.provider_name}] No tools provided")
            
    def _log_response(self, response: ProviderResponse, elapsed_time: float) -> None:
        """Log the response details and record costs."""
        logger.info(f"[{self.provider_name}] Response received in {elapsed_time:.2f}s")
        if response.tool_calls:
            logger.info(f"[{self.provider_name}] Tool calls: {[tc.name for tc in response.tool_calls]}")
        if response.usage:
            logger.info(f"[{self.provider_name}] Token usage: {response.usage}")
            
            # Record cost at provider level
            try:
                from ..provider_cost_tracker import record_provider_cost
                cost = record_provider_cost(response)
                logger.info(f"[{self.provider_name}] Cost recorded: ${cost:.6f}")
            except Exception as e:
                logger.debug(f"[{self.provider_name}] Cost tracking failed: {e}")
            
    # Removed _handle_error - all providers should fail fast without error handling