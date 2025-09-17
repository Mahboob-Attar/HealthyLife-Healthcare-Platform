// Elements
const doctorBtn = document.getElementById("doctorBtn");
const doctorPopup = document.getElementById("doctorPopup");
const closeDoctor = document.getElementById("closeDoctor");
const doctorForm = document.getElementById("doctorForm");

const successPopup = document.getElementById("successPopup");
const closeSuccess = document.getElementById("closeSuccess");
const successMessage = document.getElementById("successMessage");

// Open/Close Doctor Popup
doctorBtn?.addEventListener("click", () => doctorPopup.classList.add("active"));
closeDoctor?.addEventListener("click", () =>
  doctorPopup.classList.remove("active")
);

// Handle Doctor Form Submission
doctorForm?.addEventListener("submit", async (e) => {
  e.preventDefault();

  // Use FormData (supports text + files)
  const formData = new FormData(doctorForm);

  try {
    const response = await fetch("/register_doctor", {
      method: "POST",
      body: formData, // send as multipart/form-data
    });

    const result = await response.json();

    if (result.success) {
      doctorForm.reset();
      doctorPopup.classList.remove("active");
      successMessage.innerHTML =
        "✅ Successfully Registered! <br> If you need help or any changes, please visit the Support page.";
      successPopup.classList.add("active");
    } else {
      alert(result.message || "⚠️ Registration failed. Please try again.");
    }
  } catch (err) {
    console.error(err);
    alert("⚠️ Server error. Please contact support.");
  }
});

// Close Success Popup
closeSuccess?.addEventListener("click", () =>
  successPopup.classList.remove("active")
);
