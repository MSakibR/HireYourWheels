const searchButtonToggle = document.getElementById("search-button-toggle");
const searchContainer = document.getElementById("search-container");
const overlay = document.getElementById("overlay");
const searchForm = document.getElementById("search-form");

// Toggle Search Form
searchButtonToggle.addEventListener("click", () => {
  searchContainer.classList.toggle("show");
  overlay.classList.toggle("show");

  // Focus on first input field
  if (searchContainer.classList.contains("show")) {
    const firstInput = searchContainer.querySelector("input, select");
    if (firstInput) {
      firstInput.focus();
    }
  }
});

// Close Search Form when Overlay is Clicked
overlay.addEventListener("click", () => {
  searchContainer.classList.remove("show");
  overlay.classList.remove("show");
});

// Handle Search Form Submission
searchForm.addEventListener("submit", (event) => {
  event.preventDefault(); // Prevent default form submission
  console.log("Search submitted!");
});

document.addEventListener("DOMContentLoaded", function () {
  const filterButton = document.querySelector(".filter-button");
  const filterContainer = document.querySelector(".filter-container");
  const filterOverlay = document.querySelector(".filter-overlay");

  filterButton.addEventListener("click", function () {
    filterContainer.classList.toggle("show");
    filterOverlay.classList.toggle("show");
  });

  filterOverlay.addEventListener("click", function () {
    filterContainer.classList.remove("show");
    filterOverlay.classList.remove("show");
  });
});

let activeForm = null; // Keep track of the currently active date form

function showDateForm(button) {
  // Find the car card container that this button belongs to
  const carCard = button.closest(".car-card");

  // If there's an active form, hide it and reset the car card details
  if (activeForm && activeForm !== carCard) {
    // Reset the previous active form
    activeForm
      .querySelector(".car-details")
      .querySelectorAll("p")
      .forEach((p) => (p.style.display = "block"));
    activeForm.querySelector(".car-details").querySelector("h3").style.display =
      "block";
    activeForm.querySelector(".rent-button").style.display = "block";

    activeForm.querySelector(".date-form-container").style.display = "none";
  }

  // Now show the date form for the current car card
  const carDetails = carCard.querySelector(".car-details");
  carDetails.querySelectorAll("p").forEach((p) => (p.style.display = "none"));
  carDetails.querySelector("h3").style.display = "none";

  // Hide the "Rent Now" button
  button.style.display = "none";

  // Show the date form
  const dateFormContainer = carCard.querySelector(".date-form-container");
  dateFormContainer.style.display = "block";

  // Set the current car card as the active one
  activeForm = carCard;

  // Add event listener for Confirm button
  const confirmButton = dateFormContainer.querySelector(".confirm-button");
  confirmButton.addEventListener("click", function () {
    // Redirect to another page after confirmation
    window.location.href = "../Full Page/demo.html"; // Replace with your actual page URL
  });
}

function cancelForm(button) {
  // Find the car card container that this button belongs to
  const carCard = button.closest(".car-card");

  // Reset and hide the date form, restore the car details and rent button
  const carDetails = carCard.querySelector(".car-details");
  carDetails.querySelectorAll("p").forEach((p) => (p.style.display = "block"));
  carDetails.querySelector("h3").style.display = "block";

  // Show the "Rent Now" button again
  carCard.querySelector(".rent-button").style.display = "block";

  // Hide the date form container
  carCard.querySelector(".date-form-container").style.display = "none";

  // Reset the active form tracking
  activeForm = null;
}
