// ============================
// Doctor Registration System
// ============================

// DOM Elements
const doctorForm = document.getElementById("doctorForm");
const licenseStatus = document.getElementById("licenseStatus");
const successPopup = document.getElementById("successPopup");
const successMessage = document.getElementById("successMessage");
const doctorPopup = document.getElementById("doctorPopup");


// ============================
// 1. License Email Validation
// ============================
function validateLicense(email) {
  // Format: ABC123@gov.ac.in
  const pattern = /^[A-Z0-9]{3,}@gov\.ac\.in$/i;
  return pattern.test(email);
}


// ============================
// 2. Capitalize Utility
// ============================
function capitalizeFirstLetter(text) {
  return text.charAt(0).toUpperCase() + text.slice(1).toLowerCase();
}


// ============================
// 3. Check if Email Exists
// ============================
async function checkEmailExists(email) {
  try {
    const res = await fetch(`/doctors/check-email?email=${encodeURIComponent(email)}`);
    const data = await res.json();
    return data.exists === true;
  } catch (err) {
    console.error("Email check error:", err);
    return false;
  }
}


// ============================
// 4. Check if Phone Exists
// ============================
async function checkPhoneExists(phone) {
  try {
    const res = await fetch(`/doctors/check-phone?phone=${encodeURIComponent(phone)}`);
    const data = await res.json();
    return data.exists === true;
  } catch (err) {
    console.error("Phone check error:", err);
    return false;
  }
}


// ============================
// 5. Show Success Popup
// ============================
function showSuccess(message) {
  successMessage.innerHTML = message;
  successPopup.classList.add("show");

  // Hide popup smoothly
  setTimeout(() => {
    successPopup.classList.remove("show");
  }, 3500);
}


// ============================
// 6. Handle Form Submit
// ============================
doctorForm?.addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = new FormData(doctorForm);

  // Capitalize location
  if (formData.has("location")) {
    formData.set("location", capitalizeFirstLetter(formData.get("location")));
  }

  const email = formData.get("email");
  const phone = formData.get("phone");

  // Validate License Format
  if (!validateLicense(formData.get("license"))) {
    alert("⚠️ Invalid Govt License (Format: ABC123@gov.ac.in)");
    return;
  }

  // Validate Experience
  const experience = formData.get("experience");
  if (isNaN(experience) || experience < 0) {
    alert("⚠️ Experience must be a positive number");
    return;
  }

  // Validate Phone
  if (!/^\+?\d{10,15}$/.test(phone)) {
    alert("⚠️ Invalid phone number (10–15 digits allowed)");
    return;
  }

  // Check Phone in Backend
  if (await checkPhoneExists(phone)) {
    alert("⚠️ Phone already registered!");
    return;
  }

  // === Submit to Backend ===
  try {
    const response = await fetch("/doctors/register", {
      method: "POST",
      body: formData,
    });

    const result = await response.json();

    if (result.success) {
      doctorForm.reset();
      licenseStatus.textContent = "";

      showSuccess("✅ Doctor Registered Successfully!");
      setTimeout(() => {
        doctorPopup.classList.remove("active");
      }, 800);

    } else {
      alert(result.message || "⚠️ Registration failed.");
    }

  } catch (err) {
    console.error(err);
    alert("⚠️ Server error — try again later.");
  }
});


// ============================
// 7. License Input Live Check
// ============================
const licenseInput = document.getElementById("licenseInput");

licenseInput?.addEventListener("input", () => {
  const val = licenseInput.value.trim();
  const spinner = document.getElementById("licenseSpinner");

  licenseStatus.textContent = "";
  
  if (!val) {
    spinner.style.display = "none";
    return;
  }

  // Show spinner while validating
  spinner.style.display = "inline-block";

  setTimeout(() => {
    spinner.style.display = "none";

    if (validateLicense(val)) {
      licenseStatus.textContent = "✔ Valid License";
      licenseStatus.className = "valid-check";
    } else {
      licenseStatus.textContent = "✖ Invalid Format";
      licenseStatus.className = "invalid-check";
    }

  }, 800); // delay for realistic UX
});
