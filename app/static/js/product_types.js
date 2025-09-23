// 🔍 Search filter for dropdown
const searchInput = document.getElementById("searchInput");
const select = document.getElementById("subtype");

searchInput.addEventListener("keyup", function () {
  let filter = this.value.toLowerCase();
  let options = select.options;

  for (let i = 0; i < options.length; i++) {
    let txt = options[i].text.toLowerCase();
    // skip optgroup labels
    if (options[i].parentElement.tagName === "OPTGROUP") {
      options[i].style.display = txt.includes(filter) ? "" : "none";
    }
  }
});
