"""
app.py — Streamlit RAG chat app powered by Groq + ChromaDB.
Run with: streamlit run app.py
"""

import os
from pathlib import Path
from typing import Generator

import streamlit as st
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq

load_dotenv()

CHROMA_DIR = Path("chroma_db")
EMBED_MODEL = "all-MiniLM-L6-v2"
GROQ_MODEL = "llama-3.1-8b-instant"
TOP_K = 5
MAX_QUESTIONS = 5  # per session


def get_secret(key: str, default: str = "") -> str:
    try:
        return os.getenv(key) or st.secrets.get(key, default)
    except Exception:
        return os.getenv(key, default)


GROQ_API_KEY = get_secret("GROQ_API_KEY")

st.set_page_config(page_title="RAG Chat", page_icon="🔍", layout="wide")


# --- Sidebar ---

with st.sidebar:
    st.title("RAG Chat")
    st.caption(f"Model: `{GROQ_MODEL}`")
    st.divider()

    st.markdown("**How it works**")
    st.markdown(
        "Your question is matched against document chunks stored in a local vector DB. "
        "The most relevant chunks are passed to the LLM as context."
    )
    st.divider()

    questions_used = st.session_state.get("question_count", 0)
    remaining = MAX_QUESTIONS - questions_used
    st.markdown("**Session usage**")
    st.progress(questions_used / MAX_QUESTIONS, text=f"{remaining}/{MAX_QUESTIONS} questions left")

    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.question_count = 0
        st.rerun()


# --- Main ---

st.title("Ask my documents")


@st.cache_resource(show_spinner="Loading vector store...")
def load_db():
    if not CHROMA_DIR.exists():
        return None
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    return Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=embeddings,
        collection_name="rag_docs",
    )


@st.cache_resource(show_spinner=False)
def get_llm():
    if not GROQ_API_KEY:
        st.error("GROQ_API_KEY not set. Add it to your .env file or Streamlit secrets.")
        st.stop()
    return ChatGroq(api_key=GROQ_API_KEY, model=GROQ_MODEL, temperature=0, streaming=True)


def retrieve_context(db: Chroma, query: str) -> tuple[str, list]:
    results = db.similarity_search(query, k=TOP_K)
    context_parts = []
    sources = []
    for i, doc in enumerate(results, 1):
        source = doc.metadata.get("source", "unknown")
        page = doc.metadata.get("page", "")
        label = f"{Path(source).name}" + (f" (p.{page + 1})" if page != "" else "")
        context_parts.append(f"[{i}] {label}:\n{doc.page_content}")
        sources.append(label)
    return "\n\n".join(context_parts), sources


def stream_response(llm, question: str, context: str) -> Generator:
    system = (
        "You are a helpful assistant. Answer the user's question using ONLY the "
        "provided context. If the context doesn't contain enough information to "
        "answer, say so clearly. Do not make up information.\n\n"
        f"Context:\n{context}"
    )
    for chunk in llm.stream([SystemMessage(content=system), HumanMessage(content=question)]):
        yield chunk.content


# --- UI ---

db = load_db()

if db is None:
    st.warning("No vector store found. Run `python ingest.py` first to index your documents.")
    st.stop()

llm = get_llm()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "question_count" not in st.session_state:
    st.session_state.question_count = 0

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("Sources"):
                for s in msg["sources"]:
                    st.markdown(f"- {s}")

remaining = MAX_QUESTIONS - st.session_state.question_count

if remaining <= 0:
    st.warning("Session limit reached. Click **Clear chat** in the sidebar to start over.")
    st.stop()

# Sample questions — only shown when chat is empty
SAMPLE_QUESTIONS = [
    "Who is Christian Schmid?",
    "What are his main skills?",
    "What is his work experience?",
    "What has he studied?",
]

if not st.session_state.messages:
    st.markdown("**Try asking:**")
    cols = st.columns(len(SAMPLE_QUESTIONS))
    for col, question in zip(cols, SAMPLE_QUESTIONS):
        if col.button(question, use_container_width=True):
            st.session_state["_sample_prompt"] = question
            st.rerun()

prompt = st.session_state.pop("_sample_prompt", None)
if not prompt:
    prompt = st.chat_input("Ask a question about your documents...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.question_count += 1
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.status("Thinking...", expanded=True) as status:
            st.write("Searching vector database...")
            context, sources = retrieve_context(db, prompt)
            st.write(f"Found {len(sources)} relevant chunk(s). Asking the model...")
            status.update(label="Generating answer...", state="running")

        answer = st.write_stream(stream_response(llm, prompt, context))

        if sources:
            with st.expander("Sources"):
                for s in sources:
                    st.markdown(f"- {s}")

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "sources": sources}
    )

    # refresh sidebar progress bar
    st.rerun()
