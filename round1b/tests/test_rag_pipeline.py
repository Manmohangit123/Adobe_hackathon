from src.rag_pipeline import run_rag

def test_rag_response():
    result = run_rag("Explain persona behavior.", "input/knowledge_base/paper1.txt")
    assert isinstance(result, str)
    assert len(result) > 0
