const userBtn = document.getElementById("userBtn");
const feedbackPopup = document.getElementById("feedbackPopup");
const closeFeedback = document.getElementById("closeFeedback");
const thankYouPopup = document.getElementById("thankYouPopup");
const closeThankYou = document.getElementById("closeThankYou");
const feedbackForm = document.getElementById("feedbackForm");

const stars = document.querySelectorAll(".star");
let selectedRating = 0;

// Open Popup
userBtn?.addEventListener("click", () => {
  togglePopup(feedbackPopup, true);
});

// Close Popup
closeFeedback?.addEventListener("click", () => {
  togglePopup(feedbackPopup, false);
});

// Close Thank You popup
closeThankYou?.addEventListener("click", () => {
  togglePopup(thankYouPopup, false);
});

// Close on background click
window.addEventListener("click", (e) => {
  if (e.target === feedbackPopup) togglePopup(feedbackPopup, false);
  if (e.target === thankYouPopup) togglePopup(thankYouPopup, false);
});

// Star Rating System
stars.forEach((star, index) => {
  star.addEventListener("mouseover", () => highlightStars(index));
  star.addEventListener("mouseout", () => resetStars());
  star.addEventListener("click", () => {
    selectedRating = index + 1;
    highlightStars(index);
  });
});

function highlightStars(index) {
  stars.forEach((star, i) => {
    star.classList.toggle("selected", i <= index);
  });
}

function resetStars() {
  stars.forEach((star, i) => {
    star.classList.toggle("selected", i < selectedRating);
  });
}

// Submit Feedback
feedbackForm?.addEventListener("submit", async (e) => {
  e.preventDefault();

  const username = document.getElementById("username").value.trim();
  const review = document.getElementById("review").value.trim();

  if (!selectedRating) {
    alert("Please select a rating!");
    return;
  }

  try {
    const response = await fetch("/feedback/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username,
        rating: selectedRating,
        review
      })
    });

    const result = await response.json().catch(() => null);

    if (result?.success) {
      resetForm();
      togglePopup(feedbackPopup, false);
      togglePopup(thankYouPopup, true);

      setTimeout(() => togglePopup(thankYouPopup, false), 2200);
    } else {
      alert(result?.message || "Error submitting feedback!");
    }

  } catch (err) {
    console.error(err);
    alert("Server error. Please try again later.");
  }
});

// Helpers
function togglePopup(el, show = true) {
  el.style.display = show ? "block" : "none";
}

function resetForm() {
  feedbackForm.reset();
  selectedRating = 0;
  stars.forEach((star) => star.classList.remove("selected"));
}
