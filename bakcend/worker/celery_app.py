import os
from dotenv import load_dotenv
from celery import Celery

# Load environment variables from the .env file
load_dotenv()

# Get the Redis URL from the environment variable
redis_url = str(os.getenv('REDIS_URL'))

celery_app = Celery(
    "tasks",
    broker=redis_url+"/0",
    backend=redis_url+"/0",
)

celery_app.config_from_object('worker.celeryconfig')
