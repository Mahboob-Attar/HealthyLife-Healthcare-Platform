document.addEventListener("DOMContentLoaded", async () => {
  try {
    //
    // ================= 1 Fetch Doctor Stats =================
    //
    const res = await fetch("/admin/dashboard/data");
    const result = await res.json();

    if (!result.success) {
      console.error("Dashboard Data Error:", result.message);
      return;
    }

    const data = result.data;

    // Update Total Doctors
    const totalDocEl = document.getElementById("totalDoctors");
    if (totalDocEl) totalDocEl.textContent = data.total_doctors || 0;

    // Render Specialization Doughnut Chart
    const specCanvas = document.getElementById("specializationChart");
    if (specCanvas && data.specializations.length > 0) {
      new Chart(specCanvas.getContext("2d"), {
        type: "doughnut",
        data: {
          labels: data.specializations.map(s => s.specialization),
          datasets: [{
            data: data.specializations.map(s => s.count),
            backgroundColor: [
              "#1da1f2", "#00ffcc", "#ff6384",
              "#ff9f40", "#36a2eb", "#9966ff"
            ]
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: { position: "bottom" }
          }
        }
      });
    }

    // ================= 2️ Fetch Feedback Ratings =================
   
    const feedbackRes = await fetch("/admin/dashboard/ratings");
    const feedbackResult = await feedbackRes.json();

    if (!feedbackResult.success) {
      console.error("Feedback Ratings Error:", feedbackResult.message);
      return;
    }

    const ratingsData = feedbackResult.data.feedback_ratings || {};
    const feedbackCanvas = document.getElementById("feedbackChart");

    const ratingCounts = ["1", "2", "3", "4", "5"].map(
      r => ratingsData[r] || 0
    );

    const totalRatings = ratingCounts.reduce((sum, v) => sum + v, 0);

    // Update Total Ratings Text
    const totalRatingText = document.getElementById("totalRatingsText");
    if (totalRatingText) {
      totalRatingText.textContent = `Total Ratings: ${totalRatings}`;
    }

    // Render Ratings Bar Chart ONLY if data exists
    if (feedbackCanvas && totalRatings > 0) {
      new Chart(feedbackCanvas.getContext("2d"), {
        type: "bar",
        data: {
          labels: ["1 ★", "2 ★", "3 ★", "4 ★", "5 ★"],
          datasets: [{
          label: "Users",
          data: ratingCounts,
          backgroundColor: [
            "rgba(255,77,79,0.9)",
            "rgba(255,136,56,0.9)",
            "rgba(255,219,50,0.9)",
            "rgba(110,207,57,0.9)",
            "rgba(54,207,201,0.95)"
          ],
          borderWidth: 0,
          barPercentage: 0.4,
          categoryPercentage: 0.6
        }]
        },
        options: {
          responsive: true,
          plugins: { legend: { display: false } },
          scales: {
            y: {
              beginAtZero: true,
              display: false,
              grid: { display: false }
            },
            x: {
              grid: { display: false },
              ticks: { color: "#b1c7ff" }
            }
          }
        }
      });
    }

  } catch (err) {
    console.error("Dashboard JS Fatal Error:", err);
  }
});
