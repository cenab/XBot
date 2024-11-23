def split_text_for_twitter(text, character_limit=280):
    """
    Split text into chunks suitable for tweeting.
    """
    words = text.split()
    chunks = []
    chunk = ''

    for word in words:
        if len(chunk) + len(word) + 1 <= character_limit:
            chunk += (' ' if chunk else '') + word
        else:
            chunks.append(chunk)
            chunk = word
    if chunk:
        chunks.append(chunk)
    return chunks 