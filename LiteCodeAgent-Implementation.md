# LiteCodeAgent Implementation Plan

## Overview

This document outlines the implementation plan for `LiteCodeAgent`, a secure code-executing agent for the liteagent framework that will allow LLMs to write and execute Python code within secure containerized environments.

## Background

The `LiteCodeAgent` builds on the concept of code-based agents introduced by smolagents' `CodeAgent`, but with a strict focus on containerized execution for security. This approach enables the agent to execute code without exposing the host system to potential risks while working with real files through a shadow copy mechanism.

## Core Design Principles

1. **Security First**: All code execution happens in isolated containers
2. **Shadow Copy**: Developer files are protected by working with copies
3. **Controlled Environment**: Limited resources and restrictive permissions
4. **LiteLLM Integration**: Seamless compatibility with the existing liteagent framework

## Implementation Tasks

### 1. Container Execution Environment

#### 1.1 ContainerExecutor Class
- [ ] Implement base `ContainerExecutor` class 
- [ ] Add Docker container creation and management
- [ ] Add Podman support as an alternative
- [ ] Implement shadow directory copying mechanism
- [ ] Create result serialization methods
- [ ] Add logging and error handling

#### 1.2 Container Security Features
- [ ] Implement memory and CPU limits
- [ ] Configure network access controls
- [ ] Set up execution timeouts
- [ ] Configure read-only filesystem mounts
- [ ] Add container cleanup mechanisms

### 2. LiteCodeAgent Implementation

#### 2.1 Core Agent Class
- [ ] Create `LiteCodeAgent` class extending `LiteAgent`
- [ ] Implement initialization with container configuration
- [ ] Create code-specific system prompts
- [ ] Adapt tools for code-based execution

#### 2.2 Code Handling Features
- [ ] Implement code block extraction from LLM responses
- [ ] Create code validation and preparation methods
- [ ] Implement tool-to-Python-code conversion
- [ ] Add final answer detection in code

#### 2.3 Agent-Container Integration
- [ ] Create execution flow from LLM to container
- [ ] Implement result handling and parsing
- [ ] Add state preservation between executions
- [ ] Create error recovery mechanisms

### 3. Tool Integration

#### 3.1 Tool Representation
- [ ] Design Python code representation of tools
- [ ] Implement tool function wrapper generation
- [ ] Add mechanism to expose tools in container
- [ ] Create helper functions for tool execution

#### 3.2 Tool Result Handling
- [ ] Implement serialization of tool results
- [ ] Create verification mechanisms for outputs
- [ ] Add container-to-agent result passing
- [ ] Implement graceful failure handling

### 4. User Interface and Configuration

#### 4.1 User Configuration
- [ ] Create configuration schema for containers
- [ ] Implement directory specification interface
- [ ] Add authorized imports configuration
- [ ] Create resource limit specifications

#### 4.2 Feedback and Monitoring
- [ ] Implement execution logging
- [ ] Add progress indicators
- [ ] Create summary reports of execution
- [ ] Implement diff generation for file changes

### 5. Documentation and Examples

#### 5.1 Developer Documentation
- [ ] Create API documentation
- [ ] Write security best practices
- [ ] Document configuration options
- [ ] Create troubleshooting guide

#### 5.2 Examples and Templates
- [ ] Create basic usage examples
- [ ] Implement advanced use cases
- [ ] Create template configurations
- [ ] Add example prompts for different models

## Technical Specifications

### Container Executor Specification

```python
class ContainerExecutor:
    """Executor for running LLM-generated Python code in a secure container environment"""
    
    def __init__(self, 
                 source_directory: str,
                 authorized_imports: List[str] = None,
                 container_type: str = "docker",  # Alternatives: "podman"
                 memory_limit: str = "1g",
                 timeout: int = 30,
                 network_enabled: bool = False):
        """
        Initialize the container executor.
        
        Args:
            source_directory: Directory to be mounted in the container
            authorized_imports: List of Python packages allowed to be imported
            container_type: Type of container technology to use
            memory_limit: Memory limit for the container
            timeout: Maximum execution time in seconds
            network_enabled: Whether to allow network access from the container
        """
        pass
        
    def create_shadow_copy(self, src_dir: str) -> str:
        """Create a shadow copy of the source directory"""
        pass
        
    def prepare_container(self) -> None:
        """Set up the container with necessary dependencies"""
        pass
        
    def execute_code(self, code: str) -> Tuple[Any, str, bool]:
        """Execute code in the container and return result, logs, and final status"""
        pass
        
    def cleanup(self) -> None:
        """Clean up resources after execution"""
        pass
```

### Standardized Container Creation

To simplify container creation and ensure consistent security, we'll implement a standardized configuration approach:

