#!/bin/bash

# Run script for Fauxmots SMTP Test Server

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the server
python run.py "$@"
