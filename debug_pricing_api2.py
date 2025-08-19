#!/usr/bin/env python3
"""
Debug script to check the actual structure of models.dev API.
"""

import requests
import json

def debug_pricing_api():
    """Debug the models.dev API structure."""
    print("🔍 DEBUGGING MODELS.DEV API STRUCTURE")
    print("="*50)
    
    try:
        response = requests.get("https://models.dev/api.json", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"Response type: {type(data)}")
            
            if isinstance(data, dict):
                print(f"Top-level keys: {list(data.keys())}")
                
                # Look for models in various places
                for key, value in data.items():
                    print(f"\n🔍 Key '{key}': {type(value)}")
                    if isinstance(value, list):
                        print(f"  List length: {len(value)}")
                        if len(value) > 0:
                            first_item = value[0]
                            print(f"  First item type: {type(first_item)}")
                            if isinstance(first_item, dict):
                                print(f"  First item keys: {list(first_item.keys())}")
                                if 'id' in first_item:
                                    print(f"  First item ID: {first_item['id']}")
                    elif isinstance(value, dict):
                        print(f"  Dict keys: {list(value.keys())[:10]}...")  # Show first 10 keys
                        
                # Check if there's a 'models' key or similar
                if 'models' in data:
                    models = data['models']
                    print(f"\n🤖 Found 'models' key with {len(models)} items")
                    
                    # Look for Claude models
                    claude_models = []
                    for model in models:
                        if isinstance(model, dict) and 'id' in model:
                            if 'claude' in model['id'].lower():
                                claude_models.append(model)
                                
                    print(f"Found {len(claude_models)} Claude models")
                    if claude_models:
                        print("First Claude model:")
                        print(json.dumps(claude_models[0], indent=2))
                        
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    debug_pricing_api()