# main.py - Production-ready RAG system with OpenAI
import warnings
warnings.filterwarnings('ignore')

import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings  # OpenAI integration
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import hashlib
import json

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

def main():
    print("🤖 Promtior AI Assistant")
    print("Loading...")
    
    # 1. LOAD DATA FROM WEB SCRAPING
    try:
        from scraper import get_website_content
        documents = get_website_content()
        
    except Exception as e:
        print(f"❌ ERROR: Failed to load content: {e}")
        return
    
    # 2. CREATE EMBEDDINGS - OpenAI
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
    
    # 4. CONFIGURE CHAT MODEL - OpenAI
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
    
    # 6. CHATBOT INTERFACE
    print("\n" + "="*60)
    print("🎯 PROMTIOR AI ASSISTANT READY")
    print("="*60)
    
    # Predefined questions for the technical test
    main_questions = [
        "When was Promtior founded?",
        "What services does Promtior offer?",
        "What results have Promtior clients achieved?"
    ]
    
    # Additional questions for exploration
    additional_questions = [
        "What does Promtior do?",
        "What is GenAI Product Delivery?",
        "What is RAG architecture?",
        "How does Promtior help with automation?",
        "What technologies does Promtior use?",
        "What processes can Promtior automate?",
        "What is GenAI Department as a service?",
        "How can I contact Promtior?"
    ]
    
    def show_additional_questions():
        print("\n" + "-"*60)
        print("Additional questions you can ask:")
        for i, question in enumerate(additional_questions, 1):
            print(f"{i}. {question}")
        print("9. Back to main menu")
        print("-"*60)
        
        while True:
            try:
                choice = input("❓ Choose a question (1-9): ").strip()
                
                if choice == '9':
                    return None
                elif choice.isdigit() and 1 <= int(choice) <= 8:
                    return additional_questions[int(choice) - 1]
                else:
                    print("Please choose a valid option (1-9).")
            except (ValueError, IndexError):
                print("Please choose a valid option (1-9).")
    
    while True:
        try:
            print("\n" + "-"*60)
            print("Choose an option:")
            print("1. When was Promtior founded?")
            print("2. What services does Promtior offer?") 
            print("3. What results have Promtior clients achieved?")
            print("4. More questions")
            print("5. Ask your own question")
            print("6. Quit")
            print("-"*60)
            
            choice = input("❓ Your choice (1-6): ").strip()
            
            if choice in ['6', 'quit', 'exit', 'q']:
                print("👋 Thank you for using Promtior AI Assistant!")
                break
            
            question = None
            
            if choice == '1':
                question = main_questions[0]
            elif choice == '2':
                question = main_questions[1]
            elif choice == '3':
                question = main_questions[2]
            elif choice == '4':
                question = show_additional_questions()
                if question is None:  # User chose to go back
                    continue
            elif choice == '5':
                question = input("\n❓ Your question: ").strip()
                if not question:
                    print("Please enter a question.")
                    continue
            else:
                print("Please choose a valid option (1-6).")
                continue
            
            if question:
                print(f"\n🔍 Question: {question}")
                print("🤔 Thinking...")
                
                result = qa_chain.invoke({"query": question})
                print(f"\n🤖 Answer: {result['result']}")
            
        except KeyboardInterrupt:
            print("\n👋 Thank you for using Promtior AI Assistant!")
            break
        except Exception as e:
            print(f"❌ Sorry, I encountered an error: {e}")

if __name__ == "__main__":
    main()