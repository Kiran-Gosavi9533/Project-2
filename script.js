document.addEventListener("DOMContentLoaded", function () {
    const chatbox = document.getElementById("chatbox");
    const userMessageInput = document.getElementById("user-message");
    const sendButton = document.getElementById("send-button");

    if (!sendButton) {
        console.error("Send button not found! Make sure the button has id='send-button'.");
        return;
    }

    // Function to append messages to chatbox
    function appendMessage(sender, message, isImage = false) {
        const messageElement = document.createElement("div");
        messageElement.classList.add(sender);

        const timestamp = document.createElement("span");
        timestamp.classList.add("timestamp");
        timestamp.textContent = new Date().toLocaleTimeString();

        if (isImage) {
            const imgElement = document.createElement("img");
            imgElement.src = message;
            imgElement.style.width = "200px";
            imgElement.style.borderRadius = "10px";
            messageElement.appendChild(imgElement);
        } else {
            messageElement.textContent = message;
        }

        messageElement.appendChild(timestamp);
        chatbox.appendChild(messageElement);
        chatbox.scrollTop = chatbox.scrollHeight;
    }

    function showTypingIndicator() {
        if (!document.querySelector(".typing-indicator")) {
            const typingIndicator = document.createElement("div");
            typingIndicator.classList.add("bot", "typing-indicator");
            typingIndicator.textContent = "Bot is typing...";
            chatbox.appendChild(typingIndicator);
            chatbox.scrollTop = chatbox.scrollHeight;
        }
    }

    function removeTypingIndicator() {
        const typingIndicator = document.querySelector(".typing-indicator");
        if (typingIndicator) typingIndicator.remove();
    }

    function sendMessage() {
        const userMessage = userMessageInput.value.trim();
        if (userMessage === "") return;

        appendMessage("user", userMessage);
        userMessageInput.value = "";
        sendButton.disabled = true;

        showTypingIndicator();

        fetch("/chat", {
            method: "POST",
            body: JSON.stringify({ message: userMessage }),
            headers: { "Content-Type": "application/json" },
        })
        .then(response => response.json())
        .then(data => {
            removeTypingIndicator();
            if (data.reply.startsWith("http")) {
                appendMessage("bot", data.reply, true);
            } else {
                appendMessage("bot", data.reply);
            }
        })
        .catch(error => {
            removeTypingIndicator();
            console.error("Error:", error);
            appendMessage("bot", "Sorry, something went wrong. Please try again.");
        })
        .finally(() => {
            sendButton.disabled = false;
        });
    }

    sendButton.addEventListener("click", sendMessage);
    userMessageInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            sendMessage();
        }
    });
});
