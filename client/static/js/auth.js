/* ==========================
   GLOBAL DOM HELPERS
========================== */
function showBox(boxId) {
  document
    .querySelectorAll(".auth-box")
    .forEach((b) => (b.style.display = "none"));
  document.getElementById(boxId).style.display = "flex";
}

function closeAuthPopup() {
  document.getElementById("authMasterPopup").style.display = "none";
}

/* ==========================
   ROLE SELECTION
========================== */
function selectRole(role) {
  if (role === "patient") {
    showBox("patientSignupBox");
  } else if (role === "doctor") {
    showBox("doctorSignupBox");
  }
}

function openLogin() {
  // Default to patient login, user can switch
  showBox("patientLoginBox");
}

function openForgotPassword() {
  showBox("forgotBox");
}

function openAdminLogin() {
  showBox("adminLoginBox");
}

function showRoleBox() {
  showBox("roleBox");
}

/* ==========================
   POPUP TRIGGER (3-bar menu)
========================== */
document.addEventListener("DOMContentLoaded", () => {
  const menuIcon = document.querySelector(".menu-icon");
  const authPopup = document.getElementById("authMasterPopup");

  if (menuIcon && authPopup) {
    menuIcon.addEventListener("click", () => {
      authPopup.style.display = "flex";
      showRoleBox();
    });

    // Close when clicking outside
    authPopup.addEventListener("click", (e) => {
      if (e.target === authPopup) closeAuthPopup();
    });
  }
});

/* ==========================
   BACKEND API CALL (HELPER)
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

/* ==========================
   SEND OTP (Patient / Doctor / Forgot)
========================== */
async function sendOTP(type) {
  let email = null;
  let purpose = null;

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

  if (!email) return alert("Please enter email");

  const res = await api("/auth/send-otp", "POST", { email, purpose });

  alert(res.msg || (res.status === "success" ? "OTP sent!" : "Failed"));
}

/* ==========================
   PATIENT SIGNUP
========================== */
async function patientSignup() {
  const name = document.getElementById("p_name").value;
  const email = document.getElementById("p_email").value;
  const otp = document.getElementById("p_otp").value;
  const pass = document.getElementById("p_pass").value;

  if (!name || !email || !otp || !pass) return alert("All fields required");

  const verify = await api("/auth/verify-otp", "POST", { email, otp });
  if (verify.status !== "success") return alert(verify.msg);

  const signup = await api("/auth/signup", "POST", {
    name,
    email,
    password: pass,
    role: "patient",
  });

  alert(signup.msg);

  if (signup.status === "success") openLogin();
}

/* ==========================
   DOCTOR SIGNUP (only base user)
========================== */
async function doctorSignup() {
  const name = document.getElementById("d_name").value;
  const email = document.getElementById("d_email").value;
  const otp = document.getElementById("d_otp").value;
  const pass = document.getElementById("d_pass").value;

  if (!name || !email || !otp || !pass) return alert("All fields required");

  const verify = await api("/auth/verify-otp", "POST", { email, otp });
  if (verify.status !== "success") return alert(verify.msg);

  const signup = await api("/auth/signup", "POST", {
    name,
    email,
    password: pass,
    role: "doctor",
  });

  alert(signup.msg);

  if (signup.status === "success") {
    alert("Account created. Please login and complete registration.");
    openLogin();
  }
}

/* ==========================
   PATIENT LOGIN
========================== */
async function patientLogin() {
  const email = document.getElementById("pl_email").value;
  const pass = document.getElementById("pl_pass").value;

  if (!email || !pass) return alert("Email and password required");

  const res = await api("/auth/login", "POST", { email, password: pass });

  if (res.status !== "success") return alert(res.msg);

  alert("Login success!");
  window.location.reload();
}

/* ==========================
   DOCTOR LOGIN
========================== */
async function doctorLogin() {
  const email = document.getElementById("dl_email").value;
  const pass = document.getElementById("dl_pass").value;

  const res = await api("/auth/login", "POST", { email, password: pass });

  if (res.status !== "success") return alert(res.msg);

  alert("Doctor login success!");

  // redirect doctor to profile completion or status check later
  window.location.reload();
}

/* ==========================
   ADMIN LOGIN
========================== */
async function adminLogin() {
  const email = document.getElementById("a_email").value;
  const pass = document.getElementById("a_pass").value;

  const res = await api("/admin/login", "POST", { email, password: pass });

  if (res.status !== "success") return alert(res.msg);

  alert("Admin login success!");
  window.location.href = "/admin/dashboard"; // later update
}

/* ==========================
   RESET PASSWORD
========================== */
async function resetPassword() {
  const email = document.getElementById("fp_email").value;
  const otp = document.getElementById("fp_otp").value;
  const pass = document.getElementById("fp_pass").value;

  if (!email || !otp || !pass) return alert("All fields required");

  const res = await api("/auth/reset", "POST", { email, otp, password: pass });

  alert(res.msg);

  if (res.status === "success") openLogin();
}

async function sendOTP(role) {
  let email = "";

  if (role === "patient") {
    email = document.getElementById("p_email").value;
  } else if (role === "doctor") {
    email = document.getElementById("d_email").value;
  } else {
    alert("Invalid role");
    return;
  }

  if (!email) {
    alert("Please enter email first");
    return;
  }

  let res = await fetch("/auth/send-otp", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email: email }),
  });

  let data = await res.json();
  alert(data.msg);
}
