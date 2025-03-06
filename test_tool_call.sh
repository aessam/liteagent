#!/bin/bash

# Load environment variables
if [ -f .env ]; then
    source .env
fi

# Ensure response directory exists
mkdir -p .tool_test/

# Default configuration
PROVIDER="ollama"
MODEL=""
RUN_TOOL_TEST=false
ALL_MODELS=false
LIST=false
RUN_ALL=false

# Function schema for tool calls
FUNCTION_SCHEMA='{
    "name": "get_weather",
    "description": "Get the current weather for a location",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city and state"
            }
        },
        "required": ["location"]
    }
}'

# Function to print usage
usage() {
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "  -p, --provider PROVIDER    Specify provider (ollama, openai, anthropic, groq, deepseek, mistral)"
    echo "  -m, --model MODEL          Specify model name"
    echo "  -l, --list                 List available models for the selected provider"
    echo "  -r, --run-test             Run tool calling test on specified model"
    echo "  --all                      Test all available models for the provider"
    echo "  --run-all                  List models AND run tests for all of them"
    echo "  -h, --help                 Show this help message"
    echo ""
    echo "Environment variables (can be set in .env file):"
    echo "  OPENAI_API_KEY             API key for OpenAI"
    echo "  ANTHROPIC_API_KEY          API key for Anthropic"
    echo "  GROQ_API_KEY               API key for Groq"
    echo "  DEEPSEEK_API_KEY           API key for Deepseek"
    echo "  MISTRAL_API_KEY            API key for Mistral"
    exit 1
}

# Function to list available models
list_models() {
    case "$PROVIDER" in
        "ollama")
            echo "Available Ollama models:"
            ollama list | tail -n +2
            ;;
        "openai")
            if [ -z "$OPENAI_API_KEY" ]; then
                echo "Error: OPENAI_API_KEY is not set"
                exit 1
            fi
            echo "Available OpenAI models:"
            curl -s "https://api.openai.com/v1/models" \
                -H "Authorization: Bearer $OPENAI_API_KEY" | jq -r '.data[].id'
            ;;
        "anthropic")
            if [ -z "$ANTHROPIC_API_KEY" ]; then
                echo "Error: ANTHROPIC_API_KEY is not set"
                exit 1
            fi
            echo "Available Anthropic models:"
            curl -s "https://api.anthropic.com/v1/models" \
                -H "x-api-key: $ANTHROPIC_API_KEY" \
                -H "anthropic-version: 2023-06-01" | jq -r '.data[].id'
            ;;
        "groq")
            if [ -z "$GROQ_API_KEY" ]; then
                echo "Error: GROQ_API_KEY is not set"
                exit 1
            fi
            echo "Available Groq models:"
            curl -s "https://api.groq.com/openai/v1/models" \
                -H "Authorization: Bearer $GROQ_API_KEY" \
                -H "Content-Type: application/json" | jq -r '.data[].id'
            ;;
        "deepseek")
            if [ -z "$DEEPSEEK_API_KEY" ]; then
                echo "Error: DEEPSEEK_API_KEY is not set"
                exit 1
            fi
            echo "Available Deepseek models:"
            curl -s "https://api.deepseek.com/v1/models" \
                -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
                -H "Content-Type: application/json" | jq -r '.data[].id'
            ;;
        "mistral")
            if [ -z "$MISTRAL_API_KEY" ]; then
                echo "Error: MISTRAL_API_KEY is not set"
                exit 1
            fi
            echo "Available Mistral models:"
            curl -s "https://api.mistral.ai/v1/models" \
                -H "Authorization: Bearer $MISTRAL_API_KEY" \
                -H "Content-Type: application/json" | jq -r '.data[].id'
            ;;
        *)
            echo "Unknown provider: $PROVIDER"
            exit 1
            ;;
    esac
}

