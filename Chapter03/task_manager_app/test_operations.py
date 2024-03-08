from conftest import TEST_TASKS_CSV
from models import Task, TaskWithID
from operations import (
    create_task,
    get_next_id,
    modify_task,
    read_all_tasks,
    read_task,
    remove_task,
    write_task_into_csv,
)


def test_read_all_tasks():
    assert read_all_tasks() == [
        TaskWithID(**task) for task in TEST_TASKS_CSV
    ]


def test_get_next_id():
    assert get_next_id() == 3


def test_write_task_into_csv():
    task = TaskWithID(
        id=3,
        title="New Task",
        description="New Desc",
        status="Open",
    )
    write_task_into_csv(task)
    assert read_all_tasks() == list(
        map(
            lambda task: TaskWithID(**task),
            TEST_TASKS_CSV,
        )
    ) + [
        TaskWithID(
            id=3,
            title="New Task",
            description="New Desc",
            status="Open",
        )
    ]


def test_create_task():
    task = Task(
        title="New Task",
        description="New Desc",
        status="Open",
    )
    result = create_task(task)

    assert result.id == 3

    assert read_task(3) == TaskWithID(
        id=3, **task.model_dump()
    )


def test_read_task():
    assert read_task(1) == TaskWithID(
        **TEST_TASKS_CSV[0]
    )


def test_modify_task():
    updated_task = {"title": "New Title"}
    modify_task(1, updated_task)
    assert read_task(1).title == "New Title"


def test_remove_task():
    remove_task(1)
    assert read_task(1) is None
