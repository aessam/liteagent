"""
Provider-specific role configurations for LiteAgent.

This module defines expected message role configurations for different model providers,
helping ensure compatibility across different LLM APIs.
"""

from typing import Dict, List, Set, Optional, Any

# Define supported roles for each provider
PROVIDER_ROLES = {
    "openai": {"system", "user", "assistant", "function", "tool"},
    "anthropic": {"system", "user", "assistant"},  # No function or tool roles
    "mistral": {"system", "user", "assistant", "tool"},  # No function role
    "deepseek": {"system", "user", "assistant", "tool"},  # No function role
    "groq": {"system", "user", "assistant", "function", "tool"},
    "ollama": {"system", "user", "assistant"}  # Ollama needs special handling for tools
}

# Define which providers require specific role sequences
PROVIDER_CONSTRAINTS = {
    "mistral": {
        "last_message_role": {"user", "tool"},  # Last message must be user or tool
        "strict_sequence": True,  # Enforces strict role alternation
        "system_position": "first_only"  # System message can only appear at the beginning
    },
    "deepseek": {
        "last_message_role": {"user", "tool"},  # Last message must be user or tool
        "strict_sequence": True,  # Enforces strict role alternation
        "system_position": "first_only"  # System message can only appear at the beginning
    },
    "ollama": {
        "last_message_role": {"user"},  # Last message must be user 
        "strict_sequence": True,  # Enforces strict role alternation
        "system_position": "first_only",  # System message can only appear at the beginning
        "embed_tool_calls": True  # Embed tool calls in user messages
    }
}

def process_messages_for_provider(messages: List[Dict], provider: str) -> List[Dict]:
    """
    Process messages to ensure compatibility with specific model providers.
    
    Args:
        messages: List of message dictionaries
        provider: Provider name (e.g., "openai", "anthropic", "mistral")
        
    Returns:
        Processed list of messages compatible with the provider
    """
    normalized_provider = provider.lower()
    
    # Extract the base provider (e.g., "openai" from "openai/gpt-4")
    if "/" in normalized_provider:
        normalized_provider = normalized_provider.split("/")[0]
    
    # Use OpenAI as default if provider not found
    if normalized_provider not in PROVIDER_ROLES:
        normalized_provider = "openai"
    
    # Get the supported roles for this provider
    supported_roles = PROVIDER_ROLES.get(normalized_provider, PROVIDER_ROLES["openai"])
    constraints = PROVIDER_CONSTRAINTS.get(normalized_provider, {})
    
    # Handle Ollama system prompt with tools
    if normalized_provider == "ollama":
        for msg in messages:
            if msg.get("role") == "system" and "tools" in msg:
                tools = msg.get("tools", [])
                if tools:  # Only augment if there are actual tools
                    tools_description = "\n".join([
                        f"- {tool.get('name', 'unknown')}: {tool.get('description', 'No description')}"
                        for tool in tools
                    ])
                    current_content = msg.get("content", "")
                    augmented_content = (
                        f"{current_content}\n\n"
                        f"You have access to the following tools:\n{tools_description}\n\n"
                        f"To use a tool, clearly indicate the tool name and parameters like this:\n"
                        f"'I'll use the [TOOL_NAME] tool with parameters: parameter1=value1, parameter2=value2'\n"
                        f"After seeing a tool result, process it and continue helping the user."
                    )
                    msg["content"] = augmented_content
    
    # Process messages
    processed_messages = []
    seen_assistant = False
    system_messages = []
    
    # First pass: Collect system messages and process other messages
    for msg in messages:
        role = msg.get("role", "")
        
        # Special handling for system messages based on constraints
        if role == "system":
            if constraints.get("system_position") == "first_only" and seen_assistant:
                # Convert system message after assistant to user message
                processed_messages.append({
                    "role": "user",
                    "content": f"System instruction: {msg.get('content', '')}"
                })
            else:
                system_messages.append(msg)
            continue
        
        # Mark if we've seen an assistant message
        if role == "assistant":
            seen_assistant = True
        
        # Special handling for Ollama - embed tool calls and responses in user/assistant messages
        if constraints.get("embed_tool_calls") and (role == "function" or role == "tool"):
            tool_name = msg.get("name", "unknown")
            tool_content = msg.get("content", "")
            
            # Format the tool response as a user message for Ollama
            processed_messages.append({
                "role": "user",
                "content": f"Tool result from {tool_name}: {tool_content}\nPlease process this result and continue."
            })
            continue
            
        # Handle unsupported roles
        if role not in supported_roles:
            if role == "function" or (role == "tool" and normalized_provider == "anthropic"):
                # Convert function/tool message to assistant message
                processed_messages.append({
                    "role": "assistant",
                    "content": f"Function {msg.get('name', 'unknown')} returned: {msg.get('content', '')}"
                })
            else:
                # For other unsupported roles, convert to user message
                processed_messages.append({
                    "role": "user",
                    "content": msg.get("content", "")
                })
        else:
            # Role is supported, keep it as is
            processed_messages.append(msg)
    
    # Reorganize messages with system messages at the beginning
    if constraints.get("system_position") == "first_only" and system_messages:
        final_messages = system_messages + processed_messages
    else:
        final_messages = processed_messages
    
    # Apply strict sequence constraints if needed
    if constraints.get("strict_sequence", False) and final_messages:
        reorganized_messages = []
        prev_role = None
        
        for i, msg in enumerate(final_messages):
            role = msg.get("role", "")
            
            # Handle first message (usually system)
            if prev_role is None:
                reorganized_messages.append(msg)
                prev_role = role
                continue
                
            # For subsequent messages, ensure proper alternation
            if role == prev_role and role != "system":
                # If same role appears consecutively (except system), force alternation
                if role == "user":
                    # Add a placeholder assistant message
                    reorganized_messages.append({"role": "assistant", "content": "I understand."})
                    reorganized_messages.append(msg)
                    prev_role = role
                elif role == "assistant":
                    # Add a placeholder user message
                    reorganized_messages.append({"role": "user", "content": "Please continue."})
                    reorganized_messages.append(msg)
                    prev_role = role
                else:
                    # For other consecutive roles, just append
                    reorganized_messages.append(msg)
                    prev_role = role
            else:
                # Roles are different, no need for alternation
                reorganized_messages.append(msg)
                prev_role = role
        
        final_messages = reorganized_messages
    
    # Check last message role constraint
    if "last_message_role" in constraints and final_messages:
        allowed_last_roles = constraints["last_message_role"]
        current_last_role = final_messages[-1].get("role")
        
        if current_last_role not in allowed_last_roles:
            # Add an empty user message to satisfy the constraint
            final_messages.append({"role": "user", "content": "Continue."})
    
    return final_messages 