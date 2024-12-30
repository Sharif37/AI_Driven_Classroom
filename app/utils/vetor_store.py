from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_store = None

def initialize_vector_store(text_content: str):
    global vector_store
    documents = [Document(page_content=text_content, metadata={})]
    if vector_store is None:
        vector_store = FAISS.from_documents(documents, embeddings)
    else:
        vector_store.add_documents(documents)

def get_vector_store():
    return vector_store
