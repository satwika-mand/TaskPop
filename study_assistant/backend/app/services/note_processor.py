def chunk_note_content(content: str) -> list[str]:
    chunks = [chunk.strip() for chunk in content.split("\n\n") if chunk.strip()]
    return chunks
