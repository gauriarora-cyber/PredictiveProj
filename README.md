# PredictiveProj
# Wine Quality Prediction Using Machine Learning

Predicting the quality of red wine from its physicochemical properties
using Linear Regression and Logistic Regression (Python, scikit-learn).

## Problem statement
Predict wine quality from measurements such as acidity, sugar, pH,
alcohol content and sulphates.

## Research objective
Determine how well chemical measurements can predict a wine's quality
score, and whether a classifier can distinguish lower-quality wines
from higher-quality ones.

## Dataset
UCI Wine Quality (red): 1,599 samples, 11 features, quality score 3-8.
After removing 240 duplicate rows, 1,359 samples remain.

## Method
1. Load and clean data (no missing values; duplicates removed)
2. Targets: quality score (regression); quality >= 7 = "high" (classification)
3. 80/20 train-test split (stratified for classification), StandardScaler
4. Linear Regression -> numeric quality score
5. Logistic Regression -> high / lower quality
6. Evaluation plots and a prediction function for new wine samples

## Results (test set, random_state=42)
| Model | Metric | Value |
|---|---|---|
| Linear Regression | RMSE | 0.657 |
| Linear Regression | R² | 0.39 |
| Logistic Regression | Accuracy | 0.875 |
| Logistic Regression | Precision / Recall / F1 (high quality) | 0.60 / 0.24 / 0.35 |

Note: always predicting "lower quality" gives 86.4% accuracy, so accuracy
alone is misleading here. Recall for high-quality wines is low because only
about 13.5% of wines are high quality.

Alcohol is the strongest predictor in both models, followed by volatile
acidity and sulphates.

## How to run
pip install -r requirements.txt
python main.py
