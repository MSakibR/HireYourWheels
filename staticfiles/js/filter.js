// Get the filter button, overlay, and close button
const filterBtn = document.getElementById("filter-btn");
const filterOverlay = document.getElementById("filter-overlay");
const closeFilterBtn = document.getElementById("close-filter");

// Show the filter overlay when the filter button is clicked
filterBtn.addEventListener("click", () => {
  filterOverlay.style.display = "flex";
});

// Close the filter overlay when the close button is clicked
closeFilterBtn.addEventListener("click", () => {
  filterOverlay.style.display = "none";
});
