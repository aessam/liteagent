"""
Google Gemini Chat Sessions provider for stateful conversations.

This provider uses Gemini's chat session API to maintain conversation state
without resending full context on every request.
"""

import os
import time
from typing import Any, Dict, List, Optional, Union

try:
    import google.generativeai as genai
    from google.generativeai.types import GenerateContentResponse
    from google.generativeai.types.generation_types import BlockedPromptException
except ImportError:
    raise ImportError("Google Generative AI library not installed. Install with: pip install google-generativeai")

from .base import ProviderInterface, ProviderResponse, ToolCall
from ..utils import logger


class GeminiChatProvider(ProviderInterface):
    """
    Google Gemini provider with chat session management.
    
    Key advantages:
    - Chat sessions maintain conversation state
    - No need to resend full conversation history
    - Automatic context management via SDK
    - Support for both text and multimodal content
    """
    
    def __init__(self, model_name: str, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Gemini Chat provider.
        
        Args:
            model_name: Gemini model name (e.g., 'gemini-1.5-pro', 'gemini-1.5-flash')
            api_key: Google AI API key
            **kwargs: Additional configuration
        """
        self.chat_session = None
        self.model = None
        self.system_instruction = kwargs.get('system_instruction', '')
        
        super().__init__(model_name, api_key, **kwargs)
        
    def _get_provider_name(self) -> str:
        """Return provider name."""
        return 'gemini_chat'
        
    def _setup_client(self) -> None:
        """Setup Gemini client and model."""
        api_key = self.api_key or os.getenv('GOOGLE_AI_API_KEY') or os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("Google AI API key required. Set GOOGLE_AI_API_KEY environment variable.")
            
        genai.configure(api_key=api_key)
        
        # Create model instance
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=self.system_instruction
        )
        
        logger.info(f"[{self.provider_name}] Initialized Gemini model: {self.model_name}")
    
    def start_chat_session(self, history: Optional[List[Dict[str, Any]]] = None) -> str:
        """
        Start a new chat session.
        
        Args:
            history: Optional conversation history to initialize with
            
        Returns:
            str: Session identifier (for tracking purposes)
        """
        if not self.model:
            raise ValueError("Model not initialized")
            
        # Convert history to Gemini format
        gemini_history = []
        if history:
            for msg in history:
                role = msg.get('role')
                content = msg.get('content', '')
                
                # Skip system messages (they go in system_instruction)
                if role == 'system':
                    continue
                    
                # Convert role names
                if role == 'assistant':
                    role = 'model'
                elif role != 'user':
                    continue  # Skip unsupported roles
                    
                gemini_history.append({
                    'role': role,
                    'parts': [content]
                })
        
        try:
            self.chat_session = self.model.start_chat(history=gemini_history)
            session_id = f"chat_{int(time.time())}_{id(self.chat_session)}"
            
            logger.info(f"[{self.provider_name}] Started chat session: {session_id}")
            return session_id
            
        except Exception as e:
            logger.error(f"[{self.provider_name}] Failed to start chat session: {e}")
            raise
    
    def fork_chat_session(self, base_history: List[Dict[str, Any]], role_message: str) -> str:
        """
        Create a forked chat session with shared history plus role message.
        
        Args:
            base_history: Base conversation history to fork from
            role_message: Role-specific message for the fork
            
        Returns:
            str: New session identifier
        """
        # Add role message to history
        fork_history = base_history + [{'role': 'user', 'content': role_message}]
        return self.start_chat_session(fork_history)
    
    def send_message(self, message: str) -> ProviderResponse:
        """
        Send a message in the current chat session.
        
        Args:
            message: Message to send
            
        Returns:
            ProviderResponse: Response from model
        """
        if not self.chat_session:
            raise ValueError("No active chat session. Start a chat session first.")
            
        start_time = time.time()
        
        try:
            response = self.chat_session.send_message(message)
            
            elapsed_time = time.time() - start_time
            logger.info(f"[{self.provider_name}] Message sent in {elapsed_time:.2f}s")
            
            return self._convert_response(response, elapsed_time)
            
        except BlockedPromptException as e:
            logger.error(f"[{self.provider_name}] Content blocked: {e}")
            raise
        except Exception as e:
            logger.error(f"[{self.provider_name}] Error sending message: {e}")
            raise
    
    def generate_response(
        self, 
        messages: List[Dict[str, Any]], 
        tools: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> ProviderResponse:
        """
        Generate response using chat session or direct generation.
        
        Args:
            messages: List of messages
            tools: Optional tools (not implemented yet)
            **kwargs: Additional parameters
            
        Returns:
            ProviderResponse: Standardized response
        """
        start_time = time.time()
        
        # If we have an active chat session and only one new message, use it
        if (self.chat_session and 
            len(messages) == 1 and 
            messages[0].get('role') == 'user'):
            return self.send_message(messages[0]['content'])
        
        # Otherwise, create a new session with full history
        # Extract system instruction
        system_instruction = ""
        conversation_history = []
        
        for msg in messages[:-1]:  # All but last message
            role = msg.get('role')
            content = msg.get('content', '')
            
            if role == 'system':
                system_instruction = content
            else:
                conversation_history.append(msg)
        
        # Update system instruction if provided
        if system_instruction and system_instruction != self.system_instruction:
            self.system_instruction = system_instruction
            self.model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=system_instruction
            )
        
        # Start new session with history
        self.start_chat_session(conversation_history)
        
        # Send the latest message
        latest_message = messages[-1]
        if latest_message.get('role') == 'user':
            return self.send_message(latest_message['content'])
        else:
            # For non-user messages, use direct generation
            return self._generate_direct(messages, **kwargs)
    
    def _generate_direct(self, messages: List[Dict[str, Any]], **kwargs) -> ProviderResponse:
        """Generate response using direct model.generate_content."""
        start_time = time.time()
        
        # Convert messages to Gemini format
        content_parts = []
        for msg in messages:
            role = msg.get('role')
            content = msg.get('content', '')
            
            if role == 'system':
                continue  # System handled in system_instruction
            elif role in ['user', 'assistant']:
                content_parts.append(f"{role}: {content}")
        
        prompt = "\n".join(content_parts)
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=kwargs.get('temperature'),
                    max_output_tokens=kwargs.get('max_tokens'),
                    top_p=kwargs.get('top_p'),
                    top_k=kwargs.get('top_k')
                )
            )
            
            elapsed_time = time.time() - start_time
            logger.info(f"[{self.provider_name}] Direct generation in {elapsed_time:.2f}s")
            
            return self._convert_response(response, elapsed_time)
            
        except Exception as e:
            logger.error(f"[{self.provider_name}] Error in direct generation: {e}")
            raise
    
    def _convert_response(self, response: GenerateContentResponse, elapsed_time: float) -> ProviderResponse:
        """Convert Gemini response to standardized format."""
        # Extract text content
        content = ""
        if response.text:
            content = response.text
        
        # Extract usage information
        usage = {}
        if hasattr(response, 'usage_metadata') and response.usage_metadata:
            usage = {
                'prompt_tokens': getattr(response.usage_metadata, 'prompt_token_count', 0),
                'completion_tokens': getattr(response.usage_metadata, 'candidates_token_count', 0),
                'total_tokens': getattr(response.usage_metadata, 'total_token_count', 0),
                'cached_content_token_count': getattr(response.usage_metadata, 'cached_content_token_count', 0)
            }
        
        # Extract finish reason
        finish_reason = 'stop'
        if response.candidates and len(response.candidates) > 0:
            candidate = response.candidates[0]
            if hasattr(candidate, 'finish_reason'):
                finish_reason = str(candidate.finish_reason).lower()
        
        return ProviderResponse(
            content=content,
            tool_calls=[],  # Tool calls not implemented yet
            usage=usage,
            model=self.model_name,
            provider=self.provider_name,
            raw_response=response,
            finish_reason=finish_reason
        )
    
    def get_chat_history(self) -> List[Dict[str, Any]]:
        """Get current chat session history."""
        if not self.chat_session:
            return []
            
        history = []
        for message in self.chat_session.history:
            role = message.role
            if role == 'model':
                role = 'assistant'
                
            content = ""
            for part in message.parts:
                content += part.text
                
            history.append({
                'role': role,
                'content': content
            })
            
        return history
    
    def supports_stateful_sessions(self) -> bool:
        """Return True as this provider supports stateful sessions."""
        return True
    
    def supports_caching(self) -> bool:
        """Return True as Gemini supports context caching."""
        return True
    
    def supports_tool_calling(self) -> bool:
        """Return False for now (could be implemented)."""
        return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model."""
        try:
            model_info = genai.get_model(f"models/{self.model_name}")
            return {
                'name': model_info.name,
                'display_name': model_info.display_name,
                'description': model_info.description,
                'input_token_limit': model_info.input_token_limit,
                'output_token_limit': model_info.output_token_limit,
                'supported_generation_methods': model_info.supported_generation_methods
            }
        except Exception as e:
            logger.warning(f"[{self.provider_name}] Could not get model info: {e}")
            return {}
    
    def cleanup(self) -> None:
        """Clean up chat session."""
        if self.chat_session:
            self.chat_session = None
            logger.info(f"[{self.provider_name}] Chat session cleaned up")