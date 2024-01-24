from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, Request
import logging
from fastapi.responses import HTMLResponse
import pandas as pd
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")
logging.basicConfig(level=logging.INFO, filename="to_do_tasks.txt", encoding="utf-8")
logger = logging.getLogger(__name__)

TO_DO_COMMON_LIST = []


class To_do_task(BaseModel):
    id: int
    header: Optional[str] = None
    description: Optional[str] = None
    done_status: bool = False


@app.post("/tasks/", response_model=To_do_task)
async def create_item(to_do_task: To_do_task):
    logger.info(f'Создали задание: {to_do_task}')
    to_do_task_id = len(TO_DO_COMMON_LIST) + 1
    to_do_task.id = to_do_task_id
    TO_DO_COMMON_LIST.append(to_do_task)
    return to_do_task_id


@app.get('/tasks/', response_class=HTMLResponse)
async def users_list(request: Request):
    logger.info('Создали таблицу заданий')
    to_do_task_table = pd.DataFrame([vars(to_do_task) for to_do_task in TO_DO_COMMON_LIST]).to_html()
    return templates.TemplateResponse("tasks.html", {"request": request, "users_table": to_do_task_table})


@app.get('/tasks/{id}', response_class=HTMLResponse)
async def users_list(request: Request, to_do_task: To_do_task):
    logger.info(f'Выводим задание {to_do_task}')
    to_do_task_table = pd.DataFrame([vars(to_do_task)]).to_html()
    return templates.TemplateResponse("tasks.html", {"request": request, "to_do_task_table": to_do_task_table})


@app.put('/tasks/{id}', response_model=To_do_task)
async def update_user_info(to_do_task_id: int, to_do_task: To_do_task):
    logger.info(f'Обновили задание {to_do_task_id}')
    for i, current_to_do_task in enumerate(TO_DO_COMMON_LIST):
        if current_to_do_task.id == to_do_task_id:
            TO_DO_COMMON_LIST[i] = to_do_task
            return {"to_do_task_id": to_do_task_id, "to_do_task": to_do_task}


@app.delete('/tasks/{id}')
async def delete_user(to_do_task_id: int):
    logger.info(f'Удалили задание {to_do_task_id}')
    for i, current_to_do_task in enumerate(TO_DO_COMMON_LIST):
        if current_to_do_task.id == to_do_task_id:
            TO_DO_COMMON_LIST.pop(i)
        return {"to_do_task_id": to_do_task_id}
    else:
        return print("There is no task with such id")
