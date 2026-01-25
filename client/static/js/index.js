// ===================== INFO POPUPS =====================

// Popup Triggers
const aboutLink = document.querySelector('a[href="#about"]');
if (aboutLink) {
  aboutLink.addEventListener('click', (e) => {
    e.preventDefault();
    document.getElementById('aboutPopup')?.classList.add('active');
  });
}

const faqLink = document.querySelector('a[href="#faq"]');
if (faqLink) {
  faqLink.addEventListener('click', (e) => {
    e.preventDefault();
    document.getElementById('faqPopup')?.classList.add('active');
  });
}

const supportLink = document.querySelector('a[href="#contact"]');
if (supportLink) {
  supportLink.addEventListener('click', (e) => {
    e.preventDefault();
    document.getElementById('supportPopup')?.classList.add('active');
  });
}

// Close Info Popups
document.querySelectorAll('.close-info').forEach(btn => {
  btn.addEventListener('click', () => {
    const popupId = btn.getAttribute('data-close');
    document.getElementById(popupId)?.classList.remove('active');
  });
});

// ===================== AUTH POPUP =====================

function showRoleBox() {
  // Hide all boxes first
  document.querySelectorAll(".auth-box").forEach(box => {
    box.style.display = "none";
  });
  
  // Show role selector box
  const roleBox = document.getElementById("roleBox");
  if (roleBox) roleBox.style.display = "flex";
}

document.addEventListener("DOMContentLoaded", () => {
  const menuIcon = document.querySelector(".menu-icon");
  const authPopup = document.getElementById("authMasterPopup");

  // OPEN POPUP
  if (menuIcon && authPopup) {
    menuIcon.addEventListener("click", () => {
      authPopup.style.display = "flex";
      showRoleBox(); // always reset to role selection
    });

    // CLOSE ON CLICK OUTSIDE
    authPopup.addEventListener("click", (e) => {
      if (e.target === authPopup) {
        closeAuthPopup();
      }
    });
  }
});

function closeAuthPopup() {
  const authPopup = document.getElementById("authMasterPopup");
  if (authPopup) {
    authPopup.style.display = "none";
  }
}
// ===================== AUTH VIEW SWITCHING =====================

// Hide all forms
function hideAllAuthBoxes() {
  document.querySelectorAll(".auth-box").forEach(box => {
    box.style.display = "none";
  });
}

// Already have function showRoleBox() from above — we reuse it

// Select Role
function selectRole(role) {
  hideAllAuthBoxes();
  if (role === "patient") {
    document.getElementById("patientSignupBox").style.display = "flex";
  } else if (role === "doctor") {
    document.getElementById("doctorSignupBox").style.display = "flex";
  }
}

// Open Login Box
function openLogin() {
  hideAllAuthBoxes();
  // default go to patient login
  document.getElementById("patientLoginBox").style.display = "flex";
}

// Open Forgot Password
function openForgotPassword() {
  hideAllAuthBoxes();
  document.getElementById("forgotBox").style.display = "flex";
}

// Open Admin Login
function openAdminLogin() {
  hideAllAuthBoxes();
  document.getElementById("adminLoginBox").style.display = "flex";
}

// ===================== TEST BUTTON STUBS =====================

function sendOTP(type) {
  alert("Send OTP for: " + type);
}

function patientSignup() {
  alert("Patient Signup clicked");
}

function patientLogin() {
  alert("Patient Login clicked");
}

function doctorSignup() {
  alert("Doctor Signup clicked");
}

function doctorLogin() {
  alert("Doctor Login clicked");
}

function adminLogin() {
  alert("Admin Login clicked");
}

function resetPassword() {
  alert("Reset Password clicked");
}
