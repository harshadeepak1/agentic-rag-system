# System Design Document
## Agentic RAG System

---

## Executive Summary

This document describes the architecture and design of an Agentic RAG (Retrieval-Augmented Generation) system that uses specialized AI agents to intelligently process and answer questions from multiple document formats. The system employs a router-based architecture where queries are automatically directed to the most appropriate specialist agent, enabling accurate and context-aware responses.

---

## 1. System Architecture

### 1.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface                          │
│                      (Streamlit Web App)                        │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Router Agent                             │
│              (Query Classification & Routing)                   │
└────┬──────────────────┬──────────────────┬─────────────────────┘
     │                  │                  │
     ▼                  ▼                  ▼
┌─────────┐      ┌─────────────┐    ┌──────────┐
│Document │      │    Excel    │    │    QA    │
│ Agent   │      │    Agent    │    │  Agent   │
└────┬────┘      └──────┬──────┘    └─────┬────┘
     │                  │                  │
     └──────────────────┼──────────────────┘
                        │
                        ▼
           ┌────────────────────────┐
           │   Retrieval Pipeline   │
           └────────────────────────┘
                        │
            ┌───────────┴───────────┐
            │                       │
            ▼                       ▼
    ┌──────────────┐        ┌──────────────┐
    │    Vector    │        │     LLM      │
    │  Database    │        │   (Gemini)   │
    │  (Milvus)    │        └──────────────┘
    └──────────────┘
            ▲
            │
    ┌──────────────┐
    │  Document    │
    │  Processor   │
    └──────────────┘
```

### 1.2 Component Description

#### **1.2.1 User Interface Layer**
- **Technology**: Streamlit
- **Purpose**: Provides interactive web interface for document upload and querying
- **Features**:
  - File upload with validation
  - Real-time chat interface
  - Progress indicators
  - Result visualization with sources and confidence scores

#### **1.2.2 Agent Layer**
Four specialized agents working in coordination:

**Router Agent**
- **Role**: Central orchestrator
- **Function**: Analyzes incoming queries and routes to appropriate specialist agent
- **Decision Making**: Uses LLM-based classification with predefined categories

**Document Agent**
- **Specialization**: PDF, DOCX, PPTX, TXT files
- **Strength**: Text comprehension and information extraction
- **Context**: Focuses on written content, policies, presentations

**Excel Agent**
- **Specialization**: XLSX files
- **Strength**: Numerical analysis, data patterns, statistics
- **Context**: Handles tabular data, calculations, trends

**QA Agent**
- **Specialization**: General questions
- **Strength**: Fallback handler and general knowledge
- **Context**: Non-document specific queries

#### **1.2.3 Core Processing Layer**

**Document Processor**
- Extracts text from multiple formats
- Implements format-specific parsers
- Performs text chunking with overlap
- Maintains document metadata

**Embedding Generator**
- Uses Google's embedding-001 model
- Generates 768-dimensional vectors
- Implements batch processing
- Handles both documents and queries

**Vector Store (Milvus)**
- Stores document embeddings
- Performs similarity search
- Uses COSINE metric
- IVF_FLAT index for efficiency

**LLM Interface**
- Google Gemini 1.5 Flash
- Handles text generation
- Query classification
- Answer synthesis

---

## 2. Agentic Workflow Design

### 2.1 Query Processing Flow

```
User Query
    │
    ▼
┌───────────────────────────────────┐
│  1. QUERY ANALYSIS                │
│  - Extract intent                 │
│  - Identify key terms             │
│  - Determine query type           │
└────────────┬──────────────────────┘
             │
             ▼
┌───────────────────────────────────┐
│  2. AGENT ROUTING                 │
│  - LLM-based classification       │
│  - Route to specialist agent      │
│  Decision factors:                │
│    • Keywords (data, numbers)     │
│    • Document types available     │
│    • Query structure              │
└────────────┬──────────────────────┘
             │
             ▼
┌───────────────────────────────────┐
│  3. CONTEXT RETRIEVAL             │
│  - Generate query embedding       │
│  - Search vector database         │
│  - Retrieve top-k chunks          │
│  - Filter by metadata (optional)  │
└────────────┬──────────────────────┘
             │
             ▼
