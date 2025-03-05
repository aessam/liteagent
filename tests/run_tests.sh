#!/bin/bash

# Navigate to the project root (assuming this script is in the tests directory)
cd "$(dirname "$0")/.."

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "Error: pytest is not installed. Please install it first:"
    echo "pip install -r tests/requirements-test.txt"
    exit 1
fi

# Load environment variables from .env file if it exists
if [ -f .env ]; then
    echo "Loading environment variables from .env file..."
    # Export environment variables from .env file
    export $(grep -v '^#' .env | xargs)
else
    echo "Warning: .env file not found. Make sure API keys are set in your environment."
fi

# Parse arguments
RUN_INTEGRATION=false
RUN_UNIT=true

# Process command-line arguments
for arg in "$@"; do
    case $arg in
        --integration)
            RUN_INTEGRATION=true
            ;;
        --unit-only)
            RUN_INTEGRATION=false
            ;;
        --all)
            RUN_INTEGRATION=true
            ;;
        *)
            # Unknown option
            ;;
    esac
done

# Run the unit tests with coverage
if [ "$RUN_UNIT" = true ]; then
    echo "Running unit tests with coverage..."
    python -m pytest tests/unit --cov=liteagent --cov-report=term --cov-report=html:tests/coverage
    UNIT_EXIT_CODE=${PIPESTATUS[0]}
else
    UNIT_EXIT_CODE=0
fi

# Run integration tests if requested
if [ "$RUN_INTEGRATION" = true ]; then
    echo -e "\nRunning integration tests..."
    echo "Note: Integration tests require API keys and may take longer to run."
    echo "      They are marked with @pytest.mark.integration and @pytest.mark.slow."
    
    # Ask for confirmation
    read -p "Do you want to continue with integration tests? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python -m pytest tests/integration -v
        INTEGRATION_EXIT_CODE=${PIPESTATUS[0]}
    else
        echo "Skipping integration tests."
        INTEGRATION_EXIT_CODE=0
    fi
else
    INTEGRATION_EXIT_CODE=0
fi

# Show the coverage report summary
if [ "$RUN_UNIT" = true ]; then
    echo -e "\nCoverage Report Summary:"
    coverage report
    
    echo -e "\nHTML coverage report generated at: tests/coverage/index.html"
fi

# Print usage information
echo -e "\nUsage:"
echo "  ./tests/run_tests.sh            # Run unit tests only"
echo "  ./tests/run_tests.sh --integration  # Run unit tests followed by integration tests"
echo "  ./tests/run_tests.sh --all      # Run all tests (unit and integration)"

# Exit with a non-zero status if any test suite failed
if [ $UNIT_EXIT_CODE -ne 0 ] || [ $INTEGRATION_EXIT_CODE -ne 0 ]; then
    exit 1
else
    exit 0
fi 