#!/bin/bash

echo "Starting project setup for Linux..."

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for Python 3
if ! command_exists python3; then
    echo "Error: Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi
echo "Python 3 found."

# Check for pip
if ! command_exists pip3; then
    echo "Warning: pip3 not found. Attempting to install dependencies using 'python3 -m pip'."
    PIP_CMD="python3 -m pip"
else
    PIP_CMD="pip3"
fi


# Define virtual environment directory
VENV_DIR="venv"

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating Python virtual environment in '$VENV_DIR'..."
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment."
        exit 1
    fi
else
    echo "Virtual environment '$VENV_DIR' already exists."
fi

# Activate virtual environment and install dependencies
echo "Activating virtual environment and installing dependencies..."
source "$VENV_DIR/bin/activate"

if [ ! -f "requirements.txt" ]; then
    echo "Error: requirements.txt not found. Cannot install dependencies."
    deactivate
    exit 1
fi

$PIP_CMD install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies from requirements.txt."
    deactivate
    exit 1
fi

echo "Dependencies installed successfully."
echo "Setup complete! To activate the virtual environment in your current shell, run: source $VENV_DIR/bin/activate"
echo "You can then run the application using: ./run.sh or python currency_service.py"

# Note: The script activates the venv for installing dependencies,
# but the activation is local to this script's execution.
# The user needs to activate it separately in their shell if they want to run commands manually.