┌───────────────────────────────────┐
│  4. RERANKING                     │
│  - Score by relevance             │
│  - Sort by similarity             │
│  - Select top-3 chunks            │
└────────────┬──────────────────────┘
             │
             ▼
┌───────────────────────────────────┐
│  5. ANSWER GENERATION             │
│  - Construct prompt               │
│  - Add agent-specific context     │
│  - Generate response via LLM      │
│  - Include source attribution     │
└────────────┬──────────────────────┘
             │
             ▼
┌───────────────────────────────────┐
│  6. RESPONSE VALIDATION           │
│  - Calculate confidence score     │
│  - Verify source references       │
│  - Format final output            │
└────────────┬──────────────────────┘
             │
             ▼
        User Response
```

### 2.2 Agentic Behavior Characteristics

**Autonomy**
- Agents independently decide on retrieval strategy
- Self-select relevant context chunks
- Adjust search parameters based on query type

**Reactivity**
- Real-time response to user queries
- Dynamic routing based on query analysis
- Adaptive confidence scoring

**Proactivity**
- Reranking to improve relevance
- Multi-source context aggregation
- Source verification and attribution

**Social Ability**
- Router coordinates with specialists
- Agents share common retrieval infrastructure
- Unified response format

---

## 3. Context Construction Strategy

### 3.1 Document Processing

**Chunking Strategy**
```
Parameters:
- Chunk Size: 1000 characters
- Overlap: 200 characters
- Break Points: Sentence boundaries when possible

Rationale:
- 1000 chars provides sufficient context
- 200 char overlap prevents information loss
- Sentence boundaries maintain semantic coherence
```

**Metadata Enrichment**
```python
metadata = {
    'source': filename,
    'file_type': extension,
    'chunk_index': position,
    'total_chunks': count
}
```

### 3.2 Embedding Generation

**Model**: Google embedding-001
- **Dimension**: 768
- **Task Types**:
  - `retrieval_document` for documents
  - `retrieval_query` for queries
- **Batch Processing**: 100 texts per batch

### 3.3 Retrieval Strategy

**Primary Retrieval**
1. Generate query embedding
2. COSINE similarity search in Milvus
3. Retrieve top-5 candidates
4. Apply metadata filters if specified

**Reranking**
1. Score results by similarity
2. Select top-3 for context
3. Maintain source diversity

**Context Assembly**
```
Context Window:
[Source 1] chunk_text_1
[Source 2] chunk_text_2
[Source 3] chunk_text_3

Total: ~3000 characters
Fits comfortably in LLM context window
```

---

## 4. Technology Choices and Rationale

### 4.1 Core Technologies

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Vector DB | Milvus | - Open source<br>- High performance<br>- Scalable<br>- Rich feature set |
| LLM | Google Gemini 1.5 Flash | - Free tier available<br>- Fast inference<br>- Good quality<br>- Multimodal capable |
| Embeddings | Google embedding-001 | - Compatible with Gemini<br>- 768 dimensions (efficient)<br>- Task-specific modes |
| UI Framework | Streamlit | - Rapid development<br>- Python-native<br>- Rich components<br>- Easy deployment |
| Document Parsing | PyPDF2, python-docx, python-pptx, openpyxl | - Mature libraries<br>- Good format coverage<br>- Active maintenance |

### 4.2 Design Patterns

**Agent Pattern**
- Enables specialization
- Improves answer quality
- Allows independent scaling
- Facilitates testing

**Repository Pattern**
- Single interface to vector store
- Abstracts storage complexity
- Enables easy replacement

**Strategy Pattern**
- Different processing per file type
- Pluggable parsers
- Easy to extend

---

## 5. Key Design Decisions

### 5.1 Agent Architecture

**Decision**: Multi-agent system with router
**Alternatives Considered**:
- Single general-purpose agent
- Pipeline-based processing

**Rationale**:
- Specialized agents provide better accuracy
- Router enables intelligent task distribution
- Modular design allows independent improvements
- Better error isolation

### 5.2 Chunking Strategy

**Decision**: 1000 chars with 200 overlap
**Alternatives Considered**:
- 500 chars / 100 overlap (more granular)
- 2000 chars / 400 overlap (more context)

**Rationale**:
- Balance between context and precision
- Fits LLM context window efficiently
- Overlap prevents information loss at boundaries
- Performs well across document types

### 5.3 Embedding Model

**Decision**: Google embedding-001
**Alternatives Considered**:
- OpenAI ada-002
- Sentence-transformers

**Rationale**:
- Free tier available
- Integrated with Gemini ecosystem
- Good performance/cost ratio
- Task-specific modes improve retrieval

### 5.4 Reranking Approach

**Decision**: Simple score-based sorting
**Alternatives Considered**:
- Cross-encoder reranking
- LLM-based relevance scoring

**Rationale**:
- Sufficient for current scope
- Low latency impact
- Can be upgraded later
- Embedding quality makes it effective

---

## 6. Data Flow

### 6.1 Document Ingestion Flow

```
File Upload
    │
    ▼
