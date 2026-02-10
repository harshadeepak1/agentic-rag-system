# Video Demonstration Script
## Agentic RAG System (~3 minutes)

---

## 🎬 Pre-Recording Checklist

Before you start recording:
- [ ] Application is running (`streamlit run app.py`)
- [ ] Sample documents ready to upload
- [ ] Browser window maximized
- [ ] No sensitive information visible
- [ ] Microphone tested
- [ ] Screen recording software ready (OBS/QuickTime/Xbox Game Bar)
- [ ] Close unnecessary tabs/applications

---

## 📝 Script Timeline

### [0:00 - 0:20] Introduction (20 seconds)

**What to show**: Your face or avatar, project title slide

**Script**:
> "Hello! I'm [Your Name], and today I'll be demonstrating my Agentic RAG System - an intelligent document question-answering system powered by specialized AI agents. This system can process multiple document formats and provide accurate, context-aware answers. Let's dive in!"

**Actions**:
- Show title screen with project name
- Show your name
- Quick smile/wave

---

### [0:20 - 0:50] Architecture Overview (30 seconds)

**What to show**: System architecture diagram (from design doc) or draw it

**Script**:
> "The system uses a multi-agent architecture. At the top, we have a Router Agent that analyzes incoming queries and routes them to specialized agents - a Document Agent for text documents, an Excel Agent for spreadsheet data, and a QA Agent for general questions. 
>
> All agents retrieve context from our Milvus vector database and use Google Gemini to generate answers. This agentic approach ensures each query gets the most appropriate specialist."

**Actions**:
- Show/draw architecture diagram
- Point to each component as you mention it
- Highlight the flow from query to answer

**Visual Aid** (can be simple):
```
User Query
    ↓
Router Agent
    ↓
[Document | Excel | QA] Agents
    ↓
Vector DB + LLM
    ↓
Answer
```

---

### [0:50 - 1:30] Document Upload Demo (40 seconds)

**What to show**: Streamlit app interface

**Script**:
> "Let me show you how it works. First, I'll upload some documents. The system supports PDF, Word, PowerPoint, Excel, and text files.
>
> [Upload 2-3 files]
>
> I'll click 'Process Documents' and you can see the system extracting text, generating embeddings, and storing them in the vector database.
>
> [Point to progress]
>
> Great! We now have [X] chunks stored in our database."

**Actions**:
1. Click "Browse files"
2. Select 2-3 different file types
3. Click "Process Documents"
4. Show progress bar
5. Point to success message
6. Show database stats increasing

**Files to use**:
- company_policy.txt
- (Add a sample PDF if you have one)
- (Add a sample XLSX if you have one)

---

### [1:30 - 2:30] Query Processing Demo (60 seconds)

**What to show**: Chat interface with queries and responses

**Script**:
> "Now let's ask some questions. First, a document-based question:
>
> [Type: 'What is the remote work policy?']
>
> Notice the Router Agent selected the Document Agent, retrieved relevant context from our policy document, and generated this accurate answer with source citations.
>
> Let me try a data question:
>
> [Type: 'What are the total sales figures?' OR another data question]
>
> This time, the Excel Agent was selected because the query relates to spreadsheet data.
>
> Finally, a general question:
>
> [Type: 'What are the benefits of remote work?']
>
> The system intelligently combines information from multiple sources and provides a comprehensive answer."

**Actions**:
1. Clear chat or start fresh
2. Type first question slowly
3. Show the answer appearing
4. Expand "Agent Used" - highlight DocumentAgent
5. Expand "Sources" - show document name
6. Expand "Context" - show retrieved chunks
7. Type second question
8. Show ExcelAgent being used
9. Type third question
10. Show combined answer

**Queries to use**:
- Query 1 (Document): "What is the remote work policy?" or "What are the work hours?"
- Query 2 (Excel): "What are the sales trends?" or "Show me the data summary"
- Query 3 (General): "What are the benefits mentioned in the documents?"

---

### [2:30 - 2:50] Show Agent Routing (20 seconds)

**What to show**: Zoom in on agent badges and routing

**Script**:
> "What makes this system 'agentic' is this intelligent routing. Each query is automatically directed to the most appropriate specialist, ensuring high-quality, context-aware responses.
>
> You can see which agent handled each query, along with confidence scores and source documents."

