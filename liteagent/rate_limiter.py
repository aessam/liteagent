"""
Rate limiting system for LiteAgent with token bucket algorithm.

This module provides intelligent rate limiting across different LLM providers
with per-model, per-tier throttling to prevent API rate limit errors.
"""

import json
import time
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Tuple, Any
from collections import defaultdict

from .utils import logger


@dataclass
class RateLimit:
    """Rate limit configuration for a specific model."""
    rpm: int  # Requests per minute
    tpm: int  # Tokens per minute  
    daily_tokens: Optional[int] = None
    rpd: Optional[int] = None  # Requests per day (for Google)
    notes: str = ""


@dataclass 
class TokenBucket:
    """Token bucket for rate limiting."""
    capacity: float
    tokens: float
    refill_rate: float  # tokens per second
    last_refill: float
    
    def __post_init__(self):
        if self.last_refill == 0:
            self.last_refill = time.time()


class RateLimitError(Exception):
    """Raised when rate limits would be exceeded."""
    def __init__(self, message: str, retry_after: float = 0):
        super().__init__(message)
        self.retry_after = retry_after


class RateLimiter:
    """
    Intelligent rate limiter with token bucket algorithm.
    
    Features:
    - Per-provider, per-model rate limiting
    - Token bucket algorithm for smooth rate limiting
    - Safety buffers to prevent hitting limits
    - Real-time usage tracking
    - Dynamic delay calculation
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize rate limiter.
        
        Args:
            config_path: Path to rate_limits.json config file
        """
        self.config_path = config_path or self._get_default_config_path()
        self.limits: Dict[str, Dict[str, Dict[str, RateLimit]]] = {}
        self.buckets: Dict[str, Dict[str, TokenBucket]] = defaultdict(dict)
        self.request_counts: Dict[str, int] = defaultdict(int)
        self.daily_token_usage: Dict[str, int] = defaultdict(int)
        self.last_reset: Dict[str, float] = defaultdict(lambda: time.time())
        self._lock = threading.Lock()
        
        self._load_config()
        self._setup_buckets()
        
    def _get_default_config_path(self) -> str:
        """Get default config file path."""
        return str(Path(__file__).parent / "config" / "rate_limits.json")
        
    def _load_config(self):
        """Load rate limits configuration."""
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                
            self.safety_multipliers = config.get("safety_multipliers", {
                "rpm_safety": 0.8,
                "tpm_safety": 0.8
            })
            self.default_tiers = config.get("default_tier_assumptions", {})
            
            # Parse rate limits
            for provider, models in config.items():
                if provider.startswith("_") or provider in ["default_tier_assumptions", "safety_multipliers"]:
                    continue
                    
                self.limits[provider] = {}
                for model, tiers in models.items():
                    self.limits[provider][model] = {}
                    for tier, limits in tiers.items():
                        # Handle special cases
                        rpm = limits.get("rpm", 0)
                        tpm = limits.get("tpm", 0)
                        
                        # Handle "unlimited" TPM (set to very high number)
                        if tpm == "unlimited":
                            tpm = 1000000
                            
                        self.limits[provider][model][tier] = RateLimit(
                            rpm=int(rpm * self.safety_multipliers.get("rpm_safety", 0.8)),
                            tpm=int(tpm * self.safety_multipliers.get("tpm_safety", 0.8)) if isinstance(tpm, (int, float)) else tpm,
                            daily_tokens=limits.get("daily_tokens"),
                            rpd=limits.get("rpd"),
                            notes=limits.get("notes", "")
                        )
                        
            logger.info(f"✅ Loaded rate limits for {len(self.limits)} providers")
            
        except FileNotFoundError:
            raise RateLimitError(
                f"Rate limits config not found at {self.config_path}. "
                "Create the config file with model limits before using ForkedAgents."
            )
        except Exception as e:
            raise RateLimitError(f"Failed to load rate limits config: {e}")
            
    def _setup_buckets(self):
        """Initialize token buckets for all configured limits."""
        current_time = time.time()
        
        for provider, models in self.limits.items():
            self.buckets[provider] = {}
            for model, tiers in models.items():
                self.buckets[provider][model] = {}
                for tier, limit in tiers.items():
                    # Create RPM bucket
                    rpm_key = f"{provider}:{model}:{tier}:rpm"
                    self.buckets[provider][model][f"{tier}_rpm"] = TokenBucket(
                        capacity=limit.rpm,
                        tokens=limit.rpm,
                        refill_rate=limit.rpm / 60.0,  # tokens per second
                        last_refill=current_time
                    )
                    
                    # Create TPM bucket
                    tpm_key = f"{provider}:{model}:{tier}:tpm"
                    self.buckets[provider][model][f"{tier}_tpm"] = TokenBucket(
                        capacity=limit.tpm,
                        tokens=limit.tpm,
                        refill_rate=limit.tpm / 60.0,  # tokens per second
                        last_refill=current_time
                    )
    
    def get_rate_limit(self, provider: str, model: str, tier: Optional[str] = None) -> RateLimit:
        """
        Get rate limit for a specific provider/model/tier.
        
        Args:
            provider: Provider name (e.g., 'openai', 'anthropic')
            model: Model name (e.g., 'gpt-4o', 'claude-3-5-sonnet-20241022')
            tier: Tier name (e.g., 'tier_1', 'free'). Uses default if None.
            
        Returns:
            RateLimit: Rate limit configuration
            
        Raises:
            RateLimitError: If model not found in config
        """
        if provider not in self.limits:
            raise RateLimitError(
                f"❌ Provider '{provider}' not found in rate limits config. "
                f"Available providers: {list(self.limits.keys())}"
            )
            
        if model not in self.limits[provider]:
            raise RateLimitError(
                f"❌ Model '{model}' not found for provider '{provider}'. "
                f"Available models: {list(self.limits[provider].keys())}. "
                f"Add this model to {self.config_path} before using it."
            )
            
        if tier is None:
            tier = self.default_tiers.get(provider, list(self.limits[provider][model].keys())[0])
            
        if tier not in self.limits[provider][model]:
            available_tiers = list(self.limits[provider][model].keys())
            raise RateLimitError(
                f"❌ Tier '{tier}' not found for {provider}/{model}. "
                f"Available tiers: {available_tiers}"
            )
            
        return self.limits[provider][model][tier]
    
    def _refill_bucket(self, bucket: TokenBucket) -> None:
        """Refill token bucket based on elapsed time."""
        current_time = time.time()
        elapsed = current_time - bucket.last_refill
        
        # Add tokens based on refill rate
        tokens_to_add = elapsed * bucket.refill_rate
        bucket.tokens = min(bucket.capacity, bucket.tokens + tokens_to_add)
        bucket.last_refill = current_time
    
    def can_proceed(self, provider: str, model: str, tier: Optional[str] = None, 
                   estimated_tokens: int = 1) -> Tuple[bool, float]:
        """
        Check if request can proceed without hitting rate limits.
        
        Args:
            provider: Provider name
            model: Model name  
            tier: Tier name (uses default if None)
            estimated_tokens: Estimated tokens for this request
            
        Returns:
            Tuple of (can_proceed, wait_time_seconds)
        """
        with self._lock:
            # Get rate limits
            try:
                limits = self.get_rate_limit(provider, model, tier)
            except RateLimitError:
                # If no limits configured, allow but warn
                logger.warning(f"⚠️ No rate limits configured for {provider}/{model}")
                return True, 0
                
            if tier is None:
                tier = self.default_tiers.get(provider, list(self.limits[provider][model].keys())[0])
                
            # Get buckets
            if provider not in self.buckets or model not in self.buckets[provider]:
                logger.warning(f"⚠️ No buckets configured for {provider}/{model}")
                return True, 0
                
            rpm_bucket = self.buckets[provider][model].get(f"{tier}_rpm")
            tpm_bucket = self.buckets[provider][model].get(f"{tier}_tpm")
            
            if not rpm_bucket or not tpm_bucket:
                logger.warning(f"⚠️ Missing buckets for {provider}/{model}/{tier}")
                return True, 0
            
            # Refill buckets
            self._refill_bucket(rpm_bucket)
            self._refill_bucket(tpm_bucket)
            
            # Check if we have enough tokens
            rpm_available = rpm_bucket.tokens >= 1
            tpm_available = tpm_bucket.tokens >= estimated_tokens
            
            if rpm_available and tpm_available:
                return True, 0
                
            # Calculate wait time
            wait_times = []
            
            if not rpm_available:
                # Time to get 1 request token
                wait_time = (1 - rpm_bucket.tokens) / rpm_bucket.refill_rate
                wait_times.append(wait_time)
                
            if not tpm_available:
                # Time to get required tokens
                tokens_needed = estimated_tokens - tpm_bucket.tokens
                wait_time = tokens_needed / tpm_bucket.refill_rate
                wait_times.append(wait_time)
                
            return False, max(wait_times)
    
    def consume_tokens(self, provider: str, model: str, tier: Optional[str] = None,
                      actual_tokens: int = 1) -> None:
        """
        Consume tokens after successful request.
        
        Args:
            provider: Provider name
            model: Model name
            tier: Tier name
            actual_tokens: Actual tokens used in the request
        """
        with self._lock:
            if tier is None:
                tier = self.default_tiers.get(provider, list(self.limits[provider][model].keys())[0])
                
            # Get buckets
            if (provider not in self.buckets or 
                model not in self.buckets[provider]):
                return
                
            rpm_bucket = self.buckets[provider][model].get(f"{tier}_rpm")
            tpm_bucket = self.buckets[provider][model].get(f"{tier}_tpm")
            
            if rpm_bucket:
                rpm_bucket.tokens = max(0, rpm_bucket.tokens - 1)
                
            if tpm_bucket:
                tpm_bucket.tokens = max(0, tpm_bucket.tokens - actual_tokens)
                
            # Track usage
            usage_key = f"{provider}:{model}:{tier}"
            self.request_counts[usage_key] += 1
            self.daily_token_usage[usage_key] += actual_tokens
    
    def wait_if_needed(self, provider: str, model: str, tier: Optional[str] = None,
                      estimated_tokens: int = 1) -> float:
        """
        Wait if needed to respect rate limits.
        
        Args:
            provider: Provider name
            model: Model name
            tier: Tier name
            estimated_tokens: Estimated tokens for this request
            
        Returns:
            float: Time waited in seconds
        """
        can_proceed, wait_time = self.can_proceed(provider, model, tier, estimated_tokens)
        
        if not can_proceed and wait_time > 0:
            logger.info(f"🕐 Rate limit reached for {provider}/{model}. Waiting {wait_time:.1f}s...")
            time.sleep(wait_time)
            return wait_time
            
        return 0
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get current usage statistics."""
        with self._lock:
            stats = {
                "request_counts": dict(self.request_counts),
                "daily_token_usage": dict(self.daily_token_usage),
                "bucket_status": {}
            }
            
            for provider, models in self.buckets.items():
                stats["bucket_status"][provider] = {}
                for model, buckets in models.items():
                    stats["bucket_status"][provider][model] = {}
                    for bucket_name, bucket in buckets.items():
                        self._refill_bucket(bucket)
                        stats["bucket_status"][provider][model][bucket_name] = {
                            "tokens": bucket.tokens,
                            "capacity": bucket.capacity,
                            "utilization": (bucket.capacity - bucket.tokens) / bucket.capacity
                        }
            
            return stats


# Global rate limiter instance
_rate_limiter: Optional[RateLimiter] = None


def get_rate_limiter() -> RateLimiter:
    """Get global rate limiter instance."""
    global _rate_limiter
    if _rate_limiter is None:
        _rate_limiter = RateLimiter()
    return _rate_limiter


def reset_rate_limiter():
    """Reset global rate limiter (useful for testing)."""
    global _rate_limiter
    _rate_limiter = None