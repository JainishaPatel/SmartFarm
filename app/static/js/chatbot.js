document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("chat-form");
  const chatBox = document.getElementById("chat-box");
  const input = document.getElementById("prompt");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    let userMessage = input.value.trim();
    if (!userMessage) return;

    // Show user message
    chatBox.innerHTML += `<div class="chat-message user"><strong>You:</strong> ${userMessage}</div>`;
    chatBox.scrollTop = chatBox.scrollHeight;

    // Clear input
    input.value = "";

    try {
      let formData = new FormData(form);
      let response = await fetch(form.action, {
        method: "POST",
        body: formData,
        headers: { "X-Requested-With": "XMLHttpRequest" }
      });

      let data = await response.json();

      // Show bot reply
      chatBox.innerHTML += `<div class="chat-message bot"><strong>Bot:</strong> ${data.reply}</div>`;
      chatBox.scrollTop = chatBox.scrollHeight;
    } catch (err) {
      chatBox.innerHTML += `<div class="chat-message bot"><strong>Bot:</strong> ⚠️ Error connecting to server</div>`;
    }
  });
});
