from __future__ import annotations
from typing import TYPE_CHECKING

import celery.states
from celery.result import AsyncResult
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from worker.celery_app import celery_app
from worker.celery_worker import long_task, generate_text, generate_image
from pydantic import BaseModel

class Chat(BaseModel):
    prompt: str = "hello AI"

class Image(BaseModel):
  prompt:str = "cat"
  image_size:str = "1024"
  image_width:str = "1024"

if TYPE_CHECKING:
    from celery import Task
    long_task: Task
    generate_text: Task
    generate_image: Task

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/{word}")
async def root(word: str):
    task_name = "worker.celery_worker.long_task"
    # task = long_task.apply_async(args=[word])
    task = celery_app.send_task(task_name, args=[word])
    # background_task.add_task(background_on_message, task)

    return {"task_id": task.id}

@app.get("/api/{task_id}/status")
async def status(task_id: str) -> dict:
    res = AsyncResult(task_id)
    if res.state == celery.states.SUCCESS:
        return {'state': celery.states.SUCCESS,
                'result': res.result}
    return {'state': res.state, }

@app.post('/api/chat')
def chat(prompt: Chat):
  task = generate_text(prompt.prompt)
  # Return task id
  return {"data": task}

@app.post('/api/async/chat')
async def chat(prompt: Chat):
    task_name = "worker.celery_worker.generate_text"
    # prompt = app.request.json.get('prompt')
    task = celery_app.send_task(task_name, args=[prompt.prompt])
    # Return task id
    return {"task_id": task.id}

@app.get("/api/async/chat/{task_id}/status")
async def status(task_id: str) -> dict:
    res = AsyncResult(task_id)
    if res.state == celery.states.SUCCESS:
        return {'state': celery.states.SUCCESS,
                'data': res.result}
    return {'state': res.state}

@app.post('/api/image_chat')
def image_chat(image: Image):
  task = generate_image(image.prompt, image.image_size, image.image_width)
  # Return task id
  return {"data": task}

@app.post('/api/async/image_chat')
async def image_chat(image: Image):
    task_name = "worker.celery_worker.generate_image"
    task = celery_app.send_task(task_name, args=[image.prompt, image.image_size, image.image_width])
    # Return task id
    return {"task_id": task.id}

@app.get("/api/async/image/{task_id}/status")
async def image_result(task_id: str):
    # Get task result
    res = AsyncResult(task_id)
    if res.state == celery.states.SUCCESS:
        return {'state': celery.states.SUCCESS,
                'data': res.result}
    return {'state': res.state}

# RAG

# WebSearch

# AutoGPT

# Assistant

# 