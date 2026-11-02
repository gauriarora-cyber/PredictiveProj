"""
Project: Wine Quality Prediction Using Linear and Logistic Regression
Subject: Predictive Modeling (CWS Submission)
Author: Student Submission
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    mean_squared_error,
    r2_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)


# ==========================================
# 1. DATA COLLECTION & INGESTION
# ==========================================
csv_path = "winequality-red.csv"

if not os.path.exists(csv_path):
    raise FileNotFoundError(
        f"Could not find '{csv_path}' in the current working directory.\n"
        "Download it from the UCI repository: "
        "https://archive.ics.uci.edu/dataset/186/wine+quality"
    )

# The UCI Wine Quality dataset is semicolon-delimited (sep=';')
df = pd.read_csv(csv_path, sep=';')

print("=" * 60)
print("1. DATASET EXPLORATION & OVERVIEW")
print("=" * 60)
print(f"Dataset shape (rows, columns): {df.shape}\n")
print("First 5 rows:")
print(df.head())
print("\nDataset Info:")
df.info()
print("\nDescriptive Statistics:")
print(df.describe())


# ==========================================
# 2. DATA PREPROCESSING & CLEANING
# ==========================================
print("\n" + "=" * 60)
print("2. DATA PREPROCESSING & CLEANING")
print("=" * 60)

# Check missing values
missing_counts = df.isnull().sum()
print(f"Missing values per feature:\n{missing_counts}")

# Deduplication
duplicate_count = df.duplicated().sum()
print(f"\nNumber of duplicate records detected: {duplicate_count}")
if duplicate_count > 0:
    df = df.drop_duplicates().reset_index(drop=True)
    print(f"Shape after removing duplicates: {df.shape}")

# Separate base features and continuous target
feature_columns = [
    'fixed acidity', 'volatile acidity', 'citric acid', 'residual sugar',
    'chlorides', 'free sulfur dioxide', 'total sulfur dioxide', 'density',
    'pH', 'sulphates', 'alcohol'
]

X = df[feature_columns]
y_reg = df['quality']

# Binary target for classification: 1 (High Quality >= 7), 0 (Low Quality < 7)
y_clf = (df['quality'] >= 7).astype(int)

print(f"\nTarget distribution (Continuous - Quality Scores):\n{y_reg.value_counts().sort_index()}")
print(f"\nTarget distribution (Binary Classification):\n{y_clf.value_counts(normalize=True).rename({0: 'Low (<7)', 1: 'High (>=7)'})}")


# ==========================================
# 3. TRAIN-TEST SPLIT & FEATURE SCALING
# ==========================================
print("\n" + "=" * 60)
print("3. TRAIN-TEST SPLIT & SCALING")
print("=" * 60)

# Split for Regression (80% train, 20% test)
X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(
    X, y_reg, test_size=0.20, random_state=42
)

# Split for Classification (Stratified to handle class imbalance: ~86% low vs ~14% high)
X_train_clf, X_test_clf, y_train_clf, y_test_clf = train_test_split(
    X, y_clf, test_size=0.20, random_state=42, stratify=y_clf
)

# Standardize features using StandardScaler
scaler_reg = StandardScaler()
X_train_reg_scaled = scaler_reg.fit_transform(X_train_reg)
X_test_reg_scaled = scaler_reg.transform(X_test_reg)

scaler_clf = StandardScaler()
X_train_clf_scaled = scaler_clf.fit_transform(X_train_clf)
X_test_clf_scaled = scaler_clf.transform(X_test_clf)

print(f"Regression train set shape: {X_train_reg_scaled.shape}, test set: {X_test_reg_scaled.shape}")
print(f"Classification train set shape: {X_train_clf_scaled.shape}, test set: {X_test_clf_scaled.shape}")


# ==========================================
# 4. MODEL 1: LINEAR REGRESSION
# ==========================================
print("\n" + "=" * 60)
print("4. LINEAR REGRESSION (NUMERICAL PREDICTION)")
print("=" * 60)

lin_reg = LinearRegression()
lin_reg.fit(X_train_reg_scaled, y_train_reg)

y_pred_reg = lin_reg.predict(X_test_reg_scaled)

mse = mean_squared_error(y_test_reg, y_pred_reg)
rmse = np.sqrt(mse)
r2 = r2_score(y_test_reg, y_pred_reg)

print(f"Mean Squared Error (MSE)      : {mse:.4f}")
print(f"Root Mean Squared Error (RMSE) : {rmse:.4f}")
print(f"R-squared (R2) Score          : {r2:.4f}")


# ==========================================
# 5. MODEL 2: LOGISTIC REGRESSION
# ==========================================
print("\n" + "=" * 60)
print("5. LOGISTIC REGRESSION (BINARY CLASSIFICATION)")
print("=" * 60)

log_reg = LogisticRegression(max_iter=1000, random_state=42)
log_reg.fit(X_train_clf_scaled, y_train_clf)

y_pred_clf = log_reg.predict(X_test_clf_scaled)

accuracy = accuracy_score(y_test_clf, y_pred_clf)
precision = precision_score(y_test_clf, y_pred_clf, zero_division=0)
recall = recall_score(y_test_clf, y_pred_clf, zero_division=0)
f1 = f1_score(y_test_clf, y_pred_clf, zero_division=0)
cm = confusion_matrix(y_test_clf, y_pred_clf)

print(f"Accuracy Score  : {accuracy:.4f}")
print(f"Precision Score : {precision:.4f}")
print(f"Recall Score    : {recall:.4f}")
print(f"F1-Score        : {f1:.4f}\n")
print("Classification Report:")
print(classification_report(y_test_clf, y_pred_clf, target_names=["Low Quality (<7)", "High Quality (>=7)"]))


# ==========================================
# 6. DATA VISUALIZATION
# ==========================================
print("\n" + "=" * 60)
print("6. GENERATING PERFORMANCE VISUALIZATIONS")
print("=" * 60)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Plot 1: Actual vs Predicted (Linear Regression)
sns.scatterplot(
    x=y_test_reg,
    y=y_pred_reg,
    ax=axes[0],
    color='royalblue',
    alpha=0.6,
    edgecolor='k'
)
# Reference line for ideal predictions
min_val = min(y_test_reg.min(), y_pred_reg.min())
max_val = max(y_test_reg.max(), y_pred_reg.max())
axes[0].plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Ideal Fit')
axes[0].set_title("Linear Regression: Actual vs Predicted Quality", fontsize=12)
axes[0].set_xlabel("Actual Quality Score", fontsize=10)
axes[0].set_ylabel("Predicted Quality Score", fontsize=10)
axes[0].legend()
axes[0].grid(True, linestyle=":", alpha=0.6)

# Plot 2: Confusion Matrix Heatmap (Logistic Regression)
sns.heatmap(
    cm,
    annot=True,
    fmt='d',
    cmap='Blues',
    cbar=False,
    ax=axes[1],
    xticklabels=["Low Quality (<7)", "High Quality (>=7)"],
    yticklabels=["Low Quality (<7)", "High Quality (>=7)"]
)
axes[1].set_title("Logistic Regression: Confusion Matrix", fontsize=12)
axes[1].set_xlabel("Predicted Class", fontsize=10)
axes[1].set_ylabel("Actual Class", fontsize=10)

plt.tight_layout()
try:
    plt.savefig("model_performance_evaluation.png", dpi=300)
except OSError:
    pass  # read-only filesystem (e.g. Vercel)
plt.show()
print("Saved plots as 'model_performance_evaluation.png'")


# ==========================================
# 7. INFERENCE FUNCTION FOR NEW SAMPLES
# ==========================================
def predict_wine_sample(sample_dict):
    """
    Takes a dictionary containing 11 physicochemical measurements,
    scales the values, and outputs both regression and classification predictions.
    """
    sample_df = pd.DataFrame([sample_dict])[feature_columns]
    
    # Scale features using the respective pre-fitted scalers
    sample_scaled_reg = scaler_reg.transform(sample_df)
    sample_scaled_clf = scaler_clf.transform(sample_df)
    
    predicted_score = lin_reg.predict(sample_scaled_reg)[0]
    predicted_class = log_reg.predict(sample_scaled_clf)[0]
    predicted_prob = log_reg.predict_proba(sample_scaled_clf)[0][1]
    
    class_label = "High Quality (Score >= 7)" if predicted_class == 1 else "Low Quality (Score < 7)"
    
    return {
        "predicted_score": round(predicted_score, 2),
        "predicted_category": class_label,
        "high_quality_probability": round(predicted_prob, 4)
    }


# Test with an example high-alcohol, low-volatile-acidity profile
print("\n" + "=" * 60)
print("7. INFERENCE TEST ON NEW SAMPLE")
print("=" * 60)

sample_wine = {
    'fixed acidity': 7.4,
    'volatile acidity': 0.35,
    'citric acid': 0.45,
    'residual sugar': 2.0,
    'chlorides': 0.065,
    'free sulfur dioxide': 15.0,
    'total sulfur dioxide': 38.0,
    'density': 0.9950,
    'pH': 3.35,
    'sulphates': 0.75,
    'alcohol': 12.0
}

result = predict_wine_sample(sample_wine)
print(f"Sample Chemical Input: {sample_wine}")
print(f"Predicted Continuous Score : {result['predicted_score']}")
print(f"Predicted Category         : {result['predicted_category']}")
print(f"Probability of High Quality: {result['high_quality_probability']}")