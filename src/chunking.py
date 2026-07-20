import re

def split_sentences(text: str) -> list[str]:
    """
    Naive sentence splitter
    - splits on '.', '!', '?' followed by whitespace
    """
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s for s in sentences if s]

def chunk_text(text: str, chunk_size: int = 500, overlap_sentences: int = 1) -> list[str]:
    """
    Docstring for chunk_text
    
    Split text into chunks by grouping whole sentences so no sentence cut mid-way
    - chunk_size = soft target in chars
    - overlap_sentences = controls # trailing sentences repeat at start of next chunk (for context continuity)
    """

    sentences = split_sentences(text)

    if not sentences: return []

    chunks = []
    current = []
    current_len = 0

    for sentence in sentences:
        if current_len + len(sentence) > chunk_size and current:
            chunks.append(" ".join(current))
            # start next chunk w/ overlap from the end of this one
            current = current[-overlap_sentences:] if overlap_sentences else []
            current_len = sum(len(s) for s in current)
        current.append(sentence)
        current_len += len(sentences)

    if current:
        chunks.append(" ".join(current))
    
    return chunks