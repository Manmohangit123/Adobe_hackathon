import sys
import os
import pickle
from sentence_transformers import SentenceTransformer
from pdf_loader import load_documents_from_directory, chunk_text

def embed_and_store(input_dir: str, output_dir: str):
    documents = load_documents_from_directory(input_dir)
    chunks = chunk_text(documents)

    if not chunks:
        raise ValueError("No text chunks found. Check input folder or file types.")

    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode([chunk["text"] for chunk in chunks], show_progress_bar=True)

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "vector_store.pkl")
    with open(output_path, "wb") as f:
        pickle.dump((chunks, embeddings), f)

    print(f"✅ Vector store saved to {output_path}")

if __name__ == "__main__":
    input_dir = sys.argv[1] if len(sys.argv) > 1 else "input/knowledge_base/collection_1"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "output"
    embed_and_store(input_dir, output_dir)
