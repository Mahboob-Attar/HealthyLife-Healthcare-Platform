const doctorBtn = document.getElementById("doctorBtn");
const doctorPopup = document.getElementById("doctorPopup");
const closeDoctor = document.getElementById("closeDoctor");
const doctorForm = document.getElementById("doctorForm");
const successPopup = document.getElementById("successPopup");
const closeSuccess = document.getElementById("closeSuccess");
const successMessage = document.getElementById("successMessage");

const licenseInput = document.getElementById("licenseInput");
const licenseStatus = document.getElementById("licenseStatus");

doctorBtn?.addEventListener("click", () => doctorPopup.classList.add("active"));
closeDoctor?.addEventListener("click", () =>
  doctorPopup.classList.remove("active")
);

// Capitalize helper
function capitalizeFirstLetter(str) {
  if (!str) return "";
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}

// Govt license validation
function validateLicense(email) {
  const licenseRegex = /^[A-Z]{3}[0-9]{3}@gov\.ac\.in$/;
  return licenseRegex.test(email);
}

// Live license check
licenseInput?.addEventListener("input", () => {
  const value = licenseInput.value.trim();
  licenseStatus.textContent = "";

  if (!value) return;

  licenseStatus.innerHTML = '<span class="spinner"></span> Verifying...';
  licenseStatus.style.color = "orange";

  setTimeout(() => {
    if (validateLicense(value)) {
      licenseStatus.textContent = "✔ Verified";
      licenseStatus.style.color = "green";
    } else {
      licenseStatus.textContent = "✖ Invalid";
      licenseStatus.style.color = "red";
    }
  }, 2500);
});

// =======================
// FORM SUBMIT (FIXED URL)
// =======================
doctorForm?.addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = new FormData(doctorForm);

  if (formData.has("location")) {
    formData.set(
      "location",
      capitalizeFirstLetter(formData.get("location"))
    );
  }

  if (!validateLicense(formData.get("license"))) {
    alert("⚠️ Invalid Govt License Email.");
    return;
  }

  const experience = formData.get("experience");
  const phone = formData.get("phone");

  if (isNaN(experience) || experience < 0) {
    alert("⚠️ Invalid experience");
    return;
  }

  if (!/^\+?\d{10,15}$/.test(phone)) {
    alert("⚠️ Invalid phone number");
    return;
  }

  try {
    const response = await fetch("/doctors/register", {   // ✅ FIX HERE
      method: "POST",
      body: formData,
    });

    const result = await response.json();

    if (result.success) {
      doctorForm.reset();
      licenseStatus.textContent = "";
      successMessage.innerHTML =
        "✅ Request sent successfully! Our team will verify your details for more update Active in your Inbox.";
      successPopup.classList.add("show");

      setTimeout(() => successPopup.classList.remove("show"), 7000);
      setTimeout(() => doctorPopup.classList.remove("active"), 500);
    } else {
      alert(result.message || "⚠️ Registration failed.");
    }
  } catch (err) {
    console.error("Doctor Register Error:", err);
    alert("⚠️ Server error. Please try again.");
  }
});

closeSuccess?.addEventListener("click", () =>
  successPopup.classList.remove("show")
);
