"""
Comprehensive metrics and monitoring for ForkedAgents.

This module provides detailed tracking of:
- Rate limit utilization
- Cache efficiency across providers
- Cost analysis and optimization
- Performance benchmarking
- Error rates and patterns
"""

import json
import time
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any
from collections import defaultdict, deque
from pathlib import Path
import threading

from .utils import logger


@dataclass
class RequestMetrics:
    """Metrics for a single request."""
    timestamp: float
    provider: str
    model: str
    tier: str
    estimated_tokens: int
    actual_tokens: int
    cache_hit: bool
    cache_tokens: int
    response_time: float
    cost: float
    success: bool
    error: Optional[str] = None


@dataclass
class ProviderStats:
    """Aggregated statistics for a provider."""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    total_tokens: int = 0
    cached_tokens: int = 0
    total_cost: float = 0.0
    avg_response_time: float = 0.0
    cache_hit_rate: float = 0.0
    error_rate: float = 0.0
    rate_limit_hits: int = 0


@dataclass
class SessionMetrics:
    """Metrics for a ForkedAgent session."""
    session_id: str
    agent_name: str
    provider: str
    model: str
    session_type: str
    start_time: float
    end_time: Optional[float] = None
    total_forks: int = 0
    successful_forks: int = 0
    failed_forks: int = 0
    total_cost: float = 0.0
    peak_parallel_forks: int = 0


