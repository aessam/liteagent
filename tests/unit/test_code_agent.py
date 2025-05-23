"""
Tests for code_agent.py
"""

import os
import tempfile
import shutil
from unittest import mock
import pytest

from liteagent.code_agent import LiteCodeAgent


class TestLiteCodeAgent:
    """Test cases for the LiteCodeAgent class."""
    
    def setup_method(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        # Create a test file in the test directory
        with open(os.path.join(self.test_dir, "test_file.txt"), "w") as f:
            f.write("test content")
            
    def teardown_method(self):
        """Clean up test environment."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
            
    def test_init(self):
        """Test initialization of the LiteCodeAgent."""
        # Mock the LiteAgent.__init__ method
        with mock.patch("liteagent.agent.LiteAgent.__init__", return_value=None) as mock_init:
            agent = LiteCodeAgent(
                model="gpt-4",
                name="TestCodeAgent",
                system_prompt="Custom prompt",
                debug=True,
                container_type="docker",
                container_config={"source_directory": self.test_dir}
            )
            
            # Check that LiteAgent.__init__ was called with the right parameters
            mock_init.assert_called_with(
                model="gpt-4",
                name="TestCodeAgent",
                system_prompt="Custom prompt",
                tools=None,
                debug=True,
                drop_params=True,
                parent_context_id=None,
                context_id=None,
                observers=None,
                description=None
            )
            
            # Check that the parameters were set correctly
            assert agent.container_type == "docker"
            assert agent.container_config["source_directory"] == self.test_dir
            assert agent.temp_dir is None  # We provided a source_directory
            
    def test_init_temp_dir(self):
        """Test initialization with a temporary directory."""
        # Mock the LiteAgent.__init__ method
        with mock.patch("liteagent.agent.LiteAgent.__init__", return_value=None) as mock_init:
            agent = LiteCodeAgent(
                model="gpt-4",
                container_type="podman"
            )
            
            # Check that a temporary directory was created
            assert agent.temp_dir is not None
            assert os.path.exists(agent.temp_dir)
            assert agent.container_config["source_directory"] == agent.temp_dir
            
            # Clean up
            agent.cleanup()
            assert not os.path.exists(agent.temp_dir)
            
    def test_extract_code_block(self):
        """Test extracting code from markdown code blocks."""
        agent = LiteCodeAgent(model="gpt-4")
        
        # Test with Python code block
        markdown = """
Here's some code to solve the problem:

```python
def hello():
    print("Hello, world!")
    
hello()
```

This code will print 'Hello, world!'.
"""
        code = agent._extract_code_block(markdown)
        assert code == 'def hello():\n    print("Hello, world!")\n    \nhello()'
        
        # Test with code block without language specifier
        markdown = """
Here's some code:

```
def hello():
    print("Hello, world!")
    
hello()
```

This code will print 'Hello, world!'.
"""
        code = agent._extract_code_block(markdown)
        assert code == 'def hello():\n    print("Hello, world!")\n    \nhello()'
        
        # Test with no code block
        text = 'print("Hello, world!")'
        code = agent._extract_code_block(text)
        assert code == 'print("Hello, world!")'
        
    @mock.patch("liteagent.container_executor.ContainerFactory.create_container")
    def test_execute_code(self, mock_create_container):
        """Test executing code in a container."""
        agent = LiteCodeAgent(
            model="gpt-4",
            container_type="podman",
            container_config={"source_directory": self.test_dir}
        )
        
        # Mock the container executor
        mock_container = mock.MagicMock()
        mock_container.__enter__.return_value = mock_container
        mock_container.execute_code.return_value = (
            {"success": True, "output": "Hello, world!"},
            "Execution log",
            True
        )
        mock_create_container.return_value = mock_container
        
        # Execute code
        result = agent._execute_code('print("Hello, world!")')
        
        # Check that the container was created and the code was executed
        mock_create_container.assert_called_with(
            container_type="podman",
            source_directory=self.test_dir
        )
        mock_container.execute_code.assert_called_with('print("Hello, world!")')
        
        # Check the result
        assert result["success"] is True
        assert result["result"]["success"] is True
        assert result["result"]["output"] == "Hello, world!"
        assert result["logs"] == "Execution log"
        
    @mock.patch("liteagent.container_executor.ContainerFactory.create_container")
    def test_execute_code_error(self, mock_create_container):
        """Test executing code with an error."""
        agent = LiteCodeAgent(
            model="gpt-4",
            container_type="podman",
            container_config={"source_directory": self.test_dir}
        )
        
        # Mock the container executor to raise an exception
        mock_create_container.side_effect = Exception("Test error")
        
        # Execute code
        result = agent._execute_code('print("Hello, world!")')
        
        # Check the result
        assert result["success"] is False
        assert "error" in result["result"]
        assert "Test error" in result["result"]["error"]
        assert "Error executing code" in result["logs"]
        
    def test_cleanup(self):
        """Test cleaning up temporary resources."""
        agent = LiteCodeAgent(model="gpt-4")
        
        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()
        agent.temp_dir = temp_dir
        
        # Cleanup
        agent.cleanup()
        
        # Check that the directory was removed
        assert not os.path.exists(temp_dir)
        assert agent.temp_dir is None
        
    def test_context_manager(self):
        """Test using the LiteCodeAgent as a context manager."""
        with mock.patch("liteagent.code_agent.LiteCodeAgent.cleanup") as mock_cleanup:
            with LiteCodeAgent(model="gpt-4") as agent:
                assert isinstance(agent, LiteCodeAgent)
                
            # Check that cleanup was called
            mock_cleanup.assert_called_once()
            
    def test_chat(self):
        """Test chatting with the agent."""
        # Mock the LiteAgent.chat method
        with mock.patch("liteagent.agent.LiteAgent.chat", return_value="Response") as mock_chat:
            agent = LiteCodeAgent(model="gpt-4")
            result = agent.chat("Hello, can you help me with a Python problem?")
            
            # Check that LiteAgent.chat was called
            mock_chat.assert_called_once_with("Hello, can you help me with a Python problem?")
            assert result == "Response"