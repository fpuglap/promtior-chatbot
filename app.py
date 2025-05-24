import os
import warnings
warnings.filterwarnings('ignore')

from flask import Flask, request, jsonify, render_template_string
from dotenv import load_dotenv
load_dotenv()

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.schema import Document
import hashlib
import json

app = Flask(__name__)

# Global variables for the RAG system
qa_chain = None
is_initialized = False

def get_content_hash(documents):
    """Generate hash of document content for cache validation"""
    content = json.dumps([doc.page_content for doc in documents], sort_keys=True)
    return hashlib.md5(content.encode()).hexdigest()

def load_or_create_vectorstore(documents, embeddings, force_recreate=False):
    """Load existing vectorstore or create new one if needed"""
    
    cache_dir = "./chroma_db"
    hash_file = f"{cache_dir}/content_hash.txt"
    current_hash = get_content_hash(documents)
    
    # Check if we should use existing cache
    if not force_recreate and os.path.exists(cache_dir) and os.path.exists(hash_file):
        try:
            with open(hash_file, 'r') as f:
                stored_hash = f.read().strip()
            
            if stored_hash == current_hash:
                return Chroma(
                    persist_directory=cache_dir,
                    embedding_function=embeddings
                )
        except Exception as e:
            pass  # Cache error, just recreate
    
    # Create new vectorstore
    
    # Clean old cache if exists
    if os.path.exists(cache_dir):
        import shutil
        shutil.rmtree(cache_dir)
    
    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200
    )
    split_docs = text_splitter.split_documents(documents)
    
    # Create vectorstore
    vectorstore = Chroma.from_documents(
        documents=split_docs,
        embedding=embeddings,
        persist_directory=cache_dir
    )
    
    # Save content hash for future validation
    os.makedirs(cache_dir, exist_ok=True)
    with open(hash_file, 'w') as f:
        f.write(current_hash)
    
    return vectorstore

def initialize_rag():
    """Initialize the RAG system"""
    global qa_chain, is_initialized
    
    if is_initialized:
        return True
    
    try:
        print("🤖 Initializing Promtior AI Assistant...")
        
        # 1. LOAD DATA FROM WEB SCRAPING
        from scraper import get_website_content
        documents = get_website_content()
        
        # 2. CREATE EMBEDDINGS
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # 3. SMART VECTORSTORE LOADING
        vectorstore = load_or_create_vectorstore(
            documents=documents, 
            embeddings=embeddings,
            force_recreate=False
        )
        
        # 4. CONFIGURE CHAT MODEL
        chat_model = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # 5. CREATE RAG CHAIN
        custom_prompt = PromptTemplate(
            template="""Answer the question using only the information provided in the context below. 
            Be direct and natural in your response. If the information is not available in the context, 
            say "I don't have that information available."
            
            Context: {context}

            Question: {question}

            Answer:""",
            input_variables=["context", "question"]
        )
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=chat_model,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_kwargs={"k": 10}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": custom_prompt}
        )
        
        is_initialized = True
        print("✅ RAG system initialized successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error initializing RAG system: {e}")
        return False

def ask_question(question):
    """Process a question through the RAG system"""
    global qa_chain
    
    if not is_initialized:
        if not initialize_rag():
            return "❌ System not initialized. Please try again."
    
    try:
        result = qa_chain.invoke({"query": question})
        return result['result']
    except Exception as e:
        return f"❌ Error processing question: {e}"

