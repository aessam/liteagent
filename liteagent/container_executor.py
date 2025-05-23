"""
ContainerExecutor - Classes for executing code safely in containers.

This module provides classes for running LLM-generated code in secure containers
using either Docker or Podman.
"""

import os
import tempfile
import json
import shutil
import subprocess
import uuid
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple, Union

from .utils import logger


class ContainerExecutor(ABC):
    """
    Abstract base class for executing code in a container environment.
    
    This class defines the interface for container executors and provides
    common utility methods.
    """
    
    def __init__(self, 
                 source_directory: str,
                 authorized_imports: List[str] = None,
                 memory_limit: str = "1g",
                 timeout: int = 30,
                 network_enabled: bool = False):
        """
        Initialize the container executor.
        
        Args:
            source_directory: Directory to be mounted in the container
            authorized_imports: List of Python packages allowed to be imported
            memory_limit: Memory limit for the container
            timeout: Maximum execution time in seconds
            network_enabled: Whether to allow network access from the container
        """
        self.source_directory = os.path.abspath(source_directory)
        self.authorized_imports = authorized_imports or ["os", "sys", "json", "re", "collections", "datetime"]
        self.memory_limit = memory_limit
        self.timeout = timeout
        self.network_enabled = network_enabled
        self.container_id = None
        self.shadow_dir = None
        
    def create_shadow_copy(self) -> str:
        """
        Create a shadow copy of the source directory to avoid modifying original files.
        
        Returns:
            Path to the shadow directory
        """
        # Create a temporary directory for the shadow copy
        shadow_dir = tempfile.mkdtemp(prefix="liteagent_shadow_")
        
        try:
            # Copy files from source directory to shadow directory
            if os.path.exists(self.source_directory):
                for item in os.listdir(self.source_directory):
                    src_path = os.path.join(self.source_directory, item)
                    dst_path = os.path.join(shadow_dir, item)
                    
                    if os.path.isdir(src_path):
                        shutil.copytree(src_path, dst_path)
                    else:
                        shutil.copy2(src_path, dst_path)
                
            # Save the shadow directory path
            self.shadow_dir = shadow_dir
            return shadow_dir
            
        except Exception as e:
            # Clean up on error
            if os.path.exists(shadow_dir):
                shutil.rmtree(shadow_dir)
            raise ValueError(f"Failed to create shadow copy: {str(e)}")
    
    @abstractmethod
    def prepare_container(self) -> None:
        """Set up the container with necessary dependencies"""
        pass
        
    @abstractmethod
    def execute_code(self, code: str) -> Tuple[Any, str, bool]:
        """
        Execute code in the container and return result, logs, and status.
        
        Args:
            code: Python code to execute
            
        Returns:
            Tuple containing (result, logs, success_status)
        """
        pass
        
    @abstractmethod
    def cleanup(self) -> None:
        """Clean up resources after execution"""
        pass
    
    def __enter__(self):
        """Context manager entry point"""
        if not self.shadow_dir:
            self.create_shadow_copy()
        self.prepare_container()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit point"""
        self.cleanup()


class DockerExecutor(ContainerExecutor):
    """
    Executor for running code in a Docker container.
    """
    
    def __init__(self, 
                 source_directory: str,
                 authorized_imports: List[str] = None,
                 memory_limit: str = "1g",
                 timeout: int = 30,
                 network_enabled: bool = False,
                 image: str = "python:3.9-slim"):
        """
        Initialize the Docker executor.
        
        Args:
            source_directory: Directory to be mounted in the container
            authorized_imports: List of Python packages allowed to be imported
            memory_limit: Memory limit for the container
            timeout: Maximum execution time in seconds
            network_enabled: Whether to allow network access from the container
            image: Docker image to use
        """
        super().__init__(source_directory, authorized_imports, memory_limit, timeout, network_enabled)
        self.image = image
        
    def prepare_container(self) -> None:
        """Set up the Docker container"""
        # Check if Docker is installed
        try:
            subprocess.run(
                ["docker", "--version"], 
                check=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
        except (subprocess.SubprocessError, FileNotFoundError):
            raise RuntimeError("Docker is not installed or not available in PATH")
            
        # Make sure we have a shadow directory
        if not self.shadow_dir:
            self.create_shadow_copy()
            
        # Pull the Docker image if needed
        try:
            subprocess.run(
                ["docker", "image", "inspect", self.image],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        except subprocess.CalledProcessError:
            logger.info(f"Pulling Docker image: {self.image}")
            subprocess.run(
                ["docker", "pull", self.image],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        
    def execute_code(self, code: str) -> Tuple[Any, str, bool]:
        """
        Execute code in the Docker container.
        
        Args:
            code: Python code to execute
            
        Returns:
            Tuple containing (result, logs, success_status)
        """
        if not self.shadow_dir:
            self.create_shadow_copy()
            
        # Write the code to a file in the shadow directory
        code_file = os.path.join(self.shadow_dir, "code_to_execute.py")
        result_file = os.path.join(self.shadow_dir, "execution_result.json")
        
        # Prepare code with authorized imports only
        code_with_restricted_imports = self._prepare_restricted_code(code)
        
        with open(code_file, "w") as f:
            f.write(code_with_restricted_imports)
            
        # Define container parameters
        network_param = [] if self.network_enabled else ["--network", "none"]
        memory_param = ["--memory", self.memory_limit]
        mount_param = ["-v", f"{self.shadow_dir}:/workspace"]
        
        # Run the container with the code
        container_id = str(uuid.uuid4())[:12]
        self.container_id = container_id
        
        try:
            cmd = [
                "docker", "run", "--rm",
                "--name", f"liteagent-{container_id}",
                *memory_param,
                *network_param,
                *mount_param,
                "--workdir", "/workspace",
                self.image,
                "python", "code_to_execute.py"
            ]
            
            # Execute the command with timeout
            process = subprocess.run(
                cmd,
                capture_output=True,
                timeout=self.timeout,
                text=True
            )
            
            logs = process.stdout
            error_logs = process.stderr
            success = process.returncode == 0
            
            if success:
                # Try to load execution results from file if it exists
                if os.path.exists(result_file):
                    with open(result_file, "r") as f:
                        try:
                            result = json.load(f)
                        except json.JSONDecodeError:
                            result = {"output": "Result file not in valid JSON format"}
                else:
                    result = {"output": logs.strip()}
            else:
                result = {"error": error_logs.strip()}
                
            return result, logs + error_logs, success
            
        except subprocess.TimeoutExpired:
            # Kill the container if it's still running
            try:
                subprocess.run(
                    ["docker", "kill", f"liteagent-{container_id}"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            except Exception:
                pass
                
            return (
                {"error": "Execution timed out"},
                f"Code execution timed out after {self.timeout} seconds",
                False
            )
        except Exception as e:
            return (
                {"error": str(e)},
                f"Error while executing code: {str(e)}",
                False
            )
            
    def cleanup(self) -> None:
        """Clean up resources after execution"""
        # Remove the container if it's still running
        if self.container_id:
            try:
                subprocess.run(
                    ["docker", "rm", "-f", f"liteagent-{self.container_id}"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            except Exception:
                pass
            
            self.container_id = None
                
        # Remove the shadow directory
        if self.shadow_dir and os.path.exists(self.shadow_dir):
            shutil.rmtree(self.shadow_dir)
            self.shadow_dir = None
    
    def _prepare_restricted_code(self, code: str) -> str:
        """
        Modify code to only allow authorized imports and capture results.
        
        Args:
            code: Original Python code
            
        Returns:
            Modified Python code with import restrictions and result capturing
        """
        # Prepare wrapper code that captures imports and writes results to file
        wrapper_code = f"""
