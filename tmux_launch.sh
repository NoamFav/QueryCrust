#!/bin/bash

SESSION_NAME="querycrust"

tmux new-session -d -s $SESSION_NAME

tmux send-keys -t $SESSION_NAME "cd backend && export FLASK_APP=app.py && export FLASK_ENV=development && python3 app.py" C-m

tmux split-window -v -t $SESSION_NAME
tmux send-keys -t $SESSION_NAME "cd frontend && npm start" C-m

tmux attach-session -t $SESSION_NAME
