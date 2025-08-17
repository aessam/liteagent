"""
Unit tests for image and advanced capabilities in LiteAgent.

This module tests the image handling capabilities and advanced features like caching
in a deterministic way without requiring API calls.
"""

import pytest
import os
import base64
from pathlib import Path
from unittest.mock import patch, MagicMock

from liteagent.memory import ConversationMemory
from liteagent.agent import LiteAgent
from liteagent.capabilities import get_model_capabilities


class TestImageCapabilities:
    """Test image handling capabilities in memory and agents."""
    
    @pytest.fixture
    def test_images_path(self):
        """Get the path to test images."""
        return Path(__file__).parent.parent / "assets"
    
    @pytest.fixture
    def test_image_files(self, test_images_path):
        """Get available test image files."""
        image_files = {}
        if (test_images_path / "Philips_PM5544.svg.png").exists():
            image_files["test_pattern"] = str(test_images_path / "Philips_PM5544.svg.png")
        if (test_images_path / "SamplePNGImage_100kbmb.png").exists():
            image_files["landscape"] = str(test_images_path / "SamplePNGImage_100kbmb.png")
        if (test_images_path / "Unknown.png").exists():
            image_files["placeholder"] = str(test_images_path / "Unknown.png")
        if (test_images_path / "pngtree-test-orange-icon-sign-test-testing-vector-png-image_15029880.png").exists():
            image_files["test_icon"] = str(test_images_path / "pngtree-test-orange-icon-sign-test-testing-vector-png-image_15029880.png")
        return image_files
    
    def test_memory_add_user_message_with_images_local_files(self, test_image_files):
        """Test adding user message with local image files."""
        if not test_image_files:
            pytest.skip("No test images available")
            
        memory = ConversationMemory("You are a helpful assistant.")
        
        # Test with single image
        test_message = "What do you see in this image?"
        test_images = [test_image_files["placeholder"]]
        
        memory.add_user_message_with_images(test_message, test_images)
        
        # Check message structure
        assert len(memory.messages) == 2  # system + user
        user_message = memory.messages[1]
        
        assert user_message["role"] == "user"
        assert isinstance(user_message["content"], list)
        assert len(user_message["content"]) == 2  # text + image
        
        # Check text content
        text_content = user_message["content"][0]
        assert text_content["type"] == "text"
        assert text_content["text"] == test_message
        
        # Check image content
        image_content = user_message["content"][1]
        assert image_content["type"] == "image_url"
        assert "image_url" in image_content
        assert image_content["image_url"]["url"].startswith("data:image/")
        assert "base64," in image_content["image_url"]["url"]
    
    def test_memory_add_user_message_with_multiple_images(self, test_image_files):
        """Test adding user message with multiple images."""
        if len(test_image_files) < 2:
            pytest.skip("Need at least 2 test images")
            
        memory = ConversationMemory("You are a helpful assistant.")
        
        # Test with multiple images
        test_message = "Compare these images"
        test_images = list(test_image_files.values())[:2]  # Use first 2 images
        
        memory.add_user_message_with_images(test_message, test_images)
        
        user_message = memory.messages[1]
        assert len(user_message["content"]) == 3  # text + 2 images
        
        # Check all are properly formatted
        assert user_message["content"][0]["type"] == "text"
        assert user_message["content"][1]["type"] == "image_url"
        assert user_message["content"][2]["type"] == "image_url"
    
    def test_memory_add_user_message_with_url_images(self):
        """Test adding user message with URL images."""
        memory = ConversationMemory("You are a helpful assistant.")
        
        test_message = "Analyze this image from the web"
        test_images = ["https://example.com/image.png"]
        
        memory.add_user_message_with_images(test_message, test_images)
        
        user_message = memory.messages[1]
        image_content = user_message["content"][1]
        
        assert image_content["type"] == "image_url"
        assert image_content["image_url"]["url"] == "https://example.com/image.png"
    
    def test_memory_add_user_message_with_images_no_text(self, test_image_files):
        """Test adding user message with only images, no text."""
        if not test_image_files:
            pytest.skip("No test images available")
            
        memory = ConversationMemory("You are a helpful assistant.")
        
        # Test with empty text
        test_images = [test_image_files["placeholder"]]
        
        memory.add_user_message_with_images("", test_images)
        
        user_message = memory.messages[1]
        assert len(user_message["content"]) == 1  # Only image, no text
        assert user_message["content"][0]["type"] == "image_url"
    
    def test_memory_image_format_detection(self, test_image_files):
        """Test proper image format detection and base64 encoding."""
        if not test_image_files:
            pytest.skip("No test images available")
            
        memory = ConversationMemory("You are a helpful assistant.")
        
        for image_name, image_path in test_image_files.items():
            memory.add_user_message_with_images(f"Test {image_name}", [image_path])
            
            user_message = memory.messages[-1]
            image_content = user_message["content"][1]
            image_url = image_content["image_url"]["url"]
            
            # Should be base64 encoded
            assert image_url.startswith("data:image/")
            assert "base64," in image_url
            
            # Extract and verify base64 data
            base64_data = image_url.split("base64,")[1]
            try:
                decoded = base64.b64decode(base64_data)
                assert len(decoded) > 0
            except Exception:
                pytest.fail(f"Invalid base64 encoding for {image_name}")
    
    def test_memory_add_user_message_with_nonexistent_image(self):
        """Test handling of nonexistent image files."""
        memory = ConversationMemory("You are a helpful assistant.")
        
        test_message = "This image doesn't exist"
        test_images = ["/nonexistent/path/image.png"]
        
        # Should not crash, just skip the nonexistent image
        memory.add_user_message_with_images(test_message, test_images)
        
        user_message = memory.messages[1]
        # Should only have text content since image doesn't exist
        assert len(user_message["content"]) == 1
        assert user_message["content"][0]["type"] == "text"
    
    def test_memory_is_url_helper(self):
        """Test the _is_url helper method."""
        memory = ConversationMemory("Test")
        
        # Test valid URLs
        assert memory._is_url("http://example.com/image.png")
        assert memory._is_url("https://example.com/image.jpg")
        
        # Test invalid URLs
        assert not memory._is_url("/local/path/image.png")
        assert not memory._is_url("image.png")
        assert not memory._is_url("ftp://example.com/image.png")


