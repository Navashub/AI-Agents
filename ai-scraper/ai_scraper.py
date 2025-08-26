# import streamlit as st

# from langchain_community.document_loaders import SeleniumURLLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_core.vectorstores import InMemoryVectorStore
# from langchain_ollama import OllamaEmbeddings
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_ollama.llms import OllamaLLM

# template = """
# You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
# Question: {question} 
# Context: {context} 
# Answer:
# """

# embeddings = OllamaEmbeddings(model="llama3.2")
# vector_store = InMemoryVectorStore(embeddings)

# model = OllamaLLM(model="llama3.2")

# def load_page(url):
#     loader = SeleniumURLLoader(
#         urls=[url]
#     )
#     documents = loader.load()

#     return documents

# def split_text(documents):
#     text_splitter = RecursiveCharacterTextSplitter(
#         chunk_size=1000,
#         chunk_overlap=200,
#         add_start_index=True
#     )
#     data = text_splitter.split_documents(documents)

#     return data

# def index_docs(documents):
#     vector_store.add_documents(documents)

# def retrieve_docs(query):
#     return vector_store.similarity_search(query)

# def answer_question(question, context):
#     prompt = ChatPromptTemplate.from_template(template)
#     chain = prompt | model
#     return chain.invoke({"question": question, "context": context})

# st.title("AI Crawler")
# url = st.text_input("Enter URL:")

# documents = load_page(url)
# chunked_documents = split_text(documents)

# index_docs(chunked_documents)

# question = st.chat_input()

# if question:
#     st.chat_message("user").write(question)
#     retrieve_documents = retrieve_docs(question)
#     context = "\n\n".join([doc.page_content for doc in retrieve_documents])
#     answer = answer_question(question, context)
#     st.chat_message("assistant").write(answer)


import streamlit as st
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_core.documents import Document


template = """
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
Question: {question} 
Context: {context} 
Answer:
"""

# Initialize session state
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = None
if 'documents_loaded' not in st.session_state:
    st.session_state.documents_loaded = False
if 'current_url' not in st.session_state:
    st.session_state.current_url = ""

