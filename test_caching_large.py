#!/usr/bin/env python3
"""
Test script to verify caching works with larger content.
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


def test_large_content_caching():
    """Test caching with larger content."""
    print("🧪 TESTING CACHING WITH LARGE CONTENT")
    print("="*60)
    
    # Reset cost tracker
    cost_tracker = get_cost_tracker()
    cost_tracker.events = []
    
    # Create larger test content (should trigger caching)
    test_content = "This is a large test context for caching. " * 500  # ~20K characters
    print(f"📊 Large content size: {len(test_content):,} characters")
    
    # Create parent agent with caching
    print("\n🤖 Creating parent agent with large content...")
    parent = ForkedAgent(
        model="claude-3-5-sonnet-20241022",
        name="large_test_parent",
        system_prompt=f"You are a test agent with large context. Context: {test_content}",
        provider="anthropic",
        enable_caching=True,
        debug=False  # Reduce noise
    )
    print(f"✅ Parent created with {len(parent.system_prompt):,} char system prompt")
    
    # First call (should create cache)
    print("\n💬 Call 1: Parent (should CREATE cache)...")
    try:
        response1 = parent.chat("Hello, please respond briefly.")
        print(f"✅ Response 1: {response1[:50]}...")
        
        # Check cost/tokens after first call
        cost1 = cost_tracker.get_total_cost()
        tokens1 = cost_tracker.get_total_tokens()
        print(f"💰 Cost: ${cost1:.6f} ({tokens1:,} tokens)")
        
        # Check for cache creation
        events = cost_tracker.get_summary().get('events', [])
        if events:
            last_event = events[-1]
            cache_created = last_event.get('cache_creation_input_tokens', 0)
            if cache_created > 0:
                print(f"🎯 Cache created: {cache_created:,} tokens")
            else:
                print("⚠️ No cache creation detected")
        
    except Exception as e:
        print(f"❌ First call failed: {e}")
        return
    
    # Create fork
    print("\n🔀 Creating fork...")
    fork = parent.fork(name="large_test_fork", prefill_role="helpful assistant")
    print(f"✅ Fork created")
    
    # Second call with fork (should use cache)
    print("\n💬 Call 2: Fork (should USE cache)...")
    try:
        response2 = fork.chat("Hello again, please respond briefly.")
        print(f"✅ Response 2: {response2[:50]}...")
        
        # Check cost/tokens after second call
        cost2 = cost_tracker.get_total_cost()
        tokens2 = cost_tracker.get_total_tokens()
        call2_cost = cost2 - cost1
        call2_tokens = tokens2 - tokens1
        print(f"💰 Call 2 cost: ${call2_cost:.6f} ({call2_tokens:,} tokens)")
        
        # Check for cache usage
        events = cost_tracker.get_summary().get('events', [])
        if len(events) >= 2:
            last_event = events[-1]
            cache_read = last_event.get('cache_read_input_tokens', 0)
            if cache_read > 0:
                print(f"🎯 Cache used: {cache_read:,} tokens")
                print("✅ CACHING IS WORKING!")
            else:
                print("⚠️ No cache usage detected")
        
    except Exception as e:
        print(f"❌ Second call failed: {e}")
        return
    
    # Third call with parent again (should also use cache)
    print("\n💬 Call 3: Parent again (should USE existing cache)...")
    try:
        response3 = parent.chat("One more brief response please.")
        print(f"✅ Response 3: {response3[:50]}...")
        
        # Final analysis
        final_cost = cost_tracker.get_total_cost()
        final_tokens = cost_tracker.get_total_tokens()
        call3_cost = final_cost - cost2
        call3_tokens = final_tokens - tokens2
        print(f"💰 Call 3 cost: ${call3_cost:.6f} ({call3_tokens:,} tokens)")
        
    except Exception as e:
        print(f"❌ Third call failed: {e}")
    
    # Final summary
    print(f"\n📊 FINAL ANALYSIS:")
    summary = cost_tracker.get_summary()
    total_cached = sum(event.get('cache_read_input_tokens', 0) + 
                      event.get('cached_tokens', 0) 
                      for event in summary.get('events', []))
    total_created = sum(event.get('cache_creation_input_tokens', 0) 
                       for event in summary.get('events', []))
    
    print(f"  • Total cost: ${summary['total_cost']:.6f}")
    print(f"  • Total tokens: {summary['total_tokens']:,}")
    print(f"  • Cache created: {total_created:,} tokens")
    print(f"  • Cache used: {total_cached:,} tokens")
    
    if total_created > 0 or total_cached > 0:
        print("  ✅ Caching system is functional!")
    else:
        print("  ⚠️ Caching not detected - may need larger content or different model")
    
    print(f"\n🧪 Large content caching test completed!")


if __name__ == "__main__":
    test_large_content_caching()