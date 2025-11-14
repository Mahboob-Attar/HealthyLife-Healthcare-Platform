document.addEventListener("DOMContentLoaded", async () => {
  try {
    const res = await fetch("/dashboard/data"); // ✅ FIXED URL
    const result = await res.json();

    if (!result.success) {
      console.error("Backend Error:", result.message);
      return;
    }

    const data = result.data;

    // Total Doctors
    document.getElementById("totalDoctors").textContent =
      data.total_doctors || 0;

    // Total Users
    document.getElementById("totalUsers").textContent =
      data.total_users || 0;

    // Specialization Chart
    const specCanvas = document.getElementById("specializationChart");
    if (specCanvas) {
      new Chart(specCanvas.getContext("2d"), {
        type: "doughnut",
        data: {
          labels: data.specializations.map((s) => s.specialization),
          datasets: [
            {
              data: data.specializations.map((s) => s.count),
              backgroundColor: [
                "#1da1f2",
                "#00ffcc",
                "#ff6384",
                "#ff9f40",
                "#36a2eb",
                "#9966ff",
              ],
            },
          ],
        },
        options: {
          responsive: true,
          plugins: { legend: { position: "bottom" } },
        },
      });
    }

    // ML Accuracy Chart
    const mlCanvas = document.getElementById("mlAccuracyChart");
    if (mlCanvas) {
      new Chart(mlCanvas.getContext("2d"), {
        type: "bar",
        data: {
          labels: Object.keys(data.ml_accuracy),
          datasets: [
            {
              label: "Accuracy (%)",
              data: Object.values(data.ml_accuracy),
              backgroundColor: "#ffcd56",
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            y: { beginAtZero: true, max: 100 },
          },
        },
      });
    }
  } catch (err) {
    console.error("Dashboard JS Error:", err);
  }
});
