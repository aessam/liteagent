#!/usr/bin/env python3
"""
Test script to verify the HONEST caching approach works.

This tests the corrected architecture where:
1. Parent establishes shared cacheable context
2. All forks share the same cached conversation start
3. Only role-specific messages are unique per fork
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


def test_honest_caching():
    """Test the honest caching approach."""
    print("🎯 TESTING HONEST CACHING ARCHITECTURE")
    print("="*60)
    
    # Reset cost tracker
    cost_tracker = get_cost_tracker()
    cost_tracker.events = []
    
    # Create large test content that should definitely be cached
    large_content = "This is large context for honest caching test. " * 1000  # ~45K characters
    print(f"📊 Large content size: {len(large_content):,} characters")
    
    # Create parent agent
    print(f"\n🤖 Creating parent agent...")
    parent = ForkedAgent(
        model="claude-3-5-sonnet-20241022",
        name="honest_parent",
        system_prompt=f"You are a comprehensive code analysis system loaded with a large codebase. CODEBASE: {large_content}",
        provider="anthropic",
        enable_caching=True,
        debug=True
    )
    print(f"✅ Parent created: {parent.context_id}")
    
    # Check initial state
    initial_messages = parent.memory.get_messages()
    print(f"📋 Initial message count: {len(initial_messages)}")
    
    # Create first fork (this should trigger cache preparation)
    print(f"\n🔀 Creating first fork (should prepare caching)...")
    fork1 = parent.fork(
        name="security_auditor", 
        prefill_role="security expert focusing on vulnerabilities"
    )
    print(f"✅ Fork 1 created: {fork1.context_id}")
    
    # Check parent state after cache preparation
    after_prep_messages = parent.memory.get_messages()
    print(f"📋 Messages after cache prep: {len(after_prep_messages)}")
    
    if len(after_prep_messages) > len(initial_messages):
        print(f"🎯 Cache preparation messages added:")
        for i, msg in enumerate(after_prep_messages[len(initial_messages):], len(initial_messages) + 1):
            role = msg.get('role', 'unknown')
            content = msg.get('content', '')[:100]
            print(f"   {i}. {role}: {content}...")
    
    # Check fork 1 state
    fork1_messages = fork1.memory.get_messages()
    print(f"📋 Fork 1 message count: {len(fork1_messages)}")
    
    # Create second fork (should use existing cache preparation)
    print(f"\n🔀 Creating second fork (should reuse cached context)...")
    fork2 = parent.fork(
        name="performance_optimizer",
        prefill_role="performance expert focusing on optimization"
    )
    print(f"✅ Fork 2 created: {fork2.context_id}")
    
    # Check fork 2 state
    fork2_messages = fork2.memory.get_messages()
    print(f"📋 Fork 2 message count: {len(fork2_messages)}")
    
    # Verify both forks share the same cached prefix
    print(f"\n🔍 CACHE SHARING ANALYSIS:")
    
    # Find the shared portion (should be identical up to role definition)
    shared_count = 0
    for i in range(min(len(fork1_messages), len(fork2_messages))):
        if (fork1_messages[i].get('role') == fork2_messages[i].get('role') and 
            fork1_messages[i].get('content') == fork2_messages[i].get('content')):
            shared_count += 1
        else:
            break
    
    print(f"   🎯 Shared message count: {shared_count}")
    print(f"   📊 Fork 1 total messages: {len(fork1_messages)}")
    print(f"   📊 Fork 2 total messages: {len(fork2_messages)}")
    
    if shared_count >= 3:  # System + cache prep + assistant response
        print(f"   ✅ GOOD: Forks share {shared_count} messages (cacheable context)")
    else:
        print(f"   ❌ BAD: Only {shared_count} shared messages (insufficient for caching)")
    
    # Test fork conversations
    print(f"\n💬 Testing fork conversations...")
    
    # Fork 1 conversation
    print(f"   🔐 Testing security auditor...")
    try:
        response1 = fork1.chat("Please provide a brief security analysis.")
        print(f"      ✅ Response: {response1[:50]}...")
        success1 = True
    except Exception as e:
        print(f"      ❌ Failed: {e}")
        success1 = False
    
    # Check cost after fork 1
    cost1 = cost_tracker.get_total_cost()
    tokens1 = cost_tracker.get_total_tokens()
    print(f"      💰 Cost so far: ${cost1:.6f} ({tokens1:,} tokens)")
    
    # Fork 2 conversation
    print(f"   ⚡ Testing performance optimizer...")
    try:
        response2 = fork2.chat("Please provide a brief performance analysis.")
        print(f"      ✅ Response: {response2[:50]}...")
        success2 = True
    except Exception as e:
        print(f"      ❌ Failed: {e}")
        success2 = False
    
    # Final cost analysis
    final_cost = cost_tracker.get_total_cost()
    final_tokens = cost_tracker.get_total_tokens()
    fork2_cost = final_cost - cost1
    fork2_tokens = final_tokens - tokens1
    
    print(f"      💰 Fork 2 cost: ${fork2_cost:.6f} ({fork2_tokens:,} tokens)")
    print(f"      💰 Total cost: ${final_cost:.6f} ({final_tokens:,} tokens)")
    
    # Check for actual caching
    print(f"\n📊 CACHING EFFECTIVENESS:")
    
    total_cached_tokens = 0
    cache_creation_tokens = 0
    
    for event in cost_tracker.get_summary().get('events', []):
        cached = event.get('cache_read_input_tokens', 0) + event.get('cached_tokens', 0)
        created = event.get('cache_creation_input_tokens', 0)
        total_cached_tokens += cached
        cache_creation_tokens += created
        
        if cached > 0 or created > 0:
            agent = event.get('agent_name', 'unknown')
            print(f"   🎯 {agent}: created {created:,}, used {cached:,} cached tokens")
    
    print(f"\n   📈 Summary:")
    print(f"      • Cache created: {cache_creation_tokens:,} tokens")
    print(f"      • Cache used: {total_cached_tokens:,} tokens")
    print(f"      • Total tokens: {final_tokens:,}")
    
    if total_cached_tokens > 0:
        cache_efficiency = (total_cached_tokens / final_tokens) * 100
        print(f"      • Real cache efficiency: {cache_efficiency:.1f}%")
        print(f"      ✅ HONEST CACHING IS WORKING!")
    else:
        print(f"      ❌ No caching detected - architecture needs more work")
    
    print(f"\n🎯 OVERALL ASSESSMENT:")
    if success1 and success2:
        print(f"   ✅ Both forks completed successfully")
    else:
        print(f"   ❌ Some forks failed")
        
    if shared_count >= 3:
        print(f"   ✅ Forks share cacheable context")
    else:
        print(f"   ❌ Insufficient context sharing")
        
    if total_cached_tokens > 0:
        print(f"   ✅ Real caching detected from provider")
    else:
        print(f"   ❌ No caching detected")
    
    print(f"\n🧪 Honest caching test completed!")


if __name__ == "__main__":
    test_honest_caching()