/* ==========================
    GLOBAL HELPERS
========================== */
function showBox(boxId) {
  document.querySelectorAll(".auth-box").forEach(b => b.style.display = "none");
  document.getElementById(boxId).style.display = "flex";
}

function closeAuthPopup() {
  document.getElementById("authMasterPopup").style.display = "none";
}

/* ==========================
    ROLE SWITCHING
========================== */
function selectRole(role) {
  showBox(role === "patient" ? "patientSignupBox" : "doctorSignupBox");
}

function openLogin() { showBox("patientLoginBox"); }
function openForgotPassword() { showBox("forgotBox"); }
function openAdminLogin() { showBox("adminLoginBox"); }
function showRoleBox() { showBox("roleBox"); }

/* ==========================
    EMAIL VALIDATION
========================== */
function validateEmail(email) {
  return /\S+@\S+\.\S+/.test(email);
}

/* ==========================
    SETUP OTP FIELD
========================== */
function setupOtpField(emailId, buttonId) {
  const emailInput = document.getElementById(emailId);
  const sendBtn = document.getElementById(buttonId);
  if (!emailInput || !sendBtn) return;

  sendBtn.disabled = true;
  emailInput.addEventListener("input", () => {
    sendBtn.disabled = !validateEmail(emailInput.value.trim());
  });
}

/* ==========================
    API HELPER
========================== */
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

/* ==========================
    OTP STATE
========================== */
let otpVerified = { patient: false, doctor: false };

/* ==========================
    SHOW VERIFIED
========================== */
function showVerified(type) {
  otpVerified[type] = true;
  const input = document.getElementById(type === "patient" ? "p_otp" : "d_otp");
  input.style.border = "2px solid #28a745";
  input.style.color = "#28a745";
  input.style.fontWeight = "bold";
}

/* ==========================
    SEND OTP
========================== */
async function sendOTP(type) {
  let email = "";

  if (type === "patient") email = p_email.value;
  if (type === "doctor") email = d_email.value;
  if (type === "forgot") email = fp_email.value;

  if (!validateEmail(email)) return alert("Enter valid email!");

  const res = await api("/auth/send-otp", "POST", { email, purpose: "signup" });
  alert(res.msg);
}

/* ==========================
    SIGNUP
========================== */
async function patientSignup() {
  const name = p_name.value, email = p_email.value, otp = p_otp.value, pass = p_pass.value;

  if (!name || !email || !otp || !pass) return alert("All fields required!");

  if (!otpVerified.patient) {
    const v = await api("/auth/verify-otp", "POST", { email, otp });
    if (v.status !== "success") return alert(v.msg);
    showVerified("patient");
  }

  const res = await api("/auth/signup", "POST", { name, email, password: pass, role: "patient" });
  alert(res.msg);
  if (res.status === "success") openLogin();
}

async function doctorSignup() {
  const name = d_name.value, email = d_email.value, otp = d_otp.value, pass = d_pass.value;

  if (!name || !email || !otp || !pass) return alert("All fields required!");

  if (!otpVerified.doctor) {
    const v = await api("/auth/verify-otp", "POST", { email, otp });
    if (v.status !== "success") return alert(v.msg);
    showVerified("doctor");
  }

  const res = await api("/auth/signup", "POST", { name, email, password: pass, role: "doctor" });
  alert(res.msg);
  if (res.status === "success") openLogin();
}

/* ==========================
    LOGIN
========================== */
async function patientLogin() {
  const email = pl_email.value, pass = pl_pass.value;
  const res = await api("/auth/login", "POST", { email, password: pass });

  if (res.status !== "success") return alert(res.msg);

  localStorage.setItem("user_name", res.name);
  localStorage.setItem("user_role", res.role);

  window.location.href = "/";
}

async function doctorLogin() {
  const email = dl_email.value, pass = dl_pass.value;
  const res = await api("/auth/login", "POST", { email, password: pass });

  if (res.status !== "success") return alert(res.msg);

  localStorage.setItem("user_name", res.name);
  localStorage.setItem("user_role", res.role);

  window.location.href = "/";
}

async function adminLogin() {
  const res = await api("/admin/login", "POST", { email: a_email.value, password: a_pass.value });

  if (res.status !== "success") return alert(res.msg);

  window.location.href = "/admin/dashboard";
}

/* ==========================
    NAVBAR USER AVATAR
========================== */
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
    dropdown.style.display = dropdown.style.display === "flex" ? "none" : "flex";
  };

  document.addEventListener("click", (e) => {
    if (!userContainer.contains(e.target)) dropdown.style.display = "none";
  });
}

/* ==========================
    LOGOUT
========================== */
function logoutUser() {
  localStorage.removeItem("user_name");
  localStorage.removeItem("user_role");
  window.location.href = "/";
}

/* ==========================
    INIT ON PAGE LOAD
========================== */
document.addEventListener("DOMContentLoaded", () => {
  setupOtpField("p_email", "p_send_btn");
  setupOtpField("d_email", "d_send_btn");
  setupOtpField("fp_email", "fp_send_btn");
  initUserNavbar();
});
