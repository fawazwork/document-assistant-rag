from llm import answer_question
from vector_store import build_index, search
from embedder import embed_texts
from chunker import chunk_pages
import streamlit as st
from pypdf import PdfReader

st.title("Intelligent Document Assistant")
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file is not None:
    reader = PdfReader(uploaded_file)
    pages = []
    for number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        if text and text.strip():
            pages.append({"page": number, "text": text})

    if not pages:
        st.error("No text found. This may be a scanned PDF.")
    else:
        st.write(f"Pages with text: {len(pages)} of {len(reader.pages)}")
        st.text(pages[0]["text"][:500])
        chunks = chunk_pages(pages)
        st.write(f"Total chunks: {len(chunks)}")
        st.text(chunks[0]["text"])
        vectors = embed_texts([c["text"] for c in chunks])
        st.write(f"Embeddings shape: {vectors.shape}")
        index = build_index(vectors)
        question = st.text_input("Ask a question about the PDF")
        if question:
            scores, ids = search(index, embed_texts([question]))
            top_chunks = [chunks[i] for i in ids]
            with st.spinner("Thinking..."):
                answer = answer_question(question, top_chunks)
            st.write(answer)