# Adobe india hackathon

This Adobe india hackathon consists of two challenges

they are done in two different files in this repository on the name of:

1.) Round 1a

2.) Round 1b

## Round 1a:

## 📄 PDF Outline Extractor – Structured Understanding of Documents

### 💡 Problem Statement
In today's document-heavy digital world, unstructured PDFs make it difficult for machines to extract meaning.  
Our task: **transform raw PDFs into a machine-interpretable structured outline** that includes:
- Document title
- Hierarchical headings (H1–H3 or H4)
- Associated page numbers  
Output: Clean, valid **JSON**.

This forms the foundation for intelligent applications like:
- Semantic search
- Document summarization
- Context-aware recommendation systems

---

### 🎯 Objective

Build a system that:
- Accepts one or more PDF files (≤ 50 pages each)
- Analyzes content structure
- Returns hierarchical JSON outlines

**Example Output:**

{
  
  "title": "Understanding AI",
  
  "outline": [
  
    { "level": "H1", "text": "Introduction", "page": 0 },
  
    { "level": "H2", "text": "What is AI?", "page": 1 },
  
    { "level": "H3", "text": "History", "page": 2 }
  
  ]
  
}

### 🚀 Features

PDF Text & Style Extraction using PyMuPDF

Font-Based Hierarchy Detection for heading classification

Automatic Title Detection from largest text on page 1

Filtering & Cleanup to remove false positives

JSON Output with heading levels and page numbers

Offline RAG Pipeline for knowledge-based Q&A (no internet required)

Dockerized for platform portability

### 🛠 Tech Stack

Python – Core processing logic

PyMuPDF (fitz) – PDF parsing & text extraction

LangChain + ChromaDB – Retrieval-Augmented Generation (RAG) for local Q&A

SentenceTransformers – Embedding generation

Docker – Deployment environment

### ⚙️ How It Works

Text & Font Extraction – Extract text spans, sizes, positions per page.

Font Size Ranking – Map most frequent large fonts to heading levels (H1–H3/H4).

Title Detection – Select largest text on first page.

False Positive Removal – Ignore "Table of Contents", "References", etc.

JSON Output – Save outline and title to fileXX.json.

RAG Pipeline (Optional) – Retrieve knowledge from local text files and answer queries.

### 📂 Project Structure

pdf-outline-extractor/

│── src/

│   ├── pdf_outline_extractor.py 

│   ├── vector_store.py    

│   ├── rag_pipeline.py 

│── input/  

│── output/ 

│── requirements.txt

│── Dockerfile

│── README.md

### This repository contains solutions for Round 1a

Run this after navigating to round1a:

python src\pdf_outline_extractor.py input\knowledge_base output

### 🔑 Environment Restrictions

Runtime: ≤ 10 seconds per PDF

CPU-only (no GPU)

No internet access during execution

Model size ≤ 200MB

### 🐳 Docker Usage

Build and run inside Docker:

docker build -t pdf-outline-extractor .

docker run --rm pdf-outline-extractor

## Round 1b:

## 🤖 Persona-Driven Document Intelligence

### 💡 Problem Statement
In the document-heavy digital world, users have different **personas** and specific **jobs-to-be-done**.  
The challenge: From a **set of related PDFs**, extract and rank sections **most relevant** to:
- A **persona role** (e.g., student, analyst, researcher)
- A **task** they want to accomplish (e.g., "Prepare a literature review")

---

### 🎯 Objective
Build an **offline, persona-aware PDF analysis engine** that:
- Accepts **3–10 related PDF documents**
- Accepts a **JSON input** with:
  - Persona role
  - Job-to-be-done task
- Outputs:
  - Top relevant sections (title, page, document source)
  - Ranked importance
  - Refined text snippet

---

### 📥 Sample Input JSON

{

  "persona": {
  
    "role": "PhD Researcher in Computational Biology"
    
  },
  
  "job_to_be_done": {
  
    "task": "Prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks"
    
  }
  
}

### 📤 Sample Output JSON

{

  "metadata": {
    
    "documents": ["doc1.pdf", "doc2.pdf"],
    
    "persona": "PhD Researcher in Computational Biology",
    
    "job_to_be_done": "Prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks",
    
    "processed_on": "2025-07-28T14:35:00"
  
  },
  
  "results": [
  
    {
    
      "document": "doc1.pdf",
      
      "page": 5,
      
      "section_title": "Methodology and Benchmarking",
      
      "importance_rank": 1,
      
      "refined_text": "This section details datasets used for molecular prediction and compares three GNN models across performance metrics..."
    
    },
    
    {
    
      "document": "doc2.pdf",
      
      "page": 3,
      
      "section_title": "Datasets in Drug Discovery",
      
      "importance_rank": 2,
      
      "refined_text": "Included datasets: PubChem, Tox21, SIDER. Key pre-processing techniques described..."
    
    }
  
  ]

}

### 🚀 Features

📄 Multi-document analysis (3–10 PDFs)

🧠 Persona-aware query modification for better context relevance

🔍 Semantic chunk retrieval using embeddings + cosine similarity

📊 Ranked results based on importance to the persona/task

🐳 Dockerized for easy, offline deployment

### 🛠 Tech Stack

Python – Core processing logic

PyMuPDF – PDF parsing

SentenceTransformers (all-MiniLM-L6-v2) – Embedding generation

Torch – Backend for embeddings

Pickle – Offline vector storage

Docker – Deployment & portability

### ⚙️ How It Works

Document Loading (pdf_loader.py)

Parse PDFs into raw text per page.

Chunking

Split text into ~500-word semantic chunks for better embedding.

Vectorization (vector_store.py)

Encode chunks into embeddings using all-MiniLM-L6-v2.

Persona-aware Querying (persona_embedder.py)

Modify job-to-be-done with persona context before searching.

Semantic Matching (rag_pipeline.py)

Retrieve top matching chunks using cosine similarity.

Output

Ranked JSON results with title, page, doc name, and snippet.

### 📂 Project Structure

persona-doc-intelligence/

│── src/

│   ├── pdf_loader.py

│   ├── persona_embedder.py

│   ├── vector_store.py

│   ├── rag_pipeline.py

│── input/

│   ├── pdfs/          # Input documents

│   ├── persona.json   # Example persona/task input

│── output/

│── requirements.txt

│── Dockerfile

│── README.md


### This repository contains solutions for Round 1b. 

1B: navigate to round1b then:run these two

collection_1: python src/vector_store.py input/knowledge_base/collection_1 input/knowledge_base/collection_1

python src/rag_pipeline.py --input input/knowledge_base/collection_1/challenge1b_input.json --vectorstore input/knowledge_base/collection_1/vector_store.pkl --output input/knowledge_base/collection_1/challenge1b_output.json

collection_2 python src/vector_store.py input/knowledge_base/collection_2 input/knowledge_base/collection_2

python src/rag_pipeline.py --input input/knowledge_base/collection_2/challenge1b_input.json --vectorstore input/knowledge_base/collection_2/vector_store.pkl --output input/knowledge_base/collection_2/challenge1b_output.json

collection_3: python src/vector_store.py input/knowledge_base/collection_3 input/knowledge_base/collection_3

python src/rag_pipeline.py --input input/knowledge_base/collection_3/challenge1b_input.json --vectorstore input/knowledge_base/collection_3/vector_store.pkl --output input/knowledge_base/collection_3/challenge1b_output.json
