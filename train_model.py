import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os

# Create synthetic data
# Format: [hold1, hold2, hold3, flight1, flight2]
X = []
y = []

# Human data (higher variability)
for _ in range(100):
    hold = np.random.normal(0.15, 0.05, 3)
    flight = np.random.normal(0.10, 0.03, 2)
    X.append(np.concatenate([hold, flight]))
    y.append("human")

# Bot data (more uniform and faster)
for _ in range(100):
    hold = np.random.normal(0.05, 0.01, 3)
    flight = np.random.normal(0.03, 0.01, 2)
    X.append(np.concatenate([hold, flight]))
    y.append("bot")

X = np.array(X)
y = np.array(y)

# Train the model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Save model to backend/models/
model_dir = os.path.join("models")
os.makedirs(model_dir, exist_ok=True)
model_path = os.path.join(model_dir, "rf_model.pkl")
joblib.dump(clf, model_path)

print(f"✅ Model saved to {model_path}")
