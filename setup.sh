#!/bin/bash

# Parse command line arguments for the `--force` flag
FORCE=false
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --force) FORCE=true ;;
        *) echo "[+] Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

# Exit on error
set -e

# Load environment variables from model.env
if [ -f "model.env" ]; then
    source model.env
else
    echo "[+] Error: model.env file not found"
    exit 1
fi

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if conda environment already exists
env_exists() {
    conda env list | grep -q "^doc_qa "
    return $?
}

# Function to check if an Ollama model exists
model_exists() {
    # Extract base model name without version
    MODEL_BASE=$(echo $OLLAMA_MODEL | cut -d':' -f1)
    ollama list | grep -q "$MODEL_BASE"
    return $?
}

# Check if conda is installed
if ! command_exists conda; then
    echo "[+] Conda is not installed. Please install Miniconda or Anaconda first."
    echo "[+] Visit https://docs.conda.io/en/latest/miniconda.html for installation instructions."
    exit 1
fi

# Handle conda environment creation
if [ "$FORCE" = true ]; then
    echo "[+] Force flag detected. Removing existing environment if any..."
    if env_exists; then
        conda remove -n doc_qa --all -y
    fi
    echo "[+] Creating fresh conda environment..."
    conda create -n doc_qa python=3.9 -y
else
    if env_exists; then
        echo "[+] Using existing conda environment 'doc_qa'..."
    else
        echo "[+] Creating new conda environment..."
        conda create -n doc_qa python=3.9 -y
    fi
fi

# Activate conda environment
echo "[+] Activating conda environment..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate doc_qa

# Install the package in development mode
echo "[+] Installing intelli_docs package in development mode..."
pip install -e ".[dev]"

# Install Ollama (if not already installed)
if ! command_exists ollama; then
    echo "[+] Installing Ollama..."
    curl https://ollama.ai/install.sh | sh
fi

# Check if Ollama service is running
if ! curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "[+] Starting Ollama service..."
    ollama serve &
    sleep 5  # Wait for service to start
fi

# Setup Ollama model
echo "[+] Setting up Ollama model..."
if ! model_exists; then
    echo "[+] Pulling $OLLAMA_MODEL model..."
    ollama pull $OLLAMA_MODEL
else
    echo "[+] $OLLAMA_MODEL model already exists, skipped pulling..."
fi

# Create necessary directories
echo "[+] Creating project directories..."
mkdir -p data/raw
mkdir -p data/processed
mkdir -p tests

echo "[+] Setup completed successfully!"
echo "[+] To activate the environment, run: conda activate doc_qa"
echo "[+] To start the application, run: ./start.sh" 