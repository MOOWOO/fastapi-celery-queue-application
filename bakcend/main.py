from __future__ import annotations
from typing import TYPE_CHECKING

import celery.states
from celery.result import AsyncResult
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from worker.celery_app import celery_app
from worker.celery_worker import long_task, generate_text, generate_image

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
def chat(prompt: str = "Hello ai"):
  task = generate_text(prompt)
  # Return task id
  return {"result": task}

@app.post('/api/async/chat')
async def chat(prompt: str = "Hello ai"):
    task_name = "worker.celery_worker.generate_text"
    # prompt = app.request.json.get('prompt')
    task = celery_app.send_task(task_name, args=[prompt])
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
def image_chat(prompt:str = "cat", image_size:str = "1024", image_width:str = "1024"):
  task = generate_image(prompt, image_size, image_width)
  # Return task id
  return {"result": task}

@app.post('/api/async/image_chat')
async def image_chat(prompt:str = "cat", image_size:str = "1024", image_width:str = "1024"):
    task_name = "worker.celery_worker.generate_image"
    task = celery_app.send_task(task_name, args=[prompt, image_size, image_width])
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
