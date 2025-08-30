function checkSoilType(event) {
  event.preventDefault();
  const texture = document.getElementById('texture').value;
  const resultDiv = document.getElementById('soilResult');

  let message = '';
  switch (texture) {
    case 'sandy':
      message = '⚠️ Sandy soil drains quickly. Add organic matter and water more often.';
      break;
    case 'clay':
      message = '💧 Clay soil holds water well. Improve drainage and aeration for better growth.';
      break;
    case 'loamy':
      message = '✅ Loamy soil is ideal for most crops. Maintain with compost and regular rotation.';
      break;
    case 'silty':
      message = '🌱 Silty soil retains moisture. Avoid waterlogging and improve drainage.';
      break;
    default:
      message = 'Select a valid soil type.';
  }

  resultDiv.classList.remove('d-none');
  resultDiv.innerText = message;
}
