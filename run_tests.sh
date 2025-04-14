#!/bin/bash

# Run all tests for the Fauxmots project
echo "Running tests for Fauxmots SMTP Test Server..."

# Check if pytest is installed
if ! python -c "import pytest" &> /dev/null; then
    echo "pytest is required but not installed. Installing..."
    pip install pytest pytest-cov
fi

# Run tests with coverage report
python -m pytest tests/ -v --cov=app --cov-report=term-missing

# Exit with pytest's exit code
exit $?