import sys
import json
import builtins

# Store the original import function
original_import = builtins.__import__

# Define list of authorized modules
AUTHORIZED_IMPORTS = {self.authorized_imports!r}

# Custom import function to restrict imports
def restricted_import(name, *args, **kwargs):
    if name not in AUTHORIZED_IMPORTS:
        raise ImportError(f"Import of '{{name}}' is not allowed in this restricted environment")
    return original_import(name, *args, **kwargs)
    
# Replace the built-in import function
builtins.__import__ = restricted_import

# Capture standard output and errors
from io import StringIO
import contextlib

@contextlib.contextmanager
def capture():
    out, err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = out, err
        yield out, err
    finally:
        sys.stdout, sys.stderr = old_out, old_err

# Execute the user code and capture results
result = {{}}
with capture() as (stdout, stderr):
    try:
        # ===== USER CODE STARTS HERE =====
{code}
        # ===== USER CODE ENDS HERE =====
        result["success"] = True
        result["output"] = stdout.getvalue().strip()
        if stderr.getvalue().strip():
            result["warnings"] = stderr.getvalue().strip()
            
    except Exception as e:
        result["success"] = False
        result["error"] = str(e)
        result["error_type"] = type(e).__name__
        
# Write the results to file
with open("execution_result.json", "w") as f:
    json.dump(result, f, indent=2)
