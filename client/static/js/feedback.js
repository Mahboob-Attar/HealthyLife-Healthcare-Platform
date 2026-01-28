const userBtn = document.getElementById("userBtn");
const feedbackPopup = document.getElementById("feedbackPopup");
const closeFeedback = document.getElementById("closeFeedback");
const thankYouPopup = document.getElementById("thankYouPopup");
const closeThankYou = document.getElementById("closeThankYou");
const feedbackForm = document.getElementById("feedbackForm");

const stars = document.querySelectorAll(".star");
const reviewInput = document.getElementById("review");
const charCount = document.getElementById("charCount");

let selectedRating = 0;
const MAX_CHARS = 60;

/* OPEN FEEDBACK POPUP */
userBtn?.addEventListener("click", () => {
  togglePopup(feedbackPopup, true);
});

/* CLOSE POPUPS */
closeFeedback?.addEventListener("click", () => {
  togglePopup(feedbackPopup, false);
});

closeThankYou?.addEventListener("click", () => {
  togglePopup(thankYouPopup, false);
});

/* CLICK OUTSIDE TO CLOSE */
window.addEventListener("click", (e) => {
  if (e.target === feedbackPopup) togglePopup(feedbackPopup, false);
  if (e.target === thankYouPopup) togglePopup(thankYouPopup, false);
});

/* STAR RATING */
stars.forEach((star, index) => {
  star.addEventListener("mouseover", () => highlightStars(index));
  star.addEventListener("mouseout", resetStars);
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

/* CHARACTER COUNTER */
reviewInput?.addEventListener("input", () => {
  const length = reviewInput.value.length;

  if (length > MAX_CHARS) {
    reviewInput.value = reviewInput.value.slice(0, MAX_CHARS);
  }

  if (charCount) {
    charCount.textContent = `${reviewInput.value.length} / ${MAX_CHARS}`;
  }
});

/* SUBMIT FEEDBACK */
feedbackForm?.addEventListener("submit", async (e) => {
  e.preventDefault();

  const review = reviewInput.value.trim();

  if (!selectedRating) {
    alert("Please select a rating");
    return;
  }

  if (!review) {
    alert("Please write your feedback");
    return;
  }

  try {
    const response = await fetch("/feedback/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        rating: selectedRating,
        review: review
      })
    });

    const result = await response.json();

    if (result.success) {
      resetForm();
      togglePopup(feedbackPopup, false);
      togglePopup(thankYouPopup, true);

      setTimeout(() => togglePopup(thankYouPopup, false), 6000);
    } else {
      alert(result.message || "Failed to submit feedback");
    }
  } catch (err) {
    console.error(err);
    alert("Server error. Please try again later.");
  }
});

/* HELPERS */
function togglePopup(el, show = true) {
  el.style.display = show ? "flex" : "none";
}

function resetForm() {
  feedbackForm.reset();
  selectedRating = 0;
  stars.forEach((star) => star.classList.remove("selected"));
  if (charCount) charCount.textContent = `0 / ${MAX_CHARS}`;
}
