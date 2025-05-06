function moveFocus(currentInput, nextInputId) {
  // Move to the next input if the current input has a value
  if (currentInput.value.length == currentInput.maxLength) {
    document.getElementById(nextInputId)?.focus();
  }
  // Check if all OTP fields are filled
  if (allOtpFieldsFilled()) {
    // Simulate button click when all OTP fields are filled
    document.getElementById("verifyBtn").click();
  }
}

function allOtpFieldsFilled() {
  // Check if all OTP input fields have a value
  for (let i = 1; i <= 6; i++) {
    if (document.getElementById("otp" + i).value === "") {
      return false;
    }
  }
  return true;
}
