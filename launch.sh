#!/bin/bash

# Function to stop both Flask and npm
cleanup() {
  echo "Stopping Flask and npm..."
  kill $FLASK_PID 2>/dev/null
  kill $NPM_PID 2>/dev/null
  wait $FLASK_PID 2>/dev/null
  wait $NPM_PID 2>/dev/null
}

# Trap SIGINT and SIGTERM for graceful shutdown
trap cleanup SIGINT SIGTERM

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

# Wait for both processes to finish
wait $FLASK_PID
wait $NPM_PID
