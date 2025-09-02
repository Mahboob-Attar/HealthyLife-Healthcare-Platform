document.addEventListener("DOMContentLoaded", () => {
  const sendBtn = document.getElementById("sendBtn");
  const userInput = document.getElementById("userInput");
  const chatbox = document.getElementById("chatbox");
  const loadingMsg = document.createElement("div");

  // Loader Styling
  loadingMsg.classList.add("bot-msg");
  loadingMsg.innerHTML = "🤖 Typing...";
  loadingMsg.style.opacity = "0.7";
  loadingMsg.style.fontStyle = "italic";

  // Send Button Click
  sendBtn.addEventListener("click", sendMessage);

  // Enter Key Press
  userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      sendMessage();
    }
  });

  // Send Message Function
  function sendMessage() {
    const message = userInput.value.trim();
    if (message === "") return;

    appendMessage("user", message);
    userInput.value = "";

    // Show loader while waiting
    chatbox.appendChild(loadingMsg);
    chatbox.scrollTop = chatbox.scrollHeight;

    // Send message to Flask backend
    fetch("/chatbot/get_response", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    })
      .then((res) => res.json())
      .then((data) => {
        chatbox.removeChild(loadingMsg);
        appendMessage("bot", data.response);
      })
      .catch(() => {
        chatbox.removeChild(loadingMsg);
        appendMessage("bot", "⚠️ Server not responding. Try again later.");
      });
  }

  // Append Message Function
  function appendMessage(sender, text) {
    const msg = document.createElement("div");
    msg.classList.add(sender === "user" ? "user-msg" : "bot-msg");

    // Smooth typing effect for bot messages
    if (sender === "bot") {
      let index = 0;
      const typingInterval = setInterval(() => {
        msg.innerHTML = text.slice(0, index++);
        if (index > text.length) clearInterval(typingInterval);
      }, 15);
    } else {
      msg.textContent = text;
    }

    chatbox.appendChild(msg);
    chatbox.scrollTo({ top: chatbox.scrollHeight, behavior: "smooth" });
  }
});
