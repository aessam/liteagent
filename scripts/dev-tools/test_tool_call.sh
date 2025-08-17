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

# Centralized function for making HTTP requests
# Usage: request "URL" "HEADERS" "BODY" "OUTPUT_FILE"
request() {
    local URL=$1
    local HEADERS=$2
    local BODY=$3
    local OUTPUT_FILE=$4
    
    # Create a temporary file for the request body if provided
    if [ -n "$BODY" ]; then
        local TEMP_FILE=$(mktemp)
        echo "$BODY" > "$TEMP_FILE"
        
        # Execute curl with body
        eval "curl -s -X POST \"$URL\" $HEADERS -d @\"$TEMP_FILE\"" > "$OUTPUT_FILE"
        
        # Clean up temp file
        rm "$TEMP_FILE"
    else
        # Execute curl without body (GET request)
        eval "curl -s \"$URL\" $HEADERS" > "$OUTPUT_FILE"
    fi
    
    # Check if the output file exists and has content
    if [ ! -s "$OUTPUT_FILE" ]; then
        echo "Error: Request failed or returned empty response" >&2
        return 1
    fi
    
    return 0
}


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

# Function to generate payload based on provider
get_payload() {
    local provider=$1
    local model=$2
    local is_simulated=${3:-false}
    
    if [ "$is_simulated" = "true" ]; then
        # Simulated tools payload - works with any provider
echo '{
    "model": "'$model'",
    "messages": [
        {
            "role": "system", 
            "content": "You have access to these functions. When using any function, any thoughts or reasoning should be in the \"reason\" field, and the parameters should be in the \"parameters\" field. Respond exactly like this format: {\"name\": function_name, \"reason\":reason_for_calling_function, \"parameters\": {parameter_dictionary}}

Available functions:
1. get_weather - Takes a location parameter
2. search_web - Takes a query parameter
3. calculate - Takes num1, num2, and operation parameters

Important: Don'\''t use variables, replace parameter values with actual requested info, no explanations before/after tool call, no markdown."
        },
        {
            "role": "user", 
            "content": "What'\''s the weather like in San Francisco?"
        }
    ],
    "stream": false
}'
    elif [ "$provider" = "anthropic" ]; then
        # Anthropic has a different format for tools
        echo '{
    "model": "'$model'",
    "messages": [
        {"role": "user", "content": "What'\''s the weather like in San Francisco? Please use the tool to get the weather."}
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
    "max_tokens": 1024
}'
    else
        # Standard format for all other providers
        echo '{
    "model": "'$model'",
    "messages": [
        {"role": "user", "content": "What'\''s the weather like in San Francisco?"}
    ],
    "tools": [
        {
            "type": "function",
            "function": '$FUNCTION_SCHEMA'
        }
    ]
}'
    fi
}

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
    # Use tr to capitalize the first letter of provider name
    local DISPLAY_PROVIDER=$(echo "$PROVIDER" | tr '[:lower:]' '[:upper:]' | cut -c1)$(echo "$PROVIDER" | cut -c2-)
    echo "Available $DISPLAY_PROVIDER models:"
    
    if [ "$PROVIDER" = "ollama" ]; then
        # Special case for Ollama which uses a local command
        ollama list | tail -n +2
    else
        # Create a temporary file for the response
        local TEMP_RESPONSE=$(mktemp)
        
        # Make the request using the request function
        if request "$LIST_MODEL_URL" "$HEADERS" "" "$TEMP_RESPONSE"; then
            # Output the model IDs
            jq -r '.data[].id' "$TEMP_RESPONSE"
        else
            echo "Failed to fetch models list"
        fi
        
        # Clean up
        rm "$TEMP_RESPONSE"
    fi
}

# Function to get models list as array
get_models_list() {
    if [ "$PROVIDER" = "ollama" ]; then
        # Special case for Ollama which uses a local command
        echo "$(ollama list | tail -n +2 | awk '{print $1}')"
    else
        # Create a temporary file for the response
        local TEMP_RESPONSE=$(mktemp)
        
        # Make the request using the request function
        if request "$LIST_MODEL_URL" "$HEADERS" "" "$TEMP_RESPONSE"; then
            # Output the model IDs
            local MODELS=$(jq -r '.data[].id' "$TEMP_RESPONSE")
            rm "$TEMP_RESPONSE"
            echo "$MODELS"
        else
            rm "$TEMP_RESPONSE"
            echo ""
        fi
    fi
}

