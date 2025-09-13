const form = document.getElementById("predictForm");
const resultBox = document.getElementById("result");
const predictionText = document.getElementById("prediction");

// Hide result initially
resultBox.style.display = "none";

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  // Get symptoms as comma-separated input and convert to array
  const symptomsInput = document.getElementById("symptoms").value.trim();
  if (!symptomsInput) return;

  const symptomsArray = symptomsInput.split(",").map(s => s.trim());

  try {
    const res = await fetch("/diagnostics/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ symptoms: symptomsArray }),
    });

    const data = await res.json();
    const disease = data?.prediction || "Unable to predict.";

    predictionText.textContent = disease;
    resultBox.style.display = "block";
  } catch (err) {
    predictionText.textContent = "Error contacting prediction service.";
    resultBox.style.display = "block";
  }
});
