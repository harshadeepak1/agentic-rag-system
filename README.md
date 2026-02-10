# Agentic RAG System

An intelligent document question-answering system powered by AI agents that can process multiple document types and provide contextual answers.

## 🎯 Features

- **Multi-format Document Support**: PDF, DOCX, PPT, Excel, and Text files
- **Agentic Workflow**: Intelligent query routing and processing
- **Vector Database**: Milvus for efficient similarity search
- **Advanced Retrieval**: Hybrid search with reranking
- **Web UI**: Clean Streamlit interface
- **Comprehensive Error Handling**: Robust error management throughout

## 🏗️ System Architecture

```
User Query → Agent Router → [Document Agent | Excel Agent | General QA Agent]
                ↓
        Vector Database (Milvus)
                ↓
        Retrieval & Reranking
                ↓
        LLM Response Generation
```

## 📋 Prerequisites

- Python 3.9+
- Docker and Docker Compose (for Milvus)
- 8GB+ RAM recommended
- Git

## 🚀 Installation & Setup

### Step 1: Clone Repository

```bash
git clone <your-repo-url>
cd agentic-rag-system
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Setup Milvus Vector Database

```bash
# Start Milvus using Docker Compose
docker-compose up -d

# Wait for Milvus to be ready (about 30 seconds)
```

### Step 5: Configure Environment Variables

Create a `.env` file in the project root:

```bash
# API Keys
GOOGLE_API_KEY=your_google_api_key_here

# Milvus Configuration
MILVUS_HOST=localhost
MILVUS_PORT=19530

# Model Configuration
EMBEDDING_MODEL=models/embedding-001
LLM_MODEL=gemini-1.5-flash
```

**Get Google API Key:**
1. Go to https://makersuite.google.com/app/apikey
2. Create a new API key
3. Copy and paste it in the `.env` file

### Step 6: Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
agentic-rag-system/
├── app.py                      # Streamlit UI
├── agents/
│   ├── __init__.py
│   ├── base_agent.py          # Base agent class
│   ├── document_agent.py      # Document processing agent
│   ├── excel_agent.py         # Excel processing agent
│   ├── qa_agent.py            # Question answering agent
│   └── router_agent.py        # Agent router/orchestrator
├── core/
│   ├── __init__.py
│   ├── document_processor.py  # Document ingestion
│   ├── vector_store.py        # Milvus operations
│   ├── embeddings.py          # Embedding generation
│   └── llm.py                 # LLM interface
├── utils/
│   ├── __init__.py
│   ├── config.py              # Configuration management
│   └── logger.py              # Logging utilities
├── data/
│   └── sample/                # Sample documents
├── docker-compose.yml         # Milvus setup
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## 🎮 Usage Guide

### 1. Upload Documents

- Click "Browse files" in the sidebar
- Upload PDF, DOCX, PPT, XLSX, or TXT files
- Click "Process Documents"
- Wait for processing to complete

### 2. Ask Questions

- Type your question in the text input
- The agent will:
  - Route query to appropriate specialist agent
  - Retrieve relevant context from vector database
  - Generate answer using LLM
  - Display sources used

### 3. View Agent Activity

- See which agent handled your query
- View retrieved context chunks
- Check confidence scores

## 🤖 Agentic Workflow

### Agent Types

1. **Router Agent**: Analyzes queries and routes to specialist agents
2. **Document Agent**: Handles questions about general documents
3. **Excel Agent**: Specializes in spreadsheet data queries
4. **QA Agent**: Handles general knowledge questions

### Workflow Steps

```
1. Query Analysis
   ↓
2. Agent Selection (Router decides which agent to use)
   ↓
3. Context Retrieval (Agent searches vector database)
   ↓
4. Reranking (Prioritize most relevant chunks)
   ↓
5. Answer Generation (LLM generates response)
   ↓
6. Response Validation (Agent verifies answer quality)
```

## 🔧 Configuration

### Embedding Model
- Default: Google's `models/embedding-001`
- Can be changed in `.env`

### LLM Model
- Default: `gemini-1.5-flash` (fast and free)
- Alternative: `gemini-1.5-pro` (more capable)

### Vector Database
- Milvus running on `localhost:19530`
- Collection: `document_collection`
- Dimension: 768

## 📊 Sample Data

Sample documents are provided in `data/sample/`:
- `company_policy.pdf` - Sample company policy
- `sales_data.xlsx` - Sample sales data
- `presentation.pptx` - Sample presentation

## 🐛 Troubleshooting

### Milvus Connection Issues
```bash
# Check if Milvus is running
docker ps

# Restart Milvus
docker-compose restart

# Check logs
docker-compose logs
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### API Key Issues
- Verify your Google API key is valid
- Check if you've enabled Gemini API in Google AI Studio
- Ensure `.env` file is in the project root

## 🎯 Key Design Decisions

1. **Milvus as Vector Database**: Chosen for scalability and performance
2. **Google Gemini**: Free tier, fast, and capable
3. **Agentic Design**: Specialized agents for better context handling
4. **Hybrid Retrieval**: Combines semantic search with reranking
5. **Chunking Strategy**: 1000 chars with 200 char overlap for context preservation

## ⚠️ Limitations

- Maximum file size: 50MB per document
- Concurrent users: Best for single-user or small teams
- Language: Optimized for English
- Token limits: Subject to Gemini API limits

## 🔒 Security Notes

- Never commit `.env` file to Git
- Keep API keys secure
- Sanitize user inputs
- Validate file uploads

## 📝 License

MIT License

## 👥 Contributing

Contributions welcome! Please open an issue or submit a pull request.

## 📧 Support

For issues or questions, please open a GitHub issue.
