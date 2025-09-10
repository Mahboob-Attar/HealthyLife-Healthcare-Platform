document.addEventListener("DOMContentLoaded", () => {
  const predictBtn = document.getElementById("predictBtn");
  const chatbotIcon = document.getElementById("chatbotIcon");
  const chatPopup = document.getElementById("chatPopup");
  const closeChat = document.getElementById("closeChat");

  // Predict Now Button → Go to Diagnostics Page
  if (predictBtn) {
    predictBtn.addEventListener("click", () => {
      window.location.href = "/diagnostics";
    });
  }

  // Chatbot Icon → Toggle Chat Popup
  if (chatbotIcon && chatPopup) {
    chatbotIcon.addEventListener("click", () => {
      chatPopup.classList.add("active");
    });
  }

  // Close Button → Hide Chat Popup
  if (closeChat) {
    closeChat.addEventListener("click", () => {
      chatPopup.classList.remove("active");
    });
  }
});
