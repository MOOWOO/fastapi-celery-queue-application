from __future__ import annotations
from typing import TYPE_CHECKING

import celery.states
from celery.result import AsyncResult
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from worker.celery_app import celery_app
from worker.celery_worker import long_task

if TYPE_CHECKING:
    from celery import Task
    long_task: Task

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

@app.route('/chat', methods=['POST'])
def chat():
    # Get prompt from client
    prompt = app.request.json.get('prompt')
    task = celery_app.send_task("generate_text", args=[prompt])
    # Return task id
    return {"task_id": task.id}

@app.get("/chat/{task_id}/status")
async def status(task_id: str) -> dict:
    res = AsyncResult(task_id)
    if res.state == celery.states.SUCCESS:
        return {'state': celery.states.SUCCESS,
                'data': res.result['choices'][0]['text']}
    return {'state': res.state}

@app.route('/image_chat', methods=['POST'])
def image_chat():
    # Get prompt from client
    prompt = app.request.json.get('prompt', "cartoon cat")
    number = app.request.json.get('number', 1)
    image_size = app.request.json.get('image_size', 1024)
    image_width = app.request.json.get('image_width', 1024)

    # Run GPT-3 task asynchronously
    task = celery_app.send_task("generate_image", args=[prompt, number, image_size, image_width])

    # Return task id
    return {"task_id": task.id}


@app.get("/image/{task_id}/status")
def image_result(task_id: str):
    # Get task result
    res = AsyncResult(task_id)
    if res.state == celery.states.SUCCESS:
        return {'state': celery.states.SUCCESS,
                'data': res.result}
    return {'state': res.state}
