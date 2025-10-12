// Toggle only the clicked doctor's details
function toggleDetails(id) {
  const details = document.getElementById("details-" + id);
  if (!details) return;

  // Optional: Close all other open doctor details
  const allDetails = document.querySelectorAll(".doctor-details");
  allDetails.forEach((d) => {
    if (d !== details) {
      d.style.display = "none";
    }
  });

  // Toggle this doctor's details
  details.style.display = details.style.display === "block" ? "none" : "block";
}

// Filter doctors by city from dropdown
function filterByCity() {
  const city = document.getElementById("cityDropdown").value;
  if (city) {
    window.location.href = "/appointment?city=" + encodeURIComponent(city);
  } else {
    window.location.href = "/appointment";
  }
}
