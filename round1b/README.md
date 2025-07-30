# Adobe Hackathon Submission

This repository contains solutions for  Round 1b.
1B:
navigate to round1b then:run these two

collection_1:
python src/vector_store.py input/knowledge_base/collection_1 input/knowledge_base/collection_1



python src/rag_pipeline.py --input input/knowledge_base/collection_1/challenge1b_input.json --vectorstore input/knowledge_base/collection_1/vector_store.pkl --output input/knowledge_base/collection_1/challenge1b_output.json


collection_2
python src/vector_store.py input/knowledge_base/collection_2 input/knowledge_base/collection_2

python src/rag_pipeline.py --input input/knowledge_base/collection_2/challenge1b_input.json --vectorstore input/knowledge_base/collection_2/vector_store.pkl --output input/knowledge_base/collection_2/challenge1b_output.json

collection_3:
python src/vector_store.py input/knowledge_base/collection_3 input/knowledge_base/collection_3

python src/rag_pipeline.py --input input/knowledge_base/collection_3/challenge1b_input.json --vectorstore input/knowledge_base/collection_3/vector_store.pkl --output input/knowledge_base/collection_3/challenge1b_output.json
