import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get the Redis URL from the environment variable
redis_url = str(os.getenv('REDIS_URL'))

## Broker settings.
broker_url = redis_url+'/0'

# List of modules to import when the Celery worker starts.
imports = ('worker.celery_worker',)

## Using the database to store task state and results.
result_backend = redis_url+'/0'

task_annotations = {'tasks.add': {'rate_limit': '5/s'}}

task_queues = {
    'test-queue': {
        'exchange': 'test-queue',
    }
}
task_routes = {
    "worker.celery_worker.long_task": "test-queue",
    "worker.celery_worker.generate_text": "test-queue",
    "worker.celery_worker.generate_image": "test-queue",
}

result_persistent = True
result_expires = 3600 # seconds
task_track_started = True
worker_concurrency = 1
worker_prefetch_multiplier = 2
worker_max_tasks_per_child = 500
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'UTC'
enable_utc = True
worker_pool_restarts=True