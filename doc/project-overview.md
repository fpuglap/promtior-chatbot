# 📋 Project Overview

## 🧠 Implementation Approach

This RAG (Retrieval Augmented Generation) chatbot was developed to answer questions about Promtior using real-time web scraping and document processing. The solution combines modern AI technologies with robust data extraction techniques to create an intelligent web-based assistant deployed on cloud infrastructure.

### 🚀 How I Approached the Challenge

1. **Real Data Extraction**  
   Implemented a comprehensive web scraper that extracts current content from [promtior.ai](https://promtior.ai) and processes the provided PDF document—avoiding hardcoded data.

2. **RAG Architecture**  
   Built a complete RAG pipeline using **LangChain** that combines document retrieval with language model generation for accurate, context-aware responses.

3. **Professional Web Interface**  
   Created a beautiful, responsive **Flask web application** with predefined question buttons and custom input fields, making it easy for evaluators to test required questions and explore additional capabilities.

4. **Cloud-Ready Deployment**  
   Migrated from local models to **OpenAI APIs** and deployed the solution on **Railway** cloud platform with automatic GitHub integration for production accessibility.

5. **Production-Ready Code**  
   Integrated smart caching, error handling, and performance optimizations to ensure the system works reliably in cloud environments.

---

### 🔁 Implementation Logic

The system follows this workflow:

1. **Data Ingestion**

   - Web scraper uses **BeautifulSoup** to extract content from promtior.ai
   - PDF processor extracts text from the technical test document using **PyPDF2**
   - Content is categorized and structured for optimal retrieval

2. **Document Processing**

   - Text is split into manageable chunks (2000 chars with 200 overlap)
   - **OpenAI embeddings** (`text-embedding-3-small`) convert text chunks into vectors
   - **Chroma** stores embeddings in a vector database for fast retrieval

3. **Query Processing**

   - User query from web interface (predefined buttons or custom input)
   - Query is embedded with the same OpenAI embedding model
   - Vector similarity search retrieves the most relevant content
   - Retrieved context is combined with the original query

4. **Response Generation**
   - **OpenAI GPT-4o-mini** model generates answers using only the retrieved context
   - A custom prompt ensures answers stay grounded in source content
   - Clean, conversational output is returned to the web interface

---

### ⚠️ Main Challenges Encountered

1. **Semantic Search Limitations**

   - **Problem**: Embeddings occasionally failed to match similar phrasing (e.g., "When was Promtior founded?" vs "In May 2023...")
   - **Solution**: Increased `k` (retrieval count) to 10 for broader context coverage

2. **Data Quality and Structure**

   - **Problem**: Raw scraped content was noisy and unstructured
   - **Solution**: Implemented categorization and logical document structuring

3. **Local to Cloud Migration**

   - **Problem**: Local Ollama models weren't suitable for cloud deployment due to size and resource constraints
   - **Solution**: Successfully migrated to OpenAI APIs for reliable, scalable cloud-based inference

4. **Web Interface Development**

   - **Problem**: Transitioning from CLI to professional web interface while maintaining functionality
   - **Solution**: Built responsive Flask application with intuitive UI and real-time AJAX responses

5. **Deployment Configuration**
   - **Problem**: Managing environment variables and ensuring proper configuration in cloud environment
   - **Solution**: Implemented secure environment variable management through Railway platform

---

### 🛠️ How I Overcame These Challenges

- **API Integration**: Seamlessly integrated OpenAI APIs for both embeddings and chat completion
- **Progressive Enhancement**: Started with CLI, then built web interface, maintaining core functionality throughout
- **Cloud Architecture**: Designed system with cloud deployment in mind from the beginning
- **Environment Management**: Proper separation of secrets and configuration for secure deployment
- **Iterative Testing**: Continuously tested required queries across different interfaces to verify consistent output
- **Smart Caching**: Used content hash-based caching to balance freshness and performance
- **Clean Architecture**: Isolated logic for scraping, processing, retrieval, and response generation

---

### 🧩 Key Design Decisions

1. **OpenAI Integration**  
   Chose OpenAI APIs over local models for reliable cloud deployment, consistent performance, and better scalability.

2. **Flask Web Framework**  
   Selected Flask for its simplicity and effectiveness in creating a professional web interface that showcases the assistant's capabilities.

3. **Railway Cloud Platform**  
   Deployed on Railway for automatic GitHub integration, easy environment management, and reliable hosting.

4. **No Fallback Data**  
   The assistant always uses real-time scraped content. If scraping fails, it reports the issue rather than fabricating a fallback response.

5. **Comprehensive Content Extraction**  
   Combines web and PDF sources to build a rich information base for accurate responses.

6. **Natural Prompt Engineering**  
   Prompts encourage the LLM to generate conversational and grounded answers while staying within retrieved context.

7. **Scalable, Modular Design**  
   System components (scraper, vector store, query engine, web interface) are modular for easy upgrades or reuse.

---

## 🌐 Final Architecture

The production system features:

- **🖥️ Flask Web Interface**: Professional, responsive UI with predefined questions and custom input
- **🧠 OpenAI GPT-4o-mini**: Fast, reliable language model for response generation
- **🔢 OpenAI Embeddings**: High-quality text embeddings for semantic search
- **🗄️ Chroma Vector Store**: Efficient vector storage and retrieval
- **☁️ Railway Deployment**: Automatic deployment with GitHub integration
- **🔒 Secure Configuration**: Environment-based API key management

This implementation demonstrates not only technical proficiency with RAG systems and modern AI technologies, but also practical software development skills including web development, cloud deployment, API integration, and production-ready code practices.

---

## 🚀 Live Demo

The application is deployed and accessible at the public URL provided by Railway, showcasing a complete, production-ready RAG chatbot solution.
