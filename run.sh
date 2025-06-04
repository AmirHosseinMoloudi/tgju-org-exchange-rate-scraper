#!/bin/bash

echo "Starting application..."

VENV_DIR="venv"

# Check if virtual environment directory exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Error: Virtual environment directory '$VENV_DIR' not found."
    echo "Please run the setup script first: ./setup.sh"
    exit 1
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"
echo "Virtual environment activated."

# Check if the main script exists in its new location
if [ ! -f "src/tgju/currency_service.py" ]; then
    echo "Error: Main script 'src/tgju/currency_service.py' not found."
    deactivate
    exit 1
fi

# Run the Python script from its new location, ensuring src is in PYTHONPATH
PYTHONPATH=./src:$PYTHONPATH python -B src/tgju/currency_service.py

# Deactivate virtual environment upon script completion (optional, good practice)
# echo "Deactivating virtual environment."
# deactivate
# The deactivate command might not be strictly necessary here as the script will exit,
# and the parent shell's environment is not affected by 'source' in a subshell.
# However, if the script were more complex or interactive, it might be useful.

echo "Application finished."
