"""
Memory management for LiteAgent.

This module provides classes for managing conversation history and memory
for the agent.
"""

import json
from typing import Dict, List, Optional, Any, Union
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result

class ConversationMemory:
    """Class to manage conversation history."""
    
    def xǁConversationMemoryǁ__init____mutmut_orig(self, system_prompt: str):
        """
        Initialize conversation memory.
        
        Args:
            system_prompt: The system prompt to use
        """
        self.system_prompt = system_prompt
        self.messages = [{"role": "system", "content": system_prompt}]
        self.function_calls = {}  # Track function calls to detect loops
        self.last_function_call = None
    
    def xǁConversationMemoryǁ__init____mutmut_1(self, system_prompt: str):
        """
        Initialize conversation memory.
        
        Args:
            system_prompt: The system prompt to use
        """
        self.system_prompt = None
        self.messages = [{"role": "system", "content": system_prompt}]
        self.function_calls = {}  # Track function calls to detect loops
        self.last_function_call = None
    
    def xǁConversationMemoryǁ__init____mutmut_2(self, system_prompt: str):
        """
        Initialize conversation memory.
        
        Args:
            system_prompt: The system prompt to use
        """
        self.system_prompt = system_prompt
        self.messages = None
        self.function_calls = {}  # Track function calls to detect loops
        self.last_function_call = None
    
    def xǁConversationMemoryǁ__init____mutmut_3(self, system_prompt: str):
        """
        Initialize conversation memory.
        
        Args:
            system_prompt: The system prompt to use
        """
        self.system_prompt = system_prompt
        self.messages = [{"XXroleXX": "system", "content": system_prompt}]
        self.function_calls = {}  # Track function calls to detect loops
        self.last_function_call = None
    
    def xǁConversationMemoryǁ__init____mutmut_4(self, system_prompt: str):
        """
        Initialize conversation memory.
        
        Args:
            system_prompt: The system prompt to use
        """
        self.system_prompt = system_prompt
        self.messages = [{"ROLE": "system", "content": system_prompt}]
        self.function_calls = {}  # Track function calls to detect loops
        self.last_function_call = None
    
    def xǁConversationMemoryǁ__init____mutmut_5(self, system_prompt: str):
        """
        Initialize conversation memory.
        
        Args:
            system_prompt: The system prompt to use
        """
        self.system_prompt = system_prompt
        self.messages = [{"role": "XXsystemXX", "content": system_prompt}]
        self.function_calls = {}  # Track function calls to detect loops
        self.last_function_call = None
    
    def xǁConversationMemoryǁ__init____mutmut_6(self, system_prompt: str):
        """
        Initialize conversation memory.
        
        Args:
            system_prompt: The system prompt to use
        """
        self.system_prompt = system_prompt
        self.messages = [{"role": "SYSTEM", "content": system_prompt}]
        self.function_calls = {}  # Track function calls to detect loops
        self.last_function_call = None
    
    def xǁConversationMemoryǁ__init____mutmut_7(self, system_prompt: str):
        """
        Initialize conversation memory.
        
        Args:
            system_prompt: The system prompt to use
        """
        self.system_prompt = system_prompt
        self.messages = [{"role": "system", "XXcontentXX": system_prompt}]
        self.function_calls = {}  # Track function calls to detect loops
        self.last_function_call = None
    
    def xǁConversationMemoryǁ__init____mutmut_8(self, system_prompt: str):
        """
        Initialize conversation memory.
        
        Args:
            system_prompt: The system prompt to use
        """
        self.system_prompt = system_prompt
        self.messages = [{"role": "system", "CONTENT": system_prompt}]
        self.function_calls = {}  # Track function calls to detect loops
        self.last_function_call = None
    
    def xǁConversationMemoryǁ__init____mutmut_9(self, system_prompt: str):
        """
        Initialize conversation memory.
        
        Args:
            system_prompt: The system prompt to use
        """
        self.system_prompt = system_prompt
        self.messages = [{"role": "system", "content": system_prompt}]
        self.function_calls = None  # Track function calls to detect loops
        self.last_function_call = None
    
    def xǁConversationMemoryǁ__init____mutmut_10(self, system_prompt: str):
        """
        Initialize conversation memory.
        
        Args:
            system_prompt: The system prompt to use
        """
        self.system_prompt = system_prompt
        self.messages = [{"role": "system", "content": system_prompt}]
        self.function_calls = {}  # Track function calls to detect loops
        self.last_function_call = ""
    
    xǁConversationMemoryǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁConversationMemoryǁ__init____mutmut_1': xǁConversationMemoryǁ__init____mutmut_1, 
        'xǁConversationMemoryǁ__init____mutmut_2': xǁConversationMemoryǁ__init____mutmut_2, 
        'xǁConversationMemoryǁ__init____mutmut_3': xǁConversationMemoryǁ__init____mutmut_3, 
        'xǁConversationMemoryǁ__init____mutmut_4': xǁConversationMemoryǁ__init____mutmut_4, 
        'xǁConversationMemoryǁ__init____mutmut_5': xǁConversationMemoryǁ__init____mutmut_5, 
        'xǁConversationMemoryǁ__init____mutmut_6': xǁConversationMemoryǁ__init____mutmut_6, 
        'xǁConversationMemoryǁ__init____mutmut_7': xǁConversationMemoryǁ__init____mutmut_7, 
        'xǁConversationMemoryǁ__init____mutmut_8': xǁConversationMemoryǁ__init____mutmut_8, 
        'xǁConversationMemoryǁ__init____mutmut_9': xǁConversationMemoryǁ__init____mutmut_9, 
        'xǁConversationMemoryǁ__init____mutmut_10': xǁConversationMemoryǁ__init____mutmut_10
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁConversationMemoryǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁConversationMemoryǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁConversationMemoryǁ__init____mutmut_orig)
    xǁConversationMemoryǁ__init____mutmut_orig.__name__ = 'xǁConversationMemoryǁ__init__'
    
    def xǁConversationMemoryǁadd_user_message__mutmut_orig(self, content: str) -> None:
        """
        Add a user message to the conversation.
        
        Args:
            content: The message content
        """
        self.messages.append({"role": "user", "content": content})
    
    def xǁConversationMemoryǁadd_user_message__mutmut_1(self, content: str) -> None:
        """
        Add a user message to the conversation.
        
        Args:
            content: The message content
        """
        self.messages.append(None)
    
    def xǁConversationMemoryǁadd_user_message__mutmut_2(self, content: str) -> None:
        """
        Add a user message to the conversation.
        
        Args:
            content: The message content
        """
        self.messages.append({"XXroleXX": "user", "content": content})
    
    def xǁConversationMemoryǁadd_user_message__mutmut_3(self, content: str) -> None:
        """
        Add a user message to the conversation.
        
        Args:
            content: The message content
        """
        self.messages.append({"ROLE": "user", "content": content})
    
    def xǁConversationMemoryǁadd_user_message__mutmut_4(self, content: str) -> None:
        """
        Add a user message to the conversation.
        
        Args:
            content: The message content
        """
        self.messages.append({"role": "XXuserXX", "content": content})
    
    def xǁConversationMemoryǁadd_user_message__mutmut_5(self, content: str) -> None:
        """
        Add a user message to the conversation.
        
        Args:
            content: The message content
        """
        self.messages.append({"role": "USER", "content": content})
    
    def xǁConversationMemoryǁadd_user_message__mutmut_6(self, content: str) -> None:
        """
        Add a user message to the conversation.
        
        Args:
            content: The message content
        """
        self.messages.append({"role": "user", "XXcontentXX": content})
    
    def xǁConversationMemoryǁadd_user_message__mutmut_7(self, content: str) -> None:
        """
        Add a user message to the conversation.
        
        Args:
            content: The message content
        """
        self.messages.append({"role": "user", "CONTENT": content})
    
    xǁConversationMemoryǁadd_user_message__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁConversationMemoryǁadd_user_message__mutmut_1': xǁConversationMemoryǁadd_user_message__mutmut_1, 
        'xǁConversationMemoryǁadd_user_message__mutmut_2': xǁConversationMemoryǁadd_user_message__mutmut_2, 
        'xǁConversationMemoryǁadd_user_message__mutmut_3': xǁConversationMemoryǁadd_user_message__mutmut_3, 
        'xǁConversationMemoryǁadd_user_message__mutmut_4': xǁConversationMemoryǁadd_user_message__mutmut_4, 
        'xǁConversationMemoryǁadd_user_message__mutmut_5': xǁConversationMemoryǁadd_user_message__mutmut_5, 
        'xǁConversationMemoryǁadd_user_message__mutmut_6': xǁConversationMemoryǁadd_user_message__mutmut_6, 
        'xǁConversationMemoryǁadd_user_message__mutmut_7': xǁConversationMemoryǁadd_user_message__mutmut_7
    }
    
    def add_user_message(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁConversationMemoryǁadd_user_message__mutmut_orig"), object.__getattribute__(self, "xǁConversationMemoryǁadd_user_message__mutmut_mutants"), args, kwargs, self)
        return result 
    
    add_user_message.__signature__ = _mutmut_signature(xǁConversationMemoryǁadd_user_message__mutmut_orig)
    xǁConversationMemoryǁadd_user_message__mutmut_orig.__name__ = 'xǁConversationMemoryǁadd_user_message'
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_orig(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_1(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = None
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_2(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append(None)
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_3(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "XXtypeXX": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_4(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "TYPE": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_5(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "XXtextXX",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_6(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "TEXT",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_7(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "XXtextXX": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_8(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "TEXT": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_9(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(None):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_10(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append(None)
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_11(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "XXtypeXX": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_12(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "TYPE": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_13(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "XXimage_urlXX",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_14(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "IMAGE_URL",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_15(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "XXimage_urlXX": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_16(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "IMAGE_URL": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_17(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"XXurlXX": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_18(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"URL": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_19(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(None):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_20(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(None, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_21(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, None) as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_22(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open("rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_23(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, ) as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_24(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "XXrbXX") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_25(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "RB") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_26(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = None
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_27(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(None).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_28(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = None
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_29(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].upper()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_30(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(None)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_31(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[2].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_32(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension not in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_33(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['XX.jpgXX', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_34(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.JPG', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_35(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', 'XX.jpegXX']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_36(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.JPEG']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_37(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = None
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_38(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'XXjpegXX'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_39(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'JPEG'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_40(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension != '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_41(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == 'XX.pngXX':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_42(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.PNG':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_43(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = None
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_44(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'XXpngXX'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_45(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'PNG'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_46(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension != '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_47(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == 'XX.gifXX':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_48(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.GIF':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_49(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = None
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_50(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'XXgifXX'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_51(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'GIF'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_52(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension != '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_53(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == 'XX.webpXX':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_54(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.WEBP':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_55(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = None
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_56(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'XXwebpXX'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_57(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'WEBP'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_58(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = None  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_59(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'XXjpegXX'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_60(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'JPEG'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_61(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append(None)
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_62(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "XXtypeXX": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_63(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "TYPE": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_64(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "XXimage_urlXX",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_65(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "IMAGE_URL",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_66(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "XXimage_urlXX": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_67(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "IMAGE_URL": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_68(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "XXurlXX": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_69(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "URL": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_70(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append(None)
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_71(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "XXroleXX": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_72(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "ROLE": "user", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_73(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "XXuserXX", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_74(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "USER", 
            "content": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_75(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "XXcontentXX": message_content
        })
    
    def xǁConversationMemoryǁadd_user_message_with_images__mutmut_76(self, content: str, images: List[str]) -> None:
        """
        Add a user message with images to the conversation.
        
        Args:
            content: The message content
            images: List of image paths or URLs
        """
        import base64
        import os
        from typing import Union
        
        # Prepare message content for multimodal format
        message_content = []
        
        # Add text content
        if content:
            message_content.append({
                "type": "text",
                "text": content
            })
        
        # Add images
        for image in images:
            if self._is_url(image):
                # Remote image URL
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": image}
                })
            else:
                # Local image file - convert to base64
                if os.path.exists(image):
                    with open(image, "rb") as image_file:
                        image_data = base64.b64encode(image_file.read()).decode()
                        # Determine image format
                        extension = os.path.splitext(image)[1].lower()
                        if extension in ['.jpg', '.jpeg']:
                            format_type = 'jpeg'
                        elif extension == '.png':
                            format_type = 'png'
                        elif extension == '.gif':
                            format_type = 'gif'
                        elif extension == '.webp':
                            format_type = 'webp'
                        else:
                            format_type = 'jpeg'  # Default
                        
                        message_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{format_type};base64,{image_data}"
                            }
                        })
        
        self.messages.append({
            "role": "user", 
            "CONTENT": message_content
        })
    
    xǁConversationMemoryǁadd_user_message_with_images__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁConversationMemoryǁadd_user_message_with_images__mutmut_1': xǁConversationMemoryǁadd_user_message_with_images__mutmut_1, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_2': xǁConversationMemoryǁadd_user_message_with_images__mutmut_2, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_3': xǁConversationMemoryǁadd_user_message_with_images__mutmut_3, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_4': xǁConversationMemoryǁadd_user_message_with_images__mutmut_4, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_5': xǁConversationMemoryǁadd_user_message_with_images__mutmut_5, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_6': xǁConversationMemoryǁadd_user_message_with_images__mutmut_6, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_7': xǁConversationMemoryǁadd_user_message_with_images__mutmut_7, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_8': xǁConversationMemoryǁadd_user_message_with_images__mutmut_8, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_9': xǁConversationMemoryǁadd_user_message_with_images__mutmut_9, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_10': xǁConversationMemoryǁadd_user_message_with_images__mutmut_10, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_11': xǁConversationMemoryǁadd_user_message_with_images__mutmut_11, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_12': xǁConversationMemoryǁadd_user_message_with_images__mutmut_12, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_13': xǁConversationMemoryǁadd_user_message_with_images__mutmut_13, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_14': xǁConversationMemoryǁadd_user_message_with_images__mutmut_14, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_15': xǁConversationMemoryǁadd_user_message_with_images__mutmut_15, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_16': xǁConversationMemoryǁadd_user_message_with_images__mutmut_16, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_17': xǁConversationMemoryǁadd_user_message_with_images__mutmut_17, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_18': xǁConversationMemoryǁadd_user_message_with_images__mutmut_18, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_19': xǁConversationMemoryǁadd_user_message_with_images__mutmut_19, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_20': xǁConversationMemoryǁadd_user_message_with_images__mutmut_20, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_21': xǁConversationMemoryǁadd_user_message_with_images__mutmut_21, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_22': xǁConversationMemoryǁadd_user_message_with_images__mutmut_22, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_23': xǁConversationMemoryǁadd_user_message_with_images__mutmut_23, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_24': xǁConversationMemoryǁadd_user_message_with_images__mutmut_24, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_25': xǁConversationMemoryǁadd_user_message_with_images__mutmut_25, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_26': xǁConversationMemoryǁadd_user_message_with_images__mutmut_26, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_27': xǁConversationMemoryǁadd_user_message_with_images__mutmut_27, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_28': xǁConversationMemoryǁadd_user_message_with_images__mutmut_28, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_29': xǁConversationMemoryǁadd_user_message_with_images__mutmut_29, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_30': xǁConversationMemoryǁadd_user_message_with_images__mutmut_30, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_31': xǁConversationMemoryǁadd_user_message_with_images__mutmut_31, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_32': xǁConversationMemoryǁadd_user_message_with_images__mutmut_32, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_33': xǁConversationMemoryǁadd_user_message_with_images__mutmut_33, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_34': xǁConversationMemoryǁadd_user_message_with_images__mutmut_34, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_35': xǁConversationMemoryǁadd_user_message_with_images__mutmut_35, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_36': xǁConversationMemoryǁadd_user_message_with_images__mutmut_36, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_37': xǁConversationMemoryǁadd_user_message_with_images__mutmut_37, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_38': xǁConversationMemoryǁadd_user_message_with_images__mutmut_38, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_39': xǁConversationMemoryǁadd_user_message_with_images__mutmut_39, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_40': xǁConversationMemoryǁadd_user_message_with_images__mutmut_40, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_41': xǁConversationMemoryǁadd_user_message_with_images__mutmut_41, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_42': xǁConversationMemoryǁadd_user_message_with_images__mutmut_42, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_43': xǁConversationMemoryǁadd_user_message_with_images__mutmut_43, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_44': xǁConversationMemoryǁadd_user_message_with_images__mutmut_44, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_45': xǁConversationMemoryǁadd_user_message_with_images__mutmut_45, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_46': xǁConversationMemoryǁadd_user_message_with_images__mutmut_46, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_47': xǁConversationMemoryǁadd_user_message_with_images__mutmut_47, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_48': xǁConversationMemoryǁadd_user_message_with_images__mutmut_48, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_49': xǁConversationMemoryǁadd_user_message_with_images__mutmut_49, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_50': xǁConversationMemoryǁadd_user_message_with_images__mutmut_50, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_51': xǁConversationMemoryǁadd_user_message_with_images__mutmut_51, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_52': xǁConversationMemoryǁadd_user_message_with_images__mutmut_52, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_53': xǁConversationMemoryǁadd_user_message_with_images__mutmut_53, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_54': xǁConversationMemoryǁadd_user_message_with_images__mutmut_54, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_55': xǁConversationMemoryǁadd_user_message_with_images__mutmut_55, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_56': xǁConversationMemoryǁadd_user_message_with_images__mutmut_56, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_57': xǁConversationMemoryǁadd_user_message_with_images__mutmut_57, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_58': xǁConversationMemoryǁadd_user_message_with_images__mutmut_58, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_59': xǁConversationMemoryǁadd_user_message_with_images__mutmut_59, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_60': xǁConversationMemoryǁadd_user_message_with_images__mutmut_60, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_61': xǁConversationMemoryǁadd_user_message_with_images__mutmut_61, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_62': xǁConversationMemoryǁadd_user_message_with_images__mutmut_62, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_63': xǁConversationMemoryǁadd_user_message_with_images__mutmut_63, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_64': xǁConversationMemoryǁadd_user_message_with_images__mutmut_64, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_65': xǁConversationMemoryǁadd_user_message_with_images__mutmut_65, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_66': xǁConversationMemoryǁadd_user_message_with_images__mutmut_66, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_67': xǁConversationMemoryǁadd_user_message_with_images__mutmut_67, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_68': xǁConversationMemoryǁadd_user_message_with_images__mutmut_68, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_69': xǁConversationMemoryǁadd_user_message_with_images__mutmut_69, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_70': xǁConversationMemoryǁadd_user_message_with_images__mutmut_70, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_71': xǁConversationMemoryǁadd_user_message_with_images__mutmut_71, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_72': xǁConversationMemoryǁadd_user_message_with_images__mutmut_72, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_73': xǁConversationMemoryǁadd_user_message_with_images__mutmut_73, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_74': xǁConversationMemoryǁadd_user_message_with_images__mutmut_74, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_75': xǁConversationMemoryǁadd_user_message_with_images__mutmut_75, 
        'xǁConversationMemoryǁadd_user_message_with_images__mutmut_76': xǁConversationMemoryǁadd_user_message_with_images__mutmut_76
    }
    
    def add_user_message_with_images(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁConversationMemoryǁadd_user_message_with_images__mutmut_orig"), object.__getattribute__(self, "xǁConversationMemoryǁadd_user_message_with_images__mutmut_mutants"), args, kwargs, self)
        return result 
    
    add_user_message_with_images.__signature__ = _mutmut_signature(xǁConversationMemoryǁadd_user_message_with_images__mutmut_orig)
    xǁConversationMemoryǁadd_user_message_with_images__mutmut_orig.__name__ = 'xǁConversationMemoryǁadd_user_message_with_images'
    
    def xǁConversationMemoryǁ_is_url__mutmut_orig(self, string: str) -> bool:
        """Check if a string is a URL."""
        return string.startswith(('http://', 'https://'))
    
    def xǁConversationMemoryǁ_is_url__mutmut_1(self, string: str) -> bool:
        """Check if a string is a URL."""
        return string.startswith(None)
    
    def xǁConversationMemoryǁ_is_url__mutmut_2(self, string: str) -> bool:
        """Check if a string is a URL."""
        return string.startswith(('XXhttp://XX', 'https://'))
    
    def xǁConversationMemoryǁ_is_url__mutmut_3(self, string: str) -> bool:
        """Check if a string is a URL."""
        return string.startswith(('HTTP://', 'https://'))
    
    def xǁConversationMemoryǁ_is_url__mutmut_4(self, string: str) -> bool:
        """Check if a string is a URL."""
        return string.startswith(('http://', 'XXhttps://XX'))
    
    def xǁConversationMemoryǁ_is_url__mutmut_5(self, string: str) -> bool:
        """Check if a string is a URL."""
        return string.startswith(('http://', 'HTTPS://'))
    
    xǁConversationMemoryǁ_is_url__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁConversationMemoryǁ_is_url__mutmut_1': xǁConversationMemoryǁ_is_url__mutmut_1, 
        'xǁConversationMemoryǁ_is_url__mutmut_2': xǁConversationMemoryǁ_is_url__mutmut_2, 
        'xǁConversationMemoryǁ_is_url__mutmut_3': xǁConversationMemoryǁ_is_url__mutmut_3, 
        'xǁConversationMemoryǁ_is_url__mutmut_4': xǁConversationMemoryǁ_is_url__mutmut_4, 
        'xǁConversationMemoryǁ_is_url__mutmut_5': xǁConversationMemoryǁ_is_url__mutmut_5
    }
    
    def _is_url(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁConversationMemoryǁ_is_url__mutmut_orig"), object.__getattribute__(self, "xǁConversationMemoryǁ_is_url__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _is_url.__signature__ = _mutmut_signature(xǁConversationMemoryǁ_is_url__mutmut_orig)
    xǁConversationMemoryǁ_is_url__mutmut_orig.__name__ = 'xǁConversationMemoryǁ_is_url'
    
    def xǁConversationMemoryǁadd_assistant_message__mutmut_orig(self, content: str) -> None:
        """
        Add an assistant message to the conversation.
        
        Args:
            content: The message content
        """
        self.messages.append({"role": "assistant", "content": content})
    
    def xǁConversationMemoryǁadd_assistant_message__mutmut_1(self, content: str) -> None:
        """
        Add an assistant message to the conversation.
        
        Args:
            content: The message content
        """
        self.messages.append(None)
    
    def xǁConversationMemoryǁadd_assistant_message__mutmut_2(self, content: str) -> None:
        """
        Add an assistant message to the conversation.
        
        Args:
            content: The message content
        """
        self.messages.append({"XXroleXX": "assistant", "content": content})
    
    def xǁConversationMemoryǁadd_assistant_message__mutmut_3(self, content: str) -> None:
        """
        Add an assistant message to the conversation.
        
        Args:
            content: The message content
        """
        self.messages.append({"ROLE": "assistant", "content": content})
    
    def xǁConversationMemoryǁadd_assistant_message__mutmut_4(self, content: str) -> None:
        """
        Add an assistant message to the conversation.
        
        Args:
            content: The message content
        """
        self.messages.append({"role": "XXassistantXX", "content": content})
    
    def xǁConversationMemoryǁadd_assistant_message__mutmut_5(self, content: str) -> None:
        """
        Add an assistant message to the conversation.
        
        Args:
            content: The message content
        """
        self.messages.append({"role": "ASSISTANT", "content": content})
    
    def xǁConversationMemoryǁadd_assistant_message__mutmut_6(self, content: str) -> None:
        """
        Add an assistant message to the conversation.
        
        Args:
            content: The message content
        """
        self.messages.append({"role": "assistant", "XXcontentXX": content})
    
    def xǁConversationMemoryǁadd_assistant_message__mutmut_7(self, content: str) -> None:
        """
        Add an assistant message to the conversation.
        
        Args:
            content: The message content
        """
        self.messages.append({"role": "assistant", "CONTENT": content})
    
    xǁConversationMemoryǁadd_assistant_message__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁConversationMemoryǁadd_assistant_message__mutmut_1': xǁConversationMemoryǁadd_assistant_message__mutmut_1, 
        'xǁConversationMemoryǁadd_assistant_message__mutmut_2': xǁConversationMemoryǁadd_assistant_message__mutmut_2, 
        'xǁConversationMemoryǁadd_assistant_message__mutmut_3': xǁConversationMemoryǁadd_assistant_message__mutmut_3, 
        'xǁConversationMemoryǁadd_assistant_message__mutmut_4': xǁConversationMemoryǁadd_assistant_message__mutmut_4, 
        'xǁConversationMemoryǁadd_assistant_message__mutmut_5': xǁConversationMemoryǁadd_assistant_message__mutmut_5, 
        'xǁConversationMemoryǁadd_assistant_message__mutmut_6': xǁConversationMemoryǁadd_assistant_message__mutmut_6, 
        'xǁConversationMemoryǁadd_assistant_message__mutmut_7': xǁConversationMemoryǁadd_assistant_message__mutmut_7
    }
    
    def add_assistant_message(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁConversationMemoryǁadd_assistant_message__mutmut_orig"), object.__getattribute__(self, "xǁConversationMemoryǁadd_assistant_message__mutmut_mutants"), args, kwargs, self)
        return result 
    
    add_assistant_message.__signature__ = _mutmut_signature(xǁConversationMemoryǁadd_assistant_message__mutmut_orig)
    xǁConversationMemoryǁadd_assistant_message__mutmut_orig.__name__ = 'xǁConversationMemoryǁadd_assistant_message'
    
    def xǁConversationMemoryǁadd_function_call__mutmut_orig(self, name: str, args: Dict[str, Any], call_id: Optional[str] = None) -> None:
        """
        Add a function call to the conversation (OpenAI format).
        
        Args:
            name: Function name
            args: Function arguments
            call_id: Unique ID for this function call
        """
        # Convert args to string if needed for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "function_call": {
                "name": name,
                "arguments": args_str
            }
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        call_info = {"args": args}
        if call_id:
            call_info["call_id"] = call_id
            
        self.function_calls[name].append(call_info)
    
    def xǁConversationMemoryǁadd_function_call__mutmut_1(self, name: str, args: Dict[str, Any], call_id: Optional[str] = None) -> None:
        """
        Add a function call to the conversation (OpenAI format).
        
        Args:
            name: Function name
            args: Function arguments
            call_id: Unique ID for this function call
        """
        # Convert args to string if needed for OpenAI format
        args_str = None
        
        message = {
            "role": "assistant",
            "content": None,
            "function_call": {
                "name": name,
                "arguments": args_str
            }
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        call_info = {"args": args}
        if call_id:
            call_info["call_id"] = call_id
            
        self.function_calls[name].append(call_info)
    
    def xǁConversationMemoryǁadd_function_call__mutmut_2(self, name: str, args: Dict[str, Any], call_id: Optional[str] = None) -> None:
        """
        Add a function call to the conversation (OpenAI format).
        
        Args:
            name: Function name
            args: Function arguments
            call_id: Unique ID for this function call
        """
        # Convert args to string if needed for OpenAI format
        args_str = json.dumps(None) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "function_call": {
                "name": name,
                "arguments": args_str
            }
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        call_info = {"args": args}
        if call_id:
            call_info["call_id"] = call_id
            
        self.function_calls[name].append(call_info)
    
    def xǁConversationMemoryǁadd_function_call__mutmut_3(self, name: str, args: Dict[str, Any], call_id: Optional[str] = None) -> None:
        """
        Add a function call to the conversation (OpenAI format).
        
        Args:
            name: Function name
            args: Function arguments
            call_id: Unique ID for this function call
        """
        # Convert args to string if needed for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(None)
        
        message = {
            "role": "assistant",
            "content": None,
            "function_call": {
                "name": name,
                "arguments": args_str
            }
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        call_info = {"args": args}
        if call_id:
            call_info["call_id"] = call_id
            
        self.function_calls[name].append(call_info)
    
    def xǁConversationMemoryǁadd_function_call__mutmut_4(self, name: str, args: Dict[str, Any], call_id: Optional[str] = None) -> None:
        """
        Add a function call to the conversation (OpenAI format).
        
        Args:
            name: Function name
            args: Function arguments
            call_id: Unique ID for this function call
        """
        # Convert args to string if needed for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = None
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        call_info = {"args": args}
        if call_id:
            call_info["call_id"] = call_id
            
        self.function_calls[name].append(call_info)
    
    def xǁConversationMemoryǁadd_function_call__mutmut_5(self, name: str, args: Dict[str, Any], call_id: Optional[str] = None) -> None:
        """
        Add a function call to the conversation (OpenAI format).
        
        Args:
            name: Function name
            args: Function arguments
            call_id: Unique ID for this function call
        """
        # Convert args to string if needed for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "XXroleXX": "assistant",
            "content": None,
            "function_call": {
                "name": name,
                "arguments": args_str
            }
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        call_info = {"args": args}
        if call_id:
            call_info["call_id"] = call_id
            
        self.function_calls[name].append(call_info)
    
    def xǁConversationMemoryǁadd_function_call__mutmut_6(self, name: str, args: Dict[str, Any], call_id: Optional[str] = None) -> None:
        """
        Add a function call to the conversation (OpenAI format).
        
        Args:
            name: Function name
            args: Function arguments
            call_id: Unique ID for this function call
        """
        # Convert args to string if needed for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "ROLE": "assistant",
            "content": None,
            "function_call": {
                "name": name,
                "arguments": args_str
            }
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        call_info = {"args": args}
        if call_id:
            call_info["call_id"] = call_id
            
        self.function_calls[name].append(call_info)
    
    def xǁConversationMemoryǁadd_function_call__mutmut_7(self, name: str, args: Dict[str, Any], call_id: Optional[str] = None) -> None:
        """
        Add a function call to the conversation (OpenAI format).
        
        Args:
            name: Function name
            args: Function arguments
            call_id: Unique ID for this function call
        """
        # Convert args to string if needed for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "XXassistantXX",
            "content": None,
            "function_call": {
                "name": name,
                "arguments": args_str
            }
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        call_info = {"args": args}
        if call_id:
            call_info["call_id"] = call_id
            
        self.function_calls[name].append(call_info)
    
    def xǁConversationMemoryǁadd_function_call__mutmut_8(self, name: str, args: Dict[str, Any], call_id: Optional[str] = None) -> None:
        """
        Add a function call to the conversation (OpenAI format).
        
        Args:
            name: Function name
            args: Function arguments
            call_id: Unique ID for this function call
        """
        # Convert args to string if needed for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "ASSISTANT",
            "content": None,
            "function_call": {
                "name": name,
                "arguments": args_str
            }
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        call_info = {"args": args}
        if call_id:
            call_info["call_id"] = call_id
            
        self.function_calls[name].append(call_info)
    
    def xǁConversationMemoryǁadd_function_call__mutmut_9(self, name: str, args: Dict[str, Any], call_id: Optional[str] = None) -> None:
        """
        Add a function call to the conversation (OpenAI format).
        
        Args:
            name: Function name
            args: Function arguments
            call_id: Unique ID for this function call
        """
        # Convert args to string if needed for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "XXcontentXX": None,
            "function_call": {
                "name": name,
                "arguments": args_str
            }
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        call_info = {"args": args}
        if call_id:
            call_info["call_id"] = call_id
            
        self.function_calls[name].append(call_info)
    
    def xǁConversationMemoryǁadd_function_call__mutmut_10(self, name: str, args: Dict[str, Any], call_id: Optional[str] = None) -> None:
        """
        Add a function call to the conversation (OpenAI format).
        
        Args:
            name: Function name
            args: Function arguments
            call_id: Unique ID for this function call
        """
        # Convert args to string if needed for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "CONTENT": None,
            "function_call": {
                "name": name,
                "arguments": args_str
            }
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        call_info = {"args": args}
        if call_id:
            call_info["call_id"] = call_id
            
        self.function_calls[name].append(call_info)
    
    def xǁConversationMemoryǁadd_function_call__mutmut_11(self, name: str, args: Dict[str, Any], call_id: Optional[str] = None) -> None:
        """
        Add a function call to the conversation (OpenAI format).
        
        Args:
            name: Function name
            args: Function arguments
            call_id: Unique ID for this function call
        """
        # Convert args to string if needed for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "XXfunction_callXX": {
                "name": name,
                "arguments": args_str
            }
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        call_info = {"args": args}
        if call_id:
            call_info["call_id"] = call_id
            
        self.function_calls[name].append(call_info)
    
    def xǁConversationMemoryǁadd_function_call__mutmut_12(self, name: str, args: Dict[str, Any], call_id: Optional[str] = None) -> None:
        """
        Add a function call to the conversation (OpenAI format).
        
        Args:
            name: Function name
            args: Function arguments
            call_id: Unique ID for this function call
        """
        # Convert args to string if needed for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "FUNCTION_CALL": {
                "name": name,
                "arguments": args_str
            }
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        call_info = {"args": args}
        if call_id:
            call_info["call_id"] = call_id
            
        self.function_calls[name].append(call_info)
    
    def xǁConversationMemoryǁadd_function_call__mutmut_13(self, name: str, args: Dict[str, Any], call_id: Optional[str] = None) -> None:
        """
        Add a function call to the conversation (OpenAI format).
        
        Args:
            name: Function name
            args: Function arguments
            call_id: Unique ID for this function call
        """
        # Convert args to string if needed for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "function_call": {
                "XXnameXX": name,
                "arguments": args_str
            }
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        call_info = {"args": args}
        if call_id:
            call_info["call_id"] = call_id
            
        self.function_calls[name].append(call_info)
    
    def xǁConversationMemoryǁadd_function_call__mutmut_14(self, name: str, args: Dict[str, Any], call_id: Optional[str] = None) -> None:
        """
        Add a function call to the conversation (OpenAI format).
        
        Args:
            name: Function name
            args: Function arguments
            call_id: Unique ID for this function call
        """
        # Convert args to string if needed for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "function_call": {
                "NAME": name,
                "arguments": args_str
            }
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        call_info = {"args": args}
        if call_id:
            call_info["call_id"] = call_id
            
        self.function_calls[name].append(call_info)
    
    def xǁConversationMemoryǁadd_function_call__mutmut_15(self, name: str, args: Dict[str, Any], call_id: Optional[str] = None) -> None:
        """
        Add a function call to the conversation (OpenAI format).
        
        Args:
            name: Function name
            args: Function arguments
            call_id: Unique ID for this function call
        """
        # Convert args to string if needed for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "function_call": {
                "name": name,
                "XXargumentsXX": args_str
            }
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        call_info = {"args": args}
        if call_id:
            call_info["call_id"] = call_id
            
        self.function_calls[name].append(call_info)
    
    def xǁConversationMemoryǁadd_function_call__mutmut_16(self, name: str, args: Dict[str, Any], call_id: Optional[str] = None) -> None:
        """
        Add a function call to the conversation (OpenAI format).
        
        Args:
            name: Function name
            args: Function arguments
            call_id: Unique ID for this function call
        """
        # Convert args to string if needed for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "function_call": {
                "name": name,
                "ARGUMENTS": args_str
            }
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        call_info = {"args": args}
        if call_id:
            call_info["call_id"] = call_id
            
        self.function_calls[name].append(call_info)
    
    def xǁConversationMemoryǁadd_function_call__mutmut_17(self, name: str, args: Dict[str, Any], call_id: Optional[str] = None) -> None:
        """
        Add a function call to the conversation (OpenAI format).
        
        Args:
            name: Function name
            args: Function arguments
            call_id: Unique ID for this function call
        """
        # Convert args to string if needed for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "function_call": {
                "name": name,
                "arguments": args_str
            }
        }
        
        self.messages.append(None)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        call_info = {"args": args}
        if call_id:
            call_info["call_id"] = call_id
            
        self.function_calls[name].append(call_info)
    
    def xǁConversationMemoryǁadd_function_call__mutmut_18(self, name: str, args: Dict[str, Any], call_id: Optional[str] = None) -> None:
        """
        Add a function call to the conversation (OpenAI format).
        
        Args:
            name: Function name
            args: Function arguments
            call_id: Unique ID for this function call
        """
        # Convert args to string if needed for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "function_call": {
                "name": name,
                "arguments": args_str
            }
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name in self.function_calls:
            self.function_calls[name] = []
            
        call_info = {"args": args}
        if call_id:
            call_info["call_id"] = call_id
            
        self.function_calls[name].append(call_info)
    
    def xǁConversationMemoryǁadd_function_call__mutmut_19(self, name: str, args: Dict[str, Any], call_id: Optional[str] = None) -> None:
        """
        Add a function call to the conversation (OpenAI format).
        
        Args:
            name: Function name
            args: Function arguments
            call_id: Unique ID for this function call
        """
        # Convert args to string if needed for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "function_call": {
                "name": name,
                "arguments": args_str
            }
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = None
            
        call_info = {"args": args}
        if call_id:
            call_info["call_id"] = call_id
            
        self.function_calls[name].append(call_info)
    
    def xǁConversationMemoryǁadd_function_call__mutmut_20(self, name: str, args: Dict[str, Any], call_id: Optional[str] = None) -> None:
        """
        Add a function call to the conversation (OpenAI format).
        
        Args:
            name: Function name
            args: Function arguments
            call_id: Unique ID for this function call
        """
        # Convert args to string if needed for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "function_call": {
                "name": name,
                "arguments": args_str
            }
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        call_info = None
        if call_id:
            call_info["call_id"] = call_id
            
        self.function_calls[name].append(call_info)
    
    def xǁConversationMemoryǁadd_function_call__mutmut_21(self, name: str, args: Dict[str, Any], call_id: Optional[str] = None) -> None:
        """
        Add a function call to the conversation (OpenAI format).
        
        Args:
            name: Function name
            args: Function arguments
            call_id: Unique ID for this function call
        """
        # Convert args to string if needed for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "function_call": {
                "name": name,
                "arguments": args_str
            }
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        call_info = {"XXargsXX": args}
        if call_id:
            call_info["call_id"] = call_id
            
        self.function_calls[name].append(call_info)
    
    def xǁConversationMemoryǁadd_function_call__mutmut_22(self, name: str, args: Dict[str, Any], call_id: Optional[str] = None) -> None:
        """
        Add a function call to the conversation (OpenAI format).
        
        Args:
            name: Function name
            args: Function arguments
            call_id: Unique ID for this function call
        """
        # Convert args to string if needed for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "function_call": {
                "name": name,
                "arguments": args_str
            }
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        call_info = {"ARGS": args}
        if call_id:
            call_info["call_id"] = call_id
            
        self.function_calls[name].append(call_info)
    
    def xǁConversationMemoryǁadd_function_call__mutmut_23(self, name: str, args: Dict[str, Any], call_id: Optional[str] = None) -> None:
        """
        Add a function call to the conversation (OpenAI format).
        
        Args:
            name: Function name
            args: Function arguments
            call_id: Unique ID for this function call
        """
        # Convert args to string if needed for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "function_call": {
                "name": name,
                "arguments": args_str
            }
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        call_info = {"args": args}
        if call_id:
            call_info["call_id"] = None
            
        self.function_calls[name].append(call_info)
    
    def xǁConversationMemoryǁadd_function_call__mutmut_24(self, name: str, args: Dict[str, Any], call_id: Optional[str] = None) -> None:
        """
        Add a function call to the conversation (OpenAI format).
        
        Args:
            name: Function name
            args: Function arguments
            call_id: Unique ID for this function call
        """
        # Convert args to string if needed for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "function_call": {
                "name": name,
                "arguments": args_str
            }
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        call_info = {"args": args}
        if call_id:
            call_info["XXcall_idXX"] = call_id
            
        self.function_calls[name].append(call_info)
    
    def xǁConversationMemoryǁadd_function_call__mutmut_25(self, name: str, args: Dict[str, Any], call_id: Optional[str] = None) -> None:
        """
        Add a function call to the conversation (OpenAI format).
        
        Args:
            name: Function name
            args: Function arguments
            call_id: Unique ID for this function call
        """
        # Convert args to string if needed for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "function_call": {
                "name": name,
                "arguments": args_str
            }
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        call_info = {"args": args}
        if call_id:
            call_info["CALL_ID"] = call_id
            
        self.function_calls[name].append(call_info)
    
    def xǁConversationMemoryǁadd_function_call__mutmut_26(self, name: str, args: Dict[str, Any], call_id: Optional[str] = None) -> None:
        """
        Add a function call to the conversation (OpenAI format).
        
        Args:
            name: Function name
            args: Function arguments
            call_id: Unique ID for this function call
        """
        # Convert args to string if needed for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "function_call": {
                "name": name,
                "arguments": args_str
            }
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        call_info = {"args": args}
        if call_id:
            call_info["call_id"] = call_id
            
        self.function_calls[name].append(None)
    
    xǁConversationMemoryǁadd_function_call__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁConversationMemoryǁadd_function_call__mutmut_1': xǁConversationMemoryǁadd_function_call__mutmut_1, 
        'xǁConversationMemoryǁadd_function_call__mutmut_2': xǁConversationMemoryǁadd_function_call__mutmut_2, 
        'xǁConversationMemoryǁadd_function_call__mutmut_3': xǁConversationMemoryǁadd_function_call__mutmut_3, 
        'xǁConversationMemoryǁadd_function_call__mutmut_4': xǁConversationMemoryǁadd_function_call__mutmut_4, 
        'xǁConversationMemoryǁadd_function_call__mutmut_5': xǁConversationMemoryǁadd_function_call__mutmut_5, 
        'xǁConversationMemoryǁadd_function_call__mutmut_6': xǁConversationMemoryǁadd_function_call__mutmut_6, 
        'xǁConversationMemoryǁadd_function_call__mutmut_7': xǁConversationMemoryǁadd_function_call__mutmut_7, 
        'xǁConversationMemoryǁadd_function_call__mutmut_8': xǁConversationMemoryǁadd_function_call__mutmut_8, 
        'xǁConversationMemoryǁadd_function_call__mutmut_9': xǁConversationMemoryǁadd_function_call__mutmut_9, 
        'xǁConversationMemoryǁadd_function_call__mutmut_10': xǁConversationMemoryǁadd_function_call__mutmut_10, 
        'xǁConversationMemoryǁadd_function_call__mutmut_11': xǁConversationMemoryǁadd_function_call__mutmut_11, 
        'xǁConversationMemoryǁadd_function_call__mutmut_12': xǁConversationMemoryǁadd_function_call__mutmut_12, 
        'xǁConversationMemoryǁadd_function_call__mutmut_13': xǁConversationMemoryǁadd_function_call__mutmut_13, 
        'xǁConversationMemoryǁadd_function_call__mutmut_14': xǁConversationMemoryǁadd_function_call__mutmut_14, 
        'xǁConversationMemoryǁadd_function_call__mutmut_15': xǁConversationMemoryǁadd_function_call__mutmut_15, 
        'xǁConversationMemoryǁadd_function_call__mutmut_16': xǁConversationMemoryǁadd_function_call__mutmut_16, 
        'xǁConversationMemoryǁadd_function_call__mutmut_17': xǁConversationMemoryǁadd_function_call__mutmut_17, 
        'xǁConversationMemoryǁadd_function_call__mutmut_18': xǁConversationMemoryǁadd_function_call__mutmut_18, 
        'xǁConversationMemoryǁadd_function_call__mutmut_19': xǁConversationMemoryǁadd_function_call__mutmut_19, 
        'xǁConversationMemoryǁadd_function_call__mutmut_20': xǁConversationMemoryǁadd_function_call__mutmut_20, 
        'xǁConversationMemoryǁadd_function_call__mutmut_21': xǁConversationMemoryǁadd_function_call__mutmut_21, 
        'xǁConversationMemoryǁadd_function_call__mutmut_22': xǁConversationMemoryǁadd_function_call__mutmut_22, 
        'xǁConversationMemoryǁadd_function_call__mutmut_23': xǁConversationMemoryǁadd_function_call__mutmut_23, 
        'xǁConversationMemoryǁadd_function_call__mutmut_24': xǁConversationMemoryǁadd_function_call__mutmut_24, 
        'xǁConversationMemoryǁadd_function_call__mutmut_25': xǁConversationMemoryǁadd_function_call__mutmut_25, 
        'xǁConversationMemoryǁadd_function_call__mutmut_26': xǁConversationMemoryǁadd_function_call__mutmut_26
    }
    
    def add_function_call(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁConversationMemoryǁadd_function_call__mutmut_orig"), object.__getattribute__(self, "xǁConversationMemoryǁadd_function_call__mutmut_mutants"), args, kwargs, self)
        return result 
    
    add_function_call.__signature__ = _mutmut_signature(xǁConversationMemoryǁadd_function_call__mutmut_orig)
    xǁConversationMemoryǁadd_function_call__mutmut_orig.__name__ = 'xǁConversationMemoryǁadd_function_call'
    
    def xǁConversationMemoryǁadd_tool_call__mutmut_orig(self, name: str, args: Dict[str, Any], call_id: str) -> None:
        """
        Add a tool call to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            args: Tool arguments
            call_id: Unique ID for this tool call
        """
        # Convert args to string for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": call_id,
                    "type": "function",
                    "function": {
                        "name": name,
                        "arguments": args_str
                    }
                }
            ]
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        self.function_calls[name].append({"args": args, "call_id": call_id})
    
    def xǁConversationMemoryǁadd_tool_call__mutmut_1(self, name: str, args: Dict[str, Any], call_id: str) -> None:
        """
        Add a tool call to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            args: Tool arguments
            call_id: Unique ID for this tool call
        """
        # Convert args to string for OpenAI format
        args_str = None
        
        message = {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": call_id,
                    "type": "function",
                    "function": {
                        "name": name,
                        "arguments": args_str
                    }
                }
            ]
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        self.function_calls[name].append({"args": args, "call_id": call_id})
    
    def xǁConversationMemoryǁadd_tool_call__mutmut_2(self, name: str, args: Dict[str, Any], call_id: str) -> None:
        """
        Add a tool call to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            args: Tool arguments
            call_id: Unique ID for this tool call
        """
        # Convert args to string for OpenAI format
        args_str = json.dumps(None) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": call_id,
                    "type": "function",
                    "function": {
                        "name": name,
                        "arguments": args_str
                    }
                }
            ]
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        self.function_calls[name].append({"args": args, "call_id": call_id})
    
    def xǁConversationMemoryǁadd_tool_call__mutmut_3(self, name: str, args: Dict[str, Any], call_id: str) -> None:
        """
        Add a tool call to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            args: Tool arguments
            call_id: Unique ID for this tool call
        """
        # Convert args to string for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(None)
        
        message = {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": call_id,
                    "type": "function",
                    "function": {
                        "name": name,
                        "arguments": args_str
                    }
                }
            ]
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        self.function_calls[name].append({"args": args, "call_id": call_id})
    
    def xǁConversationMemoryǁadd_tool_call__mutmut_4(self, name: str, args: Dict[str, Any], call_id: str) -> None:
        """
        Add a tool call to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            args: Tool arguments
            call_id: Unique ID for this tool call
        """
        # Convert args to string for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = None
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        self.function_calls[name].append({"args": args, "call_id": call_id})
    
    def xǁConversationMemoryǁadd_tool_call__mutmut_5(self, name: str, args: Dict[str, Any], call_id: str) -> None:
        """
        Add a tool call to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            args: Tool arguments
            call_id: Unique ID for this tool call
        """
        # Convert args to string for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "XXroleXX": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": call_id,
                    "type": "function",
                    "function": {
                        "name": name,
                        "arguments": args_str
                    }
                }
            ]
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        self.function_calls[name].append({"args": args, "call_id": call_id})
    
    def xǁConversationMemoryǁadd_tool_call__mutmut_6(self, name: str, args: Dict[str, Any], call_id: str) -> None:
        """
        Add a tool call to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            args: Tool arguments
            call_id: Unique ID for this tool call
        """
        # Convert args to string for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "ROLE": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": call_id,
                    "type": "function",
                    "function": {
                        "name": name,
                        "arguments": args_str
                    }
                }
            ]
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        self.function_calls[name].append({"args": args, "call_id": call_id})
    
    def xǁConversationMemoryǁadd_tool_call__mutmut_7(self, name: str, args: Dict[str, Any], call_id: str) -> None:
        """
        Add a tool call to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            args: Tool arguments
            call_id: Unique ID for this tool call
        """
        # Convert args to string for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "XXassistantXX",
            "content": None,
            "tool_calls": [
                {
                    "id": call_id,
                    "type": "function",
                    "function": {
                        "name": name,
                        "arguments": args_str
                    }
                }
            ]
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        self.function_calls[name].append({"args": args, "call_id": call_id})
    
    def xǁConversationMemoryǁadd_tool_call__mutmut_8(self, name: str, args: Dict[str, Any], call_id: str) -> None:
        """
        Add a tool call to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            args: Tool arguments
            call_id: Unique ID for this tool call
        """
        # Convert args to string for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "ASSISTANT",
            "content": None,
            "tool_calls": [
                {
                    "id": call_id,
                    "type": "function",
                    "function": {
                        "name": name,
                        "arguments": args_str
                    }
                }
            ]
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        self.function_calls[name].append({"args": args, "call_id": call_id})
    
    def xǁConversationMemoryǁadd_tool_call__mutmut_9(self, name: str, args: Dict[str, Any], call_id: str) -> None:
        """
        Add a tool call to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            args: Tool arguments
            call_id: Unique ID for this tool call
        """
        # Convert args to string for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "XXcontentXX": None,
            "tool_calls": [
                {
                    "id": call_id,
                    "type": "function",
                    "function": {
                        "name": name,
                        "arguments": args_str
                    }
                }
            ]
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        self.function_calls[name].append({"args": args, "call_id": call_id})
    
    def xǁConversationMemoryǁadd_tool_call__mutmut_10(self, name: str, args: Dict[str, Any], call_id: str) -> None:
        """
        Add a tool call to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            args: Tool arguments
            call_id: Unique ID for this tool call
        """
        # Convert args to string for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "CONTENT": None,
            "tool_calls": [
                {
                    "id": call_id,
                    "type": "function",
                    "function": {
                        "name": name,
                        "arguments": args_str
                    }
                }
            ]
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        self.function_calls[name].append({"args": args, "call_id": call_id})
    
    def xǁConversationMemoryǁadd_tool_call__mutmut_11(self, name: str, args: Dict[str, Any], call_id: str) -> None:
        """
        Add a tool call to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            args: Tool arguments
            call_id: Unique ID for this tool call
        """
        # Convert args to string for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "XXtool_callsXX": [
                {
                    "id": call_id,
                    "type": "function",
                    "function": {
                        "name": name,
                        "arguments": args_str
                    }
                }
            ]
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        self.function_calls[name].append({"args": args, "call_id": call_id})
    
    def xǁConversationMemoryǁadd_tool_call__mutmut_12(self, name: str, args: Dict[str, Any], call_id: str) -> None:
        """
        Add a tool call to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            args: Tool arguments
            call_id: Unique ID for this tool call
        """
        # Convert args to string for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "TOOL_CALLS": [
                {
                    "id": call_id,
                    "type": "function",
                    "function": {
                        "name": name,
                        "arguments": args_str
                    }
                }
            ]
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        self.function_calls[name].append({"args": args, "call_id": call_id})
    
    def xǁConversationMemoryǁadd_tool_call__mutmut_13(self, name: str, args: Dict[str, Any], call_id: str) -> None:
        """
        Add a tool call to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            args: Tool arguments
            call_id: Unique ID for this tool call
        """
        # Convert args to string for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "XXidXX": call_id,
                    "type": "function",
                    "function": {
                        "name": name,
                        "arguments": args_str
                    }
                }
            ]
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        self.function_calls[name].append({"args": args, "call_id": call_id})
    
    def xǁConversationMemoryǁadd_tool_call__mutmut_14(self, name: str, args: Dict[str, Any], call_id: str) -> None:
        """
        Add a tool call to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            args: Tool arguments
            call_id: Unique ID for this tool call
        """
        # Convert args to string for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "ID": call_id,
                    "type": "function",
                    "function": {
                        "name": name,
                        "arguments": args_str
                    }
                }
            ]
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        self.function_calls[name].append({"args": args, "call_id": call_id})
    
    def xǁConversationMemoryǁadd_tool_call__mutmut_15(self, name: str, args: Dict[str, Any], call_id: str) -> None:
        """
        Add a tool call to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            args: Tool arguments
            call_id: Unique ID for this tool call
        """
        # Convert args to string for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": call_id,
                    "XXtypeXX": "function",
                    "function": {
                        "name": name,
                        "arguments": args_str
                    }
                }
            ]
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        self.function_calls[name].append({"args": args, "call_id": call_id})
    
    def xǁConversationMemoryǁadd_tool_call__mutmut_16(self, name: str, args: Dict[str, Any], call_id: str) -> None:
        """
        Add a tool call to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            args: Tool arguments
            call_id: Unique ID for this tool call
        """
        # Convert args to string for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": call_id,
                    "TYPE": "function",
                    "function": {
                        "name": name,
                        "arguments": args_str
                    }
                }
            ]
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        self.function_calls[name].append({"args": args, "call_id": call_id})
    
    def xǁConversationMemoryǁadd_tool_call__mutmut_17(self, name: str, args: Dict[str, Any], call_id: str) -> None:
        """
        Add a tool call to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            args: Tool arguments
            call_id: Unique ID for this tool call
        """
        # Convert args to string for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": call_id,
                    "type": "XXfunctionXX",
                    "function": {
                        "name": name,
                        "arguments": args_str
                    }
                }
            ]
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        self.function_calls[name].append({"args": args, "call_id": call_id})
    
    def xǁConversationMemoryǁadd_tool_call__mutmut_18(self, name: str, args: Dict[str, Any], call_id: str) -> None:
        """
        Add a tool call to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            args: Tool arguments
            call_id: Unique ID for this tool call
        """
        # Convert args to string for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": call_id,
                    "type": "FUNCTION",
                    "function": {
                        "name": name,
                        "arguments": args_str
                    }
                }
            ]
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        self.function_calls[name].append({"args": args, "call_id": call_id})
    
    def xǁConversationMemoryǁadd_tool_call__mutmut_19(self, name: str, args: Dict[str, Any], call_id: str) -> None:
        """
        Add a tool call to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            args: Tool arguments
            call_id: Unique ID for this tool call
        """
        # Convert args to string for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": call_id,
                    "type": "function",
                    "XXfunctionXX": {
                        "name": name,
                        "arguments": args_str
                    }
                }
            ]
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        self.function_calls[name].append({"args": args, "call_id": call_id})
    
    def xǁConversationMemoryǁadd_tool_call__mutmut_20(self, name: str, args: Dict[str, Any], call_id: str) -> None:
        """
        Add a tool call to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            args: Tool arguments
            call_id: Unique ID for this tool call
        """
        # Convert args to string for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": call_id,
                    "type": "function",
                    "FUNCTION": {
                        "name": name,
                        "arguments": args_str
                    }
                }
            ]
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        self.function_calls[name].append({"args": args, "call_id": call_id})
    
    def xǁConversationMemoryǁadd_tool_call__mutmut_21(self, name: str, args: Dict[str, Any], call_id: str) -> None:
        """
        Add a tool call to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            args: Tool arguments
            call_id: Unique ID for this tool call
        """
        # Convert args to string for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": call_id,
                    "type": "function",
                    "function": {
                        "XXnameXX": name,
                        "arguments": args_str
                    }
                }
            ]
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        self.function_calls[name].append({"args": args, "call_id": call_id})
    
    def xǁConversationMemoryǁadd_tool_call__mutmut_22(self, name: str, args: Dict[str, Any], call_id: str) -> None:
        """
        Add a tool call to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            args: Tool arguments
            call_id: Unique ID for this tool call
        """
        # Convert args to string for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": call_id,
                    "type": "function",
                    "function": {
                        "NAME": name,
                        "arguments": args_str
                    }
                }
            ]
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        self.function_calls[name].append({"args": args, "call_id": call_id})
    
    def xǁConversationMemoryǁadd_tool_call__mutmut_23(self, name: str, args: Dict[str, Any], call_id: str) -> None:
        """
        Add a tool call to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            args: Tool arguments
            call_id: Unique ID for this tool call
        """
        # Convert args to string for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": call_id,
                    "type": "function",
                    "function": {
                        "name": name,
                        "XXargumentsXX": args_str
                    }
                }
            ]
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        self.function_calls[name].append({"args": args, "call_id": call_id})
    
    def xǁConversationMemoryǁadd_tool_call__mutmut_24(self, name: str, args: Dict[str, Any], call_id: str) -> None:
        """
        Add a tool call to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            args: Tool arguments
            call_id: Unique ID for this tool call
        """
        # Convert args to string for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": call_id,
                    "type": "function",
                    "function": {
                        "name": name,
                        "ARGUMENTS": args_str
                    }
                }
            ]
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        self.function_calls[name].append({"args": args, "call_id": call_id})
    
    def xǁConversationMemoryǁadd_tool_call__mutmut_25(self, name: str, args: Dict[str, Any], call_id: str) -> None:
        """
        Add a tool call to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            args: Tool arguments
            call_id: Unique ID for this tool call
        """
        # Convert args to string for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": call_id,
                    "type": "function",
                    "function": {
                        "name": name,
                        "arguments": args_str
                    }
                }
            ]
        }
        
        self.messages.append(None)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        self.function_calls[name].append({"args": args, "call_id": call_id})
    
    def xǁConversationMemoryǁadd_tool_call__mutmut_26(self, name: str, args: Dict[str, Any], call_id: str) -> None:
        """
        Add a tool call to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            args: Tool arguments
            call_id: Unique ID for this tool call
        """
        # Convert args to string for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": call_id,
                    "type": "function",
                    "function": {
                        "name": name,
                        "arguments": args_str
                    }
                }
            ]
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name in self.function_calls:
            self.function_calls[name] = []
            
        self.function_calls[name].append({"args": args, "call_id": call_id})
    
    def xǁConversationMemoryǁadd_tool_call__mutmut_27(self, name: str, args: Dict[str, Any], call_id: str) -> None:
        """
        Add a tool call to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            args: Tool arguments
            call_id: Unique ID for this tool call
        """
        # Convert args to string for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": call_id,
                    "type": "function",
                    "function": {
                        "name": name,
                        "arguments": args_str
                    }
                }
            ]
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = None
            
        self.function_calls[name].append({"args": args, "call_id": call_id})
    
    def xǁConversationMemoryǁadd_tool_call__mutmut_28(self, name: str, args: Dict[str, Any], call_id: str) -> None:
        """
        Add a tool call to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            args: Tool arguments
            call_id: Unique ID for this tool call
        """
        # Convert args to string for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": call_id,
                    "type": "function",
                    "function": {
                        "name": name,
                        "arguments": args_str
                    }
                }
            ]
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        self.function_calls[name].append(None)
    
    def xǁConversationMemoryǁadd_tool_call__mutmut_29(self, name: str, args: Dict[str, Any], call_id: str) -> None:
        """
        Add a tool call to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            args: Tool arguments
            call_id: Unique ID for this tool call
        """
        # Convert args to string for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": call_id,
                    "type": "function",
                    "function": {
                        "name": name,
                        "arguments": args_str
                    }
                }
            ]
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        self.function_calls[name].append({"XXargsXX": args, "call_id": call_id})
    
    def xǁConversationMemoryǁadd_tool_call__mutmut_30(self, name: str, args: Dict[str, Any], call_id: str) -> None:
        """
        Add a tool call to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            args: Tool arguments
            call_id: Unique ID for this tool call
        """
        # Convert args to string for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": call_id,
                    "type": "function",
                    "function": {
                        "name": name,
                        "arguments": args_str
                    }
                }
            ]
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        self.function_calls[name].append({"ARGS": args, "call_id": call_id})
    
    def xǁConversationMemoryǁadd_tool_call__mutmut_31(self, name: str, args: Dict[str, Any], call_id: str) -> None:
        """
        Add a tool call to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            args: Tool arguments
            call_id: Unique ID for this tool call
        """
        # Convert args to string for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": call_id,
                    "type": "function",
                    "function": {
                        "name": name,
                        "arguments": args_str
                    }
                }
            ]
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        self.function_calls[name].append({"args": args, "XXcall_idXX": call_id})
    
    def xǁConversationMemoryǁadd_tool_call__mutmut_32(self, name: str, args: Dict[str, Any], call_id: str) -> None:
        """
        Add a tool call to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            args: Tool arguments
            call_id: Unique ID for this tool call
        """
        # Convert args to string for OpenAI format
        args_str = json.dumps(args) if isinstance(args, dict) else str(args)
        
        message = {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": call_id,
                    "type": "function",
                    "function": {
                        "name": name,
                        "arguments": args_str
                    }
                }
            ]
        }
        
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
            
        self.function_calls[name].append({"args": args, "CALL_ID": call_id})
    
    xǁConversationMemoryǁadd_tool_call__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁConversationMemoryǁadd_tool_call__mutmut_1': xǁConversationMemoryǁadd_tool_call__mutmut_1, 
        'xǁConversationMemoryǁadd_tool_call__mutmut_2': xǁConversationMemoryǁadd_tool_call__mutmut_2, 
        'xǁConversationMemoryǁadd_tool_call__mutmut_3': xǁConversationMemoryǁadd_tool_call__mutmut_3, 
        'xǁConversationMemoryǁadd_tool_call__mutmut_4': xǁConversationMemoryǁadd_tool_call__mutmut_4, 
        'xǁConversationMemoryǁadd_tool_call__mutmut_5': xǁConversationMemoryǁadd_tool_call__mutmut_5, 
        'xǁConversationMemoryǁadd_tool_call__mutmut_6': xǁConversationMemoryǁadd_tool_call__mutmut_6, 
        'xǁConversationMemoryǁadd_tool_call__mutmut_7': xǁConversationMemoryǁadd_tool_call__mutmut_7, 
        'xǁConversationMemoryǁadd_tool_call__mutmut_8': xǁConversationMemoryǁadd_tool_call__mutmut_8, 
        'xǁConversationMemoryǁadd_tool_call__mutmut_9': xǁConversationMemoryǁadd_tool_call__mutmut_9, 
        'xǁConversationMemoryǁadd_tool_call__mutmut_10': xǁConversationMemoryǁadd_tool_call__mutmut_10, 
        'xǁConversationMemoryǁadd_tool_call__mutmut_11': xǁConversationMemoryǁadd_tool_call__mutmut_11, 
        'xǁConversationMemoryǁadd_tool_call__mutmut_12': xǁConversationMemoryǁadd_tool_call__mutmut_12, 
        'xǁConversationMemoryǁadd_tool_call__mutmut_13': xǁConversationMemoryǁadd_tool_call__mutmut_13, 
        'xǁConversationMemoryǁadd_tool_call__mutmut_14': xǁConversationMemoryǁadd_tool_call__mutmut_14, 
        'xǁConversationMemoryǁadd_tool_call__mutmut_15': xǁConversationMemoryǁadd_tool_call__mutmut_15, 
        'xǁConversationMemoryǁadd_tool_call__mutmut_16': xǁConversationMemoryǁadd_tool_call__mutmut_16, 
        'xǁConversationMemoryǁadd_tool_call__mutmut_17': xǁConversationMemoryǁadd_tool_call__mutmut_17, 
        'xǁConversationMemoryǁadd_tool_call__mutmut_18': xǁConversationMemoryǁadd_tool_call__mutmut_18, 
        'xǁConversationMemoryǁadd_tool_call__mutmut_19': xǁConversationMemoryǁadd_tool_call__mutmut_19, 
        'xǁConversationMemoryǁadd_tool_call__mutmut_20': xǁConversationMemoryǁadd_tool_call__mutmut_20, 
        'xǁConversationMemoryǁadd_tool_call__mutmut_21': xǁConversationMemoryǁadd_tool_call__mutmut_21, 
        'xǁConversationMemoryǁadd_tool_call__mutmut_22': xǁConversationMemoryǁadd_tool_call__mutmut_22, 
        'xǁConversationMemoryǁadd_tool_call__mutmut_23': xǁConversationMemoryǁadd_tool_call__mutmut_23, 
        'xǁConversationMemoryǁadd_tool_call__mutmut_24': xǁConversationMemoryǁadd_tool_call__mutmut_24, 
        'xǁConversationMemoryǁadd_tool_call__mutmut_25': xǁConversationMemoryǁadd_tool_call__mutmut_25, 
        'xǁConversationMemoryǁadd_tool_call__mutmut_26': xǁConversationMemoryǁadd_tool_call__mutmut_26, 
        'xǁConversationMemoryǁadd_tool_call__mutmut_27': xǁConversationMemoryǁadd_tool_call__mutmut_27, 
        'xǁConversationMemoryǁadd_tool_call__mutmut_28': xǁConversationMemoryǁadd_tool_call__mutmut_28, 
        'xǁConversationMemoryǁadd_tool_call__mutmut_29': xǁConversationMemoryǁadd_tool_call__mutmut_29, 
        'xǁConversationMemoryǁadd_tool_call__mutmut_30': xǁConversationMemoryǁadd_tool_call__mutmut_30, 
        'xǁConversationMemoryǁadd_tool_call__mutmut_31': xǁConversationMemoryǁadd_tool_call__mutmut_31, 
        'xǁConversationMemoryǁadd_tool_call__mutmut_32': xǁConversationMemoryǁadd_tool_call__mutmut_32
    }
    
    def add_tool_call(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁConversationMemoryǁadd_tool_call__mutmut_orig"), object.__getattribute__(self, "xǁConversationMemoryǁadd_tool_call__mutmut_mutants"), args, kwargs, self)
        return result 
    
    add_tool_call.__signature__ = _mutmut_signature(xǁConversationMemoryǁadd_tool_call__mutmut_orig)
    xǁConversationMemoryǁadd_tool_call__mutmut_orig.__name__ = 'xǁConversationMemoryǁadd_tool_call'
    
    def xǁConversationMemoryǁadd_function_result__mutmut_orig(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "assistant",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "tool",
                "name": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_1(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = True, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "assistant",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "tool",
                "name": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_2(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider or provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "assistant",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "tool",
                "name": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_3(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.upper() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "assistant",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "tool",
                "name": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_4(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() != "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "assistant",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "tool",
                "name": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_5(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "XXanthropicXX":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "assistant",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "tool",
                "name": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_6(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "ANTHROPIC":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "assistant",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "tool",
                "name": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_7(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = None
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "tool",
                "name": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_8(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "XXroleXX": "assistant",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "tool",
                "name": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_9(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "ROLE": "assistant",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "tool",
                "name": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_10(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "XXassistantXX",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "tool",
                "name": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_11(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "ASSISTANT",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "tool",
                "name": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_12(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "assistant",
                "XXcontentXX": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "tool",
                "name": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_13(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "assistant",
                "CONTENT": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "tool",
                "name": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_14(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "assistant",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = None
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_15(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "assistant",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "XXroleXX": "tool",
                "name": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_16(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "assistant",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "ROLE": "tool",
                "name": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_17(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "assistant",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "XXtoolXX",
                "name": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_18(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "assistant",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "TOOL",
                "name": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_19(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "assistant",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "tool",
                "XXnameXX": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_20(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "assistant",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "tool",
                "NAME": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_21(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "assistant",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "tool",
                "name": name,
                "XXcontentXX": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_22(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "assistant",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "tool",
                "name": name,
                "CONTENT": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_23(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "assistant",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "tool",
                "name": name,
                "content": str(None)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_24(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "assistant",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "tool",
                "name": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = None
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_25(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "assistant",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "tool",
                "name": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["XXtool_call_idXX"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_26(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "assistant",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "tool",
                "name": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["TOOL_CALL_ID"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_27(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "assistant",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "tool",
                "name": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = None
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_28(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "assistant",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "tool",
                "name": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["XXis_errorXX"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_29(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "assistant",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "tool",
                "name": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["IS_ERROR"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_30(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "assistant",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "tool",
                "name": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = False
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_31(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "assistant",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "tool",
                "name": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = None
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_32(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "assistant",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "tool",
                "name": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["XXargsXX"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_33(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "assistant",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "tool",
                "name": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["ARGS"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_34(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "assistant",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "tool",
                "name": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(None)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_35(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "assistant",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "tool",
                "name": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_36(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "assistant",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "tool",
                "name": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = None
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_37(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "assistant",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "tool",
                "name": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = None
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_38(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "assistant",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "tool",
                "name": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "XXnameXX": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_39(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "assistant",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "tool",
                "name": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "NAME": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_40(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "assistant",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "tool",
                "name": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "XXresultXX": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_41(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "assistant",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "tool",
                "name": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "RESULT": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_42(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "assistant",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "tool",
                "name": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = None
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_43(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "assistant",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "tool",
                "name": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["XXargsXX"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_44(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "assistant",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "tool",
                "name": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["ARGS"] = args
        if call_id:
            self.last_function_call["call_id"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_45(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "assistant",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "tool",
                "name": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["call_id"] = None
    
    def xǁConversationMemoryǁadd_function_result__mutmut_46(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "assistant",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "tool",
                "name": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["XXcall_idXX"] = call_id
    
    def xǁConversationMemoryǁadd_function_result__mutmut_47(self, name: str, content: str, args: Optional[Dict] = None, call_id: Optional[str] = None, is_error: bool = False, provider: Optional[str] = None) -> None:
        """
        Add a function result to the conversation.
        
        Args:
            name: Function name
            content: Function result
            args: Function arguments
            call_id: Unique ID for this function call (to link call with result)
            is_error: Whether this result represents an error
            provider: The model provider (e.g., "anthropic", "openai")
        """
        # Handle provider-specific tool result formats
        if provider and provider.lower() == "anthropic":
            # For Anthropic, use assistant role with text content to avoid tool_result validation issues
            message = {
                "role": "assistant",
                "content": f"I called the {name} function with {args} and got this result: {content}"
            }
        else:
            # Use modern 'tool' role for all other providers (including Ollama with native tool calling)
            message = {
                "role": "tool",
                "name": name,
                "content": str(content)
            }
            
            # Add tool call ID if provided (modern format)
            if call_id:
                message["tool_call_id"] = call_id
                
            # Add error flag if this is an error result
            if is_error:
                message["is_error"] = True
                
            if args:
                # Store args for better repetition detection
                message["args"] = args
            
        self.messages.append(message)
        
        # Track function calls for loop detection
        if name not in self.function_calls:
            self.function_calls[name] = []
        
        # Update the last_function_call with the complete information
        self.last_function_call = {
            "name": name,
            "result": content
        }
        
        if args:
            self.last_function_call["args"] = args
        if call_id:
            self.last_function_call["CALL_ID"] = call_id
    
    xǁConversationMemoryǁadd_function_result__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁConversationMemoryǁadd_function_result__mutmut_1': xǁConversationMemoryǁadd_function_result__mutmut_1, 
        'xǁConversationMemoryǁadd_function_result__mutmut_2': xǁConversationMemoryǁadd_function_result__mutmut_2, 
        'xǁConversationMemoryǁadd_function_result__mutmut_3': xǁConversationMemoryǁadd_function_result__mutmut_3, 
        'xǁConversationMemoryǁadd_function_result__mutmut_4': xǁConversationMemoryǁadd_function_result__mutmut_4, 
        'xǁConversationMemoryǁadd_function_result__mutmut_5': xǁConversationMemoryǁadd_function_result__mutmut_5, 
        'xǁConversationMemoryǁadd_function_result__mutmut_6': xǁConversationMemoryǁadd_function_result__mutmut_6, 
        'xǁConversationMemoryǁadd_function_result__mutmut_7': xǁConversationMemoryǁadd_function_result__mutmut_7, 
        'xǁConversationMemoryǁadd_function_result__mutmut_8': xǁConversationMemoryǁadd_function_result__mutmut_8, 
        'xǁConversationMemoryǁadd_function_result__mutmut_9': xǁConversationMemoryǁadd_function_result__mutmut_9, 
        'xǁConversationMemoryǁadd_function_result__mutmut_10': xǁConversationMemoryǁadd_function_result__mutmut_10, 
        'xǁConversationMemoryǁadd_function_result__mutmut_11': xǁConversationMemoryǁadd_function_result__mutmut_11, 
        'xǁConversationMemoryǁadd_function_result__mutmut_12': xǁConversationMemoryǁadd_function_result__mutmut_12, 
        'xǁConversationMemoryǁadd_function_result__mutmut_13': xǁConversationMemoryǁadd_function_result__mutmut_13, 
        'xǁConversationMemoryǁadd_function_result__mutmut_14': xǁConversationMemoryǁadd_function_result__mutmut_14, 
        'xǁConversationMemoryǁadd_function_result__mutmut_15': xǁConversationMemoryǁadd_function_result__mutmut_15, 
        'xǁConversationMemoryǁadd_function_result__mutmut_16': xǁConversationMemoryǁadd_function_result__mutmut_16, 
        'xǁConversationMemoryǁadd_function_result__mutmut_17': xǁConversationMemoryǁadd_function_result__mutmut_17, 
        'xǁConversationMemoryǁadd_function_result__mutmut_18': xǁConversationMemoryǁadd_function_result__mutmut_18, 
        'xǁConversationMemoryǁadd_function_result__mutmut_19': xǁConversationMemoryǁadd_function_result__mutmut_19, 
        'xǁConversationMemoryǁadd_function_result__mutmut_20': xǁConversationMemoryǁadd_function_result__mutmut_20, 
        'xǁConversationMemoryǁadd_function_result__mutmut_21': xǁConversationMemoryǁadd_function_result__mutmut_21, 
        'xǁConversationMemoryǁadd_function_result__mutmut_22': xǁConversationMemoryǁadd_function_result__mutmut_22, 
        'xǁConversationMemoryǁadd_function_result__mutmut_23': xǁConversationMemoryǁadd_function_result__mutmut_23, 
        'xǁConversationMemoryǁadd_function_result__mutmut_24': xǁConversationMemoryǁadd_function_result__mutmut_24, 
        'xǁConversationMemoryǁadd_function_result__mutmut_25': xǁConversationMemoryǁadd_function_result__mutmut_25, 
        'xǁConversationMemoryǁadd_function_result__mutmut_26': xǁConversationMemoryǁadd_function_result__mutmut_26, 
        'xǁConversationMemoryǁadd_function_result__mutmut_27': xǁConversationMemoryǁadd_function_result__mutmut_27, 
        'xǁConversationMemoryǁadd_function_result__mutmut_28': xǁConversationMemoryǁadd_function_result__mutmut_28, 
        'xǁConversationMemoryǁadd_function_result__mutmut_29': xǁConversationMemoryǁadd_function_result__mutmut_29, 
        'xǁConversationMemoryǁadd_function_result__mutmut_30': xǁConversationMemoryǁadd_function_result__mutmut_30, 
        'xǁConversationMemoryǁadd_function_result__mutmut_31': xǁConversationMemoryǁadd_function_result__mutmut_31, 
        'xǁConversationMemoryǁadd_function_result__mutmut_32': xǁConversationMemoryǁadd_function_result__mutmut_32, 
        'xǁConversationMemoryǁadd_function_result__mutmut_33': xǁConversationMemoryǁadd_function_result__mutmut_33, 
        'xǁConversationMemoryǁadd_function_result__mutmut_34': xǁConversationMemoryǁadd_function_result__mutmut_34, 
        'xǁConversationMemoryǁadd_function_result__mutmut_35': xǁConversationMemoryǁadd_function_result__mutmut_35, 
        'xǁConversationMemoryǁadd_function_result__mutmut_36': xǁConversationMemoryǁadd_function_result__mutmut_36, 
        'xǁConversationMemoryǁadd_function_result__mutmut_37': xǁConversationMemoryǁadd_function_result__mutmut_37, 
        'xǁConversationMemoryǁadd_function_result__mutmut_38': xǁConversationMemoryǁadd_function_result__mutmut_38, 
        'xǁConversationMemoryǁadd_function_result__mutmut_39': xǁConversationMemoryǁadd_function_result__mutmut_39, 
        'xǁConversationMemoryǁadd_function_result__mutmut_40': xǁConversationMemoryǁadd_function_result__mutmut_40, 
        'xǁConversationMemoryǁadd_function_result__mutmut_41': xǁConversationMemoryǁadd_function_result__mutmut_41, 
        'xǁConversationMemoryǁadd_function_result__mutmut_42': xǁConversationMemoryǁadd_function_result__mutmut_42, 
        'xǁConversationMemoryǁadd_function_result__mutmut_43': xǁConversationMemoryǁadd_function_result__mutmut_43, 
        'xǁConversationMemoryǁadd_function_result__mutmut_44': xǁConversationMemoryǁadd_function_result__mutmut_44, 
        'xǁConversationMemoryǁadd_function_result__mutmut_45': xǁConversationMemoryǁadd_function_result__mutmut_45, 
        'xǁConversationMemoryǁadd_function_result__mutmut_46': xǁConversationMemoryǁadd_function_result__mutmut_46, 
        'xǁConversationMemoryǁadd_function_result__mutmut_47': xǁConversationMemoryǁadd_function_result__mutmut_47
    }
    
    def add_function_result(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁConversationMemoryǁadd_function_result__mutmut_orig"), object.__getattribute__(self, "xǁConversationMemoryǁadd_function_result__mutmut_mutants"), args, kwargs, self)
        return result 
    
    add_function_result.__signature__ = _mutmut_signature(xǁConversationMemoryǁadd_function_result__mutmut_orig)
    xǁConversationMemoryǁadd_function_result__mutmut_orig.__name__ = 'xǁConversationMemoryǁadd_function_result'
    
    def xǁConversationMemoryǁadd_tool_result__mutmut_orig(self, name: str, content: str, call_id: str, is_error: bool = False) -> None:
        """
        Add a tool result to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            content: Tool result content
            call_id: ID of the tool call this is responding to
            is_error: Whether this result represents an error
        """
        message = {
            "role": "tool",
            "content": str(content),
            "tool_call_id": call_id
        }
        
        if name:  # Some models don't require name in tool responses
            message["name"] = name
            
        if is_error:
            message["is_error"] = True
        
        self.messages.append(message)
    
    def xǁConversationMemoryǁadd_tool_result__mutmut_1(self, name: str, content: str, call_id: str, is_error: bool = True) -> None:
        """
        Add a tool result to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            content: Tool result content
            call_id: ID of the tool call this is responding to
            is_error: Whether this result represents an error
        """
        message = {
            "role": "tool",
            "content": str(content),
            "tool_call_id": call_id
        }
        
        if name:  # Some models don't require name in tool responses
            message["name"] = name
            
        if is_error:
            message["is_error"] = True
        
        self.messages.append(message)
    
    def xǁConversationMemoryǁadd_tool_result__mutmut_2(self, name: str, content: str, call_id: str, is_error: bool = False) -> None:
        """
        Add a tool result to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            content: Tool result content
            call_id: ID of the tool call this is responding to
            is_error: Whether this result represents an error
        """
        message = None
        
        if name:  # Some models don't require name in tool responses
            message["name"] = name
            
        if is_error:
            message["is_error"] = True
        
        self.messages.append(message)
    
    def xǁConversationMemoryǁadd_tool_result__mutmut_3(self, name: str, content: str, call_id: str, is_error: bool = False) -> None:
        """
        Add a tool result to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            content: Tool result content
            call_id: ID of the tool call this is responding to
            is_error: Whether this result represents an error
        """
        message = {
            "XXroleXX": "tool",
            "content": str(content),
            "tool_call_id": call_id
        }
        
        if name:  # Some models don't require name in tool responses
            message["name"] = name
            
        if is_error:
            message["is_error"] = True
        
        self.messages.append(message)
    
    def xǁConversationMemoryǁadd_tool_result__mutmut_4(self, name: str, content: str, call_id: str, is_error: bool = False) -> None:
        """
        Add a tool result to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            content: Tool result content
            call_id: ID of the tool call this is responding to
            is_error: Whether this result represents an error
        """
        message = {
            "ROLE": "tool",
            "content": str(content),
            "tool_call_id": call_id
        }
        
        if name:  # Some models don't require name in tool responses
            message["name"] = name
            
        if is_error:
            message["is_error"] = True
        
        self.messages.append(message)
    
    def xǁConversationMemoryǁadd_tool_result__mutmut_5(self, name: str, content: str, call_id: str, is_error: bool = False) -> None:
        """
        Add a tool result to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            content: Tool result content
            call_id: ID of the tool call this is responding to
            is_error: Whether this result represents an error
        """
        message = {
            "role": "XXtoolXX",
            "content": str(content),
            "tool_call_id": call_id
        }
        
        if name:  # Some models don't require name in tool responses
            message["name"] = name
            
        if is_error:
            message["is_error"] = True
        
        self.messages.append(message)
    
    def xǁConversationMemoryǁadd_tool_result__mutmut_6(self, name: str, content: str, call_id: str, is_error: bool = False) -> None:
        """
        Add a tool result to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            content: Tool result content
            call_id: ID of the tool call this is responding to
            is_error: Whether this result represents an error
        """
        message = {
            "role": "TOOL",
            "content": str(content),
            "tool_call_id": call_id
        }
        
        if name:  # Some models don't require name in tool responses
            message["name"] = name
            
        if is_error:
            message["is_error"] = True
        
        self.messages.append(message)
    
    def xǁConversationMemoryǁadd_tool_result__mutmut_7(self, name: str, content: str, call_id: str, is_error: bool = False) -> None:
        """
        Add a tool result to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            content: Tool result content
            call_id: ID of the tool call this is responding to
            is_error: Whether this result represents an error
        """
        message = {
            "role": "tool",
            "XXcontentXX": str(content),
            "tool_call_id": call_id
        }
        
        if name:  # Some models don't require name in tool responses
            message["name"] = name
            
        if is_error:
            message["is_error"] = True
        
        self.messages.append(message)
    
    def xǁConversationMemoryǁadd_tool_result__mutmut_8(self, name: str, content: str, call_id: str, is_error: bool = False) -> None:
        """
        Add a tool result to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            content: Tool result content
            call_id: ID of the tool call this is responding to
            is_error: Whether this result represents an error
        """
        message = {
            "role": "tool",
            "CONTENT": str(content),
            "tool_call_id": call_id
        }
        
        if name:  # Some models don't require name in tool responses
            message["name"] = name
            
        if is_error:
            message["is_error"] = True
        
        self.messages.append(message)
    
    def xǁConversationMemoryǁadd_tool_result__mutmut_9(self, name: str, content: str, call_id: str, is_error: bool = False) -> None:
        """
        Add a tool result to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            content: Tool result content
            call_id: ID of the tool call this is responding to
            is_error: Whether this result represents an error
        """
        message = {
            "role": "tool",
            "content": str(None),
            "tool_call_id": call_id
        }
        
        if name:  # Some models don't require name in tool responses
            message["name"] = name
            
        if is_error:
            message["is_error"] = True
        
        self.messages.append(message)
    
    def xǁConversationMemoryǁadd_tool_result__mutmut_10(self, name: str, content: str, call_id: str, is_error: bool = False) -> None:
        """
        Add a tool result to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            content: Tool result content
            call_id: ID of the tool call this is responding to
            is_error: Whether this result represents an error
        """
        message = {
            "role": "tool",
            "content": str(content),
            "XXtool_call_idXX": call_id
        }
        
        if name:  # Some models don't require name in tool responses
            message["name"] = name
            
        if is_error:
            message["is_error"] = True
        
        self.messages.append(message)
    
    def xǁConversationMemoryǁadd_tool_result__mutmut_11(self, name: str, content: str, call_id: str, is_error: bool = False) -> None:
        """
        Add a tool result to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            content: Tool result content
            call_id: ID of the tool call this is responding to
            is_error: Whether this result represents an error
        """
        message = {
            "role": "tool",
            "content": str(content),
            "TOOL_CALL_ID": call_id
        }
        
        if name:  # Some models don't require name in tool responses
            message["name"] = name
            
        if is_error:
            message["is_error"] = True
        
        self.messages.append(message)
    
    def xǁConversationMemoryǁadd_tool_result__mutmut_12(self, name: str, content: str, call_id: str, is_error: bool = False) -> None:
        """
        Add a tool result to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            content: Tool result content
            call_id: ID of the tool call this is responding to
            is_error: Whether this result represents an error
        """
        message = {
            "role": "tool",
            "content": str(content),
            "tool_call_id": call_id
        }
        
        if name:  # Some models don't require name in tool responses
            message["name"] = None
            
        if is_error:
            message["is_error"] = True
        
        self.messages.append(message)
    
    def xǁConversationMemoryǁadd_tool_result__mutmut_13(self, name: str, content: str, call_id: str, is_error: bool = False) -> None:
        """
        Add a tool result to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            content: Tool result content
            call_id: ID of the tool call this is responding to
            is_error: Whether this result represents an error
        """
        message = {
            "role": "tool",
            "content": str(content),
            "tool_call_id": call_id
        }
        
        if name:  # Some models don't require name in tool responses
            message["XXnameXX"] = name
            
        if is_error:
            message["is_error"] = True
        
        self.messages.append(message)
    
    def xǁConversationMemoryǁadd_tool_result__mutmut_14(self, name: str, content: str, call_id: str, is_error: bool = False) -> None:
        """
        Add a tool result to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            content: Tool result content
            call_id: ID of the tool call this is responding to
            is_error: Whether this result represents an error
        """
        message = {
            "role": "tool",
            "content": str(content),
            "tool_call_id": call_id
        }
        
        if name:  # Some models don't require name in tool responses
            message["NAME"] = name
            
        if is_error:
            message["is_error"] = True
        
        self.messages.append(message)
    
    def xǁConversationMemoryǁadd_tool_result__mutmut_15(self, name: str, content: str, call_id: str, is_error: bool = False) -> None:
        """
        Add a tool result to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            content: Tool result content
            call_id: ID of the tool call this is responding to
            is_error: Whether this result represents an error
        """
        message = {
            "role": "tool",
            "content": str(content),
            "tool_call_id": call_id
        }
        
        if name:  # Some models don't require name in tool responses
            message["name"] = name
            
        if is_error:
            message["is_error"] = None
        
        self.messages.append(message)
    
    def xǁConversationMemoryǁadd_tool_result__mutmut_16(self, name: str, content: str, call_id: str, is_error: bool = False) -> None:
        """
        Add a tool result to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            content: Tool result content
            call_id: ID of the tool call this is responding to
            is_error: Whether this result represents an error
        """
        message = {
            "role": "tool",
            "content": str(content),
            "tool_call_id": call_id
        }
        
        if name:  # Some models don't require name in tool responses
            message["name"] = name
            
        if is_error:
            message["XXis_errorXX"] = True
        
        self.messages.append(message)
    
    def xǁConversationMemoryǁadd_tool_result__mutmut_17(self, name: str, content: str, call_id: str, is_error: bool = False) -> None:
        """
        Add a tool result to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            content: Tool result content
            call_id: ID of the tool call this is responding to
            is_error: Whether this result represents an error
        """
        message = {
            "role": "tool",
            "content": str(content),
            "tool_call_id": call_id
        }
        
        if name:  # Some models don't require name in tool responses
            message["name"] = name
            
        if is_error:
            message["IS_ERROR"] = True
        
        self.messages.append(message)
    
    def xǁConversationMemoryǁadd_tool_result__mutmut_18(self, name: str, content: str, call_id: str, is_error: bool = False) -> None:
        """
        Add a tool result to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            content: Tool result content
            call_id: ID of the tool call this is responding to
            is_error: Whether this result represents an error
        """
        message = {
            "role": "tool",
            "content": str(content),
            "tool_call_id": call_id
        }
        
        if name:  # Some models don't require name in tool responses
            message["name"] = name
            
        if is_error:
            message["is_error"] = False
        
        self.messages.append(message)
    
    def xǁConversationMemoryǁadd_tool_result__mutmut_19(self, name: str, content: str, call_id: str, is_error: bool = False) -> None:
        """
        Add a tool result to the conversation (newer OpenAI format).
        
        Args:
            name: Tool name
            content: Tool result content
            call_id: ID of the tool call this is responding to
            is_error: Whether this result represents an error
        """
        message = {
            "role": "tool",
            "content": str(content),
            "tool_call_id": call_id
        }
        
        if name:  # Some models don't require name in tool responses
            message["name"] = name
            
        if is_error:
            message["is_error"] = True
        
        self.messages.append(None)
    
    xǁConversationMemoryǁadd_tool_result__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁConversationMemoryǁadd_tool_result__mutmut_1': xǁConversationMemoryǁadd_tool_result__mutmut_1, 
        'xǁConversationMemoryǁadd_tool_result__mutmut_2': xǁConversationMemoryǁadd_tool_result__mutmut_2, 
        'xǁConversationMemoryǁadd_tool_result__mutmut_3': xǁConversationMemoryǁadd_tool_result__mutmut_3, 
        'xǁConversationMemoryǁadd_tool_result__mutmut_4': xǁConversationMemoryǁadd_tool_result__mutmut_4, 
        'xǁConversationMemoryǁadd_tool_result__mutmut_5': xǁConversationMemoryǁadd_tool_result__mutmut_5, 
        'xǁConversationMemoryǁadd_tool_result__mutmut_6': xǁConversationMemoryǁadd_tool_result__mutmut_6, 
        'xǁConversationMemoryǁadd_tool_result__mutmut_7': xǁConversationMemoryǁadd_tool_result__mutmut_7, 
        'xǁConversationMemoryǁadd_tool_result__mutmut_8': xǁConversationMemoryǁadd_tool_result__mutmut_8, 
        'xǁConversationMemoryǁadd_tool_result__mutmut_9': xǁConversationMemoryǁadd_tool_result__mutmut_9, 
        'xǁConversationMemoryǁadd_tool_result__mutmut_10': xǁConversationMemoryǁadd_tool_result__mutmut_10, 
        'xǁConversationMemoryǁadd_tool_result__mutmut_11': xǁConversationMemoryǁadd_tool_result__mutmut_11, 
        'xǁConversationMemoryǁadd_tool_result__mutmut_12': xǁConversationMemoryǁadd_tool_result__mutmut_12, 
        'xǁConversationMemoryǁadd_tool_result__mutmut_13': xǁConversationMemoryǁadd_tool_result__mutmut_13, 
        'xǁConversationMemoryǁadd_tool_result__mutmut_14': xǁConversationMemoryǁadd_tool_result__mutmut_14, 
        'xǁConversationMemoryǁadd_tool_result__mutmut_15': xǁConversationMemoryǁadd_tool_result__mutmut_15, 
        'xǁConversationMemoryǁadd_tool_result__mutmut_16': xǁConversationMemoryǁadd_tool_result__mutmut_16, 
        'xǁConversationMemoryǁadd_tool_result__mutmut_17': xǁConversationMemoryǁadd_tool_result__mutmut_17, 
        'xǁConversationMemoryǁadd_tool_result__mutmut_18': xǁConversationMemoryǁadd_tool_result__mutmut_18, 
        'xǁConversationMemoryǁadd_tool_result__mutmut_19': xǁConversationMemoryǁadd_tool_result__mutmut_19
    }
    
    def add_tool_result(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁConversationMemoryǁadd_tool_result__mutmut_orig"), object.__getattribute__(self, "xǁConversationMemoryǁadd_tool_result__mutmut_mutants"), args, kwargs, self)
        return result 
    
    add_tool_result.__signature__ = _mutmut_signature(xǁConversationMemoryǁadd_tool_result__mutmut_orig)
    xǁConversationMemoryǁadd_tool_result__mutmut_orig.__name__ = 'xǁConversationMemoryǁadd_tool_result'
    
    def xǁConversationMemoryǁadd_system_message__mutmut_orig(self, content: str) -> None:
        """
        Add a system message to the conversation.
        
        Args:
            content: The message content
        """
        self.messages.append({"role": "system", "content": content})
    
    def xǁConversationMemoryǁadd_system_message__mutmut_1(self, content: str) -> None:
        """
        Add a system message to the conversation.
        
        Args:
            content: The message content
        """
        self.messages.append(None)
    
    def xǁConversationMemoryǁadd_system_message__mutmut_2(self, content: str) -> None:
        """
        Add a system message to the conversation.
        
        Args:
            content: The message content
        """
        self.messages.append({"XXroleXX": "system", "content": content})
    
    def xǁConversationMemoryǁadd_system_message__mutmut_3(self, content: str) -> None:
        """
        Add a system message to the conversation.
        
        Args:
            content: The message content
        """
        self.messages.append({"ROLE": "system", "content": content})
    
    def xǁConversationMemoryǁadd_system_message__mutmut_4(self, content: str) -> None:
        """
        Add a system message to the conversation.
        
        Args:
            content: The message content
        """
        self.messages.append({"role": "XXsystemXX", "content": content})
    
    def xǁConversationMemoryǁadd_system_message__mutmut_5(self, content: str) -> None:
        """
        Add a system message to the conversation.
        
        Args:
            content: The message content
        """
        self.messages.append({"role": "SYSTEM", "content": content})
    
    def xǁConversationMemoryǁadd_system_message__mutmut_6(self, content: str) -> None:
        """
        Add a system message to the conversation.
        
        Args:
            content: The message content
        """
        self.messages.append({"role": "system", "XXcontentXX": content})
    
    def xǁConversationMemoryǁadd_system_message__mutmut_7(self, content: str) -> None:
        """
        Add a system message to the conversation.
        
        Args:
            content: The message content
        """
        self.messages.append({"role": "system", "CONTENT": content})
    
    xǁConversationMemoryǁadd_system_message__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁConversationMemoryǁadd_system_message__mutmut_1': xǁConversationMemoryǁadd_system_message__mutmut_1, 
        'xǁConversationMemoryǁadd_system_message__mutmut_2': xǁConversationMemoryǁadd_system_message__mutmut_2, 
        'xǁConversationMemoryǁadd_system_message__mutmut_3': xǁConversationMemoryǁadd_system_message__mutmut_3, 
        'xǁConversationMemoryǁadd_system_message__mutmut_4': xǁConversationMemoryǁadd_system_message__mutmut_4, 
        'xǁConversationMemoryǁadd_system_message__mutmut_5': xǁConversationMemoryǁadd_system_message__mutmut_5, 
        'xǁConversationMemoryǁadd_system_message__mutmut_6': xǁConversationMemoryǁadd_system_message__mutmut_6, 
        'xǁConversationMemoryǁadd_system_message__mutmut_7': xǁConversationMemoryǁadd_system_message__mutmut_7
    }
    
    def add_system_message(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁConversationMemoryǁadd_system_message__mutmut_orig"), object.__getattribute__(self, "xǁConversationMemoryǁadd_system_message__mutmut_mutants"), args, kwargs, self)
        return result 
    
    add_system_message.__signature__ = _mutmut_signature(xǁConversationMemoryǁadd_system_message__mutmut_orig)
    xǁConversationMemoryǁadd_system_message__mutmut_orig.__name__ = 'xǁConversationMemoryǁadd_system_message'
    
    def xǁConversationMemoryǁget_messages__mutmut_orig(self, count: Optional[int] = None) -> List[Dict]:
        """
        Get messages in the conversation, optionally limited to the last 'count' messages.
        
        Args:
            count: Optional number of recent messages to return
            
        Returns:
            List of message dictionaries
        """
        # Filter out internal fields that shouldn't be sent to the model
        filtered_messages = []
        messages_to_process = self.messages
        
        # If count is specified, limit to the last 'count' messages
        if count is not None:
            messages_to_process = self.messages[-count:]
        
        for message in messages_to_process:
            filtered_message = message.copy()
            
            # Remove fields that aren't part of the standard message format
            if "args" in filtered_message:
                del filtered_message["args"]
            if "function_call_id" in filtered_message:
                del filtered_message["function_call_id"]
            if "is_error" in filtered_message:
                del filtered_message["is_error"]
                
            filtered_messages.append(filtered_message)
            
        return filtered_messages
    
    def xǁConversationMemoryǁget_messages__mutmut_1(self, count: Optional[int] = None) -> List[Dict]:
        """
        Get messages in the conversation, optionally limited to the last 'count' messages.
        
        Args:
            count: Optional number of recent messages to return
            
        Returns:
            List of message dictionaries
        """
        # Filter out internal fields that shouldn't be sent to the model
        filtered_messages = None
        messages_to_process = self.messages
        
        # If count is specified, limit to the last 'count' messages
        if count is not None:
            messages_to_process = self.messages[-count:]
        
        for message in messages_to_process:
            filtered_message = message.copy()
            
            # Remove fields that aren't part of the standard message format
            if "args" in filtered_message:
                del filtered_message["args"]
            if "function_call_id" in filtered_message:
                del filtered_message["function_call_id"]
            if "is_error" in filtered_message:
                del filtered_message["is_error"]
                
            filtered_messages.append(filtered_message)
            
        return filtered_messages
    
    def xǁConversationMemoryǁget_messages__mutmut_2(self, count: Optional[int] = None) -> List[Dict]:
        """
        Get messages in the conversation, optionally limited to the last 'count' messages.
        
        Args:
            count: Optional number of recent messages to return
            
        Returns:
            List of message dictionaries
        """
        # Filter out internal fields that shouldn't be sent to the model
        filtered_messages = []
        messages_to_process = None
        
        # If count is specified, limit to the last 'count' messages
        if count is not None:
            messages_to_process = self.messages[-count:]
        
        for message in messages_to_process:
            filtered_message = message.copy()
            
            # Remove fields that aren't part of the standard message format
            if "args" in filtered_message:
                del filtered_message["args"]
            if "function_call_id" in filtered_message:
                del filtered_message["function_call_id"]
            if "is_error" in filtered_message:
                del filtered_message["is_error"]
                
            filtered_messages.append(filtered_message)
            
        return filtered_messages
    
    def xǁConversationMemoryǁget_messages__mutmut_3(self, count: Optional[int] = None) -> List[Dict]:
        """
        Get messages in the conversation, optionally limited to the last 'count' messages.
        
        Args:
            count: Optional number of recent messages to return
            
        Returns:
            List of message dictionaries
        """
        # Filter out internal fields that shouldn't be sent to the model
        filtered_messages = []
        messages_to_process = self.messages
        
        # If count is specified, limit to the last 'count' messages
        if count is None:
            messages_to_process = self.messages[-count:]
        
        for message in messages_to_process:
            filtered_message = message.copy()
            
            # Remove fields that aren't part of the standard message format
            if "args" in filtered_message:
                del filtered_message["args"]
            if "function_call_id" in filtered_message:
                del filtered_message["function_call_id"]
            if "is_error" in filtered_message:
                del filtered_message["is_error"]
                
            filtered_messages.append(filtered_message)
            
        return filtered_messages
    
    def xǁConversationMemoryǁget_messages__mutmut_4(self, count: Optional[int] = None) -> List[Dict]:
        """
        Get messages in the conversation, optionally limited to the last 'count' messages.
        
        Args:
            count: Optional number of recent messages to return
            
        Returns:
            List of message dictionaries
        """
        # Filter out internal fields that shouldn't be sent to the model
        filtered_messages = []
        messages_to_process = self.messages
        
        # If count is specified, limit to the last 'count' messages
        if count is not None:
            messages_to_process = None
        
        for message in messages_to_process:
            filtered_message = message.copy()
            
            # Remove fields that aren't part of the standard message format
            if "args" in filtered_message:
                del filtered_message["args"]
            if "function_call_id" in filtered_message:
                del filtered_message["function_call_id"]
            if "is_error" in filtered_message:
                del filtered_message["is_error"]
                
            filtered_messages.append(filtered_message)
            
        return filtered_messages
    
    def xǁConversationMemoryǁget_messages__mutmut_5(self, count: Optional[int] = None) -> List[Dict]:
        """
        Get messages in the conversation, optionally limited to the last 'count' messages.
        
        Args:
            count: Optional number of recent messages to return
            
        Returns:
            List of message dictionaries
        """
        # Filter out internal fields that shouldn't be sent to the model
        filtered_messages = []
        messages_to_process = self.messages
        
        # If count is specified, limit to the last 'count' messages
        if count is not None:
            messages_to_process = self.messages[+count:]
        
        for message in messages_to_process:
            filtered_message = message.copy()
            
            # Remove fields that aren't part of the standard message format
            if "args" in filtered_message:
                del filtered_message["args"]
            if "function_call_id" in filtered_message:
                del filtered_message["function_call_id"]
            if "is_error" in filtered_message:
                del filtered_message["is_error"]
                
            filtered_messages.append(filtered_message)
            
        return filtered_messages
    
    def xǁConversationMemoryǁget_messages__mutmut_6(self, count: Optional[int] = None) -> List[Dict]:
        """
        Get messages in the conversation, optionally limited to the last 'count' messages.
        
        Args:
            count: Optional number of recent messages to return
            
        Returns:
            List of message dictionaries
        """
        # Filter out internal fields that shouldn't be sent to the model
        filtered_messages = []
        messages_to_process = self.messages
        
        # If count is specified, limit to the last 'count' messages
        if count is not None:
            messages_to_process = self.messages[-count:]
        
        for message in messages_to_process:
            filtered_message = None
            
            # Remove fields that aren't part of the standard message format
            if "args" in filtered_message:
                del filtered_message["args"]
            if "function_call_id" in filtered_message:
                del filtered_message["function_call_id"]
            if "is_error" in filtered_message:
                del filtered_message["is_error"]
                
            filtered_messages.append(filtered_message)
            
        return filtered_messages
    
    def xǁConversationMemoryǁget_messages__mutmut_7(self, count: Optional[int] = None) -> List[Dict]:
        """
        Get messages in the conversation, optionally limited to the last 'count' messages.
        
        Args:
            count: Optional number of recent messages to return
            
        Returns:
            List of message dictionaries
        """
        # Filter out internal fields that shouldn't be sent to the model
        filtered_messages = []
        messages_to_process = self.messages
        
        # If count is specified, limit to the last 'count' messages
        if count is not None:
            messages_to_process = self.messages[-count:]
        
        for message in messages_to_process:
            filtered_message = message.copy()
            
            # Remove fields that aren't part of the standard message format
            if "XXargsXX" in filtered_message:
                del filtered_message["args"]
            if "function_call_id" in filtered_message:
                del filtered_message["function_call_id"]
            if "is_error" in filtered_message:
                del filtered_message["is_error"]
                
            filtered_messages.append(filtered_message)
            
        return filtered_messages
    
    def xǁConversationMemoryǁget_messages__mutmut_8(self, count: Optional[int] = None) -> List[Dict]:
        """
        Get messages in the conversation, optionally limited to the last 'count' messages.
        
        Args:
            count: Optional number of recent messages to return
            
        Returns:
            List of message dictionaries
        """
        # Filter out internal fields that shouldn't be sent to the model
        filtered_messages = []
        messages_to_process = self.messages
        
        # If count is specified, limit to the last 'count' messages
        if count is not None:
            messages_to_process = self.messages[-count:]
        
        for message in messages_to_process:
            filtered_message = message.copy()
            
            # Remove fields that aren't part of the standard message format
            if "ARGS" in filtered_message:
                del filtered_message["args"]
            if "function_call_id" in filtered_message:
                del filtered_message["function_call_id"]
            if "is_error" in filtered_message:
                del filtered_message["is_error"]
                
            filtered_messages.append(filtered_message)
            
        return filtered_messages
    
    def xǁConversationMemoryǁget_messages__mutmut_9(self, count: Optional[int] = None) -> List[Dict]:
        """
        Get messages in the conversation, optionally limited to the last 'count' messages.
        
        Args:
            count: Optional number of recent messages to return
            
        Returns:
            List of message dictionaries
        """
        # Filter out internal fields that shouldn't be sent to the model
        filtered_messages = []
        messages_to_process = self.messages
        
        # If count is specified, limit to the last 'count' messages
        if count is not None:
            messages_to_process = self.messages[-count:]
        
        for message in messages_to_process:
            filtered_message = message.copy()
            
            # Remove fields that aren't part of the standard message format
            if "args" not in filtered_message:
                del filtered_message["args"]
            if "function_call_id" in filtered_message:
                del filtered_message["function_call_id"]
            if "is_error" in filtered_message:
                del filtered_message["is_error"]
                
            filtered_messages.append(filtered_message)
            
        return filtered_messages
    
    def xǁConversationMemoryǁget_messages__mutmut_10(self, count: Optional[int] = None) -> List[Dict]:
        """
        Get messages in the conversation, optionally limited to the last 'count' messages.
        
        Args:
            count: Optional number of recent messages to return
            
        Returns:
            List of message dictionaries
        """
        # Filter out internal fields that shouldn't be sent to the model
        filtered_messages = []
        messages_to_process = self.messages
        
        # If count is specified, limit to the last 'count' messages
        if count is not None:
            messages_to_process = self.messages[-count:]
        
        for message in messages_to_process:
            filtered_message = message.copy()
            
            # Remove fields that aren't part of the standard message format
            if "args" in filtered_message:
                del filtered_message["XXargsXX"]
            if "function_call_id" in filtered_message:
                del filtered_message["function_call_id"]
            if "is_error" in filtered_message:
                del filtered_message["is_error"]
                
            filtered_messages.append(filtered_message)
            
        return filtered_messages
    
    def xǁConversationMemoryǁget_messages__mutmut_11(self, count: Optional[int] = None) -> List[Dict]:
        """
        Get messages in the conversation, optionally limited to the last 'count' messages.
        
        Args:
            count: Optional number of recent messages to return
            
        Returns:
            List of message dictionaries
        """
        # Filter out internal fields that shouldn't be sent to the model
        filtered_messages = []
        messages_to_process = self.messages
        
        # If count is specified, limit to the last 'count' messages
        if count is not None:
            messages_to_process = self.messages[-count:]
        
        for message in messages_to_process:
            filtered_message = message.copy()
            
            # Remove fields that aren't part of the standard message format
            if "args" in filtered_message:
                del filtered_message["ARGS"]
            if "function_call_id" in filtered_message:
                del filtered_message["function_call_id"]
            if "is_error" in filtered_message:
                del filtered_message["is_error"]
                
            filtered_messages.append(filtered_message)
            
        return filtered_messages
    
    def xǁConversationMemoryǁget_messages__mutmut_12(self, count: Optional[int] = None) -> List[Dict]:
        """
        Get messages in the conversation, optionally limited to the last 'count' messages.
        
        Args:
            count: Optional number of recent messages to return
            
        Returns:
            List of message dictionaries
        """
        # Filter out internal fields that shouldn't be sent to the model
        filtered_messages = []
        messages_to_process = self.messages
        
        # If count is specified, limit to the last 'count' messages
        if count is not None:
            messages_to_process = self.messages[-count:]
        
        for message in messages_to_process:
            filtered_message = message.copy()
            
            # Remove fields that aren't part of the standard message format
            if "args" in filtered_message:
                del filtered_message["args"]
            if "XXfunction_call_idXX" in filtered_message:
                del filtered_message["function_call_id"]
            if "is_error" in filtered_message:
                del filtered_message["is_error"]
                
            filtered_messages.append(filtered_message)
            
        return filtered_messages
    
    def xǁConversationMemoryǁget_messages__mutmut_13(self, count: Optional[int] = None) -> List[Dict]:
        """
        Get messages in the conversation, optionally limited to the last 'count' messages.
        
        Args:
            count: Optional number of recent messages to return
            
        Returns:
            List of message dictionaries
        """
        # Filter out internal fields that shouldn't be sent to the model
        filtered_messages = []
        messages_to_process = self.messages
        
        # If count is specified, limit to the last 'count' messages
        if count is not None:
            messages_to_process = self.messages[-count:]
        
        for message in messages_to_process:
            filtered_message = message.copy()
            
            # Remove fields that aren't part of the standard message format
            if "args" in filtered_message:
                del filtered_message["args"]
            if "FUNCTION_CALL_ID" in filtered_message:
                del filtered_message["function_call_id"]
            if "is_error" in filtered_message:
                del filtered_message["is_error"]
                
            filtered_messages.append(filtered_message)
            
        return filtered_messages
    
    def xǁConversationMemoryǁget_messages__mutmut_14(self, count: Optional[int] = None) -> List[Dict]:
        """
        Get messages in the conversation, optionally limited to the last 'count' messages.
        
        Args:
            count: Optional number of recent messages to return
            
        Returns:
            List of message dictionaries
        """
        # Filter out internal fields that shouldn't be sent to the model
        filtered_messages = []
        messages_to_process = self.messages
        
        # If count is specified, limit to the last 'count' messages
        if count is not None:
            messages_to_process = self.messages[-count:]
        
        for message in messages_to_process:
            filtered_message = message.copy()
            
            # Remove fields that aren't part of the standard message format
            if "args" in filtered_message:
                del filtered_message["args"]
            if "function_call_id" not in filtered_message:
                del filtered_message["function_call_id"]
            if "is_error" in filtered_message:
                del filtered_message["is_error"]
                
            filtered_messages.append(filtered_message)
            
        return filtered_messages
    
    def xǁConversationMemoryǁget_messages__mutmut_15(self, count: Optional[int] = None) -> List[Dict]:
        """
        Get messages in the conversation, optionally limited to the last 'count' messages.
        
        Args:
            count: Optional number of recent messages to return
            
        Returns:
            List of message dictionaries
        """
        # Filter out internal fields that shouldn't be sent to the model
        filtered_messages = []
        messages_to_process = self.messages
        
        # If count is specified, limit to the last 'count' messages
        if count is not None:
            messages_to_process = self.messages[-count:]
        
        for message in messages_to_process:
            filtered_message = message.copy()
            
            # Remove fields that aren't part of the standard message format
            if "args" in filtered_message:
                del filtered_message["args"]
            if "function_call_id" in filtered_message:
                del filtered_message["XXfunction_call_idXX"]
            if "is_error" in filtered_message:
                del filtered_message["is_error"]
                
            filtered_messages.append(filtered_message)
            
        return filtered_messages
    
    def xǁConversationMemoryǁget_messages__mutmut_16(self, count: Optional[int] = None) -> List[Dict]:
        """
        Get messages in the conversation, optionally limited to the last 'count' messages.
        
        Args:
            count: Optional number of recent messages to return
            
        Returns:
            List of message dictionaries
        """
        # Filter out internal fields that shouldn't be sent to the model
        filtered_messages = []
        messages_to_process = self.messages
        
        # If count is specified, limit to the last 'count' messages
        if count is not None:
            messages_to_process = self.messages[-count:]
        
        for message in messages_to_process:
            filtered_message = message.copy()
            
            # Remove fields that aren't part of the standard message format
            if "args" in filtered_message:
                del filtered_message["args"]
            if "function_call_id" in filtered_message:
                del filtered_message["FUNCTION_CALL_ID"]
            if "is_error" in filtered_message:
                del filtered_message["is_error"]
                
            filtered_messages.append(filtered_message)
            
        return filtered_messages
    
    def xǁConversationMemoryǁget_messages__mutmut_17(self, count: Optional[int] = None) -> List[Dict]:
        """
        Get messages in the conversation, optionally limited to the last 'count' messages.
        
        Args:
            count: Optional number of recent messages to return
            
        Returns:
            List of message dictionaries
        """
        # Filter out internal fields that shouldn't be sent to the model
        filtered_messages = []
        messages_to_process = self.messages
        
        # If count is specified, limit to the last 'count' messages
        if count is not None:
            messages_to_process = self.messages[-count:]
        
        for message in messages_to_process:
            filtered_message = message.copy()
            
            # Remove fields that aren't part of the standard message format
            if "args" in filtered_message:
                del filtered_message["args"]
            if "function_call_id" in filtered_message:
                del filtered_message["function_call_id"]
            if "XXis_errorXX" in filtered_message:
                del filtered_message["is_error"]
                
            filtered_messages.append(filtered_message)
            
        return filtered_messages
    
    def xǁConversationMemoryǁget_messages__mutmut_18(self, count: Optional[int] = None) -> List[Dict]:
        """
        Get messages in the conversation, optionally limited to the last 'count' messages.
        
        Args:
            count: Optional number of recent messages to return
            
        Returns:
            List of message dictionaries
        """
        # Filter out internal fields that shouldn't be sent to the model
        filtered_messages = []
        messages_to_process = self.messages
        
        # If count is specified, limit to the last 'count' messages
        if count is not None:
            messages_to_process = self.messages[-count:]
        
        for message in messages_to_process:
            filtered_message = message.copy()
            
            # Remove fields that aren't part of the standard message format
            if "args" in filtered_message:
                del filtered_message["args"]
            if "function_call_id" in filtered_message:
                del filtered_message["function_call_id"]
            if "IS_ERROR" in filtered_message:
                del filtered_message["is_error"]
                
            filtered_messages.append(filtered_message)
            
        return filtered_messages
    
    def xǁConversationMemoryǁget_messages__mutmut_19(self, count: Optional[int] = None) -> List[Dict]:
        """
        Get messages in the conversation, optionally limited to the last 'count' messages.
        
        Args:
            count: Optional number of recent messages to return
            
        Returns:
            List of message dictionaries
        """
        # Filter out internal fields that shouldn't be sent to the model
        filtered_messages = []
        messages_to_process = self.messages
        
        # If count is specified, limit to the last 'count' messages
        if count is not None:
            messages_to_process = self.messages[-count:]
        
        for message in messages_to_process:
            filtered_message = message.copy()
            
            # Remove fields that aren't part of the standard message format
            if "args" in filtered_message:
                del filtered_message["args"]
            if "function_call_id" in filtered_message:
                del filtered_message["function_call_id"]
            if "is_error" not in filtered_message:
                del filtered_message["is_error"]
                
            filtered_messages.append(filtered_message)
            
        return filtered_messages
    
    def xǁConversationMemoryǁget_messages__mutmut_20(self, count: Optional[int] = None) -> List[Dict]:
        """
        Get messages in the conversation, optionally limited to the last 'count' messages.
        
        Args:
            count: Optional number of recent messages to return
            
        Returns:
            List of message dictionaries
        """
        # Filter out internal fields that shouldn't be sent to the model
        filtered_messages = []
        messages_to_process = self.messages
        
        # If count is specified, limit to the last 'count' messages
        if count is not None:
            messages_to_process = self.messages[-count:]
        
        for message in messages_to_process:
            filtered_message = message.copy()
            
            # Remove fields that aren't part of the standard message format
            if "args" in filtered_message:
                del filtered_message["args"]
            if "function_call_id" in filtered_message:
                del filtered_message["function_call_id"]
            if "is_error" in filtered_message:
                del filtered_message["XXis_errorXX"]
                
            filtered_messages.append(filtered_message)
            
        return filtered_messages
    
    def xǁConversationMemoryǁget_messages__mutmut_21(self, count: Optional[int] = None) -> List[Dict]:
        """
        Get messages in the conversation, optionally limited to the last 'count' messages.
        
        Args:
            count: Optional number of recent messages to return
            
        Returns:
            List of message dictionaries
        """
        # Filter out internal fields that shouldn't be sent to the model
        filtered_messages = []
        messages_to_process = self.messages
        
        # If count is specified, limit to the last 'count' messages
        if count is not None:
            messages_to_process = self.messages[-count:]
        
        for message in messages_to_process:
            filtered_message = message.copy()
            
            # Remove fields that aren't part of the standard message format
            if "args" in filtered_message:
                del filtered_message["args"]
            if "function_call_id" in filtered_message:
                del filtered_message["function_call_id"]
            if "is_error" in filtered_message:
                del filtered_message["IS_ERROR"]
                
            filtered_messages.append(filtered_message)
            
        return filtered_messages
    
    def xǁConversationMemoryǁget_messages__mutmut_22(self, count: Optional[int] = None) -> List[Dict]:
        """
        Get messages in the conversation, optionally limited to the last 'count' messages.
        
        Args:
            count: Optional number of recent messages to return
            
        Returns:
            List of message dictionaries
        """
        # Filter out internal fields that shouldn't be sent to the model
        filtered_messages = []
        messages_to_process = self.messages
        
        # If count is specified, limit to the last 'count' messages
        if count is not None:
            messages_to_process = self.messages[-count:]
        
        for message in messages_to_process:
            filtered_message = message.copy()
            
            # Remove fields that aren't part of the standard message format
            if "args" in filtered_message:
                del filtered_message["args"]
            if "function_call_id" in filtered_message:
                del filtered_message["function_call_id"]
            if "is_error" in filtered_message:
                del filtered_message["is_error"]
                
            filtered_messages.append(None)
            
        return filtered_messages
    
    xǁConversationMemoryǁget_messages__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁConversationMemoryǁget_messages__mutmut_1': xǁConversationMemoryǁget_messages__mutmut_1, 
        'xǁConversationMemoryǁget_messages__mutmut_2': xǁConversationMemoryǁget_messages__mutmut_2, 
        'xǁConversationMemoryǁget_messages__mutmut_3': xǁConversationMemoryǁget_messages__mutmut_3, 
        'xǁConversationMemoryǁget_messages__mutmut_4': xǁConversationMemoryǁget_messages__mutmut_4, 
        'xǁConversationMemoryǁget_messages__mutmut_5': xǁConversationMemoryǁget_messages__mutmut_5, 
        'xǁConversationMemoryǁget_messages__mutmut_6': xǁConversationMemoryǁget_messages__mutmut_6, 
        'xǁConversationMemoryǁget_messages__mutmut_7': xǁConversationMemoryǁget_messages__mutmut_7, 
        'xǁConversationMemoryǁget_messages__mutmut_8': xǁConversationMemoryǁget_messages__mutmut_8, 
        'xǁConversationMemoryǁget_messages__mutmut_9': xǁConversationMemoryǁget_messages__mutmut_9, 
        'xǁConversationMemoryǁget_messages__mutmut_10': xǁConversationMemoryǁget_messages__mutmut_10, 
        'xǁConversationMemoryǁget_messages__mutmut_11': xǁConversationMemoryǁget_messages__mutmut_11, 
        'xǁConversationMemoryǁget_messages__mutmut_12': xǁConversationMemoryǁget_messages__mutmut_12, 
        'xǁConversationMemoryǁget_messages__mutmut_13': xǁConversationMemoryǁget_messages__mutmut_13, 
        'xǁConversationMemoryǁget_messages__mutmut_14': xǁConversationMemoryǁget_messages__mutmut_14, 
        'xǁConversationMemoryǁget_messages__mutmut_15': xǁConversationMemoryǁget_messages__mutmut_15, 
        'xǁConversationMemoryǁget_messages__mutmut_16': xǁConversationMemoryǁget_messages__mutmut_16, 
        'xǁConversationMemoryǁget_messages__mutmut_17': xǁConversationMemoryǁget_messages__mutmut_17, 
        'xǁConversationMemoryǁget_messages__mutmut_18': xǁConversationMemoryǁget_messages__mutmut_18, 
        'xǁConversationMemoryǁget_messages__mutmut_19': xǁConversationMemoryǁget_messages__mutmut_19, 
        'xǁConversationMemoryǁget_messages__mutmut_20': xǁConversationMemoryǁget_messages__mutmut_20, 
        'xǁConversationMemoryǁget_messages__mutmut_21': xǁConversationMemoryǁget_messages__mutmut_21, 
        'xǁConversationMemoryǁget_messages__mutmut_22': xǁConversationMemoryǁget_messages__mutmut_22
    }
    
    def get_messages(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁConversationMemoryǁget_messages__mutmut_orig"), object.__getattribute__(self, "xǁConversationMemoryǁget_messages__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_messages.__signature__ = _mutmut_signature(xǁConversationMemoryǁget_messages__mutmut_orig)
    xǁConversationMemoryǁget_messages__mutmut_orig.__name__ = 'xǁConversationMemoryǁget_messages'
    
    def xǁConversationMemoryǁhas_function_been_called__mutmut_orig(self, function_name: str, args: Dict[str, Any]) -> bool:
        """
        Check if a function has been called with specific arguments.
        
        Args:
            function_name: Name of the function
            args: Function arguments to check for
            
        Returns:
            bool: Whether the function has been called with these arguments
        """
        if function_name not in self.function_calls:
            return False
            
        for call in self.function_calls[function_name]:
            if call.get("args") == args:
                return True
                
        return False
    
    def xǁConversationMemoryǁhas_function_been_called__mutmut_1(self, function_name: str, args: Dict[str, Any]) -> bool:
        """
        Check if a function has been called with specific arguments.
        
        Args:
            function_name: Name of the function
            args: Function arguments to check for
            
        Returns:
            bool: Whether the function has been called with these arguments
        """
        if function_name in self.function_calls:
            return False
            
        for call in self.function_calls[function_name]:
            if call.get("args") == args:
                return True
                
        return False
    
    def xǁConversationMemoryǁhas_function_been_called__mutmut_2(self, function_name: str, args: Dict[str, Any]) -> bool:
        """
        Check if a function has been called with specific arguments.
        
        Args:
            function_name: Name of the function
            args: Function arguments to check for
            
        Returns:
            bool: Whether the function has been called with these arguments
        """
        if function_name not in self.function_calls:
            return True
            
        for call in self.function_calls[function_name]:
            if call.get("args") == args:
                return True
                
        return False
    
    def xǁConversationMemoryǁhas_function_been_called__mutmut_3(self, function_name: str, args: Dict[str, Any]) -> bool:
        """
        Check if a function has been called with specific arguments.
        
        Args:
            function_name: Name of the function
            args: Function arguments to check for
            
        Returns:
            bool: Whether the function has been called with these arguments
        """
        if function_name not in self.function_calls:
            return False
            
        for call in self.function_calls[function_name]:
            if call.get(None) == args:
                return True
                
        return False
    
    def xǁConversationMemoryǁhas_function_been_called__mutmut_4(self, function_name: str, args: Dict[str, Any]) -> bool:
        """
        Check if a function has been called with specific arguments.
        
        Args:
            function_name: Name of the function
            args: Function arguments to check for
            
        Returns:
            bool: Whether the function has been called with these arguments
        """
        if function_name not in self.function_calls:
            return False
            
        for call in self.function_calls[function_name]:
            if call.get("XXargsXX") == args:
                return True
                
        return False
    
    def xǁConversationMemoryǁhas_function_been_called__mutmut_5(self, function_name: str, args: Dict[str, Any]) -> bool:
        """
        Check if a function has been called with specific arguments.
        
        Args:
            function_name: Name of the function
            args: Function arguments to check for
            
        Returns:
            bool: Whether the function has been called with these arguments
        """
        if function_name not in self.function_calls:
            return False
            
        for call in self.function_calls[function_name]:
            if call.get("ARGS") == args:
                return True
                
        return False
    
    def xǁConversationMemoryǁhas_function_been_called__mutmut_6(self, function_name: str, args: Dict[str, Any]) -> bool:
        """
        Check if a function has been called with specific arguments.
        
        Args:
            function_name: Name of the function
            args: Function arguments to check for
            
        Returns:
            bool: Whether the function has been called with these arguments
        """
        if function_name not in self.function_calls:
            return False
            
        for call in self.function_calls[function_name]:
            if call.get("args") != args:
                return True
                
        return False
    
    def xǁConversationMemoryǁhas_function_been_called__mutmut_7(self, function_name: str, args: Dict[str, Any]) -> bool:
        """
        Check if a function has been called with specific arguments.
        
        Args:
            function_name: Name of the function
            args: Function arguments to check for
            
        Returns:
            bool: Whether the function has been called with these arguments
        """
        if function_name not in self.function_calls:
            return False
            
        for call in self.function_calls[function_name]:
            if call.get("args") == args:
                return False
                
        return False
    
    def xǁConversationMemoryǁhas_function_been_called__mutmut_8(self, function_name: str, args: Dict[str, Any]) -> bool:
        """
        Check if a function has been called with specific arguments.
        
        Args:
            function_name: Name of the function
            args: Function arguments to check for
            
        Returns:
            bool: Whether the function has been called with these arguments
        """
        if function_name not in self.function_calls:
            return False
            
        for call in self.function_calls[function_name]:
            if call.get("args") == args:
                return True
                
        return True
    
    xǁConversationMemoryǁhas_function_been_called__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁConversationMemoryǁhas_function_been_called__mutmut_1': xǁConversationMemoryǁhas_function_been_called__mutmut_1, 
        'xǁConversationMemoryǁhas_function_been_called__mutmut_2': xǁConversationMemoryǁhas_function_been_called__mutmut_2, 
        'xǁConversationMemoryǁhas_function_been_called__mutmut_3': xǁConversationMemoryǁhas_function_been_called__mutmut_3, 
        'xǁConversationMemoryǁhas_function_been_called__mutmut_4': xǁConversationMemoryǁhas_function_been_called__mutmut_4, 
        'xǁConversationMemoryǁhas_function_been_called__mutmut_5': xǁConversationMemoryǁhas_function_been_called__mutmut_5, 
        'xǁConversationMemoryǁhas_function_been_called__mutmut_6': xǁConversationMemoryǁhas_function_been_called__mutmut_6, 
        'xǁConversationMemoryǁhas_function_been_called__mutmut_7': xǁConversationMemoryǁhas_function_been_called__mutmut_7, 
        'xǁConversationMemoryǁhas_function_been_called__mutmut_8': xǁConversationMemoryǁhas_function_been_called__mutmut_8
    }
    
    def has_function_been_called(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁConversationMemoryǁhas_function_been_called__mutmut_orig"), object.__getattribute__(self, "xǁConversationMemoryǁhas_function_been_called__mutmut_mutants"), args, kwargs, self)
        return result 
    
    has_function_been_called.__signature__ = _mutmut_signature(xǁConversationMemoryǁhas_function_been_called__mutmut_orig)
    xǁConversationMemoryǁhas_function_been_called__mutmut_orig.__name__ = 'xǁConversationMemoryǁhas_function_been_called'
    
    def xǁConversationMemoryǁreset__mutmut_orig(self) -> None:
        """Reset the conversation to only include the system prompt."""
        self.messages = [{"role": "system", "content": self.system_prompt}]
        self.function_calls = {}
        self.last_function_call = None
    
    def xǁConversationMemoryǁreset__mutmut_1(self) -> None:
        """Reset the conversation to only include the system prompt."""
        self.messages = None
        self.function_calls = {}
        self.last_function_call = None
    
    def xǁConversationMemoryǁreset__mutmut_2(self) -> None:
        """Reset the conversation to only include the system prompt."""
        self.messages = [{"XXroleXX": "system", "content": self.system_prompt}]
        self.function_calls = {}
        self.last_function_call = None
    
    def xǁConversationMemoryǁreset__mutmut_3(self) -> None:
        """Reset the conversation to only include the system prompt."""
        self.messages = [{"ROLE": "system", "content": self.system_prompt}]
        self.function_calls = {}
        self.last_function_call = None
    
    def xǁConversationMemoryǁreset__mutmut_4(self) -> None:
        """Reset the conversation to only include the system prompt."""
        self.messages = [{"role": "XXsystemXX", "content": self.system_prompt}]
        self.function_calls = {}
        self.last_function_call = None
    
    def xǁConversationMemoryǁreset__mutmut_5(self) -> None:
        """Reset the conversation to only include the system prompt."""
        self.messages = [{"role": "SYSTEM", "content": self.system_prompt}]
        self.function_calls = {}
        self.last_function_call = None
    
    def xǁConversationMemoryǁreset__mutmut_6(self) -> None:
        """Reset the conversation to only include the system prompt."""
        self.messages = [{"role": "system", "XXcontentXX": self.system_prompt}]
        self.function_calls = {}
        self.last_function_call = None
    
    def xǁConversationMemoryǁreset__mutmut_7(self) -> None:
        """Reset the conversation to only include the system prompt."""
        self.messages = [{"role": "system", "CONTENT": self.system_prompt}]
        self.function_calls = {}
        self.last_function_call = None
    
    def xǁConversationMemoryǁreset__mutmut_8(self) -> None:
        """Reset the conversation to only include the system prompt."""
        self.messages = [{"role": "system", "content": self.system_prompt}]
        self.function_calls = None
        self.last_function_call = None
    
    def xǁConversationMemoryǁreset__mutmut_9(self) -> None:
        """Reset the conversation to only include the system prompt."""
        self.messages = [{"role": "system", "content": self.system_prompt}]
        self.function_calls = {}
        self.last_function_call = ""
    
    xǁConversationMemoryǁreset__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁConversationMemoryǁreset__mutmut_1': xǁConversationMemoryǁreset__mutmut_1, 
        'xǁConversationMemoryǁreset__mutmut_2': xǁConversationMemoryǁreset__mutmut_2, 
        'xǁConversationMemoryǁreset__mutmut_3': xǁConversationMemoryǁreset__mutmut_3, 
        'xǁConversationMemoryǁreset__mutmut_4': xǁConversationMemoryǁreset__mutmut_4, 
        'xǁConversationMemoryǁreset__mutmut_5': xǁConversationMemoryǁreset__mutmut_5, 
        'xǁConversationMemoryǁreset__mutmut_6': xǁConversationMemoryǁreset__mutmut_6, 
        'xǁConversationMemoryǁreset__mutmut_7': xǁConversationMemoryǁreset__mutmut_7, 
        'xǁConversationMemoryǁreset__mutmut_8': xǁConversationMemoryǁreset__mutmut_8, 
        'xǁConversationMemoryǁreset__mutmut_9': xǁConversationMemoryǁreset__mutmut_9
    }
    
    def reset(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁConversationMemoryǁreset__mutmut_orig"), object.__getattribute__(self, "xǁConversationMemoryǁreset__mutmut_mutants"), args, kwargs, self)
        return result 
    
    reset.__signature__ = _mutmut_signature(xǁConversationMemoryǁreset__mutmut_orig)
    xǁConversationMemoryǁreset__mutmut_orig.__name__ = 'xǁConversationMemoryǁreset'
    
    def xǁConversationMemoryǁupdate_system_prompt__mutmut_orig(self, system_prompt: str) -> None:
        """
        Update the system prompt.
        
        Args:
            system_prompt: The new system prompt
        """
        self.system_prompt = system_prompt
        # Update the first message if it's a system message
        if self.messages and self.messages[0]["role"] == "system":
            self.messages[0]["content"] = system_prompt
        else:
            # Insert at the beginning if there's no system message
            self.messages.insert(0, {"role": "system", "content": system_prompt})
    
    def xǁConversationMemoryǁupdate_system_prompt__mutmut_1(self, system_prompt: str) -> None:
        """
        Update the system prompt.
        
        Args:
            system_prompt: The new system prompt
        """
        self.system_prompt = None
        # Update the first message if it's a system message
        if self.messages and self.messages[0]["role"] == "system":
            self.messages[0]["content"] = system_prompt
        else:
            # Insert at the beginning if there's no system message
            self.messages.insert(0, {"role": "system", "content": system_prompt})
    
    def xǁConversationMemoryǁupdate_system_prompt__mutmut_2(self, system_prompt: str) -> None:
        """
        Update the system prompt.
        
        Args:
            system_prompt: The new system prompt
        """
        self.system_prompt = system_prompt
        # Update the first message if it's a system message
        if self.messages or self.messages[0]["role"] == "system":
            self.messages[0]["content"] = system_prompt
        else:
            # Insert at the beginning if there's no system message
            self.messages.insert(0, {"role": "system", "content": system_prompt})
    
    def xǁConversationMemoryǁupdate_system_prompt__mutmut_3(self, system_prompt: str) -> None:
        """
        Update the system prompt.
        
        Args:
            system_prompt: The new system prompt
        """
        self.system_prompt = system_prompt
        # Update the first message if it's a system message
        if self.messages and self.messages[1]["role"] == "system":
            self.messages[0]["content"] = system_prompt
        else:
            # Insert at the beginning if there's no system message
            self.messages.insert(0, {"role": "system", "content": system_prompt})
    
    def xǁConversationMemoryǁupdate_system_prompt__mutmut_4(self, system_prompt: str) -> None:
        """
        Update the system prompt.
        
        Args:
            system_prompt: The new system prompt
        """
        self.system_prompt = system_prompt
        # Update the first message if it's a system message
        if self.messages and self.messages[0]["XXroleXX"] == "system":
            self.messages[0]["content"] = system_prompt
        else:
            # Insert at the beginning if there's no system message
            self.messages.insert(0, {"role": "system", "content": system_prompt})
    
    def xǁConversationMemoryǁupdate_system_prompt__mutmut_5(self, system_prompt: str) -> None:
        """
        Update the system prompt.
        
        Args:
            system_prompt: The new system prompt
        """
        self.system_prompt = system_prompt
        # Update the first message if it's a system message
        if self.messages and self.messages[0]["ROLE"] == "system":
            self.messages[0]["content"] = system_prompt
        else:
            # Insert at the beginning if there's no system message
            self.messages.insert(0, {"role": "system", "content": system_prompt})
    
    def xǁConversationMemoryǁupdate_system_prompt__mutmut_6(self, system_prompt: str) -> None:
        """
        Update the system prompt.
        
        Args:
            system_prompt: The new system prompt
        """
        self.system_prompt = system_prompt
        # Update the first message if it's a system message
        if self.messages and self.messages[0]["role"] != "system":
            self.messages[0]["content"] = system_prompt
        else:
            # Insert at the beginning if there's no system message
            self.messages.insert(0, {"role": "system", "content": system_prompt})
    
    def xǁConversationMemoryǁupdate_system_prompt__mutmut_7(self, system_prompt: str) -> None:
        """
        Update the system prompt.
        
        Args:
            system_prompt: The new system prompt
        """
        self.system_prompt = system_prompt
        # Update the first message if it's a system message
        if self.messages and self.messages[0]["role"] == "XXsystemXX":
            self.messages[0]["content"] = system_prompt
        else:
            # Insert at the beginning if there's no system message
            self.messages.insert(0, {"role": "system", "content": system_prompt})
    
    def xǁConversationMemoryǁupdate_system_prompt__mutmut_8(self, system_prompt: str) -> None:
        """
        Update the system prompt.
        
        Args:
            system_prompt: The new system prompt
        """
        self.system_prompt = system_prompt
        # Update the first message if it's a system message
        if self.messages and self.messages[0]["role"] == "SYSTEM":
            self.messages[0]["content"] = system_prompt
        else:
            # Insert at the beginning if there's no system message
            self.messages.insert(0, {"role": "system", "content": system_prompt})
    
    def xǁConversationMemoryǁupdate_system_prompt__mutmut_9(self, system_prompt: str) -> None:
        """
        Update the system prompt.
        
        Args:
            system_prompt: The new system prompt
        """
        self.system_prompt = system_prompt
        # Update the first message if it's a system message
        if self.messages and self.messages[0]["role"] == "system":
            self.messages[0]["content"] = None
        else:
            # Insert at the beginning if there's no system message
            self.messages.insert(0, {"role": "system", "content": system_prompt})
    
    def xǁConversationMemoryǁupdate_system_prompt__mutmut_10(self, system_prompt: str) -> None:
        """
        Update the system prompt.
        
        Args:
            system_prompt: The new system prompt
        """
        self.system_prompt = system_prompt
        # Update the first message if it's a system message
        if self.messages and self.messages[0]["role"] == "system":
            self.messages[1]["content"] = system_prompt
        else:
            # Insert at the beginning if there's no system message
            self.messages.insert(0, {"role": "system", "content": system_prompt})
    
    def xǁConversationMemoryǁupdate_system_prompt__mutmut_11(self, system_prompt: str) -> None:
        """
        Update the system prompt.
        
        Args:
            system_prompt: The new system prompt
        """
        self.system_prompt = system_prompt
        # Update the first message if it's a system message
        if self.messages and self.messages[0]["role"] == "system":
            self.messages[0]["XXcontentXX"] = system_prompt
        else:
            # Insert at the beginning if there's no system message
            self.messages.insert(0, {"role": "system", "content": system_prompt})
    
    def xǁConversationMemoryǁupdate_system_prompt__mutmut_12(self, system_prompt: str) -> None:
        """
        Update the system prompt.
        
        Args:
            system_prompt: The new system prompt
        """
        self.system_prompt = system_prompt
        # Update the first message if it's a system message
        if self.messages and self.messages[0]["role"] == "system":
            self.messages[0]["CONTENT"] = system_prompt
        else:
            # Insert at the beginning if there's no system message
            self.messages.insert(0, {"role": "system", "content": system_prompt})
    
    def xǁConversationMemoryǁupdate_system_prompt__mutmut_13(self, system_prompt: str) -> None:
        """
        Update the system prompt.
        
        Args:
            system_prompt: The new system prompt
        """
        self.system_prompt = system_prompt
        # Update the first message if it's a system message
        if self.messages and self.messages[0]["role"] == "system":
            self.messages[0]["content"] = system_prompt
        else:
            # Insert at the beginning if there's no system message
            self.messages.insert(None, {"role": "system", "content": system_prompt})
    
    def xǁConversationMemoryǁupdate_system_prompt__mutmut_14(self, system_prompt: str) -> None:
        """
        Update the system prompt.
        
        Args:
            system_prompt: The new system prompt
        """
        self.system_prompt = system_prompt
        # Update the first message if it's a system message
        if self.messages and self.messages[0]["role"] == "system":
            self.messages[0]["content"] = system_prompt
        else:
            # Insert at the beginning if there's no system message
            self.messages.insert(0, None)
    
    def xǁConversationMemoryǁupdate_system_prompt__mutmut_15(self, system_prompt: str) -> None:
        """
        Update the system prompt.
        
        Args:
            system_prompt: The new system prompt
        """
        self.system_prompt = system_prompt
        # Update the first message if it's a system message
        if self.messages and self.messages[0]["role"] == "system":
            self.messages[0]["content"] = system_prompt
        else:
            # Insert at the beginning if there's no system message
            self.messages.insert({"role": "system", "content": system_prompt})
    
    def xǁConversationMemoryǁupdate_system_prompt__mutmut_16(self, system_prompt: str) -> None:
        """
        Update the system prompt.
        
        Args:
            system_prompt: The new system prompt
        """
        self.system_prompt = system_prompt
        # Update the first message if it's a system message
        if self.messages and self.messages[0]["role"] == "system":
            self.messages[0]["content"] = system_prompt
        else:
            # Insert at the beginning if there's no system message
            self.messages.insert(0, )
    
    def xǁConversationMemoryǁupdate_system_prompt__mutmut_17(self, system_prompt: str) -> None:
        """
        Update the system prompt.
        
        Args:
            system_prompt: The new system prompt
        """
        self.system_prompt = system_prompt
        # Update the first message if it's a system message
        if self.messages and self.messages[0]["role"] == "system":
            self.messages[0]["content"] = system_prompt
        else:
            # Insert at the beginning if there's no system message
            self.messages.insert(1, {"role": "system", "content": system_prompt})
    
    def xǁConversationMemoryǁupdate_system_prompt__mutmut_18(self, system_prompt: str) -> None:
        """
        Update the system prompt.
        
        Args:
            system_prompt: The new system prompt
        """
        self.system_prompt = system_prompt
        # Update the first message if it's a system message
        if self.messages and self.messages[0]["role"] == "system":
            self.messages[0]["content"] = system_prompt
        else:
            # Insert at the beginning if there's no system message
            self.messages.insert(0, {"XXroleXX": "system", "content": system_prompt})
    
    def xǁConversationMemoryǁupdate_system_prompt__mutmut_19(self, system_prompt: str) -> None:
        """
        Update the system prompt.
        
        Args:
            system_prompt: The new system prompt
        """
        self.system_prompt = system_prompt
        # Update the first message if it's a system message
        if self.messages and self.messages[0]["role"] == "system":
            self.messages[0]["content"] = system_prompt
        else:
            # Insert at the beginning if there's no system message
            self.messages.insert(0, {"ROLE": "system", "content": system_prompt})
    
    def xǁConversationMemoryǁupdate_system_prompt__mutmut_20(self, system_prompt: str) -> None:
        """
        Update the system prompt.
        
        Args:
            system_prompt: The new system prompt
        """
        self.system_prompt = system_prompt
        # Update the first message if it's a system message
        if self.messages and self.messages[0]["role"] == "system":
            self.messages[0]["content"] = system_prompt
        else:
            # Insert at the beginning if there's no system message
            self.messages.insert(0, {"role": "XXsystemXX", "content": system_prompt})
    
    def xǁConversationMemoryǁupdate_system_prompt__mutmut_21(self, system_prompt: str) -> None:
        """
        Update the system prompt.
        
        Args:
            system_prompt: The new system prompt
        """
        self.system_prompt = system_prompt
        # Update the first message if it's a system message
        if self.messages and self.messages[0]["role"] == "system":
            self.messages[0]["content"] = system_prompt
        else:
            # Insert at the beginning if there's no system message
            self.messages.insert(0, {"role": "SYSTEM", "content": system_prompt})
    
    def xǁConversationMemoryǁupdate_system_prompt__mutmut_22(self, system_prompt: str) -> None:
        """
        Update the system prompt.
        
        Args:
            system_prompt: The new system prompt
        """
        self.system_prompt = system_prompt
        # Update the first message if it's a system message
        if self.messages and self.messages[0]["role"] == "system":
            self.messages[0]["content"] = system_prompt
        else:
            # Insert at the beginning if there's no system message
            self.messages.insert(0, {"role": "system", "XXcontentXX": system_prompt})
    
    def xǁConversationMemoryǁupdate_system_prompt__mutmut_23(self, system_prompt: str) -> None:
        """
        Update the system prompt.
        
        Args:
            system_prompt: The new system prompt
        """
        self.system_prompt = system_prompt
        # Update the first message if it's a system message
        if self.messages and self.messages[0]["role"] == "system":
            self.messages[0]["content"] = system_prompt
        else:
            # Insert at the beginning if there's no system message
            self.messages.insert(0, {"role": "system", "CONTENT": system_prompt})
    
    xǁConversationMemoryǁupdate_system_prompt__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁConversationMemoryǁupdate_system_prompt__mutmut_1': xǁConversationMemoryǁupdate_system_prompt__mutmut_1, 
        'xǁConversationMemoryǁupdate_system_prompt__mutmut_2': xǁConversationMemoryǁupdate_system_prompt__mutmut_2, 
        'xǁConversationMemoryǁupdate_system_prompt__mutmut_3': xǁConversationMemoryǁupdate_system_prompt__mutmut_3, 
        'xǁConversationMemoryǁupdate_system_prompt__mutmut_4': xǁConversationMemoryǁupdate_system_prompt__mutmut_4, 
        'xǁConversationMemoryǁupdate_system_prompt__mutmut_5': xǁConversationMemoryǁupdate_system_prompt__mutmut_5, 
        'xǁConversationMemoryǁupdate_system_prompt__mutmut_6': xǁConversationMemoryǁupdate_system_prompt__mutmut_6, 
        'xǁConversationMemoryǁupdate_system_prompt__mutmut_7': xǁConversationMemoryǁupdate_system_prompt__mutmut_7, 
        'xǁConversationMemoryǁupdate_system_prompt__mutmut_8': xǁConversationMemoryǁupdate_system_prompt__mutmut_8, 
        'xǁConversationMemoryǁupdate_system_prompt__mutmut_9': xǁConversationMemoryǁupdate_system_prompt__mutmut_9, 
        'xǁConversationMemoryǁupdate_system_prompt__mutmut_10': xǁConversationMemoryǁupdate_system_prompt__mutmut_10, 
        'xǁConversationMemoryǁupdate_system_prompt__mutmut_11': xǁConversationMemoryǁupdate_system_prompt__mutmut_11, 
        'xǁConversationMemoryǁupdate_system_prompt__mutmut_12': xǁConversationMemoryǁupdate_system_prompt__mutmut_12, 
        'xǁConversationMemoryǁupdate_system_prompt__mutmut_13': xǁConversationMemoryǁupdate_system_prompt__mutmut_13, 
        'xǁConversationMemoryǁupdate_system_prompt__mutmut_14': xǁConversationMemoryǁupdate_system_prompt__mutmut_14, 
        'xǁConversationMemoryǁupdate_system_prompt__mutmut_15': xǁConversationMemoryǁupdate_system_prompt__mutmut_15, 
        'xǁConversationMemoryǁupdate_system_prompt__mutmut_16': xǁConversationMemoryǁupdate_system_prompt__mutmut_16, 
        'xǁConversationMemoryǁupdate_system_prompt__mutmut_17': xǁConversationMemoryǁupdate_system_prompt__mutmut_17, 
        'xǁConversationMemoryǁupdate_system_prompt__mutmut_18': xǁConversationMemoryǁupdate_system_prompt__mutmut_18, 
        'xǁConversationMemoryǁupdate_system_prompt__mutmut_19': xǁConversationMemoryǁupdate_system_prompt__mutmut_19, 
        'xǁConversationMemoryǁupdate_system_prompt__mutmut_20': xǁConversationMemoryǁupdate_system_prompt__mutmut_20, 
        'xǁConversationMemoryǁupdate_system_prompt__mutmut_21': xǁConversationMemoryǁupdate_system_prompt__mutmut_21, 
        'xǁConversationMemoryǁupdate_system_prompt__mutmut_22': xǁConversationMemoryǁupdate_system_prompt__mutmut_22, 
        'xǁConversationMemoryǁupdate_system_prompt__mutmut_23': xǁConversationMemoryǁupdate_system_prompt__mutmut_23
    }
    
    def update_system_prompt(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁConversationMemoryǁupdate_system_prompt__mutmut_orig"), object.__getattribute__(self, "xǁConversationMemoryǁupdate_system_prompt__mutmut_mutants"), args, kwargs, self)
        return result 
    
    update_system_prompt.__signature__ = _mutmut_signature(xǁConversationMemoryǁupdate_system_prompt__mutmut_orig)
    xǁConversationMemoryǁupdate_system_prompt__mutmut_orig.__name__ = 'xǁConversationMemoryǁupdate_system_prompt'
    
    def xǁConversationMemoryǁis_function_call_loop__mutmut_orig(self, function_name: str, args: Dict) -> bool:
        """
        Check if we're in a function calling loop.
        
        Args:
            function_name: Name of the function
            args: Function arguments
            
        Returns:
            bool: Whether we're in a loop
        """
        # Normalize arguments for comparison
        def normalize_args(args_dict):
            normalized = {}
            for k, v in args_dict.items():
                if isinstance(v, str):
                    # Remove extra quotes that might be added by the model
                    normalized[k] = v.strip('"\'')
                else:
                    normalized[k] = v
            return normalized
            
        normalized_args = normalize_args(args)
        
        # Check if this function has been called with similar args too many times
        call_count = 0
        if function_name in self.function_calls:
            for call in self.function_calls[function_name]:
                if normalize_args(call.get("args", {})) == normalized_args:
                    call_count += 1
        
        # Save this call for future reference
        self.last_function_call = {
            "name": function_name,
            "args": args
        }
        
        # Consider it a loop if called more than twice with the same args
        return call_count >= 2
    
    def xǁConversationMemoryǁis_function_call_loop__mutmut_1(self, function_name: str, args: Dict) -> bool:
        """
        Check if we're in a function calling loop.
        
        Args:
            function_name: Name of the function
            args: Function arguments
            
        Returns:
            bool: Whether we're in a loop
        """
        # Normalize arguments for comparison
        def normalize_args(args_dict):
            normalized = None
            for k, v in args_dict.items():
                if isinstance(v, str):
                    # Remove extra quotes that might be added by the model
                    normalized[k] = v.strip('"\'')
                else:
                    normalized[k] = v
            return normalized
            
        normalized_args = normalize_args(args)
        
        # Check if this function has been called with similar args too many times
        call_count = 0
        if function_name in self.function_calls:
            for call in self.function_calls[function_name]:
                if normalize_args(call.get("args", {})) == normalized_args:
                    call_count += 1
        
        # Save this call for future reference
        self.last_function_call = {
            "name": function_name,
            "args": args
        }
        
        # Consider it a loop if called more than twice with the same args
        return call_count >= 2
    
    def xǁConversationMemoryǁis_function_call_loop__mutmut_2(self, function_name: str, args: Dict) -> bool:
        """
        Check if we're in a function calling loop.
        
        Args:
            function_name: Name of the function
            args: Function arguments
            
        Returns:
            bool: Whether we're in a loop
        """
        # Normalize arguments for comparison
        def normalize_args(args_dict):
            normalized = {}
            for k, v in args_dict.items():
                if isinstance(v, str):
                    # Remove extra quotes that might be added by the model
                    normalized[k] = None
                else:
                    normalized[k] = v
            return normalized
            
        normalized_args = normalize_args(args)
        
        # Check if this function has been called with similar args too many times
        call_count = 0
        if function_name in self.function_calls:
            for call in self.function_calls[function_name]:
                if normalize_args(call.get("args", {})) == normalized_args:
                    call_count += 1
        
        # Save this call for future reference
        self.last_function_call = {
            "name": function_name,
            "args": args
        }
        
        # Consider it a loop if called more than twice with the same args
        return call_count >= 2
    
    def xǁConversationMemoryǁis_function_call_loop__mutmut_3(self, function_name: str, args: Dict) -> bool:
        """
        Check if we're in a function calling loop.
        
        Args:
            function_name: Name of the function
            args: Function arguments
            
        Returns:
            bool: Whether we're in a loop
        """
        # Normalize arguments for comparison
        def normalize_args(args_dict):
            normalized = {}
            for k, v in args_dict.items():
                if isinstance(v, str):
                    # Remove extra quotes that might be added by the model
                    normalized[k] = v.strip(None)
                else:
                    normalized[k] = v
            return normalized
            
        normalized_args = normalize_args(args)
        
        # Check if this function has been called with similar args too many times
        call_count = 0
        if function_name in self.function_calls:
            for call in self.function_calls[function_name]:
                if normalize_args(call.get("args", {})) == normalized_args:
                    call_count += 1
        
        # Save this call for future reference
        self.last_function_call = {
            "name": function_name,
            "args": args
        }
        
        # Consider it a loop if called more than twice with the same args
        return call_count >= 2
    
    def xǁConversationMemoryǁis_function_call_loop__mutmut_4(self, function_name: str, args: Dict) -> bool:
        """
        Check if we're in a function calling loop.
        
        Args:
            function_name: Name of the function
            args: Function arguments
            
        Returns:
            bool: Whether we're in a loop
        """
        # Normalize arguments for comparison
        def normalize_args(args_dict):
            normalized = {}
            for k, v in args_dict.items():
                if isinstance(v, str):
                    # Remove extra quotes that might be added by the model
                    normalized[k] = v.strip('XX"\'XX')
                else:
                    normalized[k] = v
            return normalized
            
        normalized_args = normalize_args(args)
        
        # Check if this function has been called with similar args too many times
        call_count = 0
        if function_name in self.function_calls:
            for call in self.function_calls[function_name]:
                if normalize_args(call.get("args", {})) == normalized_args:
                    call_count += 1
        
        # Save this call for future reference
        self.last_function_call = {
            "name": function_name,
            "args": args
        }
        
        # Consider it a loop if called more than twice with the same args
        return call_count >= 2
    
    def xǁConversationMemoryǁis_function_call_loop__mutmut_5(self, function_name: str, args: Dict) -> bool:
        """
        Check if we're in a function calling loop.
        
        Args:
            function_name: Name of the function
            args: Function arguments
            
        Returns:
            bool: Whether we're in a loop
        """
        # Normalize arguments for comparison
        def normalize_args(args_dict):
            normalized = {}
            for k, v in args_dict.items():
                if isinstance(v, str):
                    # Remove extra quotes that might be added by the model
                    normalized[k] = v.strip('"\'')
                else:
                    normalized[k] = None
            return normalized
            
        normalized_args = normalize_args(args)
        
        # Check if this function has been called with similar args too many times
        call_count = 0
        if function_name in self.function_calls:
            for call in self.function_calls[function_name]:
                if normalize_args(call.get("args", {})) == normalized_args:
                    call_count += 1
        
        # Save this call for future reference
        self.last_function_call = {
            "name": function_name,
            "args": args
        }
        
        # Consider it a loop if called more than twice with the same args
        return call_count >= 2
    
    def xǁConversationMemoryǁis_function_call_loop__mutmut_6(self, function_name: str, args: Dict) -> bool:
        """
        Check if we're in a function calling loop.
        
        Args:
            function_name: Name of the function
            args: Function arguments
            
        Returns:
            bool: Whether we're in a loop
        """
        # Normalize arguments for comparison
        def normalize_args(args_dict):
            normalized = {}
            for k, v in args_dict.items():
                if isinstance(v, str):
                    # Remove extra quotes that might be added by the model
                    normalized[k] = v.strip('"\'')
                else:
                    normalized[k] = v
            return normalized
            
        normalized_args = None
        
        # Check if this function has been called with similar args too many times
        call_count = 0
        if function_name in self.function_calls:
            for call in self.function_calls[function_name]:
                if normalize_args(call.get("args", {})) == normalized_args:
                    call_count += 1
        
        # Save this call for future reference
        self.last_function_call = {
            "name": function_name,
            "args": args
        }
        
        # Consider it a loop if called more than twice with the same args
        return call_count >= 2
    
    def xǁConversationMemoryǁis_function_call_loop__mutmut_7(self, function_name: str, args: Dict) -> bool:
        """
        Check if we're in a function calling loop.
        
        Args:
            function_name: Name of the function
            args: Function arguments
            
        Returns:
            bool: Whether we're in a loop
        """
        # Normalize arguments for comparison
        def normalize_args(args_dict):
            normalized = {}
            for k, v in args_dict.items():
                if isinstance(v, str):
                    # Remove extra quotes that might be added by the model
                    normalized[k] = v.strip('"\'')
                else:
                    normalized[k] = v
            return normalized
            
        normalized_args = normalize_args(None)
        
        # Check if this function has been called with similar args too many times
        call_count = 0
        if function_name in self.function_calls:
            for call in self.function_calls[function_name]:
                if normalize_args(call.get("args", {})) == normalized_args:
                    call_count += 1
        
        # Save this call for future reference
        self.last_function_call = {
            "name": function_name,
            "args": args
        }
        
        # Consider it a loop if called more than twice with the same args
        return call_count >= 2
    
    def xǁConversationMemoryǁis_function_call_loop__mutmut_8(self, function_name: str, args: Dict) -> bool:
        """
        Check if we're in a function calling loop.
        
        Args:
            function_name: Name of the function
            args: Function arguments
            
        Returns:
            bool: Whether we're in a loop
        """
        # Normalize arguments for comparison
        def normalize_args(args_dict):
            normalized = {}
            for k, v in args_dict.items():
                if isinstance(v, str):
                    # Remove extra quotes that might be added by the model
                    normalized[k] = v.strip('"\'')
                else:
                    normalized[k] = v
            return normalized
            
        normalized_args = normalize_args(args)
        
        # Check if this function has been called with similar args too many times
        call_count = None
        if function_name in self.function_calls:
            for call in self.function_calls[function_name]:
                if normalize_args(call.get("args", {})) == normalized_args:
                    call_count += 1
        
        # Save this call for future reference
        self.last_function_call = {
            "name": function_name,
            "args": args
        }
        
        # Consider it a loop if called more than twice with the same args
        return call_count >= 2
    
    def xǁConversationMemoryǁis_function_call_loop__mutmut_9(self, function_name: str, args: Dict) -> bool:
        """
        Check if we're in a function calling loop.
        
        Args:
            function_name: Name of the function
            args: Function arguments
            
        Returns:
            bool: Whether we're in a loop
        """
        # Normalize arguments for comparison
        def normalize_args(args_dict):
            normalized = {}
            for k, v in args_dict.items():
                if isinstance(v, str):
                    # Remove extra quotes that might be added by the model
                    normalized[k] = v.strip('"\'')
                else:
                    normalized[k] = v
            return normalized
            
        normalized_args = normalize_args(args)
        
        # Check if this function has been called with similar args too many times
        call_count = 1
        if function_name in self.function_calls:
            for call in self.function_calls[function_name]:
                if normalize_args(call.get("args", {})) == normalized_args:
                    call_count += 1
        
        # Save this call for future reference
        self.last_function_call = {
            "name": function_name,
            "args": args
        }
        
        # Consider it a loop if called more than twice with the same args
        return call_count >= 2
    
    def xǁConversationMemoryǁis_function_call_loop__mutmut_10(self, function_name: str, args: Dict) -> bool:
        """
        Check if we're in a function calling loop.
        
        Args:
            function_name: Name of the function
            args: Function arguments
            
        Returns:
            bool: Whether we're in a loop
        """
        # Normalize arguments for comparison
        def normalize_args(args_dict):
            normalized = {}
            for k, v in args_dict.items():
                if isinstance(v, str):
                    # Remove extra quotes that might be added by the model
                    normalized[k] = v.strip('"\'')
                else:
                    normalized[k] = v
            return normalized
            
        normalized_args = normalize_args(args)
        
        # Check if this function has been called with similar args too many times
        call_count = 0
        if function_name not in self.function_calls:
            for call in self.function_calls[function_name]:
                if normalize_args(call.get("args", {})) == normalized_args:
                    call_count += 1
        
        # Save this call for future reference
        self.last_function_call = {
            "name": function_name,
            "args": args
        }
        
        # Consider it a loop if called more than twice with the same args
        return call_count >= 2
    
    def xǁConversationMemoryǁis_function_call_loop__mutmut_11(self, function_name: str, args: Dict) -> bool:
        """
        Check if we're in a function calling loop.
        
        Args:
            function_name: Name of the function
            args: Function arguments
            
        Returns:
            bool: Whether we're in a loop
        """
        # Normalize arguments for comparison
        def normalize_args(args_dict):
            normalized = {}
            for k, v in args_dict.items():
                if isinstance(v, str):
                    # Remove extra quotes that might be added by the model
                    normalized[k] = v.strip('"\'')
                else:
                    normalized[k] = v
            return normalized
            
        normalized_args = normalize_args(args)
        
        # Check if this function has been called with similar args too many times
        call_count = 0
        if function_name in self.function_calls:
            for call in self.function_calls[function_name]:
                if normalize_args(None) == normalized_args:
                    call_count += 1
        
        # Save this call for future reference
        self.last_function_call = {
            "name": function_name,
            "args": args
        }
        
        # Consider it a loop if called more than twice with the same args
        return call_count >= 2
    
    def xǁConversationMemoryǁis_function_call_loop__mutmut_12(self, function_name: str, args: Dict) -> bool:
        """
        Check if we're in a function calling loop.
        
        Args:
            function_name: Name of the function
            args: Function arguments
            
        Returns:
            bool: Whether we're in a loop
        """
        # Normalize arguments for comparison
        def normalize_args(args_dict):
            normalized = {}
            for k, v in args_dict.items():
                if isinstance(v, str):
                    # Remove extra quotes that might be added by the model
                    normalized[k] = v.strip('"\'')
                else:
                    normalized[k] = v
            return normalized
            
        normalized_args = normalize_args(args)
        
        # Check if this function has been called with similar args too many times
        call_count = 0
        if function_name in self.function_calls:
            for call in self.function_calls[function_name]:
                if normalize_args(call.get(None, {})) == normalized_args:
                    call_count += 1
        
        # Save this call for future reference
        self.last_function_call = {
            "name": function_name,
            "args": args
        }
        
        # Consider it a loop if called more than twice with the same args
        return call_count >= 2
    
    def xǁConversationMemoryǁis_function_call_loop__mutmut_13(self, function_name: str, args: Dict) -> bool:
        """
        Check if we're in a function calling loop.
        
        Args:
            function_name: Name of the function
            args: Function arguments
            
        Returns:
            bool: Whether we're in a loop
        """
        # Normalize arguments for comparison
        def normalize_args(args_dict):
            normalized = {}
            for k, v in args_dict.items():
                if isinstance(v, str):
                    # Remove extra quotes that might be added by the model
                    normalized[k] = v.strip('"\'')
                else:
                    normalized[k] = v
            return normalized
            
        normalized_args = normalize_args(args)
        
        # Check if this function has been called with similar args too many times
        call_count = 0
        if function_name in self.function_calls:
            for call in self.function_calls[function_name]:
                if normalize_args(call.get("args", None)) == normalized_args:
                    call_count += 1
        
        # Save this call for future reference
        self.last_function_call = {
            "name": function_name,
            "args": args
        }
        
        # Consider it a loop if called more than twice with the same args
        return call_count >= 2
    
    def xǁConversationMemoryǁis_function_call_loop__mutmut_14(self, function_name: str, args: Dict) -> bool:
        """
        Check if we're in a function calling loop.
        
        Args:
            function_name: Name of the function
            args: Function arguments
            
        Returns:
            bool: Whether we're in a loop
        """
        # Normalize arguments for comparison
        def normalize_args(args_dict):
            normalized = {}
            for k, v in args_dict.items():
                if isinstance(v, str):
                    # Remove extra quotes that might be added by the model
                    normalized[k] = v.strip('"\'')
                else:
                    normalized[k] = v
            return normalized
            
        normalized_args = normalize_args(args)
        
        # Check if this function has been called with similar args too many times
        call_count = 0
        if function_name in self.function_calls:
            for call in self.function_calls[function_name]:
                if normalize_args(call.get({})) == normalized_args:
                    call_count += 1
        
        # Save this call for future reference
        self.last_function_call = {
            "name": function_name,
            "args": args
        }
        
        # Consider it a loop if called more than twice with the same args
        return call_count >= 2
    
    def xǁConversationMemoryǁis_function_call_loop__mutmut_15(self, function_name: str, args: Dict) -> bool:
        """
        Check if we're in a function calling loop.
        
        Args:
            function_name: Name of the function
            args: Function arguments
            
        Returns:
            bool: Whether we're in a loop
        """
        # Normalize arguments for comparison
        def normalize_args(args_dict):
            normalized = {}
            for k, v in args_dict.items():
                if isinstance(v, str):
                    # Remove extra quotes that might be added by the model
                    normalized[k] = v.strip('"\'')
                else:
                    normalized[k] = v
            return normalized
            
        normalized_args = normalize_args(args)
        
        # Check if this function has been called with similar args too many times
        call_count = 0
        if function_name in self.function_calls:
            for call in self.function_calls[function_name]:
                if normalize_args(call.get("args", )) == normalized_args:
                    call_count += 1
        
        # Save this call for future reference
        self.last_function_call = {
            "name": function_name,
            "args": args
        }
        
        # Consider it a loop if called more than twice with the same args
        return call_count >= 2
    
    def xǁConversationMemoryǁis_function_call_loop__mutmut_16(self, function_name: str, args: Dict) -> bool:
        """
        Check if we're in a function calling loop.
        
        Args:
            function_name: Name of the function
            args: Function arguments
            
        Returns:
            bool: Whether we're in a loop
        """
        # Normalize arguments for comparison
        def normalize_args(args_dict):
            normalized = {}
            for k, v in args_dict.items():
                if isinstance(v, str):
                    # Remove extra quotes that might be added by the model
                    normalized[k] = v.strip('"\'')
                else:
                    normalized[k] = v
            return normalized
            
        normalized_args = normalize_args(args)
        
        # Check if this function has been called with similar args too many times
        call_count = 0
        if function_name in self.function_calls:
            for call in self.function_calls[function_name]:
                if normalize_args(call.get("XXargsXX", {})) == normalized_args:
                    call_count += 1
        
        # Save this call for future reference
        self.last_function_call = {
            "name": function_name,
            "args": args
        }
        
        # Consider it a loop if called more than twice with the same args
        return call_count >= 2
    
    def xǁConversationMemoryǁis_function_call_loop__mutmut_17(self, function_name: str, args: Dict) -> bool:
        """
        Check if we're in a function calling loop.
        
        Args:
            function_name: Name of the function
            args: Function arguments
            
        Returns:
            bool: Whether we're in a loop
        """
        # Normalize arguments for comparison
        def normalize_args(args_dict):
            normalized = {}
            for k, v in args_dict.items():
                if isinstance(v, str):
                    # Remove extra quotes that might be added by the model
                    normalized[k] = v.strip('"\'')
                else:
                    normalized[k] = v
            return normalized
            
        normalized_args = normalize_args(args)
        
        # Check if this function has been called with similar args too many times
        call_count = 0
        if function_name in self.function_calls:
            for call in self.function_calls[function_name]:
                if normalize_args(call.get("ARGS", {})) == normalized_args:
                    call_count += 1
        
        # Save this call for future reference
        self.last_function_call = {
            "name": function_name,
            "args": args
        }
        
        # Consider it a loop if called more than twice with the same args
        return call_count >= 2
    
    def xǁConversationMemoryǁis_function_call_loop__mutmut_18(self, function_name: str, args: Dict) -> bool:
        """
        Check if we're in a function calling loop.
        
        Args:
            function_name: Name of the function
            args: Function arguments
            
        Returns:
            bool: Whether we're in a loop
        """
        # Normalize arguments for comparison
        def normalize_args(args_dict):
            normalized = {}
            for k, v in args_dict.items():
                if isinstance(v, str):
                    # Remove extra quotes that might be added by the model
                    normalized[k] = v.strip('"\'')
                else:
                    normalized[k] = v
            return normalized
            
        normalized_args = normalize_args(args)
        
        # Check if this function has been called with similar args too many times
        call_count = 0
        if function_name in self.function_calls:
            for call in self.function_calls[function_name]:
                if normalize_args(call.get("args", {})) != normalized_args:
                    call_count += 1
        
        # Save this call for future reference
        self.last_function_call = {
            "name": function_name,
            "args": args
        }
        
        # Consider it a loop if called more than twice with the same args
        return call_count >= 2
    
    def xǁConversationMemoryǁis_function_call_loop__mutmut_19(self, function_name: str, args: Dict) -> bool:
        """
        Check if we're in a function calling loop.
        
        Args:
            function_name: Name of the function
            args: Function arguments
            
        Returns:
            bool: Whether we're in a loop
        """
        # Normalize arguments for comparison
        def normalize_args(args_dict):
            normalized = {}
            for k, v in args_dict.items():
                if isinstance(v, str):
                    # Remove extra quotes that might be added by the model
                    normalized[k] = v.strip('"\'')
                else:
                    normalized[k] = v
            return normalized
            
        normalized_args = normalize_args(args)
        
        # Check if this function has been called with similar args too many times
        call_count = 0
        if function_name in self.function_calls:
            for call in self.function_calls[function_name]:
                if normalize_args(call.get("args", {})) == normalized_args:
                    call_count = 1
        
        # Save this call for future reference
        self.last_function_call = {
            "name": function_name,
            "args": args
        }
        
        # Consider it a loop if called more than twice with the same args
        return call_count >= 2
    
    def xǁConversationMemoryǁis_function_call_loop__mutmut_20(self, function_name: str, args: Dict) -> bool:
        """
        Check if we're in a function calling loop.
        
        Args:
            function_name: Name of the function
            args: Function arguments
            
        Returns:
            bool: Whether we're in a loop
        """
        # Normalize arguments for comparison
        def normalize_args(args_dict):
            normalized = {}
            for k, v in args_dict.items():
                if isinstance(v, str):
                    # Remove extra quotes that might be added by the model
                    normalized[k] = v.strip('"\'')
                else:
                    normalized[k] = v
            return normalized
            
        normalized_args = normalize_args(args)
        
        # Check if this function has been called with similar args too many times
        call_count = 0
        if function_name in self.function_calls:
            for call in self.function_calls[function_name]:
                if normalize_args(call.get("args", {})) == normalized_args:
                    call_count -= 1
        
        # Save this call for future reference
        self.last_function_call = {
            "name": function_name,
            "args": args
        }
        
        # Consider it a loop if called more than twice with the same args
        return call_count >= 2
    
    def xǁConversationMemoryǁis_function_call_loop__mutmut_21(self, function_name: str, args: Dict) -> bool:
        """
        Check if we're in a function calling loop.
        
        Args:
            function_name: Name of the function
            args: Function arguments
            
        Returns:
            bool: Whether we're in a loop
        """
        # Normalize arguments for comparison
        def normalize_args(args_dict):
            normalized = {}
            for k, v in args_dict.items():
                if isinstance(v, str):
                    # Remove extra quotes that might be added by the model
                    normalized[k] = v.strip('"\'')
                else:
                    normalized[k] = v
            return normalized
            
        normalized_args = normalize_args(args)
        
        # Check if this function has been called with similar args too many times
        call_count = 0
        if function_name in self.function_calls:
            for call in self.function_calls[function_name]:
                if normalize_args(call.get("args", {})) == normalized_args:
                    call_count += 2
        
        # Save this call for future reference
        self.last_function_call = {
            "name": function_name,
            "args": args
        }
        
        # Consider it a loop if called more than twice with the same args
        return call_count >= 2
    
    def xǁConversationMemoryǁis_function_call_loop__mutmut_22(self, function_name: str, args: Dict) -> bool:
        """
        Check if we're in a function calling loop.
        
        Args:
            function_name: Name of the function
            args: Function arguments
            
        Returns:
            bool: Whether we're in a loop
        """
        # Normalize arguments for comparison
        def normalize_args(args_dict):
            normalized = {}
            for k, v in args_dict.items():
                if isinstance(v, str):
                    # Remove extra quotes that might be added by the model
                    normalized[k] = v.strip('"\'')
                else:
                    normalized[k] = v
            return normalized
            
        normalized_args = normalize_args(args)
        
        # Check if this function has been called with similar args too many times
        call_count = 0
        if function_name in self.function_calls:
            for call in self.function_calls[function_name]:
                if normalize_args(call.get("args", {})) == normalized_args:
                    call_count += 1
        
        # Save this call for future reference
        self.last_function_call = None
        
        # Consider it a loop if called more than twice with the same args
        return call_count >= 2
    
    def xǁConversationMemoryǁis_function_call_loop__mutmut_23(self, function_name: str, args: Dict) -> bool:
        """
        Check if we're in a function calling loop.
        
        Args:
            function_name: Name of the function
            args: Function arguments
            
        Returns:
            bool: Whether we're in a loop
        """
        # Normalize arguments for comparison
        def normalize_args(args_dict):
            normalized = {}
            for k, v in args_dict.items():
                if isinstance(v, str):
                    # Remove extra quotes that might be added by the model
                    normalized[k] = v.strip('"\'')
                else:
                    normalized[k] = v
            return normalized
            
        normalized_args = normalize_args(args)
        
        # Check if this function has been called with similar args too many times
        call_count = 0
        if function_name in self.function_calls:
            for call in self.function_calls[function_name]:
                if normalize_args(call.get("args", {})) == normalized_args:
                    call_count += 1
        
        # Save this call for future reference
        self.last_function_call = {
            "XXnameXX": function_name,
            "args": args
        }
        
        # Consider it a loop if called more than twice with the same args
        return call_count >= 2
    
    def xǁConversationMemoryǁis_function_call_loop__mutmut_24(self, function_name: str, args: Dict) -> bool:
        """
        Check if we're in a function calling loop.
        
        Args:
            function_name: Name of the function
            args: Function arguments
            
        Returns:
            bool: Whether we're in a loop
        """
        # Normalize arguments for comparison
        def normalize_args(args_dict):
            normalized = {}
            for k, v in args_dict.items():
                if isinstance(v, str):
                    # Remove extra quotes that might be added by the model
                    normalized[k] = v.strip('"\'')
                else:
                    normalized[k] = v
            return normalized
            
        normalized_args = normalize_args(args)
        
        # Check if this function has been called with similar args too many times
        call_count = 0
        if function_name in self.function_calls:
            for call in self.function_calls[function_name]:
                if normalize_args(call.get("args", {})) == normalized_args:
                    call_count += 1
        
        # Save this call for future reference
        self.last_function_call = {
            "NAME": function_name,
            "args": args
        }
        
        # Consider it a loop if called more than twice with the same args
        return call_count >= 2
    
    def xǁConversationMemoryǁis_function_call_loop__mutmut_25(self, function_name: str, args: Dict) -> bool:
        """
        Check if we're in a function calling loop.
        
        Args:
            function_name: Name of the function
            args: Function arguments
            
        Returns:
            bool: Whether we're in a loop
        """
        # Normalize arguments for comparison
        def normalize_args(args_dict):
            normalized = {}
            for k, v in args_dict.items():
                if isinstance(v, str):
                    # Remove extra quotes that might be added by the model
                    normalized[k] = v.strip('"\'')
                else:
                    normalized[k] = v
            return normalized
            
        normalized_args = normalize_args(args)
        
        # Check if this function has been called with similar args too many times
        call_count = 0
        if function_name in self.function_calls:
            for call in self.function_calls[function_name]:
                if normalize_args(call.get("args", {})) == normalized_args:
                    call_count += 1
        
        # Save this call for future reference
        self.last_function_call = {
            "name": function_name,
            "XXargsXX": args
        }
        
        # Consider it a loop if called more than twice with the same args
        return call_count >= 2
    
    def xǁConversationMemoryǁis_function_call_loop__mutmut_26(self, function_name: str, args: Dict) -> bool:
        """
        Check if we're in a function calling loop.
        
        Args:
            function_name: Name of the function
            args: Function arguments
            
        Returns:
            bool: Whether we're in a loop
        """
        # Normalize arguments for comparison
        def normalize_args(args_dict):
            normalized = {}
            for k, v in args_dict.items():
                if isinstance(v, str):
                    # Remove extra quotes that might be added by the model
                    normalized[k] = v.strip('"\'')
                else:
                    normalized[k] = v
            return normalized
            
        normalized_args = normalize_args(args)
        
        # Check if this function has been called with similar args too many times
        call_count = 0
        if function_name in self.function_calls:
            for call in self.function_calls[function_name]:
                if normalize_args(call.get("args", {})) == normalized_args:
                    call_count += 1
        
        # Save this call for future reference
        self.last_function_call = {
            "name": function_name,
            "ARGS": args
        }
        
        # Consider it a loop if called more than twice with the same args
        return call_count >= 2
    
    def xǁConversationMemoryǁis_function_call_loop__mutmut_27(self, function_name: str, args: Dict) -> bool:
        """
        Check if we're in a function calling loop.
        
        Args:
            function_name: Name of the function
            args: Function arguments
            
        Returns:
            bool: Whether we're in a loop
        """
        # Normalize arguments for comparison
        def normalize_args(args_dict):
            normalized = {}
            for k, v in args_dict.items():
                if isinstance(v, str):
                    # Remove extra quotes that might be added by the model
                    normalized[k] = v.strip('"\'')
                else:
                    normalized[k] = v
            return normalized
            
        normalized_args = normalize_args(args)
        
        # Check if this function has been called with similar args too many times
        call_count = 0
        if function_name in self.function_calls:
            for call in self.function_calls[function_name]:
                if normalize_args(call.get("args", {})) == normalized_args:
                    call_count += 1
        
        # Save this call for future reference
        self.last_function_call = {
            "name": function_name,
            "args": args
        }
        
        # Consider it a loop if called more than twice with the same args
        return call_count > 2
    
    def xǁConversationMemoryǁis_function_call_loop__mutmut_28(self, function_name: str, args: Dict) -> bool:
        """
        Check if we're in a function calling loop.
        
        Args:
            function_name: Name of the function
            args: Function arguments
            
        Returns:
            bool: Whether we're in a loop
        """
        # Normalize arguments for comparison
        def normalize_args(args_dict):
            normalized = {}
            for k, v in args_dict.items():
                if isinstance(v, str):
                    # Remove extra quotes that might be added by the model
                    normalized[k] = v.strip('"\'')
                else:
                    normalized[k] = v
            return normalized
            
        normalized_args = normalize_args(args)
        
        # Check if this function has been called with similar args too many times
        call_count = 0
        if function_name in self.function_calls:
            for call in self.function_calls[function_name]:
                if normalize_args(call.get("args", {})) == normalized_args:
                    call_count += 1
        
        # Save this call for future reference
        self.last_function_call = {
            "name": function_name,
            "args": args
        }
        
        # Consider it a loop if called more than twice with the same args
        return call_count >= 3
    
    xǁConversationMemoryǁis_function_call_loop__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁConversationMemoryǁis_function_call_loop__mutmut_1': xǁConversationMemoryǁis_function_call_loop__mutmut_1, 
        'xǁConversationMemoryǁis_function_call_loop__mutmut_2': xǁConversationMemoryǁis_function_call_loop__mutmut_2, 
        'xǁConversationMemoryǁis_function_call_loop__mutmut_3': xǁConversationMemoryǁis_function_call_loop__mutmut_3, 
        'xǁConversationMemoryǁis_function_call_loop__mutmut_4': xǁConversationMemoryǁis_function_call_loop__mutmut_4, 
        'xǁConversationMemoryǁis_function_call_loop__mutmut_5': xǁConversationMemoryǁis_function_call_loop__mutmut_5, 
        'xǁConversationMemoryǁis_function_call_loop__mutmut_6': xǁConversationMemoryǁis_function_call_loop__mutmut_6, 
        'xǁConversationMemoryǁis_function_call_loop__mutmut_7': xǁConversationMemoryǁis_function_call_loop__mutmut_7, 
        'xǁConversationMemoryǁis_function_call_loop__mutmut_8': xǁConversationMemoryǁis_function_call_loop__mutmut_8, 
        'xǁConversationMemoryǁis_function_call_loop__mutmut_9': xǁConversationMemoryǁis_function_call_loop__mutmut_9, 
        'xǁConversationMemoryǁis_function_call_loop__mutmut_10': xǁConversationMemoryǁis_function_call_loop__mutmut_10, 
        'xǁConversationMemoryǁis_function_call_loop__mutmut_11': xǁConversationMemoryǁis_function_call_loop__mutmut_11, 
        'xǁConversationMemoryǁis_function_call_loop__mutmut_12': xǁConversationMemoryǁis_function_call_loop__mutmut_12, 
        'xǁConversationMemoryǁis_function_call_loop__mutmut_13': xǁConversationMemoryǁis_function_call_loop__mutmut_13, 
        'xǁConversationMemoryǁis_function_call_loop__mutmut_14': xǁConversationMemoryǁis_function_call_loop__mutmut_14, 
        'xǁConversationMemoryǁis_function_call_loop__mutmut_15': xǁConversationMemoryǁis_function_call_loop__mutmut_15, 
        'xǁConversationMemoryǁis_function_call_loop__mutmut_16': xǁConversationMemoryǁis_function_call_loop__mutmut_16, 
        'xǁConversationMemoryǁis_function_call_loop__mutmut_17': xǁConversationMemoryǁis_function_call_loop__mutmut_17, 
        'xǁConversationMemoryǁis_function_call_loop__mutmut_18': xǁConversationMemoryǁis_function_call_loop__mutmut_18, 
        'xǁConversationMemoryǁis_function_call_loop__mutmut_19': xǁConversationMemoryǁis_function_call_loop__mutmut_19, 
        'xǁConversationMemoryǁis_function_call_loop__mutmut_20': xǁConversationMemoryǁis_function_call_loop__mutmut_20, 
        'xǁConversationMemoryǁis_function_call_loop__mutmut_21': xǁConversationMemoryǁis_function_call_loop__mutmut_21, 
        'xǁConversationMemoryǁis_function_call_loop__mutmut_22': xǁConversationMemoryǁis_function_call_loop__mutmut_22, 
        'xǁConversationMemoryǁis_function_call_loop__mutmut_23': xǁConversationMemoryǁis_function_call_loop__mutmut_23, 
        'xǁConversationMemoryǁis_function_call_loop__mutmut_24': xǁConversationMemoryǁis_function_call_loop__mutmut_24, 
        'xǁConversationMemoryǁis_function_call_loop__mutmut_25': xǁConversationMemoryǁis_function_call_loop__mutmut_25, 
        'xǁConversationMemoryǁis_function_call_loop__mutmut_26': xǁConversationMemoryǁis_function_call_loop__mutmut_26, 
        'xǁConversationMemoryǁis_function_call_loop__mutmut_27': xǁConversationMemoryǁis_function_call_loop__mutmut_27, 
        'xǁConversationMemoryǁis_function_call_loop__mutmut_28': xǁConversationMemoryǁis_function_call_loop__mutmut_28
    }
    
    def is_function_call_loop(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁConversationMemoryǁis_function_call_loop__mutmut_orig"), object.__getattribute__(self, "xǁConversationMemoryǁis_function_call_loop__mutmut_mutants"), args, kwargs, self)
        return result 
    
    is_function_call_loop.__signature__ = _mutmut_signature(xǁConversationMemoryǁis_function_call_loop__mutmut_orig)
    xǁConversationMemoryǁis_function_call_loop__mutmut_orig.__name__ = 'xǁConversationMemoryǁis_function_call_loop'
    
    def xǁConversationMemoryǁget_last_function_result__mutmut_orig(self, function_name: str) -> Optional[str]:
        """
        Get the last result from a specific function.
        
        Args:
            function_name: Name of the function
            
        Returns:
            str or None: The function result or None if not found
        """
        for message in reversed(self.messages):
            # Check for both 'tool' (modern) and 'function' (legacy) roles for backward compatibility
            if (message.get("role") in ["tool", "function"]) and message.get("name") == function_name:
                return message.get("content")
        return None
        
    
    def xǁConversationMemoryǁget_last_function_result__mutmut_1(self, function_name: str) -> Optional[str]:
        """
        Get the last result from a specific function.
        
        Args:
            function_name: Name of the function
            
        Returns:
            str or None: The function result or None if not found
        """
        for message in reversed(None):
            # Check for both 'tool' (modern) and 'function' (legacy) roles for backward compatibility
            if (message.get("role") in ["tool", "function"]) and message.get("name") == function_name:
                return message.get("content")
        return None
        
    
    def xǁConversationMemoryǁget_last_function_result__mutmut_2(self, function_name: str) -> Optional[str]:
        """
        Get the last result from a specific function.
        
        Args:
            function_name: Name of the function
            
        Returns:
            str or None: The function result or None if not found
        """
        for message in reversed(self.messages):
            # Check for both 'tool' (modern) and 'function' (legacy) roles for backward compatibility
            if (message.get("role") in ["tool", "function"]) or message.get("name") == function_name:
                return message.get("content")
        return None
        
    
    def xǁConversationMemoryǁget_last_function_result__mutmut_3(self, function_name: str) -> Optional[str]:
        """
        Get the last result from a specific function.
        
        Args:
            function_name: Name of the function
            
        Returns:
            str or None: The function result or None if not found
        """
        for message in reversed(self.messages):
            # Check for both 'tool' (modern) and 'function' (legacy) roles for backward compatibility
            if (message.get(None) in ["tool", "function"]) and message.get("name") == function_name:
                return message.get("content")
        return None
        
    
    def xǁConversationMemoryǁget_last_function_result__mutmut_4(self, function_name: str) -> Optional[str]:
        """
        Get the last result from a specific function.
        
        Args:
            function_name: Name of the function
            
        Returns:
            str or None: The function result or None if not found
        """
        for message in reversed(self.messages):
            # Check for both 'tool' (modern) and 'function' (legacy) roles for backward compatibility
            if (message.get("XXroleXX") in ["tool", "function"]) and message.get("name") == function_name:
                return message.get("content")
        return None
        
    
    def xǁConversationMemoryǁget_last_function_result__mutmut_5(self, function_name: str) -> Optional[str]:
        """
        Get the last result from a specific function.
        
        Args:
            function_name: Name of the function
            
        Returns:
            str or None: The function result or None if not found
        """
        for message in reversed(self.messages):
            # Check for both 'tool' (modern) and 'function' (legacy) roles for backward compatibility
            if (message.get("ROLE") in ["tool", "function"]) and message.get("name") == function_name:
                return message.get("content")
        return None
        
    
    def xǁConversationMemoryǁget_last_function_result__mutmut_6(self, function_name: str) -> Optional[str]:
        """
        Get the last result from a specific function.
        
        Args:
            function_name: Name of the function
            
        Returns:
            str or None: The function result or None if not found
        """
        for message in reversed(self.messages):
            # Check for both 'tool' (modern) and 'function' (legacy) roles for backward compatibility
            if (message.get("role") not in ["tool", "function"]) and message.get("name") == function_name:
                return message.get("content")
        return None
        
    
    def xǁConversationMemoryǁget_last_function_result__mutmut_7(self, function_name: str) -> Optional[str]:
        """
        Get the last result from a specific function.
        
        Args:
            function_name: Name of the function
            
        Returns:
            str or None: The function result or None if not found
        """
        for message in reversed(self.messages):
            # Check for both 'tool' (modern) and 'function' (legacy) roles for backward compatibility
            if (message.get("role") in ["XXtoolXX", "function"]) and message.get("name") == function_name:
                return message.get("content")
        return None
        
    
    def xǁConversationMemoryǁget_last_function_result__mutmut_8(self, function_name: str) -> Optional[str]:
        """
        Get the last result from a specific function.
        
        Args:
            function_name: Name of the function
            
        Returns:
            str or None: The function result or None if not found
        """
        for message in reversed(self.messages):
            # Check for both 'tool' (modern) and 'function' (legacy) roles for backward compatibility
            if (message.get("role") in ["TOOL", "function"]) and message.get("name") == function_name:
                return message.get("content")
        return None
        
    
    def xǁConversationMemoryǁget_last_function_result__mutmut_9(self, function_name: str) -> Optional[str]:
        """
        Get the last result from a specific function.
        
        Args:
            function_name: Name of the function
            
        Returns:
            str or None: The function result or None if not found
        """
        for message in reversed(self.messages):
            # Check for both 'tool' (modern) and 'function' (legacy) roles for backward compatibility
            if (message.get("role") in ["tool", "XXfunctionXX"]) and message.get("name") == function_name:
                return message.get("content")
        return None
        
    
    def xǁConversationMemoryǁget_last_function_result__mutmut_10(self, function_name: str) -> Optional[str]:
        """
        Get the last result from a specific function.
        
        Args:
            function_name: Name of the function
            
        Returns:
            str or None: The function result or None if not found
        """
        for message in reversed(self.messages):
            # Check for both 'tool' (modern) and 'function' (legacy) roles for backward compatibility
            if (message.get("role") in ["tool", "FUNCTION"]) and message.get("name") == function_name:
                return message.get("content")
        return None
        
    
    def xǁConversationMemoryǁget_last_function_result__mutmut_11(self, function_name: str) -> Optional[str]:
        """
        Get the last result from a specific function.
        
        Args:
            function_name: Name of the function
            
        Returns:
            str or None: The function result or None if not found
        """
        for message in reversed(self.messages):
            # Check for both 'tool' (modern) and 'function' (legacy) roles for backward compatibility
            if (message.get("role") in ["tool", "function"]) and message.get(None) == function_name:
                return message.get("content")
        return None
        
    
    def xǁConversationMemoryǁget_last_function_result__mutmut_12(self, function_name: str) -> Optional[str]:
        """
        Get the last result from a specific function.
        
        Args:
            function_name: Name of the function
            
        Returns:
            str or None: The function result or None if not found
        """
        for message in reversed(self.messages):
            # Check for both 'tool' (modern) and 'function' (legacy) roles for backward compatibility
            if (message.get("role") in ["tool", "function"]) and message.get("XXnameXX") == function_name:
                return message.get("content")
        return None
        
    
    def xǁConversationMemoryǁget_last_function_result__mutmut_13(self, function_name: str) -> Optional[str]:
        """
        Get the last result from a specific function.
        
        Args:
            function_name: Name of the function
            
        Returns:
            str or None: The function result or None if not found
        """
        for message in reversed(self.messages):
            # Check for both 'tool' (modern) and 'function' (legacy) roles for backward compatibility
            if (message.get("role") in ["tool", "function"]) and message.get("NAME") == function_name:
                return message.get("content")
        return None
        
    
    def xǁConversationMemoryǁget_last_function_result__mutmut_14(self, function_name: str) -> Optional[str]:
        """
        Get the last result from a specific function.
        
        Args:
            function_name: Name of the function
            
        Returns:
            str or None: The function result or None if not found
        """
        for message in reversed(self.messages):
            # Check for both 'tool' (modern) and 'function' (legacy) roles for backward compatibility
            if (message.get("role") in ["tool", "function"]) and message.get("name") != function_name:
                return message.get("content")
        return None
        
    
    def xǁConversationMemoryǁget_last_function_result__mutmut_15(self, function_name: str) -> Optional[str]:
        """
        Get the last result from a specific function.
        
        Args:
            function_name: Name of the function
            
        Returns:
            str or None: The function result or None if not found
        """
        for message in reversed(self.messages):
            # Check for both 'tool' (modern) and 'function' (legacy) roles for backward compatibility
            if (message.get("role") in ["tool", "function"]) and message.get("name") == function_name:
                return message.get(None)
        return None
        
    
    def xǁConversationMemoryǁget_last_function_result__mutmut_16(self, function_name: str) -> Optional[str]:
        """
        Get the last result from a specific function.
        
        Args:
            function_name: Name of the function
            
        Returns:
            str or None: The function result or None if not found
        """
        for message in reversed(self.messages):
            # Check for both 'tool' (modern) and 'function' (legacy) roles for backward compatibility
            if (message.get("role") in ["tool", "function"]) and message.get("name") == function_name:
                return message.get("XXcontentXX")
        return None
        
    
    def xǁConversationMemoryǁget_last_function_result__mutmut_17(self, function_name: str) -> Optional[str]:
        """
        Get the last result from a specific function.
        
        Args:
            function_name: Name of the function
            
        Returns:
            str or None: The function result or None if not found
        """
        for message in reversed(self.messages):
            # Check for both 'tool' (modern) and 'function' (legacy) roles for backward compatibility
            if (message.get("role") in ["tool", "function"]) and message.get("name") == function_name:
                return message.get("CONTENT")
        return None
        
    
    xǁConversationMemoryǁget_last_function_result__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁConversationMemoryǁget_last_function_result__mutmut_1': xǁConversationMemoryǁget_last_function_result__mutmut_1, 
        'xǁConversationMemoryǁget_last_function_result__mutmut_2': xǁConversationMemoryǁget_last_function_result__mutmut_2, 
        'xǁConversationMemoryǁget_last_function_result__mutmut_3': xǁConversationMemoryǁget_last_function_result__mutmut_3, 
        'xǁConversationMemoryǁget_last_function_result__mutmut_4': xǁConversationMemoryǁget_last_function_result__mutmut_4, 
        'xǁConversationMemoryǁget_last_function_result__mutmut_5': xǁConversationMemoryǁget_last_function_result__mutmut_5, 
        'xǁConversationMemoryǁget_last_function_result__mutmut_6': xǁConversationMemoryǁget_last_function_result__mutmut_6, 
        'xǁConversationMemoryǁget_last_function_result__mutmut_7': xǁConversationMemoryǁget_last_function_result__mutmut_7, 
        'xǁConversationMemoryǁget_last_function_result__mutmut_8': xǁConversationMemoryǁget_last_function_result__mutmut_8, 
        'xǁConversationMemoryǁget_last_function_result__mutmut_9': xǁConversationMemoryǁget_last_function_result__mutmut_9, 
        'xǁConversationMemoryǁget_last_function_result__mutmut_10': xǁConversationMemoryǁget_last_function_result__mutmut_10, 
        'xǁConversationMemoryǁget_last_function_result__mutmut_11': xǁConversationMemoryǁget_last_function_result__mutmut_11, 
        'xǁConversationMemoryǁget_last_function_result__mutmut_12': xǁConversationMemoryǁget_last_function_result__mutmut_12, 
        'xǁConversationMemoryǁget_last_function_result__mutmut_13': xǁConversationMemoryǁget_last_function_result__mutmut_13, 
        'xǁConversationMemoryǁget_last_function_result__mutmut_14': xǁConversationMemoryǁget_last_function_result__mutmut_14, 
        'xǁConversationMemoryǁget_last_function_result__mutmut_15': xǁConversationMemoryǁget_last_function_result__mutmut_15, 
        'xǁConversationMemoryǁget_last_function_result__mutmut_16': xǁConversationMemoryǁget_last_function_result__mutmut_16, 
        'xǁConversationMemoryǁget_last_function_result__mutmut_17': xǁConversationMemoryǁget_last_function_result__mutmut_17
    }
    
    def get_last_function_result(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁConversationMemoryǁget_last_function_result__mutmut_orig"), object.__getattribute__(self, "xǁConversationMemoryǁget_last_function_result__mutmut_mutants"), args, kwargs, self)
        return result 
    
    get_last_function_result.__signature__ = _mutmut_signature(xǁConversationMemoryǁget_last_function_result__mutmut_orig)
    xǁConversationMemoryǁget_last_function_result__mutmut_orig.__name__ = 'xǁConversationMemoryǁget_last_function_result'
    def clear(self) -> None:
        """Clear all conversation history except the system prompt."""
        # This is an alias for reset()
        self.reset() 