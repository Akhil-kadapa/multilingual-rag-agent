# 🌐 Multilingual RAG System Agent

> **Search smarter across languages** — An AI-powered document intelligence platform that enables semantic search and question answering across multiple documents in 5 languages.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![Groq](https://img.shields.io/badge/Groq-LLaMA%203.3%2070B-orange.svg)](https://groq.com)
[![FAISS](https://img.shields.io/badge/FAISS-Vector%20DB-green.svg)](https://github.com/facebookresearch/faiss)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [How RAG Works](#how-rag-works)
- [API Configuration](#api-configuration)
- [Deployment](#deployment)
- [Contributing](#contributing)

---

## 🎯 Overview

The **Multilingual RAG System Agent** is a production-ready Retrieval Augmented Generation (RAG) application that allows users to upload documents in any language, receive AI-generated summaries, and ask questions — all in their preferred output language.

Unlike standard RAG implementations, this system features:
- **Cross-language semantic search** — ask questions in English about Hindi documents
- **Real-time RAG evaluation** — every answer is scored 0-100 for faithfulness
- **Automatic failure diagnosis** — identifies whether failures occur in retrieval or generation
- **Dynamic language switching** — change output language mid-session without restarting

**Live Demo:** [multilingual-rag-agent.streamlit.app](https://multilingual-rag-agent.streamlit.app)

---

## ✨ Features

### Core RAG Pipeline
- ✅ **Multi-document support** — Upload multiple PDF and TXT files simultaneously
- ✅ **Intelligent chunking** — 500-character chunks with 50-character overlap to prevent information loss
- ✅ **Semantic embeddings** — Text converted to 384-dimensional vectors using Sentence Transformers
- ✅ **FAISS vector search** — Fast similarity search with L2 distance filtering
- ✅ **Relevance filtering** — Only returns chunks with distance < 2.0 threshold

### Multilingual Intelligence
- ✅ **5 output languages** — English, Telugu, Hindi, French, Spanish
- ✅ **50+ input languages** — Documents in any language supported
- ✅ **Cross-language retrieval** — English questions find answers in Hindi documents
- ✅ **Dynamic switching** — Change language anytime without reprocessing documents

### AI-Powered Features
- ✅ **Auto summarization** — Documents summarized on upload using 4-section sampling
- ✅ **RAG evaluation** — Faithfulness scoring with retrieval vs generation diagnosis
- ✅ **Source citation** — Every answer cites the exact source document
- ✅ **Chat history** — Full conversation maintained within session

### Professional UI
- ✅ **Dark theme** — Professional Streamlit interface
- ✅ **Progress bars** — Real-time processing status with step-by-step feedback
- ✅ **PDF export** — Download complete chat history as formatted PDF
- ✅ **Responsive layout** — Sidebar controls with main chat area

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface (Streamlit)                │
│  ┌─────────────┐              ┌──────────────────────────┐  │
│  │   Sidebar   │              │       Main Area           │  │
│  │             │              │                           │  │
│  │ 📁 Upload   │              │  📄 Document Summaries    │  │
│  │ 🌍 Language │              │  💬 Chat Interface        │  │
│  │ 📊 Stats    │              │  📊 Evaluation Scores     │  │
│  └─────────────┘              └──────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      RAG Pipeline                            │
│                                                             │
│  Documents → Chunking → Embeddings → FAISS → Retrieval      │
│                                          ↓                  │
│                              Groq LLaMA 3.3 70B             │
│                                          ↓                  │
│                         Answer + Sources + Evaluation        │
└─────────────────────────────────────────────────────────────┘
```

### Complete Data Flow

```
1. User uploads PDF/TXT documents
2. document_loader.py extracts text (PyPDF2 for PDF, chardet for encoding)
3. chunk_text() splits into 500-char chunks with 50-char overlap
4. create_embeddings() converts to 384-dim vectors (multilingual model)
5. store_embeddings() indexes in FAISS with L2 distance metric
6. User asks question in selected language
7. Question converted to embedding using same model
8. FAISS searches for top-3 most similar chunks (distance < 2.0)
9. Groq LLaMA 3.3 70B generates answer from retrieved context
10. evaluate_answer() scores faithfulness 0-100 with diagnosis
11. Answer + sources + evaluation displayed to user
```

---

## 🛠️ Tech Stack

| Category | Technology | Purpose |
|----------|-----------|---------|
| **Frontend** | Streamlit 1.28+ | Web interface and deployment |
| **LLM** | Groq API (LLaMA 3.3 70B) | Answer generation and summarization |
| **Embeddings** | Sentence Transformers | Text to vector conversion |
| **Embedding Model** | paraphrase-multilingual-MiniLM-L12-v2 | 50+ language support, 384 dimensions |
| **Vector Database** | FAISS (faiss-cpu) | Fast similarity search |
| **PDF Processing** | PyPDF2 | PDF text extraction |
| **Encoding Detection** | chardet | Auto-detect file encoding |
| **Security** | python-dotenv | API key management |
| **PDF Generation** | fpdf2 | Chat history export |
| **Array Processing** | NumPy | FAISS float32 array handling |

---

## 🚀 Installation

### Prerequisites
- Python 3.10+
- Groq API key (free at [console.groq.com](https://console.groq.com))

### 1. Clone Repository

```bash
git clone https://github.com/Akhil-kadapa/multilingual-rag-agent.git
cd multilingual-rag-agent
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Run Application

```bash
# Web Interface (Recommended)
streamlit run app.py

# Terminal Interface
python main.py
```

---

## 📖 Usage

### Web Interface

1. **Upload Documents** — Click Upload in sidebar, select PDF or TXT files
2. **Select Language** — Choose output language from dropdown (English, Telugu, Hindi, French, Spanish)
3. **Process Documents** — Click "Process Documents" and watch the progress bar
4. **Review Summaries** — AI-generated summaries appear for each document
5. **Ask Questions** — Type in the chat box and press Enter
6. **Review Evaluation** — Check faithfulness score, retrieval quality, and diagnosis
7. **Download History** — Click "Download PDF" to export chat as formatted PDF

### Terminal Interface

```bash
python main.py
```

Follow the prompts to select language and ask questions.

### Example Queries

```
# Cross-language search (English question → Hindi document)
"Who was the first person on the moon?"

# Language-specific output
Select Telugu → "What is space?"
→ Returns: "అంతరిక్షం అనేది భూమి వాతావరణానికి అతీతంగా ఉన్న విశ్వంలో ఒక భాగం"

# Multi-document search
Upload cricket.pdf + football.pdf + space.txt
Ask: "Who won the 2022 World Cup?"
→ Searches all documents, cites correct source
```

---

## 📁 Project Structure

```
multilingual-rag-agent/
│
├── app.py                 # Streamlit web application
├── main.py                # Terminal interface
├── document_loader.py     # PDF/TXT reading and chunking
├── embeddings.py          # Vector creation and FAISS storage
├── retriever.py           # Semantic search with distance filtering
├── generator.py           # Groq LLM answer generation + evaluation
│
├── requirements.txt       # Python dependencies
├── .env                   # API keys (not committed to Git)
├── .gitignore             # Git ignore rules
│
└── documents/             # Place your documents here
    └── .gitkeep
```

---

## 🧠 How RAG Works

### The Problem RAG Solves

Standard LLMs answer from training memory and can **hallucinate** — making up information that sounds plausible but is incorrect.

**RAG Solution:** Before answering, the system searches your documents first, then generates answers **only from what it found**.

### The Pipeline

```
Standard LLM:
Question → LLM Memory → Answer (may hallucinate)

RAG System:
Question → Search Documents → Retrieve Evidence → LLM → Grounded Answer
```

### Chunking Strategy

```python
chunk_size = 500    # Characters per chunk
overlap = 50        # Shared characters between chunks

# Example:
Chunk 1: characters 0-500
Chunk 2: characters 450-950   # 50 char overlap
Chunk 3: characters 900-1400  # 50 char overlap
```

**Why overlap?** Prevents information loss at chunk boundaries — a key sentence split across two chunks remains coherent in both.

### Multilingual Embeddings

The model `paraphrase-multilingual-MiniLM-L12-v2` maps text from 50+ languages to the same 384-dimensional space:

```
"cost of product" (English)  → [0.23, -0.14, 0.87, ...]
"precio del producto" (Spanish) → [0.24, -0.13, 0.86, ...]
# Similar meaning → Similar vectors → Found by FAISS!
```

### RAG Evaluation System

Every answer is automatically evaluated:

| Metric | Description |
|--------|-------------|
| **Faithfulness Score** | 0-100: How well answer matches source documents |
| **Retrieval Quality** | Good/Bad: Did FAISS find the right chunks? |
| **Problem Area** | Generation/Retrieval/None: Where failure occurred |
| **Diagnosis** | One-line explanation of the evaluation |

```
Score ≥ 80 → Excellent (green)
Score 50-79 → Average (yellow)  
Score < 50 → Poor (red) — check diagnosis!
```

---

## 🔑 API Configuration

### Groq API (Free Tier)

| Model | Requests/Day | Tokens/Min |
|-------|-------------|-----------|
| llama-3.3-70b-versatile | 1,000 | 12,000 |

### Environment Variables

```env
# .env file (local development)
GROQ_API_KEY=gsk_your_key_here
```

```toml
# .streamlit/secrets.toml (Streamlit Cloud deployment)
GROQ_API_KEY = "gsk_your_key_here"
```

---

## ☁️ Deployment

### Streamlit Cloud (Free)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Set main file: `app.py`
5. Add secrets: `GROQ_API_KEY = "your_key"`
6. Click Deploy!

Your app will be live at:
```
https://your-app-name.streamlit.app
```

---

## 📊 Performance

| Operation | Time |
|-----------|------|
| Document loading (per file) | < 1 second |
| Embedding creation (per chunk) | ~50ms |
| FAISS search | < 10ms |
| Groq LLM response | 1-3 seconds |
| Total per question | 2-5 seconds |

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Planned Features
- [ ] Conversation memory for follow-up questions
- [ ] FastAPI REST endpoint
- [ ] Docker containerization
- [ ] Additional language support
- [ ] Document comparison mode
- [ ] Batch question processing

---

## 📄 License

This project is currently unlicensed. All rights reserved by Akhil Kadapa.

---

## 👤 Author

**Ahamed Akhil Kadapa**

**M.S. Artificial Intelligence, University of Bridgeport**

**Machine Learning | Artificial Intelligence | AI Engineering**

- GitHub: [@Akhil-kadapa](https://github.com/Akhil-kadapa)
- LinkedIn: [Akhil Kadapa](https://linkedin.com/in/akhil-kadapa786)

---

## 🙏 Acknowledgments

- [Groq](https://groq.com) — Ultra-fast LLM inference
- [Facebook AI Research](https://github.com/facebookresearch/faiss) — FAISS vector database
- [Sentence Transformers](https://sbert.net) — Multilingual embeddings
- [Streamlit](https://streamlit.io) — Python web framework

---

<div align="center">
  <strong>Built with ❤️ by Akhil Kadapa</strong><br>
  <em>AI Engineer Portfolio Project</em>
</div>
