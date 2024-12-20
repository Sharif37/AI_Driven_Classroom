import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
from fastapi import APIRouter, UploadFile, File, Form
from langchain.schema import Document
from app.utils.file_utils import extract_text_from_pdf

# Load environment variables
load_dotenv()

# Get API key from environment variables
gemini_api_key = os.getenv('GEMINI_API_KEY')

router = APIRouter()

async def generate_quiz_with_rag(text_content, difficulty, num_questions, language, question_type):
    # Convert text content to a list of Document objects
    documents = [Document(page_content=text_content, metadata={})]

    # Generate embeddings using HuggingFace
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Create a vector store using FAISS
    vector_store = FAISS.from_documents(documents, embeddings)

    # Initialize the Google Gemini model with the API key
    llm = GoogleGenerativeAI(model="gemini-pro", api_key=gemini_api_key)

    # Create a retrieval-based QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",  # Use 'stuff' for simple retrieval chain
        retriever=vector_store.as_retriever()
    )

    # Create a prompt to generate quiz questions
    prompt = f"Generate {num_questions} quiz questions on the topic of the uploaded document. Difficulty: {difficulty}, Language: {language}, Question type: {question_type}."
    
    # Get response from the QA chain
    response = qa_chain.run(prompt)

    return response

@router.post("/upload/")
async def upload_file(
    file: UploadFile = File(...),
    difficulty: str = Form("medium"),
    num_questions: int = Form(5),
    language: str = Form("English"),
    question_type: str = Form("mix")
):
    # Extract text from the uploaded file
    text_content = await extract_text_from_pdf(file)

    # Generate quiz using RAG and Google Gemini
    quiz = await generate_quiz_with_rag(text_content, difficulty, num_questions, language, question_type)
    print(quiz)

    return {"quiz": quiz}
