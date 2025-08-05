This Adobe india hackathon consists of two challenges
they are done in two different files in this repository on the name of:
1.) Round 1a
2.) Round 1b

Round 1a:
# 📄 PDF Outline Extractor – Structured Understanding of Documents

## 💡 Problem Statement
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

## 🎯 Objective
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
🚀 Features
PDF Text & Style Extraction using PyMuPDF

Font-Based Hierarchy Detection for heading classification

Automatic Title Detection from largest text on page 1

Filtering & Cleanup to remove false positives

JSON Output with heading levels and page numbers

Offline RAG Pipeline for knowledge-based Q&A (no internet required)

Dockerized for platform portability

## 🛠 Tech Stack
Python – Core processing logic

PyMuPDF (fitz) – PDF parsing & text extraction

LangChain + ChromaDB – Retrieval-Augmented Generation (RAG) for local Q&A

SentenceTransformers – Embedding generation

Docker – Deployment environment

## ⚙️ How It Works
Text & Font Extraction – Extract text spans, sizes, positions per page.

Font Size Ranking – Map most frequent large fonts to heading levels (H1–H3/H4).

Title Detection – Select largest text on first page.

False Positive Removal – Ignore "Table of Contents", "References", etc.

JSON Output – Save outline and title to fileXX.json.

RAG Pipeline (Optional) – Retrieve knowledge from local text files and answer queries.

## 📂 Project Structure
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

## This repository contains solutions for Round 1a

Run this after navigating to round1a:

python src\pdf_outline_extractor.py input\knowledge_base output

## 🔑 Environment Restrictions
Runtime: ≤ 10 seconds per PDF

CPU-only (no GPU)

No internet access during execution

Model size ≤ 200MB

## 🐳 Docker Usage
Build and run inside Docker:
docker build -t pdf-outline-extractor .
docker run --rm pdf-outline-extractor
