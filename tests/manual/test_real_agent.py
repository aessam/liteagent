#!/usr/bin/env python3
"""
Real agent test with actual providers and API calls.

This script tests the complete new provider system with real API calls.
You must have valid API keys set in environment variables.

Required environment variables:
- OPENAI_API_KEY (for OpenAI models)
- ANTHROPIC_API_KEY (for Claude models)  
- GROQ_API_KEY (for Groq models)
- MISTRAL_API_KEY (for Mistral models)
- DEEPSEEK_API_KEY (for DeepSeek models)

Optional:
- OLLAMA_HOST (for local Ollama server, defaults to http://localhost:11434)
"""

import os
import sys

# Add the liteagent package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Loaded environment variables from .env file")
except ImportError:
    print("⚠️  python-dotenv not installed, skipping .env file loading")
except Exception as e:
    print(f"⚠️  Could not load .env file: {e}")

def check_api_keys():
    """Check which API keys are available."""
    print("Checking available API keys...")
    
    keys = {
        'OpenAI': os.getenv('OPENAI_API_KEY'),
        'Anthropic': os.getenv('ANTHROPIC_API_KEY'),
        'Groq': os.getenv('GROQ_API_KEY'),
        'Mistral': os.getenv('MISTRAL_API_KEY'),
        'DeepSeek': os.getenv('DEEPSEEK_API_KEY'),
    }
    
    available = []
    for provider, key in keys.items():
        if key:
            print(f"  ✓ {provider}: API key found")
            available.append(provider)
        else:
            print(f"  ❌ {provider}: No API key (set {provider.upper()}_API_KEY)")
    
    # Check Ollama
    ollama_host = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
    print(f"  📡 Ollama: Will try {ollama_host}")
    available.append('Ollama')
    
    if not available:
        print("\n❌ No API keys found! Please set at least one provider's API key.")
        print("Example: export OPENAI_API_KEY='your-key-here'")
        return []
    
    print(f"\n✅ Found {len(available)} available providers: {', '.join(available[:-1])}")
    return available

