# 📋 Project Overview

## 🧠 Implementation Approach

This RAG (Retrieval Augmented Generation) chatbot was developed to answer questions about Promtior using real-time web scraping and document processing. The solution combines modern AI technologies with robust data extraction techniques to create an intelligent assistant.

### 🚀 How I Approached the Challenge

1. **Real Data Extraction**  
   Implemented a comprehensive web scraper that extracts current content from [promtior.ai](https://promtior.ai) and processes the provided PDF document—avoiding hardcoded data.

2. **RAG Architecture**  
   Built a complete RAG pipeline using **LangChain** that combines document retrieval with language model generation for accurate, context-aware responses.

3. **User Experience Focus**  
   Created a professional, menu-driven interface that makes it easy for evaluators to test the required questions and explore additional capabilities.

4. **Production-Ready Code**  
   Integrated smart caching, error handling, and performance optimizations to ensure the system works reliably.

---

### 🔁 Implementation Logic

The system follows this workflow:

1. **Data Ingestion**

   - Web scraper uses **BeautifulSoup** to extract content from promtior.ai
   - PDF processor extracts text from the technical test document using **PyPDF2**
   - Content is categorized and structured for optimal retrieval

2. **Document Processing**

   - Text is split into manageable chunks (2000 chars with 200 overlap)
   - **Ollama** embeddings convert text chunks into vectors
   - **Chroma** stores embeddings in a vector database for fast retrieval

3. **Query Processing**

   - User query is embedded with the same model
   - Vector similarity search retrieves the most relevant content
   - Retrieved context is combined with the original query

4. **Response Generation**
   - **llama3.2:3b** model generates answers using only the retrieved context
   - A custom prompt ensures answers stay grounded in source content
   - Clean, conversational output is returned to the user

---

### ⚠️ Main Challenges Encountered

1. **Semantic Search Limitations**

   - **Problem**: Embeddings occasionally failed to match similar phrasing (e.g., "When was Promtior founded?" vs "In May 2023...")
   - **Solution**: Increased `k` (retrieval count) to 10 for broader context coverage

2. **Data Quality and Structure**

   - **Problem**: Raw scraped content was noisy and unstructured
   - **Solution**: Implemented categorization and logical document structuring

3. **User Experience Design**

   - **Problem**: Needed to be intuitive for non-technical testers
   - **Solution**: Developed a clean, menu-driven CLI for easy interaction

4. **Avoiding Hardcoded Solutions**
   - **Problem**: Ensuring outputs depend solely on real-time data
   - **Solution**: Removed fallback responses and built in graceful error handling

---

### 🛠️ How I Overcame These Challenges

- **Iterative Testing**: Continuously tested required queries to verify correct output
- **Smart Caching**: Used content hash-based caching to balance freshness and performance
- **Clean Architecture**: Isolated logic for scraping, processing, retrieval, and response generation
- **Professional Interface**: Simple, effective CLI to showcase the assistant’s capabilities

---

### 🧩 Key Design Decisions

1. **No Fallback Data**  
   The assistant always uses real-time scraped content. If scraping fails, it reports the issue rather than fabricating a fallback response.

2. **Comprehensive Content Extraction**  
   Combines web and PDF sources to build a rich information base.

3. **Natural Prompt Engineering**  
   Prompts encourage the LLM to generate conversational and grounded answers.

4. **Scalable, Modular Design**  
   System components (scraper, vector store, query engine) are modular for easy upgrades or reuse.

---

This implementation demonstrates not only technical proficiency with RAG systems but also practical software development skills including user experience design, performance optimization, and production-ready code practices.
