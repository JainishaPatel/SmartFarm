document.addEventListener("DOMContentLoaded", () => {
  const tableBody = document.getElementById("marketTableBody");

  // Example data - replace this with API fetch if available
  const marketData = [
    { crop: "Wheat", location: "Indore, MP", min: 2150, max: 2280, modal: 2200 },
    { crop: "Rice", location: "Raipur, CG", min: 1800, max: 1950, modal: 1870 },
    { crop: "Soybean", location: "Nagpur, MH", min: 4100, max: 4400, modal: 4250 },
    { crop: "Onion", location: "Nashik, MH", min: 900, max: 1200, modal: 1100 },
    { crop: "Tomato", location: "Pune, MH", min: 600, max: 950, modal: 850 }
  ];

  marketData.forEach(item => {
    const row = `<tr>
      <td>${item.crop}</td>
      <td>${item.location}</td>
      <td>${item.min}</td>
      <td>${item.max}</td>
      <td>${item.modal}</td>
    </tr>`;
    tableBody.innerHTML += row;
  });
});
