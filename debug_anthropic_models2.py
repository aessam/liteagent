#!/usr/bin/env python3
"""
Debug script to check Anthropic models structure.
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
                models = anthropic_data.get('models', [])
                
                print(f"🤖 Found {len(models)} Anthropic models:")
                print(f"Models type: {type(models)}")
                
                if models:
                    print(f"First model type: {type(models[0])}")
                    print(f"First model: {models[0]}")
                    
                    if isinstance(models[0], str):
                        print("\n📝 Models are strings (IDs):")
                        for i, model in enumerate(models):
                            print(f"  {i+1}. {model}")
                            if model == 'claude-3-5-sonnet-20241022':
                                print(f"      🎯 FOUND TARGET MODEL!")
                    else:
                        print("\n📊 Models are objects:")
                        for model in models:
                            print(f"  • Type: {type(model)}")
                            if isinstance(model, dict):
                                print(f"    Keys: {list(model.keys())}")
                                print(f"    Content: {json.dumps(model, indent=4)}")
                
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_anthropic_models()