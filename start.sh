#!/bin/bash

# Load environment variables from model.env
if [ -f "model.env" ]; then
    source model.env
else
    echo "Error: model.env file not found"
    exit 1
fi

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if Python is installed
if ! command_exists python3; then
    echo "Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Check if pip is installed
if ! command_exists pip3; then
    echo "pip3 is not installed. Please install pip3 and try again."
    exit 1
fi

# Activate conda environment
echo "Activating conda environment..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate doc_qa

# Install the package in development mode
echo "Installing intelli_docs package in development mode..."
pip install -e ".[dev]"

# Check if Ollama is installed
if ! command_exists ollama; then
    echo "Ollama is not installed. Please install Ollama and try again."
    echo "Visit https://ollama.ai for installation instructions."
    exit 1
fi

# Check if Ollama service is running
if ! curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "Ollama service is not running. Please start Ollama and try again."
    exit 1
fi

# Extract model name without version for checking
MODEL_BASE=$(echo $OLLAMA_MODEL | cut -d':' -f1)

# Pull the model if not already present
echo "Checking for $OLLAMA_MODEL model..."
if ! ollama list | grep -q "$MODEL_BASE"; then
    echo "Pulling $OLLAMA_MODEL model..."
    ollama pull $OLLAMA_MODEL
else
    echo "$OLLAMA_MODEL model is already present"
fi

# Start the FastAPI server
echo "Starting FastAPI server..."
uvicorn intelli_docs.main:app --reload --host 0.0.0.0 --port 8000 