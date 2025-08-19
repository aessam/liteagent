#!/usr/bin/env python3
"""
Test script to verify ForkedAgents caching works with multiple providers.

This script tests the caching functionality for both Anthropic and OpenAI
providers to ensure cost optimization is working correctly.
"""

import os
import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))

from liteagent.forked_agent import ForkedAgent
from liteagent import liteagent_tool
from liteagent.provider_cost_tracker import get_cost_tracker

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


@liteagent_tool(name="test_tool", description="A simple test tool")
def test_tool(message: str) -> str:
    """Simple test tool that returns the input message."""
    return f"Tool executed: {message}"


def test_provider_caching(provider: str, model: str):
    """Test caching functionality for a specific provider."""
    print(f"\n{'='*60}")
    print(f"🧪 TESTING {provider.upper()} CACHING")
    print(f"{'='*60}")
    
    # Create a large context to trigger caching
    large_context = """
    This is a large context that should trigger caching mechanisms.
    """ * 50  # Repeat to make it large enough
    
    print(f"📊 Context size: {len(large_context):,} characters")
    
    # Create parent agent with large context
    print(f"🤖 Creating parent agent with {provider}...")
    
    parent = ForkedAgent(
        model=model,
        name=f"test_parent_{provider}",
        system_prompt=f"You are a test agent. Context: {large_context}",
        tools=[test_tool],
        provider=provider,
        enable_caching=True,
        debug=True
    )
    
    print(f"✅ Parent agent created")
    
    # Check if caching is supported
    caching_supported = parent.model_interface.supports_caching()
    print(f"🔧 Caching supported: {caching_supported}")
    
    # Create a fork
    print(f"🔀 Creating fork...")
    fork = parent.fork(
        name=f"test_fork_{provider}",
        prefill_role="test assistant",
        allowed_tools=["test_tool"]
    )
    
    print(f"✅ Fork created: {fork.name}")
    
    # Test with parent
    print(f"💬 Testing parent agent...")
    parent_response = parent.chat("Hello, please use the test_tool with message 'parent test'")
    print(f"📝 Parent response length: {len(parent_response)} chars")
    
    # Test with fork
    print(f"💬 Testing fork agent...")
    fork_response = fork.chat("Hello, please use the test_tool with message 'fork test'")
    print(f"📝 Fork response length: {len(fork_response)} chars")
    
    # Get cost summary
    cost_tracker = get_cost_tracker()
    cost_summary = cost_tracker.get_summary()
    
    print(f"\n💰 Cost Summary for {provider}:")
    if "message" in cost_summary:
        print(f"  • {cost_summary['message']}")
    else:
        print(f"  • Total cost: ${cost_summary['total_cost']:.6f}")
        print(f"  • Total tokens: {cost_summary['total_tokens']:,}")
        print(f"  • Total events: {cost_summary['total_events']}")
        
        fork_savings = cost_summary.get('fork_savings', {})
        if not isinstance(fork_savings, str):
            cached_tokens = fork_savings.get('cached_tokens', 0)
            print(f"  • Cached tokens: {cached_tokens:,}")
            if cached_tokens > 0:
                print(f"  ✅ Caching is working!")
            else:
                print(f"  ⚠️ No cached tokens detected")
    
    return {
        'provider': provider,
        'model': model,
        'caching_supported': caching_supported,
        'cost_summary': cost_summary
    }


def main():
    """Test caching with multiple providers."""
    print("🚀 ForkedAgents Caching Test")
    print("="*60)
    
    # Test configurations
    test_configs = []
    
    # Add Anthropic if API key is available
    if os.getenv('ANTHROPIC_API_KEY'):
        test_configs.append(('anthropic', 'claude-3-5-sonnet-20241022'))
    
    # Add OpenAI if API key is available
    if os.getenv('OPENAI_API_KEY'):
        test_configs.append(('openai', 'gpt-4o'))
    
    if not test_configs:
        print("❌ No API keys found. Please set ANTHROPIC_API_KEY or OPENAI_API_KEY")
        return
    
    results = []
    
    for provider, model in test_configs:
        try:
            result = test_provider_caching(provider, model)
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed for {provider}: {e}")
            results.append({
                'provider': provider,
                'model': model,
                'error': str(e)
            })
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 FINAL SUMMARY")
    print(f"{'='*60}")
    
    for result in results:
        provider = result['provider']
        if 'error' in result:
            print(f"❌ {provider}: {result['error']}")
        else:
            caching = "✅" if result['caching_supported'] else "❌"
            print(f"{caching} {provider}: Caching {('supported' if result['caching_supported'] else 'not supported')}")
    
    print(f"\n✨ ForkedAgents caching test completed!")


if __name__ == "__main__":
    main()