**Actions**:
- Scroll through previous queries
- Point to agent badges (different colors)
- Point to confidence scores
- Show sources cited

---

### [2:50 - 3:10] Conclusion (20 seconds)

**What to show**: Back to you or final slide

**Script**:
> "This Agentic RAG system demonstrates how specialized AI agents can work together to provide intelligent document analysis. The system is production-ready, scalable, and can be easily extended with additional agents or document types.
>
> Thank you for watching! The complete code and documentation are available on GitHub."

**Actions**:
- Show GitHub URL briefly (optional)
- Quick summary of key features:
  * Multi-format support ✓
  * Intelligent routing ✓
  * Source attribution ✓
  * Clean UI ✓

---

## 🎨 Visual Tips

### During Recording:
1. **Speak clearly and at moderate pace**
2. **Use your cursor to point at important elements**
3. **Pause briefly between sections**
4. **Show enthusiasm but stay professional**
5. **Keep browser at 100% zoom for readability**

### Screen Layout:
```
┌──────────────────────────────────────┐
│  Browser - Streamlit App (75%)       │
│  ┌────────────────────────────────┐  │
│  │                                │  │
│  │    Your App Interface          │  │
│  │                                │  │
│  └────────────────────────────────┘  │
│                                       │
│  Optional: Terminal/Logs (25%)       │
└──────────────────────────────────────┘
```

---

## 🎯 Key Points to Emphasize

1. **Multi-agent architecture** - specialized agents for different tasks
2. **Intelligent routing** - automatic agent selection
3. **Multiple document formats** - PDF, DOCX, PPTX, XLSX, TXT
4. **Source attribution** - shows where answers come from
5. **Vector database** - Milvus for efficient retrieval
6. **Clean UI** - easy to use interface

---

## ⚠️ Common Mistakes to Avoid

- ❌ Talking too fast
- ❌ Not showing enough of the actual system working
- ❌ Spending too long on any one section
- ❌ Having errors during demo (test first!)
- ❌ Poor audio quality
- ❌ Screen too small to read
- ❌ Going over 3 minutes

---

## 🎬 Recording Tools

### Windows:
- **Xbox Game Bar**: Win + G (built-in, easy)
- **OBS Studio**: More professional, free
- **PowerPoint**: Has screen recording feature

### Mac:
- **QuickTime Player**: Built-in, simple
- **OBS Studio**: More professional, free
- **Screenshot app**: Shift + Cmd + 5

### Online:
- **Loom**: Easy, automatic upload
- **Zoom**: Record yourself presenting

---

## 📤 After Recording

1. **Review the video**
   - Watch it fully
   - Check audio quality
   - Verify everything is visible
   - Confirm time is under 3 minutes

2. **Edit if needed**
   - Trim awkward pauses
   - Add title slide (optional)
   - Add subtitles (optional but helpful)

3. **Upload**
   - YouTube (unlisted or public)
   - Google Drive (public link)
   - Vimeo
   - Loom

4. **Test the link**
   - Open in incognito/private window
   - Verify it plays
   - Confirm audio works

---

## 📋 Video Upload Checklist

- [ ] Video is under 3 minutes
- [ ] Audio is clear
- [ ] Screen is readable (720p minimum)
- [ ] All features demonstrated
- [ ] Uploaded successfully
- [ ] Link is publicly accessible
- [ ] Link is tested in incognito mode

---

## 💡 Pro Tips

1. **Do a practice run** without recording first
2. **Have your script visible** but don't read robotically
3. **Smile** - even if people can't see you, it affects your voice
4. **Speak to the camera** like you're explaining to a friend
5. **Don't worry about being perfect** - authenticity is good
6. **Show, don't just tell** - demonstrate features actively
7. **End strong** - leave viewers impressed

---

## 🎓 Alternative Format (If Nervous About Voice)

You can also create:
1. **Screen recording with text overlays**
2. **Presentation-style with bullet points**
3. **Animated diagram with captions**

But voice narration is recommended as it's more personal and engaging!

---

**You've got this! 🎬**

The key is to show your system works, explain how it works, and demonstrate why the agentic approach is valuable. Good luck!
