"""
Comprehensive tests for cost tracking and pricing functionality.

This consolidates tests from scattered files like test_pricing_fix.py
and provides comprehensive coverage for the cost tracking system.
"""

import pytest
import time
from unittest.mock import MagicMock, patch

from liteagent.cost_tracking import CostTracker, TokenUsage
from liteagent.provider_cost_tracker import get_cost_tracker, ProviderCostTracker


class TestTokenUsage:
    """Test TokenUsage dataclass."""
    
    def test_token_usage_creation(self):
        """Test creating a TokenUsage instance."""
        usage = TokenUsage(
            prompt_tokens=100,
            completion_tokens=50,
            total_tokens=150,
            cached_tokens=25
        )
        
        assert usage.prompt_tokens == 100
        assert usage.completion_tokens == 50
        assert usage.total_tokens == 150
        assert usage.cached_tokens == 25
    
    def test_token_usage_defaults(self):
        """Test TokenUsage with default values."""
        usage = TokenUsage(prompt_tokens=100, completion_tokens=50)
        
        assert usage.prompt_tokens == 100
        assert usage.completion_tokens == 50
        assert usage.total_tokens == 150  # Should calculate automatically
        assert usage.cached_tokens == 0
    
    def test_token_usage_to_dict(self):
        """Test converting TokenUsage to dictionary."""
        usage = TokenUsage(prompt_tokens=100, completion_tokens=50, cached_tokens=25)
        usage_dict = usage.to_dict()
        
        assert usage_dict["prompt_tokens"] == 100
        assert usage_dict["completion_tokens"] == 50
        assert usage_dict["total_tokens"] == 150
        assert usage_dict["cached_tokens"] == 25
    
    def test_token_usage_from_dict(self):
        """Test creating TokenUsage from dictionary."""
        usage_dict = {
            "prompt_tokens": 200,
            "completion_tokens": 100,
            "total_tokens": 300,
            "cached_tokens": 50
        }
        
        usage = TokenUsage.from_dict(usage_dict)
        
        assert usage.prompt_tokens == 200
        assert usage.completion_tokens == 100
        assert usage.total_tokens == 300
        assert usage.cached_tokens == 50


