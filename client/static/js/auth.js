/* GLOBAL HELPERS*/
function showBox(boxId) {
  document
    .querySelectorAll(".auth-box")
    .forEach((b) => (b.style.display = "none"));
  document.getElementById(boxId).style.display = "flex";
}

function closeAuthPopup() {
  document.getElementById("authMasterPopup").style.display = "none";
}

/* NAVIGATION*/
function openLogin() {
  showBox("userLoginBox");
}
function openForgotPassword() {
  showBox("forgotBox");
}
function openAdminLogin() {
  showBox("adminLoginBox");
}
function openSignup() {
  showBox("userSignupBox");
}

/* EMAIL VALIDATION*/
function validateEmail(email) {
  return /\S+@\S+\.\S+/.test(email);
}

/* OTP FIELD SETUP*/
function setupOtpField(emailId, buttonId) {
  const emailInput = document.getElementById(emailId);
  const sendBtn = document.getElementById(buttonId);
  if (!emailInput || !sendBtn) return;

  sendBtn.disabled = true;
  emailInput.addEventListener("input", () => {
    sendBtn.disabled = !validateEmail(emailInput.value.trim());
  });
}

/* API HELPER*/
async function api(url, method = "POST", data = {}) {
  try {
    const res = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: method === "GET" ? null : JSON.stringify(data),
    });
    return await res.json();
  } catch {
    return { status: "error", msg: "Network error" };
  }
}

/* OTP STATE */
let otpVerified = false;

function showVerified() {
  otpVerified = true;
  const input = document.getElementById("u_otp");
  input.style.border = "2px solid #28a745";
  input.style.color = "#28a745";
  input.style.fontWeight = "bold";
}

/* SEND OTP */
async function sendOTP() {
  const email = u_email.value;
  if (!validateEmail(email)) return alert("Enter valid email!");

  const res = await api("/auth/send-otp", "POST", {
    email,
    purpose: "signup",
  });
  alert(res.msg);
}

/* USER SIGNUP */
async function userSignup() {
  const name = u_name.value;
  const email = u_email.value;
  const otp = u_otp.value;
  const pass = u_pass.value;

  if (!name || !email || !otp || !pass)
    return alert("All fields required!");

  if (!otpVerified) {
    const v = await api("/auth/verify-otp", "POST", { email, otp });
    if (v.status !== "success") return alert(v.msg);
    showVerified();
  }

  const res = await api("/auth/signup", "POST", {
    name,
    email,
    password: pass,
  });

  alert(res.msg);
  if (res.status === "success") openLogin();
}

/* USER LOGIN */
async function userLogin() {
  const email = ul_email.value;
  const pass = ul_pass.value;

  const res = await api("/auth/login", "POST", {
    email,
    password: pass,
  });

  if (res.status !== "success") return alert(res.msg);

  localStorage.setItem("user_name", res.name);
  window.location.href = "/";
}

/* ADMIN LOGIN*/
async function adminLogin() {
  const res = await api("/admin/login", "POST", {
    email: a_email.value,
    password: a_pass.value,
  });

  if (res.status !== "success") return alert(res.msg);
  window.location.href = "/admin/dashboard";
}

/* NAVBAR USER AVATAR*/
function initUserNavbar() {
  const user = localStorage.getItem("user_name");
  const menuIcon = document.getElementById("menuIcon");
  const userContainer = document.getElementById("navUserContainer");
  const avatar = document.getElementById("navUserAvatar");
  const dropdown = document.getElementById("userDropdown");

  if (user) {
    avatar.innerText = user.charAt(0).toUpperCase();
    menuIcon.style.display = "none";
    userContainer.style.display = "flex";
  }

  avatar.onclick = () => {
    dropdown.style.display =
      dropdown.style.display === "flex" ? "none" : "flex";
  };

  document.addEventListener("click", (e) => {
    if (!userContainer.contains(e.target)) dropdown.style.display = "none";
  });
}

/* LOGOUT*/
function logoutUser() {
  localStorage.removeItem("user_name");
  window.location.href = "/";
}

/* INIT */
document.addEventListener("DOMContentLoaded", () => {
  setupOtpField("u_email", "u_send_btn");
  setupOtpField("fp_email", "fp_send_btn");
  initUserNavbar();
});
