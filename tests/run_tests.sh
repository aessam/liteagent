#!/bin/bash

# Navigate to the project root (assuming this script is in the tests directory)
cd "$(dirname "$0")/.."

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "Error: pytest is not installed. Please install it first:"
    echo "pip install -r tests/requirements-test.txt"
    exit 1
fi

# Run the tests with coverage
echo "Running tests with coverage..."
python -m pytest tests/unit --cov=liteagent --cov-report=term --cov-report=html:tests/coverage

# Show the coverage report summary
echo -e "\nCoverage Report Summary:"
coverage report

# Open the HTML coverage report if running on macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo -e "\nOpening HTML coverage report..."
    open tests/coverage/index.html
else
    echo -e "\nHTML coverage report generated at: tests/coverage/index.html"
fi

# Exit with the status of the tests
exit ${PIPESTATUS[0]} 