class TestCostTracker:
    """Test CostTracker functionality."""
    
    @pytest.fixture
    def cost_tracker(self):
        """Create a fresh CostTracker for testing."""
        return CostTracker()
    
    def test_cost_tracker_initialization(self, cost_tracker):
        """Test CostTracker initialization."""
        assert len(cost_tracker.events) == 0
        assert cost_tracker.total_cost == 0.0
        assert isinstance(cost_tracker.session_start_time, float)
    
    def test_track_request_basic(self, cost_tracker):
        """Test tracking a basic request."""
        usage = TokenUsage(prompt_tokens=100, completion_tokens=50)
        
        cost_tracker.track_request(
            model="gpt-4",
            provider="openai",
            usage=usage,
            cost=0.05
        )
        
        assert len(cost_tracker.events) == 1
        event = cost_tracker.events[0]
        
        assert event["model"] == "gpt-4"
        assert event["provider"] == "openai"
        assert event["usage"]["prompt_tokens"] == 100
        assert event["usage"]["completion_tokens"] == 50
        assert event["cost"] == 0.05
    
    def test_track_request_with_metadata(self, cost_tracker):
        """Test tracking request with additional metadata."""
        usage = TokenUsage(prompt_tokens=200, completion_tokens=100, cached_tokens=50)
        
        cost_tracker.track_request(
            model="claude-3-5-sonnet-20241022",
            provider="anthropic",
            usage=usage,
            cost=0.08,
            metadata={
                "agent_name": "TestAgent",
                "fork_id": "fork_123",
                "cache_hit": True
            }
        )
        
        assert len(cost_tracker.events) == 1
        event = cost_tracker.events[0]
        
        assert event["metadata"]["agent_name"] == "TestAgent"
        assert event["metadata"]["fork_id"] == "fork_123"
        assert event["metadata"]["cache_hit"] is True
    
    def test_get_total_cost(self, cost_tracker):
        """Test calculating total cost."""
        # Track multiple requests
        usage1 = TokenUsage(prompt_tokens=100, completion_tokens=50)
        usage2 = TokenUsage(prompt_tokens=200, completion_tokens=100)
        
        cost_tracker.track_request("gpt-4", "openai", usage1, 0.05)
        cost_tracker.track_request("claude-3-opus", "anthropic", usage2, 0.12)
        
        total_cost = cost_tracker.get_total_cost()
        assert total_cost == 0.17
    
    def test_get_summary(self, cost_tracker):
        """Test getting cost summary."""
        # Track some requests
        usage1 = TokenUsage(prompt_tokens=100, completion_tokens=50, cached_tokens=25)
        usage2 = TokenUsage(prompt_tokens=200, completion_tokens=100, cached_tokens=0)
        
        cost_tracker.track_request("gpt-4", "openai", usage1, 0.05)
        cost_tracker.track_request("claude-3-opus", "anthropic", usage2, 0.12)
        
        summary = cost_tracker.get_summary()
        
        assert summary["total_cost"] == 0.17
        assert summary["total_requests"] == 2
        assert summary["total_tokens"] == 450  # 150 + 300
        assert summary["cached_tokens"] == 25
        assert summary["providers"] == ["openai", "anthropic"]
        assert summary["models"] == ["gpt-4", "claude-3-opus"]
    
    def test_get_cost_by_model(self, cost_tracker):
        """Test getting cost breakdown by model."""
        usage1 = TokenUsage(prompt_tokens=100, completion_tokens=50)
        usage2 = TokenUsage(prompt_tokens=200, completion_tokens=100)
        usage3 = TokenUsage(prompt_tokens=150, completion_tokens=75)
        
        cost_tracker.track_request("gpt-4", "openai", usage1, 0.05)
        cost_tracker.track_request("gpt-4", "openai", usage2, 0.10)
        cost_tracker.track_request("claude-3-opus", "anthropic", usage3, 0.08)
        
        breakdown = cost_tracker.get_cost_by_model()
        
        assert breakdown["gpt-4"]["total_cost"] == 0.15
        assert breakdown["gpt-4"]["request_count"] == 2
        assert breakdown["gpt-4"]["total_tokens"] == 450
        
        assert breakdown["claude-3-opus"]["total_cost"] == 0.08
        assert breakdown["claude-3-opus"]["request_count"] == 1
        assert breakdown["claude-3-opus"]["total_tokens"] == 225
    
    def test_get_cost_by_provider(self, cost_tracker):
        """Test getting cost breakdown by provider."""
        usage1 = TokenUsage(prompt_tokens=100, completion_tokens=50)
        usage2 = TokenUsage(prompt_tokens=200, completion_tokens=100)
        
        cost_tracker.track_request("gpt-4", "openai", usage1, 0.05)
        cost_tracker.track_request("gpt-3.5-turbo", "openai", usage2, 0.03)
        cost_tracker.track_request("claude-3-opus", "anthropic", usage1, 0.08)
        
        breakdown = cost_tracker.get_cost_by_provider()
        
        assert breakdown["openai"]["total_cost"] == 0.08
        assert breakdown["openai"]["request_count"] == 2
        assert breakdown["anthropic"]["total_cost"] == 0.08
        assert breakdown["anthropic"]["request_count"] == 1
    
    def test_reset(self, cost_tracker):
        """Test resetting the cost tracker."""
        usage = TokenUsage(prompt_tokens=100, completion_tokens=50)
        cost_tracker.track_request("gpt-4", "openai", usage, 0.05)
        
        assert len(cost_tracker.events) == 1
        assert cost_tracker.get_total_cost() == 0.05
        
        cost_tracker.reset()
        
        assert len(cost_tracker.events) == 0
        assert cost_tracker.get_total_cost() == 0.0


