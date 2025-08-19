#!/usr/bin/env python3
"""
Test script to verify the ForkedAgents fixes work properly.

This script tests:
1. Real context sharing with caching
2. Accurate success/failure reporting  
3. Rate limit handling
4. Mathematically consistent metrics
"""

import os
import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))

from liteagent.forked_agent import ForkedAgent
from liteagent.provider_cost_tracker import get_cost_tracker

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def test_fixed_forked_agents():
    """Test the fixed ForkedAgents implementation."""
    print("🧪 TESTING FIXED FORKEDAGENTS IMPLEMENTATION")
    print("="*60)
    
    # Reset cost tracker
    cost_tracker = get_cost_tracker()
    cost_tracker.events = []
    
    # Create smaller test content to avoid overwhelming the API
    test_content = "This is a test context. " * 100  # ~2K characters
    print(f"📊 Test content size: {len(test_content):,} characters")
    
    # Create parent agent with caching
    print("\n🤖 Creating parent agent with caching...")
    parent = ForkedAgent(
        model="claude-3-5-sonnet-20241022",
        name="test_parent",
        system_prompt=f"You are a test agent. Test content: {test_content}",
        provider="anthropic",
        enable_caching=True,
        debug=True
    )
    print(f"✅ Parent created: {parent.context_id}")
    
    # Check cost after parent
    parent_cost = cost_tracker.get_total_cost()
    parent_tokens = cost_tracker.get_total_tokens()
    print(f"💰 Parent cost: ${parent_cost:.6f} ({parent_tokens:,} tokens)")
    
    # Create a simple fork
    print("\n🔀 Creating test fork...")
    fork = parent.fork(
        name="test_fork",
        prefill_role="simple test assistant"
    )
    print(f"✅ Fork created: {fork.context_id}")
    
    # Test parent chat
    print("\n💬 Testing parent chat...")
    try:
        parent_response = parent.chat("Say hello briefly.")
        print(f"✅ Parent response: {parent_response[:100]}...")
        parent_success = True
    except Exception as e:
        print(f"❌ Parent failed: {e}")
        parent_success = False
    
    # Check cost after parent chat
    after_parent_cost = cost_tracker.get_total_cost()
    after_parent_tokens = cost_tracker.get_total_tokens()
    parent_chat_cost = after_parent_cost - parent_cost
    parent_chat_tokens = after_parent_tokens - parent_tokens
    print(f"💰 Parent chat cost: ${parent_chat_cost:.6f} ({parent_chat_tokens:,} tokens)")
    
    # Test fork chat
    print("\n💬 Testing fork chat...")
    try:
        fork_response = fork.chat("Say hello briefly.")
        print(f"✅ Fork response: {fork_response[:100]}...")
        fork_success = True
        
        # Check if response indicates rate limit or error
        if "Rate limit" in fork_response or "Error" in fork_response:
            print("⚠️ Fork response indicates issues")
            fork_success = False
            
    except Exception as e:
        print(f"❌ Fork failed: {e}")
        fork_success = False
    
    # Final cost analysis
    final_cost = cost_tracker.get_total_cost()
    final_tokens = cost_tracker.get_total_tokens()
    fork_chat_cost = final_cost - after_parent_cost
    fork_chat_tokens = final_tokens - after_parent_tokens
    print(f"💰 Fork chat cost: ${fork_chat_cost:.6f} ({fork_chat_tokens:,} tokens)")
    
    # Get detailed metrics
    print("\n📊 METRICS ANALYSIS:")
    cost_summary = cost_tracker.get_summary()
    
    total_cached_tokens = 0
    for event in cost_summary.get('events', []):
        cached = event.get('cached_tokens', 0)
        total_cached_tokens += cached
        if cached > 0:
            print(f"  🎯 Found cached tokens: {cached:,}")
    
    print(f"\n📈 Summary:")
    print(f"  • Parent success: {'✅' if parent_success else '❌'}")
    print(f"  • Fork success: {'✅' if fork_success else '❌'}")
    print(f"  • Total cost: ${final_cost:.6f}")
    print(f"  • Total tokens: {final_tokens:,}")
    print(f"  • Cached tokens: {total_cached_tokens:,}")
    
    if final_tokens > 0:
        cache_efficiency = (total_cached_tokens / final_tokens) * 100
        print(f"  • Cache efficiency: {cache_efficiency:.1f}%")
        
        # Check for mathematical consistency
        if cache_efficiency > 100:
            print("  ❌ Cache efficiency >100% - mathematically impossible!")
        elif cache_efficiency > 0:
            print("  ✅ Cache efficiency is mathematically consistent")
        else:
            print("  ⚠️ No caching detected")
    
    # Test fork savings calculation
    fork_savings = cost_summary.get('fork_savings', {})
    if isinstance(fork_savings, dict) and not fork_savings.get('error'):
        savings_percent = fork_savings.get('savings_percent', 0)
        cache_eff = fork_savings.get('cache_efficiency_percent', 0)
        
        print(f"\n🔍 Fork Savings Analysis:")
        print(f"  • Savings: {savings_percent:.1f}%")
        print(f"  • Cache efficiency: {cache_eff:.1f}%")
        print(f"  • Mathematically consistent: {fork_savings.get('mathematically_consistent', False)}")
        
        if savings_percent > 100 or cache_eff > 100:
            print("  ❌ Metrics exceed 100% - still broken!")
        else:
            print("  ✅ Metrics are within realistic bounds")
    
    # Overall assessment
    print(f"\n🎯 OVERALL ASSESSMENT:")
    if parent_success and fork_success:
        print("  ✅ Both parent and fork completed successfully")
        print("  ✅ No rate limit errors detected")
        print("  ✅ System appears to be working")
    else:
        failed_count = sum(1 for success in [parent_success, fork_success] if not success)
        print(f"  ❌ {failed_count} out of 2 agents failed")
        print("  ❌ System still needs optimization")
    
    if total_cached_tokens > 0:
        print("  ✅ Real caching detected in provider responses")
    else:
        print("  ⚠️ No cached tokens - caching may not be working")
    
    print(f"\n🧪 Test completed!")


if __name__ == "__main__":
    test_fixed_forked_agents()