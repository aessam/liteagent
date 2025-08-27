#!/usr/bin/env python3
"""
Debug script to verify what we're actually sending to the API.
"""

import os
import sys
import json
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


def debug_cache_payload():
    """Debug what's actually being sent in the API calls."""
    print("🔍 DEBUGGING CACHE PAYLOAD")
    print("="*50)
    
    # Reset cost tracker
    cost_tracker = get_cost_tracker()
    cost_tracker.events = []
    
    # Create a large system prompt
    large_content = "This is test content. " * 1000  # ~20K characters
    print(f"📊 Large content size: {len(large_content):,} characters")
    
    # Monkey-patch the Anthropic provider to log the actual request
    from liteagent.providers.anthropic_provider import AnthropicProvider
    original_generate = AnthropicProvider.generate_response
    
    def logged_generate(self, messages, tools=None, **kwargs):
        print(f"\n🔵 API CALL to {self.model_name}:")
        print(f"   Messages count: {len(messages)}")
        
        # Log each message's size
        for i, msg in enumerate(messages):
            role = msg.get('role', 'unknown')
            content = msg.get('content', '')
            
            if isinstance(content, str):
                content_size = len(content)
            elif isinstance(content, list):
                # For multimodal format, get the text size
                text_size = 0
                for item in content:
                    if isinstance(item, dict) and item.get('type') == 'text':
                        text_size += len(item.get('text', ''))
                content_size = text_size
            else:
                content_size = 0
                
            print(f"   Message {i+1} ({role}): {content_size:,} chars")
            
            # Show if cache_control is present
            if isinstance(content, list):
                for item in content:
                    if isinstance(item, dict) and 'cache_control' in item:
                        print(f"      → Has cache_control: {item['cache_control']}")
        
        # Call original method
        return original_generate(self, messages, tools, **kwargs)
    
    # Apply the monkey patch
    AnthropicProvider.generate_response = logged_generate
    
    # Create parent agent
    print("\n🤖 Creating parent agent...")
    parent = ForkedAgent(
        model="claude-3-5-sonnet-20241022",
        name="debug_parent",
        system_prompt=f"You are a test agent. Here is large content: {large_content}",
        provider="anthropic",
        enable_caching=True,
        debug=False  # Turn off debug to reduce noise
    )
    
    print(f"✅ Parent created with {len(parent.system_prompt):,} char system prompt")
    
    # Create a fork
    print("\n🔀 Creating fork...")
    fork = parent.fork(name="debug_fork", prefill_role="test assistant")
    print(f"✅ Fork created")
    
    # Test with parent (first call - should create cache)
    print("\n💬 Call 1: Parent agent (should CREATE cache)...")
    parent_response = parent.chat("Hello, respond briefly.")
    print(f"   Response: {parent_response[:50]}...")
    
    # Check costs after parent
    cost_after_parent = cost_tracker.get_total_cost()
    tokens_after_parent = cost_tracker.get_total_tokens()
    print(f"   Cost: ${cost_after_parent:.6f} ({tokens_after_parent:,} tokens)")
    
    # Test with fork (should use cache)
    print("\n💬 Call 2: Fork agent (should USE cache)...")
    fork_response = fork.chat("Hello, respond briefly.")
    print(f"   Response: {fork_response[:50]}...")
    
    # Check final costs
    final_cost = cost_tracker.get_total_cost()
    final_tokens = cost_tracker.get_total_tokens()
    fork_cost = final_cost - cost_after_parent
    fork_tokens = final_tokens - tokens_after_parent
    print(f"   Fork cost: ${fork_cost:.6f} ({fork_tokens:,} tokens)")
    
    # Test parent again (should use existing cache)
    print("\n💬 Call 3: Parent agent again (should USE existing cache)...")
    parent_response2 = parent.chat("Another brief message.")
    print(f"   Response: {parent_response2[:50]}...")
    
    # Final analysis
    print("\n📊 ANALYSIS:")
    cost_summary = cost_tracker.get_summary()
    
    if cost_summary['total_events'] >= 2:
        events = cost_summary.get('events', [])
        if len(events) >= 2:
            first_event = events[-3] if len(events) >= 3 else events[0]
            second_event = events[-2] if len(events) >= 3 else events[1]
            
            print(f"\n   First call tokens: {first_event.get('total_tokens', 0):,}")
            print(f"   Cache created: {first_event.get('cache_creation_input_tokens', 0):,} tokens")
            
            print(f"\n   Second call tokens: {second_event.get('total_tokens', 0):,}")
            print(f"   Cache read: {second_event.get('cache_read_input_tokens', 0):,} tokens")
            
            if first_event.get('cache_creation_input_tokens', 0) > 0 and \
               second_event.get('cache_read_input_tokens', 0) > 0:
                print("\n   ✅ CACHE IS WORKING: We're NOT resending the full context!")
                print("      The API recognizes the cached content and doesn't charge for it.")
            else:
                print("\n   ⚠️ Cache may not be working as expected")
    
    print("\n" + "="*50)
    print("KEY INSIGHT: Even though we send the same messages structure,")
    print("Anthropic's API recognizes cached content by its hash and doesn't")
    print("reprocess it. The cache_control markers tell the API what to cache.")
    print("="*50)


if __name__ == "__main__":
    debug_cache_payload()