import ollama


def answer_question(question, chunks):
    context = "\n\n".join(f"[Page {c['page']}]\n{c['text']}" for c in chunks)
    prompt = f"""Answer the question using only the context below.
Give a short, direct answer in 1 to 3 sentences.
If the context states the answer, give it directly. Do not say the text doesn't mention it.

Context:
{context}

Question: {question}"""
    response = ollama.chat(
        model="llama3.1:8b",
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0},
    )
    return response["message"]["content"]