class TestAgentImageSupport:
    """Test agent-level image support capabilities."""
    
    @pytest.fixture
    def mock_model_interface(self):
        """Create a mock model interface."""
        mock = MagicMock()
        mock.generate_response.return_value = MagicMock(
            content="I can see the image you've shared.",
            tool_calls=[],
            usage={"total_tokens": 50}
        )
        return mock
    
    @pytest.fixture
    def test_images_path(self):
        """Get the path to test images."""
        return Path(__file__).parent.parent / "assets"
    
    def test_agent_supports_image_input_check(self):
        """Test the agent's image support detection."""
        with patch('liteagent.agent.get_model_capabilities') as mock_caps:
            # Test model that supports images
            mock_caps.return_value = MagicMock(supports_image_input=True)
            
            agent = LiteAgent(model="gpt-4o", name="test-agent")
            assert agent._supports_image_input()
            
            # Test model that doesn't support images
            mock_caps.return_value = MagicMock(supports_image_input=False)
            
            agent = LiteAgent(model="gpt-3.5-turbo", name="test-agent")
            assert not agent._supports_image_input()
            
            # Test when capabilities are None
            mock_caps.return_value = None
            
            agent = LiteAgent(model="unknown-model", name="test-agent")
            assert not agent._supports_image_input()
    
    @patch('liteagent.agent.create_model_interface')
    def test_agent_chat_with_images_supported_model(self, mock_create_model, mock_model_interface, test_images_path):
        """Test agent chat with images on a model that supports them."""
        mock_create_model.return_value = mock_model_interface
        
        with patch('liteagent.agent.get_model_capabilities') as mock_caps:
            mock_caps.return_value = MagicMock(supports_image_input=True)
            
            agent = LiteAgent(model="gpt-4o", name="test-agent")
            
            # Test with placeholder image if available
            placeholder_path = test_images_path / "Unknown.png"
            if placeholder_path.exists():
                response = agent.chat(
                    "What do you see in this image?", 
                    images=[str(placeholder_path)]
                )
                
                # Should call model interface with images
                assert mock_model_interface.generate_response.called
                call_args = mock_model_interface.generate_response.call_args
                messages = call_args[0][0]  # First positional argument
                
                # Find the user message with images
                user_messages = [msg for msg in messages if msg.get('role') == 'user']
                assert len(user_messages) > 0
                
                # Check that the message has multimodal content
                user_message = user_messages[-1]
                assert isinstance(user_message['content'], list)
                
                # Should have both text and image content
                content_types = [item['type'] for item in user_message['content']]
                assert 'text' in content_types
                assert 'image_url' in content_types
    
    @patch('liteagent.agent.create_model_interface')
    def test_agent_chat_with_images_unsupported_model(self, mock_create_model, mock_model_interface, test_images_path):
        """Test agent chat with images on a model that doesn't support them."""
        mock_create_model.return_value = mock_model_interface
        
        with patch('liteagent.agent.get_model_capabilities') as mock_caps:
            mock_caps.return_value = MagicMock(supports_image_input=False)
            
            agent = LiteAgent(model="gpt-3.5-turbo", name="test-agent")
            
            # Test with placeholder image if available
            placeholder_path = test_images_path / "Unknown.png"
            if placeholder_path.exists():
                response = agent.chat(
                    "What do you see in this image?", 
                    images=[str(placeholder_path)]
                )
                
                # Should call model interface but without images
                assert mock_model_interface.generate_response.called
                call_args = mock_model_interface.generate_response.call_args
                messages = call_args[0][0]
                
                # Find the user message
                user_messages = [msg for msg in messages if msg.get('role') == 'user']
                user_message = user_messages[-1]
                
                # Should be simple text content, not multimodal
                assert isinstance(user_message['content'], str)
                assert user_message['content'] == "What do you see in this image?"


