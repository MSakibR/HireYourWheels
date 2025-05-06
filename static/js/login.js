const container = document.getElementById("container");
const formSide = document.getElementById("formSide");
const imageSide = document.getElementById("imageSide");
const sideText = document.getElementById("sideText");
const overlay = document.getElementById("overlay");

function toggleForm(mode) {
  if (mode === "signup") {
    formSide.classList.remove("active-login");
    formSide.classList.add("active-signup");
    container.classList.add("active");
    //imageSide.querySelector('img').src = 'signup-image.jpg';
    sideText.textContent = "Join us today! Create your account.";
  } else {
    formSide.classList.remove("active-signup");
    formSide.classList.add("active-login");
    container.classList.remove("active");

    sideText.textContent = "Welcome back! Please login to your account.";
  }
}

function togglePassword(id) {
  const input = document.getElementById(id);
  if (input.type === "password") {
    input.type = "text";
  } else {
    input.type = "password";
  }
}

document.querySelectorAll(".role-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    document
      .querySelectorAll(".role-btn")
      .forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
  });
});

function toggleRole(button) {
  // Remove the 'active' class from both buttons
  const buttons = document.querySelectorAll(".role-btn");
  buttons.forEach((btn) => btn.classList.remove("active"));

  // Add the 'active' class to the clicked button
  button.classList.add("active");
}
