"""Streamlit UI for the Agentic RAG System."""

import streamlit as st
from pathlib import Path
import time
from typing import List
import os

from core import document_processor, embedding_generator, vector_store
from agents import router_agent
from utils import config, logger

# Page configuration
st.set_page_config(
    page_title="Agentic RAG System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .agent-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 0.25rem;
        font-weight: 600;
        font-size: 0.875rem;
        margin: 0.25rem;
    }
    .document-agent {
        background-color: #d4edda;
        color: #155724;
    }
    .excel-agent {
        background-color: #d1ecf1;
        color: #0c5460;
    }
    .qa-agent {
        background-color: #fff3cd;
        color: #856404;
    }
    .source-box {
        background-color: #f8f9fa;
        border-left: 3px solid #1f77b4;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0.25rem;
    }
    .confidence-high {
        color: #28a745;
        font-weight: bold;
    }
    .confidence-medium {
        color: #ffc107;
        font-weight: bold;
    }
    .confidence-low {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'documents_processed' not in st.session_state:
        st.session_state.documents_processed = False
    if 'total_chunks' not in st.session_state:
        st.session_state.total_chunks = 0


def process_uploaded_files(uploaded_files):
    """Process uploaded files and add to vector store."""
    try:
        with st.spinner("Processing documents..."):
            all_chunks = []
            all_embeddings = []
            all_metadatas = []
            
            progress_bar = st.progress(0)
            
            for idx, uploaded_file in enumerate(uploaded_files):
                # Save uploaded file temporarily
                temp_path = Path(f"/tmp/{uploaded_file.name}")
                temp_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Process file
                try:
                    result = document_processor.process_file(str(temp_path))
                    
                    chunks = result['chunks']
                    metadatas = result['metadatas']
                    
                    # Generate embeddings
                    st.info(f"Generating embeddings for {uploaded_file.name}...")
                    embeddings = embedding_generator.generate_embeddings(chunks)
                    
                    all_chunks.extend(chunks)
                    all_embeddings.extend(embeddings)
                    all_metadatas.extend(metadatas)
                    
                    # Clean up temp file
                    temp_path.unlink()
                    
                except Exception as e:
                    st.error(f"Error processing {uploaded_file.name}: {e}")
                    logger.error(f"Error processing {uploaded_file.name}: {e}")
                
                # Update progress
                progress_bar.progress((idx + 1) / len(uploaded_files))
            
            # Insert into vector store
            if all_chunks:
                st.info("Storing documents in vector database...")
                success = vector_store.insert(
                    texts=all_chunks,
                    embeddings=all_embeddings,
                    metadatas=all_metadatas
                )
                
                if success:
                    st.session_state.documents_processed = True
                    st.session_state.total_chunks = len(all_chunks)
                    st.success(f"✅ Successfully processed {len(uploaded_files)} files ({len(all_chunks)} chunks)")
                else:
                    st.error("Failed to store documents in vector database")
            
    except Exception as e:
        st.error(f"Error processing files: {e}")
        logger.error(f"Error in process_uploaded_files: {e}")


def get_agent_badge(agent_name: str) -> str:
    """Get HTML badge for agent."""
    agent_classes = {
        'DocumentAgent': 'document-agent',
        'ExcelAgent': 'excel-agent',
        'QAAgent': 'qa-agent'
    }
    
    agent_class = agent_classes.get(agent_name, 'qa-agent')
    return f'<span class="agent-badge {agent_class}">{agent_name}</span>'


def get_confidence_class(confidence: float) -> str:
    """Get CSS class for confidence score."""
    if confidence >= 0.7:
        return 'confidence-high'
    elif confidence >= 0.4:
        return 'confidence-medium'
    else:
        return 'confidence-low'


def main():
    """Main application."""
    initialize_session_state()
    
    # Validate configuration
    try:
        config.validate()
    except ValueError as e:
        st.error(f"Configuration Error: {e}")
        st.info("Please set up your .env file with required API keys.")
        st.stop()
    
    # Header
    st.markdown('<h1 class="main-header">🤖 Agentic RAG System</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("📁 Document Management")
        
        # File uploader
        uploaded_files = st.file_uploader(
            "Upload Documents",
            type=['pdf', 'docx', 'pptx', 'xlsx', 'txt'],
            accept_multiple_files=True,
            help="Upload PDF, DOCX, PPTX, XLSX, or TXT files"
        )
        
        # Process button
        if uploaded_files:
            if st.button("🚀 Process Documents", type="primary"):
                process_uploaded_files(uploaded_files)
        
        st.divider()
        
        # Database stats
        st.header("📊 Database Stats")
        stats = vector_store.get_stats()
        st.metric("Documents in Database", stats.get('num_documents', 0))
        
        if st.button("🗑️ Clear Database"):
            if st.session_state.total_chunks > 0:
                with st.spinner("Clearing database..."):
                    vector_store.delete_all()
                    st.session_state.documents_processed = False
                    st.session_state.total_chunks = 0
                    st.success("Database cleared successfully")
                    st.rerun()
        
        st.divider()
        
        # Agent information
        st.header("🤖 Available Agents")
        agents_info = router_agent.get_agent_info()
        for agent in agents_info:
            st.markdown(f"**{agent['name']}**")
            st.caption(agent['description'])
        
        st.divider()
        
        # Settings
        st.header("⚙️ Settings")
        top_k = st.slider("Number of context chunks", 1, 10, 5)
    
    # Main chat interface
    st.header("💬 Chat Interface")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            if message["role"] == "assistant" and "metadata" in message:
                metadata = message["metadata"]
                
                # Display agent used
                if "agent" in metadata:
                    st.markdown(
                        f"Agent: {get_agent_badge(metadata['agent'])}",
                        unsafe_allow_html=True
                    )
                
                # Display confidence
                if "confidence" in metadata:
                    confidence = metadata['confidence']
                    confidence_class = get_confidence_class(confidence)
                    st.markdown(
                        f"Confidence: <span class='{confidence_class}'>{confidence:.2%}</span>",
                        unsafe_allow_html=True
                    )
                
                # Display sources
                if "sources" in metadata and metadata["sources"]:
                    with st.expander("📚 Sources"):
                        for source in metadata["sources"]:
                            st.markdown(f"- {source}")
                
                # Display context
                if "context" in metadata and metadata["context"]:
                    with st.expander("🔍 Retrieved Context"):
                        for i, ctx in enumerate(metadata["context"][:3]):
                            st.markdown(f"**Chunk {i+1}** (Score: {ctx.get('score', 0):.3f})")
                            st.markdown(f'<div class="source-box">{ctx["text"][:300]}...</div>', unsafe_allow_html=True)
    
    # Chat input
    if prompt := st.chat_input("Ask a question about your documents..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Process query through router agent
                result = router_agent.process_query(prompt, top_k=top_k)
                
                # Display answer
                answer = result.get('answer', 'I could not generate an answer.')
                st.markdown(answer)
                
                # Display metadata
                agent_name = result.get('agent', 'Unknown')
                st.markdown(
                    f"Agent: {get_agent_badge(agent_name)}",
                    unsafe_allow_html=True
                )
                
                confidence = result.get('confidence', 0.0)
                confidence_class = get_confidence_class(confidence)
                st.markdown(
                    f"Confidence: <span class='{confidence_class}'>{confidence:.2%}</span>",
                    unsafe_allow_html=True
                )
                
                # Display sources
                sources = result.get('sources', [])
                if sources:
                    with st.expander("📚 Sources"):
                        for source in sources:
                            st.markdown(f"- {source}")
                
                # Display context
                context = result.get('context', [])
                if context:
                    with st.expander("🔍 Retrieved Context"):
                        for i, ctx in enumerate(context[:3]):
                            st.markdown(f"**Chunk {i+1}** (Score: {ctx.get('score', 0):.3f})")
                            st.markdown(f'<div class="source-box">{ctx["text"][:300]}...</div>', unsafe_allow_html=True)
        
        # Add assistant message
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "metadata": {
                "agent": agent_name,
                "confidence": confidence,
                "sources": sources,
                "context": context
            }
        })


if __name__ == "__main__":
    main()
