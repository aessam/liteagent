"""
Deterministic mock provider for reliable testing.

This provider provides 100% predictable behavior for unit testing,
with configurable scenarios for different test cases.
"""

import time
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
from pathlib import Path
import json

from .mock_provider import MockProvider, MockResponse
from .base import ProviderResponse
from ..utils import logger


@dataclass
class TestScenario:
    """Defines a test scenario with expected behaviors."""
    name: str
    responses: List[MockResponse]
    should_error: bool = False
    error_message: Optional[str] = None
    rate_limit_after: Optional[int] = None  # Trigger rate limit after N requests
    cache_hit_pattern: Optional[List[bool]] = None  # Pattern of cache hits


class DeterministicMockProvider(MockProvider):
    """
    Deterministic version of MockProvider for testing.
    
    Features:
    - No randomness - completely predictable
    - Scenario-based responses
    - Configurable error injection
    - Predictable cache patterns
    - Fixed token counts
    """
    
    def __init__(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize deterministic mock provider.
        
        Args:
            model_name: Model to simulate
            api_key: Ignored for mock provider
            scenario: Test scenario name
            **kwargs: Additional configuration
        """
        # Disable all randomness
        kwargs['simulate_rate_limits'] = kwargs.get('simulate_rate_limits', False)
        kwargs['simulate_caching'] = kwargs.get('simulate_caching', True)
        kwargs['error_rate'] = 0.0  # No random errors
        kwargs['base_delay'] = 0.01  # Minimal delay for speed
        kwargs['cache_hit_rate'] = 1.0  # Will be controlled by scenario
        
        super().__init__(model_name, api_key, **kwargs)
        
        # Load scenario
        self.scenario_name = kwargs.get('scenario', 'default')
        self.scenario = self._load_scenario(self.scenario_name)
        self.scenario_index = 0
        
    def _load_scenario(self, scenario_name: str) -> TestScenario:
        """Load a test scenario."""
        scenarios = {
            'default': TestScenario(
                name='default',
                responses=[
                    MockResponse(
                        content="Test response 1",
                        usage={"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150},
                        model=self.model_name,
                        provider="mock",
                        response_time=0.1,
                        cache_hit=False
                    ),
                    MockResponse(
                        content="Test response 2",
                        usage={"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150, 
                               "cache_read_input_tokens": 100},
                        model=self.model_name,
                        provider="mock",
                        response_time=0.05,
                        cache_hit=True
                    ),
                ]
            ),
            
            'forking': TestScenario(
                name='forking',
                responses=[
                    MockResponse(
                        content="Parent agent response",
                        usage={"prompt_tokens": 200, "completion_tokens": 100, "total_tokens": 300,
                               "cache_creation_input_tokens": 200},
                        model=self.model_name,
                        provider="mock",
                        response_time=0.2,
                        cache_hit=False
                    ),
                    MockResponse(
                        content="Fork 1 response - specialized for security",
                        usage={"prompt_tokens": 250, "completion_tokens": 150, "total_tokens": 400,
                               "cache_read_input_tokens": 200},
                        model=self.model_name,
                        provider="mock",
                        response_time=0.1,
                        cache_hit=True
                    ),
                    MockResponse(
                        content="Fork 2 response - specialized for performance",
                        usage={"prompt_tokens": 250, "completion_tokens": 150, "total_tokens": 400,
                               "cache_read_input_tokens": 200},
                        model=self.model_name,
                        provider="mock",
                        response_time=0.1,
                        cache_hit=True
                    ),
                ],
                cache_hit_pattern=[False, True, True]
            ),
            
            'cost_tracking': TestScenario(
                name='cost_tracking',
                responses=[
                    MockResponse(
                        content="Response with no caching",
                        usage={"prompt_tokens": 1000, "completion_tokens": 500, "total_tokens": 1500},
                        model=self.model_name,
                        provider="mock",
                        response_time=0.5,
                        cache_hit=False
                    ),
                    MockResponse(
                        content="Response with partial caching",
                        usage={"prompt_tokens": 1000, "completion_tokens": 500, "total_tokens": 1500,
                               "cache_read_input_tokens": 800},
                        model=self.model_name,
                        provider="mock",
                        response_time=0.3,
                        cache_hit=True
                    ),
                    MockResponse(
                        content="Response with full caching",
                        usage={"prompt_tokens": 1000, "completion_tokens": 500, "total_tokens": 1500,
                               "cache_read_input_tokens": 1000},
                        model=self.model_name,
                        provider="mock",
                        response_time=0.2,
                        cache_hit=True
                    ),
                ]
            ),
            
            'rate_limit': TestScenario(
                name='rate_limit',
                responses=[
                    MockResponse(
                        content=f"Response {i}",
                        usage={"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150},
                        model=self.model_name,
                        provider="mock",
                        response_time=0.1,
                        cache_hit=False
                    ) for i in range(5)
                ],
                rate_limit_after=3  # Trigger rate limit after 3 requests
            ),
            
            'error': TestScenario(
                name='error',
                responses=[],
                should_error=True,
                error_message="Simulated API error for testing"
            ),
            
            'tool_calling': TestScenario(
                name='tool_calling',
                responses=[
                    MockResponse(
                        content="I'll help you with that calculation.",
                        usage={"prompt_tokens": 150, "completion_tokens": 75, "total_tokens": 225},
                        model=self.model_name,
                        provider="mock",
                        response_time=0.15,
                        cache_hit=False
                    ),
                ]
            ),
        }
        
        # Load custom scenario from file if not built-in
        if scenario_name not in scenarios:
            scenario_path = Path(__file__).parent.parent / 'test_data' / 'scenarios' / f'{scenario_name}.json'
            if scenario_path.exists():
                return self._load_scenario_from_file(scenario_path)
            else:
                logger.warning(f"Unknown scenario '{scenario_name}', using default")
                return scenarios['default']
        
        return scenarios[scenario_name]
    
    def _load_scenario_from_file(self, path: Path) -> TestScenario:
        """Load scenario from JSON file."""
        with open(path, 'r') as f:
            data = json.load(f)
        
        responses = []
        for resp_data in data.get('responses', []):
            responses.append(MockResponse(**resp_data))
        
        return TestScenario(
            name=data['name'],
            responses=responses,
            should_error=data.get('should_error', False),
            error_message=data.get('error_message'),
            rate_limit_after=data.get('rate_limit_after'),
            cache_hit_pattern=data.get('cache_hit_pattern')
        )
    
    def generate_response(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate deterministic response based on scenario.
        
        Args:
            messages: Message history
            tools: Tools (ignored in mock)
            **kwargs: Additional parameters
            
        Returns:
            ProviderResponse: Deterministic response
        """
        self.request_count += 1
        
        # Check for error scenario
        if self.scenario.should_error:
            raise Exception(self.scenario.error_message or "Simulated error")
        
        # Check for rate limit scenario
        if self.scenario.rate_limit_after and self.request_count > self.scenario.rate_limit_after:
            raise Exception("Rate limit exceeded")
        
        # Get next response from scenario
        if not self.scenario.responses:
            raise ValueError(f"No responses defined for scenario '{self.scenario_name}'")
        
        response = self.scenario.responses[self.scenario_index % len(self.scenario.responses)]
        self.scenario_index += 1
        
        # Apply cache hit pattern if defined
        if self.scenario.cache_hit_pattern:
            pattern_index = (self.scenario_index - 1) % len(self.scenario.cache_hit_pattern)
            response.cache_hit = self.scenario.cache_hit_pattern[pattern_index]
        
        # Update statistics
        self._update_stats(response)
        
        # Minimal processing delay for realism
        time.sleep(0.01)
        
        return ProviderResponse(
            content=response.content,
            tool_calls=[],
            usage=response.usage,
            model=response.model,
            provider=self.provider_name,
            raw_response={
                'mock': True, 
                'deterministic': True,
                'scenario': self.scenario_name,
                'response_index': self.scenario_index - 1
            },
            finish_reason='stop'
        )
    
    def _simulate_error(self):
        """Override to prevent random errors."""
        # No random errors in deterministic mode
        pass
    
    def _simulate_rate_limit_check(self, messages: List[Dict[str, Any]]):
        """Override to prevent random rate limiting."""
        # No random rate limiting in deterministic mode
        pass
    
    def _calculate_processing_delay(self, response: MockResponse) -> float:
        """Override for minimal, fixed delay."""
        return 0.01  # Fixed 10ms delay
    
    def reset_scenario(self):
        """Reset scenario to beginning."""
        self.scenario_index = 0
        self.request_count = 0
        self.reset_stats()
        logger.info(f"[{self.provider_name}] Scenario '{self.scenario_name}' reset")
    
    def set_scenario(self, scenario_name: str):
        """Change to a different scenario."""
        self.scenario_name = scenario_name
        self.scenario = self._load_scenario(scenario_name)
        self.reset_scenario()
        logger.info(f"[{self.provider_name}] Switched to scenario '{scenario_name}'")