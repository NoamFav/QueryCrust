#!/bin/bash

cleanup() {
  echo "Stopping Flask and npm..."
  kill $FLASK_PID 2>/dev/null
  kill $NPM_PID 2>/dev/null
  wait $FLASK_PID 2>/dev/null
  wait $NPM_PID 2>/dev/null
}

trap cleanup SIGINT SIGTERM

echo "Starting Flask backend..."
cd backend
python3 app.py &
FLASK_PID=$! 

echo "Starting npm frontend..."
cd ../frontend
npm start &
NPM_PID=$! 

wait $FLASK_PID
wait $NPM_PID