```python
class ContainerFactory:
    """Factory for creating secure container environments with standardized configurations"""
    
    @staticmethod
    def create_container(container_type: str, template: str = "default", **custom_config) -> ContainerExecutor:
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
                "authorized_imports": ["os", "sys", "json", "re", "collections", "datetime"]
            },
            "secure": {
                "memory_limit": "512m",
                "timeout": 15,
                "network_enabled": False,
                "authorized_imports": ["json", "re", "collections"]
            },
            "ml": {
                "memory_limit": "4g",
                "timeout": 120,
                "network_enabled": False,
                "authorized_imports": ["numpy", "pandas", "sklearn", "matplotlib"]
            },
            # Add more templates as needed
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
```

### LiteCodeAgent Specification

```python
class LiteCodeAgent(LiteAgent):
    """
    A lightweight agent that generates and executes Python code actions in a secure container.
    """
    
    def __init__(self, 
                 model, 
                 name, 
                 work_directory: str,
                 system_prompt=None, 
                 tools=None, 
                 debug=False,
                 authorized_imports: List[str] = None,
                 container_config: Dict = None,
                 **kwargs):
        """
        Initialize the LiteCodeAgent.
        
        Args:
            model: The LLM model to use
            name: Name of the agent
            work_directory: Directory to be mounted in the container
            system_prompt: System prompt to use (will be modified for code generation)
            tools: List of tool functions to use
            debug: Whether to print debug information
            authorized_imports: List of Python packages allowed to be imported
            container_config: Additional configuration for the container executor
            **kwargs: Additional arguments passed to LiteAgent
        """
        pass
        
    def _build_code_system_prompt(self) -> str:
        """Generate a system prompt that encourages code-based responses"""
        pass
        
    def _parse_code_blocks(self, response_text: str) -> List[str]:
        """Extract Python code blocks from LLM response"""
        pass
        
    def _prepare_tool_code(self) -> str:
        """Generate Python code representations of available tools"""
        pass
        
    def _execute_code_action(self, code: str) -> Tuple[Any, str, bool]:
        """Execute code in the container and determine if it's a final answer"""
        pass
        
    def process_model_response(self, response, user_query):
        """Process the model's response, looking for code blocks instead of function calls"""
        pass
```

## Security Considerations

### Container Isolation
The primary security mechanism is container isolation, which prevents the executed code from accessing the host system directly.

### Shadow Copy Mechanism
By creating a shadow copy of the source directory:
1. Original files are never modified directly
2. Changes can be reviewed before being applied back
3. Malicious file operations are contained

### Resource Limitations
Containers will have strict resource limitations:
- Memory caps to prevent memory exhaustion
- CPU limits to prevent excessive usage
- Execution timeouts to prevent infinite loops
- Disk space quotas to prevent storage attacks

### Network Isolation
By default, containers will have no network access, preventing:
- Data exfiltration
- API abuse
- Network scanning
- External resource access

## Example Implementations

### 1. Digger Agent

The Digger agent uses Python and Bash to search through codebases, documentation, and data to find answers to user questions.

#### Implementation

```python
from liteagent import LiteCodeAgent, tool

class DiggerAgent(LiteCodeAgent):
    """An agent specialized in finding and extracting information from codebases and data sources"""
    
    def __init__(self, model, work_directory, **kwargs):
        # Configure with file access tools and search capabilities
        tools = [
            self.search_files,
            self.grep_code,
            self.analyze_file,
            self.run_bash_command,
            self.summarize_findings
        ]
        
        super().__init__(
            model=model,
            name="Digger",
            work_directory=work_directory,
            tools=tools,
            container_config={
                "template": "secure",
                "authorized_imports": ["os", "re", "json", "subprocess", "glob", "fnmatch"]
            },
            **kwargs
        )
    
    @tool
    def search_files(self, pattern: str, directory: str = ".") -> List[str]:
        """Search for files matching a pattern in the given directory"""
        pass
    
    @tool
    def grep_code(self, pattern: str, file_pattern: str = "*") -> Dict[str, List[str]]:
        """Search for a regex pattern across files matching file_pattern"""
        pass
    
    @tool
    def analyze_file(self, filepath: str) -> Dict[str, Any]:
        """Analyze a file and return statistics and key information"""
        pass
    
    @tool
    def run_bash_command(self, command: str) -> str:
        """Run a bash command and return its output"""
        pass
    
    @tool
    def summarize_findings(self, findings: Dict[str, Any]) -> str:
        """Summarize the findings in a human-readable format"""
        pass
```

#### Command Line Usage

```bash
# Find all deprecated API usages in a codebase
liteagent digger "Find all instances of deprecated API calls in our code base and suggest modern alternatives" --dir ./my-project

# Analyze test coverage and identify untested functions
liteagent digger "Analyze our test coverage and identify the top 10 most complex functions that lack tests" --dir ./src

# Find security vulnerabilities in dependencies
liteagent digger "Check our npm dependencies for known security vulnerabilities and suggest fixes" --dir ./node-project
```

### 2. CodeMod Agent

The CodeMod agent specializes in making bulk changes across codebases, finding and replacing patterns while maintaining code integrity.

#### Implementation

