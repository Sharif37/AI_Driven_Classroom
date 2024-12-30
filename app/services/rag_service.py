import os 
import json
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from app.utils.vetor_store import get_vector_store, initialize_vector_store
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv('GEMINI_API_KEY')


async def generate_quiz_with_rag(text_content: str, difficulty: str, num_questions: int, language: str, question_type: str):
    try:
        # Initialize vector store with the given text content
        initialize_vector_store(text_content)

        # Get the current vector store
        vector_store = get_vector_store()

        # Initialize the Google Gemini model
        llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=gemini_api_key)

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

        formatted_prompt = prompt_template.format(
            content=text_content,
            difficulty=difficulty,
            num_questions=num_questions,
            language=language,
            question_type=question_type
        )

        response = qa_chain.run(formatted_prompt)
        quiz_data = json.loads(response)
        return quiz_data

    except Exception as e:
        raise Exception(f"Error generating quiz: {str(e)}")


async def chat_with_document(text_content: str, user_message: str):
    try:

        

        # Get the current vector store
        vector_store = get_vector_store()
        llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=gemini_api_key)

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vector_store.as_retriever()
        )

        prompt_template = PromptTemplate(
            input_variables=["user_message"],
            template="""
            You are a helpful assistant. Here is the user's query: {user_message}
            Please respond in a conversational and helpful manner.
            """
        )

        formatted_prompt = prompt_template.format(user_message=user_message)
        response = qa_chain.run(formatted_prompt)
        return response

    except Exception as e:
        raise Exception(f"Error during chat: {str(e)}")
