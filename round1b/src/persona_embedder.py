from sentence_transformers import SentenceTransformer

class PersonaEmbedder:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed_query(self, query, persona=None):
        if persona:
            query = f"{persona}: {query}"
        return self.model.encode([query])[0]
