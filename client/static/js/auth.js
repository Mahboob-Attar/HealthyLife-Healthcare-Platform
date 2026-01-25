/* ==========================
   GLOBAL DOM HELPERS
========================== */
function showBox(boxId) {
  document.querySelectorAll(".auth-box").forEach(b => (b.style.display = "none"));
  document.getElementById(boxId).style.display = "flex";
}

function closeAuthPopup() {
  document.getElementById("authMasterPopup").style.display = "none";
}

/* ==========================
   ROLE SELECTION
========================== */
function selectRole(role) {
  if (role === "patient") showBox("patientSignupBox");
  if (role === "doctor") showBox("doctorSignupBox");
}

function openLogin() { showBox("patientLoginBox"); }
function openForgotPassword() { showBox("forgotBox"); }
function openAdminLogin() { showBox("adminLoginBox"); }
function showRoleBox() { showBox("roleBox"); }

/* ==========================
   POPUP TRIGGER
========================== */
document.addEventListener("DOMContentLoaded", () => {
  const menuIcon = document.querySelector(".menu-icon");
  const authPopup = document.getElementById("authMasterPopup");

  if (menuIcon && authPopup) {
    menuIcon.addEventListener("click", () => {
      authPopup.style.display = "flex";
      showRoleBox();
    });

    authPopup.addEventListener("click", e => {
      if (e.target === authPopup) closeAuthPopup();
    });
  }

  setupOtpField("p_email", "p_send_btn");
  setupOtpField("d_email", "d_send_btn");
  setupOtpField("fp_email", "fp_send_btn");
});

/* ==========================
   EMAIL VALIDATION
========================== */
function validateEmail(email) {
  return /\S+@\S+\.\S+/.test(email);
}

function setupOtpField(emailId, buttonId) {
  const emailInput = document.getElementById(emailId);
  const sendBtn = document.getElementById(buttonId);

  if (!emailInput || !sendBtn) return;

  sendBtn.disabled = true; // disable initially

  emailInput.addEventListener("input", () => {
    const val = emailInput.value.trim();
    sendBtn.disabled = !validateEmail(val);
  });
}

/* ==========================
   API WRAPPER
========================== */
async function api(url, method = "POST", data = {}) {
  try {
    const res = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: method === "GET" ? null : JSON.stringify(data),
    });
    return res.json();
  } catch (err) {
    return { status: "error", msg: "Network error" };
  }
}

/* ===================================
   OTP TIMER + RESEND HANDLER
=================================== */
let otpTimers = {};

function startOtpTimer(role) {
  let timerSpan = document.getElementById(`${role}_timer`);
  let sendBtn = document.getElementById(`${role}_send_btn`);
  let resendBtn = document.getElementById(`${role}_resend_btn`);

  if (otpTimers[role]) clearInterval(otpTimers[role]);

  let remaining = 120; // 2 minutes

  sendBtn.style.display = "none";
  resendBtn.style.display = "none";
  timerSpan.style.display = "inline-block";
  timerSpan.innerText = `(${remaining}s)`;

  otpTimers[role] = setInterval(() => {
    remaining--;
    timerSpan.innerText = `(${remaining}s)`;

    if (remaining <= 0) {
      clearInterval(otpTimers[role]);
      timerSpan.innerText = "";
      resendBtn.style.display = "inline-block";
    }
  }, 1000);
}

/* ==========================
   SEND OTP
========================== */
async function sendOTP(type) {
  let email = "", purpose = "";

  if (type === "patient") {
    email = document.getElementById("p_email").value;
    purpose = "signup";
  }
  if (type === "doctor") {
    email = document.getElementById("d_email").value;
    purpose = "signup";
  }
  if (type === "forgot") {
    email = document.getElementById("fp_email").value;
    purpose = "forgot";
  }

  if (!validateEmail(email)) return alert("Enter valid email!");

  const res = await api("/auth/send-otp", "POST", { email, purpose });

  alert(res.msg);

  if (res.status === "success") startOtpTimer(type);
}

/* ==========================
   PATIENT SIGNUP
========================== */
async function patientSignup() {
  const name = p_name.value, email = p_email.value, otp = p_otp.value, pass = p_pass.value;

  if (!name || !email || !otp || !pass) return alert("All fields required");

  const verify = await api("/auth/verify-otp", "POST", { email, otp });
  if (verify.status !== "success") return alert(verify.msg);

  const signup = await api("/auth/signup", "POST", { name, email, password: pass, role: "patient" });

  alert(signup.msg);
  if (signup.status === "success") openLogin();
}

/* ==========================
   DOCTOR SIGNUP
========================== */
async function doctorSignup() {
  const name = d_name.value, email = d_email.value, otp = d_otp.value, pass = d_pass.value;

  if (!name || !email || !otp || !pass) return alert("All fields required");

  const verify = await api("/auth/verify-otp", "POST", { email, otp });
  if (verify.status !== "success") return alert(verify.msg);

  const signup = await api("/auth/signup", "POST", { name, email, password: pass, role: "doctor" });

  alert(signup.msg);
  if (signup.status === "success") {
    alert("Account created. Please login & complete registration.");
    openLogin();
  }
}

/* ==========================
   PATIENT LOGIN
========================== */
async function patientLogin() {
  const email = pl_email.value, pass = pl_pass.value;
  if (!email || !pass) return alert("Email & password required");

  const res = await api("/auth/login", "POST", { email, password: pass });
  if (res.status !== "success") return alert(res.msg);

  window.location.reload();
}

/* ==========================
   DOCTOR LOGIN
========================== */
async function doctorLogin() {
  const email = dl_email.value, pass = dl_pass.value;
  const res = await api("/auth/login", "POST", { email, password: pass });

  if (res.status !== "success") return alert(res.msg);
  window.location.reload();
}

/* ==========================
   ADMIN LOGIN
========================== */
async function adminLogin() {
  const email = a_email.value, pass = a_pass.value;
  const res = await api("/admin/login", "POST", { email, password: pass });

  if (res.status !== "success") return alert(res.msg);
  window.location.href = "/admin/dashboard";
}

/* ==========================
   RESET PASSWORD
========================== */
async function resetPassword() {
  const email = fp_email.value, otp = fp_otp.value, pass = fp_pass.value;

  if (!email || !otp || !pass) return alert("All fields required");

  const res = await api("/auth/reset", "POST", { email, otp, password: pass });

  alert(res.msg);
  if (res.status === "success") openLogin();
}
