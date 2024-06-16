#!/bin/bash

# Generate the page
echo "Running src/main.py..."
python src/main.py  

# Small delay to ensure the server starts before requests are made
sleep 2

# Start the server
echo "Starting server..."
python server.py --dir public