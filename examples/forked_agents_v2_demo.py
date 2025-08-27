#!/usr/bin/env python3
"""
ForkedAgents v2 demonstration with intelligent rate limiting and provider optimization.

This example showcases the new architecture with:
- Automatic provider selection (stateful vs stateless)
- Intelligent rate limiting with token bucket algorithm
- Cost-effective testing with mock providers
- Comprehensive metrics and monitoring
"""

import os
import sys
import argparse
import time
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from liteagent.forked_agent_v2 import ForkedAgentV2, ForkConfig
from liteagent.rate_limiter import get_rate_limiter, RateLimitError
from liteagent.providers.mock_provider import MockProvider

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def load_sample_codebase() -> str:
    """Load sample codebase for analysis."""
    # Use a smaller sample for demo purposes
    sample_code = """
# Sample Python codebase for analysis
import os
import json
from typing import Dict, List, Optional

class DataProcessor:
    def __init__(self, config_file: str):
        self.config = self._load_config(config_file)
        self.data_cache = {}
        
    def _load_config(self, config_file: str) -> Dict:
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Config file {config_file} not found")
            return {}
    
    def process_data(self, data: List[Dict]) -> List[Dict]:
        processed = []
        for item in data:
            # Basic processing logic
            if 'id' in item and 'value' in item:
                processed_item = {
                    'id': item['id'],
                    'processed_value': item['value'] * 2,
                    'status': 'processed'
                }
                processed.append(processed_item)
        return processed
    
    def cache_result(self, key: str, result: any):
        self.data_cache[key] = result
    
    def get_cached_result(self, key: str) -> Optional[any]:
        return self.data_cache.get(key)

# Example usage
if __name__ == "__main__":
    processor = DataProcessor("config.json")
    sample_data = [
        {"id": 1, "value": 10},
        {"id": 2, "value": 20},
        {"id": 3, "value": 30}
    ]
    results = processor.process_data(sample_data)
    print(f"Processed {len(results)} items")
    """
    return sample_code


def demo_mock_provider():
    """Demonstrate cost-effective testing with mock provider."""
    print("\n" + "="*60)
    print("🧪 MOCK PROVIDER DEMONSTRATION")
    print("="*60)
    
    print("📊 Creating mock-based ForkedAgent...")
    
    try:
        # Create agent with mock provider
        agent = ForkedAgentV2(
            model="mock",  # Use mock as model name
            provider="mock",
            system_prompt="You are a comprehensive code analysis system.",
            name="mock_demo_agent",
            enable_rate_limiting=True
        )
        
        print(f"✅ Created agent: {agent.name}")
        print(f"📡 Session type: {agent.session_type.value}")
        
        # Prepare for forking
        if agent.prepare_for_forking():
            print("✅ Agent prepared for forking")
        else:
            print("❌ Failed to prepare agent")
            return
        
        # Define analysis tasks
        tasks = [
            {
                "name": "security_audit",
                "role": "security expert", 
                "message": "Analyze this code for security vulnerabilities."
            },
            {
                "name": "performance_review",
                "role": "performance optimizer",
                "message": "Identify performance bottlenecks and optimization opportunities."
            },
            {
                "name": "style_check", 
                "role": "code style reviewer",
                "message": "Review code style and suggest improvements."
            }
        ]
        
        print(f"\n🔀 Running {len(tasks)} analysis tasks...")
        start_time = time.time()
        
        # Run batch analysis
        results = agent.batch_analyze(tasks, max_parallel=2)
        
        total_time = time.time() - start_time
        print(f"⏱️ Total execution time: {total_time:.2f}s")
        
        # Display results
        print(f"\n📋 ANALYSIS RESULTS:")
        for task_name, result in results.items():
            status = "✅ SUCCESS" if result['success'] else "❌ FAILED"
            print(f"   {status} {task_name}")
            if result['success']:
                print(f"      Response: {result['response'][:100]}...")
            else:
                print(f"      Error: {result['error']}")
        
        # Show mock statistics
        if isinstance(agent.provider, MockProvider):
            stats = agent.provider.get_mock_stats()
            print(f"\n📊 MOCK PROVIDER STATISTICS:")
            for key, value in stats.items():
                print(f"   {key}: {value}")
        
        # Show rate limiter stats
        rate_limiter = get_rate_limiter()
        limiter_stats = rate_limiter.get_usage_stats()
        print(f"\n🚦 RATE LIMITER STATISTICS:")
        print(f"   Total requests tracked: {sum(limiter_stats['request_counts'].values())}")
        print(f"   Token usage: {sum(limiter_stats['daily_token_usage'].values())}")
        
        agent.cleanup()
        print("✅ Mock demonstration completed successfully!")
        
    except RateLimitError as e:
        print(f"❌ Rate limit configuration error: {e}")
        print("💡 Please update the rate_limits.json file with correct values")
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()


