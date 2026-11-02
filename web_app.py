from pathlib import Path
import os
import runpy
import matplotlib

# The original main.py creates its evaluation plot and calls plt.show().
# Use a non-interactive backend so this works when launched as a web server.
matplotlib.use("Agg")

from flask import Flask, render_template, request, jsonify

BASE_DIR = Path(__file__).resolve().parent
os.chdir(BASE_DIR)

# Execute the ORIGINAL main.py and reuse its fitted models, scalers,
# metrics, feature list and predict_wine_sample() inference function.
model_context = runpy.run_path(str(BASE_DIR / "main.py"), run_name="wine_quality_original")

predict_wine_sample = model_context["predict_wine_sample"]
feature_columns = model_context["feature_columns"]
df = model_context["df"]

metrics = {
    "rmse": round(float(model_context["rmse"]), 3),
    "r2": round(float(model_context["r2"]), 2),
    "accuracy": round(float(model_context["accuracy"]), 3),
    "precision": round(float(model_context["precision"]), 2),
    "recall": round(float(model_context["recall"]), 2),
    "f1": round(float(model_context["f1"]), 2),
    "total_rows": 1599,
    "clean_rows": int(len(df)),
    "duplicates": int(1599 - len(df)),
    "high_quality_share": round(float((df["quality"] >= 7).mean() * 100), 1),
}

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", metrics=metrics)

@app.route("/api/predict", methods=["POST"])
def predict():
    try:
        payload = request.get_json(force=True)
        sample = {feature: float(payload[feature]) for feature in feature_columns}
        result = predict_wine_sample(sample)
        return jsonify({
            "predicted_score": result["predicted_score"],
            "predicted_category": (
                "High quality" if "High Quality" in result["predicted_category"]
                else "Lower quality"
            ),
            "high_quality_probability": round(
                float(result["high_quality_probability"]) * 100, 1
            ),
            "class_prediction": 1 if "High Quality" in result["predicted_category"] else 0
        })
    except (KeyError, TypeError, ValueError) as exc:
        return jsonify({"error": f"Please provide valid numeric values for all 11 properties. ({exc})"}), 400

@app.route("/api/metrics")
def get_metrics():
    return jsonify(metrics)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    on_server = "PORT" in os.environ
    app.run(host="0.0.0.0" if on_server else "127.0.0.1", port=port, debug=not on_server)
