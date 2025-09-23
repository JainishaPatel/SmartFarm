// Product type lists
const productTypes = {
  "Seeds": [
    "Wheat", "Rice", "Maize", "Cotton", "Soybean", "Groundnut", 
    "Mustard", "Sugarcane", "Vegetable Seeds", "Fruit Seeds", "Pulses"
  ],
  "Fertilizers": [
    "Urea", "DAP", "MOP (Potash)", "NPK", "Super Phosphate",
    "Compost", "Vermicompost", "Bio-fertilizers", "Micronutrients"
  ],
  "Pesticides": [
    "Insecticides", "Fungicides", "Herbicides", "Weedicides",
    "Bio-pesticides", "Neem-based", "Plant Growth Regulators"
  ]
};

$(document).ready(function () {
  // Initialize searchable dropdown
  $('#typeSelect').select2({
    placeholder: "Select a type...",
    width: '100%'
  });

  // Update types based on category
  $('#categorySelect').on('change', function () {
    const category = $(this).val();
    const types = productTypes[category] || [];

    $('#typeSelect').empty().append('<option></option>');
    types.forEach(t => {
      $('#typeSelect').append(new Option(t, t));
    });

    $('#typeSelect').trigger('change'); // refresh Select2
  });
});
