import asyncio
from app.core.database import engine, Base
from sqlalchemy import text
from app.models.schema import Subject, Task, Note, NoteCard

async def init_models():
    async with engine.begin() as conn:
        # Create vector extension if not exists
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        # Create all tables
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully!")

if __name__ == "__main__":
    asyncio.run(init_models())
