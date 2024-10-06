#!/bin/bash

# Navigate to the backend directory and start Flask
echo "Starting Flask backend..."
cd backend
export FLASK_APP=app.py  # Replace with the actual Flask entry point
export FLASK_ENV=development  # Or 'production'
python3 app.py &
FLASK_PID=$!  # Capture Flask process ID

# Navigate to the frontend directory and start npm
echo "Starting npm frontend..."
cd ../frontend
npm start &
NPM_PID=$!  # Capture npm process ID

# Trap the script termination (Ctrl+C) to stop Flask and npm processes
trap "echo 'Stopping Flask and npm...'; kill $FLASK_PID; kill $NPM_PID" SIGINT

# Wait for both processes to finish
wait