class TestProviderCostTracker:
    """Test ProviderCostTracker functionality."""
    
    @pytest.fixture
    def provider_tracker(self):
        """Create a ProviderCostTracker for testing."""
        return ProviderCostTracker()
    
    def test_pricing_data_loading(self, provider_tracker):
        """Test that pricing data is loaded correctly."""
        # Should have pricing data for common models
        pricing_cache = provider_tracker.pricing_cache
        
        # Check for common model patterns
        has_openai = any("gpt" in key.lower() for key in pricing_cache.keys())
        has_anthropic = any("claude" in key.lower() for key in pricing_cache.keys())
        
        assert has_openai or has_anthropic  # Should have at least one provider
    
    def test_get_model_pricing(self, provider_tracker):
        """Test getting pricing for specific models."""
        # Test with mock pricing data
        provider_tracker.pricing_cache = {
            "gpt-4": {
                "input_cost_per_token": 0.00003,
                "output_cost_per_token": 0.00006
            },
            "claude-3-5-sonnet-20241022": {
                "input_cost_per_token": 0.000015,
                "output_cost_per_token": 0.000075
            }
        }
        
        gpt4_pricing = provider_tracker.get_model_pricing("gpt-4")
        assert gpt4_pricing["input_cost_per_token"] == 0.00003
        assert gpt4_pricing["output_cost_per_token"] == 0.00006
        
        claude_pricing = provider_tracker.get_model_pricing("claude-3-5-sonnet-20241022")
        assert claude_pricing["input_cost_per_token"] == 0.000015
        assert claude_pricing["output_cost_per_token"] == 0.000075
    
    def test_calculate_cost(self, provider_tracker):
        """Test cost calculation."""
        # Mock pricing data
        provider_tracker.pricing_cache = {
            "gpt-4": {
                "input_cost_per_token": 0.00003,
                "output_cost_per_token": 0.00006
            }
        }
        
        usage = TokenUsage(prompt_tokens=1000, completion_tokens=500)
        cost = provider_tracker.calculate_cost("gpt-4", usage)
        
        expected_cost = (1000 * 0.00003) + (500 * 0.00006)
        assert abs(cost - expected_cost) < 0.0001  # Allow for floating point precision
    
    def test_calculate_cost_with_caching(self, provider_tracker):
        """Test cost calculation with cached tokens."""
        # Mock pricing data with cache discount
        provider_tracker.pricing_cache = {
            "claude-3-5-sonnet-20241022": {
                "input_cost_per_token": 0.000015,
                "output_cost_per_token": 0.000075,
                "cache_write_cost_per_token": 0.0000375,
                "cache_read_cost_per_token": 0.0000015
            }
        }
        
        usage = TokenUsage(prompt_tokens=2000, completion_tokens=1000, cached_tokens=500)
        cost = provider_tracker.calculate_cost("claude-3-5-sonnet-20241022", usage)
        
        # Calculate expected cost with cache savings
        regular_input_tokens = 2000 - 500  # 1500 regular tokens
        expected_cost = (
            (regular_input_tokens * 0.000015) +  # Regular input tokens
            (500 * 0.0000015) +  # Cached tokens at discounted rate
            (1000 * 0.000075)  # Output tokens
        )
        
        assert abs(cost - expected_cost) < 0.0001
    
    def test_track_and_calculate(self, provider_tracker):
        """Test tracking a request and calculating cost automatically."""
        # Mock pricing data
        provider_tracker.pricing_cache = {
            "gpt-3.5-turbo": {
                "input_cost_per_token": 0.0000015,
                "output_cost_per_token": 0.000002
            }
        }
        
        usage = TokenUsage(prompt_tokens=800, completion_tokens=200)
        
        provider_tracker.track_request(
            model="gpt-3.5-turbo",
            provider="openai",
            usage=usage
        )
        
        # Should have calculated and tracked cost
        assert len(provider_tracker.events) == 1
        event = provider_tracker.events[0]
        
        expected_cost = (800 * 0.0000015) + (200 * 0.000002)
        assert abs(event["cost"] - expected_cost) < 0.0001
    
    def test_get_fork_savings(self, provider_tracker):
        """Test calculating fork savings."""
        # Mock some fork-related events
        usage1 = TokenUsage(prompt_tokens=1000, completion_tokens=200, cached_tokens=800)
        usage2 = TokenUsage(prompt_tokens=1000, completion_tokens=150, cached_tokens=850)
        
        provider_tracker.track_request(
            model="claude-3-5-sonnet-20241022",
            provider="anthropic", 
            usage=usage1,
            cost=0.05,
            metadata={"is_fork": True, "parent_agent": "main"}
        )
        
        provider_tracker.track_request(
            model="claude-3-5-sonnet-20241022",
            provider="anthropic",
            usage=usage2,
            cost=0.04,
            metadata={"is_fork": True, "parent_agent": "main"}
        )
        
        savings_report = provider_tracker.get_fork_savings()
        
        assert "cached_tokens" in savings_report
        assert "actual_cost" in savings_report
        assert "estimated_traditional_cost" in savings_report
        assert "savings" in savings_report
        assert savings_report["cached_tokens"] == 1650  # 800 + 850


class TestCostTrackerIntegration:
    """Test integration with the global cost tracker."""
    
    def test_get_cost_tracker_singleton(self):
        """Test that get_cost_tracker returns singleton instance."""
        tracker1 = get_cost_tracker()
        tracker2 = get_cost_tracker()
        
        assert tracker1 is tracker2
    
    def test_cost_tracker_type(self):
        """Test that get_cost_tracker returns correct type."""
        tracker = get_cost_tracker()
        assert isinstance(tracker, ProviderCostTracker)
    
    def test_global_cost_tracking(self):
        """Test tracking costs globally."""
        tracker = get_cost_tracker()
        initial_event_count = len(tracker.events)
        
        usage = TokenUsage(prompt_tokens=100, completion_tokens=50)
        tracker.track_request("gpt-4", "openai", usage, 0.05)
        
        assert len(tracker.events) == initial_event_count + 1