```python
from liteagent import LiteCodeAgent, tool

class CodeModAgent(LiteCodeAgent):
    """An agent specialized in making bulk modifications to codebases"""
    
    def __init__(self, model, work_directory, **kwargs):
        # Configure with code modification tools
        tools = [
            self.find_pattern,
            self.generate_replacement,
            self.preview_changes,
            self.apply_changes,
            self.verify_compilation,
            self.run_tests
        ]
        
        super().__init__(
            model=model,
            name="CodeMod",
            work_directory=work_directory,
            tools=tools,
            container_config={
                "template": "default",
                "authorized_imports": ["os", "re", "ast", "glob", "fnmatch", "difflib"]
            },
            **kwargs
        )
    
    @tool
    def find_pattern(self, pattern: str, file_pattern: str = "*.py") -> Dict[str, List[Tuple[int, str]]]:
        """Find all instances of a code pattern in files matching file_pattern"""
        pass
    
    @tool
    def generate_replacement(self, original_code: str, context: Dict[str, Any]) -> str:
        """Generate a replacement for the given code pattern"""
        pass
    
    @tool
    def preview_changes(self, changes: Dict[str, Dict[int, str]]) -> str:
        """Generate a diff of the proposed changes"""
        pass
    
    @tool
    def apply_changes(self, changes: Dict[str, Dict[int, str]], confirmed: bool = False) -> str:
        """Apply the changes to the shadow copy (only applies to original if confirmed=True)"""
        pass
    
    @tool
    def verify_compilation(self, files: List[str] = None) -> bool:
        """Verify that the modified code still compiles/parses correctly"""
        pass
    
    @tool
    def run_tests(self, test_path: str = None) -> Dict[str, Any]:
        """Run tests to verify changes don't break functionality"""
        pass
```

#### Command Line Usage

```bash
# Upgrade library usage across codebase
liteagent codemod "Update all instances of jQuery 2.x API calls to jQuery 3.x compatible versions" --dir ./web-app

# Refactor code to use newer language features
liteagent codemod "Refactor all traditional JavaScript functions to use arrow functions where appropriate" --dir ./js-src

# Apply consistent code style
liteagent codemod "Standardize error handling patterns across the codebase to use our custom ErrorHandler class" --dir ./src
```

### 3. Ten Example Agent Use Cases

1. **API Migration Assistant**
   ```bash
   liteagent codemod "Migrate our code from the Twitter API v1 to v2, updating all endpoints and response handling" --dir ./twitter-client
   ```

2. **Database Query Optimizer**
   ```bash
   liteagent digger "Find all SQL queries in our codebase and suggest optimizations for the slow ones" --dir ./backend
   ```

3. **Accessibility Compliance Checker**
   ```bash
   liteagent digger "Scan our web components for accessibility issues and suggest fixes to meet WCAG AA standards" --dir ./frontend
   ```

4. **Code Deprecation Handler**
   ```bash
   liteagent codemod "Find and update all usages of our deprecated internal APIs according to our migration guide" --dir ./sdk
   ```

5. **Documentation Generator**
   ```bash
   liteagent digger "Analyze our codebase and generate comprehensive markdown documentation for all public APIs" --dir ./lib
   ```

6. **Test Coverage Enhancer**
   ```bash
   liteagent codemod "Generate unit tests for all public methods in our services directory that currently lack tests" --dir ./src
   ```

7. **Security Vulnerability Patcher**
   ```bash
   liteagent codemod "Find all instances of potential SQL injection vulnerabilities and apply parameterized queries" --dir ./app
   ```

8. **Performance Profiler**
   ```bash
   liteagent digger "Identify CPU-intensive operations in our codebase and suggest performance optimizations" --dir ./core
   ```

9. **Internationalization Helper**
   ```bash
   liteagent codemod "Extract all hardcoded user-facing strings into our i18n translation system" --dir ./ui
   ```

10. **Code Standardization Tool**
    ```bash
    liteagent codemod "Refactor our error handling to use the new Result<T, E> pattern across all services" --dir ./api
    ```

## Future Enhancements

### Differential Execution
A potential enhancement would be to implement "differential execution" that:
1. Tracks all file changes made by the code
2. Generates a comprehensive diff of modifications
3. Allows the user to selectively apply changes back to the original directory
4. Provides visual diffs for each modified file

### Multi-Stage Execution
For complex tasks, implement a multi-stage execution pipeline:
1. Planning stage (container with no file access)
2. Read-only stage (container with read-only access)
3. Execution stage (container with controlled write access)
4. Review stage (diff generation and user approval)

### Enhanced Tool Security
Implement fine-grained permissions for individual tools:
1. Tool-specific network access rules
2. Resource limits per tool
3. File access controls based on tool purpose

### Integration with External Security Tools
Add support for:
1. Static code analysis before execution
2. Runtime sandboxing technologies like gVisor
3. Container vulnerability scanning

## Conclusion

The `LiteCodeAgent` implementation will provide a secure way to leverage the power of code-generating LLMs within the liteagent framework. By focusing on containerized execution and shadow copies, we can balance the flexibility of code-based agents with the security needs of real-world applications. The specialized implementations like Digger and CodeMod agents demonstrate the practical applications of this approach for real-world development tasks. 