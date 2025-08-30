document.addEventListener("DOMContentLoaded", function () {
  const contactButtons = document.querySelectorAll(".contact-btn");

  contactButtons.forEach(button => {
    button.addEventListener("click", function () {
      document.getElementById("sellerName").innerText = this.dataset.name;
      document.getElementById("sellerEmail").innerText = this.dataset.email;
      document.getElementById("sellerPhone").innerText = this.dataset.phone;

      const modal = new bootstrap.Modal(document.getElementById("contactModal"));
      modal.show();
    });
  });

  // Form validation
  const form = document.querySelector("form");
  form.addEventListener("submit", function (e) {
    const name = form.querySelector("input[name='name']").value.trim();
    const price = form.querySelector("input[name='price']").value.trim();
    const sellerName = form.querySelector("input[name='seller_name']").value.trim();
    const sellerPhone = form.querySelector("input[name='seller_phone']").value.trim();

    if (!name || !price || !sellerName || !sellerPhone) {
      alert("Please fill all required fields correctly.");
      e.preventDefault();
    }
  });
});
