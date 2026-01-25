// ===================== INFO POPUPS =====================

// Popup Triggers
const aboutLink = document.querySelector('a[href="#about"]');
if (aboutLink) {
  aboutLink.addEventListener("click", (e) => {
    e.preventDefault();
    document.getElementById("aboutPopup")?.classList.add("active");
  });
}

const faqLink = document.querySelector('a[href="#faq"]');
if (faqLink) {
  faqLink.addEventListener("click", (e) => {
    e.preventDefault();
    document.getElementById("faqPopup")?.classList.add("active");
  });
}

const supportLink = document.querySelector('a[href="#contact"]');
if (supportLink) {
  supportLink.addEventListener("click", (e) => {
    e.preventDefault();
    document.getElementById("supportPopup")?.classList.add("active");
  });
}

// Close Info Popups
document.querySelectorAll(".close-info").forEach((btn) => {
  btn.addEventListener("click", () => {
    const popupId = btn.getAttribute("data-close");
    document.getElementById(popupId)?.classList.remove("active");
  });
});

// ===================== AUTH POPUP HANDLING =====================

function showRoleBox() {
  document
    .querySelectorAll(".auth-box")
    .forEach((box) => (box.style.display = "none"));
  document.getElementById("roleBox").style.display = "flex";
}

function closeAuthPopup() {
  const authPopup = document.getElementById("authMasterPopup");
  if (authPopup) authPopup.style.display = "none";
}

document.addEventListener("DOMContentLoaded", () => {
  const menuIcon = document.querySelector(".menu-icon");
  const authPopup = document.getElementById("authMasterPopup");

  if (menuIcon && authPopup) {
    menuIcon.addEventListener("click", () => {
      authPopup.style.display = "flex";
      showRoleBox();
    });

    authPopup.addEventListener("click", (e) => {
      if (e.target === authPopup) closeAuthPopup();
    });
  }
});

// ===================== AUTH SWITCH VIEW =====================

function hideAllAuthBoxes() {
  document
    .querySelectorAll(".auth-box")
    .forEach((box) => (box.style.display = "none"));
}

function selectRole(role) {
  hideAllAuthBoxes();
  if (role === "patient") {
    document.getElementById("patientSignupBox").style.display = "flex";
  } else if (role === "doctor") {
    document.getElementById("doctorSignupBox").style.display = "flex";
  }
}

function openLogin() {
  hideAllAuthBoxes();
  document.getElementById("patientLoginBox").style.display = "flex";
}

function openForgotPassword() {
  hideAllAuthBoxes();
  document.getElementById("forgotBox").style.display = "flex";
}

function openAdminLogin() {
  hideAllAuthBoxes();
  document.getElementById("adminLoginBox").style.display = "flex";
}

// ===================== EMAIL VALIDATION FOR OTP =====================

function setupOtpField(emailInputId, sendBtnId) {
  const emailInput = document.getElementById(emailInputId);
  const sendBtn = document.getElementById(sendBtnId);

  if (!emailInput || !sendBtn) return;

  sendBtn.disabled = true;

  emailInput.addEventListener("input", () => {
    const val = emailInput.value.trim();
    sendBtn.disabled = !validateEmail(val);
  });
}

function validateEmail(email) {
  return /\S+@\S+\.\S+/.test(email);
}

setupOtpField("p_email", "p_send_btn");
setupOtpField("d_email", "d_send_btn");
setupOtpField("fp_email", "fp_send_btn");

