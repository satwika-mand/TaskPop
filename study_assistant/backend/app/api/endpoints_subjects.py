from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.core.database import get_db
from app.models.schema import Subject
from app.models.pydantic_models import SubjectCreate, SubjectResponse

router = APIRouter()

@router.post("/", response_model=SubjectResponse)
async def create_subject(subject: SubjectCreate, db: AsyncSession = Depends(get_db)):
    db_subject = Subject(name=subject.name, description=subject.description)
    db.add(db_subject)
    await db.commit()
    await db.refresh(db_subject)
    return db_subject

@router.get("/", response_model=List[SubjectResponse])
async def read_subjects(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Subject).offset(skip).limit(limit))
    subjects = result.scalars().all()
    return subjects
