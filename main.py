"""
Main entry point for running LiteAgent examples.
"""

from dotenv import load_dotenv
import litellm
import os
import sys
import argparse
from liteagent.utils import setup_logging, logger
from liteagent.observer import ConsoleObserver, FileObserver, TreeTraceObserver

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="LiteAgent - A lightweight agent framework using LiteLLM for LLM interactions",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Model selection
    parser.add_argument("--model", type=str,
                        help="Model to use for the agent (e.g., gpt-3.5-turbo, gpt-4o-mini, ollama/phi4)")
    
    # Example selection
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--class-methods", action="store_true",
                      help="Run only the class methods example")
    group.add_argument("--custom-agents", action="store_true",
                      help="Run only the custom agents example")
    group.add_argument("--all", action="store_true",
                      help="Run all examples (this is the default behavior)")
    
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

def main():
    """Main entry point."""
    # Parse command line arguments
    args = parse_arguments()
    # Check if model parameter is provided
    if not args.model:
        print("--model argument is required")
        sys.exit(1)

    # Show version if requested
    if args.version:
        show_version()
    # Load environment variables from .env file
    load_dotenv()
    if os.environ["LITELLM_VERBOSE"] == "true" or args.debug_litellm:
        litellm._turn_on_debug()

    # Set up logging
    log_level = "DEBUG" if args.debug else "INFO"
    setup_logging(log_level=log_level, log_to_file=args.log_file, use_colors=not args.no_color)
    
    logger.info("Starting LiteAgent")
    logger.info(f"Using model: {args.model}")
    
    # Set drop_params globally if needed
    litellm.drop_params = True
    
    # Enable debug mode for LiteLLM if requested
    if args.debug:
        logger.info("Debug mode enabled")
        litellm._turn_on_debug()
        
        # Automatically prepend 'ollama/' to model name if not already present
        if not args.model.startswith("ollama/"):
            args.model = f"ollama/{args.model}"
            logger.info(f"Updated model name to: {args.model}")
    
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
        from liteagent.examples import run_class_methods_example
        run_class_methods_example(model=args.model, observers=observers)
    elif args.custom_agents:
        logger.info("Running custom agents example")
        from liteagent.examples import run_custom_agents_example
        run_custom_agents_example(model=args.model, observers=observers)
    else:  # Default or --all
        logger.info("Running all examples")
        from liteagent.examples import run_examples
        run_examples(model=args.model, observers=observers)
        
    # Print tree trace if observability is enabled
    if args.enable_observability:
        for observer in observers:
            if isinstance(observer, TreeTraceObserver):
                observer.print_trace()

if __name__ == "__main__":
    main()