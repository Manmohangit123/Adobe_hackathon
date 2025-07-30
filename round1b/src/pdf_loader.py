import os
import fitz  # PyMuPDF

def replace_ligatures(text):
    ligatures = {
        "\ufb00": "ff",
        "\ufb01": "fi",
        "\ufb02": "fl",
        "\ufb03": "ffi",
        "\ufb04": "ffl",
    }
    for ligature, replacement in ligatures.items():
        text = text.replace(ligature, replacement)
    return text

def is_probably_heading(line: str) -> bool:
    """
    Basic heuristic to detect headings:
    - Line is not empty
    - Line is not too long (<= 100 chars)
    - Line starts with uppercase or looks like a heading
    """
    line = line.strip()
    if not line:
        return False
    if len(line) > 100:
        return False
    if line[0].isupper() or line.endswith(":") or line.startswith("•") or line.startswith("-"):
        return True
    return False

def extract_section_title(page_text: str) -> str:
    """
    Extract a best guess for section title from first few lines of page.
    """
    lines = [line.strip() for line in page_text.split('\n') if line.strip()]
    for line in lines[:5]:
        if is_probably_heading(line):
            return line
    if lines:
        first_line = lines[0]
        if len(first_line) <= 100:
            return first_line
    return "Unknown Section"

def load_documents_from_directory(directory_path):
    """
    Load PDFs and extract per-page chunks with metadata: filename, page_number, section_title, text
    """
    documents = []
    for filename in os.listdir(directory_path):
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(directory_path, filename)
            with fitz.open(file_path) as doc:
                for page in doc:
                    page_text = page.get_text()
                    page_text = replace_ligatures(page_text)  # cleanup ligatures here
                    section_title = extract_section_title(page_text)
                    documents.append({
                        "filename": filename,
                        "page_number": page.number + 1,
                        "section_title": section_title,
                        "text": page_text
                    })
    return documents

def chunk_text(documents, chunk_size=500):
    """
    Chunk documents (page texts) into smaller chunks if too long,
    preserving metadata.
    """
    chunks = []
    for doc in documents:
        words = doc["text"].split()
        if len(words) <= chunk_size:
            chunks.append(doc)
        else:
            for i in range(0, len(words), chunk_size):
                chunk_text = " ".join(words[i:i + chunk_size])
                chunks.append({
                    "filename": doc["filename"],
                    "page_number": doc["page_number"],
                    "section_title": doc["section_title"],
                    "text": chunk_text
                })
    return chunks

if __name__ == "__main__":
    input_dir = "input/knowledge_base/collection_1"  # adjust path if needed
    docs = load_documents_from_directory(input_dir)
    chunks = chunk_text(docs)
    print(f"Loaded {len(docs)} pages, split into {len(chunks)} chunks.")
    if chunks:
        print("Sample chunk metadata:", {k: chunks[0][k] for k in ['filename', 'page_number', 'section_title']})
        print("Sample chunk text snippet:", chunks[0]["text"][:200] + "...")
