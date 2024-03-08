from typing import Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from models import Task, TaskV2WithID, TaskWithID
from operations import (
    create_task,
    modify_task,
    read_all_tasks,
    read_all_tasks_v2,
    read_task,
    remove_task,
)
from security import (
    User,
    UserInDB,
    fake_token_generator,
    fake_users_db,
    fakely_hash_password,
    get_user_from_token,
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Customized Title",
        version="2.0.0",
        description="This is a custom OpenAPI schema",
        routes=app.routes,
    )
    del openapi_schema["paths"]["/token"]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app = FastAPI(
    title="Task Manager API",
    description="This is a task management API",
    version="0.1.0",
)

app.openapi = custom_openapi


@app.get("/tasks", response_model=list[TaskWithID])
def get_tasks(
    status: Optional[str] = None,
    title: Optional[str] = None,
):
    tasks = read_all_tasks()
    if status:
        tasks = [
            task
            for task in tasks
            if task.status == status
        ]
    if title:
        tasks = [
            task
            for task in tasks
            if task.title == title
        ]
    return tasks


@app.get("/task/{task_id}")
def get_task(task_id: int):
    task = read_task(task_id)
    if not task:
        raise HTTPException(
            status_code=404, detail="task not found"
        )
    return task


@app.post("/task", response_model=TaskWithID)
def add_task(task: Task):
    return create_task(task)


class UpdateTask(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None


@app.put("/task/{task_id}", response_model=TaskWithID)
def update_task(task_id: int, task_update: UpdateTask):
    modified = modify_task(
        task_id,
        task_update.model_dump(exclude_unset=True),
    )
    if not modified:
        raise HTTPException(
            status_code=404, detail="task not found"
        )

    return modified


@app.delete("/task/{task_id}", response_model=Task)
def delete_task(task_id: int):
    removed_task = remove_task(task_id)
    if not removed_task:
        raise HTTPException(
            status_code=404, detail="task not found"
        )
    return removed_task


@app.get(
    "/tasks/search", response_model=list[TaskWithID]
)
def search_tasks(keyword: str):
    tasks = read_all_tasks()
    filtered_tasks = [
        task
        for task in tasks
        if keyword.lower()
        in (task.title + task.description).lower()
    ]
    return filtered_tasks


@app.get("/v2/tasks", response_model=list[TaskV2WithID])
def get_tasks_v2():
    tasks = read_all_tasks_v2()
    return tasks


@app.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
        )
    user = UserInDB(**user_dict)
    hashed_password = fakely_hash_password(
        form_data.password
    )
    if not hashed_password == user.hashed_password:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
        )

    token = fake_token_generator(user)

    return {
        "access_token": token,
        "token_type": "bearer",
    }


@app.get("/users/me", response_model=User)
def read_users_me(
    current_user: User = Depends(get_user_from_token),
):
    return current_user