# Function to get models list as array
get_models_list() {
    case "$PROVIDER" in
        "ollama")
            echo "$(ollama list | tail -n +2 | awk '{print $1}')"
            ;;
        "openai")
            echo "$(curl -s "https://api.openai.com/v1/models" \
                -H "Authorization: Bearer $OPENAI_API_KEY" | jq -r '.data[].id')"
            ;;
        "anthropic")
            echo "$(curl -s "https://api.anthropic.com/v1/models" \
                -H "x-api-key: $ANTHROPIC_API_KEY" \
                -H "anthropic-version: 2023-06-01" | jq -r '.data[].id')"
            ;;
        "groq")
            echo "$(curl -s "https://api.groq.com/openai/v1/models" \
                -H "Authorization: Bearer $GROQ_API_KEY" \
                -H "Content-Type: application/json" | jq -r '.data[].id')"
            ;;
        "deepseek")
            echo "$(curl -s "https://api.deepseek.com/v1/models" \
                -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
                -H "Content-Type: application/json" | jq -r '.data[].id')"
            ;;
        "mistral")
            echo "$(curl -s "https://api.mistral.ai/v1/models" \
                -H "Authorization: Bearer $MISTRAL_API_KEY" \
                -H "Content-Type: application/json" | jq -r '.data[].id')"
            ;;
    esac
}

# Function to test a model on Ollama
test_ollama_model() {
    local MODEL=$1
    local API_URL="http://localhost:11434/api/chat"
    local RESPONSE_FILE=".tool_test/response_ollama_${MODEL}.json"
    
    read -r -d '' PAYLOAD << EOM
{
    "model": "$MODEL",
    "messages": [
        {"role": "user", "content": "What's the weather like in San Francisco?"}
    ],
    "tools": [
        {
            "type": "function",
            "function": $FUNCTION_SCHEMA
        }
    ],
    "options": {
        "temperature": 0.1
    }
}
EOM

    echo -e "\n\033[1;36mTesting Ollama model: $MODEL\033[0m"
    curl -s -X POST "$API_URL" \
        -H "Content-Type: application/json" \
        -d "$PAYLOAD" > "$RESPONSE_FILE"

    # Analyze response
    if grep -q "does not support tools" "$RESPONSE_FILE"; then
        echo -e "\033[1;31m❌ Model explicitly doesn't support tools\033[0m"
        jq '.error' "$RESPONSE_FILE" 2>/dev/null
    elif grep -q "\"type\":\"function_call\"" "$RESPONSE_FILE" || grep -q "tool_calls" "$RESPONSE_FILE"; then
        echo -e "\033[1;32m✅ Success! Function call detected\033[0m"
        jq '.message.content' "$RESPONSE_FILE" 2>/dev/null
        echo -e "\nFunction call details:"
        jq '.message.tool_calls' "$RESPONSE_FILE" 2>/dev/null
    elif jq -e '.message.content' "$RESPONSE_FILE" >/dev/null 2>&1; then
        echo -e "\033[1;33m⚠️ Model responded conversationally without using the tool\033[0m"
        echo -e "Response content:"
        jq '.message.content' "$RESPONSE_FILE"
    else
        echo -e "\033[1;31m❌ Unknown response format\033[0m"
        jq '.' "$RESPONSE_FILE" 2>/dev/null
    fi
    
    echo -e "Response saved to: $RESPONSE_FILE"
}

# Function to test a model on OpenAI
test_openai_model() {
    local MODEL=$1
    local API_URL="https://api.openai.com/v1/chat/completions"
    local RESPONSE_FILE=".tool_test/response_openai_${MODEL//\//_}.json"
    
    if [ -z "$OPENAI_API_KEY" ]; then
        echo "Error: OPENAI_API_KEY is not set"
        exit 1
    fi
    
    read -r -d '' PAYLOAD << EOM
{
    "model": "$MODEL",
    "messages": [
        {"role": "user", "content": "What's the weather like in San Francisco?"}
    ],
    "tools": [
        {
            "type": "function",
            "function": $FUNCTION_SCHEMA
        }
    ],
    "temperature": 0.1
}
EOM

    echo -e "\n\033[1;36mTesting OpenAI model: $MODEL\033[0m"
    curl -s -X POST "$API_URL" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $OPENAI_API_KEY" \
        -d "$PAYLOAD" > "$RESPONSE_FILE"

    # Check for error
    if jq -e '.error' "$RESPONSE_FILE" >/dev/null 2>&1; then
        echo -e "\033[1;31m❌ Error:\033[0m"
        jq '.error' "$RESPONSE_FILE"
    # Check for tool calls
    elif jq -e '.choices[0].message.tool_calls' "$RESPONSE_FILE" >/dev/null 2>&1; then
        echo -e "\033[1;32m✅ Success! Function call detected\033[0m"
        jq '.choices[0].message.content' "$RESPONSE_FILE"
        echo -e "\nFunction call details:"
        jq '.choices[0].message.tool_calls' "$RESPONSE_FILE"
    else
        echo -e "\033[1;33m⚠️ Model responded without using the tool\033[0m"
        jq '.choices[0].message.content' "$RESPONSE_FILE"
    fi
    
    echo -e "Response saved to: $RESPONSE_FILE"
}

