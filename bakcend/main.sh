#!/bin/sh

# Load environment variables from the .env file
eval $(python3 load_env.py)

# Function to check if a port is in use
is_port_in_use() {
  nc -z localhost $1
}

# Ports to check
REDIS_PORT=6379
FLOWER_PORT=5555
UVICORN_PORT=8000

# Check and kill processes using the ports (if needed)
for PORT in $REDIS_PORT $FLOWER_PORT $UVICORN_PORT; do
  if is_port_in_use $PORT; then
    PID=$(lsof -t -i :$PORT)
    if [ ! -z "$PID" ]; then
      kill -9 $PID
      echo "Killed process $PID using port $PORT"
    fi
  fi
done

# Start a Redis container on port 6379. Redis is an in-memory data structure store, often used as a message broker for Celery.
# sudo docker run -p 6379:6379 redis
# set redis -> config set tcp-keepalive 300

# Start a Celery worker with the application defined in 'worker.celery_app'.
# '--loglevel=INFO' sets the logging level to INFO.
# '-E' enables events so that you can monitor the worker.
# celery -A worker.celery_app worker --loglevel=INFO -E &
celery -A worker.celery_app worker -P threads --loglevel=INFO -E &
celery -A worker.celery_app beat & 
sleep 5.0

# Verify worker status
celery -A worker.celery_app status

# Start Flower to monitor the Celery workers.
# '--port=5555' sets the port for the Flower monitoring tool.
celery --broker=$REDIS_URL flower --port=5555 &
# Start a Uvicorn server (port 8000) for an ASGI application defined in 'main:app'.
# '--reload' enables auto-reloading of the server when code changes are detected.
# fastapi docs http://localhost:8000/docs
uvicorn main:app --reload --no-server-header
