import argparse
import json
import os
from datetime import datetime
import pickle
from sentence_transformers import SentenceTransformer, util

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def load_vector_store(path):
    with open(path, "rb") as f:
        return pickle.load(f)  # returns (chunks, embeddings)


def embed_query(query, persona=None):
    if persona:
        query = f"{persona}: {query}"
    return embedding_model.encode(query, convert_to_tensor=True)


def get_top_k_indices(query_embedding, embeddings, top_k=10):
    similarities = util.cos_sim(query_embedding, embeddings)[0]
    top_results = similarities.argsort(descending=True)[:top_k]
    return top_results.cpu().tolist(), similarities


def remove_newlines(obj):
    """
    Recursively remove newlines ('\n') from all string values in the data structure.
    """
    if isinstance(obj, dict):
        return {k: remove_newlines(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [remove_newlines(item) for item in obj]
    elif isinstance(obj, str):
        return obj.replace('\n', ' ')
    else:
        return obj



def main(input_json_path, vector_store_path, output_json_path=None):
    with open(input_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # More descriptive prompt to improve relevance
    base_query = data["job_to_be_done"]["task"]
    query_prompt = (
        f"{data.get('persona', {}).get('role', 'Traveler')}: "
        f"Please plan a 4-day itinerary with must-see cities, activities, local cuisine, "
        f"nightlife and accommodation recommendations for a group of 10 college friends visiting the South of France. "
        f"{base_query}"
    )

    persona = data.get("persona", {}).get("role", None)
    input_docs = [doc["filename"] for doc in data.get("documents", [])]

    chunks, embeddings = load_vector_store(vector_store_path)
    query_embedding = embed_query(query_prompt, persona)

    top_k = 10  # retrieve more for deduplication
    top_indices, _ = get_top_k_indices(query_embedding, embeddings, top_k=top_k)

    # Deduplicate by document for diversity (limit to 5 output sections)
    seen_docs = set()
    extracted_sections = []
    subsection_analysis = []
    importance_rank = 1

    for idx in top_indices:
        chunk = chunks[idx]
        doc = chunk.get("filename", "N/A")
        if doc not in seen_docs:
            seen_docs.add(doc)
            section_title = chunk.get("section_title", "Unknown Section")
            page_number = chunk.get("page_number", -1)

            extracted_sections.append({
                "document": doc,
                "section_title": section_title,
                "importance_rank": importance_rank,
                "page_number": page_number
            })

            refined_text = chunk["text"]
            if len(refined_text) > 500:
                refined_text = refined_text[:500].rstrip() + "..."
            subsection_analysis.append({
                "document": doc,
                "refined_text": refined_text,
                "page_number": page_number
            })

            importance_rank += 1
            if importance_rank > 5:
                break

    result = {
        "metadata": {
            "input_documents": input_docs,
            "persona": persona or "",
            "job_to_be_done": base_query,
            "processing_timestamp": datetime.utcnow().isoformat()
        },
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }

    # --- Modify here to apply Unicode unescaping and optional newline removal ---
    # Uncomment below line if you want to remove all newlines in output text.
    result = remove_newlines(result)

    if output_json_path:
        os.makedirs(os.path.dirname(output_json_path) or ".", exist_ok=True)
        with open(output_json_path, "w", encoding="utf-8") as out_f:
            # Use ensure_ascii=False to output real accented characters, not unicode escapes
            json.dump(result, out_f, indent=2, ensure_ascii=False)
        print(f"✅ Output saved to {output_json_path}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RAG pipeline with Unicode unescaping and optional newline removal")
    parser.add_argument("--input", type=str, required=True, help="Input JSON filepath")
    parser.add_argument("--vectorstore", type=str, required=True, help="Vector store .pkl filepath")
    parser.add_argument("--output", type=str, help="Output JSON filepath (optional)")
    args = parser.parse_args()

    main(args.input, args.vectorstore, args.output)