def check_ollama_status():
    """Check if Ollama is running and model is available"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        models = response.json()
        model_names = [model['name'] for model in models.get('models', [])]
        return 'llama3.2:latest' in model_names or 'llama3.2' in model_names
    except:
        return False

def create_selenium_driver():
    """Create a properly configured Chrome driver"""
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-images") 
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(30)
        return driver
    except Exception as e:
        st.error(f"Failed to create Chrome driver: {str(e)}")
        return None

def load_page_with_selenium(url):
    """Load page content using direct Selenium approach"""
    driver = None
    try:
        with st.spinner("Loading page with Selenium..."):
            driver = create_selenium_driver()
            if not driver:
                return None
            
            driver.get(url)
            
          
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
           
            time.sleep(2)
            
            # Get page content
            page_content = driver.page_source
            page_title = driver.title
            
            # Create document
            document = Document(
                page_content=page_content,
                metadata={"source": url, "title": page_title}
            )
            
            return [document]
            
    except Exception as e:
        st.error(f"Selenium direct approach failed: {str(e)}")
        return None
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

def extract_text_from_html(html_content):
    """Extract clean text from HTML content"""
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text and clean it
        text = soup.get_text()
        
        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    except Exception as e:
        st.warning(f"HTML parsing warning: {str(e)}")
        return html_content

def load_page_simple(url):
    """Fallback method using WebBaseLoader"""
    try:
        with st.spinner("Loading page with simple loader..."):
            loader = WebBaseLoader([url])
            documents = loader.load()
            return documents
    except Exception as e:
        st.error(f"Simple loader failed: {str(e)}")
        return None

def load_page(url):
    """Try multiple methods to load the page"""
    if not url or not url.strip():
        st.warning("Please enter a valid URL")
        return None
    
    # Add protocol if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Try direct Selenium first
    documents = load_page_with_selenium(url)
    
    if documents and documents[0].page_content:
        # Extract clean text from HTML
        clean_text = extract_text_from_html(documents[0].page_content)
        documents[0].page_content = clean_text
        
        if clean_text.strip():
            st.success(f"Successfully loaded content with Selenium ({len(clean_text)} characters)")
            return documents
    
    # Fallback to simple loader
    st.info("Selenium didn't get good content, trying simple web loader...")
    documents = load_page_simple(url)
    
    if not documents:
        st.error("Failed to load content from the URL with all methods")
        return None
    
    if not documents[0].page_content.strip():
        st.warning("The loaded page appears to be empty or contains no text content")
        return None
    
    st.success(f"Successfully loaded {len(documents)} document(s) with simple loader")
    return documents

def split_text(documents):
    """Split documents into chunks"""
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            add_start_index=True
        )
        chunks = text_splitter.split_documents(documents)
        st.info(f"Split into {len(chunks)} chunks")
        return chunks
    except Exception as e:
        st.error(f"Failed to split text: {str(e)}")
        return None

def initialize_vector_store():
    """Initialize vector store with embeddings"""
    try:
        with st.spinner("Initializing embeddings..."):
            embeddings = OllamaEmbeddings(model="llama3.2")
            vector_store = InMemoryVectorStore(embeddings)
            return vector_store
    except Exception as e:
        st.error(f"Failed to initialize vector store: {str(e)}")
        return None

def index_docs(vector_store, documents):
    """Add documents to vector store"""
    try:
        with st.spinner("Indexing documents..."):
            vector_store.add_documents(documents)
            st.success("Documents indexed successfully!")
            return True
    except Exception as e:
        st.error(f"Failed to index documents: {str(e)}")
        return False

def retrieve_docs(vector_store, query, k=3):
    """Retrieve relevant documents"""
    try:
        return vector_store.similarity_search(query, k=k)
    except Exception as e:
        st.error(f"Failed to retrieve documents: {str(e)}")
        return []

def answer_question(question, context):
    """Generate answer using Ollama"""
    try:
        model = OllamaLLM(model="llama3.2")
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | model
        
        with st.spinner("Generating answer..."):
            response = chain.invoke({"question": question, "context": context})
            return response
    except Exception as e:
        st.error(f"Failed to generate answer: {str(e)}")
        return "Sorry, I couldn't generate an answer due to an error."


st.title("🤖 AI Web Scraper & Q&A")
st.markdown("Enter a URL to scrape content and ask questions about it!")

# Check Ollama status
if not check_ollama_status():
    st.error("""
    ⚠️ **Ollama Issues Detected**
    
    Please ensure:
    1. Ollama is running: `ollama serve`
    2. llama3.2 model is installed: `ollama pull llama3.2`
    3. Ollama is accessible at http://localhost:11434
    """)
    st.stop()


url = st.text_input("Enter URL:", placeholder="https://example.com")

# Process URL button
if st.button("Load & Process URL") or (url and url != st.session_state.current_url):
    if url:
        
        st.session_state.documents_loaded = False
        st.session_state.current_url = url
        
        # Load and process documents
        documents = load_page(url)
        
        if documents:
            chunked_documents = split_text(documents)
            
            if chunked_documents:
                vector_store = initialize_vector_store()
                
                if vector_store:
                    success = index_docs(vector_store, chunked_documents)
                    if success:
                        st.session_state.vector_store = vector_store
                        st.session_state.documents_loaded = True
                        
                        # Show document preview
                        with st.expander("📄 Document Preview"):
                            preview_text = documents[0].page_content[:500]
                            st.text(preview_text + "..." if len(documents[0].page_content) > 500 else preview_text)

# Chat interface
if st.session_state.documents_loaded and st.session_state.vector_store:
    st.markdown("---")
    st.markdown("### 💬 Ask Questions About the Content")
    
   
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Display previous messages
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if question := st.chat_input("Ask a question about the content..."):
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": question})
        
        with st.chat_message("user"):
            st.write(question)
        
        # Get relevant documents
        retrieved_docs = retrieve_docs(st.session_state.vector_store, question)
        
        if retrieved_docs:
            
            context = "\n\n".join([doc.page_content for doc in retrieved_docs])
            
            # Generate answer
            answer = answer_question(question, context)
            
            
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            
            with st.chat_message("assistant"):
                st.write(answer)
                
                # Show sources in expander
                with st.expander("📚 Sources"):
                    for i, doc in enumerate(retrieved_docs, 1):
                        st.markdown(f"**Source {i}:**")
                        st.text(doc.page_content[:200] + "...")
        else:
            error_msg = "Sorry, I couldn't find relevant information to answer your question."
            st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
            with st.chat_message("assistant"):
                st.write(error_msg)

elif url and not st.session_state.documents_loaded:
    st.info("👆 Click 'Load & Process URL' to start!")
else:
    st.info("👆 Enter a URL above to get started!")

# Sidebar with instructions
with st.sidebar:
    st.markdown("### 📋 Instructions")
    st.markdown("""
    1. **Enter a URL** in the text box
    2. **Click 'Load & Process URL'** to scrape content
    3. **Ask questions** about the content in the chat
    
    ### 🔧 Requirements
    - Ollama running locally
    - llama3.2 model installed
    - Internet connection for scraping
    
    ### 🚀 Tips
    - Works best with text-rich websites
    - May take a moment to load complex pages
    - Ask specific questions for better answers
    """)
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()