# Function to test simulated tools for any provider
test_simulated_tools() {
    local PROVIDER=$1
    local MODEL=$2
    local RESPONSE_FILE=".tool_test/response_${PROVIDER}_${MODEL//\//_}_simulated.json"
    
    # Prepare JSON payload
    local PAYLOAD=$(get_payload "$PROVIDER" "$MODEL" true)

    echo -e "\n\033[1;36mTesting $PROVIDER model with simulated tools: $MODEL\033[0m"
    
    # Use the centralized variables
    request "$CHAT_URL" "$HEADERS" "$PAYLOAD" "$RESPONSE_FILE"
    
    # Simply output the content
    echo "Response saved to: $RESPONSE_FILE"
    CONTENT=$(jq -r '.message.content' "$RESPONSE_FILE")
    if echo "$CONTENT" | jq &>/dev/null; then
        echo "$CONTENT" | jq
    else
        echo "❌ [Failed parsing] ->>> $CONTENT"
    fi
}

# Generic function to test a model for any provider
test_model_for_provider() {
    local PROVIDER=$1
    local MODEL=$2
    
    # Test official tool call API
    local RESPONSE_FILE=".tool_test/response_${PROVIDER}_${MODEL//\//_}.json"
    local PAYLOAD=$(get_payload "$PROVIDER" "$MODEL" false)

    echo -e "\n\033[1;36mTesting $PROVIDER model with official tools API: $MODEL\033[0m"
    
    # Use the centralized variables
    request "$CHAT_URL" "$HEADERS" "$PAYLOAD" "$RESPONSE_FILE"

    # Simply output the response
    echo "Response saved to: $RESPONSE_FILE"
    jq '.' "$RESPONSE_FILE"
    
    # Now also test with simulated tools for all providers
    test_simulated_tools "$PROVIDER" "$MODEL"
}

# Function to test a model
test_model() {
    local MODEL_TO_TEST=$1
    
    # Just use the generic test function with the current provider
    test_model_for_provider "$PROVIDER" "$MODEL_TO_TEST"
    
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

# Set provider-specific variables
LIST_MODEL_URL=""
CHAT_URL=""
HEADERS=""
API_KEY=""

case "$PROVIDER" in
    "ollama")
        LIST_MODEL_URL=""  # No URL for Ollama, using local command
        CHAT_URL="http://localhost:11434/api/chat"
        HEADERS="-H \"Content-Type: application/json\""
        ;;
    "openai")
        API_KEY="$OPENAI_API_KEY"
        LIST_MODEL_URL="https://api.openai.com/v1/models"
        CHAT_URL="https://api.openai.com/v1/chat/completions"
        HEADERS="-H \"Content-Type: application/json\" -H \"Authorization: Bearer $OPENAI_API_KEY\""
        ;;
    "anthropic")
        API_KEY="$ANTHROPIC_API_KEY"
        LIST_MODEL_URL="https://api.anthropic.com/v1/models"
        CHAT_URL="https://api.anthropic.com/v1/messages"
        HEADERS="-H \"Content-Type: application/json\" -H \"x-api-key: $ANTHROPIC_API_KEY\" -H \"anthropic-version: 2023-06-01\""
        TOOL_FORMAT="anthropic"  # Anthropic has different tool format
        ;;
    "groq")
        API_KEY="$GROQ_API_KEY"
        LIST_MODEL_URL="https://api.groq.com/openai/v1/models"
        CHAT_URL="https://api.groq.com/openai/v1/chat/completions"
        HEADERS="-H \"Content-Type: application/json\" -H \"Authorization: Bearer $GROQ_API_KEY\""
        ;;
    "deepseek")
        API_KEY="$DEEPSEEK_API_KEY"
        LIST_MODEL_URL="https://api.deepseek.com/v1/models"
        CHAT_URL="https://api.deepseek.com/v1/chat/completions"
        HEADERS="-H \"Content-Type: application/json\" -H \"Authorization: Bearer $DEEPSEEK_API_KEY\""
        ;;
    "mistral")
        API_KEY="$MISTRAL_API_KEY"
        LIST_MODEL_URL="https://api.mistral.ai/v1/models"
        CHAT_URL="https://api.mistral.ai/v1/chat/completions"
        HEADERS="-H \"Content-Type: application/json\" -H \"Authorization: Bearer $MISTRAL_API_KEY\""
        ;;
    *)
        echo "Unknown provider: $PROVIDER"
        exit 1
        ;;
esac

# Check API key for providers that need it
if [ "$PROVIDER" != "ollama" ] && [ -z "$API_KEY" ]; then
    echo "Error: API key for $PROVIDER is not set"
    exit 1
fi

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