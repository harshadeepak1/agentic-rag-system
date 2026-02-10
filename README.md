# Agentic RAG System

A modular multi-agent Retrieval-Augmented Generation (RAG) system for intelligent document querying using semantic embeddings and vector search.

This project implements a scalable architecture capable of ingesting multiple document formats, generating embeddings using HuggingFace models, storing them in a Milvus vector database, and routing user queries through specialized agents to produce contextual responses.

---

## 🚀 Overview

The system demonstrates an end-to-end RAG pipeline including:

* Document ingestion and chunking
* Semantic embedding generation
* Vector storage and similarity retrieval
* Agent-based query routing
* Context-aware answer generation
* Interactive web interface

It is designed as a production-style engineering project emphasizing modularity, extensibility, and real-world AI system design patterns.

---

## 🧠 Architecture

```
User Query
   ↓
Router Agent
   ↓
Agent Selection
   ├── Document Agent
   ├── Excel Agent
   └── QA Agent
   ↓
Embedding Generation (HuggingFace)
   ↓
Vector Retrieval (Milvus)
   ↓
Context Aggregation
   ↓
LLM Interface (Pluggable)
   ↓
Final Response
```

---

## 🛠️ Technology Stack

| Component        | Technology                               |
| ---------------- | ---------------------------------------- |
| Frontend         | Streamlit                                |
| Embeddings       | Sentence Transformers (all-MiniLM-L6-v2) |
| Vector Database  | Milvus                                   |
| Agents           | Custom Python Architecture               |
| LLM Interface    | Modular / Replaceable                    |
| Containerization | Docker                                   |
| Language         | Python                                   |

---

## 📁 Project Structure

```
agentic-rag-system/
├── app.py
├── agents/
├── core/
│   ├── document_processor.py
│   ├── vector_store.py
│   ├── embeddings.py
│   └── llm.py
├── utils/
├── data/
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### Clone Repository

```bash
git clone <repo-url>
cd agentic-rag-system
```

### Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start Milvus

```bash
docker-compose up -d
```

### Run Application

```bash
streamlit run app.py
```

Open in browser:

```
http://localhost:8501
```

---

## 🧪 Usage

1. Upload supported documents
2. Process files to generate embeddings
3. Submit queries
4. System retrieves relevant chunks
5. Agent produces contextual answer

---

## ✨ Design Highlights

* Agent-driven orchestration improves query routing
* Semantic retrieval using transformer embeddings
* Efficient similarity search via vector indexing
* Modular LLM interface for model replacement
* Clean UI for interactive experimentation

---

## 🔮 Future Improvements

* Hybrid keyword + vector retrieval
* Advanced reranking models
* Persistent conversational memory
* Distributed deployment
* Model fine-tuning support
* LLM swapping (OpenAI / HF / Local)

---

## 👤 Author

Harsha Deepak
Computer Science Engineering

---
