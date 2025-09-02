const pharmacyForm = document.getElementById("pharmacyForm");
const pharmacyResult = document.getElementById("pharmacyResult");
const medicineList = document.getElementById("medicineList");

pharmacyForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const disease = document.getElementById("disease").value.trim();
  const age = document.getElementById("age").value;
  const weight = document.getElementById("weight").value.trim();

  if (!disease || !age || !weight) return;

  try {
    const res = await fetch("/pharmacy_recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ disease, age, weight }),
    });

    const data = await res.json();
    medicineList.innerHTML = "";

    if (data.medicines && data.medicines.length > 0) {
      data.medicines.forEach((med) => {
        const li = document.createElement("li");
        li.textContent = med;
        medicineList.appendChild(li);
      });
    } else {
      medicineList.innerHTML = "<li>No medicines found.</li>";
    }
    // Hide result initially
    pharmacyResult.style.display = "block";
  } catch (err) {
    medicineList.innerHTML = "<li>Error fetching medicines.</li>";
    pharmacyResult.style.display = "block";
  }
});
