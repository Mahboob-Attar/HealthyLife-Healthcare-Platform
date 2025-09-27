const doctorBtn = document.getElementById("doctorBtn");
const doctorPopup = document.getElementById("doctorPopup");
const closeDoctor = document.getElementById("closeDoctor");
const doctorForm = document.getElementById("doctorForm");
const successPopup = document.getElementById("successPopup");
const closeSuccess = document.getElementById("closeSuccess");
const successMessage = document.getElementById("successMessage");

// Open popup
doctorBtn?.addEventListener("click", () => doctorPopup.classList.add("active"));
// Close popup
closeDoctor?.addEventListener("click", () => doctorPopup.classList.remove("active"));

// Form submission
doctorForm?.addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = new FormData(doctorForm);

  try {
    const response = await fetch("/register_doctor", {
      method: "POST",
      body: formData,
    });
    const result = await response.json();

    if (result.success) {
      doctorForm.reset();
      successMessage.innerHTML =
        "✅ Successfully Registered! Visit Support page if needed.";
      successPopup.classList.add("show");
      setTimeout(() => successPopup.classList.remove("show"), 1000);
      setTimeout(() => doctorPopup.classList.remove("active"), 500);
    } else {
      alert(result.message || "⚠️ Registration failed.");
    }
  } catch (err) {
    console.error(err);
    alert("⚠️ Server error. Please contact support.");
  }
});

// Close success popup manually
closeSuccess?.addEventListener("click", () =>
  successPopup.classList.remove("show")
);
