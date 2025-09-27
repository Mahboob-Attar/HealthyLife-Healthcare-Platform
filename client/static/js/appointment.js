function toggleDetails(id) {
  const details = document.getElementById("details-" + id);
  if (details.style.display === "block") {
    details.style.display = "none";
  } else {
    details.style.display = "block";
  }
}

// Cities passed from Flask template
const cities = JSON.parse(
  document.getElementById("citySearchData").textContent
);

function searchCity() {
  const input = document.getElementById("citySearch").value.toLowerCase();
  const suggestionsDiv = document.getElementById("suggestions");
  suggestionsDiv.innerHTML = "";

  if (input.length < 2) return; // show after 2+ characters

  const filteredCities = cities.filter((city) =>
    city.toLowerCase().includes(input)
  );

  filteredCities.forEach((city) => {
    const div = document.createElement("div");
    div.textContent = city;
    div.classList.add("suggestion-item");
    div.onclick = () => selectCity(city);
    suggestionsDiv.appendChild(div);
  });
}

function selectCity(city) {
  document.getElementById("citySearch").value = city;
  document.getElementById("suggestions").innerHTML = "";
  window.location.href = "/appointment?city=" + encodeURIComponent(city);
}
