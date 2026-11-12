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
- Llama 3.2 3B vs Llama 3.1 8B: on the question "What BLEU score did the big model get on English-to-German?", 3B mixed up the English-to-French score and contradicted itself, while 8B answered correctly (28.4) in under 5 seconds on a GTX 1660. Both refused an out-of-document question instead of guessing.
- Refuses questions the document doesn't cover instead of guessing.

## Limitations
- Scanned PDFs (images) are not supported.
- Tables and footnotes can come out as flattened text.
- The app re-processes the PDF on every question and answers one document at a time with no chat memory, so follow-up questions don't work yet.

## Run it

**You need:** Python 3.10+, Git, and [Ollama](https://ollama.com) installed.

```
git clone https://github.com/fawazwork/document-assistant-rag.git
cd document-assistant-rag
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
ollama pull llama3.1:8b
streamlit run app.py
```

Then upload a text-based PDF in the browser and ask questions.

**Notes**
- On Mac/Linux, activate with `source venv/bin/activate`.
- Llama 3.1 8B needs roughly 6 GB of GPU memory or 16 GB of RAM. On a weaker PC, use `ollama pull llama3.2:3b` and change the model name in `llm.py` (faster, less accurate).
- The first run downloads a small embedding model (about 90 MB), and the first question is slow while Ollama loads the model.
- To run `eval.py`, download the paper from https://arxiv.org/pdf/1706.03762 and save it as `sample.pdf` in the project folder.
