# Document Assistant (RAG)

Upload a PDF, ask questions, and get answers with page references. Runs fully locally with Llama 3.1 8B through Ollama, so no data leaves your machine.

## How it works
1. **Extract:** pypdf reads the text page by page.
2. **Chunk:** each page is split into 800-character chunks with 150 overlap (page number kept).
3. **Embed:** sentence-transformers (all-MiniLM-L6-v2) turns chunks into vectors.
4. **Retrieve:** FAISS finds the 5 closest chunks to the question.
5. **Generate:** Llama 3.1 8B answers using only those chunks.
6. **Cite:** source pages come from retrieval, not from the model, so they can't be hallucinated.

## Results
- Retrieval hit rate (top 3): 7/8 strict, 8/8 accepting any page that contains the answer (tested on the "Attention Is All You Need" paper).
- Llama 3.2 3B vs Llama 3.1 8B: TODO write what you found.
- Refuses questions the document doesn't cover instead of guessing.

## Limitations
- Scanned PDFs (images) are not supported.
- Tables and footnotes can come out as flattened text.
- TODO add one more.

## Run it
```
pip install -r requirements.txt
ollama pull llama3.1:8b
streamlit run app.py
```