class MetricsCollector:
    """
    Comprehensive metrics collector for ForkedAgents.
    
    Features:
    - Real-time metrics collection
    - Provider comparison and analysis
    - Cost optimization insights
    - Performance benchmarking
    - Exportable reports
    """
    
    def __init__(self, max_history: int = 10000):
        """
        Initialize metrics collector.
        
        Args:
            max_history: Maximum number of request records to keep in memory
        """
        self.max_history = max_history
        self._lock = threading.Lock()
        
        # Raw data storage
        self.request_history: deque = deque(maxlen=max_history)
        self.session_history: Dict[str, SessionMetrics] = {}
        
        # Aggregated statistics  
        self.provider_stats: Dict[str, ProviderStats] = defaultdict(ProviderStats)
        self.hourly_stats: Dict[str, Dict[str, Any]] = defaultdict(dict)
        
        # Performance tracking
        self.rate_limit_events: List[Dict[str, Any]] = []
        self.error_events: List[Dict[str, Any]] = []
        
        # Configuration
        self.collection_enabled = True
        self.auto_export_interval = 3600  # Export every hour
        self.last_export = time.time()
        
    def record_request(self, metrics: RequestMetrics):
        """Record metrics for a single request."""
        if not self.collection_enabled:
            return
            
        with self._lock:
            # Add to history
            self.request_history.append(metrics)
            
            # Update provider stats
            provider_key = f"{metrics.provider}:{metrics.model}"
            stats = self.provider_stats[provider_key]
            
            stats.total_requests += 1
            if metrics.success:
                stats.successful_requests += 1
            else:
                stats.failed_requests += 1
                
            stats.total_tokens += metrics.actual_tokens
            stats.cached_tokens += metrics.cache_tokens
            stats.total_cost += metrics.cost
            
            # Update averages
            if stats.total_requests > 0:
                stats.error_rate = stats.failed_requests / stats.total_requests
                total_cache_tokens = stats.cached_tokens + stats.total_tokens
                stats.cache_hit_rate = stats.cached_tokens / total_cache_tokens if total_cache_tokens > 0 else 0
                
                # Update response time average
                current_avg = stats.avg_response_time
                new_avg = ((current_avg * (stats.total_requests - 1)) + metrics.response_time) / stats.total_requests
                stats.avg_response_time = new_avg
            
            # Record errors and rate limits
            if not metrics.success and metrics.error:
                self.error_events.append({
                    'timestamp': metrics.timestamp,
                    'provider': metrics.provider,
                    'model': metrics.model,
                    'error': metrics.error
                })
                
                if 'rate limit' in metrics.error.lower():
                    stats.rate_limit_hits += 1
                    self.rate_limit_events.append({
                        'timestamp': metrics.timestamp,
                        'provider': metrics.provider,
                        'model': metrics.model,
                        'tier': metrics.tier
                    })
            
            # Update hourly aggregations
            hour_key = time.strftime("%Y-%m-%d %H:00", time.localtime(metrics.timestamp))
            if hour_key not in self.hourly_stats:
                self.hourly_stats[hour_key] = {
                    'requests': 0,
                    'tokens': 0,
                    'cost': 0.0,
                    'cache_hits': 0,
                    'errors': 0
                }
                
            hour_stats = self.hourly_stats[hour_key]
            hour_stats['requests'] += 1
            hour_stats['tokens'] += metrics.actual_tokens
            hour_stats['cost'] += metrics.cost
            if metrics.cache_hit:
                hour_stats['cache_hits'] += 1
            if not metrics.success:
                hour_stats['errors'] += 1
        
        # Auto-export if needed
        if time.time() - self.last_export > self.auto_export_interval:
            self._auto_export()
    
    def start_session(self, session_metrics: SessionMetrics):
        """Start tracking a new session."""
        with self._lock:
            self.session_history[session_metrics.session_id] = session_metrics
            
    def end_session(self, session_id: str, final_cost: float = 0.0):
        """End session tracking."""
        with self._lock:
            if session_id in self.session_history:
                session = self.session_history[session_id]
                session.end_time = time.time()
                session.total_cost = final_cost
    
    def record_fork_event(self, session_id: str, success: bool):
        """Record fork creation event."""
        with self._lock:
            if session_id in self.session_history:
                session = self.session_history[session_id]
                session.total_forks += 1
                if success:
                    session.successful_forks += 1
                else:
                    session.failed_forks += 1
    
    def get_provider_comparison(self) -> Dict[str, Any]:
        """Get comparison of all providers."""
        with self._lock:
            comparison = {}
            
            for provider_key, stats in self.provider_stats.items():
                if stats.total_requests == 0:
                    continue
                    
                comparison[provider_key] = {
                    'total_requests': stats.total_requests,
                    'success_rate': f"{((stats.successful_requests / stats.total_requests) * 100):.1f}%",
                    'cache_hit_rate': f"{(stats.cache_hit_rate * 100):.1f}%",
                    'avg_response_time': f"{stats.avg_response_time:.2f}s",
                    'total_cost': f"${stats.total_cost:.4f}",
                    'cost_per_request': f"${(stats.total_cost / stats.total_requests):.4f}",
                    'tokens_per_request': int(stats.total_tokens / stats.total_requests),
                    'rate_limit_hits': stats.rate_limit_hits,
                    'error_rate': f"{(stats.error_rate * 100):.1f}%"
                }
            
            return comparison
    
    def get_cost_analysis(self) -> Dict[str, Any]:
        """Get detailed cost analysis."""
        with self._lock:
            total_cost = sum(stats.total_cost for stats in self.provider_stats.values())
            total_tokens = sum(stats.total_tokens for stats in self.provider_stats.values()) 
            total_cached = sum(stats.cached_tokens for stats in self.provider_stats.values())
            
            # Calculate potential costs without caching
            estimated_full_cost = total_cost
            if total_cached > 0:
                # Rough estimate: cached tokens would cost 10x more without caching
                cache_savings = total_cached * 0.001 * 9  # Assuming $0.001 per 1K tokens saved
                estimated_full_cost += cache_savings
            
            cost_analysis = {
                'total_cost': f"${total_cost:.4f}",
                'total_tokens': f"{total_tokens:,}",
                'cached_tokens': f"{total_cached:,}",
                'estimated_full_cost_without_cache': f"${estimated_full_cost:.4f}",
                'estimated_savings': f"${(estimated_full_cost - total_cost):.4f}",
                'savings_percentage': f"{((estimated_full_cost - total_cost) / estimated_full_cost * 100):.1f}%" if estimated_full_cost > 0 else "0%",
                'avg_cost_per_token': f"${(total_cost / max(1, total_tokens)):.6f}",
                'cache_efficiency': f"{(total_cached / max(1, total_tokens + total_cached) * 100):.1f}%"
            }
            
            # Provider breakdown
            cost_analysis['provider_breakdown'] = {}
            for provider_key, stats in self.provider_stats.items():
                if stats.total_cost > 0:
                    cost_analysis['provider_breakdown'][provider_key] = {
                        'cost': f"${stats.total_cost:.4f}",
                        'percentage': f"{(stats.total_cost / total_cost * 100):.1f}%"
                    }
            
            return cost_analysis
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get performance analysis report."""
        with self._lock:
            recent_requests = list(self.request_history)[-1000:]  # Last 1000 requests
            
            if not recent_requests:
                return {'error': 'No recent requests to analyze'}
            
            # Response time analysis
            response_times = [r.response_time for r in recent_requests if r.success]
            cache_hit_times = [r.response_time for r in recent_requests if r.success and r.cache_hit]
            cache_miss_times = [r.response_time for r in recent_requests if r.success and not r.cache_hit]
            
            performance_report = {
                'total_requests_analyzed': len(recent_requests),
                'avg_response_time': f"{(sum(response_times) / len(response_times)):.2f}s" if response_times else "N/A",
                'cache_hit_avg_time': f"{(sum(cache_hit_times) / len(cache_hit_times)):.2f}s" if cache_hit_times else "N/A",
                'cache_miss_avg_time': f"{(sum(cache_miss_times) / len(cache_miss_times)):.2f}s" if cache_miss_times else "N/A",
                'cache_speedup': "N/A",
                'recent_error_rate': f"{(len([r for r in recent_requests if not r.success]) / len(recent_requests) * 100):.1f}%",
                'recent_cache_hit_rate': f"{(len([r for r in recent_requests if r.cache_hit]) / len(recent_requests) * 100):.1f}%"
            }
            
            # Calculate cache speedup
            if cache_hit_times and cache_miss_times:
                avg_hit_time = sum(cache_hit_times) / len(cache_hit_times)
                avg_miss_time = sum(cache_miss_times) / len(cache_miss_times)
                speedup = avg_miss_time / avg_hit_time if avg_hit_time > 0 else 1
                performance_report['cache_speedup'] = f"{speedup:.1f}x"
            
            return performance_report
    
    def get_rate_limit_analysis(self) -> Dict[str, Any]:
        """Analyze rate limiting patterns."""
        with self._lock:
            recent_rate_limits = [e for e in self.rate_limit_events if time.time() - e['timestamp'] < 3600]
            
            analysis = {
                'rate_limit_hits_last_hour': len(recent_rate_limits),
                'total_rate_limit_hits': len(self.rate_limit_events),
                'most_limited_provider': 'N/A',
                'most_limited_model': 'N/A'
            }
            
            if self.rate_limit_events:
                # Find most rate-limited provider/model
                provider_counts = defaultdict(int)
                model_counts = defaultdict(int)
                
                for event in self.rate_limit_events:
                    provider_counts[event['provider']] += 1
                    model_counts[f"{event['provider']}:{event['model']}"] += 1
                
                if provider_counts:
                    analysis['most_limited_provider'] = max(provider_counts, key=provider_counts.get)
                if model_counts:
                    analysis['most_limited_model'] = max(model_counts, key=model_counts.get)
            
            return analysis
    
    def export_metrics(self, filepath: Optional[str] = None) -> str:
        """Export all metrics to JSON file."""
        if filepath is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filepath = f"forked_agents_metrics_{timestamp}.json"
        
        with self._lock:
            export_data = {
                'export_timestamp': time.time(),
                'export_date': time.strftime("%Y-%m-%d %H:%M:%S"),
                'provider_comparison': self.get_provider_comparison(),
                'cost_analysis': self.get_cost_analysis(),
                'performance_report': self.get_performance_report(),
                'rate_limit_analysis': self.get_rate_limit_analysis(),
                'hourly_stats': dict(self.hourly_stats),
                'provider_stats': {k: asdict(v) for k, v in self.provider_stats.items()},
                'recent_errors': self.error_events[-50:],  # Last 50 errors
                'session_summary': {
                    'total_sessions': len(self.session_history),
                    'active_sessions': len([s for s in self.session_history.values() if s.end_time is None])
                }
            }
        
        # Write to file
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        logger.info(f"Metrics exported to {filepath}")
        return str(filepath)
    
    def _auto_export(self):
        """Automatically export metrics."""
        try:
            self.export_metrics()
            self.last_export = time.time()
        except Exception as e:
            logger.warning(f"Auto-export failed: {e}")
    
    def print_summary(self):
        """Print a comprehensive summary to console."""
        print("\n" + "="*60)
        print("📊 FORKEDAGENTS METRICS SUMMARY")
        print("="*60)
        
        # Provider comparison
        comparison = self.get_provider_comparison()
        if comparison:
            print("\n🔧 PROVIDER COMPARISON:")
            for provider, stats in comparison.items():
                print(f"   {provider}:")
                print(f"      Requests: {stats['total_requests']}")
                print(f"      Success rate: {stats['success_rate']}")
                print(f"      Cache hit rate: {stats['cache_hit_rate']}")
                print(f"      Avg response time: {stats['avg_response_time']}")
                print(f"      Total cost: {stats['total_cost']}")
        
        # Cost analysis
        cost_analysis = self.get_cost_analysis()
        print(f"\n💰 COST ANALYSIS:")
        print(f"   Total cost: {cost_analysis['total_cost']}")
        print(f"   Total tokens: {cost_analysis['total_tokens']}")
        print(f"   Cache efficiency: {cost_analysis['cache_efficiency']}")
        print(f"   Estimated savings: {cost_analysis['estimated_savings']}")
        
        # Performance
        performance = self.get_performance_report()
        print(f"\n⚡ PERFORMANCE:")
        print(f"   Avg response time: {performance['avg_response_time']}")
        print(f"   Cache hit avg: {performance['cache_hit_avg_time']}")
        print(f"   Cache miss avg: {performance['cache_miss_avg_time']}")
        print(f"   Cache speedup: {performance['cache_speedup']}")
        
        # Rate limits
        rate_limits = self.get_rate_limit_analysis()
        print(f"\n🚦 RATE LIMITING:")
        print(f"   Hits last hour: {rate_limits['rate_limit_hits_last_hour']}")
        print(f"   Total hits: {rate_limits['total_rate_limit_hits']}")
        print(f"   Most limited: {rate_limits['most_limited_provider']}")


# Global metrics collector instance
_metrics_collector: Optional[MetricsCollector] = None


def get_metrics_collector() -> MetricsCollector:
    """Get global metrics collector instance."""
    global _metrics_collector
    if _metrics_collector is None:
        _metrics_collector = MetricsCollector()
    return _metrics_collector


def reset_metrics_collector():
    """Reset global metrics collector (useful for testing)."""
    global _metrics_collector
    _metrics_collector = None