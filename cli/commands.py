"""
Command-line interface functionality for LiteAgent.
Contains the core CLI functions.
"""

import sys
import os
import argparse
from dotenv import load_dotenv
import litellm
from liteagent.utils import setup_logging, logger
from liteagent.observer import ConsoleObserver, FileObserver, TreeTraceObserver

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="LiteAgent - A lightweight agent framework using LiteLLM for LLM interactions",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Model selection
    parser.add_argument("--model", type=str, default="gpt-3.5-turbo",
                        help="Model to use for the agent (e.g., gpt-3.5-turbo, gpt-4o-mini, ollama/phi4)")
    
    # Example selection
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--class-methods", action="store_true",
                      help="Run only the class methods example")
    group.add_argument("--custom-agents", action="store_true",
                      help="Run only the custom agents example")
    group.add_argument("--all", action="store_true",
                      help="Run all examples (this is the default behavior)")
    
    # Ollama helper
    parser.add_argument("--ollama", action="store_true",
                        help="Use Ollama for local inference (automatically prepends 'ollama/' to model name if needed)")
    
    # Debug options
    debug_group = parser.add_argument_group("Debugging options")
    debug_group.add_argument("--debug", action="store_true",
                       help="Enable debug mode with verbose logging")
    debug_group.add_argument("--debug-litellm", action="store_true",
                       help="Enable debug mode with verbose logging for LiteLLM")
    debug_group.add_argument("--log-file", action="store_true",
                       help="Log output to a file in addition to console")
    debug_group.add_argument("--no-color", action="store_true",
                       help="Disable colored log output")
    
    # Observability options
    observability_group = parser.add_argument_group("Observability options")
    observability_group.add_argument("--enable-observability", action="store_true",
                       help="Enable observability features (console, file, and tree trace observers)")
    
    # Version
    parser.add_argument("--version", action="store_true",
                       help="Show version information and exit")
    
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

def main():
    """Main entry point."""
    # Parse command line arguments
    args = parse_arguments()

    # Show version if requested
    if args.version:
        show_version()
    
    # Check if model parameter is provided
    if not args.model:
        print("Error: --model argument is required")
        print("Use --help for more information")
        sys.exit(1)
        
    # Load environment variables from .env file
    load_dotenv()
    
    # Set up logging
    log_level = "DEBUG" if args.debug else "INFO"
    setup_logging(log_level=log_level, log_to_file=args.log_file, use_colors=not args.no_color)
    
    logger.info("Starting LiteAgent")
    logger.info(f"Using model: {args.model}")
    
    # Set drop_params globally if needed
    litellm.drop_params = True
    
    # Enable debug mode for LiteLLM if requested
    if args.debug_litellm or (os.environ.get("LITELLM_VERBOSE") == "true"):
        logger.info("LiteLLM debug mode enabled")
        litellm._turn_on_debug()
        
    # Automatically prepend 'ollama/' to model name if requested
    if args.ollama and not args.model.startswith("ollama/"):
        args.model = f"ollama/{args.model}"
        logger.info(f"Using Ollama - updated model name to: {args.model}")
    
    # Run examples
    run_examples(args) 