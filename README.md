![architecture](https://github.com/user-attachments/assets/1b314c28-ec5e-482f-9b6c-daad5ca92b3c)# RAG Chat — Ask Your Own Documents

A Retrieval-Augmented Generation (RAG) app that lets you chat with your own files. Drop any PDFs, text, or markdown files into `/docs`, index them once, and ask questions in a chat UI — the model answers using only what's in your documents.

Built as a showcase of how RAG works in practice using entirely free tools.

---

## Live demo

> Ask questions about Christian Schmid's CV — try it at [ragchristianschmid.streamlit.app](https://ragchristianschmid.streamlit.app)

![Uploadi<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 580" font-family="ui-sans-serif, system-ui, sans-serif">

  <!-- Background -->
  <rect width="900" height="580" fill="#0F0F14" rx="16"/>

  <!-- Title -->
  <text x="450" y="42" text-anchor="middle" fill="#E2E8F0" font-size="18" font-weight="700" letter-spacing="0.5">RAG Chat — Architecture</text>

  <!-- ── INGEST SECTION ── -->
  <rect x="30" y="64" width="840" height="210" rx="12" fill="#1A1A2E" stroke="#7C3AED" stroke-width="1.5" stroke-opacity="0.4"/>
  <text x="54" y="90" fill="#A78BFA" font-size="11" font-weight="600" letter-spacing="1.5">INGEST  (run once)</text>

  <!-- Node: Docs -->
  <rect x="54" y="104" width="120" height="56" rx="10" fill="#2D1F4E" stroke="#7C3AED" stroke-width="1.5"/>
  <text x="114" y="128" text-anchor="middle" fill="#E2E8F0" font-size="12" font-weight="600">📄 /docs</text>
  <text x="114" y="148" text-anchor="middle" fill="#A78BFA" font-size="10">PDF · TXT · MD</text>

  <!-- Arrow -->
  <line x1="174" y1="132" x2="210" y2="132" stroke="#7C3AED" stroke-width="1.5" marker-end="url(#arrow)"/>

  <!-- Node: Chunker -->
  <rect x="210" y="104" width="130" height="56" rx="10" fill="#2D1F4E" stroke="#7C3AED" stroke-width="1.5"/>
  <text x="275" y="128" text-anchor="middle" fill="#E2E8F0" font-size="12" font-weight="600">✂️ Chunker</text>
  <text x="275" y="148" text-anchor="middle" fill="#A78BFA" font-size="10">800 tokens / 100 overlap</text>

  <!-- Arrow -->
  <line x1="340" y1="132" x2="376" y2="132" stroke="#7C3AED" stroke-width="1.5" marker-end="url(#arrow)"/>

  <!-- Node: Embeddings -->
  <rect x="376" y="104" width="148" height="56" rx="10" fill="#2D1F4E" stroke="#7C3AED" stroke-width="1.5"/>
  <text x="450" y="128" text-anchor="middle" fill="#E2E8F0" font-size="12" font-weight="600">🤗 Embeddings</text>
  <text x="450" y="148" text-anchor="middle" fill="#A78BFA" font-size="10">all-MiniLM-L6-v2 · local</text>

  <!-- Arrow -->
  <line x1="524" y1="132" x2="560" y2="132" stroke="#7C3AED" stroke-width="1.5" marker-end="url(#arrow)"/>

  <!-- Node: ChromaDB -->
  <rect x="560" y="104" width="130" height="56" rx="10" fill="#2D1F4E" stroke="#7C3AED" stroke-width="1.5"/>
  <text x="625" y="128" text-anchor="middle" fill="#E2E8F0" font-size="12" font-weight="600">🗄️ ChromaDB</text>
  <text x="625" y="148" text-anchor="middle" fill="#A78BFA" font-size="10">Vector store · local file</text>

  <!-- Ingest label row -->
  <text x="114" y="186" text-anchor="middle" fill="#64748B" font-size="10">source files</text>
  <text x="275" y="186" text-anchor="middle" fill="#64748B" font-size="10">LangChain splitter</text>
  <text x="450" y="186" text-anchor="middle" fill="#64748B" font-size="10">free · no API key</text>
  <text x="625" y="186" text-anchor="middle" fill="#64748B" font-size="10">persisted to disk</text>

  <!-- Ingest: ingest.py label -->
  <rect x="680" y="104" width="160" height="56" rx="10" fill="#111827" stroke="#374151" stroke-width="1" stroke-dasharray="4 3"/>
  <text x="760" y="128" text-anchor="middle" fill="#6B7280" font-size="11" font-weight="600">ingest.py</text>
  <text x="760" y="148" text-anchor="middle" fill="#4B5563" font-size="10">run to re-index docs</text>

  <!-- ── QUERY SECTION ── -->
  <rect x="30" y="300" width="840" height="250" rx="12" fill="#1A1A2E" stroke="#06B6D4" stroke-width="1.5" stroke-opacity="0.4"/>
  <text x="54" y="326" fill="#67E8F9" font-size="11" font-weight="600" letter-spacing="1.5">QUERY  (every message)</text>

  <!-- Node: User -->
  <rect x="54" y="340" width="120" height="56" rx="10" fill="#0F2744" stroke="#06B6D4" stroke-width="1.5"/>
  <text x="114" y="364" text-anchor="middle" fill="#E2E8F0" font-size="12" font-weight="600">💬 User</text>
  <text x="114" y="384" text-anchor="middle" fill="#67E8F9" font-size="10">types a question</text>

  <!-- Arrow -->
  <line x1="174" y1="368" x2="210" y2="368" stroke="#06B6D4" stroke-width="1.5" marker-end="url(#arrow2)"/>

  <!-- Node: Embed query -->
  <rect x="210" y="340" width="148" height="56" rx="10" fill="#0F2744" stroke="#06B6D4" stroke-width="1.5"/>
  <text x="284" y="364" text-anchor="middle" fill="#E2E8F0" font-size="12" font-weight="600">🤗 Embed query</text>
  <text x="284" y="384" text-anchor="middle" fill="#67E8F9" font-size="10">same local model</text>

  <!-- Arrow -->
  <line x1="358" y1="368" x2="394" y2="368" stroke="#06B6D4" stroke-width="1.5" marker-end="url(#arrow2)"/>

  <!-- Node: ChromaDB retrieve -->
  <rect x="394" y="340" width="130" height="56" rx="10" fill="#0F2744" stroke="#06B6D4" stroke-width="1.5"/>
  <text x="459" y="364" text-anchor="middle" fill="#E2E8F0" font-size="12" font-weight="600">🗄️ ChromaDB</text>
  <text x="459" y="384" text-anchor="middle" fill="#67E8F9" font-size="10">top-5 similar chunks</text>

  <!-- Arrow -->
  <line x1="524" y1="368" x2="560" y2="368" stroke="#06B6D4" stroke-width="1.5" marker-end="url(#arrow2)"/>

  <!-- Node: Groq -->
  <rect x="560" y="340" width="130" height="56" rx="10" fill="#0F2744" stroke="#06B6D4" stroke-width="1.5"/>
  <text x="625" y="364" text-anchor="middle" fill="#E2E8F0" font-size="12" font-weight="600">⚡ Groq LLM</text>
  <text x="625" y="384" text-anchor="middle" fill="#67E8F9" font-size="10">llama-3.1-8b-instant</text>

  <!-- Arrow -->
  <line x1="690" y1="368" x2="726" y2="368" stroke="#06B6D4" stroke-width="1.5" marker-end="url(#arrow2)"/>

  <!-- Node: Streamlit -->
  <rect x="726" y="340" width="120" height="56" rx="10" fill="#0F2744" stroke="#06B6D4" stroke-width="1.5"/>
  <text x="786" y="364" text-anchor="middle" fill="#E2E8F0" font-size="12" font-weight="600">🖥️ Streamlit</text>
  <text x="786" y="384" text-anchor="middle" fill="#67E8F9" font-size="10">streamed answer</text>

  <!-- Query label row -->
  <text x="114" y="422" text-anchor="middle" fill="#64748B" font-size="10">Streamlit UI</text>
  <text x="284" y="422" text-anchor="middle" fill="#64748B" font-size="10">free · no API key</text>
  <text x="459" y="422" text-anchor="middle" fill="#64748B" font-size="10">cosine similarity</text>
  <text x="625" y="422" text-anchor="middle" fill="#64748B" font-size="10">free tier</text>
  <text x="786" y="422" text-anchor="middle" fill="#64748B" font-size="10">write_stream()</text>

  <!-- LangChain orchestration bar -->
  <rect x="54" y="444" width="792" height="32" rx="8" fill="#111827" stroke="#374151" stroke-width="1" stroke-dasharray="4 3"/>
  <text x="450" y="465" text-anchor="middle" fill="#6B7280" font-size="11" font-weight="500">🦜 LangChain — orchestration layer</text>

  <!-- DB vertical connector (ChromaDB shared) -->
  <line x1="625" y1="160" x2="625" y2="220" stroke="#7C3AED" stroke-width="1" stroke-dasharray="4 3" stroke-opacity="0.5"/>
  <line x1="625" y1="220" x2="459" y2="220" stroke="#7C3AED" stroke-width="1" stroke-dasharray="4 3" stroke-opacity="0.5"/>
  <line x1="459" y1="220" x2="459" y2="290" stroke="#7C3AED" stroke-width="1" stroke-dasharray="4 3" stroke-opacity="0.5"/>
  <text x="530" y="216" text-anchor="middle" fill="#64748B" font-size="9">shared vector store</text>

  <!-- Footer -->
  <text x="450" y="562" text-anchor="middle" fill="#374151" font-size="10">github.com/chris017/ragExample · ragchristianschmid.streamlit.app</text>

  <!-- Arrow markers -->
  <defs>
    <marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#7C3AED"/>
    </marker>
    <marker id="arrow2" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#06B6D4"/>
    </marker>
  </defs>

</svg>
ng architecture.svg…]()


---

## How it works

```
┌─────────────────────────────────────────────────────┐
│  INGEST  (run once)                                 │
│                                                     │
│  /docs/*.pdf / *.txt / *.md                         │
│       │                                             │
│       ▼                                             │
│  Split into chunks (800 tokens, 100 overlap)        │
│       │                                             │
│       ▼                                             │
│  Embed with all-MiniLM-L6-v2  (local, free)         │
│       │                                             │
│       ▼                                             │
│  Store vectors in ChromaDB  (local file)            │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  QUERY  (every message)                             │
│                                                     │
│  User question                                      │
│       │                                             │
│       ▼                                             │
│  Embed question  (same local model)                 │
│       │                                             │
│       ▼                                             │
│  Retrieve top-5 most similar chunks from ChromaDB  │
│       │                                             │
│       ▼                                             │
│  Send chunks + question to Groq LLM                │
│       │                                             │
│       ▼                                             │
│  Stream answer back to the user                     │
└─────────────────────────────────────────────────────┘
```

The key idea: the LLM never sees your full documents — only the few chunks most relevant to each question. This keeps responses focused and works even with large document collections.

---

## Stack

| Layer | Tool | Cost |
|---|---|---|
| LLM | [Groq](https://groq.com) — `llama-3.1-8b-instant` | Free tier |
| Embeddings | [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) | Free, runs locally |
| Vector store | [ChromaDB](https://www.trychroma.com) | Free, local file |
| Orchestration | [LangChain](https://langchain.com) | Free, open source |
| UI | [Streamlit](https://streamlit.io) | Free |

---

## Run it yourself

### 1. Clone & set up environment

```bash
git clone https://github.com/your-username/ragFineTune.git
cd ragFineTune

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Get a free Groq API key

Sign up at [console.groq.com](https://console.groq.com) — no credit card required.

```bash
cp .env.example .env
# open .env and add your key:
# GROQ_API_KEY=gsk_...
```

### 3. Add your documents

Drop any `.pdf`, `.txt`, or `.md` files into the `/docs` folder.

### 4. Index your documents

```bash
python ingest.py
```

This chunks your files, embeds them locally, and saves the vectors to `chroma_db/`. Run this again whenever you add new documents.

### 5. Start the app

```bash
streamlit run app.py
```

---

## Deploy to Streamlit Cloud

1. Push the repo to GitHub (the `chroma_db/` folder must be included)
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your repo
3. Set main file to `app.py`
4. Under **Settings → Secrets**, add:

```toml
GROQ_API_KEY = "gsk_..."
```

---

## Adapting this for your own use case

1. **Swap the documents** — replace the files in `/docs` with your own (company docs, notes, a book, anything)
2. **Change the LLM** — swap `ChatGroq` in `app.py` for any LangChain-compatible LLM (`ChatOpenAI`, `ChatAnthropic`, `ChatOllama` for local, etc.)
3. **Tune chunk size** — in `ingest.py`, adjust `chunk_size` and `chunk_overlap` to fit your content (smaller chunks = more precise retrieval, larger = more context per chunk)
4. **Change TOP_K** — in `app.py`, `TOP_K` controls how many chunks are retrieved per question

---

## Project structure

```
ragFineTune/
├── docs/               # Your source documents go here
├── chroma_db/          # Auto-generated vector store (committed for deployment)
├── ingest.py           # Index documents into ChromaDB
├── app.py              # Streamlit chat app
├── inspect_db.ipynb    # Jupyter notebook to inspect stored chunks
├── requirements.txt
├── .env.example
└── .streamlit/
    └── config.toml     # Streamlit theme config
```
