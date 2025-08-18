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
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result

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
    
    def xǁCapabilityDetectorǁ__init____mutmut_orig(self, cache_ttl: int = 3600):
        """
        Initialize the capability detector.
        
        Args:
            cache_ttl: Cache time-to-live in seconds (default: 1 hour)
        """
        self.cache_ttl = cache_ttl
        self._capability_cache: Dict[str, ModelCapabilities] = {}
        self._last_fetch: Optional[float] = None
        self._all_models: Dict[str, Dict[str, Any]] = {}
        
    
    def xǁCapabilityDetectorǁ__init____mutmut_1(self, cache_ttl: int = 3601):
        """
        Initialize the capability detector.
        
        Args:
            cache_ttl: Cache time-to-live in seconds (default: 1 hour)
        """
        self.cache_ttl = cache_ttl
        self._capability_cache: Dict[str, ModelCapabilities] = {}
        self._last_fetch: Optional[float] = None
        self._all_models: Dict[str, Dict[str, Any]] = {}
        
    
    def xǁCapabilityDetectorǁ__init____mutmut_2(self, cache_ttl: int = 3600):
        """
        Initialize the capability detector.
        
        Args:
            cache_ttl: Cache time-to-live in seconds (default: 1 hour)
        """
        self.cache_ttl = None
        self._capability_cache: Dict[str, ModelCapabilities] = {}
        self._last_fetch: Optional[float] = None
        self._all_models: Dict[str, Dict[str, Any]] = {}
        
    
    def xǁCapabilityDetectorǁ__init____mutmut_3(self, cache_ttl: int = 3600):
        """
        Initialize the capability detector.
        
        Args:
            cache_ttl: Cache time-to-live in seconds (default: 1 hour)
        """
        self.cache_ttl = cache_ttl
        self._capability_cache: Dict[str, ModelCapabilities] = None
        self._last_fetch: Optional[float] = None
        self._all_models: Dict[str, Dict[str, Any]] = {}
        
    
    def xǁCapabilityDetectorǁ__init____mutmut_4(self, cache_ttl: int = 3600):
        """
        Initialize the capability detector.
        
        Args:
            cache_ttl: Cache time-to-live in seconds (default: 1 hour)
        """
        self.cache_ttl = cache_ttl
        self._capability_cache: Dict[str, ModelCapabilities] = {}
        self._last_fetch: Optional[float] = ""
        self._all_models: Dict[str, Dict[str, Any]] = {}
        
    
    def xǁCapabilityDetectorǁ__init____mutmut_5(self, cache_ttl: int = 3600):
        """
        Initialize the capability detector.
        
        Args:
            cache_ttl: Cache time-to-live in seconds (default: 1 hour)
        """
        self.cache_ttl = cache_ttl
        self._capability_cache: Dict[str, ModelCapabilities] = {}
        self._last_fetch: Optional[float] = None
        self._all_models: Dict[str, Dict[str, Any]] = None
        
    
    xǁCapabilityDetectorǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁCapabilityDetectorǁ__init____mutmut_1': xǁCapabilityDetectorǁ__init____mutmut_1, 
        'xǁCapabilityDetectorǁ__init____mutmut_2': xǁCapabilityDetectorǁ__init____mutmut_2, 
        'xǁCapabilityDetectorǁ__init____mutmut_3': xǁCapabilityDetectorǁ__init____mutmut_3, 
        'xǁCapabilityDetectorǁ__init____mutmut_4': xǁCapabilityDetectorǁ__init____mutmut_4, 
        'xǁCapabilityDetectorǁ__init____mutmut_5': xǁCapabilityDetectorǁ__init____mutmut_5
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁCapabilityDetectorǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁCapabilityDetectorǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁCapabilityDetectorǁ__init____mutmut_orig)
    xǁCapabilityDetectorǁ__init____mutmut_orig.__name__ = 'xǁCapabilityDetectorǁ__init__'
    def xǁCapabilityDetectorǁget_model_capabilities__mutmut_orig(self, model_name: str) -> Optional[ModelCapabilities]:
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
        
    def xǁCapabilityDetectorǁget_model_capabilities__mutmut_1(self, model_name: str) -> Optional[ModelCapabilities]:
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
        if model_name not in self._capability_cache:
            return self._capability_cache[model_name]
            
        # Try fuzzy matching
        return self._fuzzy_match_model(model_name)
        
    def xǁCapabilityDetectorǁget_model_capabilities__mutmut_2(self, model_name: str) -> Optional[ModelCapabilities]:
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
        return self._fuzzy_match_model(None)
        
    
    xǁCapabilityDetectorǁget_model_capabilities__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁCapabilityDetectorǁget_model_capabilities__mutmut_1': xǁCapabilityDetectorǁget_model_capabilities__mutmut_1, 
        'xǁCapabilityDetectorǁget_model_capabilities__mutmut_2': xǁCapabilityDetectorǁget_model_capabilities__mutmut_2
    }
    
    def get_model_capabilities(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁCapabilityDetectorǁget_model_capabilities__mutmut_orig"), object.__getattribute__(self, "xǁCapabilityDetectorǁget_model_capabilities__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_model_capabilities.__signature__ = _mutmut_signature(xǁCapabilityDetectorǁget_model_capabilities__mutmut_orig)
    xǁCapabilityDetectorǁget_model_capabilities__mutmut_orig.__name__ = 'xǁCapabilityDetectorǁget_model_capabilities'
    def xǁCapabilityDetectorǁget_models_by_provider__mutmut_orig(self, provider: str) -> List[ModelCapabilities]:
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
        
    def xǁCapabilityDetectorǁget_models_by_provider__mutmut_1(self, provider: str) -> List[ModelCapabilities]:
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
            if cap.provider.upper() == provider.lower()
        ]
        
    def xǁCapabilityDetectorǁget_models_by_provider__mutmut_2(self, provider: str) -> List[ModelCapabilities]:
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
            if cap.provider.lower() != provider.lower()
        ]
        
    def xǁCapabilityDetectorǁget_models_by_provider__mutmut_3(self, provider: str) -> List[ModelCapabilities]:
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
            if cap.provider.lower() == provider.upper()
        ]
        
    
    xǁCapabilityDetectorǁget_models_by_provider__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁCapabilityDetectorǁget_models_by_provider__mutmut_1': xǁCapabilityDetectorǁget_models_by_provider__mutmut_1, 
        'xǁCapabilityDetectorǁget_models_by_provider__mutmut_2': xǁCapabilityDetectorǁget_models_by_provider__mutmut_2, 
        'xǁCapabilityDetectorǁget_models_by_provider__mutmut_3': xǁCapabilityDetectorǁget_models_by_provider__mutmut_3
    }
    
    def get_models_by_provider(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁCapabilityDetectorǁget_models_by_provider__mutmut_orig"), object.__getattribute__(self, "xǁCapabilityDetectorǁget_models_by_provider__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_models_by_provider.__signature__ = _mutmut_signature(xǁCapabilityDetectorǁget_models_by_provider__mutmut_orig)
    xǁCapabilityDetectorǁget_models_by_provider__mutmut_orig.__name__ = 'xǁCapabilityDetectorǁget_models_by_provider'
    def get_tool_calling_models(self) -> List[ModelCapabilities]:
        """Get all models that support tool calling."""
        self._refresh_cache_if_needed()
        
        return [
            cap for cap in self._capability_cache.values()
            if cap.tool_calling
        ]
        
    def xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_orig(self) -> None:
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
                    
    def xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_1(self) -> None:
        """Refresh the cache if it's stale."""
        current_time = None
        
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
                    
    def xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_2(self) -> None:
        """Refresh the cache if it's stale."""
        current_time = time.time()
        
        if (self._last_fetch is None and current_time - self._last_fetch > self.cache_ttl):
            try:
                self._fetch_models_data()
                self._last_fetch = current_time
                logger.info("Model capabilities cache refreshed")
            except Exception as e:
                logger.warning(f"Failed to refresh model capabilities: {e}")
                if not self._capability_cache:
                    # Fall back to static capabilities if cache is empty
                    logger.warning("Failed to fetch from models.dev API, no static fallback available")
                    
    def xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_3(self) -> None:
        """Refresh the cache if it's stale."""
        current_time = time.time()
        
        if (self._last_fetch is not None or 
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
                    
    def xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_4(self) -> None:
        """Refresh the cache if it's stale."""
        current_time = time.time()
        
        if (self._last_fetch is None or 
            current_time + self._last_fetch > self.cache_ttl):
            try:
                self._fetch_models_data()
                self._last_fetch = current_time
                logger.info("Model capabilities cache refreshed")
            except Exception as e:
                logger.warning(f"Failed to refresh model capabilities: {e}")
                if not self._capability_cache:
                    # Fall back to static capabilities if cache is empty
                    logger.warning("Failed to fetch from models.dev API, no static fallback available")
                    
    def xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_5(self) -> None:
        """Refresh the cache if it's stale."""
        current_time = time.time()
        
        if (self._last_fetch is None or 
            current_time - self._last_fetch >= self.cache_ttl):
            try:
                self._fetch_models_data()
                self._last_fetch = current_time
                logger.info("Model capabilities cache refreshed")
            except Exception as e:
                logger.warning(f"Failed to refresh model capabilities: {e}")
                if not self._capability_cache:
                    # Fall back to static capabilities if cache is empty
                    logger.warning("Failed to fetch from models.dev API, no static fallback available")
                    
    def xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_6(self) -> None:
        """Refresh the cache if it's stale."""
        current_time = time.time()
        
        if (self._last_fetch is None or 
            current_time - self._last_fetch > self.cache_ttl):
            try:
                self._fetch_models_data()
                self._last_fetch = None
                logger.info("Model capabilities cache refreshed")
            except Exception as e:
                logger.warning(f"Failed to refresh model capabilities: {e}")
                if not self._capability_cache:
                    # Fall back to static capabilities if cache is empty
                    logger.warning("Failed to fetch from models.dev API, no static fallback available")
                    
    def xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_7(self) -> None:
        """Refresh the cache if it's stale."""
        current_time = time.time()
        
        if (self._last_fetch is None or 
            current_time - self._last_fetch > self.cache_ttl):
            try:
                self._fetch_models_data()
                self._last_fetch = current_time
                logger.info(None)
            except Exception as e:
                logger.warning(f"Failed to refresh model capabilities: {e}")
                if not self._capability_cache:
                    # Fall back to static capabilities if cache is empty
                    logger.warning("Failed to fetch from models.dev API, no static fallback available")
                    
    def xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_8(self) -> None:
        """Refresh the cache if it's stale."""
        current_time = time.time()
        
        if (self._last_fetch is None or 
            current_time - self._last_fetch > self.cache_ttl):
            try:
                self._fetch_models_data()
                self._last_fetch = current_time
                logger.info("XXModel capabilities cache refreshedXX")
            except Exception as e:
                logger.warning(f"Failed to refresh model capabilities: {e}")
                if not self._capability_cache:
                    # Fall back to static capabilities if cache is empty
                    logger.warning("Failed to fetch from models.dev API, no static fallback available")
                    
    def xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_9(self) -> None:
        """Refresh the cache if it's stale."""
        current_time = time.time()
        
        if (self._last_fetch is None or 
            current_time - self._last_fetch > self.cache_ttl):
            try:
                self._fetch_models_data()
                self._last_fetch = current_time
                logger.info("model capabilities cache refreshed")
            except Exception as e:
                logger.warning(f"Failed to refresh model capabilities: {e}")
                if not self._capability_cache:
                    # Fall back to static capabilities if cache is empty
                    logger.warning("Failed to fetch from models.dev API, no static fallback available")
                    
    def xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_10(self) -> None:
        """Refresh the cache if it's stale."""
        current_time = time.time()
        
        if (self._last_fetch is None or 
            current_time - self._last_fetch > self.cache_ttl):
            try:
                self._fetch_models_data()
                self._last_fetch = current_time
                logger.info("MODEL CAPABILITIES CACHE REFRESHED")
            except Exception as e:
                logger.warning(f"Failed to refresh model capabilities: {e}")
                if not self._capability_cache:
                    # Fall back to static capabilities if cache is empty
                    logger.warning("Failed to fetch from models.dev API, no static fallback available")
                    
    def xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_11(self) -> None:
        """Refresh the cache if it's stale."""
        current_time = time.time()
        
        if (self._last_fetch is None or 
            current_time - self._last_fetch > self.cache_ttl):
            try:
                self._fetch_models_data()
                self._last_fetch = current_time
                logger.info("Model capabilities cache refreshed")
            except Exception as e:
                logger.warning(None)
                if not self._capability_cache:
                    # Fall back to static capabilities if cache is empty
                    logger.warning("Failed to fetch from models.dev API, no static fallback available")
                    
    def xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_12(self) -> None:
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
                if self._capability_cache:
                    # Fall back to static capabilities if cache is empty
                    logger.warning("Failed to fetch from models.dev API, no static fallback available")
                    
    def xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_13(self) -> None:
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
                    logger.warning(None)
                    
    def xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_14(self) -> None:
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
                    logger.warning("XXFailed to fetch from models.dev API, no static fallback availableXX")
                    
    def xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_15(self) -> None:
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
                    logger.warning("failed to fetch from models.dev api, no static fallback available")
                    
    def xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_16(self) -> None:
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
                    logger.warning("FAILED TO FETCH FROM MODELS.DEV API, NO STATIC FALLBACK AVAILABLE")
                    
    
    xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_1': xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_1, 
        'xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_2': xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_2, 
        'xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_3': xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_3, 
        'xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_4': xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_4, 
        'xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_5': xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_5, 
        'xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_6': xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_6, 
        'xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_7': xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_7, 
        'xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_8': xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_8, 
        'xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_9': xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_9, 
        'xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_10': xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_10, 
        'xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_11': xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_11, 
        'xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_12': xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_12, 
        'xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_13': xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_13, 
        'xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_14': xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_14, 
        'xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_15': xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_15, 
        'xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_16': xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_16
    }
    
    def _refresh_cache_if_needed(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_orig"), object.__getattribute__(self, "xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _refresh_cache_if_needed.__signature__ = _mutmut_signature(xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_orig)
    xǁCapabilityDetectorǁ_refresh_cache_if_needed__mutmut_orig.__name__ = 'xǁCapabilityDetectorǁ_refresh_cache_if_needed'
    def xǁCapabilityDetectorǁ_fetch_models_data__mutmut_orig(self) -> None:
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
            
    def xǁCapabilityDetectorǁ_fetch_models_data__mutmut_1(self) -> None:
        """Fetch model data from models.dev API."""
        try:
            response = None
            response.raise_for_status()
            
            data = response.json()
            self._all_models = data
            
            # Convert to our capability format
            self._build_capability_cache(data)
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch models.dev data: {e}")
            raise
            
    def xǁCapabilityDetectorǁ_fetch_models_data__mutmut_2(self) -> None:
        """Fetch model data from models.dev API."""
        try:
            response = requests.get(None, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            self._all_models = data
            
            # Convert to our capability format
            self._build_capability_cache(data)
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch models.dev data: {e}")
            raise
            
    def xǁCapabilityDetectorǁ_fetch_models_data__mutmut_3(self) -> None:
        """Fetch model data from models.dev API."""
        try:
            response = requests.get('http://models.dev/api.json', timeout=None)
            response.raise_for_status()
            
            data = response.json()
            self._all_models = data
            
            # Convert to our capability format
            self._build_capability_cache(data)
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch models.dev data: {e}")
            raise
            
    def xǁCapabilityDetectorǁ_fetch_models_data__mutmut_4(self) -> None:
        """Fetch model data from models.dev API."""
        try:
            response = requests.get(timeout=10)
            response.raise_for_status()
            
            data = response.json()
            self._all_models = data
            
            # Convert to our capability format
            self._build_capability_cache(data)
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch models.dev data: {e}")
            raise
            
    def xǁCapabilityDetectorǁ_fetch_models_data__mutmut_5(self) -> None:
        """Fetch model data from models.dev API."""
        try:
            response = requests.get('http://models.dev/api.json', )
            response.raise_for_status()
            
            data = response.json()
            self._all_models = data
            
            # Convert to our capability format
            self._build_capability_cache(data)
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch models.dev data: {e}")
            raise
            
    def xǁCapabilityDetectorǁ_fetch_models_data__mutmut_6(self) -> None:
        """Fetch model data from models.dev API."""
        try:
            response = requests.get('XXhttp://models.dev/api.jsonXX', timeout=10)
            response.raise_for_status()
            
            data = response.json()
            self._all_models = data
            
            # Convert to our capability format
            self._build_capability_cache(data)
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch models.dev data: {e}")
            raise
            
    def xǁCapabilityDetectorǁ_fetch_models_data__mutmut_7(self) -> None:
        """Fetch model data from models.dev API."""
        try:
            response = requests.get('HTTP://MODELS.DEV/API.JSON', timeout=10)
            response.raise_for_status()
            
            data = response.json()
            self._all_models = data
            
            # Convert to our capability format
            self._build_capability_cache(data)
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch models.dev data: {e}")
            raise
            
    def xǁCapabilityDetectorǁ_fetch_models_data__mutmut_8(self) -> None:
        """Fetch model data from models.dev API."""
        try:
            response = requests.get('http://models.dev/api.json', timeout=11)
            response.raise_for_status()
            
            data = response.json()
            self._all_models = data
            
            # Convert to our capability format
            self._build_capability_cache(data)
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch models.dev data: {e}")
            raise
            
    def xǁCapabilityDetectorǁ_fetch_models_data__mutmut_9(self) -> None:
        """Fetch model data from models.dev API."""
        try:
            response = requests.get('http://models.dev/api.json', timeout=10)
            response.raise_for_status()
            
            data = None
            self._all_models = data
            
            # Convert to our capability format
            self._build_capability_cache(data)
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch models.dev data: {e}")
            raise
            
    def xǁCapabilityDetectorǁ_fetch_models_data__mutmut_10(self) -> None:
        """Fetch model data from models.dev API."""
        try:
            response = requests.get('http://models.dev/api.json', timeout=10)
            response.raise_for_status()
            
            data = response.json()
            self._all_models = None
            
            # Convert to our capability format
            self._build_capability_cache(data)
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch models.dev data: {e}")
            raise
            
    def xǁCapabilityDetectorǁ_fetch_models_data__mutmut_11(self) -> None:
        """Fetch model data from models.dev API."""
        try:
            response = requests.get('http://models.dev/api.json', timeout=10)
            response.raise_for_status()
            
            data = response.json()
            self._all_models = data
            
            # Convert to our capability format
            self._build_capability_cache(None)
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch models.dev data: {e}")
            raise
            
    def xǁCapabilityDetectorǁ_fetch_models_data__mutmut_12(self) -> None:
        """Fetch model data from models.dev API."""
        try:
            response = requests.get('http://models.dev/api.json', timeout=10)
            response.raise_for_status()
            
            data = response.json()
            self._all_models = data
            
            # Convert to our capability format
            self._build_capability_cache(data)
            
        except requests.RequestException as e:
            logger.error(None)
            raise
            
    
    xǁCapabilityDetectorǁ_fetch_models_data__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁCapabilityDetectorǁ_fetch_models_data__mutmut_1': xǁCapabilityDetectorǁ_fetch_models_data__mutmut_1, 
        'xǁCapabilityDetectorǁ_fetch_models_data__mutmut_2': xǁCapabilityDetectorǁ_fetch_models_data__mutmut_2, 
        'xǁCapabilityDetectorǁ_fetch_models_data__mutmut_3': xǁCapabilityDetectorǁ_fetch_models_data__mutmut_3, 
        'xǁCapabilityDetectorǁ_fetch_models_data__mutmut_4': xǁCapabilityDetectorǁ_fetch_models_data__mutmut_4, 
        'xǁCapabilityDetectorǁ_fetch_models_data__mutmut_5': xǁCapabilityDetectorǁ_fetch_models_data__mutmut_5, 
        'xǁCapabilityDetectorǁ_fetch_models_data__mutmut_6': xǁCapabilityDetectorǁ_fetch_models_data__mutmut_6, 
        'xǁCapabilityDetectorǁ_fetch_models_data__mutmut_7': xǁCapabilityDetectorǁ_fetch_models_data__mutmut_7, 
        'xǁCapabilityDetectorǁ_fetch_models_data__mutmut_8': xǁCapabilityDetectorǁ_fetch_models_data__mutmut_8, 
        'xǁCapabilityDetectorǁ_fetch_models_data__mutmut_9': xǁCapabilityDetectorǁ_fetch_models_data__mutmut_9, 
        'xǁCapabilityDetectorǁ_fetch_models_data__mutmut_10': xǁCapabilityDetectorǁ_fetch_models_data__mutmut_10, 
        'xǁCapabilityDetectorǁ_fetch_models_data__mutmut_11': xǁCapabilityDetectorǁ_fetch_models_data__mutmut_11, 
        'xǁCapabilityDetectorǁ_fetch_models_data__mutmut_12': xǁCapabilityDetectorǁ_fetch_models_data__mutmut_12
    }
    
    def _fetch_models_data(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁCapabilityDetectorǁ_fetch_models_data__mutmut_orig"), object.__getattribute__(self, "xǁCapabilityDetectorǁ_fetch_models_data__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _fetch_models_data.__signature__ = _mutmut_signature(xǁCapabilityDetectorǁ_fetch_models_data__mutmut_orig)
    xǁCapabilityDetectorǁ_fetch_models_data__mutmut_orig.__name__ = 'xǁCapabilityDetectorǁ_fetch_models_data'
    def xǁCapabilityDetectorǁ_build_capability_cache__mutmut_orig(self, models_data: Dict[str, Any]) -> None:
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
                    
    def xǁCapabilityDetectorǁ_build_capability_cache__mutmut_1(self, models_data: Dict[str, Any]) -> None:
        """Build the capability cache from models.dev data."""
        self._capability_cache = None
        
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
                    
    def xǁCapabilityDetectorǁ_build_capability_cache__mutmut_2(self, models_data: Dict[str, Any]) -> None:
        """Build the capability cache from models.dev data."""
        self._capability_cache = {}
        
        for provider, provider_data in models_data.items():
            if isinstance(provider_data, dict):
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
                    
    def xǁCapabilityDetectorǁ_build_capability_cache__mutmut_3(self, models_data: Dict[str, Any]) -> None:
        """Build the capability cache from models.dev data."""
        self._capability_cache = {}
        
        for provider, provider_data in models_data.items():
            if not isinstance(provider_data, dict):
                break
                
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
                    
    def xǁCapabilityDetectorǁ_build_capability_cache__mutmut_4(self, models_data: Dict[str, Any]) -> None:
        """Build the capability cache from models.dev data."""
        self._capability_cache = {}
        
        for provider, provider_data in models_data.items():
            if not isinstance(provider_data, dict):
                continue
                
            models = None
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
                    
    def xǁCapabilityDetectorǁ_build_capability_cache__mutmut_5(self, models_data: Dict[str, Any]) -> None:
        """Build the capability cache from models.dev data."""
        self._capability_cache = {}
        
        for provider, provider_data in models_data.items():
            if not isinstance(provider_data, dict):
                continue
                
            models = provider_data.get(None, {})
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
                    
    def xǁCapabilityDetectorǁ_build_capability_cache__mutmut_6(self, models_data: Dict[str, Any]) -> None:
        """Build the capability cache from models.dev data."""
        self._capability_cache = {}
        
        for provider, provider_data in models_data.items():
            if not isinstance(provider_data, dict):
                continue
                
            models = provider_data.get('models', None)
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
                    
    def xǁCapabilityDetectorǁ_build_capability_cache__mutmut_7(self, models_data: Dict[str, Any]) -> None:
        """Build the capability cache from models.dev data."""
        self._capability_cache = {}
        
        for provider, provider_data in models_data.items():
            if not isinstance(provider_data, dict):
                continue
                
            models = provider_data.get({})
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
                    
    def xǁCapabilityDetectorǁ_build_capability_cache__mutmut_8(self, models_data: Dict[str, Any]) -> None:
        """Build the capability cache from models.dev data."""
        self._capability_cache = {}
        
        for provider, provider_data in models_data.items():
            if not isinstance(provider_data, dict):
                continue
                
            models = provider_data.get('models', )
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
                    
    def xǁCapabilityDetectorǁ_build_capability_cache__mutmut_9(self, models_data: Dict[str, Any]) -> None:
        """Build the capability cache from models.dev data."""
        self._capability_cache = {}
        
        for provider, provider_data in models_data.items():
            if not isinstance(provider_data, dict):
                continue
                
            models = provider_data.get('XXmodelsXX', {})
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
                    
    def xǁCapabilityDetectorǁ_build_capability_cache__mutmut_10(self, models_data: Dict[str, Any]) -> None:
        """Build the capability cache from models.dev data."""
        self._capability_cache = {}
        
        for provider, provider_data in models_data.items():
            if not isinstance(provider_data, dict):
                continue
                
            models = provider_data.get('MODELS', {})
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
                    
    def xǁCapabilityDetectorǁ_build_capability_cache__mutmut_11(self, models_data: Dict[str, Any]) -> None:
        """Build the capability cache from models.dev data."""
        self._capability_cache = {}
        
        for provider, provider_data in models_data.items():
            if not isinstance(provider_data, dict):
                continue
                
            models = provider_data.get('models', {})
            if isinstance(models, dict):
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
                    
    def xǁCapabilityDetectorǁ_build_capability_cache__mutmut_12(self, models_data: Dict[str, Any]) -> None:
        """Build the capability cache from models.dev data."""
        self._capability_cache = {}
        
        for provider, provider_data in models_data.items():
            if not isinstance(provider_data, dict):
                continue
                
            models = provider_data.get('models', {})
            if not isinstance(models, dict):
                break
                
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
                    
    def xǁCapabilityDetectorǁ_build_capability_cache__mutmut_13(self, models_data: Dict[str, Any]) -> None:
        """Build the capability cache from models.dev data."""
        self._capability_cache = {}
        
        for provider, provider_data in models_data.items():
            if not isinstance(provider_data, dict):
                continue
                
            models = provider_data.get('models', {})
            if not isinstance(models, dict):
                continue
                
            for model_id, model_info in models.items():
                if isinstance(model_info, dict):
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
                    
    def xǁCapabilityDetectorǁ_build_capability_cache__mutmut_14(self, models_data: Dict[str, Any]) -> None:
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
                    break
                    
                try:
                    capability = self._parse_model_info(model_id, provider, model_info)
                    if capability:
                        self._capability_cache[model_id] = capability
                        
                        # Also cache with common variations
                        self._add_model_aliases(model_id, capability)
                        
                except Exception as e:
                    logger.warning(f"Failed to parse model {model_id}: {e}")
                    continue
                    
    def xǁCapabilityDetectorǁ_build_capability_cache__mutmut_15(self, models_data: Dict[str, Any]) -> None:
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
                    capability = None
                    if capability:
                        self._capability_cache[model_id] = capability
                        
                        # Also cache with common variations
                        self._add_model_aliases(model_id, capability)
                        
                except Exception as e:
                    logger.warning(f"Failed to parse model {model_id}: {e}")
                    continue
                    
    def xǁCapabilityDetectorǁ_build_capability_cache__mutmut_16(self, models_data: Dict[str, Any]) -> None:
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
                    capability = self._parse_model_info(None, provider, model_info)
                    if capability:
                        self._capability_cache[model_id] = capability
                        
                        # Also cache with common variations
                        self._add_model_aliases(model_id, capability)
                        
                except Exception as e:
                    logger.warning(f"Failed to parse model {model_id}: {e}")
                    continue
                    
    def xǁCapabilityDetectorǁ_build_capability_cache__mutmut_17(self, models_data: Dict[str, Any]) -> None:
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
                    capability = self._parse_model_info(model_id, None, model_info)
                    if capability:
                        self._capability_cache[model_id] = capability
                        
                        # Also cache with common variations
                        self._add_model_aliases(model_id, capability)
                        
                except Exception as e:
                    logger.warning(f"Failed to parse model {model_id}: {e}")
                    continue
                    
    def xǁCapabilityDetectorǁ_build_capability_cache__mutmut_18(self, models_data: Dict[str, Any]) -> None:
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
                    capability = self._parse_model_info(model_id, provider, None)
                    if capability:
                        self._capability_cache[model_id] = capability
                        
                        # Also cache with common variations
                        self._add_model_aliases(model_id, capability)
                        
                except Exception as e:
                    logger.warning(f"Failed to parse model {model_id}: {e}")
                    continue
                    
    def xǁCapabilityDetectorǁ_build_capability_cache__mutmut_19(self, models_data: Dict[str, Any]) -> None:
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
                    capability = self._parse_model_info(provider, model_info)
                    if capability:
                        self._capability_cache[model_id] = capability
                        
                        # Also cache with common variations
                        self._add_model_aliases(model_id, capability)
                        
                except Exception as e:
                    logger.warning(f"Failed to parse model {model_id}: {e}")
                    continue
                    
    def xǁCapabilityDetectorǁ_build_capability_cache__mutmut_20(self, models_data: Dict[str, Any]) -> None:
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
                    capability = self._parse_model_info(model_id, model_info)
                    if capability:
                        self._capability_cache[model_id] = capability
                        
                        # Also cache with common variations
                        self._add_model_aliases(model_id, capability)
                        
                except Exception as e:
                    logger.warning(f"Failed to parse model {model_id}: {e}")
                    continue
                    
    def xǁCapabilityDetectorǁ_build_capability_cache__mutmut_21(self, models_data: Dict[str, Any]) -> None:
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
                    capability = self._parse_model_info(model_id, provider, )
                    if capability:
                        self._capability_cache[model_id] = capability
                        
                        # Also cache with common variations
                        self._add_model_aliases(model_id, capability)
                        
                except Exception as e:
                    logger.warning(f"Failed to parse model {model_id}: {e}")
                    continue
                    
    def xǁCapabilityDetectorǁ_build_capability_cache__mutmut_22(self, models_data: Dict[str, Any]) -> None:
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
                        self._capability_cache[model_id] = None
                        
                        # Also cache with common variations
                        self._add_model_aliases(model_id, capability)
                        
                except Exception as e:
                    logger.warning(f"Failed to parse model {model_id}: {e}")
                    continue
                    
    def xǁCapabilityDetectorǁ_build_capability_cache__mutmut_23(self, models_data: Dict[str, Any]) -> None:
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
                        self._add_model_aliases(None, capability)
                        
                except Exception as e:
                    logger.warning(f"Failed to parse model {model_id}: {e}")
                    continue
                    
    def xǁCapabilityDetectorǁ_build_capability_cache__mutmut_24(self, models_data: Dict[str, Any]) -> None:
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
                        self._add_model_aliases(model_id, None)
                        
                except Exception as e:
                    logger.warning(f"Failed to parse model {model_id}: {e}")
                    continue
                    
    def xǁCapabilityDetectorǁ_build_capability_cache__mutmut_25(self, models_data: Dict[str, Any]) -> None:
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
                        self._add_model_aliases(capability)
                        
                except Exception as e:
                    logger.warning(f"Failed to parse model {model_id}: {e}")
                    continue
                    
    def xǁCapabilityDetectorǁ_build_capability_cache__mutmut_26(self, models_data: Dict[str, Any]) -> None:
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
                        self._add_model_aliases(model_id, )
                        
                except Exception as e:
                    logger.warning(f"Failed to parse model {model_id}: {e}")
                    continue
                    
    def xǁCapabilityDetectorǁ_build_capability_cache__mutmut_27(self, models_data: Dict[str, Any]) -> None:
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
                    logger.warning(None)
                    continue
                    
    def xǁCapabilityDetectorǁ_build_capability_cache__mutmut_28(self, models_data: Dict[str, Any]) -> None:
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
                    break
                    
    
    xǁCapabilityDetectorǁ_build_capability_cache__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁCapabilityDetectorǁ_build_capability_cache__mutmut_1': xǁCapabilityDetectorǁ_build_capability_cache__mutmut_1, 
        'xǁCapabilityDetectorǁ_build_capability_cache__mutmut_2': xǁCapabilityDetectorǁ_build_capability_cache__mutmut_2, 
        'xǁCapabilityDetectorǁ_build_capability_cache__mutmut_3': xǁCapabilityDetectorǁ_build_capability_cache__mutmut_3, 
        'xǁCapabilityDetectorǁ_build_capability_cache__mutmut_4': xǁCapabilityDetectorǁ_build_capability_cache__mutmut_4, 
        'xǁCapabilityDetectorǁ_build_capability_cache__mutmut_5': xǁCapabilityDetectorǁ_build_capability_cache__mutmut_5, 
        'xǁCapabilityDetectorǁ_build_capability_cache__mutmut_6': xǁCapabilityDetectorǁ_build_capability_cache__mutmut_6, 
        'xǁCapabilityDetectorǁ_build_capability_cache__mutmut_7': xǁCapabilityDetectorǁ_build_capability_cache__mutmut_7, 
        'xǁCapabilityDetectorǁ_build_capability_cache__mutmut_8': xǁCapabilityDetectorǁ_build_capability_cache__mutmut_8, 
        'xǁCapabilityDetectorǁ_build_capability_cache__mutmut_9': xǁCapabilityDetectorǁ_build_capability_cache__mutmut_9, 
        'xǁCapabilityDetectorǁ_build_capability_cache__mutmut_10': xǁCapabilityDetectorǁ_build_capability_cache__mutmut_10, 
        'xǁCapabilityDetectorǁ_build_capability_cache__mutmut_11': xǁCapabilityDetectorǁ_build_capability_cache__mutmut_11, 
        'xǁCapabilityDetectorǁ_build_capability_cache__mutmut_12': xǁCapabilityDetectorǁ_build_capability_cache__mutmut_12, 
        'xǁCapabilityDetectorǁ_build_capability_cache__mutmut_13': xǁCapabilityDetectorǁ_build_capability_cache__mutmut_13, 
        'xǁCapabilityDetectorǁ_build_capability_cache__mutmut_14': xǁCapabilityDetectorǁ_build_capability_cache__mutmut_14, 
        'xǁCapabilityDetectorǁ_build_capability_cache__mutmut_15': xǁCapabilityDetectorǁ_build_capability_cache__mutmut_15, 
        'xǁCapabilityDetectorǁ_build_capability_cache__mutmut_16': xǁCapabilityDetectorǁ_build_capability_cache__mutmut_16, 
        'xǁCapabilityDetectorǁ_build_capability_cache__mutmut_17': xǁCapabilityDetectorǁ_build_capability_cache__mutmut_17, 
        'xǁCapabilityDetectorǁ_build_capability_cache__mutmut_18': xǁCapabilityDetectorǁ_build_capability_cache__mutmut_18, 
        'xǁCapabilityDetectorǁ_build_capability_cache__mutmut_19': xǁCapabilityDetectorǁ_build_capability_cache__mutmut_19, 
        'xǁCapabilityDetectorǁ_build_capability_cache__mutmut_20': xǁCapabilityDetectorǁ_build_capability_cache__mutmut_20, 
        'xǁCapabilityDetectorǁ_build_capability_cache__mutmut_21': xǁCapabilityDetectorǁ_build_capability_cache__mutmut_21, 
        'xǁCapabilityDetectorǁ_build_capability_cache__mutmut_22': xǁCapabilityDetectorǁ_build_capability_cache__mutmut_22, 
        'xǁCapabilityDetectorǁ_build_capability_cache__mutmut_23': xǁCapabilityDetectorǁ_build_capability_cache__mutmut_23, 
        'xǁCapabilityDetectorǁ_build_capability_cache__mutmut_24': xǁCapabilityDetectorǁ_build_capability_cache__mutmut_24, 
        'xǁCapabilityDetectorǁ_build_capability_cache__mutmut_25': xǁCapabilityDetectorǁ_build_capability_cache__mutmut_25, 
        'xǁCapabilityDetectorǁ_build_capability_cache__mutmut_26': xǁCapabilityDetectorǁ_build_capability_cache__mutmut_26, 
        'xǁCapabilityDetectorǁ_build_capability_cache__mutmut_27': xǁCapabilityDetectorǁ_build_capability_cache__mutmut_27, 
        'xǁCapabilityDetectorǁ_build_capability_cache__mutmut_28': xǁCapabilityDetectorǁ_build_capability_cache__mutmut_28
    }
    
    def _build_capability_cache(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁCapabilityDetectorǁ_build_capability_cache__mutmut_orig"), object.__getattribute__(self, "xǁCapabilityDetectorǁ_build_capability_cache__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _build_capability_cache.__signature__ = _mutmut_signature(xǁCapabilityDetectorǁ_build_capability_cache__mutmut_orig)
    xǁCapabilityDetectorǁ_build_capability_cache__mutmut_orig.__name__ = 'xǁCapabilityDetectorǁ_build_capability_cache'
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_orig(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_1(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = None
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_2(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get(None, model_id)
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_3(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get('name', None)
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_4(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get(model_id)
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_5(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get('name', )
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_6(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get('XXnameXX', model_id)
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_7(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get('NAME', model_id)
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_8(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get('name', model_id)
            tool_calling = None
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_9(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get('name', model_id)
            tool_calling = model_info.get(None, False)
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_10(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get('name', model_id)
            tool_calling = model_info.get('tool_call', None)
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_11(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get('name', model_id)
            tool_calling = model_info.get(False)
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_12(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get('name', model_id)
            tool_calling = model_info.get('tool_call', )
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_13(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get('name', model_id)
            tool_calling = model_info.get('XXtool_callXX', False)
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_14(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get('name', model_id)
            tool_calling = model_info.get('TOOL_CALL', False)
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_15(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get('name', model_id)
            tool_calling = model_info.get('tool_call', True)
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_16(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get('name', model_id)
            tool_calling = model_info.get('tool_call', False)
            reasoning = None
            
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_17(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get('name', model_id)
            tool_calling = model_info.get('tool_call', False)
            reasoning = model_info.get(None, False)
            
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_18(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get('name', model_id)
            tool_calling = model_info.get('tool_call', False)
            reasoning = model_info.get('reasoning', None)
            
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_19(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get('name', model_id)
            tool_calling = model_info.get('tool_call', False)
            reasoning = model_info.get(False)
            
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_20(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get('name', model_id)
            tool_calling = model_info.get('tool_call', False)
            reasoning = model_info.get('reasoning', )
            
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_21(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get('name', model_id)
            tool_calling = model_info.get('tool_call', False)
            reasoning = model_info.get('XXreasoningXX', False)
            
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_22(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get('name', model_id)
            tool_calling = model_info.get('tool_call', False)
            reasoning = model_info.get('REASONING', False)
            
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_23(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get('name', model_id)
            tool_calling = model_info.get('tool_call', False)
            reasoning = model_info.get('reasoning', True)
            
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_24(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get('name', model_id)
            tool_calling = model_info.get('tool_call', False)
            reasoning = model_info.get('reasoning', False)
            
            # Check for multimodal capabilities from modalities field
            modalities = None
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_25(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get('name', model_id)
            tool_calling = model_info.get('tool_call', False)
            reasoning = model_info.get('reasoning', False)
            
            # Check for multimodal capabilities from modalities field
            modalities = model_info.get(None, {})
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_26(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get('name', model_id)
            tool_calling = model_info.get('tool_call', False)
            reasoning = model_info.get('reasoning', False)
            
            # Check for multimodal capabilities from modalities field
            modalities = model_info.get('modalities', None)
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_27(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get('name', model_id)
            tool_calling = model_info.get('tool_call', False)
            reasoning = model_info.get('reasoning', False)
            
            # Check for multimodal capabilities from modalities field
            modalities = model_info.get({})
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_28(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get('name', model_id)
            tool_calling = model_info.get('tool_call', False)
            reasoning = model_info.get('reasoning', False)
            
            # Check for multimodal capabilities from modalities field
            modalities = model_info.get('modalities', )
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_29(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get('name', model_id)
            tool_calling = model_info.get('tool_call', False)
            reasoning = model_info.get('reasoning', False)
            
            # Check for multimodal capabilities from modalities field
            modalities = model_info.get('XXmodalitiesXX', {})
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_30(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get('name', model_id)
            tool_calling = model_info.get('tool_call', False)
            reasoning = model_info.get('reasoning', False)
            
            # Check for multimodal capabilities from modalities field
            modalities = model_info.get('MODALITIES', {})
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_31(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get('name', model_id)
            tool_calling = model_info.get('tool_call', False)
            reasoning = model_info.get('reasoning', False)
            
            # Check for multimodal capabilities from modalities field
            modalities = model_info.get('modalities', {})
            input_modalities = None
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_32(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get('name', model_id)
            tool_calling = model_info.get('tool_call', False)
            reasoning = model_info.get('reasoning', False)
            
            # Check for multimodal capabilities from modalities field
            modalities = model_info.get('modalities', {})
            input_modalities = modalities.get(None, [])
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_33(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get('name', model_id)
            tool_calling = model_info.get('tool_call', False)
            reasoning = model_info.get('reasoning', False)
            
            # Check for multimodal capabilities from modalities field
            modalities = model_info.get('modalities', {})
            input_modalities = modalities.get('input', None)
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_34(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get('name', model_id)
            tool_calling = model_info.get('tool_call', False)
            reasoning = model_info.get('reasoning', False)
            
            # Check for multimodal capabilities from modalities field
            modalities = model_info.get('modalities', {})
            input_modalities = modalities.get([])
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_35(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get('name', model_id)
            tool_calling = model_info.get('tool_call', False)
            reasoning = model_info.get('reasoning', False)
            
            # Check for multimodal capabilities from modalities field
            modalities = model_info.get('modalities', {})
            input_modalities = modalities.get('input', )
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_36(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get('name', model_id)
            tool_calling = model_info.get('tool_call', False)
            reasoning = model_info.get('reasoning', False)
            
            # Check for multimodal capabilities from modalities field
            modalities = model_info.get('modalities', {})
            input_modalities = modalities.get('XXinputXX', [])
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_37(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get('name', model_id)
            tool_calling = model_info.get('tool_call', False)
            reasoning = model_info.get('reasoning', False)
            
            # Check for multimodal capabilities from modalities field
            modalities = model_info.get('modalities', {})
            input_modalities = modalities.get('INPUT', [])
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_38(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get('name', model_id)
            tool_calling = model_info.get('tool_call', False)
            reasoning = model_info.get('reasoning', False)
            
            # Check for multimodal capabilities from modalities field
            modalities = model_info.get('modalities', {})
            input_modalities = modalities.get('input', [])
            output_modalities = None
            
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_39(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get('name', model_id)
            tool_calling = model_info.get('tool_call', False)
            reasoning = model_info.get('reasoning', False)
            
            # Check for multimodal capabilities from modalities field
            modalities = model_info.get('modalities', {})
            input_modalities = modalities.get('input', [])
            output_modalities = modalities.get(None, [])
            
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_40(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get('name', model_id)
            tool_calling = model_info.get('tool_call', False)
            reasoning = model_info.get('reasoning', False)
            
            # Check for multimodal capabilities from modalities field
            modalities = model_info.get('modalities', {})
            input_modalities = modalities.get('input', [])
            output_modalities = modalities.get('output', None)
            
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_41(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get('name', model_id)
            tool_calling = model_info.get('tool_call', False)
            reasoning = model_info.get('reasoning', False)
            
            # Check for multimodal capabilities from modalities field
            modalities = model_info.get('modalities', {})
            input_modalities = modalities.get('input', [])
            output_modalities = modalities.get([])
            
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_42(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get('name', model_id)
            tool_calling = model_info.get('tool_call', False)
            reasoning = model_info.get('reasoning', False)
            
            # Check for multimodal capabilities from modalities field
            modalities = model_info.get('modalities', {})
            input_modalities = modalities.get('input', [])
            output_modalities = modalities.get('output', )
            
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_43(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get('name', model_id)
            tool_calling = model_info.get('tool_call', False)
            reasoning = model_info.get('reasoning', False)
            
            # Check for multimodal capabilities from modalities field
            modalities = model_info.get('modalities', {})
            input_modalities = modalities.get('input', [])
            output_modalities = modalities.get('XXoutputXX', [])
            
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_44(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
        """Parse model information from models.dev format."""
        try:
            # Extract basic info from models.dev API
            name = model_info.get('name', model_id)
            tool_calling = model_info.get('tool_call', False)
            reasoning = model_info.get('reasoning', False)
            
            # Check for multimodal capabilities from modalities field
            modalities = model_info.get('modalities', {})
            input_modalities = modalities.get('input', [])
            output_modalities = modalities.get('OUTPUT', [])
            
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_45(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            multimodal = None
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_46(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            multimodal = len(input_modalities) > 1 and 'image' in input_modalities
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_47(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            multimodal = len(input_modalities) >= 1 or 'image' in input_modalities
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_48(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            multimodal = len(input_modalities) > 2 or 'image' in input_modalities
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_49(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            multimodal = len(input_modalities) > 1 or 'XXimageXX' in input_modalities
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_50(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            multimodal = len(input_modalities) > 1 or 'IMAGE' in input_modalities
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_51(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            multimodal = len(input_modalities) > 1 or 'image' not in input_modalities
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_52(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_image_input = None
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_53(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_image_input = 'XXimageXX' in input_modalities
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_54(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_image_input = 'IMAGE' in input_modalities
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_55(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_image_input = 'image' not in input_modalities
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_56(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_image_output = None
            
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_57(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_image_output = 'XXimageXX' in output_modalities
            
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_58(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_image_output = 'IMAGE' in output_modalities
            
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_59(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_image_output = 'image' not in output_modalities
            
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_60(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            limits = None
            context_limit = limits.get('context')
            output_limit = limits.get('output')
            
            # Advanced capabilities - use API data where available, conservative fallbacks otherwise
            # Parallel tools: assume supported if tool_calling is true and it's a capable model
            supports_parallel = tool_calling and any(x in model_id.lower() for x in [
                'gpt-4', 'claude-3.5', 'claude-4', 'gemini', 'llama-3.1', 'gemini-2'
            ])
            
            # Caching support - conservative approach based on known providers
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_61(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            limits = model_info.get(None, {})
            context_limit = limits.get('context')
            output_limit = limits.get('output')
            
            # Advanced capabilities - use API data where available, conservative fallbacks otherwise
            # Parallel tools: assume supported if tool_calling is true and it's a capable model
            supports_parallel = tool_calling and any(x in model_id.lower() for x in [
                'gpt-4', 'claude-3.5', 'claude-4', 'gemini', 'llama-3.1', 'gemini-2'
            ])
            
            # Caching support - conservative approach based on known providers
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_62(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            limits = model_info.get('limit', None)
            context_limit = limits.get('context')
            output_limit = limits.get('output')
            
            # Advanced capabilities - use API data where available, conservative fallbacks otherwise
            # Parallel tools: assume supported if tool_calling is true and it's a capable model
            supports_parallel = tool_calling and any(x in model_id.lower() for x in [
                'gpt-4', 'claude-3.5', 'claude-4', 'gemini', 'llama-3.1', 'gemini-2'
            ])
            
            # Caching support - conservative approach based on known providers
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_63(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            limits = model_info.get({})
            context_limit = limits.get('context')
            output_limit = limits.get('output')
            
            # Advanced capabilities - use API data where available, conservative fallbacks otherwise
            # Parallel tools: assume supported if tool_calling is true and it's a capable model
            supports_parallel = tool_calling and any(x in model_id.lower() for x in [
                'gpt-4', 'claude-3.5', 'claude-4', 'gemini', 'llama-3.1', 'gemini-2'
            ])
            
            # Caching support - conservative approach based on known providers
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_64(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            limits = model_info.get('limit', )
            context_limit = limits.get('context')
            output_limit = limits.get('output')
            
            # Advanced capabilities - use API data where available, conservative fallbacks otherwise
            # Parallel tools: assume supported if tool_calling is true and it's a capable model
            supports_parallel = tool_calling and any(x in model_id.lower() for x in [
                'gpt-4', 'claude-3.5', 'claude-4', 'gemini', 'llama-3.1', 'gemini-2'
            ])
            
            # Caching support - conservative approach based on known providers
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_65(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            limits = model_info.get('XXlimitXX', {})
            context_limit = limits.get('context')
            output_limit = limits.get('output')
            
            # Advanced capabilities - use API data where available, conservative fallbacks otherwise
            # Parallel tools: assume supported if tool_calling is true and it's a capable model
            supports_parallel = tool_calling and any(x in model_id.lower() for x in [
                'gpt-4', 'claude-3.5', 'claude-4', 'gemini', 'llama-3.1', 'gemini-2'
            ])
            
            # Caching support - conservative approach based on known providers
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_66(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            limits = model_info.get('LIMIT', {})
            context_limit = limits.get('context')
            output_limit = limits.get('output')
            
            # Advanced capabilities - use API data where available, conservative fallbacks otherwise
            # Parallel tools: assume supported if tool_calling is true and it's a capable model
            supports_parallel = tool_calling and any(x in model_id.lower() for x in [
                'gpt-4', 'claude-3.5', 'claude-4', 'gemini', 'llama-3.1', 'gemini-2'
            ])
            
            # Caching support - conservative approach based on known providers
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_67(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            context_limit = None
            output_limit = limits.get('output')
            
            # Advanced capabilities - use API data where available, conservative fallbacks otherwise
            # Parallel tools: assume supported if tool_calling is true and it's a capable model
            supports_parallel = tool_calling and any(x in model_id.lower() for x in [
                'gpt-4', 'claude-3.5', 'claude-4', 'gemini', 'llama-3.1', 'gemini-2'
            ])
            
            # Caching support - conservative approach based on known providers
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_68(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            context_limit = limits.get(None)
            output_limit = limits.get('output')
            
            # Advanced capabilities - use API data where available, conservative fallbacks otherwise
            # Parallel tools: assume supported if tool_calling is true and it's a capable model
            supports_parallel = tool_calling and any(x in model_id.lower() for x in [
                'gpt-4', 'claude-3.5', 'claude-4', 'gemini', 'llama-3.1', 'gemini-2'
            ])
            
            # Caching support - conservative approach based on known providers
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_69(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            context_limit = limits.get('XXcontextXX')
            output_limit = limits.get('output')
            
            # Advanced capabilities - use API data where available, conservative fallbacks otherwise
            # Parallel tools: assume supported if tool_calling is true and it's a capable model
            supports_parallel = tool_calling and any(x in model_id.lower() for x in [
                'gpt-4', 'claude-3.5', 'claude-4', 'gemini', 'llama-3.1', 'gemini-2'
            ])
            
            # Caching support - conservative approach based on known providers
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_70(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            context_limit = limits.get('CONTEXT')
            output_limit = limits.get('output')
            
            # Advanced capabilities - use API data where available, conservative fallbacks otherwise
            # Parallel tools: assume supported if tool_calling is true and it's a capable model
            supports_parallel = tool_calling and any(x in model_id.lower() for x in [
                'gpt-4', 'claude-3.5', 'claude-4', 'gemini', 'llama-3.1', 'gemini-2'
            ])
            
            # Caching support - conservative approach based on known providers
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_71(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            output_limit = None
            
            # Advanced capabilities - use API data where available, conservative fallbacks otherwise
            # Parallel tools: assume supported if tool_calling is true and it's a capable model
            supports_parallel = tool_calling and any(x in model_id.lower() for x in [
                'gpt-4', 'claude-3.5', 'claude-4', 'gemini', 'llama-3.1', 'gemini-2'
            ])
            
            # Caching support - conservative approach based on known providers
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_72(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            output_limit = limits.get(None)
            
            # Advanced capabilities - use API data where available, conservative fallbacks otherwise
            # Parallel tools: assume supported if tool_calling is true and it's a capable model
            supports_parallel = tool_calling and any(x in model_id.lower() for x in [
                'gpt-4', 'claude-3.5', 'claude-4', 'gemini', 'llama-3.1', 'gemini-2'
            ])
            
            # Caching support - conservative approach based on known providers
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_73(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            output_limit = limits.get('XXoutputXX')
            
            # Advanced capabilities - use API data where available, conservative fallbacks otherwise
            # Parallel tools: assume supported if tool_calling is true and it's a capable model
            supports_parallel = tool_calling and any(x in model_id.lower() for x in [
                'gpt-4', 'claude-3.5', 'claude-4', 'gemini', 'llama-3.1', 'gemini-2'
            ])
            
            # Caching support - conservative approach based on known providers
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_74(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            output_limit = limits.get('OUTPUT')
            
            # Advanced capabilities - use API data where available, conservative fallbacks otherwise
            # Parallel tools: assume supported if tool_calling is true and it's a capable model
            supports_parallel = tool_calling and any(x in model_id.lower() for x in [
                'gpt-4', 'claude-3.5', 'claude-4', 'gemini', 'llama-3.1', 'gemini-2'
            ])
            
            # Caching support - conservative approach based on known providers
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_75(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_parallel = None
            
            # Caching support - conservative approach based on known providers
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_76(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_parallel = tool_calling or any(x in model_id.lower() for x in [
                'gpt-4', 'claude-3.5', 'claude-4', 'gemini', 'llama-3.1', 'gemini-2'
            ])
            
            # Caching support - conservative approach based on known providers
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_77(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_parallel = tool_calling and any(None)
            
            # Caching support - conservative approach based on known providers
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_78(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_parallel = tool_calling and any(x not in model_id.lower() for x in [
                'gpt-4', 'claude-3.5', 'claude-4', 'gemini', 'llama-3.1', 'gemini-2'
            ])
            
            # Caching support - conservative approach based on known providers
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_79(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_parallel = tool_calling and any(x in model_id.upper() for x in [
                'gpt-4', 'claude-3.5', 'claude-4', 'gemini', 'llama-3.1', 'gemini-2'
            ])
            
            # Caching support - conservative approach based on known providers
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_80(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
                'XXgpt-4XX', 'claude-3.5', 'claude-4', 'gemini', 'llama-3.1', 'gemini-2'
            ])
            
            # Caching support - conservative approach based on known providers
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_81(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
                'GPT-4', 'claude-3.5', 'claude-4', 'gemini', 'llama-3.1', 'gemini-2'
            ])
            
            # Caching support - conservative approach based on known providers
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_82(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
                'gpt-4', 'XXclaude-3.5XX', 'claude-4', 'gemini', 'llama-3.1', 'gemini-2'
            ])
            
            # Caching support - conservative approach based on known providers
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_83(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
                'gpt-4', 'CLAUDE-3.5', 'claude-4', 'gemini', 'llama-3.1', 'gemini-2'
            ])
            
            # Caching support - conservative approach based on known providers
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_84(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
                'gpt-4', 'claude-3.5', 'XXclaude-4XX', 'gemini', 'llama-3.1', 'gemini-2'
            ])
            
            # Caching support - conservative approach based on known providers
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_85(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
                'gpt-4', 'claude-3.5', 'CLAUDE-4', 'gemini', 'llama-3.1', 'gemini-2'
            ])
            
            # Caching support - conservative approach based on known providers
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_86(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
                'gpt-4', 'claude-3.5', 'claude-4', 'XXgeminiXX', 'llama-3.1', 'gemini-2'
            ])
            
            # Caching support - conservative approach based on known providers
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_87(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
                'gpt-4', 'claude-3.5', 'claude-4', 'GEMINI', 'llama-3.1', 'gemini-2'
            ])
            
            # Caching support - conservative approach based on known providers
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_88(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
                'gpt-4', 'claude-3.5', 'claude-4', 'gemini', 'XXllama-3.1XX', 'gemini-2'
            ])
            
            # Caching support - conservative approach based on known providers
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_89(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
                'gpt-4', 'claude-3.5', 'claude-4', 'gemini', 'LLAMA-3.1', 'gemini-2'
            ])
            
            # Caching support - conservative approach based on known providers
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_90(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
                'gpt-4', 'claude-3.5', 'claude-4', 'gemini', 'llama-3.1', 'XXgemini-2XX'
            ])
            
            # Caching support - conservative approach based on known providers
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_91(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
                'gpt-4', 'claude-3.5', 'claude-4', 'gemini', 'llama-3.1', 'GEMINI-2'
            ])
            
            # Caching support - conservative approach based on known providers
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_92(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = None
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_93(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] or 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_94(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.upper() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_95(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() not in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_96(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['XXanthropicXX'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_97(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['ANTHROPIC'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_98(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'XXclaude-3XX' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_99(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'CLAUDE-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_100(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' not in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_101(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.upper()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_102(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
            # JSON mode support - based on known model capabilities
            supports_json_mode = None
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_103(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
            # JSON mode support - based on known model capabilities
            supports_json_mode = tool_calling or any(x in model_id.lower() for x in [
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_104(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
            # JSON mode support - based on known model capabilities
            supports_json_mode = tool_calling and any(None)
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_105(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
            # JSON mode support - based on known model capabilities
            supports_json_mode = tool_calling and any(x not in model_id.lower() for x in [
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_106(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
            # JSON mode support - based on known model capabilities
            supports_json_mode = tool_calling and any(x in model_id.upper() for x in [
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_107(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
            # JSON mode support - based on known model capabilities
            supports_json_mode = tool_calling and any(x in model_id.lower() for x in [
                'XXgpt-4XX', 'gpt-3.5-turbo', 'claude-3', 'gemini'
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_108(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
            # JSON mode support - based on known model capabilities
            supports_json_mode = tool_calling and any(x in model_id.lower() for x in [
                'GPT-4', 'gpt-3.5-turbo', 'claude-3', 'gemini'
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_109(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
            # JSON mode support - based on known model capabilities
            supports_json_mode = tool_calling and any(x in model_id.lower() for x in [
                'gpt-4', 'XXgpt-3.5-turboXX', 'claude-3', 'gemini'
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_110(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
            # JSON mode support - based on known model capabilities
            supports_json_mode = tool_calling and any(x in model_id.lower() for x in [
                'gpt-4', 'GPT-3.5-TURBO', 'claude-3', 'gemini'
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_111(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
            # JSON mode support - based on known model capabilities
            supports_json_mode = tool_calling and any(x in model_id.lower() for x in [
                'gpt-4', 'gpt-3.5-turbo', 'XXclaude-3XX', 'gemini'
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_112(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
            # JSON mode support - based on known model capabilities
            supports_json_mode = tool_calling and any(x in model_id.lower() for x in [
                'gpt-4', 'gpt-3.5-turbo', 'CLAUDE-3', 'gemini'
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_113(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
            # JSON mode support - based on known model capabilities
            supports_json_mode = tool_calling and any(x in model_id.lower() for x in [
                'gpt-4', 'gpt-3.5-turbo', 'claude-3', 'XXgeminiXX'
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_114(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
            # JSON mode support - based on known model capabilities
            supports_json_mode = tool_calling and any(x in model_id.lower() for x in [
                'gpt-4', 'gpt-3.5-turbo', 'claude-3', 'GEMINI'
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_115(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
            # JSON mode support - based on known model capabilities
            supports_json_mode = tool_calling and any(x in model_id.lower() for x in [
                'gpt-4', 'gpt-3.5-turbo', 'claude-3', 'gemini'
            ])
            
            # Extract pricing from cost field in API data
            cost_info = None
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_116(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
            # JSON mode support - based on known model capabilities
            supports_json_mode = tool_calling and any(x in model_id.lower() for x in [
                'gpt-4', 'gpt-3.5-turbo', 'claude-3', 'gemini'
            ])
            
            # Extract pricing from cost field in API data
            cost_info = model_info.get(None, {})
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_117(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
            # JSON mode support - based on known model capabilities
            supports_json_mode = tool_calling and any(x in model_id.lower() for x in [
                'gpt-4', 'gpt-3.5-turbo', 'claude-3', 'gemini'
            ])
            
            # Extract pricing from cost field in API data
            cost_info = model_info.get('cost', None)
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_118(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
            # JSON mode support - based on known model capabilities
            supports_json_mode = tool_calling and any(x in model_id.lower() for x in [
                'gpt-4', 'gpt-3.5-turbo', 'claude-3', 'gemini'
            ])
            
            # Extract pricing from cost field in API data
            cost_info = model_info.get({})
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_119(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
            # JSON mode support - based on known model capabilities
            supports_json_mode = tool_calling and any(x in model_id.lower() for x in [
                'gpt-4', 'gpt-3.5-turbo', 'claude-3', 'gemini'
            ])
            
            # Extract pricing from cost field in API data
            cost_info = model_info.get('cost', )
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_120(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
            # JSON mode support - based on known model capabilities
            supports_json_mode = tool_calling and any(x in model_id.lower() for x in [
                'gpt-4', 'gpt-3.5-turbo', 'claude-3', 'gemini'
            ])
            
            # Extract pricing from cost field in API data
            cost_info = model_info.get('XXcostXX', {})
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_121(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
            # JSON mode support - based on known model capabilities
            supports_json_mode = tool_calling and any(x in model_id.lower() for x in [
                'gpt-4', 'gpt-3.5-turbo', 'claude-3', 'gemini'
            ])
            
            # Extract pricing from cost field in API data
            cost_info = model_info.get('COST', {})
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_122(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
            # JSON mode support - based on known model capabilities
            supports_json_mode = tool_calling and any(x in model_id.lower() for x in [
                'gpt-4', 'gpt-3.5-turbo', 'claude-3', 'gemini'
            ])
            
            # Extract pricing from cost field in API data
            cost_info = model_info.get('cost', {})
            pricing = ""
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_123(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
            # JSON mode support - based on known model capabilities
            supports_json_mode = tool_calling and any(x in model_id.lower() for x in [
                'gpt-4', 'gpt-3.5-turbo', 'claude-3', 'gemini'
            ])
            
            # Extract pricing from cost field in API data
            cost_info = model_info.get('cost', {})
            pricing = None
            if cost_info:
                pricing = None
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_124(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
            # JSON mode support - based on known model capabilities
            supports_json_mode = tool_calling and any(x in model_id.lower() for x in [
                'gpt-4', 'gpt-3.5-turbo', 'claude-3', 'gemini'
            ])
            
            # Extract pricing from cost field in API data
            cost_info = model_info.get('cost', {})
            pricing = None
            if cost_info:
                pricing = {
                    'XXinputXX': cost_info.get('input'),
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_125(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
            # JSON mode support - based on known model capabilities
            supports_json_mode = tool_calling and any(x in model_id.lower() for x in [
                'gpt-4', 'gpt-3.5-turbo', 'claude-3', 'gemini'
            ])
            
            # Extract pricing from cost field in API data
            cost_info = model_info.get('cost', {})
            pricing = None
            if cost_info:
                pricing = {
                    'INPUT': cost_info.get('input'),
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_126(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
            # JSON mode support - based on known model capabilities
            supports_json_mode = tool_calling and any(x in model_id.lower() for x in [
                'gpt-4', 'gpt-3.5-turbo', 'claude-3', 'gemini'
            ])
            
            # Extract pricing from cost field in API data
            cost_info = model_info.get('cost', {})
            pricing = None
            if cost_info:
                pricing = {
                    'input': cost_info.get(None),
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_127(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
            # JSON mode support - based on known model capabilities
            supports_json_mode = tool_calling and any(x in model_id.lower() for x in [
                'gpt-4', 'gpt-3.5-turbo', 'claude-3', 'gemini'
            ])
            
            # Extract pricing from cost field in API data
            cost_info = model_info.get('cost', {})
            pricing = None
            if cost_info:
                pricing = {
                    'input': cost_info.get('XXinputXX'),
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_128(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
            # JSON mode support - based on known model capabilities
            supports_json_mode = tool_calling and any(x in model_id.lower() for x in [
                'gpt-4', 'gpt-3.5-turbo', 'claude-3', 'gemini'
            ])
            
            # Extract pricing from cost field in API data
            cost_info = model_info.get('cost', {})
            pricing = None
            if cost_info:
                pricing = {
                    'input': cost_info.get('INPUT'),
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_129(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
                    'XXoutputXX': cost_info.get('output')
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_130(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
                    'OUTPUT': cost_info.get('output')
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_131(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
                    'output': cost_info.get(None)
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_132(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
                    'output': cost_info.get('XXoutputXX')
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_133(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
                    'output': cost_info.get('OUTPUT')
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_134(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
                model_id=None,
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_135(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
                name=None,
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_136(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
                provider=None,
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_137(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
                tool_calling=None,
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_138(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
                reasoning=None,
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_139(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
                multimodal=None,
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_140(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
                context_limit=None,
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_141(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
                output_limit=None,
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_142(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
                supports_streaming=None,  # Most modern models support streaming
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_143(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
                supports_parallel_tools=None,
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_144(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
                supports_image_input=None,
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_145(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
                supports_image_output=None,
                supports_caching=supports_caching,
                supports_json_mode=supports_json_mode,
                supports_system_prompt=True,  # Most models support system prompts
                pricing=pricing,
                last_updated=time.time()
            )
            
        except Exception as e:
            logger.warning(f"Error parsing model info for {model_id}: {e}")
            return None
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_146(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
                supports_caching=None,
                supports_json_mode=supports_json_mode,
                supports_system_prompt=True,  # Most models support system prompts
                pricing=pricing,
                last_updated=time.time()
            )
            
        except Exception as e:
            logger.warning(f"Error parsing model info for {model_id}: {e}")
            return None
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_147(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
                supports_json_mode=None,
                supports_system_prompt=True,  # Most models support system prompts
                pricing=pricing,
                last_updated=time.time()
            )
            
        except Exception as e:
            logger.warning(f"Error parsing model info for {model_id}: {e}")
            return None
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_148(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
                supports_system_prompt=None,  # Most models support system prompts
                pricing=pricing,
                last_updated=time.time()
            )
            
        except Exception as e:
            logger.warning(f"Error parsing model info for {model_id}: {e}")
            return None
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_149(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
                pricing=None,
                last_updated=time.time()
            )
            
        except Exception as e:
            logger.warning(f"Error parsing model info for {model_id}: {e}")
            return None
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_150(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
                last_updated=None
            )
            
        except Exception as e:
            logger.warning(f"Error parsing model info for {model_id}: {e}")
            return None
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_151(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_152(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_153(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_154(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_155(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_156(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_157(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_158(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_159(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_160(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_161(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_162(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
                supports_caching=supports_caching,
                supports_json_mode=supports_json_mode,
                supports_system_prompt=True,  # Most models support system prompts
                pricing=pricing,
                last_updated=time.time()
            )
            
        except Exception as e:
            logger.warning(f"Error parsing model info for {model_id}: {e}")
            return None
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_163(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
                supports_json_mode=supports_json_mode,
                supports_system_prompt=True,  # Most models support system prompts
                pricing=pricing,
                last_updated=time.time()
            )
            
        except Exception as e:
            logger.warning(f"Error parsing model info for {model_id}: {e}")
            return None
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_164(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
                supports_system_prompt=True,  # Most models support system prompts
                pricing=pricing,
                last_updated=time.time()
            )
            
        except Exception as e:
            logger.warning(f"Error parsing model info for {model_id}: {e}")
            return None
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_165(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
                pricing=pricing,
                last_updated=time.time()
            )
            
        except Exception as e:
            logger.warning(f"Error parsing model info for {model_id}: {e}")
            return None
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_166(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
                last_updated=time.time()
            )
            
        except Exception as e:
            logger.warning(f"Error parsing model info for {model_id}: {e}")
            return None
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_167(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
                )
            
        except Exception as e:
            logger.warning(f"Error parsing model info for {model_id}: {e}")
            return None
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_168(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
                supports_streaming=False,  # Most modern models support streaming
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
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_169(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
                supports_system_prompt=False,  # Most models support system prompts
                pricing=pricing,
                last_updated=time.time()
            )
            
        except Exception as e:
            logger.warning(f"Error parsing model info for {model_id}: {e}")
            return None
            
    def xǁCapabilityDetectorǁ_parse_model_info__mutmut_170(self, model_id: str, provider: str, model_info: Dict[str, Any]) -> Optional[ModelCapabilities]:
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
            supports_caching = provider.lower() in ['anthropic'] and 'claude-3' in model_id.lower()
            
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
            logger.warning(None)
            return None
            
    
    xǁCapabilityDetectorǁ_parse_model_info__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁCapabilityDetectorǁ_parse_model_info__mutmut_1': xǁCapabilityDetectorǁ_parse_model_info__mutmut_1, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_2': xǁCapabilityDetectorǁ_parse_model_info__mutmut_2, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_3': xǁCapabilityDetectorǁ_parse_model_info__mutmut_3, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_4': xǁCapabilityDetectorǁ_parse_model_info__mutmut_4, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_5': xǁCapabilityDetectorǁ_parse_model_info__mutmut_5, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_6': xǁCapabilityDetectorǁ_parse_model_info__mutmut_6, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_7': xǁCapabilityDetectorǁ_parse_model_info__mutmut_7, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_8': xǁCapabilityDetectorǁ_parse_model_info__mutmut_8, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_9': xǁCapabilityDetectorǁ_parse_model_info__mutmut_9, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_10': xǁCapabilityDetectorǁ_parse_model_info__mutmut_10, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_11': xǁCapabilityDetectorǁ_parse_model_info__mutmut_11, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_12': xǁCapabilityDetectorǁ_parse_model_info__mutmut_12, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_13': xǁCapabilityDetectorǁ_parse_model_info__mutmut_13, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_14': xǁCapabilityDetectorǁ_parse_model_info__mutmut_14, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_15': xǁCapabilityDetectorǁ_parse_model_info__mutmut_15, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_16': xǁCapabilityDetectorǁ_parse_model_info__mutmut_16, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_17': xǁCapabilityDetectorǁ_parse_model_info__mutmut_17, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_18': xǁCapabilityDetectorǁ_parse_model_info__mutmut_18, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_19': xǁCapabilityDetectorǁ_parse_model_info__mutmut_19, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_20': xǁCapabilityDetectorǁ_parse_model_info__mutmut_20, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_21': xǁCapabilityDetectorǁ_parse_model_info__mutmut_21, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_22': xǁCapabilityDetectorǁ_parse_model_info__mutmut_22, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_23': xǁCapabilityDetectorǁ_parse_model_info__mutmut_23, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_24': xǁCapabilityDetectorǁ_parse_model_info__mutmut_24, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_25': xǁCapabilityDetectorǁ_parse_model_info__mutmut_25, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_26': xǁCapabilityDetectorǁ_parse_model_info__mutmut_26, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_27': xǁCapabilityDetectorǁ_parse_model_info__mutmut_27, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_28': xǁCapabilityDetectorǁ_parse_model_info__mutmut_28, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_29': xǁCapabilityDetectorǁ_parse_model_info__mutmut_29, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_30': xǁCapabilityDetectorǁ_parse_model_info__mutmut_30, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_31': xǁCapabilityDetectorǁ_parse_model_info__mutmut_31, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_32': xǁCapabilityDetectorǁ_parse_model_info__mutmut_32, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_33': xǁCapabilityDetectorǁ_parse_model_info__mutmut_33, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_34': xǁCapabilityDetectorǁ_parse_model_info__mutmut_34, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_35': xǁCapabilityDetectorǁ_parse_model_info__mutmut_35, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_36': xǁCapabilityDetectorǁ_parse_model_info__mutmut_36, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_37': xǁCapabilityDetectorǁ_parse_model_info__mutmut_37, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_38': xǁCapabilityDetectorǁ_parse_model_info__mutmut_38, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_39': xǁCapabilityDetectorǁ_parse_model_info__mutmut_39, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_40': xǁCapabilityDetectorǁ_parse_model_info__mutmut_40, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_41': xǁCapabilityDetectorǁ_parse_model_info__mutmut_41, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_42': xǁCapabilityDetectorǁ_parse_model_info__mutmut_42, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_43': xǁCapabilityDetectorǁ_parse_model_info__mutmut_43, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_44': xǁCapabilityDetectorǁ_parse_model_info__mutmut_44, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_45': xǁCapabilityDetectorǁ_parse_model_info__mutmut_45, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_46': xǁCapabilityDetectorǁ_parse_model_info__mutmut_46, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_47': xǁCapabilityDetectorǁ_parse_model_info__mutmut_47, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_48': xǁCapabilityDetectorǁ_parse_model_info__mutmut_48, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_49': xǁCapabilityDetectorǁ_parse_model_info__mutmut_49, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_50': xǁCapabilityDetectorǁ_parse_model_info__mutmut_50, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_51': xǁCapabilityDetectorǁ_parse_model_info__mutmut_51, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_52': xǁCapabilityDetectorǁ_parse_model_info__mutmut_52, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_53': xǁCapabilityDetectorǁ_parse_model_info__mutmut_53, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_54': xǁCapabilityDetectorǁ_parse_model_info__mutmut_54, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_55': xǁCapabilityDetectorǁ_parse_model_info__mutmut_55, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_56': xǁCapabilityDetectorǁ_parse_model_info__mutmut_56, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_57': xǁCapabilityDetectorǁ_parse_model_info__mutmut_57, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_58': xǁCapabilityDetectorǁ_parse_model_info__mutmut_58, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_59': xǁCapabilityDetectorǁ_parse_model_info__mutmut_59, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_60': xǁCapabilityDetectorǁ_parse_model_info__mutmut_60, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_61': xǁCapabilityDetectorǁ_parse_model_info__mutmut_61, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_62': xǁCapabilityDetectorǁ_parse_model_info__mutmut_62, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_63': xǁCapabilityDetectorǁ_parse_model_info__mutmut_63, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_64': xǁCapabilityDetectorǁ_parse_model_info__mutmut_64, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_65': xǁCapabilityDetectorǁ_parse_model_info__mutmut_65, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_66': xǁCapabilityDetectorǁ_parse_model_info__mutmut_66, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_67': xǁCapabilityDetectorǁ_parse_model_info__mutmut_67, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_68': xǁCapabilityDetectorǁ_parse_model_info__mutmut_68, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_69': xǁCapabilityDetectorǁ_parse_model_info__mutmut_69, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_70': xǁCapabilityDetectorǁ_parse_model_info__mutmut_70, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_71': xǁCapabilityDetectorǁ_parse_model_info__mutmut_71, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_72': xǁCapabilityDetectorǁ_parse_model_info__mutmut_72, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_73': xǁCapabilityDetectorǁ_parse_model_info__mutmut_73, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_74': xǁCapabilityDetectorǁ_parse_model_info__mutmut_74, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_75': xǁCapabilityDetectorǁ_parse_model_info__mutmut_75, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_76': xǁCapabilityDetectorǁ_parse_model_info__mutmut_76, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_77': xǁCapabilityDetectorǁ_parse_model_info__mutmut_77, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_78': xǁCapabilityDetectorǁ_parse_model_info__mutmut_78, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_79': xǁCapabilityDetectorǁ_parse_model_info__mutmut_79, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_80': xǁCapabilityDetectorǁ_parse_model_info__mutmut_80, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_81': xǁCapabilityDetectorǁ_parse_model_info__mutmut_81, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_82': xǁCapabilityDetectorǁ_parse_model_info__mutmut_82, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_83': xǁCapabilityDetectorǁ_parse_model_info__mutmut_83, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_84': xǁCapabilityDetectorǁ_parse_model_info__mutmut_84, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_85': xǁCapabilityDetectorǁ_parse_model_info__mutmut_85, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_86': xǁCapabilityDetectorǁ_parse_model_info__mutmut_86, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_87': xǁCapabilityDetectorǁ_parse_model_info__mutmut_87, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_88': xǁCapabilityDetectorǁ_parse_model_info__mutmut_88, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_89': xǁCapabilityDetectorǁ_parse_model_info__mutmut_89, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_90': xǁCapabilityDetectorǁ_parse_model_info__mutmut_90, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_91': xǁCapabilityDetectorǁ_parse_model_info__mutmut_91, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_92': xǁCapabilityDetectorǁ_parse_model_info__mutmut_92, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_93': xǁCapabilityDetectorǁ_parse_model_info__mutmut_93, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_94': xǁCapabilityDetectorǁ_parse_model_info__mutmut_94, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_95': xǁCapabilityDetectorǁ_parse_model_info__mutmut_95, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_96': xǁCapabilityDetectorǁ_parse_model_info__mutmut_96, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_97': xǁCapabilityDetectorǁ_parse_model_info__mutmut_97, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_98': xǁCapabilityDetectorǁ_parse_model_info__mutmut_98, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_99': xǁCapabilityDetectorǁ_parse_model_info__mutmut_99, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_100': xǁCapabilityDetectorǁ_parse_model_info__mutmut_100, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_101': xǁCapabilityDetectorǁ_parse_model_info__mutmut_101, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_102': xǁCapabilityDetectorǁ_parse_model_info__mutmut_102, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_103': xǁCapabilityDetectorǁ_parse_model_info__mutmut_103, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_104': xǁCapabilityDetectorǁ_parse_model_info__mutmut_104, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_105': xǁCapabilityDetectorǁ_parse_model_info__mutmut_105, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_106': xǁCapabilityDetectorǁ_parse_model_info__mutmut_106, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_107': xǁCapabilityDetectorǁ_parse_model_info__mutmut_107, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_108': xǁCapabilityDetectorǁ_parse_model_info__mutmut_108, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_109': xǁCapabilityDetectorǁ_parse_model_info__mutmut_109, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_110': xǁCapabilityDetectorǁ_parse_model_info__mutmut_110, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_111': xǁCapabilityDetectorǁ_parse_model_info__mutmut_111, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_112': xǁCapabilityDetectorǁ_parse_model_info__mutmut_112, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_113': xǁCapabilityDetectorǁ_parse_model_info__mutmut_113, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_114': xǁCapabilityDetectorǁ_parse_model_info__mutmut_114, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_115': xǁCapabilityDetectorǁ_parse_model_info__mutmut_115, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_116': xǁCapabilityDetectorǁ_parse_model_info__mutmut_116, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_117': xǁCapabilityDetectorǁ_parse_model_info__mutmut_117, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_118': xǁCapabilityDetectorǁ_parse_model_info__mutmut_118, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_119': xǁCapabilityDetectorǁ_parse_model_info__mutmut_119, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_120': xǁCapabilityDetectorǁ_parse_model_info__mutmut_120, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_121': xǁCapabilityDetectorǁ_parse_model_info__mutmut_121, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_122': xǁCapabilityDetectorǁ_parse_model_info__mutmut_122, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_123': xǁCapabilityDetectorǁ_parse_model_info__mutmut_123, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_124': xǁCapabilityDetectorǁ_parse_model_info__mutmut_124, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_125': xǁCapabilityDetectorǁ_parse_model_info__mutmut_125, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_126': xǁCapabilityDetectorǁ_parse_model_info__mutmut_126, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_127': xǁCapabilityDetectorǁ_parse_model_info__mutmut_127, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_128': xǁCapabilityDetectorǁ_parse_model_info__mutmut_128, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_129': xǁCapabilityDetectorǁ_parse_model_info__mutmut_129, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_130': xǁCapabilityDetectorǁ_parse_model_info__mutmut_130, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_131': xǁCapabilityDetectorǁ_parse_model_info__mutmut_131, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_132': xǁCapabilityDetectorǁ_parse_model_info__mutmut_132, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_133': xǁCapabilityDetectorǁ_parse_model_info__mutmut_133, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_134': xǁCapabilityDetectorǁ_parse_model_info__mutmut_134, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_135': xǁCapabilityDetectorǁ_parse_model_info__mutmut_135, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_136': xǁCapabilityDetectorǁ_parse_model_info__mutmut_136, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_137': xǁCapabilityDetectorǁ_parse_model_info__mutmut_137, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_138': xǁCapabilityDetectorǁ_parse_model_info__mutmut_138, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_139': xǁCapabilityDetectorǁ_parse_model_info__mutmut_139, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_140': xǁCapabilityDetectorǁ_parse_model_info__mutmut_140, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_141': xǁCapabilityDetectorǁ_parse_model_info__mutmut_141, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_142': xǁCapabilityDetectorǁ_parse_model_info__mutmut_142, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_143': xǁCapabilityDetectorǁ_parse_model_info__mutmut_143, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_144': xǁCapabilityDetectorǁ_parse_model_info__mutmut_144, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_145': xǁCapabilityDetectorǁ_parse_model_info__mutmut_145, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_146': xǁCapabilityDetectorǁ_parse_model_info__mutmut_146, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_147': xǁCapabilityDetectorǁ_parse_model_info__mutmut_147, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_148': xǁCapabilityDetectorǁ_parse_model_info__mutmut_148, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_149': xǁCapabilityDetectorǁ_parse_model_info__mutmut_149, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_150': xǁCapabilityDetectorǁ_parse_model_info__mutmut_150, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_151': xǁCapabilityDetectorǁ_parse_model_info__mutmut_151, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_152': xǁCapabilityDetectorǁ_parse_model_info__mutmut_152, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_153': xǁCapabilityDetectorǁ_parse_model_info__mutmut_153, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_154': xǁCapabilityDetectorǁ_parse_model_info__mutmut_154, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_155': xǁCapabilityDetectorǁ_parse_model_info__mutmut_155, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_156': xǁCapabilityDetectorǁ_parse_model_info__mutmut_156, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_157': xǁCapabilityDetectorǁ_parse_model_info__mutmut_157, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_158': xǁCapabilityDetectorǁ_parse_model_info__mutmut_158, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_159': xǁCapabilityDetectorǁ_parse_model_info__mutmut_159, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_160': xǁCapabilityDetectorǁ_parse_model_info__mutmut_160, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_161': xǁCapabilityDetectorǁ_parse_model_info__mutmut_161, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_162': xǁCapabilityDetectorǁ_parse_model_info__mutmut_162, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_163': xǁCapabilityDetectorǁ_parse_model_info__mutmut_163, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_164': xǁCapabilityDetectorǁ_parse_model_info__mutmut_164, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_165': xǁCapabilityDetectorǁ_parse_model_info__mutmut_165, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_166': xǁCapabilityDetectorǁ_parse_model_info__mutmut_166, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_167': xǁCapabilityDetectorǁ_parse_model_info__mutmut_167, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_168': xǁCapabilityDetectorǁ_parse_model_info__mutmut_168, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_169': xǁCapabilityDetectorǁ_parse_model_info__mutmut_169, 
        'xǁCapabilityDetectorǁ_parse_model_info__mutmut_170': xǁCapabilityDetectorǁ_parse_model_info__mutmut_170
    }
    
    def _parse_model_info(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁCapabilityDetectorǁ_parse_model_info__mutmut_orig"), object.__getattribute__(self, "xǁCapabilityDetectorǁ_parse_model_info__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _parse_model_info.__signature__ = _mutmut_signature(xǁCapabilityDetectorǁ_parse_model_info__mutmut_orig)
    xǁCapabilityDetectorǁ_parse_model_info__mutmut_orig.__name__ = 'xǁCapabilityDetectorǁ_parse_model_info'
    def xǁCapabilityDetectorǁ_add_model_aliases__mutmut_orig(self, model_id: str, capability: ModelCapabilities) -> None:
        """Add common aliases for the model."""
        # Add version without provider prefix
        if '/' in model_id:
            base_name = model_id.split('/', 1)[1]
            self._capability_cache[base_name] = capability
            
        # Add provider-prefixed version if not already prefixed
        if '/' not in model_id:
            prefixed_name = f"{capability.provider}/{model_id}"
            self._capability_cache[prefixed_name] = capability
            
    def xǁCapabilityDetectorǁ_add_model_aliases__mutmut_1(self, model_id: str, capability: ModelCapabilities) -> None:
        """Add common aliases for the model."""
        # Add version without provider prefix
        if 'XX/XX' in model_id:
            base_name = model_id.split('/', 1)[1]
            self._capability_cache[base_name] = capability
            
        # Add provider-prefixed version if not already prefixed
        if '/' not in model_id:
            prefixed_name = f"{capability.provider}/{model_id}"
            self._capability_cache[prefixed_name] = capability
            
    def xǁCapabilityDetectorǁ_add_model_aliases__mutmut_2(self, model_id: str, capability: ModelCapabilities) -> None:
        """Add common aliases for the model."""
        # Add version without provider prefix
        if '/' not in model_id:
            base_name = model_id.split('/', 1)[1]
            self._capability_cache[base_name] = capability
            
        # Add provider-prefixed version if not already prefixed
        if '/' not in model_id:
            prefixed_name = f"{capability.provider}/{model_id}"
            self._capability_cache[prefixed_name] = capability
            
    def xǁCapabilityDetectorǁ_add_model_aliases__mutmut_3(self, model_id: str, capability: ModelCapabilities) -> None:
        """Add common aliases for the model."""
        # Add version without provider prefix
        if '/' in model_id:
            base_name = None
            self._capability_cache[base_name] = capability
            
        # Add provider-prefixed version if not already prefixed
        if '/' not in model_id:
            prefixed_name = f"{capability.provider}/{model_id}"
            self._capability_cache[prefixed_name] = capability
            
    def xǁCapabilityDetectorǁ_add_model_aliases__mutmut_4(self, model_id: str, capability: ModelCapabilities) -> None:
        """Add common aliases for the model."""
        # Add version without provider prefix
        if '/' in model_id:
            base_name = model_id.split(None, 1)[1]
            self._capability_cache[base_name] = capability
            
        # Add provider-prefixed version if not already prefixed
        if '/' not in model_id:
            prefixed_name = f"{capability.provider}/{model_id}"
            self._capability_cache[prefixed_name] = capability
            
    def xǁCapabilityDetectorǁ_add_model_aliases__mutmut_5(self, model_id: str, capability: ModelCapabilities) -> None:
        """Add common aliases for the model."""
        # Add version without provider prefix
        if '/' in model_id:
            base_name = model_id.split('/', None)[1]
            self._capability_cache[base_name] = capability
            
        # Add provider-prefixed version if not already prefixed
        if '/' not in model_id:
            prefixed_name = f"{capability.provider}/{model_id}"
            self._capability_cache[prefixed_name] = capability
            
    def xǁCapabilityDetectorǁ_add_model_aliases__mutmut_6(self, model_id: str, capability: ModelCapabilities) -> None:
        """Add common aliases for the model."""
        # Add version without provider prefix
        if '/' in model_id:
            base_name = model_id.split(1)[1]
            self._capability_cache[base_name] = capability
            
        # Add provider-prefixed version if not already prefixed
        if '/' not in model_id:
            prefixed_name = f"{capability.provider}/{model_id}"
            self._capability_cache[prefixed_name] = capability
            
    def xǁCapabilityDetectorǁ_add_model_aliases__mutmut_7(self, model_id: str, capability: ModelCapabilities) -> None:
        """Add common aliases for the model."""
        # Add version without provider prefix
        if '/' in model_id:
            base_name = model_id.split('/', )[1]
            self._capability_cache[base_name] = capability
            
        # Add provider-prefixed version if not already prefixed
        if '/' not in model_id:
            prefixed_name = f"{capability.provider}/{model_id}"
            self._capability_cache[prefixed_name] = capability
            
    def xǁCapabilityDetectorǁ_add_model_aliases__mutmut_8(self, model_id: str, capability: ModelCapabilities) -> None:
        """Add common aliases for the model."""
        # Add version without provider prefix
        if '/' in model_id:
            base_name = model_id.rsplit('/', 1)[1]
            self._capability_cache[base_name] = capability
            
        # Add provider-prefixed version if not already prefixed
        if '/' not in model_id:
            prefixed_name = f"{capability.provider}/{model_id}"
            self._capability_cache[prefixed_name] = capability
            
    def xǁCapabilityDetectorǁ_add_model_aliases__mutmut_9(self, model_id: str, capability: ModelCapabilities) -> None:
        """Add common aliases for the model."""
        # Add version without provider prefix
        if '/' in model_id:
            base_name = model_id.split('XX/XX', 1)[1]
            self._capability_cache[base_name] = capability
            
        # Add provider-prefixed version if not already prefixed
        if '/' not in model_id:
            prefixed_name = f"{capability.provider}/{model_id}"
            self._capability_cache[prefixed_name] = capability
            
    def xǁCapabilityDetectorǁ_add_model_aliases__mutmut_10(self, model_id: str, capability: ModelCapabilities) -> None:
        """Add common aliases for the model."""
        # Add version without provider prefix
        if '/' in model_id:
            base_name = model_id.split('/', 2)[1]
            self._capability_cache[base_name] = capability
            
        # Add provider-prefixed version if not already prefixed
        if '/' not in model_id:
            prefixed_name = f"{capability.provider}/{model_id}"
            self._capability_cache[prefixed_name] = capability
            
    def xǁCapabilityDetectorǁ_add_model_aliases__mutmut_11(self, model_id: str, capability: ModelCapabilities) -> None:
        """Add common aliases for the model."""
        # Add version without provider prefix
        if '/' in model_id:
            base_name = model_id.split('/', 1)[2]
            self._capability_cache[base_name] = capability
            
        # Add provider-prefixed version if not already prefixed
        if '/' not in model_id:
            prefixed_name = f"{capability.provider}/{model_id}"
            self._capability_cache[prefixed_name] = capability
            
    def xǁCapabilityDetectorǁ_add_model_aliases__mutmut_12(self, model_id: str, capability: ModelCapabilities) -> None:
        """Add common aliases for the model."""
        # Add version without provider prefix
        if '/' in model_id:
            base_name = model_id.split('/', 1)[1]
            self._capability_cache[base_name] = None
            
        # Add provider-prefixed version if not already prefixed
        if '/' not in model_id:
            prefixed_name = f"{capability.provider}/{model_id}"
            self._capability_cache[prefixed_name] = capability
            
    def xǁCapabilityDetectorǁ_add_model_aliases__mutmut_13(self, model_id: str, capability: ModelCapabilities) -> None:
        """Add common aliases for the model."""
        # Add version without provider prefix
        if '/' in model_id:
            base_name = model_id.split('/', 1)[1]
            self._capability_cache[base_name] = capability
            
        # Add provider-prefixed version if not already prefixed
        if 'XX/XX' not in model_id:
            prefixed_name = f"{capability.provider}/{model_id}"
            self._capability_cache[prefixed_name] = capability
            
    def xǁCapabilityDetectorǁ_add_model_aliases__mutmut_14(self, model_id: str, capability: ModelCapabilities) -> None:
        """Add common aliases for the model."""
        # Add version without provider prefix
        if '/' in model_id:
            base_name = model_id.split('/', 1)[1]
            self._capability_cache[base_name] = capability
            
        # Add provider-prefixed version if not already prefixed
        if '/' in model_id:
            prefixed_name = f"{capability.provider}/{model_id}"
            self._capability_cache[prefixed_name] = capability
            
    def xǁCapabilityDetectorǁ_add_model_aliases__mutmut_15(self, model_id: str, capability: ModelCapabilities) -> None:
        """Add common aliases for the model."""
        # Add version without provider prefix
        if '/' in model_id:
            base_name = model_id.split('/', 1)[1]
            self._capability_cache[base_name] = capability
            
        # Add provider-prefixed version if not already prefixed
        if '/' not in model_id:
            prefixed_name = None
            self._capability_cache[prefixed_name] = capability
            
    def xǁCapabilityDetectorǁ_add_model_aliases__mutmut_16(self, model_id: str, capability: ModelCapabilities) -> None:
        """Add common aliases for the model."""
        # Add version without provider prefix
        if '/' in model_id:
            base_name = model_id.split('/', 1)[1]
            self._capability_cache[base_name] = capability
            
        # Add provider-prefixed version if not already prefixed
        if '/' not in model_id:
            prefixed_name = f"{capability.provider}/{model_id}"
            self._capability_cache[prefixed_name] = None
            
    
    xǁCapabilityDetectorǁ_add_model_aliases__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁCapabilityDetectorǁ_add_model_aliases__mutmut_1': xǁCapabilityDetectorǁ_add_model_aliases__mutmut_1, 
        'xǁCapabilityDetectorǁ_add_model_aliases__mutmut_2': xǁCapabilityDetectorǁ_add_model_aliases__mutmut_2, 
        'xǁCapabilityDetectorǁ_add_model_aliases__mutmut_3': xǁCapabilityDetectorǁ_add_model_aliases__mutmut_3, 
        'xǁCapabilityDetectorǁ_add_model_aliases__mutmut_4': xǁCapabilityDetectorǁ_add_model_aliases__mutmut_4, 
        'xǁCapabilityDetectorǁ_add_model_aliases__mutmut_5': xǁCapabilityDetectorǁ_add_model_aliases__mutmut_5, 
        'xǁCapabilityDetectorǁ_add_model_aliases__mutmut_6': xǁCapabilityDetectorǁ_add_model_aliases__mutmut_6, 
        'xǁCapabilityDetectorǁ_add_model_aliases__mutmut_7': xǁCapabilityDetectorǁ_add_model_aliases__mutmut_7, 
        'xǁCapabilityDetectorǁ_add_model_aliases__mutmut_8': xǁCapabilityDetectorǁ_add_model_aliases__mutmut_8, 
        'xǁCapabilityDetectorǁ_add_model_aliases__mutmut_9': xǁCapabilityDetectorǁ_add_model_aliases__mutmut_9, 
        'xǁCapabilityDetectorǁ_add_model_aliases__mutmut_10': xǁCapabilityDetectorǁ_add_model_aliases__mutmut_10, 
        'xǁCapabilityDetectorǁ_add_model_aliases__mutmut_11': xǁCapabilityDetectorǁ_add_model_aliases__mutmut_11, 
        'xǁCapabilityDetectorǁ_add_model_aliases__mutmut_12': xǁCapabilityDetectorǁ_add_model_aliases__mutmut_12, 
        'xǁCapabilityDetectorǁ_add_model_aliases__mutmut_13': xǁCapabilityDetectorǁ_add_model_aliases__mutmut_13, 
        'xǁCapabilityDetectorǁ_add_model_aliases__mutmut_14': xǁCapabilityDetectorǁ_add_model_aliases__mutmut_14, 
        'xǁCapabilityDetectorǁ_add_model_aliases__mutmut_15': xǁCapabilityDetectorǁ_add_model_aliases__mutmut_15, 
        'xǁCapabilityDetectorǁ_add_model_aliases__mutmut_16': xǁCapabilityDetectorǁ_add_model_aliases__mutmut_16
    }
    
    def _add_model_aliases(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁCapabilityDetectorǁ_add_model_aliases__mutmut_orig"), object.__getattribute__(self, "xǁCapabilityDetectorǁ_add_model_aliases__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _add_model_aliases.__signature__ = _mutmut_signature(xǁCapabilityDetectorǁ_add_model_aliases__mutmut_orig)
    xǁCapabilityDetectorǁ_add_model_aliases__mutmut_orig.__name__ = 'xǁCapabilityDetectorǁ_add_model_aliases'
    def xǁCapabilityDetectorǁ_fuzzy_match_model__mutmut_orig(self, model_name: str) -> Optional[ModelCapabilities]:
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
        
    def xǁCapabilityDetectorǁ_fuzzy_match_model__mutmut_1(self, model_name: str) -> Optional[ModelCapabilities]:
        """Attempt fuzzy matching for model names."""
        model_lower = None
        
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
        
    def xǁCapabilityDetectorǁ_fuzzy_match_model__mutmut_2(self, model_name: str) -> Optional[ModelCapabilities]:
        """Attempt fuzzy matching for model names."""
        model_lower = model_name.upper()
        
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
        
    def xǁCapabilityDetectorǁ_fuzzy_match_model__mutmut_3(self, model_name: str) -> Optional[ModelCapabilities]:
        """Attempt fuzzy matching for model names."""
        model_lower = model_name.lower()
        
        # Try partial matches
        for cached_name, capability in self._capability_cache.items():
            cached_lower = None
            
            # Check if the model name is contained in the cached name
            if model_lower in cached_lower or cached_lower in model_lower:
                # Verify it's a reasonable match (not too different)
                if abs(len(model_lower) - len(cached_lower)) < 10:
                    logger.info(f"Fuzzy matched {model_name} to {cached_name}")
                    return capability
                    
        return None
        
    def xǁCapabilityDetectorǁ_fuzzy_match_model__mutmut_4(self, model_name: str) -> Optional[ModelCapabilities]:
        """Attempt fuzzy matching for model names."""
        model_lower = model_name.lower()
        
        # Try partial matches
        for cached_name, capability in self._capability_cache.items():
            cached_lower = cached_name.upper()
            
            # Check if the model name is contained in the cached name
            if model_lower in cached_lower or cached_lower in model_lower:
                # Verify it's a reasonable match (not too different)
                if abs(len(model_lower) - len(cached_lower)) < 10:
                    logger.info(f"Fuzzy matched {model_name} to {cached_name}")
                    return capability
                    
        return None
        
    def xǁCapabilityDetectorǁ_fuzzy_match_model__mutmut_5(self, model_name: str) -> Optional[ModelCapabilities]:
        """Attempt fuzzy matching for model names."""
        model_lower = model_name.lower()
        
        # Try partial matches
        for cached_name, capability in self._capability_cache.items():
            cached_lower = cached_name.lower()
            
            # Check if the model name is contained in the cached name
            if model_lower in cached_lower and cached_lower in model_lower:
                # Verify it's a reasonable match (not too different)
                if abs(len(model_lower) - len(cached_lower)) < 10:
                    logger.info(f"Fuzzy matched {model_name} to {cached_name}")
                    return capability
                    
        return None
        
    def xǁCapabilityDetectorǁ_fuzzy_match_model__mutmut_6(self, model_name: str) -> Optional[ModelCapabilities]:
        """Attempt fuzzy matching for model names."""
        model_lower = model_name.lower()
        
        # Try partial matches
        for cached_name, capability in self._capability_cache.items():
            cached_lower = cached_name.lower()
            
            # Check if the model name is contained in the cached name
            if model_lower not in cached_lower or cached_lower in model_lower:
                # Verify it's a reasonable match (not too different)
                if abs(len(model_lower) - len(cached_lower)) < 10:
                    logger.info(f"Fuzzy matched {model_name} to {cached_name}")
                    return capability
                    
        return None
        
    def xǁCapabilityDetectorǁ_fuzzy_match_model__mutmut_7(self, model_name: str) -> Optional[ModelCapabilities]:
        """Attempt fuzzy matching for model names."""
        model_lower = model_name.lower()
        
        # Try partial matches
        for cached_name, capability in self._capability_cache.items():
            cached_lower = cached_name.lower()
            
            # Check if the model name is contained in the cached name
            if model_lower in cached_lower or cached_lower not in model_lower:
                # Verify it's a reasonable match (not too different)
                if abs(len(model_lower) - len(cached_lower)) < 10:
                    logger.info(f"Fuzzy matched {model_name} to {cached_name}")
                    return capability
                    
        return None
        
    def xǁCapabilityDetectorǁ_fuzzy_match_model__mutmut_8(self, model_name: str) -> Optional[ModelCapabilities]:
        """Attempt fuzzy matching for model names."""
        model_lower = model_name.lower()
        
        # Try partial matches
        for cached_name, capability in self._capability_cache.items():
            cached_lower = cached_name.lower()
            
            # Check if the model name is contained in the cached name
            if model_lower in cached_lower or cached_lower in model_lower:
                # Verify it's a reasonable match (not too different)
                if abs(None) < 10:
                    logger.info(f"Fuzzy matched {model_name} to {cached_name}")
                    return capability
                    
        return None
        
    def xǁCapabilityDetectorǁ_fuzzy_match_model__mutmut_9(self, model_name: str) -> Optional[ModelCapabilities]:
        """Attempt fuzzy matching for model names."""
        model_lower = model_name.lower()
        
        # Try partial matches
        for cached_name, capability in self._capability_cache.items():
            cached_lower = cached_name.lower()
            
            # Check if the model name is contained in the cached name
            if model_lower in cached_lower or cached_lower in model_lower:
                # Verify it's a reasonable match (not too different)
                if abs(len(model_lower) + len(cached_lower)) < 10:
                    logger.info(f"Fuzzy matched {model_name} to {cached_name}")
                    return capability
                    
        return None
        
    def xǁCapabilityDetectorǁ_fuzzy_match_model__mutmut_10(self, model_name: str) -> Optional[ModelCapabilities]:
        """Attempt fuzzy matching for model names."""
        model_lower = model_name.lower()
        
        # Try partial matches
        for cached_name, capability in self._capability_cache.items():
            cached_lower = cached_name.lower()
            
            # Check if the model name is contained in the cached name
            if model_lower in cached_lower or cached_lower in model_lower:
                # Verify it's a reasonable match (not too different)
                if abs(len(model_lower) - len(cached_lower)) <= 10:
                    logger.info(f"Fuzzy matched {model_name} to {cached_name}")
                    return capability
                    
        return None
        
    def xǁCapabilityDetectorǁ_fuzzy_match_model__mutmut_11(self, model_name: str) -> Optional[ModelCapabilities]:
        """Attempt fuzzy matching for model names."""
        model_lower = model_name.lower()
        
        # Try partial matches
        for cached_name, capability in self._capability_cache.items():
            cached_lower = cached_name.lower()
            
            # Check if the model name is contained in the cached name
            if model_lower in cached_lower or cached_lower in model_lower:
                # Verify it's a reasonable match (not too different)
                if abs(len(model_lower) - len(cached_lower)) < 11:
                    logger.info(f"Fuzzy matched {model_name} to {cached_name}")
                    return capability
                    
        return None
        
    def xǁCapabilityDetectorǁ_fuzzy_match_model__mutmut_12(self, model_name: str) -> Optional[ModelCapabilities]:
        """Attempt fuzzy matching for model names."""
        model_lower = model_name.lower()
        
        # Try partial matches
        for cached_name, capability in self._capability_cache.items():
            cached_lower = cached_name.lower()
            
            # Check if the model name is contained in the cached name
            if model_lower in cached_lower or cached_lower in model_lower:
                # Verify it's a reasonable match (not too different)
                if abs(len(model_lower) - len(cached_lower)) < 10:
                    logger.info(None)
                    return capability
                    
        return None
        
    
    xǁCapabilityDetectorǁ_fuzzy_match_model__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁCapabilityDetectorǁ_fuzzy_match_model__mutmut_1': xǁCapabilityDetectorǁ_fuzzy_match_model__mutmut_1, 
        'xǁCapabilityDetectorǁ_fuzzy_match_model__mutmut_2': xǁCapabilityDetectorǁ_fuzzy_match_model__mutmut_2, 
        'xǁCapabilityDetectorǁ_fuzzy_match_model__mutmut_3': xǁCapabilityDetectorǁ_fuzzy_match_model__mutmut_3, 
        'xǁCapabilityDetectorǁ_fuzzy_match_model__mutmut_4': xǁCapabilityDetectorǁ_fuzzy_match_model__mutmut_4, 
        'xǁCapabilityDetectorǁ_fuzzy_match_model__mutmut_5': xǁCapabilityDetectorǁ_fuzzy_match_model__mutmut_5, 
        'xǁCapabilityDetectorǁ_fuzzy_match_model__mutmut_6': xǁCapabilityDetectorǁ_fuzzy_match_model__mutmut_6, 
        'xǁCapabilityDetectorǁ_fuzzy_match_model__mutmut_7': xǁCapabilityDetectorǁ_fuzzy_match_model__mutmut_7, 
        'xǁCapabilityDetectorǁ_fuzzy_match_model__mutmut_8': xǁCapabilityDetectorǁ_fuzzy_match_model__mutmut_8, 
        'xǁCapabilityDetectorǁ_fuzzy_match_model__mutmut_9': xǁCapabilityDetectorǁ_fuzzy_match_model__mutmut_9, 
        'xǁCapabilityDetectorǁ_fuzzy_match_model__mutmut_10': xǁCapabilityDetectorǁ_fuzzy_match_model__mutmut_10, 
        'xǁCapabilityDetectorǁ_fuzzy_match_model__mutmut_11': xǁCapabilityDetectorǁ_fuzzy_match_model__mutmut_11, 
        'xǁCapabilityDetectorǁ_fuzzy_match_model__mutmut_12': xǁCapabilityDetectorǁ_fuzzy_match_model__mutmut_12
    }
    
    def _fuzzy_match_model(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁCapabilityDetectorǁ_fuzzy_match_model__mutmut_orig"), object.__getattribute__(self, "xǁCapabilityDetectorǁ_fuzzy_match_model__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _fuzzy_match_model.__signature__ = _mutmut_signature(xǁCapabilityDetectorǁ_fuzzy_match_model__mutmut_orig)
    xǁCapabilityDetectorǁ_fuzzy_match_model__mutmut_orig.__name__ = 'xǁCapabilityDetectorǁ_fuzzy_match_model'


# Global instance
_capability_detector = CapabilityDetector()

def x_get_model_capabilities__mutmut_orig(model_name) -> Optional[ModelCapabilities]:
    """Get capabilities for a model (convenience function)."""
    # Handle both string and tuple inputs
    if isinstance(model_name, tuple):
        provider, actual_model_name = model_name
        # Use the actual model name for capability lookup
        return _capability_detector.get_model_capabilities(actual_model_name)
    else:
        return _capability_detector.get_model_capabilities(model_name)

def x_get_model_capabilities__mutmut_1(model_name) -> Optional[ModelCapabilities]:
    """Get capabilities for a model (convenience function)."""
    # Handle both string and tuple inputs
    if isinstance(model_name, tuple):
        provider, actual_model_name = None
        # Use the actual model name for capability lookup
        return _capability_detector.get_model_capabilities(actual_model_name)
    else:
        return _capability_detector.get_model_capabilities(model_name)

def x_get_model_capabilities__mutmut_2(model_name) -> Optional[ModelCapabilities]:
    """Get capabilities for a model (convenience function)."""
    # Handle both string and tuple inputs
    if isinstance(model_name, tuple):
        provider, actual_model_name = model_name
        # Use the actual model name for capability lookup
        return _capability_detector.get_model_capabilities(None)
    else:
        return _capability_detector.get_model_capabilities(model_name)

def x_get_model_capabilities__mutmut_3(model_name) -> Optional[ModelCapabilities]:
    """Get capabilities for a model (convenience function)."""
    # Handle both string and tuple inputs
    if isinstance(model_name, tuple):
        provider, actual_model_name = model_name
        # Use the actual model name for capability lookup
        return _capability_detector.get_model_capabilities(actual_model_name)
    else:
        return _capability_detector.get_model_capabilities(None)

x_get_model_capabilities__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_model_capabilities__mutmut_1': x_get_model_capabilities__mutmut_1, 
    'x_get_model_capabilities__mutmut_2': x_get_model_capabilities__mutmut_2, 
    'x_get_model_capabilities__mutmut_3': x_get_model_capabilities__mutmut_3
}

def get_model_capabilities(*args, **kwargs):
    result = _mutmut_trampoline(x_get_model_capabilities__mutmut_orig, x_get_model_capabilities__mutmut_mutants, args, kwargs)
    return result 

get_model_capabilities.__signature__ = _mutmut_signature(x_get_model_capabilities__mutmut_orig)
x_get_model_capabilities__mutmut_orig.__name__ = 'x_get_model_capabilities'

def get_tool_calling_models() -> List[ModelCapabilities]:
    """Get all models that support tool calling (convenience function)."""
    return _capability_detector.get_tool_calling_models()

def x_refresh_capabilities__mutmut_orig() -> None:
    """Force refresh of model capabilities (convenience function)."""
    _capability_detector._last_fetch = None
    _capability_detector._refresh_cache_if_needed()

def x_refresh_capabilities__mutmut_1() -> None:
    """Force refresh of model capabilities (convenience function)."""
    _capability_detector._last_fetch = ""
    _capability_detector._refresh_cache_if_needed()

x_refresh_capabilities__mutmut_mutants : ClassVar[MutantDict] = {
'x_refresh_capabilities__mutmut_1': x_refresh_capabilities__mutmut_1
}

def refresh_capabilities(*args, **kwargs):
    result = _mutmut_trampoline(x_refresh_capabilities__mutmut_orig, x_refresh_capabilities__mutmut_mutants, args, kwargs)
    return result 

refresh_capabilities.__signature__ = _mutmut_signature(x_refresh_capabilities__mutmut_orig)
x_refresh_capabilities__mutmut_orig.__name__ = 'x_refresh_capabilities'