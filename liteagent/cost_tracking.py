"""
Cost tracking system for LiteAgent with real pricing data.

This module provides accurate cost calculation based on actual token usage
and real-time pricing data from providers.
"""

import json
import time
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import requests
from .utils import logger


@dataclass
class TokenUsage:
    """Represents token usage for a single API call."""
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int = 0  # Made optional with default value
    cached_tokens: int = 0  # For providers that support caching, default to 0
    
    def __post_init__(self):
        if self.total_tokens == 0:
            self.total_tokens = self.prompt_tokens + self.completion_tokens
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TokenUsage':
        """Create TokenUsage from dictionary."""
        return cls(
            prompt_tokens=data.get('prompt_tokens', 0),
            completion_tokens=data.get('completion_tokens', 0),
            total_tokens=data.get('total_tokens', 0),
            cached_tokens=data.get('cached_tokens')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert TokenUsage to dictionary."""
        return asdict(self)


@dataclass
class ModelPricing:
    """Pricing information for a specific model."""
    model_name: str
    provider: str
    input_cost_per_million: float  # Cost per million input tokens
    output_cost_per_million: float  # Cost per million output tokens
    context_window: Optional[int] = None
    supports_caching: bool = False
    cache_discount: float = 0.0  # Discount factor for cached tokens (0.0 = full price, 0.9 = 90% off)
    
    def calculate_cost(self, usage: TokenUsage) -> float:
        """Calculate cost for given token usage."""
        input_cost = (usage.prompt_tokens / 1_000_000) * self.input_cost_per_million
        output_cost = (usage.completion_tokens / 1_000_000) * self.output_cost_per_million
        
        # Apply cache discount if applicable
        if usage.cached_tokens and self.supports_caching:
            cached_cost = (usage.cached_tokens / 1_000_000) * self.input_cost_per_million
            cache_savings = cached_cost * self.cache_discount
            return input_cost + output_cost - cache_savings
        
        return input_cost + output_cost


@dataclass
class CostEvent:
    """Represents a cost event from an API call."""
    timestamp: datetime
    agent_id: str
    agent_name: str
    model_name: str
    provider: str
    usage: TokenUsage
    cost: float
    is_fork: bool = False
    parent_agent_id: Optional[str] = None
    context_id: Optional[str] = None


class PricingDataManager:
    """Manages pricing data from models.dev and other sources."""
    
    def __init__(self, cache_duration_hours: int = 24):
        self.cache_duration_hours = cache_duration_hours
        self._pricing_cache: Dict[str, ModelPricing] = {}
        self._last_update: Optional[datetime] = None
        self._fallback_pricing = self._get_fallback_pricing()
        
    def _get_fallback_pricing(self) -> Dict[str, ModelPricing]:
        """Fallback pricing data when API is unavailable."""
        return {
            # OpenAI Models
            "gpt-4o": ModelPricing("gpt-4o", "openai", 2.50, 10.00, 128000),
            "gpt-4o-mini": ModelPricing("gpt-4o-mini", "openai", 0.15, 0.60, 128000),
            "gpt-4-turbo": ModelPricing("gpt-4-turbo", "openai", 10.00, 30.00, 128000),
            "gpt-3.5-turbo": ModelPricing("gpt-3.5-turbo", "openai", 0.50, 1.50, 16385),
            
            # Anthropic Models (with caching support)
            "claude-3-5-sonnet-20241022": ModelPricing(
                "claude-3-5-sonnet-20241022", "anthropic", 3.00, 15.00, 200000, 
                supports_caching=True, cache_discount=0.90
            ),
            "claude-3-5-haiku-20241022": ModelPricing(
                "claude-3-5-haiku-20241022", "anthropic", 0.80, 4.00, 200000,
                supports_caching=True, cache_discount=0.90
            ),
            "claude-3-opus-20240229": ModelPricing(
                "claude-3-opus-20240229", "anthropic", 15.00, 75.00, 200000,
                supports_caching=True, cache_discount=0.90
            ),
            
            # Groq Models (typically free/very cheap)
            "llama-3.1-70b-versatile": ModelPricing("llama-3.1-70b-versatile", "groq", 0.59, 0.79, 131072),
            "llama-3.1-8b-instant": ModelPricing("llama-3.1-8b-instant", "groq", 0.05, 0.08, 131072),
            "mixtral-8x7b-32768": ModelPricing("mixtral-8x7b-32768", "groq", 0.24, 0.24, 32768),
            
            # Mistral Models
            "mistral-large-latest": ModelPricing("mistral-large-latest", "mistral", 2.00, 6.00, 128000),
            "mistral-small-latest": ModelPricing("mistral-small-latest", "mistral", 0.20, 0.60, 128000),
            
            # DeepSeek Models
            "deepseek-chat": ModelPricing("deepseek-chat", "deepseek", 0.14, 0.28, 64000),
            "deepseek-coder": ModelPricing("deepseek-coder", "deepseek", 0.14, 0.28, 64000),
        }
    
    def _fetch_pricing_data(self) -> Dict[str, ModelPricing]:
        """Fetch pricing data from models.dev API."""
        try:
            response = requests.get("https://models.dev/api.json", timeout=10)
            response.raise_for_status()
            data = response.json()
            
            pricing_data = {}
            for model_data in data.get("models", []):
                if "pricing" in model_data:
                    pricing = model_data["pricing"]
                    model_name = model_data.get("name", "")
                    provider = model_data.get("provider", "").lower()
                    
                    # Extract pricing information
                    input_cost = pricing.get("input", 0) * 1000  # Convert to per million
                    output_cost = pricing.get("output", 0) * 1000  # Convert to per million
                    context_window = model_data.get("context_window")
                    
                    # Determine cache support (mainly Anthropic for now)
                    supports_caching = provider == "anthropic" and "claude-3" in model_name.lower()
                    cache_discount = 0.90 if supports_caching else 0.0
                    
                    pricing_data[model_name] = ModelPricing(
                        model_name=model_name,
                        provider=provider,
                        input_cost_per_million=input_cost,
                        output_cost_per_million=output_cost,
                        context_window=context_window,
                        supports_caching=supports_caching,
                        cache_discount=cache_discount
                    )
            
            logger.info(f"Loaded pricing data for {len(pricing_data)} models from models.dev")
            return pricing_data
            
        except Exception as e:
            logger.warning(f"Failed to fetch pricing data from models.dev: {e}")
            return {}
    
    def get_model_pricing(self, model_name: str) -> Optional[ModelPricing]:
        """Get pricing for a specific model."""
        # Check if cache needs refresh
        if (self._last_update is None or 
            datetime.now() - self._last_update > timedelta(hours=self.cache_duration_hours)):
            self._refresh_pricing_data()
        
        # Try exact match first
        if model_name in self._pricing_cache:
            return self._pricing_cache[model_name]
        
        # Try fallback pricing
        if model_name in self._fallback_pricing:
            return self._fallback_pricing[model_name]
        
        # Try partial matches for model families
        for cached_model in self._pricing_cache:
            if self._models_match(model_name, cached_model):
                return self._pricing_cache[cached_model]
        
        return None
    
    def _models_match(self, model1: str, model2: str) -> bool:
        """Check if two model names likely refer to the same model family."""
        # Simple heuristic - could be improved
        model1_base = model1.lower().split('-')[0]
        model2_base = model2.lower().split('-')[0]
        return model1_base == model2_base
    
    def _refresh_pricing_data(self):
        """Refresh pricing data from external sources."""
        try:
            fresh_data = self._fetch_pricing_data()
            if fresh_data:
                self._pricing_cache.update(fresh_data)
            self._last_update = datetime.now()
        except Exception as e:
            logger.error(f"Error refreshing pricing data: {e}")


class CostTracker:
    """Tracks costs for agent operations."""
    
    def __init__(self):
        self.pricing_manager = PricingDataManager()
        self.cost_events: List[CostEvent] = []
        self.events: List[Dict[str, Any]] = []  # For backward compatibility with dict events
        self.total_cost = 0.0
        self.session_start_time = time.time()
        
    def record_usage(self, 
                    agent_id: str,
                    agent_name: str, 
                    model_name: str,
                    provider: str,
                    usage: TokenUsage,
                    is_fork: bool = False,
                    parent_agent_id: Optional[str] = None,
                    context_id: Optional[str] = None) -> float:
        """Record token usage and calculate cost."""
        
        pricing = self.pricing_manager.get_model_pricing(model_name)
        if not pricing:
            logger.warning(f"No pricing data found for model: {model_name}")
            return 0.0
        
        cost = pricing.calculate_cost(usage)
        
        event = CostEvent(
            timestamp=datetime.now(),
            agent_id=agent_id,
            agent_name=agent_name,
            model_name=model_name,
            provider=provider,
            usage=usage,
            cost=cost,
            is_fork=is_fork,
            parent_agent_id=parent_agent_id,
            context_id=context_id
        )
        
        self.cost_events.append(event)
        self.total_cost += cost
        
        logger.debug(f"Cost recorded: ${cost:.6f} for {usage.total_tokens} tokens ({model_name})")
        return cost
    
    def track_request(self, model: str, provider: str, usage: TokenUsage, 
                      cost: Optional[float] = None,
                      metadata: Optional[Dict[str, Any]] = None) -> float:
        """Track a request (alias for record_usage for backward compatibility)."""
        agent_id = metadata.get('agent_id', 'default') if metadata else 'default'
        agent_name = metadata.get('agent_name', 'default') if metadata else 'default'
        
        if cost is not None:
            # If cost is provided, create event dict directly for backward compatibility
            event = {
                "timestamp": datetime.now(),
                "agent_id": agent_id,
                "agent_name": agent_name,
                "model": model,
                "provider": provider,
                "usage": {
                    "prompt_tokens": usage.prompt_tokens,
                    "completion_tokens": usage.completion_tokens,
                    "total_tokens": usage.total_tokens,
                    "cached_tokens": usage.cached_tokens
                },
                "cost": cost,
                "is_fork": metadata.get('is_fork', False) if metadata else False,
                "parent_agent_id": metadata.get('parent_agent_id') if metadata else None,
                "context_id": metadata.get('context_id') if metadata else None,
                "metadata": metadata if metadata else {}
            }
            # Also create CostEvent for internal consistency
            cost_event = CostEvent(
                timestamp=event["timestamp"],
                agent_id=agent_id,
                agent_name=agent_name,
                model_name=model,
                provider=provider,
                usage=usage,
                cost=cost,
                is_fork=event["is_fork"],
                parent_agent_id=event["parent_agent_id"],
                context_id=event["context_id"]
            )
            self.cost_events.append(cost_event)
            self.events.append(event)  # For backward compatibility
            self.total_cost += cost
            return cost
        else:
            # Use normal record_usage flow
            return self.record_usage(
                agent_id=agent_id,
                agent_name=agent_name,
                model_name=model,
                provider=provider,
                usage=usage,
                is_fork=metadata.get('is_fork', False) if metadata else False,
                parent_agent_id=metadata.get('parent_agent_id') if metadata else None,
                context_id=metadata.get('context_id') if metadata else None
            )
    
    def get_total_cost(self) -> float:
        """Get total cost tracked."""
        return round(self.total_cost, 10)  # Round to avoid floating point precision issues
    
    def get_cost_by_model(self) -> Dict[str, Dict[str, Any]]:
        """Get cost breakdown by model."""
        by_model = {}
        for event in self.cost_events:
            model = event.model_name
            if model not in by_model:
                by_model[model] = {
                    "total_cost": 0.0,
                    "request_count": 0,
                    "total_tokens": 0
                }
            by_model[model]["total_cost"] += event.cost
            by_model[model]["request_count"] += 1
            by_model[model]["total_tokens"] += event.usage.total_tokens
        
        # Round total_cost for each model to avoid floating point precision issues
        for model_data in by_model.values():
            model_data["total_cost"] = round(model_data["total_cost"], 10)
        
        return by_model
    
    def get_cost_by_provider(self) -> Dict[str, Dict[str, Any]]:
        """Get cost breakdown by provider."""
        by_provider = {}
        for event in self.cost_events:
            provider = event.provider
            if provider not in by_provider:
                by_provider[provider] = {
                    "total_cost": 0.0,
                    "request_count": 0
                }
            by_provider[provider]["total_cost"] += event.cost
            by_provider[provider]["request_count"] += 1
        
        # Round total_cost for each provider to avoid floating point precision issues
        for provider_data in by_provider.values():
            provider_data["total_cost"] = round(provider_data["total_cost"], 10)
        
        return by_provider
    
    def reset(self) -> None:
        """Reset the cost tracker."""
        self.cost_events.clear()
        self.events.clear()
        self.total_cost = 0.0
        self.session_start_time = time.time()
    
    def get_summary(self) -> Dict[str, Any]:
        """Get comprehensive cost summary with expected fields."""
        if not self.cost_events:
            return {
                "total_cost": 0.0, 
                "total_requests": 0,
                "total_tokens": 0, 
                "cached_tokens": 0,
                "providers": [], 
                "models": []
            }
        
        # Calculate totals
        total_tokens = sum(event.usage.total_tokens for event in self.cost_events)
        cached_tokens = sum(event.usage.cached_tokens for event in self.cost_events)
        
        # Get unique providers and models in insertion order
        providers = []
        models = []
        seen_providers = set()
        seen_models = set()
        
        for event in self.cost_events:
            if event.provider not in seen_providers:
                providers.append(event.provider)
                seen_providers.add(event.provider)
            if event.model_name not in seen_models:
                models.append(event.model_name)
                seen_models.add(event.model_name)
        
        return {
            "total_cost": round(self.total_cost, 10),  # Round for float precision
            "total_requests": len(self.cost_events),
            "total_tokens": total_tokens,
            "cached_tokens": cached_tokens,
            "providers": providers,
            "models": models
        }
    
    def get_cost_summary(self) -> Dict[str, Any]:
        """Get comprehensive cost summary."""
        if not self.cost_events:
            return {"total_cost": 0.0, "total_tokens": 0, "events": 0}
        
        # Calculate totals
        total_tokens = sum(event.usage.total_tokens for event in self.cost_events)
        total_prompt_tokens = sum(event.usage.prompt_tokens for event in self.cost_events)
        total_completion_tokens = sum(event.usage.completion_tokens for event in self.cost_events)
        
        # Group by model
        by_model = {}
        for event in self.cost_events:
            model = event.model_name
            if model not in by_model:
                by_model[model] = {"cost": 0.0, "tokens": 0, "calls": 0}
            by_model[model]["cost"] += event.cost
            by_model[model]["tokens"] += event.usage.total_tokens
            by_model[model]["calls"] += 1
        
        # Fork vs parent costs
        fork_cost = sum(event.cost for event in self.cost_events if event.is_fork)
        parent_cost = sum(event.cost for event in self.cost_events if not event.is_fork)
        
        return {
            "total_cost": self.total_cost,
            "total_tokens": total_tokens,
            "prompt_tokens": total_prompt_tokens,
            "completion_tokens": total_completion_tokens,
            "events": len(self.cost_events),
            "by_model": by_model,
            "fork_cost": fork_cost,
            "parent_cost": parent_cost,
            "average_cost_per_token": self.total_cost / total_tokens if total_tokens > 0 else 0
        }
    
    def calculate_traditional_cost(self, fork_count: int) -> float:
        """Calculate what the cost would be without forking (for comparison)."""
        # For traditional approach, each fork would need to send the full context
        parent_events = [e for e in self.cost_events if not e.is_fork]
        if not parent_events:
            return 0.0
        
        # Estimate the cost if each fork had to send the full parent context
        parent_context_cost = sum(e.cost for e in parent_events)
        estimated_traditional_cost = parent_context_cost * (fork_count + 1)  # +1 for parent
        
        return estimated_traditional_cost
    
    def get_savings_report(self) -> Dict[str, Any]:
        """Generate a detailed savings report for forked vs traditional approach."""
        summary = self.get_cost_summary()
        fork_events = [e for e in self.cost_events if e.is_fork]
        
        if not fork_events:
            return {"message": "No fork events recorded"}
        
        fork_count = len(set(e.agent_id for e in fork_events))
        traditional_cost = self.calculate_traditional_cost(fork_count)
        actual_cost = self.total_cost
        savings = traditional_cost - actual_cost
        savings_percent = (savings / traditional_cost * 100) if traditional_cost > 0 else 0
        
        return {
            "actual_cost": actual_cost,
            "traditional_cost": traditional_cost,
            "savings": savings,
            "savings_percent": savings_percent,
            "fork_count": fork_count,
            "total_tokens": summary["total_tokens"],
            "cost_per_token": summary["average_cost_per_token"]
        }


# Global cost tracker instance
_global_cost_tracker = CostTracker()


def get_cost_tracker() -> CostTracker:
    """Get the global cost tracker instance."""
    return _global_cost_tracker


def record_agent_cost(agent_id: str, 
                     agent_name: str,
                     model_name: str, 
                     provider: str,
                     usage: TokenUsage,
                     is_fork: bool = False,
                     parent_agent_id: Optional[str] = None,
                     context_id: Optional[str] = None) -> float:
    """Convenience function to record cost using global tracker."""
    return _global_cost_tracker.record_usage(
        agent_id, agent_name, model_name, provider, usage, 
        is_fork, parent_agent_id, context_id
    )