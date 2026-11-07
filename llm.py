import ollama


def answer_question(question, chunks):
    context = "\n\n".join(f"[Page {c['page']}]\n{c['text']}" for c in chunks)
    prompt = f"""Answer the question using only the context below.
If the answer is not in the context, say "I couldn't find that in the document."
Mention the page number(s) you used.

Context:
{context}

Question: {question}"""
    response = ollama.chat(
        model="llama3.2:3b",
        messages=[{"role": "user", "content": prompt}],
    )
    return response["message"]["content"]