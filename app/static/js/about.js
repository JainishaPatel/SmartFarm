// about.js

document.addEventListener("DOMContentLoaded", () => {
  // Animate cards on scroll
  const aboutBoxes = document.querySelectorAll(".about-box");

  const observer = new IntersectionObserver(
    entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("fade-in-up");
          observer.unobserve(entry.target);
        }
      });
    },
    {
      threshold: 0.1,
    }
  );

  aboutBoxes.forEach(box => {
    observer.observe(box);
  });

  // Optional hover effect (adds pulse effect)
  aboutBoxes.forEach(box => {
    box.addEventListener("mouseenter", () => {
      box.classList.add("hover-glow");
    });
    box.addEventListener("mouseleave", () => {
      box.classList.remove("hover-glow");
    });
  });
});