# Function to test a model on Anthropic
test_anthropic_model() {
    local MODEL=$1
    local API_URL="https://api.anthropic.com/v1/messages"
    local RESPONSE_FILE=".tool_test/response_anthropic_${MODEL//\//_}.json"
    
    if [ -z "$ANTHROPIC_API_KEY" ]; then
        echo "Error: ANTHROPIC_API_KEY is not set"
        exit 1
    fi
    
    # Using the correct format for Anthropic tools
    read -r -d '' PAYLOAD << EOM
{
    "model": "$MODEL",
    "messages": [
        {"role": "user", "content": "What's the weather like in San Francisco? Please use the tool to get the weather."}
    ],
    "tools": [
        {
            "name": "get_weather",
            "description": "Get the current weather for a location",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state"
                    }
                },
                "required": ["location"]
            }
        }
    ],
    "temperature": 0.1,
    "max_tokens": 1024
}
EOM

    echo -e "\n\033[1;36mTesting Anthropic model: $MODEL\033[0m"
    curl -s -X POST "$API_URL" \
        -H "Content-Type: application/json" \
        -H "x-api-key: $ANTHROPIC_API_KEY" \
        -H "anthropic-version: 2023-06-01" \
        -d "$PAYLOAD" > "$RESPONSE_FILE"

    # Check for error
    if jq -e '.error' "$RESPONSE_FILE" >/dev/null 2>&1; then
        echo -e "\033[1;31m❌ Error:\033[0m"
        jq '.error' "$RESPONSE_FILE"
    # Check for tool calls based on the example response format
    elif jq -e '.content[] | select(.type == "tool_use")' "$RESPONSE_FILE" >/dev/null 2>&1; then
        echo -e "\033[1;32m✅ Success! Tool use detected\033[0m"
        echo -e "Text content:"
        jq '.content[] | select(.type == "text").text' "$RESPONSE_FILE"
        echo -e "\nTool use details:"
        jq '.content[] | select(.type == "tool_use")' "$RESPONSE_FILE"
        echo -e "\nStop reason: $(jq -r '.stop_reason' "$RESPONSE_FILE")"
    elif jq -e '.content[]' "$RESPONSE_FILE" >/dev/null 2>&1; then
        echo -e "\033[1;33m⚠️ Model responded without using the tool\033[0m"
        echo -e "Response content:"
        jq '.content[]' "$RESPONSE_FILE" 
        echo -e "\nStop reason: $(jq -r '.stop_reason' "$RESPONSE_FILE")"
    else
        echo -e "\033[1;31m❌ Unknown response format\033[0m"
        jq '.' "$RESPONSE_FILE"
    fi
    
    echo -e "Response saved to: $RESPONSE_FILE"
}

# Function to test a model on Groq
test_groq_model() {
    local MODEL=$1
    local API_URL="https://api.groq.com/openai/v1/chat/completions"
    local RESPONSE_FILE=".tool_test/response_groq_${MODEL//\//_}.json"
    
    if [ -z "$GROQ_API_KEY" ]; then
        echo "Error: GROQ_API_KEY is not set"
        exit 1
    fi
    
    read -r -d '' PAYLOAD << EOM
{
    "model": "$MODEL",
    "messages": [
        {"role": "user", "content": "What's the weather like in San Francisco?"}
    ],
    "tools": [
        {
            "type": "function",
            "function": $FUNCTION_SCHEMA
        }
    ],
    "temperature": 0.1
}
EOM

    echo -e "\n\033[1;36mTesting Groq model: $MODEL\033[0m"
    curl -s -X POST "$API_URL" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $GROQ_API_KEY" \
        -d "$PAYLOAD" > "$RESPONSE_FILE"

    # Check for error
    if jq -e '.error' "$RESPONSE_FILE" >/dev/null 2>&1; then
        echo -e "\033[1;31m❌ Error:\033[0m"
        jq '.error' "$RESPONSE_FILE"
    # Check for tool calls
    elif jq -e '.choices[0].message.tool_calls' "$RESPONSE_FILE" >/dev/null 2>&1; then
        echo -e "\033[1;32m✅ Success! Function call detected\033[0m"
        jq '.choices[0].message.content' "$RESPONSE_FILE"
        echo -e "\nFunction call details:"
        jq '.choices[0].message.tool_calls' "$RESPONSE_FILE"
    else
        echo -e "\033[1;33m⚠️ Model responded without using the tool\033[0m"
        jq '.choices[0].message.content' "$RESPONSE_FILE" 2>/dev/null
    fi
    
    echo -e "Response saved to: $RESPONSE_FILE"
}

