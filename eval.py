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
if not chunks:
    raise SystemExit("No text found in sample.pdf. It is probably a scanned PDF.")
index = build_index(embed_texts([c["text"] for c in chunks]))

tests = [
    ("How many layers are in the encoder stack?", 3),
    ("What optimizer was used for training?", 7),
    ("How many attention heads does the base model use?", 5),
    ("What hardware was used to train the models?", 7),
    ("What BLEU score did the big model get on English-to-German translation?", 8),
    ("Why does the model need positional encoding?", 6),
    ("What is scaled dot-product attention?", 4),
    ("What dataset was used for English-to-French training?", 7),
]
hits = 0
for question, expected_page in tests:
    _, ids = search(index, embed_texts([question]))
    found = [chunks[i]["page"] for i in ids]
    ok = expected_page in found
    hits += ok
    print(f"{'PASS' if ok else 'FAIL'} | {question} | expected {expected_page}, got {found}")

print(f"Hit rate: {hits}/{len(tests)}")