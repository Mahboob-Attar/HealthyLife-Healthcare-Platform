// chatbot.js

document.addEventListener("DOMContentLoaded", () => {
  const chatbotIcon = document.getElementById("chatbotIcon");
  const chatPopup = document.getElementById("chatPopup");
  const closeChat = document.getElementById("closeChat");
  const sendBtn = document.getElementById("sendBtn");
  const userInput = document.getElementById("userInput");
  const chatBody = document.getElementById("chatBody");

  // Open chatbot popup
  chatbotIcon.addEventListener("click", () => {
    chatPopup.classList.add("active");
    userInput.focus();

    // Show fresh welcome message when opening
    chatBody.innerHTML = `<p><b>Nurse:</b> Hi 👩‍⚕️ How can I help you today?</p>`;
  });

  // Close chatbot popup and clear messages
  closeChat.addEventListener("click", () => {
    chatPopup.classList.remove("active");
    chatBody.innerHTML = "";
    userInput.value = "";
  });

  // Send message on Enter key
  userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      sendMessage();
    }
  });

  // Send message on button click
  sendBtn.addEventListener("click", sendMessage);

  // Send message function
  function sendMessage() {
    const message = userInput.value.trim();
    if (message === "") return;

    // Show user message
    appendMessage("You", message, "user");

    // Clear input field
    userInput.value = "";

    // Show typing indicator
    const typingIndicator = document.createElement("div");
    typingIndicator.classList.add("nurse-msg");
    typingIndicator.innerHTML = `<b>Nurse:</b> <i>Typing...</i>`;
    chatBody.appendChild(typingIndicator);
    chatBody.scrollTop = chatBody.scrollHeight;

    // Fetch Nurse response from Flask API
    fetch("/chatbot", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: message }),
    })
      .then((res) => res.json())
      .then((data) => {
        typingIndicator.remove();
        appendMessage("Nurse", data.reply, "nurse");
      })
      .catch((err) => {
        typingIndicator.remove();
        appendMessage(
          "Nurse",
          "⚠️ Sorry, something went wrong. Please try again.",
          "nurse"
        );
        console.error("Chatbot Error:", err);
      });
  }

  // Append message to chat body
  function appendMessage(sender, message, type) {
    const msgDiv = document.createElement("div");
    msgDiv.classList.add(`${type}-msg`);
    msgDiv.innerHTML = `<b>${sender}:</b> ${message}`;
    chatBody.appendChild(msgDiv);
    chatBody.scrollTop = chatBody.scrollHeight;
  }
});
