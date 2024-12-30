from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from app.services.rag_service import generate_quiz_with_rag, chat_with_document
from app.utils.file_utils import extract_text_from_pdf

router = APIRouter()

# Global cache to store uploaded file content
file_cache = {}

@router.post("/upload/")
async def upload_file(
    file: UploadFile = File(...),
    difficulty: str = Form("medium"),
    num_questions: int = Form(5),
    language: str = Form("English"),
    question_type: str = Form("mcq")
):
    try:
        file_id = file.filename  # Unique identifier for the file

        if file_id not in file_cache:
            # Extract text from the uploaded PDF and store it in cache
            text_content = await extract_text_from_pdf(file)
            file_cache[file_id] = text_content
        else:
            text_content = file_cache[file_id]

        # Generate quiz using RAG
        quiz_data = await generate_quiz_with_rag(text_content, difficulty, num_questions, language, question_type)

        return JSONResponse(content={"quiz": quiz_data, "file_id": file_id})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@router.post("/chat_with_document/")
async def chat_with_document_endpoint(
    user_message: str = Form(...),
    file_id: str = Form(...)
):
    try:
        if file_id in file_cache:
            text_content = file_cache[file_id]
            response = await chat_with_document(text_content, user_message)
            return JSONResponse(content={"response": response})
        else:
            return JSONResponse(content={"error": "File not found in cache. Please upload again."}, status_code=400)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
