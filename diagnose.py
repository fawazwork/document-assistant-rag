from pypdf import PdfReader
from chunker import chunk_pages
from embedder import embed_texts
from vector_store import build_index, search

reader = PdfReader("sample.pdf")
pages = []
for number, page in enumerate(reader.pages, start=1):
    text = page.extract_text()
    if text and text.strip():
        pages.append({"page": number, "text": text})

chunks = chunk_pages(pages)
index = build_index(embed_texts([c["text"] for c in chunks]))

question = "How many attention heads does the base model use?"
_, ids = search(index, embed_texts([question]), k=len(chunks))

for rank, i in enumerate(ids, start=1):
    if "h = 8" in chunks[i]["text"]:
        print("h = 8 found at rank", rank, "on page", chunks[i]["page"])