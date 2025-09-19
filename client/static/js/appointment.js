function toggleDetails(id) {
  const details = document.getElementById("details-" + id);
  if (details.style.display === "block") {
    details.style.display = "none";
  } else {
    details.style.display = "block";
  }
}

function filterByCity() {
  const city = document.getElementById("cityFilter").value;
  window.location.href = "/appointment?city=" + city;
}
