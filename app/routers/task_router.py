from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_db

from app.models.task_model import Task
from app.models.user_model import User

from app.schemas.task_schema import (
    TaskCreate,
    TaskUpdate,
    TaskResponse
)

from app.core.security import get_current_user


router = APIRouter()


@router.get("/test")
async def test():

    return {
        "message": "working"
    }


@router.post("/tasks")
async def create_task(
    task: TaskCreate,
    current_user: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):

    user_query = await db.execute(
        select(User).where(
            User.email == current_user
        )
    )

    db_user = user_query.scalar()

    new_task = Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        user_id=db_user.id
    )

    db.add(new_task)

    await db.commit()

    await db.refresh(new_task)

    return {
        "message": "Task created successfully",
        "task_id": new_task.id,
        "task_owner": current_user
    }


@router.get(
    "/tasks",
   # response_model=list[TaskResponse]
)
async def get_tasks(
    skip: int = 0,
    limit: int = 5,
    search: str = "",
    status: str = "",
    sort: str = "latest",
    current_user: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):

    user_query = await db.execute(
        select(User).where(
            User.email == current_user
        )
    )

    db_user = user_query.scalar()

    query = select(Task).where(
        Task.user_id == db_user.id
    )

    # SEARCH
    if search:

        query = query.where(
            Task.title.ilike(f"%{search}%")
        )

    # STATUS FILTER
    if status:

        query = query.where(
            Task.status == status
        )

    # SORTING
    if sort == "latest":

        query = query.order_by(
            Task.id.desc()
        )

    elif sort == "oldest":

        query = query.order_by(
            Task.id.asc()
        )

    # PAGINATION
    query = query.offset(skip).limit(limit)

    result = await db.execute(query)

    tasks = result.scalars().unique().all()

    return tasks

@router.put("/tasks/{task_id}")
async def update_task(
    task_id: int,
    updated_task: TaskUpdate,
    current_user: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):

    user_query = await db.execute(
        select(User).where(
            User.email == current_user
        )
    )

    db_user = user_query.scalar()

    task_query = await db.execute(
        select(Task).where(
            Task.id == task_id,
            Task.user_id == db_user.id
        )
    )

    task = task_query.scalar()

    if not task:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task.title = updated_task.title

    task.description = updated_task.description

    task.status = updated_task.status

    task.priority = updated_task.priority

    await db.commit()

    await db.refresh(task)

    return {
        "message": "Task updated successfully",
        "updated_task": task.id
    }


@router.delete("/tasks/{task_id}")
async def delete_task(
    task_id: int,
    current_user: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):

    user_query = await db.execute(
        select(User).where(
            User.email == current_user
        )
    )

    db_user = user_query.scalar()

    task_query = await db.execute(
        select(Task).where(
            Task.id == task_id,
            Task.user_id == db_user.id
        )
    )

    task = task_query.scalar()

    if not task:

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    await db.delete(task)

    await db.commit()

    return {
        "message": "Task deleted successfully"
    }