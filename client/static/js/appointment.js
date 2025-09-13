document.addEventListener("DOMContentLoaded", () => {
  const authModal = document.getElementById("authModal");
  const closeAuth = document.getElementById("closeAuth");
  const authForm = document.getElementById("authForm");
  const authTitle = document.getElementById("authTitle");
  const switchToRegister = document.getElementById("switchToRegister");
  const forgotPassword = document.getElementById("forgotPassword");
  const navLinks = document.getElementById("navLinks");
  const toast = document.getElementById("toast");

  const doctorsContainer = document.getElementById("doctorsContainer");
  const citySelect = document.getElementById("citySelect");

  let isRegister = false;

  /* ---------- Open Modal ---------- */
  document.getElementById("appointmentBtn").addEventListener("click", (e) => {
    e.preventDefault();
    authModal.classList.add("show");
  });

  /* ---------- Close Modal ---------- */
  closeAuth.addEventListener("click", () => {
    authModal.classList.remove("show");
    setTimeout(() => (authModal.style.display = "none"), 300);
  });

  window.onclick = function (e) {
    if (e.target === authModal) {
      closeAuth.click();
    }
  };

  /* ---------- Switch Login/Register ---------- */
  switchToRegister.addEventListener("click", (e) => {
    e.preventDefault();
    isRegister = !isRegister;
    if (isRegister) {
      authTitle.textContent = "User Register";
      authForm.querySelector("button").textContent = "Register";
      switchToRegister.textContent = "Login";
    } else {
      authTitle.textContent = "User Login";
      authForm.querySelector("button").textContent = "Login";
      switchToRegister.textContent = "Register";
    }
  });

  /* ---------- Forgot Password ---------- */
  forgotPassword.addEventListener("click", (e) => {
    e.preventDefault();
    showToast("Password reset link sent to your email.", "success");
    // TODO: Backend email integration
  });

  /* ---------- Form Submit ---------- */
  authForm.addEventListener("submit", (e) => {
    e.preventDefault();

    const username = e.target.username.value.trim();
    const email = e.target.email.value.trim();
    const phone = e.target.phone.value.trim();
    const password = e.target.password.value.trim();

    if (!username || !email || !phone || !password) {
      showToast("Please fill all fields.", "error");
      return;
    }

    if (isRegister) {
      showToast("Registered successfully!", "success");
    } else {
      showToast("Login successful!", "success");
    }

    closeAuth.click();

    if (!document.getElementById("navUser")) {
      let userItem = document.createElement("li");
      userItem.id = "navUser";
      userItem.innerHTML = `<a href="#">${username}</a>`;
      navLinks.appendChild(userItem);
    }
  });

  /* ---------- Doctors List with City Filter ---------- */
  const cities = ["Bangalore", "Mumbai", "Delhi", "Hyderabad"];
  cities.forEach((city) => {
    let opt = document.createElement("option");
    opt.value = city;
    opt.textContent = city;
    citySelect.appendChild(opt);
  });

  citySelect.addEventListener("change", () => {
    const selectedCity = citySelect.value;
    if (!selectedCity) {
      doctorsContainer.innerHTML = "";
      return;
    }

    doctorsContainer.style.opacity = 0;
    setTimeout(() => {
      doctorsContainer.innerHTML = `
        <p>Showing doctors in <b>${selectedCity}</b></p>
        <ul>
          <li>Dr. Sharma - Cardiologist</li>
          <li>Dr. Patel - Neurologist</li>
          <li>Dr. Khan - Orthopedic</li>
        </ul>
      `;
      doctorsContainer.style.opacity = 1;
    }, 300);
  });

  /* ---------- Toast Function ---------- */
  function showToast(message, type = "success") {
    toast.textContent = message;
    toast.className = `toast show ${type}`;
    setTimeout(() => {
      toast.className = "toast";
    }, 3000);
  }
});
