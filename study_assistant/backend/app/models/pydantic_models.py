from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class SubjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class SubjectCreate(SubjectBase):
    pass

class SubjectResponse(SubjectBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_completed: bool = False

class TaskCreate(TaskBase):
    subject_id: int

class TaskResponse(TaskBase):
    id: int
    subject_id: int
    model_config = ConfigDict(from_attributes=True)

class NoteBase(BaseModel):
    title: str
    content: str
    subject_id: int

class NoteCreate(NoteBase):
    pass

class NoteResponse(NoteBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class RevisionRequest(BaseModel):
    topic: str
    limit: int = 5
