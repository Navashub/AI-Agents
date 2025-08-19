from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import re

# Initialize embeddings
try:
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")
    print("Successfully initialized mxbai-embed-large embeddings")
except Exception as e:
    print(f"Error initializing embeddings: {e}")
    raise


markdown_file = "luxdev_course_outline.md"
db_location = "./chrome_langchain_db"
collection_name = "luxdev_course_outline"


add_documents = not os.path.exists(db_location)
print(f"Vector store directory exists: {os.path.exists(db_location)}")

# Function to read and process Markdown file
def load_markdown_file(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Markdown file {file_path} not found")
        
        with open(file_path, "r", encoding="utf-8") as file:
            markdown_content = file.read()
        
        if not markdown_content.strip():
            raise ValueError(f"Markdown file {file_path} is empty")
        
        print(f"Raw Markdown content (first 500 chars): {markdown_content[:500]}")
        
        # Split by headers (##) to create one document per section
        chunks = re.split(r'\n##\s+', markdown_content)
        documents = []
        ids = []
        for i, chunk in enumerate(chunks):
            if chunk.strip():
                content = f"## {chunk.strip()}" if i > 0 else chunk.strip()
                
                section_title = chunk.split("\n")[0].strip() if "\n" in chunk else "No Title"
                document = Document(
                    page_content=content,
                    metadata={
                        "source": file_path,
                        "section_id": str(i),
                        "section_title": section_title
                    },
                    id=str(i)
                )
                documents.append(document)
                ids.append(str(i))
        
        if not documents:
            raise ValueError("No valid document chunks created from Markdown file")
        
        print(f"Created {len(documents)} document chunks")
        for i, doc in enumerate(documents[:5]):  # Print first 5 chunks for inspection
            print(f"Chunk {i}: {doc.page_content[:100]}... (Metadata: {doc.metadata})")
        
        return documents, ids
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
    except Exception as e:
        print(f"Error processing Markdown file: {e}")
        raise


if add_documents:
    print(f"Loading documents from {markdown_file}")
    documents, ids = load_markdown_file(markdown_file)
else:
    print("Vector store already exists, skipping document loading")

# Initialize Chroma vector store
try:
    vector_store = Chroma(
        collection_name=collection_name,
        persist_directory=db_location,
        embedding_function=embeddings
    )
    print("Successfully initialized Chroma vector store")
except Exception as e:
    print(f"Error initializing Chroma vector store: {e}")
    raise

# Add documents to vector store if not already added
if add_documents:
    try:
        vector_store.add_documents(documents=documents, ids=ids)
        print(f"Added {len(documents)} documents to the vector store")
    except Exception as e:
        print(f"Error adding documents to vector store: {e}")
        raise

try:
    stored_docs = vector_store.get()
    print(f"Vector store contains {len(stored_docs['ids'])} documents")
    for i, (doc_id, doc_content) in enumerate(zip(stored_docs['ids'][:5], stored_docs['documents'][:5])):
        print(f"Stored Document {doc_id}: {doc_content[:100]}...")
except Exception as e:
    print(f"Error retrieving vector store contents: {e}")

retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}
)
print("Retriever initialized successfully")