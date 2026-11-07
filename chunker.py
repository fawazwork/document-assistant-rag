def chunk_pages(pages, chunk_size=800, overlap=150):
    chunks = []
    for page in pages:
        text = page["text"]
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append({"page": page["page"], "text": text[start:end]})
            start += chunk_size - overlap
    return chunks