let selected = null;

function selectPayment(element) {
  document.querySelectorAll(".payment-card").forEach((card) => {
    card.classList.remove("active");
  });
  element.classList.add("active");
  selected = element.querySelector("span").textContent;
}

function submitPayment() {
  if (selected) {
    alert(`You selected ${selected} as your payment method.`);
  } else {
    alert("Please select a payment method.");
  }
}
