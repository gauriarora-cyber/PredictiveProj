# Wine Quality Prediction — Original ML Project + Web Frontend

This is the original `PredictiveProj-main` project with a web frontend added.
The original machine-learning implementation in `main.py`, original dataset,
requirements, and evaluation image are retained.

## Run in VS Code (Windows)

1. Extract this ZIP.
2. Open the extracted `PredictiveProj-main` folder in VS Code.
3. Open Terminal in that folder.
4. Create and activate a virtual environment (recommended):

   ```bash
   py -m venv .venv
   .venv\Scripts\activate
   ```

5. Install the project's dependencies:

   ```bash
   pip install -r requirements.txt
   ```

6. Start the web application:

   ```bash
   python web_app.py
   ```

7. Open `http://127.0.0.1:5000` in your browser.

## How the integration works

- `main.py` remains the source of the original Linear Regression and Logistic Regression implementation.
- `web_app.py` runs the original `main.py` and reuses its trained models, scalers, evaluation metrics, feature list, and `predict_wine_sample()` function.
- The frontend in `templates/` sends the 11 measurements to Flask at `/api/predict`.
- Flask calls the original prediction function and returns its result to the page.

The first startup trains the models by executing the original `main.py`.
