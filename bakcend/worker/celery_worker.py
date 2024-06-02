import asyncio
import os
from celery.utils.log import get_task_logger
from fastapi import requests
import openai
from .celery_app import celery_app

OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")
openai.api_key = OPEN_AI_KEY
logger = get_task_logger(__name__)

@celery_app.task
def long_task(word: str) -> dict:
    logger.info("long_task called")
    asyncio.run(long_async_task())
    return {'result': word}

async def long_async_task():
    for i in range(10):
        await asyncio.sleep(1)

# OPEN AI DEFAULT - generate_text
@celery_app.task
def generate_text(prompt):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=128,
        temperature=0.5
    )
    return response

# OPEN AI DEFAULT - generate_image
@celery_app.task
def generate_image(prompt, number, image_size, image_width):
    response = openai.Image.create(
        prompt=prompt,
        n=number,
        size=str(image_size) + "x" + str(image_width)
    )
    image_url = response['data']
    return image_url