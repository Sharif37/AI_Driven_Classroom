from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from app.config.settings import settings

# Initialize Gemini model with LangChain
llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=settings.GEMINI_API_KEY)

def generate_quiz(content: str, difficulty: str, num_questions: int, language: str, question_type: str):
    # Define the prompt template to instruct the model
    prompt_template = PromptTemplate(
        input_variables=["content", "difficulty", "num_questions", "language", "question_type"],
        template="""
You are an expert quiz generator. Generate a quiz based on the following requirements.

Content: {content}
Difficulty: {difficulty}
Number of Questions: {num_questions}
Language: {language}
Question Type: {question_type}

Strictly follow the JSON-like structure below in your response:

[
    {{
        "question": "Question text here",
        "type": "Multiple Choice/True-False/Short Answer/Fill in the Blank/Essay",
        "options": ["Option A", "Option B", "Option C", "Option D"] (if applicable)
    }},
    ...
]
"""
    )

    # Format the prompt with provided arguments
    prompt = prompt_template.format(
        content=content,
        difficulty=difficulty,
        num_questions=num_questions,
        language=language,
        question_type=question_type
    )

    # Get the response from the GoogleGenerativeAI model
    response = llm(prompt)
    print(response)
    # Parse the response into a structured format
    quiz_data = parse_response_to_json(response)
    
    return quiz_data


def parse_response_to_json(response: str):
    """
    Function to parse the AI response into a structured JSON format.
    """
    import json
    
    try:
        # Try parsing the response as JSON
        quiz_data = json.loads(response)
        return {"quiz": quiz_data}
    except json.JSONDecodeError:
        print("Failed to parse response as JSON.")
        return {"error": "Invalid quiz format received from the AI model."}