Format Detection
    │
    ▼
Text Extraction
(Format-specific parser)
    │
    ▼
Text Cleaning
(Remove extra spaces, normalize)
    │
    ▼
Chunking
(1000 chars, 200 overlap)
    │
    ▼
Embedding Generation
(Batch processing)
    │
    ▼
Metadata Creation
    │
    ▼
Vector Store Insertion
(Milvus with COSINE index)
```

### 6.2 Query Processing Flow

```
User Query
    │
    ▼
Router Analysis
(LLM classification)
    │
    ├─→ Document Agent
    ├─→ Excel Agent
    └─→ QA Agent
         │
         ▼
    Query Embedding
         │
         ▼
    Vector Search
    (Top-5 retrieval)
         │
         ▼
    Reranking
    (Top-3 selection)
         │
         ▼
    Prompt Construction
         │
         ▼
    LLM Generation
         │
         ▼
    Response + Sources
```

---

## 7. Error Handling Strategy

### 7.1 Input Validation
- File type checking
- File size limits (50MB)
- Encoding validation
- Empty file detection

### 7.2 Processing Errors
- Retry logic with exponential backoff
- Graceful degradation
- User-friendly error messages
- Detailed logging

### 7.3 Failure Recovery
- Vector store connection retry
- API rate limit handling
- Partial result return
- Fallback responses

---

## 8. Performance Considerations

### 8.1 Optimization Strategies

**Embedding Generation**
- Batch processing (100 texts)
- Async processing potential
- Caching for repeated texts

**Vector Search**
- IVF_FLAT index (fast search)
- Appropriate nlist parameter (128)
- COSINE metric (normalized vectors)

**LLM Calls**
- Temperature tuning per use case
- Token limit optimization
- Prompt engineering for conciseness

### 8.2 Scalability

**Current Design**: Single-user / Small team
**Scale-up Path**:
1. Add Milvus clustering
2. Implement caching layer (Redis)
3. Async processing queues
4. Load balancing for web tier
5. Distributed embedding generation

---

## 9. Security Considerations

### 9.1 Data Protection
- API keys in environment variables
- No credentials in code
- .env excluded from git

### 9.2 Input Sanitization
- File type validation
- Size limits
- Content scanning (future)

### 9.3 Access Control
- Currently single-user
- Future: User authentication
- Future: Document-level permissions

---

## 10. Limitations

### 10.1 Current Limitations

**Document Processing**
- Max file size: 50MB
- No OCR for scanned PDFs
- Limited to English language optimization
- No image extraction from documents

**Vector Search**
- No hybrid search (keyword + semantic)
- Basic metadata filtering
- No query expansion

**Agents**
- No conversation memory
- No multi-turn context
- No tool use capabilities

**Scalability**
- Single Milvus instance
- Synchronous processing
- No caching layer
- Limited to local deployment

### 10.2 Known Issues

- Large Excel files may timeout
- Complex PDF layouts may lose structure
- Requires stable Milvus connection
- API rate limits on high volume

---

## 11. Future Enhancements

### 11.1 Short-term (Next Iteration)

1. **Conversation Memory**
   - Store chat history
   - Multi-turn context awareness
   - Session management

2. **Hybrid Search**
   - Combine semantic + keyword search
   - BM25 integration
   - Better recall for specific terms

3. **Query Expansion**
   - Synonym expansion
   - Related terms
   - Better coverage

### 11.2 Long-term (Future Versions)

1. **MCP Server Integration**
   - File system access
   - External tool use
   - API integrations

2. **Advanced Retrieval**
   - Query decomposition
   - Multi-hop reasoning
   - Graph-based retrieval

3. **Self-improvement**
   - Feedback loop
   - Active learning
   - Quality metrics

4. **Multi-modal Support**
   - Image understanding
   - Audio transcription
   - Video processing

---

## 12. Testing Strategy

### 12.1 Unit Tests
- Document processor (each format)
- Embedding generation
- Vector store operations
- Agent routing logic

### 12.2 Integration Tests
- End-to-end query flow
- Multi-document retrieval
- Agent coordination
- Error scenarios

### 12.3 Performance Tests
- Large file processing
- Concurrent queries
- Memory usage
- Response latency

---

## 13. Deployment Considerations

### 13.1 Local Deployment
- Docker Compose for Milvus
- Python virtual environment
- Environment variables
- Port configuration

### 13.2 Cloud Deployment Options

**Option 1: Streamlit Cloud**
- Pros: Easy, free tier, managed
- Cons: Limited resources, public

**Option 2: AWS**
- EC2 for application
- RDS for PostgreSQL (if needed)
- Milvus on EKS or self-hosted
- S3 for document storage

**Option 3: Google Cloud**
- Cloud Run for application
- Vertex AI for embeddings
- Milvus on GKE

---

## 14. Monitoring and Observability

### 14.1 Logging
- Structured logging
- Log levels (INFO, ERROR, DEBUG)
- File-based logs
- Searchable format

### 14.2 Metrics (Future)
- Query latency
- Agent selection distribution
- Confidence score distribution
- Error rates
- Document processing time

### 14.3 Alerting (Future)
- Vector store disconnection
- API quota approaching
- Error rate threshold
- Performance degradation

---

## 15. Cost Analysis

### 15.1 Current Costs

**Free Tier Components**
- Google Gemini API: Free tier (60 queries/min)
- Google Embeddings: Free tier
- Milvus: Open source, self-hosted
- Streamlit: Free for local

**Infrastructure Costs** (if deployed)
- VPS/EC2: $10-50/month
- Storage: $5-10/month
- Total: ~$15-60/month

### 15.2 Scaling Costs

At 1000 users:
- LLM API: ~$100-200/month
- Infrastructure: ~$200-500/month
- Total: ~$300-700/month

---

## 16. Conclusion

This Agentic RAG system demonstrates a production-ready approach to intelligent document question-answering. The multi-agent architecture provides flexibility and specialization, while the modular design allows for easy extension and improvement.

Key achievements:
✅ Multi-format document support
✅ Intelligent agent routing
✅ Efficient vector storage and retrieval
✅ Clean, intuitive UI
✅ Comprehensive error handling
✅ Scalable architecture

The system is ready for immediate use and has a clear path for enhancement based on user needs and feedback.

---

## Appendix A: Technology Stack Summary

| Layer | Components |
|-------|-----------|
| Frontend | Streamlit |
| Backend | Python 3.9+ |
| Agents | Custom agent framework |
| Vector DB | Milvus 2.3.3 |
| LLM | Google Gemini 1.5 Flash |
| Embeddings | Google embedding-001 |
| Doc Parsing | PyPDF2, python-docx, python-pptx, openpyxl |
| Storage | Milvus (vector), Local filesystem (files) |
| Orchestration | Docker Compose |

---

## Appendix B: API Endpoints Reference

**Milvus Connection**
- Host: localhost
- Port: 19530
- Collection: document_collection

**Google AI**
- Embedding API: embedding-001
- LLM API: gemini-1.5-flash
- Rate Limits: 60 queries/minute (free tier)

---

**Document Version**: 1.0
**Last Updated**: 2024
**Author**: AI Engineer Assignment
