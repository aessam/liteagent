"""
Command-line interface functionality for LiteAgent.
Contains the core CLI functions.
"""

import sys
import os
import argparse
import json
from dotenv import load_dotenv
import litellm
from liteagent.utils import setup_logging, logger
from liteagent.observer import ConsoleObserver, FileObserver, TreeTraceObserver
from liteagent.tools import get_function_definitions, FunctionTool, InstanceMethodTool, liteagent_tool
from typing import List, Dict, Any

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="LiteAgent - A lightweight agent framework using LiteLLM for LLM interactions",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # 'run' command for running examples
    run_parser = subparsers.add_parser('run', help='Run examples')
    
    # Example selection for run command
    run_group = run_parser.add_mutually_exclusive_group()
    run_group.add_argument("--class-methods", action="store_true",
                      help="Run only the class methods example")
    run_group.add_argument("--custom-agents", action="store_true",
                      help="Run only the custom agents example")
    run_group.add_argument("--all", action="store_true",
                      help="Run all examples (this is the default behavior)")
    
    # Model selection for run command
    run_parser.add_argument("--model", type=str, default="gpt-3.5-turbo",
                        help="Model to use for the agent (e.g., gpt-3.5-turbo, gpt-4o-mini, ollama/phi4)")
    
    # Ollama helper for run command
    run_parser.add_argument("--ollama", action="store_true",
                        help="Use Ollama for local inference (automatically prepends 'ollama/' to model name if needed)")
    
    # Observability options for run command
    run_parser.add_argument("--enable-observability", action="store_true",
                       help="Enable observability features (console, file, and tree trace observers)")
    
    # 'tools' command for tool operations
    tools_parser = subparsers.add_parser('tools', help='Tool operations')
    tools_parser.add_argument("--sample-output", "-so", action="store_true",
                       help="Print a sample of tool definitions as they would be sent to the LLM")
    
    # Global options that apply to all commands
    parser.add_argument("--version", action="store_true",
                       help="Show version information and exit")
    
    # Debug options (global)
    debug_group = parser.add_argument_group("Debugging options")
    debug_group.add_argument("--debug", action="store_true",
                       help="Enable debug mode with verbose logging")
    debug_group.add_argument("--debug-litellm", action="store_true",
                       help="Enable debug mode with verbose logging for LiteLLM")
    debug_group.add_argument("--log-file", action="store_true",
                       help="Log output to a file in addition to console")
    debug_group.add_argument("--no-color", action="store_true",
                       help="Disable colored log output")
    
    return parser.parse_args()

def show_version():
    """Display version information."""
    # Try to import from relative path first (for package imports)
    try:
        from liteagent import __version__
        print(f"LiteAgent version: {__version__}")
    except (ImportError, ValueError):
        # Try direct import for when called from main.py
        try:
            from liteagent import __version__
            print(f"LiteAgent version: {__version__}")
        except ImportError:
            print("LiteAgent version: unknown")
    
    print("Using LiteLLM for model interactions")
    try:
        import litellm
        print(f"LiteLLM version: {litellm.__version__}")
    except (ImportError, AttributeError):
        print("LiteLLM version: unknown")
    
    sys.exit(0)

def run_examples(args):
    """Run examples based on command line arguments."""
    # Set up observers if enabled
    observers = []
    if args.enable_observability:
        logger.info("Enabling observability features")
        observers.append(ConsoleObserver())
        observers.append(FileObserver('agent_events.jsonl'))
        observers.append(TreeTraceObserver())
        
    # Determine which examples to run
    if args.class_methods:
        logger.info("Running class methods example")
        from examples.basic_examples import run_class_methods_example
        run_class_methods_example(model=args.model, observers=observers)
    elif args.custom_agents:
        logger.info("Running custom agents example")
        from examples.basic_examples import run_custom_agents_example
        run_custom_agents_example(model=args.model, observers=observers)
    else:  # Default or --all
        logger.info("Running all examples")
        from examples.basic_examples import run_examples
        run_examples(model=args.model, observers=observers)
        
    # Print tree trace if observability is enabled
    if args.enable_observability:
        for observer in observers:
            if isinstance(observer, TreeTraceObserver):
                observer.print_trace()

