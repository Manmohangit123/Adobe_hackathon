from src.rag_pipeline import run_rag

def test_rag_response():
    result = run_rag("Explain PDF heading structure.", "input/knowledge_base/format_guidelines.txt")
    assert isinstance(result, str)
    assert len(result) > 0
