const form = document.getElementById("prediction-form");
const defaults = {
  "fixed acidity": "7.4", "volatile acidity": "0.35", "citric acid": "0.45",
  "residual sugar": "2.0", "chlorides": "0.065", "free sulfur dioxide": "15",
  "total sulfur dioxide": "38", "density": "0.9950", "pH": "3.35",
  "sulphates": "0.75", "alcohol": "12.0"
};

document.getElementById("reset-btn").addEventListener("click", () => {
  Object.entries(defaults).forEach(([name, value]) => {
    form.elements.namedItem(name).value = value;
  });
  document.getElementById("empty-result").classList.remove("hidden");
  document.getElementById("prediction-result").classList.add("hidden");
  document.getElementById("error-message").classList.add("hidden");
  document.getElementById("result-status").textContent = "AWAITING INPUT";
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const button = form.querySelector("button[type='submit']");
  const originalText = button.innerHTML;
  button.disabled = true;
  button.innerHTML = "Analysing sample…";
  document.getElementById("error-message").classList.add("hidden");

  const data = {};
  [...form.querySelectorAll("input")].forEach(input => data[input.name] = Number(input.value));

  try {
    const response = await fetch("/api/predict", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(data)
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || "Prediction could not be completed.");

    document.getElementById("empty-result").classList.add("hidden");
    document.getElementById("prediction-result").classList.remove("hidden");
    document.getElementById("result-status").textContent = "PREDICTION COMPLETE";
    document.getElementById("score-number").innerHTML = `${result.predicted_score}<small> / 8</small>`;
    document.getElementById("score-ring-value").textContent = result.predicted_score;
    document.getElementById("score-ring").style.background =
      `conic-gradient(#bd7b89 ${Math.min(result.predicted_score / 8 * 100, 100)}%, #493b3c 0)`;
    document.getElementById("category-result").textContent = result.predicted_category;
    document.getElementById("category-icon").textContent = result.class_prediction ? "✦" : "◇";
    document.getElementById("probability-value").textContent = `${result.high_quality_probability}%`;
    document.getElementById("probability-bar").style.width = `${result.high_quality_probability}%`;
  } catch (error) {
    const box = document.getElementById("error-message");
    box.textContent = error.message;
    box.classList.remove("hidden");
  } finally {
    button.disabled = false;
    button.innerHTML = originalText;
  }
});
