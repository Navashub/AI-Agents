import streamlit as st
from langchain_community.document_loaders import SeleniumURLLoader, WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

template = """
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
Question: {question} 
Context: {context} 
Answer:
"""

embeddings = OllamaEmbeddings(model="llama3.2")
vector_store = InMemoryVectorStore(embeddings)
model = OllamaLLM(model="llama3.2")

def load_page(url):
    try:
        # Try Selenium first
        loader = SeleniumURLLoader(urls=[url])
        documents = loader.load()
        return documents
    except:
        # Fallback to simple loader
        try:
            loader = WebBaseLoader([url])
            documents = loader.load()
            return documents
        except Exception as e:
            st.error(f"Failed to load page: {e}")
            return []

def split_text(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )
    return text_splitter.split_documents(documents)

def index_docs(documents):
    vector_store.add_documents(documents)

def retrieve_docs(query):
    return vector_store.similarity_search(query)

def answer_question(question, context):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    return chain.invoke({"question": question, "context": context})

st.title("AI Web Scraper")
url = st.text_input("Enter URL:")

if url:
    documents = load_page(url)
    if documents:
        chunked_documents = split_text(documents)
        index_docs(chunked_documents)
        st.success("Page loaded and indexed!")

question = st.chat_input("Ask a question...")

if question and url:
    st.chat_message("user").write(question)
    retrieved_docs = retrieve_docs(question)
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])
    answer = answer_question(question, context)
    st.chat_message("assistant").write(answer)





