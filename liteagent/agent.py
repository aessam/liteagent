"""
LiteAgent - Core agent implementation.

This module contains the main LiteAgent class that handles conversation,
function calling, and response processing.
"""

import json
import time
import litellm
from .tools import get_tools, get_function_definitions
from .utils import logger, log_completion_request, log_completion_response

class LiteAgent:
    """
    A lightweight agent that uses LiteLLM for LLM interactions and tool usage.
    """
    
    DEFAULT_SYSTEM_PROMPT = """You are a helpful AI assistant. 
Use the provided functions when needed to answer the user's question. 
After calling a function and receiving its result, you MUST provide a complete 
text response to the user. Do not call functions repeatedly if you already 
have the information needed."""

    # Models known not to support function calling
    FUNCTION_CALL_UNSUPPORTED = [
        "text-davinci", "text-ada", "text-babbage", "text-curie", 
        "ollama/", "phi", "llama", "mistral"
    ]

    def __init__(self, model="gpt-3.5-turbo", name="Agent", system_prompt=None, debug=False, drop_params=True):
        """
        Initialize the LiteAgent.
        
        Args:
            model (str): The LLM model to use
            name (str): Name of the agent
            system_prompt (str, optional): System prompt to use. Defaults to DEFAULT_SYSTEM_PROMPT.
            debug (bool, optional): Whether to print debug information. Defaults to False.
            drop_params (bool, optional): Whether to drop unsupported parameters. Defaults to True.
        """
        self.model = model
        self.name = name
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.debug = debug
        self.drop_params = drop_params
        # Set global litellm setting for dropping unsupported parameters
        litellm.drop_params = self.drop_params
        self.reset_memory()

    def reset_memory(self):
        """Reset conversation history to only include the system prompt."""
        self.memory = [{"role": "system", "content": self.system_prompt}]
        self.last_function_call = None

    def _log(self, message, level="debug"):
        """Log a message at the specified level if debug mode is enabled."""
        if self.debug:
            log_method = getattr(logger, level.lower(), logger.debug)
            log_method(message)

    def model_supports_tool_calling(self):
        """
        Check if the current model supports function/tool calling.
        
        Returns:
            bool: Whether the model supports tool calling
        """
        model_lower = self.model.lower()
        
        # Check against list of models known not to support function calling
        for unsupported in self.FUNCTION_CALL_UNSUPPORTED:
            if unsupported.lower() in model_lower:
                logger.info(f"Model '{self.model}' is detected as not supporting function calling")
                return False
                
        # Default to assuming support for other models
        return True

    def _get_tool_description_in_prompt(self):
        """
        For models that don't support function calling, create a text description
        of available tools to include in the prompt.
        
        Returns:
            str: A text description of available tools
        """
        tools = get_tools()
        if not tools:
            return ""
            
        tool_descriptions = []
        for name, tool_data in tools.items():
            schema = tool_data["schema"]
            params = schema.schema().get("properties", {})
            param_desc = ", ".join([f"{p} ({t.get('type', 'any')})" 
                                  for p, t in params.items()])
            
            description = schema.__doc__ or f"Function to {name}"
            tool_descriptions.append(f"Function: {name}({param_desc})\nDescription: {description}\n")
            
        if tool_descriptions:
            return ("You have access to the following functions. To use them, output exactly "
                   "[FUNCTION_CALL] function_name(param1=value1, param2=value2) [/FUNCTION_CALL].\n\n" + 
                   "\n".join(tool_descriptions))
        return ""

    def chat(self, user_input):
        """
        Process a single user query, potentially calling tools if needed.
        
        Args:
            user_input (str): User's query
            
        Returns:
            str: Agent's response
        """
        # For models that don't support function calling, add tool descriptions to the system prompt
        if not self.model_supports_tool_calling():
            tool_descriptions = self._get_tool_description_in_prompt()
            if tool_descriptions and self.memory[0]["role"] == "system":
                # Update the system prompt with tool descriptions
                self.memory[0]["content"] = f"{self.system_prompt}\n\n{tool_descriptions}"
                
        self.memory.append({"role": "user", "content": user_input})
        max_iterations = 5  # Prevent infinite loops
        iteration = 0

        while iteration < max_iterations:
            iteration += 1
            logger.info(f"Iteration {iteration}")

            # Get response from LLM
            try:
                response = self._get_llm_response()
            except Exception as e:
                logger.error(f"Error calling LLM API: {str(e)}")
                return f"Error calling LLM API: {str(e)}"

            # Process the response
            result = self._process_response(response, iteration)
            if result is not None:
                return result

        # Fallback if no non-empty answer is produced
        return "No complete response generated after maximum iterations."

    def _get_llm_response(self):
        """
        Get a response from the LLM.
        
        Returns:
            The response from the LLM
        """
        kwargs = {"model": self.model, "messages": self.memory}
        
        if self.model_supports_tool_calling():
            # Get function definitions
            function_definitions = get_function_definitions()
            
            logger.info(f"Calling LiteLLM with model: {self.model}")
            logger.info(f"Message count: {len(self.memory)}")
            logger.info(f"Tools available: {[f['name'] for f in function_definitions]}")
            
            # Add function definitions for supported models
            kwargs["functions"] = function_definitions
            kwargs["function_call"] = "auto"
        else:
            logger.info(f"Calling LiteLLM with model: {self.model} (without function calling)")
            logger.info(f"Message count: {len(self.memory)}")
        
        # Log the request
        log_completion_request(self.model, self.memory, kwargs.get("functions"))
        
        # Track request time
        start_time = time.time()
        response = litellm.completion(**kwargs)
        elapsed_time = time.time() - start_time
        
        # Log the response
        log_completion_response(response, elapsed_time)
        
        return response

    def _process_response(self, response, iteration):
        """
        Process the response from the LLM.
        
        Args:
            response: Response from the LLM
            iteration (int): Current iteration number
            
        Returns:
            str or None: Final response if complete, None to continue
        """
        # Check if model doesn't support function calling but tries to use the special syntax
        if not self.model_supports_tool_calling():
            if hasattr(response, 'choices') and len(response.choices) > 0:
                content = response.choices[0].message.content
            elif isinstance(response, dict) and "choices" in response:
                content = response["choices"][0]["message"].get("content", "")
            else:
                content = ""
                
            # Check for our special function call syntax
            if content and "[FUNCTION_CALL]" in content and "[/FUNCTION_CALL]" in content:
                return self._process_text_function_call(content, iteration)
        
        # Process normal responses
        if hasattr(response, 'choices'):
            # It's a ModelResponse object from LiteLLM
            return self._process_model_response(response, iteration)
        else:
            # It's a dictionary (traditional format)
            return self._process_dict_response(response, iteration)

    def _process_text_function_call(self, content, iteration):
        """
        Process a function call embedded in text for models that don't support native function calling.
        
        Args:
            content (str): The response content
            iteration (int): Current iteration number
            
        Returns:
            str or None: Final response if complete, None to continue
        """
        # Extract function call from text
        start_idx = content.find("[FUNCTION_CALL]")
        end_idx = content.find("[/FUNCTION_CALL]")
        
        if start_idx == -1 or end_idx == -1 or start_idx >= end_idx:
            # No valid function call found, treat as regular response
            self.memory.append({"role": "assistant", "content": content})
            return content
            
        func_text = content[start_idx + 15:end_idx].strip()
        
        # Parse function name and arguments
        if "(" not in func_text or ")" not in func_text:
            # Invalid function call format
            self.memory.append({"role": "assistant", "content": content})
            return content
            
        func_name = func_text[:func_text.find("(")].strip()
        args_text = func_text[func_text.find("(")+1:func_text.rfind(")")].strip()
        
        # Parse arguments
        func_args = {}
        if args_text:
            for arg_pair in args_text.split(","):
                if "=" in arg_pair:
                    key, value = arg_pair.split("=", 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Try to convert value to appropriate type
                    try:
                        # Try as number
                        if value.isdigit():
                            value = int(value)
                        elif value.replace(".", "", 1).isdigit():
                            value = float(value)
                        # Try as boolean
                        elif value.lower() in ["true", "false"]:
                            value = value.lower() == "true"
                        # Keep as string if none of the above
                    except:
                        pass
                        
                    func_args[key] = value
        
        # Save the original message but modify it to remove function call syntax
        modified_content = (
            content[:start_idx].strip() + " " + 
            content[end_idx + 16:].strip()
        ).strip()
        
        if modified_content:
            self.memory.append({"role": "assistant", "content": modified_content})
            
        # Handle the extracted function call
        return self._handle_function_call(func_name, func_args, iteration)

    def _process_model_response(self, response, iteration):
        """
        Process a ModelResponse object from LiteLLM.
        
        Args:
            response: ModelResponse object
            iteration (int): Current iteration number
            
        Returns:
            str or None: Final response if complete, None to continue
        """
        if len(response.choices) == 0:
            return "No response generated by the model."
            
        message_obj = response.choices[0].message
        
        # Check for function call
        if hasattr(message_obj, 'function_call') and message_obj.function_call:
            function_call = message_obj.function_call
            function_name = function_call.name
            
            try:
                # Arguments might be a string that needs to be parsed as JSON
                function_args = json.loads(function_call.arguments) if isinstance(function_call.arguments, str) else function_call.arguments
            except json.JSONDecodeError:
                function_args = {}
                
            return self._handle_function_call(function_name, function_args, iteration)
        
        # Handle content response
        content = message_obj.content if hasattr(message_obj, 'content') else ""
        if content:
            content = str(content).strip()
            logger.info(f"Model response: {content}")
            
            if content:
                self.memory.append({"role": "assistant", "content": content})
                return content
                
        return None

    def _process_dict_response(self, response, iteration):
        """
        Process a dictionary response.
        
        Args:
            response (dict): Response dictionary
            iteration (int): Current iteration number
            
        Returns:
            str or None: Final response if complete, None to continue
        """
        logger.debug("Got response in dictionary format")
        
        if "choices" not in response or len(response["choices"]) == 0:
            logger.warning("No valid choices in model response")
            return "No valid response received from the model."
            
        choice = response["choices"][0]
        
        if "message" not in choice:
            return None
            
        message = choice["message"]
        
        # Check for function call
        if "function_call" in message:
            function_call = message["function_call"]
            function_name = function_call["name"]
            
            try:
                function_args = json.loads(function_call["arguments"])
            except json.JSONDecodeError:
                function_args = {}
                
            return self._handle_function_call(function_name, function_args, iteration)
        
        # Handle text content
        content = message.get("content", "").strip()
        logger.info(f"Model response: {content}")
        
        if content:
            self.memory.append({"role": "assistant", "content": content})
            return content
            
        return None

    def _handle_function_call(self, function_name, function_args, iteration):
        """
        Handle a function call from the LLM.
        
        Args:
            function_name (str): Name of the function to call
            function_args (dict): Arguments to pass to the function
            iteration (int): Current iteration number
            
        Returns:
            str or None: Final response if complete, None to continue
        """
        logger.info(f"Function call detected: {function_name} with args: {function_args}")
        
        tools = get_tools()
        if function_name not in tools:
            error_msg = f"Tool {function_name} is not registered."
            logger.warning(error_msg)
            self.memory.append({"role": "assistant", "content": error_msg})
            return error_msg
            
        tool_schema = tools[function_name]["schema"]
        tool_function = tools[function_name]["function"]
        
        # Check for repeated function calls
        current_call = {
            "name": function_name,
            "args": function_args
        }
        
        if self.last_function_call == current_call:
            logger.warning("Detected repeated function call! Breaking loop.")
            # Get the last function result from memory
            last_result = next((m["content"] for m in reversed(self.memory) 
                               if m["role"] == "function" and m["name"] == function_name), 
                              "unknown")
            
            response = f"The result of {function_name}({function_args}) is {last_result}."
            self.memory.append({"role": "assistant", "content": response})
            return response
        
        # Save this call to detect repetition
        self.last_function_call = current_call
        
        try:
            # Validate and execute the function
            validated_args = tool_schema(**function_args)
            function_response = tool_function(**validated_args.dict())
            
            # Add an extra hint to encourage a final response
            self.memory.append({
                "role": "function",
                "name": function_name,
                "content": str(function_response)
            })
            
            # Add a conversational prompt to guide the model to give a more natural final answer
            if iteration > 1:  # Only add this hint after the first iteration
                if function_name == "add_numbers":
                    guidance = f"The sum of {function_args.get('a')} and {function_args.get('b')} is {function_response}. Please respond conversationally to the user with this information."
                elif function_name == "get_weather":
                    guidance = f"The weather in {function_args.get('city')} is {function_response}. Please incorporate this information into a natural, conversational response."
                elif function_name == "search_database":
                    guidance = f"You found some results about '{function_args.get('query')}'. Please summarize these results in a helpful way for the user."
                else:
                    guidance = "Now provide a complete final answer to the user's question using the function result. Make your response natural and conversational."
                
                self.memory.append({
                    "role": "system",
                    "content": guidance
                })
            
            logger.info(f"Function executed: {function_name}, result: {function_response}")
            return None  # Continue the loop
            
        except Exception as e:
            error_msg = f"Error executing {function_name}: {str(e)}"
            logger.error(f"Function error: {error_msg}")
            self.memory.append({
                "role": "function",
                "name": function_name,
                "content": error_msg
            })
            return None