# Function to test a model on Deepseek
test_deepseek_model() {
    local MODEL=$1
    local API_URL="https://api.deepseek.com/v1/chat/completions"
    local RESPONSE_FILE=".tool_test/response_deepseek_${MODEL//\//_}.json"
    
    if [ -z "$DEEPSEEK_API_KEY" ]; then
        echo "Error: DEEPSEEK_API_KEY is not set"
        exit 1
    fi
    
    read -r -d '' PAYLOAD << EOM
{
    "model": "$MODEL",
    "messages": [
        {"role": "user", "content": "What's the weather like in San Francisco?"}
    ],
    "tools": [
        {
            "type": "function",
            "function": $FUNCTION_SCHEMA
        }
    ],
    "temperature": 0.1
}
EOM

    echo -e "\n\033[1;36mTesting Deepseek model: $MODEL\033[0m"
    curl -s -X POST "$API_URL" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
        -d "$PAYLOAD" > "$RESPONSE_FILE"

    # Check for error
    if jq -e '.error' "$RESPONSE_FILE" >/dev/null 2>&1; then
        echo -e "\033[1;31m❌ Error:\033[0m"
        jq '.error' "$RESPONSE_FILE"
    # Check for tool calls
    elif jq -e '.choices[0].message.tool_calls' "$RESPONSE_FILE" >/dev/null 2>&1; then
        echo -e "\033[1;32m✅ Success! Function call detected\033[0m"
        jq '.choices[0].message.content' "$RESPONSE_FILE"
        echo -e "\nFunction call details:"
        jq '.choices[0].message.tool_calls' "$RESPONSE_FILE"
    else
        echo -e "\033[1;33m⚠️ Model responded without using the tool\033[0m"
        jq '.choices[0].message.content' "$RESPONSE_FILE" 2>/dev/null
    fi
    
    echo -e "Response saved to: $RESPONSE_FILE"
}

# Function to test a model on Mistral
test_mistral_model() {
    local MODEL=$1
    local API_URL="https://api.mistral.ai/v1/chat/completions"
    local RESPONSE_FILE=".tool_test/response_mistral_${MODEL//\//_}.json"
    
    if [ -z "$MISTRAL_API_KEY" ]; then
        echo "Error: MISTRAL_API_KEY is not set"
        exit 1
    fi
    
    read -r -d '' PAYLOAD << EOM
{
    "model": "$MODEL",
    "messages": [
        {"role": "user", "content": "What's the weather like in San Francisco?"}
    ],
    "tools": [
        {
            "type": "function",
            "function": $FUNCTION_SCHEMA
        }
    ],
    "temperature": 0.1
}
EOM

    echo -e "\n\033[1;36mTesting Mistral model: $MODEL\033[0m"
    curl -s -X POST "$API_URL" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $MISTRAL_API_KEY" \
        -d "$PAYLOAD" > "$RESPONSE_FILE"

    # Check for error
    if jq -e '.error' "$RESPONSE_FILE" >/dev/null 2>&1; then
        echo -e "\033[1;31m❌ Error:\033[0m"
        jq '.error' "$RESPONSE_FILE"
    # Check for tool calls
    elif jq -e '.choices[0].message.tool_calls' "$RESPONSE_FILE" >/dev/null 2>&1; then
        echo -e "\033[1;32m✅ Success! Function call detected\033[0m"
        jq '.choices[0].message.content' "$RESPONSE_FILE"
        echo -e "\nFunction call details:"
        jq '.choices[0].message.tool_calls' "$RESPONSE_FILE"
    else
        echo -e "\033[1;33m⚠️ Model responded without using the tool\033[0m"
        jq '.choices[0].message.content' "$RESPONSE_FILE" 2>/dev/null
    fi
    
    echo -e "Response saved to: $RESPONSE_FILE"
}

