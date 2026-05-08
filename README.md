# Real-Time-News-Analyzer-using-RAG

AI-powered real-time news analysis application built using Retrieval-Augmented Generation (RAG), Ollama, Llama3, FAISS, and Streamlit.

The system dynamically fetches latest news articles, converts them into embeddings using SentenceTransformers, stores them in FAISS vector database, retrieves semantically relevant context, and generates intelligent responses using a locally hosted Llama3 model.

Tech Stack:

Python
Streamlit
NewsAPI
SentenceTransformers
FAISS
Ollama
Llama3

Workflow:

User Query
↓
Topic Extraction
↓
Fetch News
↓
Generate Embeddings
↓
FAISS Retrieval
↓
Llama3 Response Generation
