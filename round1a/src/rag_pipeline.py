import os
from langchain.chains import RetrievalQA
from langchain.llms.fake import FakeListLLM  # Offline safe LLM mock
from vector_store import build_vectorstore

def run_rag(query, kb_path):
    vectordb = build_vectorstore(kb_path)
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})

    # Using FakeListLLM to simulate LLM locally (offline)
    llm = FakeListLLM(responses=["This is a placeholder answer from RAG pipeline."])
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    result = qa.run(query)
    return result

if __name__ == "__main__":
    kb_path = "input/knowledge_base/format_guidelines.txt"
    query = "What makes a good heading in a PDF?"
    answer = run_rag(query, kb_path)
    print("Answer:", answer)
