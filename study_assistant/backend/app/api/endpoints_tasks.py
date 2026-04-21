from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.core.database import get_db
from app.models.schema import Task, Subject
from app.models.pydantic_models import TaskCreate, TaskResponse

router = APIRouter()

@router.post("/", response_model=TaskResponse)
async def create_task(task: TaskCreate, db: AsyncSession = Depends(get_db)):
    subject = await db.get(Subject, task.subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
        
    db_task = Task(
        title=task.title, 
        description=task.description, 
        is_completed=task.is_completed,
        subject_id=task.subject_id
    )
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task

@router.get("/subject/{subject_id}", response_model=List[TaskResponse])
async def read_tasks_by_subject(subject_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.subject_id == subject_id))
    tasks = result.scalars().all()
    return tasks