def handle_model_prefix(model_name, use_ollama=False):
    """
    Handle model provider prefixes correctly.
    
    Args:
        model_name: The model name that might include a provider prefix
        use_ollama: Whether to use Ollama for local inference
        
    Returns:
        Correctly formatted model name for use with LiteLLM
    """
    # Common providers that don't need prefixes with LiteLLM
    no_prefix_providers = ['openai', 'anthropic', 'google']
    
    # Providers that need to keep their prefix
    keep_prefix_providers = ['ollama']
    
    # Special case for Groq models - they need the groq/ prefix in litellm
    groq_models = ['llama-3', 'llama-3.1', 'mixtral', 'gemma']
    
    # Check if model has a provider prefix (format: "provider/model")
    if '/' in model_name:
        provider, model = model_name.split('/', 1)
        
        # For providers that don't need prefixes, just return the model part
        if provider.lower() in no_prefix_providers:
            return model
            
        # Groq models keep their prefix
        if provider.lower() == 'groq':
            return model_name
            
        # For other providers that need to keep their prefix, return as is
        if provider.lower() in keep_prefix_providers:
            return model_name
            
        # For unknown providers, log a warning but keep the full name
        logger.warning(f"Unknown provider prefix '{provider}', keeping full model name")
        return model_name
    
    # If no provider prefix but looks like a Groq model, add groq prefix
    for groq_model in groq_models:
        if groq_model in model_name.lower():
            logger.info(f"Model name '{model_name}' looks like a Groq model, adding 'groq/' prefix")
            return f"groq/{model_name}"
    
    # If no provider prefix and --ollama flag is used, add ollama prefix
    if use_ollama:
        return f"ollama/{model_name}"
    
    # No changes needed
    return model_name

def print_sample_tool_definitions():
    """Print sample tool definitions as they would be sent to the LLM."""
    logger.info("Printing sample tool definitions")
    
    # Import the decorator
    from liteagent.tools import liteagent_tool
    
    # Example 1: Basic function tools
    def get_weather(city: str, date: str = "today") -> str:
        """Gets weather forecast for a city.
        
        This function retrieves weather forecast for the specified city.
        For accurate results, provide a valid city name.
        
        Args:
            city: The name of the city to get weather for
            date: The date to get weather for (default: today)
            
        Returns:
            A string containing the weather forecast
        """
        return f"Weather forecast for {city} on {date}"
    
    def calculate(a: float, b: float, operation: str = "add") -> float:
        """Performs calculations on two numbers.
        
        This tool can perform basic arithmetic operations on two numbers.
        
        Args:
            a: First number
            b: Second number
            operation: Operation to perform, one of: add, subtract, multiply, divide
            
        Returns:
            Result of the calculation
        """
        if operation == "add":
            return a + b
        elif operation == "subtract":
            return a - b
        elif operation == "multiply":
            return a * b
        elif operation == "divide":
            return a / b
        else:
            raise ValueError(f"Unknown operation: {operation}")
    
    # Example 2: Function with the @liteagent_tool decorator (basic usage)
    @liteagent_tool
    def search_database(query: str, limit: int = 10, offset: int = 0) -> List[Dict]:
        """Searches the database for the given query.
        
        Performs a search in the system database and returns matching records.
        
        Args:
            query: The search query string
            limit: Maximum number of results to return (default: 10)
            offset: Number of results to skip for pagination (default: 0)
            
        Returns:
            List of matching records
        """
        # This is a mock function for demonstration
        return [{"id": 1, "title": "Sample result"}]
    
    # Example 3: Function with @liteagent_tool decorator with custom name and description
    @liteagent_tool(
        name="find_location",
        description="Find geographic coordinates for a location"
    )
    def get_coordinates(location: str) -> Dict[str, float]:
        """Get the latitude and longitude for a location.
        
        Args:
            location: The name of the location (city, address, landmark)
            
        Returns:
            Dictionary with latitude and longitude
        """
        # Mock implementation
        return {"latitude": 37.7749, "longitude": -122.4194}
    
    # Example 4: Class with methods using decorators
    class ToolsWithDecorators:
        """Class demonstrating tools with decorators."""
        
        @liteagent_tool
        def get_user_profile(self, user_id: str) -> Dict:
            """Get detailed profile information for a user.
            
            Retrieves comprehensive user information including preferences,
            settings, and activity history.
            
            Args:
                user_id: The ID of the user to lookup
                
            Returns:
                Dictionary with user profile information
            """
            return {
                "id": user_id,
                "name": "Sample User",
                "email": "user@example.com",
                "joined": "2023-01-15"
            }
            
        @liteagent_tool(
            name="analyze_text_sentiment",
            description="Analyze the sentiment of a text passage"
        )
        def analyze_sentiment(self, text: str) -> Dict[str, Any]:
            """Analyze the sentiment of a text passage.
            
            Performs sentiment analysis on the provided text and returns
            scores for positive, negative, and neutral sentiment.
            
            Args:
                text: The text to analyze
                
            Returns:
                Dictionary with sentiment scores
            """
            # Mock implementation
            return {
                "positive": 0.65,
                "negative": 0.15,
                "neutral": 0.20,
                "overall": "positive"
            }
    
    # Example 5: Standard class with methods
    class MathTools:
        """Sample class with method tools."""
        
        def add_numbers(self, a: int, b: int) -> int:
            """Adds two numbers together and returns the result.
            
            This is a simple addition operation.
            
            Args:
                a: First number to add
                b: Second number to add
                
            Returns:
                The sum of a and b
            """
            return a + b
            
        def calculate_area(self, shape: str, **kwargs) -> float:
            """Calculate the area of a geometric shape.
            
            This tool calculates the area of various geometric shapes.
            For a circle, provide radius.
            For a rectangle, provide width and height.
            For a triangle, provide base and height.
            
            Args:
                shape: The type of shape (circle, rectangle, triangle)
                **kwargs: Shape-specific parameters
                
            Returns:
                The calculated area
            """
            if shape == "circle":
                if "radius" not in kwargs:
                    raise ValueError("Radius is required for circle")
                return 3.14159 * kwargs["radius"] ** 2
            elif shape == "rectangle":
                if "width" not in kwargs or "height" not in kwargs:
                    raise ValueError("Width and height are required for rectangle")
                return kwargs["width"] * kwargs["height"]
            elif shape == "triangle":
                if "base" not in kwargs or "height" not in kwargs:
                    raise ValueError("Base and height are required for triangle")
                return 0.5 * kwargs["base"] * kwargs["height"]
            else:
                raise ValueError(f"Unknown shape: {shape}")
    
    # Create instances and collect tools
    tools_with_decorators = ToolsWithDecorators()
    math_tools = MathTools()
    
    # Create standard tool objects
    weather_tool = FunctionTool(get_weather)
    calculate_tool = FunctionTool(calculate)
    
    # Create instance method tools
    add_numbers_tool = InstanceMethodTool(math_tools.add_numbers, math_tools)
    calculate_area_tool = InstanceMethodTool(math_tools.calculate_area, math_tools)
    
    # Get function definitions
    # Note: Decorated functions are already wrapped as tools
    function_definitions = get_function_definitions([
        # Standard function tools
        weather_tool,
        calculate_tool,
        
        # Decorated standalone functions
        search_database,
        get_coordinates,
        
        # Instance method tools (regular way)
        add_numbers_tool,
        calculate_area_tool,
        
        # Instance methods with decorators
        tools_with_decorators.get_user_profile,
        tools_with_decorators.analyze_sentiment
    ])
    
    # Print the definitions in a pretty format
    print("\n==== Sample Tool Definitions ====")
    print("These are examples of function definitions that would be sent to the LLM.")
    print("The examples demonstrate different ways to define tools:")
    print("  - Regular functions wrapped with FunctionTool")
    print("  - Functions decorated with @liteagent_tool")
    print("  - Class methods wrapped with InstanceMethodTool")
    print("  - Class methods decorated with @liteagent_tool\n")
    print(json.dumps(function_definitions, indent=2))
    print("\n==== End of Sample Tool Definitions ====\n")
    
    # Return the definitions for potential further use
    return function_definitions

