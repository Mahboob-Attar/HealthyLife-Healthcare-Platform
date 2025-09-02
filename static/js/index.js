//  Wait until DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  const predictBtn = document.getElementById("predictBtn");
  const chatbotBtn = document.getElementById("chatbotBtn");

  // Predict Now Button → Go to Diagnostics Page
  if (predictBtn) {
    predictBtn.addEventListener("click", () => {
      window.location.href = "/diagnostics";
    });
  }

  // Chatbot Image → Go to Chatbot Page
  if (chatbotBtn) {
    chatbotBtn.addEventListener("click", () => {
      window.location.href = "/chatbot";
    });
  }
});
