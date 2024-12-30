
# 📚 Quiz and Chat System with RAG-based Solution

## 🚀 Overview

This project is a **Retrieval-Augmented Generation (RAG)** based application designed to **upload documents, generate quizzes, and enable users to chat with the document content**. It integrates advanced AI tools and frameworks for efficient content processing, embedding generation, and intelligent response generation.

---

## 🎯 Features

- **📂 File Upload and Text Extraction:**  
   - Upload PDF files and extract meaningful text content seamlessly.

- **📝 Quiz Generation:**  
   - Generate quizzes dynamically from uploaded document content.  
   - Customize difficulty levels, number of questions, language, and question types.

- **💬 Chat with Uploaded Content:**  
   - Interact conversationally with the uploaded document using an AI-powered interface.

- **⚙️ RAG-based Architecture:**  
   - **FAISS:** Enables efficient document retrieval.  
   - **HuggingFace Embeddings:** Provides semantic search capabilities.  
   - **Google Generative AI (Gemini):** Generates quiz content and chat responses.

---

## 🛠️ Technologies Used

- **LangChain:** For constructing and managing the RAG pipeline.  
- **HuggingFace Transformers:** For embedding generation.  
- **FAISS:** For optimized vector search and retrieval.  
- **Google Generative AI (Gemini):** For natural language generation tasks.  
- **FastAPI:** For building RESTful APIs.  
- **dotenv:** For managing environment variables securely.  
- **Python:** Core programming language.

---

## 📥 Installation

Follow these steps to set up the project:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Sharif37/AI_Driven_Notebook.git
   cd quiz-rag-system
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   - Create a `.env` file in the root directory.
   - Add your Google Generative AI API key:
     ```env
     GEMINI_API_KEY=your_api_key
     ```

4. **Run the server:**
   ```bash
   uvicorn app.main:app --reload
   ```

---

## 📡 API Endpoints

### **1. Upload File and Generate Quiz**

- **Endpoint:** `/upload/`  
- **Method:** `POST`  
- **Parameters:**  
   - `file` (PDF file)  
   - `difficulty` (e.g., "easy", "medium", "hard")  
   - `num_questions` (integer)  
   - `language` (e.g., "English")  
   - `question_type` (e.g., "mcq", "true-false")  

- **Response:** JSON object containing the generated quiz.

### **Example Request (Using cURL)**

```bash
curl -X POST "http://127.0.0.1:8000/upload/"   -F "file=@path_to_file.pdf"   -F "difficulty=medium"   -F "num_questions=5"   -F "language=English"   -F "question_type=mcq"
```

**Response Example:**
```json
{
  "quiz": [
    {
      "question": "What is the main topic of the document?",
      "options": ["A", "B", "C", "D"],
      "correct_answer": "A"
    }
  ]
}
```

---

## ⚖️ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
