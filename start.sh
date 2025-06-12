#!/bin/bash

# Replit Deployment Script for GC Forms RAG System

echo "Starting GC Forms RAG System..."

# Install required packages if not already installed
pip install -r requirements.txt

# Check for environment variables
if [ -z "$OPENAI_API_KEY" ]; then
  echo "Warning: OPENAI_API_KEY environment variable not set."
  echo "Please set this in the Replit Secrets tab."
fi

# Start the application
python app.py
