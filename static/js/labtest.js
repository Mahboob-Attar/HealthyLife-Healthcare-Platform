const labtestForm = document.getElementById("labtestForm");
const labtestResult = document.getElementById("labtestResult");
const testList = document.getElementById("testList");

labtestForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const disease = document.getElementById("disease").value.trim();
  const age = document.getElementById("age").value;

  if (!disease || !age) return;

  try {
    const res = await fetch("/labtest_recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ disease, age }),
    });

    const data = await res.json();
    testList.innerHTML = "";

    if (data.tests && data.tests.length > 0) {
      data.tests.forEach((test) => {
        const li = document.createElement("li");
        li.textContent = test;
        testList.appendChild(li);
      });
    } else {
      testList.innerHTML = "<li>No lab tests found.</li>";
    }
    // Hide result initially
    labtestResult.style.display = "block";
  } catch (err) {
    testList.innerHTML = "<li>Error fetching lab tests.</li>";
    labtestResult.style.display = "block";
  }
});