"""
        return wrapper_code


class PodmanExecutor(ContainerExecutor):
    """
    Executor for running code in a Podman container.
    """
    
    def __init__(self, 
                 source_directory: str,
                 authorized_imports: List[str] = None,
                 memory_limit: str = "1g",
                 timeout: int = 30,
                 network_enabled: bool = False,
                 image: str = "python:3.9-slim"):
        """
        Initialize the Podman executor.
        
        Args:
            source_directory: Directory to be mounted in the container
            authorized_imports: List of Python packages allowed to be imported
            memory_limit: Memory limit for the container
            timeout: Maximum execution time in seconds
            network_enabled: Whether to allow network access from the container
            image: Container image to use
        """
        super().__init__(source_directory, authorized_imports, memory_limit, timeout, network_enabled)
        self.image = image
        
    def prepare_container(self) -> None:
        """Set up the Podman container"""
        # Check if Podman is installed
        try:
            subprocess.run(
                ["podman", "--version"], 
                check=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
        except (subprocess.SubprocessError, FileNotFoundError):
            raise RuntimeError("Podman is not installed or not available in PATH")
            
        # Make sure we have a shadow directory
        if not self.shadow_dir:
            self.create_shadow_copy()
            
        # Pull the podman image if needed
        try:
            subprocess.run(
                ["podman", "image", "exists", self.image],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        except subprocess.CalledProcessError:
            logger.info(f"Pulling Podman image: {self.image}")
            subprocess.run(
                ["podman", "pull", self.image],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        
    def execute_code(self, code: str) -> Tuple[Any, str, bool]:
        """
        Execute code in the Podman container.
        
        Args:
            code: Python code to execute
            
        Returns:
            Tuple containing (result, logs, success_status)
        """
        if not self.shadow_dir:
            self.create_shadow_copy()
            
        # Write the code to a file in the shadow directory
        code_file = os.path.join(self.shadow_dir, "code_to_execute.py")
        result_file = os.path.join(self.shadow_dir, "execution_result.json")
        
        # Prepare code with authorized imports only
        code_with_restricted_imports = self._prepare_restricted_code(code)
        
        with open(code_file, "w") as f:
            f.write(code_with_restricted_imports)
            
        # Define container parameters
        network_param = [] if self.network_enabled else ["--network", "none"]
        memory_param = ["--memory", self.memory_limit]
        mount_param = ["-v", f"{self.shadow_dir}:/workspace:Z"]
        
        # Run the container with the code
        container_id = str(uuid.uuid4())[:12]
        self.container_id = container_id
        
        try:
            cmd = [
                "podman", "run", "--rm",
                "--name", f"liteagent-{container_id}",
                *memory_param,
                *network_param,
                *mount_param,
                "--workdir", "/workspace",
                self.image,
                "python", "code_to_execute.py"
            ]
            
            # Execute the command with timeout
            process = subprocess.run(
                cmd,
                capture_output=True,
                timeout=self.timeout,
                text=True
            )
            
            logs = process.stdout
            error_logs = process.stderr
            success = process.returncode == 0
            
            if success:
                # Try to load execution results from file if it exists
                if os.path.exists(result_file):
                    with open(result_file, "r") as f:
                        try:
                            result = json.load(f)
                        except json.JSONDecodeError:
                            result = {"output": "Result file not in valid JSON format"}
                else:
                    result = {"output": logs.strip()}
            else:
                result = {"error": error_logs.strip()}
                
            return result, logs + error_logs, success
            
        except subprocess.TimeoutExpired:
            # Kill the container if it's still running
            try:
                subprocess.run(
                    ["podman", "kill", f"liteagent-{container_id}"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            except Exception:
                pass
                
            return (
                {"error": "Execution timed out"},
                f"Code execution timed out after {self.timeout} seconds",
                False
            )
        except Exception as e:
            return (
                {"error": str(e)},
                f"Error while executing code: {str(e)}",
                False
            )
            
    def cleanup(self) -> None:
        """Clean up resources after execution"""
        # Remove the container if it's still running
        if self.container_id:
            try:
                subprocess.run(
                    ["podman", "rm", "-f", f"liteagent-{self.container_id}"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            except Exception:
                pass
            
            self.container_id = None
                
        # Remove the shadow directory
        if self.shadow_dir and os.path.exists(self.shadow_dir):
            shutil.rmtree(self.shadow_dir)
            self.shadow_dir = None
    
    def _prepare_restricted_code(self, code: str) -> str:
        """
        Modify code to only allow authorized imports and capture results.
        
        Args:
            code: Original Python code
            
        Returns:
            Modified Python code with import restrictions and result capturing
        """
        # Prepare wrapper code that captures imports and writes results to file
        wrapper_code = f"""
