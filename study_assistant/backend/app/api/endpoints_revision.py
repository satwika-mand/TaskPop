from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.core.database import get_db
from app.models.schema import NoteCard
from app.models.pydantic_models import RevisionRequest
from app.services.ai_service import get_embedding, generate_revision_guide

router = APIRouter()

@router.post("/generate")
async def generate_revision(request: RevisionRequest, db: AsyncSession = Depends(get_db)):
    try:
        query_embedding = get_embedding(request.topic)
        
        result = await db.execute(
            select(NoteCard)
            .order_by(NoteCard.embedding.cosine_distance(query_embedding))
            .limit(request.limit)
        )
        
        relevant_cards = result.scalars().all()
        
        if not relevant_cards:
            return {"revision_guide": "No relevant notes found for this topic.", "cards_used": 0}
            
        card_contents = [card.content for card in relevant_cards]
        guide = generate_revision_guide(request.topic, card_contents)
        
        return {
            "topic": request.topic,
            "revision_guide": guide,
            "cards_used": len(card_contents),
            "sources": card_contents
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