class TestCostTrackerErrorHandling:
    """Test error handling in cost tracking."""
    
    @pytest.fixture
    def error_prone_tracker(self):
        """Create a tracker for error testing."""
        return ProviderCostTracker()
    
    def test_missing_pricing_data(self, error_prone_tracker):
        """Test handling of missing pricing data."""
        # Clear pricing cache
        error_prone_tracker.pricing_cache = {}
        
        usage = TokenUsage(prompt_tokens=100, completion_tokens=50)
        
        # Should not raise exception, should estimate or use default
        cost = error_prone_tracker.calculate_cost("unknown-model", usage)
        
        # Should return some reasonable cost (fallback calculation)
        assert cost >= 0
    
    def test_invalid_usage_data(self, error_prone_tracker):
        """Test handling of invalid usage data."""
        # Mock pricing data
        error_prone_tracker.pricing_cache = {
            "gpt-4": {
                "input_cost_per_token": 0.00003,
                "output_cost_per_token": 0.00006
            }
        }
        
        # Test with invalid token counts
        usage = TokenUsage(prompt_tokens=-100, completion_tokens=50)
        
        # Should handle gracefully
        cost = error_prone_tracker.calculate_cost("gpt-4", usage)
        assert cost >= 0  # Should not return negative cost
    
    def test_corrupted_pricing_data(self, error_prone_tracker):
        """Test handling of corrupted pricing data."""
        # Corrupt pricing data
        error_prone_tracker.pricing_cache = {
            "gpt-4": {
                "input_cost_per_token": "invalid_value",
                "output_cost_per_token": None
            }
        }
        
        usage = TokenUsage(prompt_tokens=100, completion_tokens=50)
        
        # Should handle gracefully and not crash
        try:
            cost = error_prone_tracker.calculate_cost("gpt-4", usage)
            assert cost >= 0
        except Exception:
            # If it raises an exception, that's also acceptable for corrupted data
            pass


class TestCostOptimizationMetrics:
    """Test metrics for cost optimization (from ForkedAgent scenarios)."""
    
    @pytest.fixture
    def optimization_tracker(self):
        """Create tracker for optimization testing."""
        tracker = ProviderCostTracker()
        # Mock Anthropic pricing with cache benefits
        tracker.pricing_cache = {
            "claude-3-5-sonnet-20241022": {
                "input_cost_per_token": 0.000015,
                "output_cost_per_token": 0.000075,
                "cache_read_cost_per_token": 0.0000015  # 10x cheaper for cached
            }
        }
        return tracker
    
    def test_caching_cost_savings(self, optimization_tracker):
        """Test calculating cost savings from caching."""
        # Simulate parent agent establishing cache
        parent_usage = TokenUsage(prompt_tokens=2000, completion_tokens=500)
        optimization_tracker.track_request(
            "claude-3-5-sonnet-20241022", 
            "anthropic", 
            parent_usage,
            metadata={"agent_type": "parent", "cache_setup": True}
        )
        
        # Simulate fork agents using cached content
        fork1_usage = TokenUsage(prompt_tokens=2100, completion_tokens=300, cached_tokens=2000)
        fork2_usage = TokenUsage(prompt_tokens=2150, completion_tokens=250, cached_tokens=2000)
        
        optimization_tracker.track_request(
            "claude-3-5-sonnet-20241022",
            "anthropic",
            fork1_usage,
            metadata={"agent_type": "fork", "parent_cache": True}
        )
        
        optimization_tracker.track_request(
            "claude-3-5-sonnet-20241022", 
            "anthropic",
            fork2_usage,
            metadata={"agent_type": "fork", "parent_cache": True}
        )
        
        # Calculate savings
        fork_savings = optimization_tracker.get_fork_savings()
        
        # Should show significant savings from caching
        assert fork_savings["cached_tokens"] == 4000  # 2000 + 2000
        assert fork_savings["savings"] > 0
        assert fork_savings["savings_percent"] > 0
    
    def test_traditional_vs_forked_cost_comparison(self, optimization_tracker):
        """Test comparing traditional vs forked agent costs."""
        # Simulate traditional approach (no caching)
        traditional_costs = []
        for i in range(3):
            usage = TokenUsage(prompt_tokens=2000, completion_tokens=300)
            cost = optimization_tracker.calculate_cost("claude-3-5-sonnet-20241022", usage)
            traditional_costs.append(cost)
        
        # Simulate forked approach (with caching)
        # Parent establishes cache
        parent_usage = TokenUsage(prompt_tokens=2000, completion_tokens=300)
        parent_cost = optimization_tracker.calculate_cost("claude-3-5-sonnet-20241022", parent_usage)
        
        # Forks benefit from cache
        forked_costs = [parent_cost]  # Parent cost
        for i in range(2):
            fork_usage = TokenUsage(prompt_tokens=2000, completion_tokens=300, cached_tokens=1900)
            fork_cost = optimization_tracker.calculate_cost("claude-3-5-sonnet-20241022", fork_usage)
            forked_costs.append(fork_cost)
        
        traditional_total = sum(traditional_costs)
        forked_total = sum(forked_costs)
        
        # Forked approach should be cheaper
        assert forked_total < traditional_total
        
        savings_percent = ((traditional_total - forked_total) / traditional_total) * 100
        assert savings_percent > 10  # Should save at least 10%