// static/js/add_listing.js
document.addEventListener('DOMContentLoaded', () => {
  const imageInput = document.getElementById('imageInput');
  const preview = document.getElementById('preview');

  if (imageInput) {
    imageInput.addEventListener('change', (e) => {
      const file = e.target.files[0];
      if (!file) {
        preview.src = '/static/assets/default_crop.jpg';
        return;
      }
      if (file.size > 3 * 1024 * 1024) { // 3MB
        alert('Image too large (max 3MB). Please choose smaller image.');
        imageInput.value = '';
        preview.src = '/static/assets/default_crop.jpg';
        return;
      }
      const reader = new FileReader();
      reader.onload = (ev) => preview.src = ev.target.result;
      reader.readAsDataURL(file);
    });
  }
});
