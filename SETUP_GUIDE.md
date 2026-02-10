# Complete Setup Guide - Agentic RAG System

## 🎯 Project Overview

This guide will walk you through setting up a complete Agentic RAG (Retrieval-Augmented Generation) system from scratch. The system uses AI agents to intelligently process and answer questions from various document types.

---

## 📋 Prerequisites Checklist

Before starting, ensure you have:
- [ ] Python 3.9 or higher installed
- [ ] Docker Desktop installed and running
- [ ] Git installed
- [ ] Text editor or IDE (VS Code recommended)
- [ ] At least 8GB RAM available
- [ ] Stable internet connection
- [ ] Google account (for API key)

---

## 🚀 Step-by-Step Installation

### **STEP 1: Create Project Directory**

```bash
# Create project folder
mkdir agentic-rag-system
cd agentic-rag-system

# Initialize git repository
git init
```

### **STEP 2: Set Up Python Virtual Environment**

**For Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**For Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### **STEP 3: Create Project Structure**

Create the following folder structure:

```
agentic-rag-system/
├── agents/
│   ├── __init__.py
│   ├── base_agent.py
│   ├── document_agent.py
│   ├── excel_agent.py
│   ├── qa_agent.py
│   └── router_agent.py
├── core/
│   ├── __init__.py
│   ├── document_processor.py
│   ├── embeddings.py
│   ├── llm.py
│   └── vector_store.py
├── utils/
│   ├── __init__.py
│   ├── config.py
│   └── logger.py
├── data/
│   └── sample/
├── logs/
├── .env
├── .env.example
├── .gitignore
├── app.py
├── docker-compose.yml
├── requirements.txt
└── README.md
```

**Quick command to create all folders:**

```bash
# Windows (PowerShell)
New-Item -ItemType Directory -Path agents,core,utils,data\sample,logs

# Mac/Linux
mkdir -p agents core utils data/sample logs
```

### **STEP 4: Create Empty __init__.py Files**

```bash
# Windows
type nul > agents\__init__.py
type nul > core\__init__.py
type nul > utils\__init__.py

# Mac/Linux
touch agents/__init__.py
touch core/__init__.py
touch utils/__init__.py
```

### **STEP 5: Get Google API Key**

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the API key (keep it safe!)

### **STEP 6: Create .env File**

Create a file named `.env` in the project root:

```bash
# Create .env file
# Windows
type nul > .env

# Mac/Linux
touch .env
```

Add this content to `.env`:

```
GOOGLE_API_KEY=YOUR_API_KEY_HERE
MILVUS_HOST=localhost
MILVUS_PORT=19530
EMBEDDING_MODEL=models/embedding-001
LLM_MODEL=gemini-1.5-flash
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K=5
SIMILARITY_THRESHOLD=0.7
```

**Replace `YOUR_API_KEY_HERE` with your actual Google API key!**

### **STEP 7: Copy All Code Files**

Now copy all the code files from this conversation:
1. `requirements.txt`
2. `docker-compose.yml`
3. All files in `agents/`
4. All files in `core/`
5. All files in `utils/`
6. `app.py`
7. `README.md`

### **STEP 8: Create .gitignore File**

Create `.gitignore`:

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
*.egg-info/

# Environment
.env

# Logs
logs/
*.log

# Docker volumes
volumes/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Temporary files
/tmp/
*.tmp
```

### **STEP 9: Install Python Dependencies**

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt
```

This will take a few minutes. You'll see packages being installed.

### **STEP 10: Start Docker Desktop**

1. Open Docker Desktop application
2. Wait for it to fully start (whale icon should be steady)
3. Verify it's running:

```bash
docker --version
```

You should see something like: `Docker version 20.x.x`

### **STEP 11: Start Milvus Vector Database**

```bash
# Start Milvus
docker-compose up -d

# Wait 30-60 seconds for Milvus to initialize

# Check if containers are running
docker ps
```

You should see three containers running:
- milvus-standalone
- milvus-etcd
- milvus-minio

**Troubleshooting:**
If containers fail to start:
```bash
# Stop everything
docker-compose down

# Remove volumes
docker-compose down -v

# Start again
docker-compose up -d
```

### **STEP 12: Verify Installation**

Create a test script `test_setup.py`:

```python
import sys

def test_imports():
    try:
        import streamlit
        import google.generativeai
        import pymilvus
        from dotenv import load_dotenv
        import os
        
        load_dotenv()
        
        api_key = os.getenv('GOOGLE_API_KEY')
        
        if not api_key:
            print("❌ Google API Key not found in .env")
            return False
        
        if api_key == 'YOUR_API_KEY_HERE':
            print("❌ Please replace YOUR_API_KEY_HERE with actual API key")
            return False
        
        print("✅ All imports successful")
        print("✅ Google API Key found")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

if __name__ == "__main__":
    if test_imports():
        print("\n🎉 Setup verified successfully!")
        print("\nNext step: Run 'streamlit run app.py'")
    else:
        print("\n❌ Setup has issues. Please check the errors above.")
        sys.exit(1)
```

