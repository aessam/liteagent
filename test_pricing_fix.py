#!/usr/bin/env python3
"""
Test script to verify the pricing system fix.
"""

import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))

from liteagent.provider_cost_tracker import get_cost_tracker

def test_pricing_fix():
    """Test the fixed pricing system."""
    print("🧪 TESTING PRICING SYSTEM FIX")
    print("="*50)
    
    # Get the cost tracker (which loads pricing data)
    cost_tracker = get_cost_tracker()
    
    # Check if Claude pricing is loaded
    claude_keys = [
        "claude-3-5-sonnet-20241022",
        "anthropic/claude-3-5-sonnet-20241022",
    ]
    
    print(f"📊 Pricing cache size: {len(cost_tracker.pricing_cache)} entries")
    
    for key in claude_keys:
        if key in cost_tracker.pricing_cache:
            pricing = cost_tracker.pricing_cache[key]
            print(f"✅ Found pricing for {key}:")
            print(f"   • Input: ${pricing['input']:.6f} per 1K tokens")
            print(f"   • Output: ${pricing['output']:.6f} per 1K tokens") 
            print(f"   • Cache read: ${pricing['cache_read']:.6f} per 1K tokens")
            if 'cache_write' in pricing:
                print(f"   • Cache write: ${pricing['cache_write']:.6f} per 1K tokens")
        else:
            print(f"❌ No pricing found for {key}")
    
    # Test the pricing lookup method
    print(f"\n🔍 Testing pricing lookup:")
    pricing = cost_tracker._get_pricing("anthropic", "claude-3-5-sonnet-20241022")
    print(f"  Lookup result for anthropic/claude-3-5-sonnet-20241022:")
    print(f"   • Input: ${pricing['input']:.6f} per 1K tokens")
    print(f"   • Output: ${pricing['output']:.6f} per 1K tokens")
    print(f"   • Cache read: ${pricing['cache_read']:.6f} per 1K tokens")
    
    print(f"\n🧪 Pricing fix test completed!")

if __name__ == "__main__":
    test_pricing_fix()