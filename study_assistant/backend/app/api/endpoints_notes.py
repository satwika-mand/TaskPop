from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.core.database import get_db
from app.models.schema import Note, NoteCard, Subject
from app.models.pydantic_models import NoteCreate, NoteResponse
from app.services.note_processor import chunk_note_content
from app.services.ai_service import get_embedding

router = APIRouter()

@router.post("/", response_model=NoteResponse)
async def create_note(note: NoteCreate, db: AsyncSession = Depends(get_db)):
    subject = await db.get(Subject, note.subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
        
    db_note = Note(title=note.title, content=note.content, subject_id=note.subject_id)
    db.add(db_note)
    await db.commit()
    await db.refresh(db_note)
    
    chunks = chunk_note_content(db_note.content)
    for chunk in chunks:
        embedding = get_embedding(chunk)
        db_card = NoteCard(
            note_id=db_note.id,
            content=chunk,
            embedding=embedding
        )
        db.add(db_card)
    
    await db.commit()
    return db_note

@router.get("/subject/{subject_id}", response_model=List[NoteResponse])
async def read_notes_by_subject(subject_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Note).where(Note.subject_id == subject_id))
    notes = result.scalars().all()
    return notes
