from google import genai
from app.core.config import settings

client = genai.Client(api_key=settings.gemini_api_key)

def get_embedding(text: str) -> list[float]:
    response = client.models.embed_content(
        model='text-embedding-004',
        contents=text,
    )
    return response.embeddings[0].values

def generate_revision_guide(topic: str, context_cards: list[str]) -> str:
    context_str = "\n\n".join(f"Note Card {i+1}:\n{card}" for i, card in enumerate(context_cards))
    prompt = f"""
    You are an expert tutor. Create a revision guide for the topic: '{topic}'.
    Use ONLY the information provided in the following note cards.
    If the note cards do not contain relevant information, state that you don't have enough information.
    
    Context Note Cards:
    {context_str}
    
    Structure the revision guide with clear headings, bullet points, and a brief summary.
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash', # Or gemini-2.5-flash-lite if available on SDK
        contents=prompt,
    )
    return response.text
