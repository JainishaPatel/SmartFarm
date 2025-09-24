// document.addEventListener('DOMContentLoaded', function () {
//   const bookButtons = document.querySelectorAll('.book-btn');
//   const machineInput = document.getElementById('machineName');
//   const bookingForm = document.getElementById('bookingForm');

//   bookButtons.forEach(btn => {
//     btn.addEventListener('click', () => {
//       const machineName = btn.dataset.name;
//       machineInput.value = machineName;
//       const modal = new bootstrap.Modal(document.getElementById('bookingModal'));
//       modal.show();
//     });
//   });

//   bookingForm.addEventListener('submit', function (e) {
//     e.preventDefault();
//     const name = document.getElementById('farmerName').value;
//     const number = document.getElementById('contactNumber').value;
//     const machine = document.getElementById('machineName').value;

//     alert(`Booking submitted!\n\nMachine: ${machine}\nName: ${name}\nContact: ${number}`);
//     bookingForm.reset();
//     bootstrap.Modal.getInstance(document.getElementById('bookingModal')).hide();

//     // Optional: Send this data to your Flask backend via fetch() or form submission
//   });
// });
