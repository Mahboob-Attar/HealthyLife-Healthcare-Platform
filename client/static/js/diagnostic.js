const form = document.getElementById("predictForm");
const resultBox = document.getElementById("result");
const predictionText = document.getElementById("prediction");
const descriptionText = document.getElementById("description");
const precautionsList = document.getElementById("precautions");
const medicationsList = document.getElementById("medications");
const dietsList = document.getElementById("diets");
const workoutsList = document.getElementById("workouts");
// Hide result box initially
resultBox.style.display = "none";
// Helper function to populate UL lists
const populateList = (ul, items) => {
  ul.innerHTML = "";
  if (!items || items.length === 0) {
    ul.innerHTML = "<li>N/A</li>";
  } else {
    items.forEach((i) => {
      const li = document.createElement("li");
      li.textContent = i;
      ul.appendChild(li);
    });
  }
};
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const symptomsInput = document.getElementById("symptoms").value.trim();
  if (!symptomsInput) return; // Normalize input into array
  const symptomsArray = symptomsInput
    .split(",")
    .map((s) => s.trim().toLowerCase())
    .filter((s) => s.length > 0);
  try {
    const res = await fetch("/diagnostic/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ symptoms: symptomsArray }),
    });
    const data = await res.json();
    if (data.status === "success") {
      predictionText.textContent = data.prediction || "N/A";
      descriptionText.textContent = data.description || "N/A";
      populateList(precautionsList, data.precautions);
      populateList(medicationsList, data.medications);
      populateList(dietsList, data.diets);
      populateList(workoutsList, data.workouts);
    } else {
      predictionText.textContent =
        "Error: " + (data.message || "Unknown error");
      descriptionText.textContent = "";
      precautionsList.innerHTML = "";
      medicationsList.innerHTML = "";
      dietsList.innerHTML = "";
      workoutsList.innerHTML = "";
    }
    resultBox.style.display = "block";
    resultBox.classList.add("show");
  } catch (err) {
    predictionText.textContent = "Error contacting prediction service.";
    descriptionText.textContent = "";
    precautionsList.innerHTML = "";
    medicationsList.innerHTML = "";
    dietsList.innerHTML = "";
    workoutsList.innerHTML = "";
    resultBox.style.display = "block";
  }
});
