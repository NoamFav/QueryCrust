#!/bin/bash

SESSION_NAME="querycrust"  # Name of the tmux session

# Start a new tmux session, but do not attach to it (-d)
tmux new-session -d -s $SESSION_NAME

# Split the window vertically and start the Flask backend in the first pane
tmux send-keys -t $SESSION_NAME "cd backend && export FLASK_APP=app.py && export FLASK_ENV=development && python3 app.py" C-m

# Create a new window for the npm frontend
tmux split-window -v -t $SESSION_NAME
tmux send-keys -t $SESSION_NAME "cd frontend && npm start" C-m

# Attach to the session (optional: remove this if you want it to run in the background)
tmux attach-session -t $SESSION_NAME
