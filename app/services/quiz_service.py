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
        Generate a {difficulty} level quiz with {num_questions} questions in {language}.
        The questions should be of type {question_type}.
        Based on the following content:
        {content}
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

    # Parse the response into a structured format
    quiz_data = parse_response_to_json(response)
    
    return quiz_data


def parse_response_to_json(response: str):
    """
    Function to convert the AI response into a structured JSON format.
    """
    quiz_data = []
    
    # Split the response into lines
    lines = response.split("\n")
    
    # Variables to store current question and its type
    current_question = None
    question_type = None
    
    for line in lines:
        line = line.strip()

        # If the line starts with a number followed by a period (indicating a new question)
        if line and line[0].isdigit():
            # If there's a current question, add it to quiz_data
            if current_question:
                quiz_data.append(current_question)

            # Parse the question type (e.g., Multiple Choice, True/False, etc.)
            question_type = None
            if "Multiple Choice" in line:
                question_type = "Multiple Choice"
            elif "True/False" in line:
                question_type = "True/False"
            elif "Short Answer" in line:
                question_type = "Short Answer"
            elif "Fill in the Blank" in line:
                question_type = "Fill in the Blank"
            elif "Essay" in line:
                question_type = "Essay"

            # Set the new current question
            current_question = {
                "question": line.split(": ", 1)[1],  # Everything after the first ": "
                "type": question_type,
                "options": []  # We'll add options if it's multiple choice
            }

        # If it's a multiple choice option (starts with "(a)", "(b)", etc.)
        elif line.startswith("("):
            if current_question and question_type == "Multiple Choice":
                current_question["options"].append(line)
        
        # If it's a question without options (True/False, Short Answer, etc.)
        elif line:
            if current_question and question_type != "Multiple Choice":
                # Add any other types of questions (True/False, Short Answer, etc.)
                current_question["options"].append(line)

    # Add the last question if it exists
    if current_question:
        quiz_data.append(current_question)
    
    # Return the quiz in a structured format
    print(quiz_data)
    return {"quiz": quiz_data}
