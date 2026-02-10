# 🚀 QUICK START - Complete Implementation in 30 Minutes

This guide will get your Agentic RAG System up and running quickly.

---

## ⚡ Fast Track Setup (For Experienced Developers)

```bash
# 1. Setup
git clone <your-repo>
cd agentic-rag-system
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
# Edit .env and add your Google API key

# 3. Start Database
docker-compose up -d
sleep 30  # Wait for Milvus

# 4. Run
streamlit run app.py
```

---

## 📝 Detailed Step-by-Step (For Beginners)

### STEP 1: Get Google API Key (5 minutes)

1. Go to: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key (looks like: AIzaSy...)
4. Keep it safe!

### STEP 2: Setup Project (10 minutes)

**Option A: Clone from GitHub (if you already created repo)**
```bash
git clone https://github.com/YOUR_USERNAME/agentic-rag-system.git
cd agentic-rag-system
```

**Option B: Create from scratch**
```bash
mkdir agentic-rag-system
cd agentic-rag-system
```

Then download all the files I provided and organize them in this structure:

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
│       └── company_policy.txt
├── app.py
├── requirements.txt
├── docker-compose.yml
├── .env.example
└── README.md
```

### STEP 3: Create Virtual Environment (3 minutes)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal.

### STEP 4: Install Dependencies (5 minutes)

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Wait for installation to complete (will show progress).

### STEP 5: Configure Environment (2 minutes)

1. Copy `.env.example` to `.env`:
   ```bash
   # Windows
   copy .env.example .env
   
   # Mac/Linux
   cp .env.example .env
   ```

2. Edit `.env` file:
   ```
   GOOGLE_API_KEY=YOUR_ACTUAL_API_KEY_HERE
   MILVUS_HOST=localhost
   MILVUS_PORT=19530
   # ... rest stays the same
   ```

### STEP 6: Start Milvus (3 minutes)

```bash
docker-compose up -d
```

Wait 30 seconds for Milvus to initialize.

Verify it's running:
```bash
docker ps
```

You should see 3 containers running.

### STEP 7: Launch Application (2 minutes)

```bash
streamlit run app.py
```

Browser will open automatically at http://localhost:8501

---

## ✅ Verify Everything Works

### Test 1: Upload Document
1. Click "Browse files" in sidebar
2. Upload `data/sample/company_policy.txt`
3. Click "Process Documents"
4. Should see: "Successfully processed 1 files"

### Test 2: Ask Question
1. Type: "What is the remote work policy?"
2. Press Enter
3. Should get answer about remote work
4. Check agent badge shows "DocumentAgent"

### Test 3: View Context
1. Expand "Retrieved Context"
2. Should see text chunks from the document
3. Check confidence score is displayed

**If all three tests pass: ✅ Your system is working!**

---

## 🐛 Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt --force-reinstall
```

### "Cannot connect to Milvus"
```bash
docker-compose restart
# Wait 30 seconds
```

### "Invalid API key"
- Check .env file
- Make sure no extra spaces
- Get new key from Google AI Studio

### App won't start
```bash
# Check if port 8501 is free
# Windows
netstat -ano | findstr :8501

# Mac/Linux  
lsof -i:8501

# If occupied, kill the process or use different port
streamlit run app.py --server.port 8502
```

---

## 📚 What Each File Does

| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit UI |
| `agents/router_agent.py` | Routes queries to correct agent |
| `agents/document_agent.py` | Handles document questions |
| `agents/excel_agent.py` | Handles spreadsheet questions |
| `agents/qa_agent.py` | Handles general questions |
| `core/vector_store.py` | Milvus database operations |
| `core/embeddings.py` | Generate vector embeddings |
| `core/llm.py` | Google Gemini interface |
| `core/document_processor.py` | Extract text from files |
| `utils/config.py` | Configuration management |
| `utils/logger.py` | Logging setup |

---

## 🎯 Quick Test Queries

Try these after uploading documents:

**Document Questions:**
- "What is the remote work policy?"
- "What are the work hours?"
- "What equipment is provided?"

**Excel Questions (if you upload Excel):**
- "What are the sales figures?"
- "Show me the data summary"
- "What are the trends?"

**General Questions:**
- "What are the benefits of remote work?"
- "Summarize the main points"

---

## 📊 Understanding the Output

When you ask a question, you'll see:

1. **Agent Used**: Which specialist handled it
   - 🟢 DocumentAgent = Text documents
   - 🔵 ExcelAgent = Spreadsheets  
   - 🟡 QAAgent = General questions

2. **Confidence Score**: How sure the system is
   - Green (70-100%) = High confidence
   - Yellow (40-70%) = Medium confidence
   - Red (0-40%) = Low confidence

3. **Sources**: Which documents were used

4. **Context**: Actual text chunks retrieved

---

## 🎬 Record Your Demo Video

### Before Recording:
1. Have app running
2. Upload 2-3 documents
3. Prepare 3-4 questions
4. Close unnecessary tabs

### During Recording (3 minutes):
1. **Intro** (20s): Hi, I'm [name], this is my Agentic RAG System
2. **Architecture** (30s): Show how agents work together
3. **Upload** (40s): Upload and process documents
4. **Query** (60s): Ask questions, show routing
5. **Conclusion** (30s): Summary and thank you

### Recording Tools:
- **Windows**: Win + G (Xbox Game Bar)
- **Mac**: Shift + Cmd + 5
- **Online**: Loom.com (easiest!)

---

## 📤 Submit Your Project

### Checklist:
- [ ] Code on GitHub (public repo)
- [ ] README complete
- [ ] Video recorded (<3 min)
- [ ] Video uploaded (YouTube/Drive)
- [ ] System design PDF ready
- [ ] All links work

### Email Template:
```
Subject: AI Engineer Assignment - [Your Name]

Dear Hiring Team,

Please find my Agentic RAG System submission:

GitHub Repository: [your-repo-url]
Demo Video: [your-video-url]
System Design: [attached/linked]

Key Features:
- Multi-agent architecture
- Supports PDF, DOCX, PPTX, XLSX, TXT
- Milvus vector database
- Google Gemini LLM
- Clean Streamlit UI

Thank you for your consideration.

Best regards,
[Your Name]
[Your Contact]
```

---

## 🎓 Next Steps (Optional Improvements)

After basic submission:
1. Add more document types
2. Implement conversation history
3. Add export functionality
4. Better error messages
5. Deploy to cloud
6. Add MCP servers

---

## 💡 Pro Tips

1. **Test everything twice** before recording
2. **Keep it simple** - don't overcomplicate
3. **Document as you go** - don't leave it for last
4. **Ask questions early** if stuck
5. **Have fun!** This is a cool project

---

## 📞 Help & Resources

- **Streamlit Docs**: https://docs.streamlit.io
- **Milvus Docs**: https://milvus.io/docs
- **Google AI Docs**: https://ai.google.dev/docs
- **Python Docs**: https://docs.python.org

---

## ✨ You're Ready!

Follow this guide step-by-step and you'll have a working Agentic RAG System in about 30 minutes. Take your time, test thoroughly, and good luck!

**Remember**: The goal is to demonstrate understanding of:
- Agentic systems
- RAG architecture
- Vector databases
- Multiple document types
- Clean code structure

You've got all the code. Now just set it up, test it, and show it off! 🚀

---

**Need help?** Review the detailed SETUP_GUIDE.md or CHECKLIST.md files for more information.
