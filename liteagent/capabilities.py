"""
Model capability detection using models.dev API.

This module provides dynamic model capability detection by fetching
the latest information from models.dev API.
"""

import json
import time
import requests
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from .utils import logger

@dataclass
class ModelCapabilities:
    """Model capability information."""
    model_id: str
    name: str
    provider: str
    tool_calling: bool
    reasoning: bool
    multimodal: bool
    context_limit: Optional[int] = None
    output_limit: Optional[int] = None
    supports_streaming: bool = True
    supports_parallel_tools: bool = False
    supports_image_input: bool = False
    supports_image_output: bool = False
    supports_caching: bool = False
    supports_json_mode: bool = False
    supports_system_prompt: bool = True
    pricing: Optional[Dict[str, float]] = None
    last_updated: Optional[float] = None

class CapabilityDetector:
    """Dynamic model capability detection using models.dev API."""
    
    def __init__(self, cache_ttl: int = 3600):
        """
        Initialize the capability detector.
        
        Args:
            cache_ttl: Cache time-to-live in seconds (default: 1 hour)
        """
        self.cache_ttl = cache_ttl
        self._capability_cache: Dict[str, ModelCapabilities] = {}
        self._last_fetch: Optional[float] = None
        self._all_models: Dict[str, Dict[str, Any]] = {}
        
    def get_model_capabilities(self, model_name: str) -> Optional[ModelCapabilities]:
        """
        Get capabilities for a specific model.
        
        Args:
            model_name: Name of the model to look up
            
        Returns:
            ModelCapabilities or None if not found
        """
        # Ensure we have fresh data
        self._refresh_cache_if_needed()
        
        # Try exact match first
        if model_name in self._capability_cache:
            return self._capability_cache[model_name]
            
        # Try fuzzy matching
        return self._fuzzy_match_model(model_name)
        
    def get_models_by_provider(self, provider: str) -> List[ModelCapabilities]:
        """
        Get all models for a specific provider.
        
        Args:
            provider: Provider name (e.g., 'openai', 'anthropic')
            
        Returns:
            List of ModelCapabilities for the provider
        """
        self._refresh_cache_if_needed()
        
        return [
            cap for cap in self._capability_cache.values()
            if cap.provider.lower() == provider.lower()
        ]
        
    def get_tool_calling_models(self) -> List[ModelCapabilities]:
        """Get all models that support tool calling."""
        self._refresh_cache_if_needed()
        
        return [
            cap for cap in self._capability_cache.values()
            if cap.tool_calling
        ]
        
    def _refresh_cache_if_needed(self) -> None:
        """Refresh the cache if it's stale."""
        current_time = time.time()
        
        if (self._last_fetch is None or 
            current_time - self._last_fetch > self.cache_ttl):
            try:
                self._fetch_models_data()
                self._last_fetch = current_time
                logger.info("Model capabilities cache refreshed")
            except Exception as e:
                logger.warning(f"Failed to refresh model capabilities: {e}")
                if not self._capability_cache:
                    # Fall back to static capabilities if cache is empty
                    logger.warning("Failed to fetch from models.dev API, no static fallback available")
                    
    def _fetch_models_data(self) -> None:
        """Fetch model data from models.dev API."""
        try:
            response = requests.get('http://models.dev/api.json', timeout=10)
            response.raise_for_status()
            
            data = response.json()
            self._all_models = data
            
            # Convert to our capability format
            self._build_capability_cache(data)
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch models.dev data: {e}")
            raise
            
    def _build_capability_cache(self, models_data: Dict[str, Any]) -> None:
        """Build the capability cache from models.dev data."""
        self._capability_cache = {}
        
        for provider, provider_data in models_data.items():
            if not isinstance(provider_data, dict):
                continue
                
            models = provider_data.get('models', {})
            if not isinstance(models, dict):
                continue
                
            for model_id, model_info in models.items():
                if not isinstance(model_info, dict):
                    continue
                    
                try:
                    capability = self._parse_model_info(model_id, provider, model_info)
                    if capability:
                        self._capability_cache[model_id] = capability
                        
                        # Also cache with common variations
                        self._add_model_aliases(model_id, capability)
                        
                except Exception as e:
                    logger.warning(f"Failed to parse model {model_id}: {e}")
                    continue
                    
    def _parse_model_info(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get('name', model_id)
            tool_calling = model_info.get('tool_call', False)
            reasoning = model_info.get('reasoning', False)
            
            # Check for multimodal capabilities from modalities field
            modalities = model_info.get('modalities', {})
            input_modalities = modalities.get('input', [])
            output_modalities = modalities.get('output', [])
            
            # Determine multimodal and image support from API data
            multimodal = len(input_modalities) > 1 or 'image' in input_modalities
            supports_image_input = 'image' in input_modalities
            supports_image_output = 'image' in output_modalities
            
            # Extract limits from API data
            limits = model_info.get('limit', {})
            context_limit = limits.get('context')
            output_limit = limits.get('output')
            
            # Advanced capabilities - use API data where available, conservative fallbacks otherwise
            # Parallel tools: assume supported if tool_calling is true and it's a capable model
            supports_parallel = tool_calling and any(x in model_id.lower() for x in [
                'gpt-4', 'claude-3.5', 'claude-4', 'gemini', 'llama-3.1', 'gemini-2'
            ])
            
            # Caching support - conservative approach based on known providers
            supports_caching = (
                (provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()) or
                (provider.lower() in ['openai'] and ('gpt-4' in model_id.lower() or 'gpt-4o' in model_id.lower()))
            )
            
            # JSON mode support - based on known model capabilities
            supports_json_mode = tool_calling and any(x in model_id.lower() for x in [
                'gpt-4', 'gpt-3.5-turbo', 'claude-3', 'gemini'
            ])
            
            # Extract pricing from cost field in API data
            cost_info = model_info.get('cost', {})
            pricing = None
            if cost_info:
                pricing = {
                    'input': cost_info.get('input'),
                    'output': cost_info.get('output')
                }
            
            return ModelCapabilities(
                model_id=model_id,
                name=name,
                provider=provider,
                tool_calling=tool_calling,
                reasoning=reasoning,
                multimodal=multimodal,
                context_limit=context_limit,
                output_limit=output_limit,
                supports_streaming=True,  # Most modern models support streaming
                supports_parallel_tools=supports_parallel,
                supports_image_input=supports_image_input,
                supports_image_output=supports_image_output,
                supports_caching=supports_caching,
                supports_json_mode=supports_json_mode,
                supports_system_prompt=True,  # Most models support system prompts
                pricing=pricing,
                last_updated=time.time()
            )
            
        except Exception as e:
            logger.warning(f"Error parsing model info for {model_id}: {e}")
            return None
            
    def _add_model_aliases(self, model_id: str, capability: ModelCapabilities) -> None:
        """Add common aliases for the model."""
        # Add version without provider prefix
        if '/' in model_id:
            base_name = model_id.split('/', 1)[1]
            self._capability_cache[base_name] = capability
            
        # Add provider-prefixed version if not already prefixed
        if '/' not in model_id:
            prefixed_name = f"{capability.provider}/{model_id}"
            self._capability_cache[prefixed_name] = capability
            
    def _fuzzy_match_model(self, model_name: str) -> Optional[ModelCapabilities]:
        """Attempt fuzzy matching for model names."""
        model_lower = model_name.lower()
        
        # Try partial matches
        for cached_name, capability in self._capability_cache.items():
            cached_lower = cached_name.lower()
            
            # Check if the model name is contained in the cached name
            if model_lower in cached_lower or cached_lower in model_lower:
                # Verify it's a reasonable match (not too different)
                if abs(len(model_lower) - len(cached_lower)) < 10:
                    logger.info(f"Fuzzy matched {model_name} to {cached_name}")
                    return capability
                    
        return None
        


# Global instance
_capability_detector = CapabilityDetector()

def get_model_capabilities(model_name) -> Optional[ModelCapabilities]:
    """Get capabilities for a model (convenience function)."""
    # Handle both string and tuple inputs
    if isinstance(model_name, tuple):
        provider, actual_model_name = model_name
        # Use the actual model name for capability lookup
        return _capability_detector.get_model_capabilities(actual_model_name)
    else:
        return _capability_detector.get_model_capabilities(model_name)

def get_tool_calling_models() -> List[ModelCapabilities]:
    """Get all models that support tool calling (convenience function)."""
    return _capability_detector.get_tool_calling_models()

def refresh_capabilities() -> None:
    """Force refresh of model capabilities (convenience function)."""
    _capability_detector._last_fetch = None
    _capability_detector._refresh_cache_if_needed()