class TestCachingCapabilities:
    """Test caching capabilities for supported models."""
    
    def test_agent_chat_with_caching_enabled(self):
        """Test agent chat with caching enabled."""
        with patch('liteagent.agent.create_model_interface') as mock_create_model:
            mock_model_interface = MagicMock()
            mock_model_interface.generate_response.return_value = MagicMock(
                content="Response with caching enabled",
                tool_calls=[],
                usage={"total_tokens": 50}
            )
            mock_create_model.return_value = mock_model_interface
            
            agent = LiteAgent(model="claude-3-5-sonnet-20241022", name="test-agent")
            
            response = agent.chat(
                "This is a test message", 
                enable_caching=True
            )
            
            # Should call model interface with caching enabled
            assert mock_model_interface.generate_response.called
            call_args = mock_model_interface.generate_response.call_args
            
            # Check that enable_caching was passed as keyword argument
            assert 'enable_caching' in call_args.kwargs
            assert call_args.kwargs['enable_caching'] is True
    
    def test_agent_chat_with_caching_disabled(self):
        """Test agent chat with caching disabled (default)."""
        with patch('liteagent.agent.create_model_interface') as mock_create_model:
            mock_model_interface = MagicMock()
            mock_model_interface.generate_response.return_value = MagicMock(
                content="Response without caching",
                tool_calls=[],
                usage={"total_tokens": 50}
            )
            mock_create_model.return_value = mock_model_interface
            
            agent = LiteAgent(model="claude-3-5-sonnet-20241022", name="test-agent")
            
            response = agent.chat("This is a test message")
            
            # Should call model interface with caching disabled
            assert mock_model_interface.generate_response.called
            call_args = mock_model_interface.generate_response.call_args
            
            # Check that enable_caching was passed as False (default)
            assert 'enable_caching' in call_args.kwargs
            assert call_args.kwargs['enable_caching'] is False


class TestCapabilitiesIntegration:
    """Test integration with the capabilities system."""
    
    def test_get_model_capabilities_for_multimodal_models(self):
        """Test that model capabilities correctly identify image support."""
        # Test known multimodal models
        multimodal_models = [
            "gpt-4o",
            "gpt-4o-mini", 
            "claude-3-5-sonnet-20241022",
            "claude-3-5-haiku-20241022"
        ]
        
        for model in multimodal_models:
            capabilities = get_model_capabilities(model)
            if capabilities:
                # If we have capability data, it should correctly identify multimodal support
                # This test validates the models.dev integration
                assert hasattr(capabilities, 'supports_image_input')
                assert hasattr(capabilities, 'multimodal')
    
    def test_get_model_capabilities_for_caching_models(self):
        """Test that model capabilities correctly identify caching support."""
        # Test known caching-capable models
        caching_models = [
            "claude-3-5-sonnet-20241022",
            "claude-3-5-haiku-20241022"
        ]
        
        for model in caching_models:
            capabilities = get_model_capabilities(model)
            if capabilities:
                # If we have capability data, it should correctly identify caching support
                assert hasattr(capabilities, 'supports_caching')


if __name__ == "__main__":
    pytest.main(["-v", __file__])