Run the test:

```bash
python test_setup.py
```

### **STEP 13: Launch the Application**

```bash
streamlit run app.py
```

The app should open in your browser at `http://localhost:8501`

---

## 🎮 Using the Application

### **1. Upload Documents**

1. Click "Browse files" in the sidebar
2. Select one or more files (PDF, DOCX, PPTX, XLSX, TXT)
3. Click "Process Documents"
4. Wait for processing to complete

### **2. Ask Questions**

1. Type your question in the chat input
2. Press Enter
3. Watch as the system:
   - Routes to appropriate agent
   - Retrieves relevant context
   - Generates answer

### **3. View Results**

Each answer shows:
- **Agent Used**: Which specialized agent handled the query
- **Confidence Score**: How confident the system is
- **Sources**: Which documents were used
- **Context**: Actual text chunks retrieved

---

## 🔧 Common Issues & Solutions

### Issue: "Module not found"
**Solution:**
```bash
pip install -r requirements.txt --force-reinstall
```

### Issue: "Cannot connect to Milvus"
**Solution:**
```bash
# Check Docker containers
docker ps

# Restart Milvus
docker-compose restart

# If still fails, recreate
docker-compose down -v
docker-compose up -d
```

### Issue: "Invalid API key"
**Solution:**
- Verify your API key in .env file
- Get new key from Google AI Studio
- Make sure there are no extra spaces

### Issue: "Port already in use"
**Solution:**
```bash
# Kill process on port 8501
# Windows
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:8501 | xargs kill -9
```

---

## 📊 Testing the System

### Test 1: Upload Sample Document

1. Upload `data/sample/company_policy.txt`
2. Ask: "What is the remote work policy?"
3. Verify: Should get accurate answer from the document

### Test 2: Test Agent Routing

1. Upload both text and Excel files
2. Ask: "What are the sales figures?" (should route to ExcelAgent)
3. Ask: "What is the company policy?" (should route to DocumentAgent)

### Test 3: Test Multiple Documents

1. Upload 3-5 different documents
2. Ask questions that require information from multiple sources
3. Verify: System retrieves context from relevant documents

---

## 📝 Creating Your GitHub Repository

```bash
# Stage all files
git add .

# Commit
git commit -m "Initial commit: Agentic RAG System"

# Create repo on GitHub (do this in browser first)
# Then link and push
git remote add origin https://github.com/YOUR_USERNAME/agentic-rag-system.git
git branch -M main
git push -u origin main
```

---

## 🎥 Recording Demo Video

### What to Show (3 minutes):

**Minute 1: System Overview**
- Show the UI
- Explain the architecture briefly
- Show available agents

**Minute 2: Document Upload & Processing**
- Upload sample documents
- Show processing progress
- Show database stats

**Minute 3: Query Processing**
- Ask 2-3 different types of questions
- Show agent routing
- Show context retrieval
- Display final answers

### Recording Tools:
- **Windows**: Xbox Game Bar (Win + G)
- **Mac**: QuickTime Player
- **Cross-platform**: OBS Studio (free)

---

## 📧 Submission Checklist

Before submitting, verify:

- [ ] All code is on GitHub (public repo)
- [ ] README.md is complete
- [ ] requirements.txt is included
- [ ] .env.example is included (not .env!)
- [ ] Sample data is included
- [ ] Code is well-commented
- [ ] System Design Document (PDF) is ready
- [ ] Video is recorded and uploaded
- [ ] Video link is accessible

---

## 🎓 Next Steps & Improvements

After completing the basic project, consider:

1. **Add more document types**: HTML, Markdown, etc.
2. **Implement caching**: Speed up repeated queries
3. **Add conversation memory**: Multi-turn conversations
4. **Better UI**: Add charts, visualizations
5. **Deploy**: Deploy to cloud (Streamlit Cloud, AWS, etc.)
6. **MCP Integration**: Add MCP servers for bonus points

---

## 🆘 Getting Help

If you encounter issues:

1. Check the logs in `logs/` folder
2. Review error messages carefully
3. Google the specific error
4. Check Milvus documentation
5. Check Streamlit documentation

---

## ✅ Final Verification

Run this checklist before submission:

```bash
# 1. Test installation
python test_setup.py

# 2. Start application
streamlit run app.py

# 3. Upload document
# 4. Ask question
# 5. Verify answer

# 6. Check GitHub
git status
git log

# 7. Verify all files are committed
```

---

**Good luck with your project! 🚀**
