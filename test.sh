#!/bin/bash

# Function to check if Ollama is running
check_ollama_running() {
    if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
        echo "[+] Ollama is running"
        return 0
    else
        echo "[+] Ollama is not running"
        return 1
    fi
}

# Function to start Ollama
start_ollama() {
    echo "[+] Starting Ollama..."
    ollama serve &
    OLLAMA_PID=$!
    
    # Wait for Ollama to start
    echo "[+] Waiting for Ollama to start..."
    for i in {1..30}; do
        if check_ollama_running; then
            echo "[+] Ollama started successfully"
            return 0
        fi
        echo "[+] Attempt $i: Waiting for Ollama to start..."
        sleep 1
    done
    
    echo "[+] Failed to start Ollama"
    return 1
}

# Function to check if FastAPI server is running
check_fastapi_running() {
    if curl -s http://localhost:8000/ >/dev/null 2>&1; then
        echo "[+] FastAPI server is running"
        return 0
    else
        echo "[+] FastAPI server is not running"
        return 1
    fi
}

# Function to start FastAPI server
start_fastapi() {
    echo "[+] Starting FastAPI server..."
    uvicorn intelli_docs.main:app --reload &
    FASTAPI_PID=$!
    
    # Wait for the server to start
    echo "[+] Waiting for FastAPI server to start..."
    for i in {1..30}; do
        if check_fastapi_running; then
            echo "[+] FastAPI server started successfully"
            return 0
        fi
        echo "[+] Attempt $i: Waiting for FastAPI server to start..."
        sleep 1
    done
    
    echo "[+] Failed to start FastAPI server"
    return 1
}

# Cleanup function
cleanup() {
    echo "[+] Cleaning up..."
    if [ ! -z "$FASTAPI_PID" ]; then
        kill $FASTAPI_PID 2>/dev/null || true
    fi
    if [ ! -z "$OLLAMA_PID" ]; then
        kill $OLLAMA_PID 2>/dev/null || true
    fi
    pkill -f "ollama serve" 2>/dev/null || true
}

# Set up trap for cleanup
trap cleanup EXIT

# Main process
echo "[+] Checking Ollama..."
if ! check_ollama_running; then
    if ! start_ollama; then
        echo "[+] Failed to start Ollama. Exiting..."
        exit 1
    fi
fi

# Start FastAPI server
if ! start_fastapi; then
    echo "[+] Failed to start FastAPI server. Exiting..."
    exit 1
fi

# Run the tests
echo "[+] Running tests..."
python test_api.py

echo "[+] Test complete!"