import sys
import json
import builtins

# Store the original import function
original_import = builtins.__import__

# Define list of authorized modules
AUTHORIZED_IMPORTS = {self.authorized_imports!r}

# Custom import function to restrict imports
def restricted_import(name, *args, **kwargs):
    if name not in AUTHORIZED_IMPORTS:
        raise ImportError(f"Import of '{{name}}' is not allowed in this restricted environment")
    return original_import(name, *args, **kwargs)
    
# Replace the built-in import function
builtins.__import__ = restricted_import

# Capture standard output and errors
from io import StringIO
import contextlib

@contextlib.contextmanager
def capture():
    out, err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = out, err
        yield out, err
    finally:
        sys.stdout, sys.stderr = old_out, old_err

# Execute the user code and capture results
result = {{}}
with capture() as (stdout, stderr):
    try:
        # ===== USER CODE STARTS HERE =====
{code}
        # ===== USER CODE ENDS HERE =====
        result["success"] = True
        result["output"] = stdout.getvalue().strip()
        if stderr.getvalue().strip():
            result["warnings"] = stderr.getvalue().strip()
            
    except Exception as e:
        result["success"] = False
        result["error"] = str(e)
        result["error_type"] = type(e).__name__
        
# Write the results to file
with open("execution_result.json", "w") as f:
    json.dump(result, f, indent=2)
"""
        return wrapper_code


class ContainerFactory:
    """Factory for creating secure container environments with standardized configurations"""
    
    @staticmethod
    def create_container(container_type: str = "podman", 
                        template: str = "default", 
                        **custom_config) -> ContainerExecutor:
        """
        Create a container with a predefined template and optional custom configurations.
        
        Args:
            container_type: "docker" or "podman"
            template: Predefined template ("default", "secure", "ml", "web", etc.)
            **custom_config: Custom configurations to override template defaults
            
        Returns:
            Configured ContainerExecutor instance
        """
        # Templates provide sensible defaults for different use cases
        templates = {
            "default": {
                "memory_limit": "1g",
                "timeout": 30,
                "network_enabled": False,
                "authorized_imports": ["os", "sys", "json", "re", "collections", "datetime"],
                "image": "python:3.9-slim"
            },
            "secure": {
                "memory_limit": "512m",
                "timeout": 15,
                "network_enabled": False,
                "authorized_imports": ["json", "re", "collections"],
                "image": "python:3.9-slim"
            },
            "ml": {
                "memory_limit": "4g",
                "timeout": 120,
                "network_enabled": False,
                "authorized_imports": ["numpy", "pandas", "sklearn", "matplotlib"],
                "image": "python:3.9-slim"
            },
            "web": {
                "memory_limit": "2g",
                "timeout": 60,
                "network_enabled": True,
                "authorized_imports": ["os", "sys", "json", "requests", "flask", "fastapi"],
                "image": "python:3.9-slim"
            }
        }
        
        # Get base configuration from template
        config = templates.get(template, templates["default"]).copy()
        
        # Override with custom configurations
        config.update(custom_config)
        
        # Create and return the executor
        if container_type.lower() == "docker":
            return DockerExecutor(**config)
        elif container_type.lower() == "podman":
            return PodmanExecutor(**config)
        else:
            raise ValueError(f"Unsupported container type: {container_type}")