#!/usr/bin/env python3
"""
Debug script to check the models.dev API response.
"""

import requests
import json

def debug_pricing_api():
    """Debug the models.dev API."""
    print("🔍 DEBUGGING MODELS.DEV API")
    print("="*50)
    
    try:
        print("📡 Calling https://models.dev/api.json...")
        response = requests.get("https://models.dev/api.json", timeout=10)
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response type: {type(data)}")
            print(f"Response length: {len(data) if isinstance(data, list) else 'N/A'}")
            
            # Look for Claude models
            claude_models = []
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and 'id' in item:
                        if 'claude' in item['id'].lower():
                            claude_models.append(item)
            
            print(f"\n🤖 Found {len(claude_models)} Claude models:")
            for model in claude_models[:3]:  # Show first 3
                print(f"  • {model.get('id', 'No ID')}")
                if 'cost' in model:
                    cost = model['cost']
                    print(f"    - Input: {cost.get('input', 'N/A')}")
                    print(f"    - Output: {cost.get('output', 'N/A')}")
                    print(f"    - Cache read: {cost.get('cache_read', 'N/A')}")
                    print(f"    - Cache write: {cost.get('cache_write', 'N/A')}")
                
            # Check if claude-3-5-sonnet-20241022 is there
            target_model = None
            for item in data:
                if isinstance(item, dict) and item.get('id') == 'claude-3-5-sonnet-20241022':
                    target_model = item
                    break
                    
            if target_model:
                print(f"\n✅ Found target model:")
                print(json.dumps(target_model, indent=2))
            else:
                print(f"\n❌ Target model 'claude-3-5-sonnet-20241022' not found")
                
        else:
            print(f"❌ HTTP error: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    debug_pricing_api()