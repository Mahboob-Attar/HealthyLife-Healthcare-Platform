function toggleDetails(button) {
  const card = button.closest(".doctor-card");
  if (!card) return;

  const details = card.querySelector(".doctor-details");
  if (!details) return;

  const modalDetails = document.getElementById("modal-details");
  modalDetails.innerHTML = details.innerHTML;

  const modal = document.getElementById("doctorModal");
  modal.style.display = "block";
}

function closeModal() {
  document.getElementById("doctorModal").style.display = "none";
}

window.onclick = function(event) {
  const modal = document.getElementById("doctorModal");
  if (event.target === modal) {
    modal.style.display = "none";
  }
}

// Filter by city -> reload page
function filterByCity() {
  const city = document.getElementById("cityDropdown").value;
  if (city) {
    window.location.href = "/appointments/?city=" + encodeURIComponent(city);
  } else {
    window.location.href = "/appointments/";
  }
}
