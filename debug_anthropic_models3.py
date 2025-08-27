#!/usr/bin/env python3
"""
Debug script to properly check Anthropic models structure.
"""

import requests
import json

def debug_anthropic_models():
    """Debug the Anthropic models structure."""
    print("🔍 DEBUGGING ANTHROPIC MODELS STRUCTURE")
    print("="*50)
    
    try:
        response = requests.get("https://models.dev/api.json", timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            if 'anthropic' in data:
                anthropic_data = data['anthropic']
                models = anthropic_data.get('models', {})
                
                print(f"🤖 Anthropic models structure:")
                print(f"Models type: {type(models)}")
                
                if isinstance(models, dict):
                    print(f"Models keys: {list(models.keys())}")
                    
                    # Look for our target model
                    target_key = 'claude-3-5-sonnet-20241022'
                    if target_key in models:
                        print(f"\n🎯 FOUND TARGET MODEL: {target_key}")
                        model_data = models[target_key]
                        print(f"Model data type: {type(model_data)}")
                        print(json.dumps(model_data, indent=2))
                    else:
                        print(f"\n❌ Target model '{target_key}' not found")
                        
                        # Show a few examples
                        model_keys = list(models.keys())
                        print(f"\nSample models:")
                        for i, key in enumerate(model_keys[:3]):
                            print(f"  {i+1}. {key}")
                            model_data = models[key]
                            print(f"     Type: {type(model_data)}")
                            if isinstance(model_data, dict):
                                print(f"     Keys: {list(model_data.keys())}")
                
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_anthropic_models()