def demo_real_provider(provider: str, model: str):
    """Demonstrate with real provider (if configured)."""
    print("\n" + "="*60)
    print(f"🚀 REAL PROVIDER DEMONSTRATION ({provider.upper()})")
    print("="*60)
    
    try:
        # Load sample codebase
        codebase = load_sample_codebase()
        
        print(f"📊 Codebase size: {len(codebase):,} characters")
        print(f"🤖 Creating {provider} agent with model {model}...")
        
        # Create agent
        agent = ForkedAgentV2(
            model=model,
            provider=provider,
            system_prompt=f"You are a comprehensive code analysis system. CODEBASE:\n\n{codebase}",
            name=f"real_{provider}_agent",
            tier="tier_1",  # Use lowest tier for safety
            enable_rate_limiting=True
        )
        
        print(f"✅ Created agent: {agent.name}")
        print(f"📡 Session type: {agent.session_type.value}")
        
        # Check rate limits
        rate_limiter = get_rate_limiter()
        limits = rate_limiter.get_rate_limit(provider, model, "tier_1")
        print(f"🚦 Rate limits: {limits.rpm} RPM, {limits.tpm} TPM")
        
        # Prepare for forking
        print("\n🔧 Preparing agent for forking...")
        if agent.prepare_for_forking():
            print("✅ Agent prepared successfully")
        else:
            print("❌ Failed to prepare agent")
            return
        
        # Create a single fork for demonstration
        print("\n🔀 Creating security analysis fork...")
        security_config = ForkConfig(
            name="security_expert",
            role="security vulnerability expert"
        )
        
        security_fork = agent.fork(security_config)
        print(f"✅ Created fork: {security_fork.name}")
        
        # Send message to fork
        print("\n💬 Sending analysis request...")
        response = security_fork.send_message(
            "Please provide a brief security analysis of the provided codebase."
        )
        
        print(f"\n📝 SECURITY ANALYSIS:")
        print(response[:500] + "..." if len(response) > 500 else response)
        
        # Show statistics
        stats = agent.get_stats()
        print(f"\n📊 AGENT STATISTICS:")
        for key, value in stats.items():
            if key != 'rate_limiter_stats':
                print(f"   {key}: {value}")
        
        agent.cleanup()
        print("✅ Real provider demonstration completed!")
        
    except RateLimitError as e:
        print(f"❌ Rate limit error: {e}")
        print("💡 This is expected - the system is protecting against rate limits!")
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Main demonstration function."""
    parser = argparse.ArgumentParser(description="ForkedAgents v2 Demo")
    parser.add_argument("--provider", "-p", default="mock", 
                       help="Provider to use (mock, openai, anthropic, google)")
    parser.add_argument("--model", "-m", default="gpt-4o",
                       help="Model to use")
    parser.add_argument("--demo-type", default="both", 
                       choices=["mock", "real", "both"],
                       help="Type of demo to run")
    
    args = parser.parse_args()
    
    print("🔀 FORKEDAGENTS V2 DEMONSTRATION")
    print("=" * 60)
    print("Features demonstrated:")
    print("• Intelligent provider routing (stateful vs stateless)")
    print("• Token bucket rate limiting")
    print("• True context sharing where supported")
    print("• Cost-effective testing with mock providers")
    print("• Comprehensive metrics and monitoring")
    
    # Always show mock demo (free and educational)
    if args.demo_type in ["mock", "both"]:
        demo_mock_provider()
    
    # Show real provider demo if requested and configured
    if args.demo_type in ["real", "both"] and args.provider != "mock":
        # Check if API keys are configured
        api_key_vars = {
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY", 
            "google": "GOOGLE_AI_API_KEY"
        }
        
        required_key = api_key_vars.get(args.provider)
        if required_key and not os.getenv(required_key):
            print(f"\n⚠️ Skipping real provider demo - {required_key} not set")
        else:
            demo_real_provider(args.provider, args.model)
    
    print(f"\n🎯 SUMMARY:")
    print("• Mock provider demo shows the system working without API costs")
    print("• Rate limiting prevents expensive API errors")
    print("• Provider routing optimizes for each API's strengths")
    print("• Cost tracking provides visibility into usage")
    print(f"• Configuration file: liteagent/config/rate_limits.json")


if __name__ == "__main__":
    main()