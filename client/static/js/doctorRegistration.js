// ================== Doctor Registration FormData Script ================== //

// Elements for doctor popup
const doctorBtn = document.getElementById("doctorBtn");
const doctorPopup = document.getElementById("doctorPopup");
const closeDoctor = document.getElementById("closeDoctor");

// Open Doctor Popup
doctorBtn?.addEventListener("click", () => {
  doctorPopup.classList.add("active");
});

// Close Doctor Popup (manual close)
closeDoctor?.addEventListener("click", () => {
  doctorPopup.classList.remove("active");
});

// Elements Form Submission and Success Popup
const doctorForm = document.getElementById("doctorForm");
const successPopup = document.getElementById("successPopup");
const closeSuccess = document.getElementById("closeSuccess");
const successMessage = document.getElementById("successMessage");

// Handle Doctor Form Submission
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
        "✅ Successfully Registered! <br> If you need help or any changes, please visit the Support page.";
      successPopup.classList.add("show");

      setTimeout(() => {
        successPopup.classList.remove("show");
        successPopup.classList.add("hide");
      }, 10000);

      
      //  Auto-close Doctor Registration popup after 0.5s
      setTimeout(() => {
        doctorPopup.classList.remove("active");
      }, 500);
    } else {
      alert(result.message || "⚠️ Registration failed. Please try again.");
    }
  } catch (err) {
    console.error(err);
    alert("⚠️ Server error. Please contact support.");
  }
});

// Close Success Popup Manually
closeSuccess?.addEventListener("click", () => {
  successPopup.classList.remove("show");
});
