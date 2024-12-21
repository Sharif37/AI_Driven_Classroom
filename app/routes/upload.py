import os
import json
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from langchain.schema import Document
from app.utils.file_utils import extract_text_from_pdf

# Load environment variables
load_dotenv()

# Get API key from environment variables
gemini_api_key = os.getenv('GEMINI_API_KEY')

# Initialize FastAPI router
router = APIRouter()

async def generate_quiz_with_rag(text_content: str, difficulty: str, num_questions: int, language: str, question_type: str):
    try:
        # Convert text content to a list of Document objects
        documents = [Document(page_content=text_content, metadata={})]

        # Generate embeddings using HuggingFace
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2")

        # Create a vector store using FAISS
        vector_store = FAISS.from_documents(documents, embeddings)

        # Initialize the Google Gemini model with the API key
        llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=gemini_api_key)

        # Create a retrieval-based QA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vector_store.as_retriever()
        )

        # Define the prompt template
        prompt_template = PromptTemplate(
            input_variables=["content", "difficulty", "num_questions", "language", "question_type"],
            template="""
    Generate a quiz with the following specifications:
    Content: {content}
    Difficulty: {difficulty}
    Number of Questions: {num_questions}
    Language: {language}
    Question Type: {question_type}

    Return the response in this exact JSON format:
    [
        {{
            "question": "Question text here",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_answer": "Correct option here"
        }}
    ]
    """
        )

        # Format the prompt
        formatted_prompt = prompt_template.format(
            content=text_content,
            difficulty=difficulty,
            num_questions=num_questions,
            language=language,
            question_type=question_type
        )

        # Get response from the QA chain
        response = qa_chain.run(formatted_prompt)
        
        # Parse the response to ensure it's valid JSON
        quiz_data = json.loads(response)
        return quiz_data

    except Exception as e:
        raise Exception(f"Error generating quiz: {str(e)}")

@router.post("/upload/")
async def upload_file(
    file: UploadFile = File(...),
    difficulty: str = Form("medium"),
    num_questions: int = Form(5),
    language: str = Form("English"),
    question_type: str = Form("mcq")
):
    try:
        # Extract text from PDF
        text_content = await extract_text_from_pdf(file)
        
        # Generate quiz
        quiz_data = await generate_quiz_with_rag(text_content, difficulty, num_questions, language, question_type)
        
        # Return the quiz data
        return JSONResponse(content={"quiz": quiz_data})

    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )