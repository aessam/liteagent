"""
Mock provider for cost-effective testing and development.

This provider simulates real API behavior including:
- Rate limiting simulation
- Cache hit/miss patterns  
- Token consumption tracking
- Realistic response delays
- Error scenarios for testing
"""

import json
import time
import random
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
from pathlib import Path

from .base import ProviderInterface, ProviderResponse, ToolCall
from ..utils import logger


@dataclass
class MockResponse:
    """Recorded real API response for playback."""
    content: str
    usage: Dict[str, Any]
    model: str
    provider: str
    response_time: float
    cache_hit: bool = False


class MockProvider(ProviderInterface):
    """
    Mock provider that simulates real API behavior.
    
    Features:
    - Plays back recorded real responses
    - Simulates rate limiting behavior
    - Realistic cache hit/miss patterns
    - Configurable error injection
    - Cost tracking without API calls
    """
    
    def __init__(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize mock provider.
        
        Args:
            model_name: Model to simulate
            api_key: Ignored for mock provider
            **kwargs: Mock configuration options
        """
        self.simulate_rate_limits = kwargs.get('simulate_rate_limits', True)
        self.simulate_caching = kwargs.get('simulate_caching', True)
        self.cache_hit_rate = kwargs.get('cache_hit_rate', 0.7)  # 70% cache hits
        self.error_rate = kwargs.get('error_rate', 0.02)  # 2% error rate
        self.base_delay = kwargs.get('base_delay', 0.5)  # Base response delay
        
        # Response recording
        self.responses_file = kwargs.get('responses_file', 'mock_responses.json')
        self.recorded_responses: List[MockResponse] = []
        self.response_index = 0
        
        # State tracking
        self.request_count = 0
        self.total_tokens_used = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.simulated_cost = 0.0
        
        super().__init__(model_name, api_key, **kwargs)
        self._load_recorded_responses()
        
    def _get_provider_name(self) -> str:
        """Return provider name."""
        return 'mock'
        
    def _setup_client(self) -> None:
        """Setup mock client (no-op)."""
        logger.info(f"[{self.provider_name}] Mock provider initialized for {self.model_name}")
        
    def _load_recorded_responses(self):
        """Load recorded responses from file."""
        responses_path = Path(__file__).parent.parent / 'test_data' / self.responses_file
        
        if responses_path.exists():
            try:
                with open(responses_path, 'r') as f:
                    data = json.load(f)
                    
                for response_data in data:
                    self.recorded_responses.append(MockResponse(
                        content=response_data['content'],
                        usage=response_data['usage'],
                        model=response_data['model'],
                        provider=response_data['provider'],
                        response_time=response_data['response_time'],
                        cache_hit=response_data.get('cache_hit', False)
                    ))
                    
                logger.info(f"[{self.provider_name}] Loaded {len(self.recorded_responses)} recorded responses")
                
            except Exception as e:
                logger.warning(f"[{self.provider_name}] Could not load recorded responses: {e}")
                self._generate_default_responses()
        else:
            self._generate_default_responses()
    
    def _generate_default_responses(self):
        """Generate default responses for testing."""
        default_responses = [
            {
                "content": "I understand and am ready to receive your definition of my role and purpose in your next message.",
                "usage": {"prompt_tokens": 25, "completion_tokens": 20, "total_tokens": 45, "cache_creation_input_tokens": 8012},
                "model": self.model_name,
                "provider": "mock",
                "response_time": 0.8,
                "cache_hit": False
            },
            {
                "content": "As a security expert, I've analyzed the codebase and found several areas for improvement including input validation, error handling, and file operations security.",
                "usage": {"prompt_tokens": 87, "completion_tokens": 180, "total_tokens": 267, "cache_read_input_tokens": 8012},
                "model": self.model_name,
                "provider": "mock", 
                "response_time": 1.2,
                "cache_hit": True
            },
            {
                "content": "From a performance perspective, I've identified opportunities for optimization in data structures, algorithm efficiency, and memory usage patterns.",
                "usage": {"prompt_tokens": 92, "completion_tokens": 195, "total_tokens": 287, "cache_read_input_tokens": 8012},
                "model": self.model_name,
                "provider": "mock",
                "response_time": 1.1,
                "cache_hit": True
            },
            {
                "content": "As a code style reviewer, I've examined the codebase for consistency, readability, and adherence to best practices.",
                "usage": {"prompt_tokens": 89, "completion_tokens": 165, "total_tokens": 254, "cache_read_input_tokens": 8012},
                "model": self.model_name,
                "provider": "mock",
                "response_time": 0.9,
                "cache_hit": True
            }
        ]
        
        for response_data in default_responses:
            self.recorded_responses.append(MockResponse(**response_data))
            
        logger.info(f"[{self.provider_name}] Generated {len(default_responses)} default responses")
    
    def generate_response(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate mock response with realistic simulation.
        
        Args:
            messages: Message history
            tools: Tools (ignored in mock)
            **kwargs: Additional parameters
            
        Returns:
            ProviderResponse: Simulated response
        """
        start_time = time.time()
        self.request_count += 1
        
        # Simulate error scenarios
        if random.random() < self.error_rate:
            self._simulate_error()
        
        # Simulate rate limiting
        if self.simulate_rate_limits:
            self._simulate_rate_limit_check(messages)
        
        # Get response (cyclic through recorded responses)
        response = self._get_next_response(messages, **kwargs)
        
        # Simulate processing delay
        processing_delay = self._calculate_processing_delay(response)
        time.sleep(processing_delay)
        
        # Update statistics
        self._update_stats(response)
        
        elapsed_time = time.time() - start_time
        logger.info(f"[{self.provider_name}] Mock response generated in {elapsed_time:.2f}s")
        
        return ProviderResponse(
            content=response.content,
            tool_calls=[],
            usage=response.usage,
            model=response.model,
            provider=self.provider_name,
            raw_response={'mock': True, 'response_index': self.response_index - 1},
            finish_reason='stop'
        )
    
    def _simulate_error(self):
        """Simulate various error scenarios."""
        error_types = [
            "Rate limit exceeded",
            "Invalid API key", 
            "Model overloaded",
            "Context length exceeded",
            "Network timeout"
        ]
        
        error = random.choice(error_types)
        logger.warning(f"[{self.provider_name}] Simulating error: {error}")
        
        # For some errors, actually raise exception
        if "Rate limit" in error:
            raise Exception(f"Simulated rate limit error: {error}")
        elif random.random() < 0.3:  # 30% of errors are exceptions
            raise Exception(f"Simulated API error: {error}")
    
    def _simulate_rate_limit_check(self, messages: List[Dict[str, Any]]):
        """Simulate rate limiting delays."""
        # Estimate tokens
        estimated_tokens = sum(len(msg.get('content', '')) for msg in messages) // 4
        
        # Simulate token bucket with random delays
        if estimated_tokens > 10000:  # Large requests
            delay = random.uniform(0.5, 2.0)
            logger.info(f"[{self.provider_name}] Simulating rate limit delay: {delay:.1f}s")
            time.sleep(delay)
        elif self.request_count > 5 and random.random() < 0.1:  # 10% chance of delay
            delay = random.uniform(0.1, 0.5)
            time.sleep(delay)
    
    def _get_next_response(self, messages: List[Dict[str, Any]], **kwargs) -> MockResponse:
        """Get next response from recorded responses."""
        if not self.recorded_responses:
            # Fallback response
            return MockResponse(
                content="This is a mock response for testing purposes.",
                usage={"prompt_tokens": 50, "completion_tokens": 10, "total_tokens": 60},
                model=self.model_name,
                provider="mock",
                response_time=0.5
            )
        
        # Cycle through responses
        response = self.recorded_responses[self.response_index % len(self.recorded_responses)]
        self.response_index += 1
        
        # Simulate cache behavior
        if self.simulate_caching and self.request_count > 1:
            response.cache_hit = random.random() < self.cache_hit_rate
            
            if response.cache_hit:
                # Modify usage to show cache hit
                new_usage = response.usage.copy()
                new_usage['cache_read_input_tokens'] = new_usage.get('prompt_tokens', 50)
                new_usage['cache_creation_input_tokens'] = 0
                response.usage = new_usage
        
        return response
    
    def _calculate_processing_delay(self, response: MockResponse) -> float:
        """Calculate realistic processing delay."""
        base_delay = self.base_delay
        
        # Faster for cache hits
        if response.cache_hit:
            base_delay *= 0.3
        
        # Add some randomness
        delay = base_delay + random.uniform(-0.2, 0.3)
        return max(0.1, delay)  # Minimum 100ms
    
    def _update_stats(self, response: MockResponse):
        """Update usage statistics."""
        self.total_tokens_used += response.usage.get('total_tokens', 0)
        
        if response.cache_hit:
            self.cache_hits += 1
        else:
            self.cache_misses += 1
        
        # Simulate costs (much lower than real APIs)
        tokens = response.usage.get('total_tokens', 0)
        if response.cache_hit:
            cost = tokens * 0.0001 * 0.1  # 10% of normal cost for cache hits
        else:
            cost = tokens * 0.0001
        
        self.simulated_cost += cost
    
    def get_mock_stats(self) -> Dict[str, Any]:
        """Get mock provider statistics."""
        cache_total = self.cache_hits + self.cache_misses
        cache_rate = (self.cache_hits / cache_total * 100) if cache_total > 0 else 0
        
        return {
            'provider': self.provider_name,
            'model': self.model_name,
            'total_requests': self.request_count,
            'total_tokens_used': self.total_tokens_used,
            'cache_hits': self.cache_hits,
            'cache_misses': self.cache_misses,
            'cache_hit_rate': f"{cache_rate:.1f}%",
            'simulated_cost': f"${self.simulated_cost:.4f}",
            'avg_tokens_per_request': self.total_tokens_used / max(1, self.request_count),
            'cost_savings_from_cache': f"${(self.cache_hits * 0.001):.4f}"
        }
    
    def record_real_response(self, response: ProviderResponse, response_time: float):
        """
        Record a real API response for future playback.
        
        Args:
            response: Real provider response
            response_time: Time taken for real response
        """
        mock_response = MockResponse(
            content=response.content,
            usage=response.usage or {},
            model=response.model,
            provider=response.provider,
            response_time=response_time,
            cache_hit=response.usage.get('cache_read_input_tokens', 0) > 0 if response.usage else False
        )
        
        self.recorded_responses.append(mock_response)
        logger.info(f"[{self.provider_name}] Recorded response for future playback")
    
    def save_recorded_responses(self, filename: Optional[str] = None):
        """Save recorded responses to file."""
        filename = filename or self.responses_file
        output_path = Path(__file__).parent.parent / 'test_data' / filename
        
        # Create directory if needed
        output_path.parent.mkdir(exist_ok=True)
        
        # Convert to serializable format
        data = []
        for response in self.recorded_responses:
            data.append({
                'content': response.content,
                'usage': response.usage,
                'model': response.model,
                'provider': response.provider,
                'response_time': response.response_time,
                'cache_hit': response.cache_hit
            })
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
            
        logger.info(f"[{self.provider_name}] Saved {len(data)} responses to {filename}")
    
    def supports_caching(self) -> bool:
        """Return True to simulate caching support."""
        return self.simulate_caching
    
    def supports_tool_calling(self) -> bool:
        """Return False for simplicity."""
        return False
    
    def supports_stateful_sessions(self) -> bool:
        """Return False - mock is stateless."""
        return False
    
    def reset_stats(self):
        """Reset usage statistics."""
        self.request_count = 0
        self.total_tokens_used = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.simulated_cost = 0.0
        self.response_index = 0
        logger.info(f"[{self.provider_name}] Statistics reset")