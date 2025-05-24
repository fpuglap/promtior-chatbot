# 🤖 Promtior RAG Chatbot

An intelligent chatbot assistant that uses **Retrieval Augmented Generation (RAG)** to answer questions about Promtior's services, history, and capabilities based on real-time web scraping and document analysis.

---

## 🎯 Technical Test Solution

This project fulfills the requirements of implementing a **RAG-based chatbot using LangChain** that can answer specific questions about Promtior by scraping content from their website and additional sources.

---

## ✅ Test Requirements Met

The chatbot successfully answers the required questions:

- **When was Promtior founded?** → May 2023
- **What services does Promtior offer?** → GenAI Product Delivery, GenAI Department as a service, GenAI Adoption Consulting
- **What results have Promtior clients achieved?** → $1.4 million savings, 90% reduction in response times

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone <repository-url>
cd promtior-chatbot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Ensure Ollama is running with required model

```bash
ollama pull llama3.2:3b
ollama serve
```

### 4. Run the chatbot

```bash
python main.py
```

---

## 🛠️ Technologies Used

- **LangChain**: RAG pipeline orchestration
- **Ollama**: Local LLM and embeddings (`llama3.2:3b`)
- **Chroma**: Vector database for document storage
- **BeautifulSoup**: Web scraping and HTML parsing
- **PyPDF2**: PDF document processing

---

## 💬 Usage Example

```
🤖 Promtior AI Assistant
Loading...
============================================================
🎯 PROMTIOR AI ASSISTANT READY
============================================================
Choose an option:
1. When was Promtior founded?
2. What services does Promtior offer?
3. What results have Promtior clients achieved?
4. More questions
5. Ask your own question
6. Quit
❓ Your choice (1-6): 1
🔍 Question: When was Promtior founded?
🤔 Thinking...
🤖 Answer: Promtior was founded in May 2023.
```

---

## 📚 Documentation

Detailed technical documentation is available in the `/doc` folder as required:

- **Project Overview**: Implementation approach and challenges
- **Component Diagram**: System architecture and interactions

---

## 📋 Prerequisites

- Python 3.9+
- Ollama installed with `llama3.2:3b` model
- Internet connection for web scraping

---

**Technical Test Submission for Promtior | RAG Implementation | LangChain + Ollama**
