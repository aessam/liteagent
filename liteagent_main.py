"""
Main entry point for running LiteAgent examples.
"""

from dotenv import load_dotenv
import litellm
import os
import sys
from liteagent.utils import setup_logging, logger

def main():
    """Main entry point."""
    # Load environment variables from .env file
    load_dotenv()
    
    # Set up logging
    debug_mode = "--debug" in sys.argv
    log_level = "DEBUG" if debug_mode else "INFO"
    log_to_file = "--log-file" in sys.argv
    setup_logging(log_level=log_level, log_to_file=log_to_file)
    
    logger.info("Starting LiteAgent")
    
    # Set drop_params globally if needed
    litellm.drop_params = True
    
    # Enable debug mode for LiteLLM if reuested
    if debug_mode:
        logger.info("Debug mode enabled")
        litellm._turn_on_debug()
        
    # Use Ollama for local inference if specified
    if "--ollama" in sys.argv:
        logger.info("Using Ollama for local inference")
        os.environ["USE_OLLAMA"] = "true"
        
    # Run the examples
    from liteagent.examples import run_examples
    run_examples(model="ollama/phi4")

if __name__ == "__main__":
    main()