# HTML Templates
HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 Promtior AI Assistant</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: white;
        }
        .container {
            background: rgba(255,255,255,0.1);
            padding: 30px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }
        h1 {
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
        }
        .question-buttons, .additional-questions {
            margin-bottom: 30px;
        }
        .question-buttons {
            display: grid;
            grid-template-columns: 1fr;
            gap: 15px;
        }
        .question-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 10px;
            margin-top: 15px;
        }
        .question-btn {
            background: rgba(255,255,255,0.2);
            border: 2px solid rgba(255,255,255,0.3);
            color: white;
            padding: 15px 20px;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 16px;
        }
        .question-btn.small {
            padding: 12px 15px;
            font-size: 14px;
        }
        .question-btn:hover {
            background: rgba(255,255,255,0.3);
            transform: translateY(-2px);
        }
        h3 {
            color: rgba(255,255,255,0.9);
            margin-bottom: 15px;
            font-size: 1.2em;
        }
        .custom-question {
            margin-top: 20px;
            padding: 20px;
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
        }
        input[type="text"] {
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 10px;
            background: rgba(255,255,255,0.9);
            color: #333;
            font-size: 16px;
            margin-bottom: 15px;
        }
        .ask-btn {
            background: #4CAF50;
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-size: 16px;
            transition: background 0.3s ease;
        }
        .ask-btn:hover {
            background: #45a049;
        }
        .answer-section {
            margin-top: 30px;
            padding: 20px;
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            display: none;
        }
        .loading {
            text-align: center;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Promtior AI Assistant</h1>
        
        <div class="question-buttons">
            <h3>🎯 Main Questions (Technical Test)</h3>
            <button class="question-btn" onclick="askPredefined('When was Promtior founded?')">
                📅 When was Promtior founded?
            </button>
            <button class="question-btn" onclick="askPredefined('What services does Promtior offer?')">
                🔧 What services does Promtior offer?
            </button>
            <button class="question-btn" onclick="askPredefined('What results have Promtior clients achieved?')">
                📊 What results have Promtior clients achieved?
            </button>
        </div>
        
        <div class="additional-questions">
            <h3>💡 Additional Questions</h3>
            <div class="question-grid">
                <button class="question-btn small" onclick="askPredefined('What does Promtior do?')">
                    🚀 What does Promtior do?
                </button>
                <button class="question-btn small" onclick="askPredefined('What is GenAI Product Delivery?')">
                    📦 What is GenAI Product Delivery?
                </button>
                <button class="question-btn small" onclick="askPredefined('What is RAG architecture?')">
                    🏗️ What is RAG architecture?
                </button>
                <button class="question-btn small" onclick="askPredefined('How does Promtior help with automation?')">
                    ⚙️ How does Promtior help with automation?
                </button>
                <button class="question-btn small" onclick="askPredefined('What technologies does Promtior use?')">
                    💻 What technologies does Promtior use?
                </button>
                <button class="question-btn small" onclick="askPredefined('What processes can Promtior automate?')">
                    🔄 What processes can Promtior automate?
                </button>
                <button class="question-btn small" onclick="askPredefined('What is GenAI Department as a service?')">
                    🏢 What is GenAI Department as a service?
                </button>
                <button class="question-btn small" onclick="askPredefined('How can I contact Promtior?')">
                    📧 How can I contact Promtior?
                </button>
            </div>
        </div>
        
        <div class="custom-question">
            <h3>💬 Ask your own question:</h3>
            <input type="text" id="customQuestion" placeholder="Type your question here..." 
                   onkeypress="if(event.key==='Enter') askCustom()">
            <button class="ask-btn" onclick="askCustom()">Ask Question</button>
        </div>
        
        <div id="answerSection" class="answer-section">
            <h3>🤖 Answer:</h3>
            <div id="answerText"></div>
        </div>
    </div>

    <script>
        async function askPredefined(question) {
            await askQuestion(question);
        }
        
        async function askCustom() {
            const question = document.getElementById('customQuestion').value.trim();
            if (!question) {
                alert('Please enter a question');
                return;
            }
            await askQuestion(question);
        }
        
        async function askQuestion(question) {
            const answerSection = document.getElementById('answerSection');
            const answerText = document.getElementById('answerText');
            
            // Show loading
            answerSection.style.display = 'block';
            answerText.innerHTML = '<div class="loading">🤔 Thinking...</div>';
            
            try {
                const response = await fetch('/ask', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ question: question })
                });
                
                const data = await response.json();
                answerText.innerHTML = `<strong>Q:</strong> ${question}<br><br><strong>A:</strong> ${data.answer}`;
            } catch (error) {
                answerText.innerHTML = '❌ Error: Could not get response. Please try again.';
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    """Home page with the chat interface"""
    return render_template_string(HOME_TEMPLATE)

@app.route('/ask', methods=['POST'])
def ask():
    """API endpoint to process questions"""
    data = request.get_json()
    question = data.get('question', '').strip()
    
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    answer = ask_question(question)
    return jsonify({'answer': answer})

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'initialized': is_initialized})

if __name__ == '__main__':
    print("🚀 Starting Promtior AI Assistant Web App...")
    initialize_rag()  # Initialize on startup
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))