def main():
    """Main entry point."""
    # Parse command line arguments
    args = parse_arguments()

    # Show version if requested (global flag)
    if args.version:
        show_version()
    
    # Set up logging (for all commands)
    log_level = "DEBUG" if hasattr(args, 'debug') and args.debug else "INFO"
    setup_logging(log_level=log_level, 
                  log_to_file=hasattr(args, 'log_file') and args.log_file, 
                  use_colors=not (hasattr(args, 'no_color') and args.no_color))
    
    # Load environment variables
    load_dotenv()
    
    # Process based on the command
    if not hasattr(args, 'command') or args.command is None:
        # No command specified, show help
        print("No command specified. Use --help for usage information.")
        return
        
    # Handle tools command
    if args.command == 'tools':
        if hasattr(args, 'sample_output') and args.sample_output:
            print_sample_tool_definitions()
        else:
            print("No tool operation specified. Use 'tools --help' for usage information.")
        return
            
    # Handle run command
    if args.command == 'run':
        logger.info("Starting LiteAgent")
        
        # Validate model parameter
        if not hasattr(args, 'model') or not args.model:
            print("Error: --model argument is required for the 'run' command")
            print("Use 'run --help' for more information")
            sys.exit(1)
            
        logger.info(f"Using model: {args.model}")
        
        # Set litellm options
        litellm.drop_params = True
        
        # Enable debug mode for LiteLLM if requested
        if hasattr(args, 'debug_litellm') and (args.debug_litellm or (os.environ.get("LITELLM_VERBOSE") == "true")):
            logger.info("LiteLLM debug mode enabled")
            litellm._turn_on_debug()
            
        # Automatically prepend 'ollama/' to model name if requested
        if hasattr(args, 'ollama') and args.ollama and not args.model.startswith("ollama/"):
            args.model = f"ollama/{args.model}"
            logger.info(f"Using Ollama - updated model name to: {args.model}")
        
        # Run examples
        run_examples(args)
        return
        
    # If we get here, command wasn't recognized
    print(f"Unknown command: {args.command}. Use --help for usage information.") 