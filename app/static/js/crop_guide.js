async function fetchWeather(event) {
  event.preventDefault();

  const season = document.getElementById("auto_season").value;

  if (!season) {
    alert("Please select a season.");
    return;
  }

  try {
    const res = await fetch("/api/weather");  // 👈 Call your Flask route instead of external API

     if (!res.ok) {
      const errData = await res.json(); // try to parse JSON error
      throw new Error(errData.error || "Unknown API error");
    }

    const data = await res.json();

    document.getElementById("auto_temp").value = data.current.temp_c;
    document.getElementById("auto_humidity").value = data.current.humidity;
    document.getElementById("auto_rain").value = data.current.precip_mm;
    document.getElementById("auto_state").value = data.location.region || "Jammu and Kashmir";

    document.getElementById("autoForm").submit();

  } catch (err) {
    console.error("❌ JS Fetch Error:", err);
    alert("JS Fetch error: " + err.message);
  }
}
