# 🤖 EDA-AI-AGENT: Professional Agentic RAG System

## 📌 Project Overview
This project is an Advanced AI Assistant designed for hardware designers and EDA engineers. It does not just chat; it thinks and acts. The system understands technical hardware files like Verilog (.v), SDC (.sdc), and Tcl scripts.

I built this system to solve a key problem: **How to analyze secret hardware code safely using AI.**

---

## 🏗 How It Works (The Architecture)

The project uses an **Agentic RAG (Retrieval-Augmented Generation)** workflow:

- **The "Eyes" (Document Loader):** Reads technical files and splits them into chunks  
- **The "Memory" (Vector DB):** Uses ChromaDB to store embeddings for retrieval  
- **The "Brain" (AI Agent):** Built with LangGraph using Reason-then-Act logic  
- **The "Tools":**
  - `list_data_files` – list available files  
  - `eda_knowledge_base` – search documents  
  - `verilog_syntax_check` – validate Verilog  
  - `timing_calculator` – engineering calculations  

---

## 🌟 Key Technical Features

### 1. Hybrid Intelligence (Cloud + Local)
- **OpenAI (GPT-4o):** fast and advanced reasoning  
- **Local Llama 3.1 (Ollama):** privacy-focused offline execution  

---

### 2. Multi-Service Backend
- FastAPI backend  
- Logging system (response time + history stored in logs/chat_history.log)

---

### 3. Professional Frontend
- Streamlit UI  
- Chat history  
- File upload  
- Model switching  

---

### 4. Production Ready (Docker)
- Fully containerized system  
- One command запускает backend + frontend + DB  

---

## 📂 Folder Structure

- `app/api/v1/` – API endpoints  
- `app/services/ai_agent/` – agent logic & tools  
- `app/services/rag/` – document processing & vector DB  
- `frontend/` – UI  
- `data/` – hardware files  
- `chroma_db/` – vector storage  
- `logs/` – monitoring  

---

## 🚀 How to Launch

### 1. Configure Environment

Create `.env`:

```
OPENAI_API_KEY=your_key
DEFAULT_MODEL="gpt-4o"
LOCAL_MODEL_NAME="llama3.1"
OLLAMA_BASE_URL="http://host.docker.internal:11434/v1"
```

---

### 2. Run with Docker

```
docker-compose up --build
```

- UI: http://localhost:8501  
- API: http://localhost:8000/docs  

---

## 🎯 Use Cases (Synopsys)

- Code explanation (Verilog / SDC)  
- Syntax validation  
- Secure local AI processing  
- Performance monitoring  
