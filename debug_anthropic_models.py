#!/usr/bin/env python3
"""
Debug script to check Anthropic models in models.dev API.
"""

import requests
import json

def debug_anthropic_models():
    """Debug the Anthropic models in models.dev API."""
    print("🔍 DEBUGGING ANTHROPIC MODELS")
    print("="*50)
    
    try:
        response = requests.get("https://models.dev/api.json", timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            if 'anthropic' in data:
                anthropic_data = data['anthropic']
                print(f"✅ Found Anthropic provider")
                print(f"Provider keys: {list(anthropic_data.keys())}")
                
                if 'models' in anthropic_data:
                    models = anthropic_data['models']
                    print(f"\n🤖 Found {len(models)} Anthropic models:")
                    
                    for model in models:
                        model_id = model.get('id', 'No ID')
                        print(f"  • {model_id}")
                        
                        # Check if this is our target model
                        if model_id == 'claude-3-5-sonnet-20241022':
                            print(f"    🎯 TARGET MODEL FOUND!")
                            print(json.dumps(model, indent=6))
                            
                else:
                    print("❌ No 'models' key in Anthropic data")
            else:
                print("❌ No 'anthropic' key in API response")
                
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    debug_anthropic_models()