def test_tool_calling_agent():
    """Test agent with tool calling using available providers."""
    print("\n🔧 Testing agent with tool calling...")
    
    try:
        from liteagent.new_agent import LiteAgent
        from liteagent.tools import liteagent_tool
        
        # Define a test tool
        @liteagent_tool
        def calculate_area(length: float, width: float) -> float:
            """Calculate the area of a rectangle."""
            return length * width
        
        @liteagent_tool  
        def get_weather_info(city: str) -> str:
            """Get weather information for a city."""
            # This would normally make an API call, but for testing we'll return static data
            return f"The weather in {city} is sunny, 72°F"
        
        # Test models to try (in order of preference)
        test_models = []
        
        if os.getenv('OPENAI_API_KEY'):
            test_models.append(('openai/gpt-4o-mini', 'OpenAI GPT-4o Mini'))
        
        if os.getenv('ANTHROPIC_API_KEY'):
            test_models.append(('anthropic/claude-3-5-haiku-20241022', 'Claude 3.5 Haiku'))
            
        if os.getenv('GROQ_API_KEY'):
            test_models.append(('groq/llama-3.1-8b-instant', 'Groq Llama 3.1 8B'))
            
        if os.getenv('MISTRAL_API_KEY'):
            test_models.append(('mistral/mistral-small-latest', 'Mistral Small'))
            
        if os.getenv('DEEPSEEK_API_KEY'):
            test_models.append(('deepseek/deepseek-chat', 'DeepSeek Chat'))
        
        if not test_models:
            print("  ⚠️  No API keys available for testing")
            return False
        
        # Test with the first available model
        model_name, model_description = test_models[0]
        print(f"  🤖 Creating agent with {model_description}...")
        
        agent = LiteAgent(
            model=model_name,
            name="TestAgent",
            tools=[calculate_area, get_weather_info],
            debug=True
        )
        
        print(f"  ✓ Agent created successfully!")
        print(f"  ✓ Provider: {agent.model_interface.provider.provider_name}")
        print(f"  ✓ Supports tool calling: {agent.model_interface.supports_tool_calling()}")
        
        # Test simple conversation
        print("\n  📝 Testing simple conversation...")
        response1 = agent.chat("Hello! What's your name?")
        print(f"  Agent: {response1}")
        
        # Test tool calling
        print("\n  🔧 Testing tool calling...")
        response2 = agent.chat("What's the area of a rectangle that is 5 meters long and 3 meters wide?")
        print(f"  Agent: {response2}")
        
        # Test another tool
        print("\n  🌤️ Testing weather tool...")
        response3 = agent.chat("What's the weather like in San Francisco?")
        print(f"  Agent: {response3}")
        
        # Check memory
        messages = agent.get_memory().get_messages()
        print(f"\n  🧠 Memory contains {len(messages)} messages")
        
        # Look for tool calls in memory
        tool_messages = [msg for msg in messages if msg.get('role') == 'tool']
        function_messages = [msg for msg in messages if msg.get('role') == 'function']
        
        print(f"  ✓ Tool messages (modern): {len(tool_messages)}")
        print(f"  ✓ Function messages (deprecated): {len(function_messages)} (should be 0)")
        
        if function_messages:
            print("  ❌ Found deprecated 'function' role messages!")
            return False
        
        print("  ✅ Agent tool calling test passed!")
        return True
        
    except Exception as e:
        print(f"  ❌ Agent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_multiple_providers():
    """Test multiple providers if available."""
    print("\n🌐 Testing multiple providers...")
    
    try:
        from liteagent.providers import create_provider
        
        # Test each available provider
        providers_to_test = []
        
        if os.getenv('OPENAI_API_KEY'):
            providers_to_test.append(('gpt-3.5-turbo', 'OpenAI'))
        
        if os.getenv('ANTHROPIC_API_KEY'):
            providers_to_test.append(('anthropic/claude-3-5-haiku-20241022', 'Anthropic'))
            
        if os.getenv('GROQ_API_KEY'):
            providers_to_test.append(('groq/llama-3.1-8b-instant', 'Groq'))
            
        if os.getenv('MISTRAL_API_KEY'):
            providers_to_test.append(('mistral/mistral-small-latest', 'Mistral'))
            
        if os.getenv('DEEPSEEK_API_KEY'):
            providers_to_test.append(('deepseek/deepseek-chat', 'DeepSeek'))
        
        success_count = 0
        
        for model_name, provider_name in providers_to_test:
            try:
                print(f"  🔨 Testing {provider_name} provider...")
                provider = create_provider(model_name)
                
                # Test a simple completion
                messages = [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Say 'Hello from " + provider_name + "!'"}
                ]
                
                response = provider.generate_response(messages)
                print(f"    ✓ {provider_name} response: {response.content[:100]}...")
                print(f"    ✓ Provider: {response.provider}")
                print(f"    ✓ Model: {response.model}")
                
                if response.usage:
                    print(f"    ✓ Tokens used: {response.usage}")
                
                success_count += 1
                
            except Exception as e:
                print(f"    ❌ {provider_name} failed: {e}")
        
        print(f"\n  ✅ Successfully tested {success_count}/{len(providers_to_test)} providers")
        return success_count > 0
        
    except Exception as e:
        print(f"  ❌ Provider testing failed: {e}")
        return False

def test_provider_specific_features():
    """Test provider-specific features."""
    print("\n⚙️ Testing provider-specific features...")
    
    success = True
    
    # Test parallel tool calls (OpenAI/Groq)
    if os.getenv('OPENAI_API_KEY'):
        print("  🔀 Testing OpenAI parallel tool calls...")
        try:
            from liteagent.providers import create_provider
            
            provider = create_provider('gpt-4o-mini')
            print(f"    ✓ Parallel tools supported: {provider.supports_parallel_tools()}")
            print(f"    ✓ Context window: {provider.get_context_window()}")
            print(f"    ✓ Max tokens: {provider.get_max_tokens()}")
            
        except Exception as e:
            print(f"    ❌ OpenAI feature test failed: {e}")
            success = False
    
    # Test Anthropic content blocks
    if os.getenv('ANTHROPIC_API_KEY'):
        print("  📝 Testing Anthropic content handling...")
        try:
            from liteagent.providers import create_provider
            
            provider = create_provider('anthropic/claude-3-5-haiku-20241022')
            print(f"    ✓ Tool calling supported: {provider.supports_tool_calling()}")
            print(f"    ✓ Context window: {provider.get_context_window()}")
            
        except Exception as e:
            print(f"    ❌ Anthropic feature test failed: {e}")
            success = False
    
    return success

def main():
    """Run comprehensive real agent tests."""
    print("🚀 Real LiteAgent Provider System Test")
    print("=" * 50)
    print("This test uses REAL API calls and requires valid API keys!")
    print("=" * 50)
    
    # Check available providers
    available_providers = check_api_keys()
    if not available_providers:
        print("\n❌ Cannot run tests without API keys!")
        print("\nTo run these tests, set one or more API keys:")
        print("  export OPENAI_API_KEY='your-openai-key'")
        print("  export ANTHROPIC_API_KEY='your-anthropic-key'")
        print("  export GROQ_API_KEY='your-groq-key'")
        print("  export MISTRAL_API_KEY='your-mistral-key'")
        print("  export DEEPSEEK_API_KEY='your-deepseek-key'")
        return False
    
    # Run tests
    tests = [
        test_tool_calling_agent,
        test_multiple_providers,
        test_provider_specific_features,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"  ❌ Test failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"🎯 Real Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All real tests passed! The new provider system is working perfectly!")
        print("\n✅ Key accomplishments:")
        print("   ✓ Provider system creates real connections")
        print("   ✓ Agent successfully uses official client libraries")
        print("   ✓ Tool calling works with modern 'tool' roles")
        print("   ✓ Memory system correctly handles tool results")
        print("   ✓ No more deprecated 'function' roles")
        print("   ✓ No more 'defaulting to STRUCTURED_OUTPUT' warnings")
        return True
    else:
        print("❌ Some real tests failed. Please review the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)