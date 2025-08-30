// contact.js

document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("#contactForm");

  if (!form) return;

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    const name = document.querySelector("#name");
    const email = document.querySelector("#email");
    const message = document.querySelector("#message");

    let isValid = true;

    // Name validation
    if (!name.value.trim()) {
      showError("name");
      isValid = false;
    } else {
      hideError("name");
    }

    // Email validation (basic pattern check)
    const emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;
    if (!email.value.trim() || !emailPattern.test(email.value)) {
      showError("email");
      isValid = false;
    } else {
      hideError("email");
    }

    // Message validation
    if (!message.value.trim()) {
      showError("message");
      isValid = false;
    } else {
      hideError("message");
    }

    if (isValid) {
      alert("Message sent successfully!");
      form.reset(); // clear form
    }
  });

  function showError(field) {
    document.querySelector(`#${field}`).classList.add("is-invalid");
    document.querySelector(`#${field}Error`).style.display = "block";
  }

  function hideError(field) {
    document.querySelector(`#${field}`).classList.remove("is-invalid");
    document.querySelector(`#${field}Error`).style.display = "none";
  }
});


// Optional: Simple toast message function
function showToast(message, type = "success") {
  const toast = document.createElement("div");
  toast.textContent = message;
  toast.className = `custom-toast ${type}`;
  document.body.appendChild(toast);

  setTimeout(() => {
    toast.classList.add("visible");
  }, 100);

  setTimeout(() => {
    toast.classList.remove("visible");
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}
