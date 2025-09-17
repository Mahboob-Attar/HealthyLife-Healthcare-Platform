// ================== General Index Script ================== //

// Chatbot Popup Logic
const chatbotIcon = document.getElementById("chatbotIcon");
const chatPopup = document.getElementById("chatPopup");
const closeChat = document.getElementById("closeChat");

chatbotIcon?.addEventListener("click", () => {
  chatPopup.classList.add("active");
});

closeChat?.addEventListener("click", () => {
  chatPopup.classList.remove("active");
});

// Doctor Registration Popup Logic
const doctorBtn = document.getElementById("doctorBtn");
const doctorPopup = document.getElementById("doctorPopup");
const closeDoctor = document.getElementById("closeDoctor"); 

// Open Doctor Popup
doctorBtn?.addEventListener("click", () => {
  doctorPopup.classList.add("active");
});

// Close Doctor Popup
closeDoctor?.addEventListener("click", () => {
  doctorPopup.classList.remove("active");
});