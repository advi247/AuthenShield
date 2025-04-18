import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
import joblib

# Load your pre-processed dataset with extracted features
df = pd.read_csv('dataset/keystroke_data.csv')
X = df.drop('label', axis=1)
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train models
svm = SVC(probability=True)
xgb = XGBClassifier()
rf = RandomForestClassifier()

svm.fit(X_train, y_train)
xgb.fit(X_train, y_train)
rf.fit(X_train, y_train)

# Save models
joblib.dump(svm, 'models/svm_model.pkl')
joblib.dump(xgb, 'models/xgb_model.pkl')
joblib.dump(rf, 'models/rf_model.pkl')
