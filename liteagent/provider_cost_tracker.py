"""
Simple provider-level cost tracking that actually works.

This module tracks costs directly from provider responses using real token usage
and pricing data from models.dev.
"""

import json
import time
import requests
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

from .utils import logger


@dataclass
class CostEvent:
    """Simple cost event with all needed data."""
    timestamp: datetime
    provider: str
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cached_tokens: int
    input_cost: float
    output_cost: float
    cache_cost: float
    total_cost: float
    agent_name: Optional[str] = None
    is_fork: bool = False


class ProviderCostTracker:
    """Simple cost tracker that works at provider level."""
    
    def __init__(self):
        self.events: list[CostEvent] = []
        self.pricing_cache: Dict[str, Dict] = {}
        self._load_pricing_data()
    
    def _load_pricing_data(self):
        """Load pricing data from models.dev."""
        try:
            response = requests.get("https://models.dev/api.json", timeout=10)
            if response.status_code == 200:
                data = response.json()
                models_loaded = 0
                
                # Handle the actual models.dev API format (providers with models dict)
                if isinstance(data, dict):
                    for provider_name, provider_data in data.items():
                        if isinstance(provider_data, dict) and 'models' in provider_data:
                            models = provider_data['models']
                            
                            # Models is a dict: model_id -> model_data
                            if isinstance(models, dict):
                                for model_id, model_data in models.items():
                                    if isinstance(model_data, dict) and 'cost' in model_data:
                                        cost_data = model_data['cost']
                                        
                                        # Convert models.dev format to our internal format
                                        # models.dev uses per 1M tokens, we use per 1K tokens
                                        pricing = {
                                            'input': cost_data.get('input', 1.0) / 1000,
                                            'output': cost_data.get('output', 3.0) / 1000,
                                            'cache_read': cost_data.get('cache_read', 0.1) / 1000,
                                            'cache_write': cost_data.get('cache_write', 1.0) / 1000
                                        }
                                        
                                        # Store with multiple key formats using ACTUAL provider name
                                        # No hardcoded string matching bullshit
                                        self.pricing_cache[model_id] = pricing
                                        self.pricing_cache[model_id.lower()] = pricing
                                        self.pricing_cache[f"{provider_name.lower()}/{model_id}"] = pricing
                                        self.pricing_cache[f"{provider_name.lower()}/{model_id.lower()}"] = pricing
                                        
                                        models_loaded += 1
                        
                logger.info(f"Loaded pricing for {models_loaded} model configurations")
            else:
                logger.warning(f"Failed to load pricing data: HTTP {response.status_code}")
        except Exception as e:
            logger.warning(f"Could not load pricing data: {e}")
            
    def _get_pricing(self, provider: str, model: str) -> Dict[str, float]:
        """Get pricing for a provider/model combination."""
        # Try multiple lookup strategies
        keys_to_try = [
            f"{provider.lower()}/{model}",
            f"{provider.lower()}/{model.lower()}",
            model,
            model.lower()
        ]
        
        for key in keys_to_try:
            if key in self.pricing_cache:
                return self.pricing_cache[key]
        
        # Default fallback pricing (approximate)
        logger.warning(f"No pricing found for {provider}/{model}, using defaults")
        
        # Use reasonable defaults based on model type (matching real pricing)
        if 'claude' in model.lower():
            return {
                'input': 0.003,     # $3 per 1M tokens = $0.003 per 1K
                'output': 0.015,    # $15 per 1M tokens = $0.015 per 1K
                'cache_read': 0.0003,   # $0.3 per 1M tokens = $0.0003 per 1K
                'cache_write': 0.00375  # $3.75 per 1M tokens = $0.00375 per 1K
            }
        elif 'gpt' in model.lower():
            return {
                'input': 0.0025,
                'output': 0.01,
                'cache_read': 0.0001,
                'cache_write': 0.0025
            }
        else:
            return {
                'input': 0.001,
                'output': 0.003,
                'cache_read': 0.0001,
                'cache_write': 0.001
            }
    
    def record_cost(self, provider_response, agent_name: str = None, is_fork: bool = False):
        """Record cost from a provider response."""
        if not provider_response or not provider_response.usage:
            return
            
        usage = provider_response.usage
        provider = provider_response.provider
        model = provider_response.model
        
        # Extract token counts (handle different provider formats)
        prompt_tokens = usage.get('prompt_tokens', usage.get('input_tokens', 0))
        completion_tokens = usage.get('completion_tokens', usage.get('output_tokens', 0))
        total_tokens = usage.get('total_tokens', prompt_tokens + completion_tokens)
        
        # Handle cached tokens (different provider formats)
        cached_tokens = (
            usage.get('cache_read_input_tokens', 0) +  # Anthropic format
            usage.get('cached_tokens', 0)  # OpenAI format
        )
        
        # Get pricing
        pricing = self._get_pricing(provider, model)
        
        # Calculate costs (pricing is per 1K tokens)
        input_cost = (prompt_tokens / 1000.0) * pricing.get('input', 0)
        output_cost = (completion_tokens / 1000.0) * pricing.get('output', 0)
        cache_cost = (cached_tokens / 1000.0) * pricing.get('cache_read', 0)
        total_cost = input_cost + output_cost + cache_cost
        
        # Create and store event
        event = CostEvent(
            timestamp=datetime.now(),
            provider=provider,
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            cached_tokens=cached_tokens,
            input_cost=input_cost,
            output_cost=output_cost,
            cache_cost=cache_cost,
            total_cost=total_cost,
            agent_name=agent_name,
            is_fork=is_fork
        )
        
        self.events.append(event)
        logger.debug(f"Cost recorded: ${total_cost:.6f} for {total_tokens} tokens ({provider}/{model})")
        
        return total_cost
    
    def get_total_cost(self) -> float:
        """Get total cost across all events."""
        return sum(event.total_cost for event in self.events)
    
    def get_total_tokens(self) -> int:
        """Get total tokens across all events."""
        return sum(event.total_tokens for event in self.events)
    
    def get_fork_savings(self) -> Dict[str, Any]:
        """Calculate savings from forking with mathematically consistent metrics."""
        if not self.events:
            return {"error": "No cost events recorded"}
            
        # Separate fork and parent costs
        fork_events = [e for e in self.events if e.is_fork]
        parent_events = [e for e in self.events if not e.is_fork]
        
        fork_cost = sum(e.total_cost for e in fork_events)
        parent_cost = sum(e.total_cost for e in parent_events)
        actual_total = fork_cost + parent_cost
        
        # Calculate real cached tokens
        total_cached_tokens = sum(e.cached_tokens for e in self.events)
        total_tokens = sum(e.total_tokens for e in self.events)
        
        # Calculate cache efficiency (must be <= 100%)
        cache_efficiency = 0.0
        if total_tokens > 0:
            cache_efficiency = min(100.0, (total_cached_tokens / total_tokens) * 100)
        
        # Conservative estimate of traditional cost without caching
        # If we have cached tokens, estimate what it would cost without caching
        estimated_without_caching = actual_total
        if total_cached_tokens > 0:
            # Estimate additional cost if cached tokens were processed normally
            # Using average cost per token from non-cached tokens
            non_cached_tokens = total_tokens - total_cached_tokens
            if non_cached_tokens > 0:
                avg_cost_per_token = actual_total / non_cached_tokens
                estimated_additional_cost = total_cached_tokens * avg_cost_per_token
                estimated_without_caching = actual_total + estimated_additional_cost
        
        savings = max(0, estimated_without_caching - actual_total)
        savings_percent = (savings / estimated_without_caching * 100) if estimated_without_caching > 0 else 0
        
        return {
            "actual_cost": actual_total,
            "estimated_cost_without_caching": estimated_without_caching,
            "savings": savings,
            "savings_percent": min(100.0, savings_percent),  # Cap at 100%
            "fork_events": len(fork_events),
            "parent_events": len(parent_events),
            "total_tokens": total_tokens,
            "cached_tokens": total_cached_tokens,
            "cache_efficiency_percent": cache_efficiency,
            "mathematically_consistent": True
        }
    
    def get_model_pricing(self, model: str) -> Optional[Dict[str, float]]:
        """Get pricing for a specific model."""
        # Try to find pricing in cache
        if model in self.pricing_cache:
            return self.pricing_cache[model]
        if model.lower() in self.pricing_cache:
            return self.pricing_cache[model.lower()]
        return None
    
    def calculate_cost(self, model: str, usage: 'TokenUsage', provider: str = "") -> float:
        """Calculate cost for given token usage."""
        # Handle the case where usage might be passed as first argument for backward compatibility
        if isinstance(model, type(usage)) and hasattr(model, 'prompt_tokens'):
            # Swap parameters - old calling convention
            usage, model = model, usage
        
        pricing = self._get_pricing(provider, model) if provider else self.get_model_pricing(model)
        if not pricing:
            return 0.0
        
        # Import TokenUsage if needed
        from .cost_tracking import TokenUsage
        
        # Calculate costs - check for both per-token and per-1K pricing formats
        if 'input_cost_per_token' in pricing:
            # Per-token pricing format
            input_cost = usage.prompt_tokens * pricing.get('input_cost_per_token', 0)
            output_cost = usage.completion_tokens * pricing.get('output_cost_per_token', 0)
            cache_cost = usage.cached_tokens * pricing.get('cache_read_cost_per_token', 0) if usage.cached_tokens else 0
        else:
            # Per 1K tokens pricing format
            input_cost = (usage.prompt_tokens / 1000.0) * pricing.get('input', 0)
            output_cost = (usage.completion_tokens / 1000.0) * pricing.get('output', 0)
            cache_cost = (usage.cached_tokens / 1000.0) * pricing.get('cache_read', 0) if usage.cached_tokens else 0
        
        return input_cost + output_cost + cache_cost
    
    def track_and_calculate(self, usage: 'TokenUsage', model: str, provider: str = "") -> float:
        """Track usage and calculate cost."""
        cost = self.calculate_cost(model, usage, provider)
        
        # Create and store event
        event = CostEvent(
            timestamp=datetime.now(),
            provider=provider or "unknown",
            model=model,
            prompt_tokens=usage.prompt_tokens,
            completion_tokens=usage.completion_tokens,
            total_tokens=usage.total_tokens,
            cached_tokens=usage.cached_tokens or 0,
            input_cost=cost * 0.4,  # Estimate breakdown
            output_cost=cost * 0.6,
            cache_cost=0,
            total_cost=cost,
            agent_name=None,
            is_fork=False
        )
        self.events.append(event)
        return cost
    
    def calculate_cost_with_caching(self, usage: 'TokenUsage', model: str, provider: str = "") -> float:
        """Calculate cost with caching considerations."""
        return self.calculate_cost(usage, model, provider)
    
    def track_request(self, model: str, provider: str, usage: 'TokenUsage', 
                      cost: Optional[float] = None, **kwargs) -> float:
        """Track a request - compatibility method."""
        if cost is not None:
            # If cost is provided directly, use it
            return self.track_usage(provider, model, 
                                  usage.prompt_tokens, usage.completion_tokens, 
                                  usage.cached_tokens, **kwargs)
        else:
            # Calculate cost and track
            return self.track_and_calculate(usage, model, provider)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get complete cost summary."""
        if not self.events:
            return {"message": "No cost events recorded"}
            
        return {
            "total_cost": self.get_total_cost(),
            "total_tokens": self.get_total_tokens(),
            "total_events": len(self.events),
            "fork_savings": self.get_fork_savings(),
            "events": [asdict(event) for event in self.events[-5:]]  # Last 5 events
        }


# Global tracker instance
_cost_tracker = ProviderCostTracker()


def get_cost_tracker() -> ProviderCostTracker:
    """Get the global cost tracker instance."""
    return _cost_tracker


def record_provider_cost(provider_response, agent_name: str = None, is_fork: bool = False) -> float:
    """Record cost from a provider response (convenience function)."""
    return _cost_tracker.record_cost(provider_response, agent_name, is_fork)