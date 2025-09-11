// Sidebar toggles
const doctorBtn = document.getElementById("doctorBtn");
const userBtn = document.getElementById("userBtn");
const doctorForm = document.getElementById("doctorForm");
const userForm = document.getElementById("userForm");
const closeDoctor = document.getElementById("closeDoctor");
const closeUser = document.getElementById("closeUser");

doctorBtn.addEventListener("click", () => doctorForm.classList.add("active"));
userBtn.addEventListener("click", () => userForm.classList.add("active"));
closeDoctor.addEventListener("click", () =>
  doctorForm.classList.remove("active")
);
closeUser.addEventListener("click", () => userForm.classList.remove("active"));

// Toast Notification
function showToast(message, type) {
  const toast = document.getElementById("toast");
  toast.textContent = message;
  toast.className = `toast show ${type}`;
  setTimeout(() => {
    toast.className = "toast";
  }, 3000);
}

// Doctor Registration Validation
document
  .getElementById("doctorRegisterForm")
  .addEventListener("submit", function (e) {
    e.preventDefault();
    const license = this.license.value.trim();
    const licensePattern = /^[A-Z]{3}[0-9]{3}@gov\.ac\.in$/;

    if (!licensePattern.test(license)) {
      showToast("❌ Invalid License Format! Must be ABC123@gov.ac.in", "error");
      return;
    }

    showToast("✅ Doctor Registered Successfully!", "success");
    doctorForm.classList.remove("active");

    // Simulate adding doctor to list (later from DB)
    const card = document.createElement("div");
    card.className = "doctor-card";
    card.innerHTML = `
    <h3>${this.name.value}</h3>
    <p><b>Specialization:</b> ${this.specialization.value}</p>
    <p><b>Experience:</b> ${this.experience.value} years</p>
    <p><b>Hospital:</b> ${this.location.value}</p>
    <p><b>Services:</b> ${this.services.value}</p>
    <button class="btn">Book Appointment</button>
  `;
    document.getElementById("doctorCards").appendChild(card);

    this.reset();
  });

// User Login
document
  .getElementById("userLoginForm")
  .addEventListener("submit", function (e) {
    e.preventDefault();
    showToast("✅ User Logged In Successfully!", "success");
    userForm.classList.remove("active");
    this.reset();
  });
