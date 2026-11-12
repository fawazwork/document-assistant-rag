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

question = "What BLEU score did the big model get on English-to-German translation?"
_, ids = search(index, embed_texts([question]), k=len(chunks))

for rank, i in enumerate(ids, start=1):
    if "28.4" in chunks[i]["text"]:
        print("28.4 found at rank", rank, "on page", chunks[i]["page"])