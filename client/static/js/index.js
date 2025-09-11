document.addEventListener("DOMContentLoaded", () => {
  const predictBtn = document.getElementById("predictBtn");
  const appointmentBtn = document.getElementById("appointmentbtn");
  const chatbotIcon = document.getElementById("chatbotIcon");
  const chatPopup = document.getElementById("chatPopup");
  const closeChat = document.getElementById("closeChat");

  // Predict Now Button → Go to Diagnostics Page
  if (predictBtn) {
    predictBtn.addEventListener("click", () => {
      window.location.href = "/diagnostics";
    });
  }

  // Appointment Now Button → Go to Appointment Portal
  if (appointmentBtn) {
    appointmentBtn.addEventListener("click", () => {
      window.location.href = "/appointment";
    });
  }

  // Chatbot Icon → Open Chat Popup
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
