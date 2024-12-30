// Prevent form submission and page reload
document.getElementById("quizForm").addEventListener("submit", async function(event) {
    event.preventDefault();  // Prevent default form submission and page reload

    const form = event.target;
    const formData = new FormData(form);
    const loadingSpinner = document.querySelector(".loading-spinner");
    const errorMessage = document.getElementById("errorMessage");
    const quizResults = document.getElementById("quizResults");
    const quizContent = document.getElementById("quizContent");

    loadingSpinner.style.display = "inline-block"; // Show loading spinner
    errorMessage.style.display = "none"; // Hide previous error message
    quizResults.style.display = "none"; // Hide quiz results initially

    try {
        // Send the form data to the server
        const response = await fetch("/upload/", {
            method: "POST",
            body: formData
        });

        const data = await response.json();
        loadingSpinner.style.display = "none"; // Hide loading spinner

        if (data.quiz) {
            quizResults.style.display = "block";
            quizContent.innerHTML = JSON.stringify(data.quiz, null, 2); // Display quiz data
        } else if (data.error) {
            errorMessage.style.display = "block";
            errorMessage.textContent = `Error: ${data.error}`;
        }
    } catch (error) {
        loadingSpinner.style.display = "none"; // Hide loading spinner
        errorMessage.style.display = "block";
        errorMessage.textContent = `Error: ${error.message}`;
    }
});

// Chat functionality
document.getElementById("sendChatBtn").addEventListener("click", async function() {
    const chatInput = document.getElementById("chatInput");
    const chatBox = document.getElementById("chatBox");

    const message = chatInput.value.trim();
    if (message) {
        // Display user message
        const userMessageDiv = document.createElement("div");
        userMessageDiv.classList.add("chat-message", "user");
        userMessageDiv.textContent = `You: ${message}`;
        chatBox.appendChild(userMessageDiv);

        // Scroll to the bottom of the chat
        chatBox.scrollTop = chatBox.scrollHeight;

        // Clear the input field
        chatInput.value = "";

        try {
            // Send the message to the chat endpoint
            const response = await fetch("/chat/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ message })
            });

            const data = await response.json();

            // Display bot response
            const botMessageDiv = document.createElement("div");
            botMessageDiv.classList.add("chat-message", "bot");
            botMessageDiv.textContent = `Bot: ${data.response}`;
            chatBox.appendChild(botMessageDiv);

            // Scroll to the bottom of the chat
            chatBox.scrollTop = chatBox.scrollHeight;
        } catch (error) {
            console.error("Error:", error);
        }
    }
});
