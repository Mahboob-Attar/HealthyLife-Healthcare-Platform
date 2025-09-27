document.addEventListener("DOMContentLoaded", async () => {
  try {
    const res = await fetch("/dashboard/dashboard_data");
    const result = await res.json();

    if (!result.success) return;

    const data = result.data;

    // Total Doctors
    const totalDoctors = data.total_doctors || 0;
    document.getElementById("totalDoctors").textContent = totalDoctors;

    // Total Users
    const totalUsers = data.total_users || 0;
    document.getElementById("totalUsers").textContent = totalUsers;

    // Doctor Specializations Chart
    const specCanvas = document.getElementById("specializationChart");
    if (specCanvas) {
      const specCtx = specCanvas.getContext("2d");
      new Chart(specCtx, {
        type: "doughnut",
        data: {
          labels: data.specializations.map((s) => s.specialization),
          datasets: [
            {
              label: "Specializations",
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
    const mlCtx = document.getElementById("mlAccuracyChart")?.getContext("2d");
    if (mlCtx) {
      new Chart(mlCtx, {
        type: "bar",
        data: {
          labels: Object.keys(data.ml_accuracy),
          datasets: [
            {
              label: "Accuracy %",
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
    console.error("Dashboard JS error:", err);
  }
});