# Function to test a model
test_model() {
    local MODEL_TO_TEST=$1
    
    case "$PROVIDER" in
        "ollama")
            test_ollama_model "$MODEL_TO_TEST"
            ;;
        "openai")
            test_openai_model "$MODEL_TO_TEST"
            ;;
        "anthropic")
            test_anthropic_model "$MODEL_TO_TEST"
            ;;
        "groq")
            test_groq_model "$MODEL_TO_TEST"
            ;;
        "deepseek")
            test_deepseek_model "$MODEL_TO_TEST"
            ;;
        "mistral")
            test_mistral_model "$MODEL_TO_TEST"
            ;;
        *)
            echo "Unknown provider: $PROVIDER"
            exit 1
            ;;
    esac
    
    echo -e "\033[1;33m--------------------------------------\033[0m"
}

# Process command line arguments directly to avoid getopt issues
while [[ $# -gt 0 ]]; do
    case "$1" in
        -p|--provider)
            PROVIDER="$2"
            shift 2
            ;;
        -m|--model)
            MODEL="$2"
            shift 2
            ;;
        -l|--list)
            LIST=true
            shift
            ;;
        -r|--run-test)
            RUN_TOOL_TEST=true
            shift
            ;;
        --all)
            ALL_MODELS=true
            shift
            ;;
        --run-all)
            RUN_ALL=true
            shift
            ;;
        -h|--help)
            usage
            ;;
        *)
            # If no flag is specified, assume it's a model name
            if [ -z "$MODEL" ]; then
                MODEL="$1"
                RUN_TOOL_TEST=true
            fi
            shift
            ;;
    esac
done

# Convert provider to lowercase
PROVIDER=$(echo "$PROVIDER" | tr '[:upper:]' '[:lower:]')

# Set default model based on provider if not specified
if [ -z "$MODEL" ] && [ "$ALL_MODELS" != true ] && [ "$RUN_ALL" != true ]; then
    case "$PROVIDER" in
        "ollama") MODEL="phi4" ;;
        "openai") MODEL="gpt-4-turbo" ;;
        "anthropic") MODEL="claude-3-sonnet-20240229" ;;
        "groq") MODEL="llama3-70b-8192" ;;
        "deepseek") MODEL="deepseek-chat" ;;
        "mistral") MODEL="mistral-large-latest" ;;
    esac
    if [ "$RUN_TOOL_TEST" = true ]; then
        echo "No model specified, using default model for $PROVIDER: $MODEL"
    fi
fi

# Run tests based on options
if [ "$LIST" = true ]; then
    # List models
    list_models
    if [ "$RUN_TOOL_TEST" = true ]; then
        # Also run test on specified model
        test_model "$MODEL"
    fi
elif [ "$RUN_ALL" = true ]; then
    # List and test all models
    echo -e "\033[1;32m======== AVAILABLE MODELS ========\033[0m"
    list_models
    echo -e "\033[1;32m======== TESTING ALL MODELS ========\033[0m"
    
    MODELS=$(get_models_list)
    if [ -z "$MODELS" ]; then
        echo "No models found for provider: $PROVIDER"
        exit 1
    fi
    
    for MODEL_TO_TEST in $MODELS; do
        test_model "$MODEL_TO_TEST"
    done
    
    echo -e "\n\033[1;32mTesting complete for all $PROVIDER models\033[0m"
elif [ "$ALL_MODELS" = true ]; then
    # Test all models for the provider
    echo "Testing all available models for $PROVIDER..."
    
    MODELS=$(get_models_list)
    if [ -z "$MODELS" ]; then
        echo "No models found for provider: $PROVIDER"
        exit 1
    fi
    
    for MODEL_TO_TEST in $MODELS; do
        test_model "$MODEL_TO_TEST"
    done
    
    echo -e "\n\033[1;32mTesting complete for all $PROVIDER models\033[0m"
elif [ "$RUN_TOOL_TEST" = true ]; then
    # Test a specific model
    test_model "$MODEL"
else
    # If no action specified, show help
    usage
fi