# scraper.py - Clean and silent web scraper for promtior.ai
import requests
from bs4 import BeautifulSoup
import os
from langchain.schema import Document

def extract_pdf_content():
    """Extract actual content from the technical test PDF"""
    try:
        import PyPDF2
        
        pdf_path = "AI Engineer.pdf"
        if not os.path.exists(pdf_path):
            return []
        
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            documents = []
            
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                
                # Split into paragraphs and clean
                paragraphs = [p.strip() for p in page_text.split('\n\n') if p.strip()]
                
                for para in paragraphs:
                    # Only include meaningful paragraphs
                    if len(para) > 50 and not para.lower().startswith(('technical test', 'promtior', 'welcome')):
                        # Clean up the text
                        clean_para = ' '.join(para.split())
                        
                        documents.append(Document(
                            page_content=clean_para,
                            metadata={
                                'source': 'pdf',
                                'page': page_num + 1,
                                'type': 'pdf_content'
                            }
                        ))
        
        return documents
        
    except Exception as e:
        return []

def clean_and_filter_text(text):
    """Clean text and filter out unwanted content"""
    if not text or len(text) < 20:
        return None
    
    # Normalize whitespace
    text = ' '.join(text.split())
    
    # Filter out unwanted content
    unwanted_patterns = [
        'cookie', 'privacy policy', 'terms of service',
        'subscribe', 'newsletter', 'follow us'
    ]
    
    if any(pattern in text.lower() for pattern in unwanted_patterns):
        return None
    
    return text.strip()

def extract_web_content():
    """Extract content from promtior.ai website"""
    url = "https://promtior.ai"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Remove unwanted elements
    for element in soup(['script', 'style', 'nav', 'footer', 'header']):
        element.decompose()
    
    # Extract text from relevant elements
    content_pieces = []
    for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'li']):
        text = clean_and_filter_text(element.get_text())
        if text:
            content_pieces.append(text)
    
    return content_pieces

def create_structured_documents(content_pieces):
    """Convert raw content into structured documents for better retrieval"""
    documents = []
    
    # Categorize content
    services_content = []
    results_content = []
    company_content = []
    individual_content = []
    
    for content in content_pieces:
        content_lower = content.lower()
        
        # Services
        if any(keyword in content_lower for keyword in [
            'genai product delivery', 'genai department', 'genai adoption',
            'service', 'delivery', 'consulting'
        ]):
            services_content.append(content)
        
        # Results and achievements
        elif any(keyword in content_lower for keyword in [
            'million', 'reduction', 'savings', 'achieved', 'results'
        ]):
            results_content.append(content)
        
        # Company information
        elif any(keyword in content_lower for keyword in [
            'promtior', 'company', 'founded', 'business'
        ]):
            company_content.append(content)
        
        # Individual valuable content
        else:
            individual_content.append(content)
    
    # Create focused documents
    
    # Services document
    if services_content:
        services_text = "Promtior offers three main services: " + " ".join(services_content[:3])
        documents.append(Document(
            page_content=services_text,
            metadata={'source': 'website', 'type': 'services'}
        ))
    
    # Results document
    if results_content:
        results_text = "Promtior clients have achieved significant results: " + " ".join(results_content[:2])
        documents.append(Document(
            page_content=results_text,
            metadata={'source': 'website', 'type': 'results'}
        ))
    
    # Company document
    if company_content:
        company_text = "About Promtior: " + " ".join(company_content[:2])
        documents.append(Document(
            page_content=company_text,
            metadata={'source': 'website', 'type': 'company'}
        ))
    
    # Individual content pieces (for better retrieval coverage)
    for i, content in enumerate(individual_content[:8]):
        documents.append(Document(
            page_content=content,
            metadata={'source': 'website', 'section': f'content_{i}'}
        ))
    
    return documents

def scrape_promtior_website():
    """Main scraping function - completely silent"""
    
    try:
        # Extract content from website
        content_pieces = extract_web_content()
        
        # Create structured documents
        web_documents = create_structured_documents(content_pieces)
        
        # Add PDF content for extra points
        pdf_documents = extract_pdf_content()
        
        # Combine all documents
        all_documents = web_documents + pdf_documents
        
        return all_documents
        
    except requests.RequestException as e:
        raise Exception(f"Web scraping failed: {e}")

def get_website_content():
    """Main entry point for getting website content"""
    return scrape_promtior_website()

if __name__ == "__main__":
    # Solo para testing - no se ejecuta cuando se importa
    try:
        docs = scrape_promtior_website()
        print(f"📊 Total documents: {len(docs)}")
        print("✅ Scraper test completed successfully")
    except Exception as e:
        print(f"❌ Error: {e}")