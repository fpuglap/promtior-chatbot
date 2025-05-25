# 🤖 Promtior RAG Chatbot

An intelligent **web-based** chatbot assistant that uses **Retrieval Augmented Generation (RAG)** to answer questions about Promtior's services, history, and capabilities based on real-time web scraping and document analysis.

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

## 🌐 Live Demo

**The application is deployed and accessible at:**
**[Live Demo on Railway](https://promtior-chatbot-production-0b0b.up.railway.app/)** __

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/fpuglap/promtior-chatbot.git
cd promtior-chatbot
```

### 2. Set up virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
# Create .env file
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
```

### 5. Run the web application

```bash
python app.py
```

### 6. Open in browser

Navigate to: `http://localhost:8000`

---

## 🛠️ Technologies Used

- **LangChain**: RAG pipeline orchestration
- **OpenAI GPT-4o-mini**: Language model for response generation
- **OpenAI Embeddings**: Text embeddings (`text-embedding-3-small`)
- **Flask**: Web application framework
- **Chroma**: Vector database for document storage
- **BeautifulSoup**: Web scraping and HTML parsing
- **PyPDF2**: PDF document processing
- **Railway**: Cloud deployment platform

---

## 💻 Web Interface Features

- **🎯 Predefined Questions**: Quick access to main technical test questions
- **💡 Additional Questions**: Extended question set for comprehensive testing
- **💬 Custom Input**: Free-form question input with real-time responses
- **📱 Responsive Design**: Beautiful, modern interface that works on all devices
- **⚡ Real-time Processing**: AJAX-powered responses without page reloads

---

## 📁 Project Structure

```
promtior-chatbot/
├── app.py               # Flask web application (main entry point)
├── main.py              # Legacy CLI version (for reference)
├── scraper.py           # Web scraping utilities
├── requirements.txt     # Python dependencies
├── Procfile            # Railway deployment configuration
├── .gitignore          # Git ignore rules
├── .env                # Environment variables (local only)
├── README.md           # This file
├── doc/                # Documentation
│   ├── project-overview.md
│   └── component-diagram.md
└── AI Engineer.pdf     # Project specification
```

---

## 📚 Documentation

Detailed technical documentation is available in the `/doc` folder as required:

- **[Project Overview](doc/project-overview.md)**: Implementation approach and challenges
- **[Component Diagram](doc/component-diagram.md)**: System architecture and interactions

---

## 📋 Prerequisites

- Python 3.9+
- OpenAI API key (get it from [platform.openai.com](https://platform.openai.com/api-keys))
- Internet connection for web scraping

---

## 🔧 Local Development

### Environment Setup

1. **Get OpenAI API Key**:

   - Visit [OpenAI API Keys](https://platform.openai.com/api-keys)
   - Create new secret key
   - Add $5+ credits to your account

2. **Configure Environment**:

   ```bash
   cp .env.example .env  # If available
   # Edit .env and add your OPENAI_API_KEY
   ```

3. **Install and Run**:
   ```bash
   pip install -r requirements.txt
   python app.py
   ```

### Troubleshooting

1. **Missing OpenAI API key**:

   ```bash
   export OPENAI_API_KEY="your_key_here"
   ```

2. **Port already in use**:

   ```bash
   # App runs on port 8000 by default
   lsof -ti:8000 | xargs kill -9  # Kill process using port 8000
   ```

3. **Virtual environment issues**:
   ```bash
   rm -rf venv
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

---

## ☁️ Cloud Deployment

This application is deployed on **Railway** with automatic GitHub integration:

### Deployment Features

- **✅ Automatic deploys** from GitHub pushes
- **✅ Environment variable management** for API keys
- **✅ Custom domain support**
- **✅ HTTPS encryption** by default
- **✅ Automatic scaling** based on traffic

### Environment Variables (Railway)

```
OPENAI_API_KEY=your_openai_api_key_here
```

---

## 🎮 How to Use

1. **Visit the web application** (locally or deployed URL)
2. **Try predefined questions** by clicking the main buttons:
   - 📅 When was Promtior founded?
   - 🔧 What services does Promtior offer?
   - 📊 What results have Promtior clients achieved?
3. **Explore additional questions** in the expanded question set
4. **Ask custom questions** using the text input field
5. **Get real-time responses** powered by RAG and OpenAI

---

## 🏗️ Architecture Highlights

- **🔍 Real-time Web Scraping**: Extracts fresh content from promtior.ai
- **📄 Document Processing**: Analyzes provided PDF specifications
- **🧠 RAG Pipeline**: Combines retrieval and generation for accurate responses
- **💾 Smart Caching**: Optimizes performance with intelligent cache management
- **🌐 Production Ready**: Deployed with proper environment management and security

---

**Technical Test Submission for Promtior | RAG Implementation | LangChain + OpenAI + Flask + Railway**
