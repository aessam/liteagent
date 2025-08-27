#!/usr/bin/env python3
"""
Debug script to test caching implementation.
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


def debug_caching():
    """Debug the caching mechanism step by step."""
    print("🔍 DEBUGGING FORKEDAGENTS CACHING")
    print("="*50)
    
    # Reset cost tracker
    cost_tracker = get_cost_tracker()
    cost_tracker.events = []
    
    # Create a large system prompt
    large_content = "This is test content. " * 1000  # ~20K characters
    print(f"📊 Large content size: {len(large_content):,} characters")
    
    # Create parent agent
    print("\n🤖 Creating parent agent...")
    parent = ForkedAgent(
        model="claude-3-5-sonnet-20241022",
        name="debug_parent",
        system_prompt=f"You are a test agent. Here is large content: {large_content}",
        provider="anthropic",
        enable_caching=True,
        debug=True
    )
    
    print(f"✅ Parent created")
    print(f"   System prompt length: {len(parent.system_prompt):,} characters")
    print(f"   Memory system prompt length: {len(parent.memory.system_prompt):,} characters")
    print(f"   Memory messages count: {len(parent.memory.messages)}")
    if parent.memory.messages:
        first_msg = parent.memory.messages[0]
        print(f"   First message role: {first_msg.get('role')}")
        print(f"   First message content length: {len(str(first_msg.get('content', '')))}")
        print(f"   First message content preview: {str(first_msg.get('content', ''))[:100]}...")
    print(f"   Caching enabled: {parent.enable_caching}")
    print(f"   Supports caching: {parent.model_interface.supports_caching()}")
    
    # Create a fork
    print("\n🔀 Creating fork...")
    fork = parent.fork(name="debug_fork", prefill_role="test assistant")
    print(f"✅ Fork created")
    print(f"   Is fork: {fork._is_fork}")
    print(f"   System prompt length: {len(fork.system_prompt):,} characters")
    
    # Test with parent
    print("\n💬 Testing parent chat...")
    parent_response = parent.chat("Hello, respond briefly.")
    print(f"   Response: {parent_response[:100]}...")
    
    # Check costs after parent
    cost_after_parent = cost_tracker.get_total_cost()
    tokens_after_parent = cost_tracker.get_total_tokens()
    print(f"   Cost: ${cost_after_parent:.6f} ({tokens_after_parent:,} tokens)")
    
    # Test with fork
    print("\n💬 Testing fork chat...")
    fork_response = fork.chat("Hello, respond briefly.")
    print(f"   Response: {fork_response[:100]}...")
    
    # Check final costs
    final_cost = cost_tracker.get_total_cost()
    final_tokens = cost_tracker.get_total_tokens()
    fork_cost = final_cost - cost_after_parent
    fork_tokens = final_tokens - tokens_after_parent
    print(f"   Fork cost: ${fork_cost:.6f} ({fork_tokens:,} tokens)")
    
    # Get detailed cost summary
    print("\n💰 Cost Analysis:")
    cost_summary = cost_tracker.get_summary()
    print(f"   Total cost: ${cost_summary['total_cost']:.6f}")
    print(f"   Total tokens: {cost_summary['total_tokens']:,}")
    print(f"   Total events: {cost_summary['total_events']}")
    
    # Check for cached tokens
    if 'fork_savings' in cost_summary:
        fork_savings = cost_summary['fork_savings']
        if not isinstance(fork_savings, str):
            cached_tokens = fork_savings.get('cached_tokens', 0)
            print(f"   Cached tokens: {cached_tokens:,}")
            if cached_tokens > 0:
                print("   ✅ Caching is working!")
            else:
                print("   ❌ No cached tokens detected")
    
    # Check the raw events for debugging
    print(f"\n🔍 Raw Events:")
    for i, event in enumerate(cost_summary.get('events', []), 1):
        print(f"   {i}. {event.get('provider', 'unknown')}: "
              f"{event.get('total_tokens', 0):,} tokens, "
              f"cached: {event.get('cached_tokens', 0):,}")


if __name__ == "__main__":
    debug_caching()