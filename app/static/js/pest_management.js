document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.getElementById("pestSearch");
  const pestCards = document.querySelectorAll(".pest-card-container");
  const noResults = document.getElementById("noResults");

  searchInput.addEventListener("input", () => {
    const searchTerm = searchInput.value.trim().toLowerCase();
    let matchFound = false;

    pestCards.forEach(card => {
      const pestName = card.getAttribute("data-name");
      if (pestName.includes(searchTerm)) {
        card.style.display = "block";
        matchFound = true;
      } else {
        card.style.display = "none";
      }
    });

    noResults.style.display = matchFound ? "none" : "block";
  });
});
