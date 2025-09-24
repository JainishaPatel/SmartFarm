// document.addEventListener("DOMContentLoaded", function () {
//   const modal = new bootstrap.Modal(document.getElementById("purchaseModal"));
//   const productSpan = document.getElementById("purchaseProduct");
//   const priceSpan = document.getElementById("purchasePrice");

//   document.querySelectorAll(".buy-btn").forEach(button => {
//     button.addEventListener("click", () => {
//       productSpan.textContent = button.dataset.name;
//       priceSpan.textContent = button.dataset.price;
//       modal.show();
//     });
//   });

//   document.getElementById("purchaseForm").addEventListener("submit", function (e) {
//     e.preventDefault();
//     alert("✅ Order placed successfully! You'll be contacted shortly.");
//     modal.hide();
//   });
// });
