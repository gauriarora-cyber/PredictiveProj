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

// Real samples from winequality-red.csv
const samples = {
  high: { "fixed acidity": 7.9, "volatile acidity": 0.35, "citric acid": 0.46,
    "residual sugar": 3.6, "chlorides": 0.078, "free sulfur dioxide": 15,
    "total sulfur dioxide": 37, "density": 0.9973, "pH": 3.35,
    "sulphates": 0.86, "alcohol": 12.8 },
  average: { "fixed acidity": 7.4, "volatile acidity": 0.7, "citric acid": 0,
    "residual sugar": 1.9, "chlorides": 0.076, "free sulfur dioxide": 11,
    "total sulfur dioxide": 34, "density": 0.9978, "pH": 3.51,
    "sulphates": 0.56, "alcohol": 9.4 },
  low: { "fixed acidity": 11.6, "volatile acidity": 0.58, "citric acid": 0.66,
    "residual sugar": 2.2, "chlorides": 0.074, "free sulfur dioxide": 10,
    "total sulfur dioxide": 47, "density": 1.0008, "pH": 3.25,
    "sulphates": 0.57, "alcohol": 9 }
};

document.querySelectorAll(".sample-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    Object.entries(samples[btn.dataset.sample]).forEach(([name, value]) => {
      form.elements.namedItem(name).value = value;
    });
  });
});
