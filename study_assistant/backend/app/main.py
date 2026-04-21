from fastapi import FastAPI
from app.api import endpoints_subjects, endpoints_tasks, endpoints_notes, endpoints_revision

app = FastAPI(
    title="StudyMate API",
    description="API for tracking tasks, notes, and AI-powered revision with Gemini",
    version="1.0.0"
)

app.include_router(endpoints_subjects.router, prefix="/api/subjects", tags=["Subjects"])
app.include_router(endpoints_tasks.router, prefix="/api/tasks", tags=["Tasks"])
app.include_router(endpoints_notes.router, prefix="/api/notes", tags=["Notes"])
app.include_router(endpoints_revision.router, prefix="/api/revision", tags=["Revision"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the StudyMate API"}
