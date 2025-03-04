#!/bin/bash

# Function to handle cleanup on exit
cleanup() {
  rm -f "$RESPONSE_FILE"
}
trap cleanup EXIT

# Create a temporary file for the response
RESPONSE_FILE=$(mktemp)

# Configuration
API_URL="http://localhost:11434/api/chat"
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

# Function to test a single model
test_model() {
  local MODEL=$1
  
  # Prepare the request payload
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

  # Make the API request
  echo -e "\n\033[1;36mTesting model: $MODEL\033[0m"
  echo "Sending request to Ollama..."
  curl -s -X POST "$API_URL" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD" > "$RESPONSE_FILE"

  # Check for specific error pattern
  if grep -q "does not support tools" "$RESPONSE_FILE"; then
    echo -e "\033[1;31m❌ Model explicitly doesn't support tools\033[0m"
    jq '.error' "$RESPONSE_FILE" 2>/dev/null
  # Check if the response contains a function call
  elif grep -q "\"type\":\"function_call\"" "$RESPONSE_FILE" || grep -q "tool_calls" "$RESPONSE_FILE"; then
    echo -e "\033[1;32m✅ Success! Function call detected\033[0m"
    jq '.message.content' "$RESPONSE_FILE" 2>/dev/null
    echo -e "\nFunction call details:"
    jq '.message.tool_calls' "$RESPONSE_FILE" 2>/dev/null
  # Handle conversational response (like llama3-groq-tool-use)
  elif jq -e '.message.content' "$RESPONSE_FILE" >/dev/null 2>&1; then
    echo -e "\033[1;33m⚠️ Model responded conversationally without using the tool\033[0m"
    echo -e "Response content:"
    jq '.message.content' "$RESPONSE_FILE"
    echo -e "\nThis model might claim to support tools but doesn't implement them correctly."
  else
    echo -e "\033[1;31m❌ Unknown response format\033[0m"
    jq '.' "$RESPONSE_FILE" 2>/dev/null
  fi
  
  echo -e "\033[1;33m--------------------------------------\033[0m"
}

# Main logic
if [ "$1" = "--all" ]; then
  # Get all models
  echo "Testing all available models..."
  MODELS=$(ollama list | tail -n +2 | awk '{print $1}')
  
  for MODEL in $MODELS; do
    test_model "$MODEL"
  done
  
  echo -e "\n\033[1;32mTesting complete for all models\033[0m"
else
  # Test a single model (default to phi4 if none specified)
  MODEL=${1:-"phi4"}
  test_model "$MODEL"
fi