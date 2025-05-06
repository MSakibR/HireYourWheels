document.addEventListener("DOMContentLoaded", function () {
  const chooseButtons = document.querySelectorAll(".choose-button");
  const hostContainer = document.querySelector(".host-container");

  chooseButtons.forEach((button) => {
    button.addEventListener("click", () => {
      hostContainer.style.display = "block"; // Show the form when clicked
      window.scrollTo({
        top: hostContainer.offsetTop,
        behavior: "smooth",
      });
    });
  });
});
