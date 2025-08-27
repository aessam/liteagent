#!/usr/bin/env python3
"""
Test the CORRECT sequencing: Parent establishes cache FIRST, then forks.
"""

import os
import sys
import time
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


def test_correct_sequence():
    """Test the correct sequencing to avoid rate limits."""
    print("🎯 TESTING CORRECT CACHE-FIRST SEQUENCE")
    print("="*60)
    
    # Reset cost tracker
    cost_tracker = get_cost_tracker()
    cost_tracker.events = []
    
    # Large content that definitely needs caching
    large_content = "This is large context for sequence testing. " * 1000  # ~45K chars
    print(f"📊 Large content size: {len(large_content):,} characters")
    
    # Step 1: Create parent (no cache yet)
    print(f"\n🤖 Step 1: Creating parent agent...")
    parent = ForkedAgent(
        model="claude-3-5-sonnet-20241022",
        name="sequence_parent",
        system_prompt=f"You are a comprehensive analysis system. CODEBASE: {large_content}",
        provider="anthropic",
        enable_caching=True,
        debug=True
    )
    print(f"✅ Parent created: {parent.context_id}")
    print(f"📋 Parent has {len(parent.memory.get_messages())} messages")
    print(f"🔍 Cache prepared: {parent._is_prepared_for_caching()}")
    
    # Step 2: FORCE cache establishment BEFORE any forks
    print(f"\n🔧 Step 2: Establishing cache (CRITICAL STEP)...")
    if not parent._is_prepared_for_caching():
        print("💡 Cache not prepared - establishing now...")
        parent._prepare_for_caching()
    else:
        print("✅ Cache already prepared")
        
    print(f"📋 Parent now has {len(parent.memory.get_messages())} messages")
    print(f"🔍 Cache prepared: {parent._is_prepared_for_caching()}")
    
    # Check cost after cache establishment
    cache_cost = cost_tracker.get_total_cost()
    cache_tokens = cost_tracker.get_total_tokens()
    print(f"💰 Cache establishment cost: ${cache_cost:.6f} ({cache_tokens:,} tokens)")
    
    # Step 3: Create forks (should use existing cache)
    print(f"\n🔀 Step 3: Creating forks (should inherit cache)...")
    
    fork1 = parent.fork(name="analyzer1", prefill_role="security expert")
    print(f"✅ Fork 1 created with {len(fork1.memory.get_messages())} messages")
    
    fork2 = parent.fork(name="analyzer2", prefill_role="performance expert") 
    print(f"✅ Fork 2 created with {len(fork2.memory.get_messages())} messages")
    
    # Step 4: Test fork conversations (should use cache)
    print(f"\n💬 Step 4: Testing fork conversations...")
    
    print(f"   🔐 Testing fork 1...")
    try:
        response1 = fork1.chat("Provide a brief analysis.")
        print(f"      ✅ Success: {response1[:50]}...")
        
        # Check cost
        cost_after_1 = cost_tracker.get_total_cost()
        tokens_after_1 = cost_tracker.get_total_tokens()
        fork1_cost = cost_after_1 - cache_cost
        fork1_tokens = tokens_after_1 - cache_tokens
        print(f"      💰 Fork 1 cost: ${fork1_cost:.6f} ({fork1_tokens:,} tokens)")
        
    except Exception as e:
        print(f"      ❌ Failed: {e}")
        if "rate_limit" in str(e).lower():
            print(f"      🚨 RATE LIMIT! Cache sequence failed!")
            return
    
    # Small delay to be extra safe
    print(f"   ⏱️ Brief pause before fork 2...")
    time.sleep(1)
    
    print(f"   ⚡ Testing fork 2...")
    try:
        response2 = fork2.chat("Provide a brief analysis.")
        print(f"      ✅ Success: {response2[:50]}...")
        
        # Final cost
        final_cost = cost_tracker.get_total_cost()
        final_tokens = cost_tracker.get_total_tokens()
        fork2_cost = final_cost - cost_after_1
        fork2_tokens = final_tokens - tokens_after_1
        print(f"      💰 Fork 2 cost: ${fork2_cost:.6f} ({fork2_tokens:,} tokens)")
        
    except Exception as e:
        print(f"      ❌ Failed: {e}")
        if "rate_limit" in str(e).lower():
            print(f"      🚨 RATE LIMIT! Even with correct sequence!")
    
    # Final analysis
    print(f"\n📊 SEQUENCE ANALYSIS:")
    total_cached = 0
    total_created = 0
    
    for event in cost_tracker.get_summary().get('events', []):
        cached = event.get('cache_read_input_tokens', 0) + event.get('cached_tokens', 0)
        created = event.get('cache_creation_input_tokens', 0)
        total_cached += cached
        total_created += created
        
        if cached > 0 or created > 0:
            agent = event.get('agent_name', 'unknown')
            print(f"   🎯 {agent}: created {created:,}, used {cached:,}")
    
    print(f"\n   📈 Final Summary:")
    print(f"      • Cache created: {total_created:,} tokens")
    print(f"      • Cache reused: {total_cached:,} tokens") 
    print(f"      • Total cost: ${final_cost:.6f}")
    
    if total_cached > total_created:
        print(f"      ✅ SUCCESS: More cache reuse than creation!")
        print(f"      ✅ Correct sequence prevented rate limits!")
    else:
        print(f"      ⚠️ Limited cache reuse - may need larger delays")
    
    print(f"\n🎯 Test completed!")


if __name__ == "__main__":
    test_correct_sequence()