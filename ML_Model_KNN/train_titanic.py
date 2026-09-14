"""
Titanic Survival Prediction — Production Model Training Script

Uses Linear Support Vector Classification (LinearSVC) within a Scikit-Learn
Pipeline (StandardScaler + LinearSVC) with comprehensive feature engineering:
  1. Title extraction from Name using regex
  2. FamilySize, IsAlone, and HasCabin derived features
  3. Age imputation based on Title x Pclass group medians
  4. One-hot encoding of categorical features with strict column alignment
  5. Probability calibration using numerically stable sigmoid on decision_function
  6. Model artifact persistence to models/titanic_pipeline.joblib and models/titanic_metadata.json
"""

import os
import json
import re
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import Pipeline


# ==============================================================================
# 1. LOAD AND PREPARE THE TRAINING DATA
# ==============================================================================
DATA_PATH = "Titanic.csv"
if not os.path.exists(DATA_PATH):
    # Fallback check
    if os.path.exists("Titanic-Dataset.csv"):
        DATA_PATH = "Titanic-Dataset.csv"
    else:
        raise FileNotFoundError(f"Dataset not found at {DATA_PATH}")

print(f"Loading dataset from: {DATA_PATH}")
df = pd.read_csv(DATA_PATH)
print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")

# --- Feature Engineering ---
# Extract Title from Name
def extract_title(name: str) -> str:
    match = re.search(r" ([A-Za-z]+)\.", name)
    title = match.group(1) if match else "Unknown"
    rare_titles = {"Lady", "Countess", "Capt", "Col", "Don", "Dr", "Major", "Rev", "Sir", "Jonkheer", "Dona"}
    replacements = {"Mlle": "Miss", "Ms": "Miss", "Mme": "Mrs"}
    if title in rare_titles:
        return "Rare"
    return replacements.get(title, title)

df["Title"] = df["Name"].apply(extract_title)

# Derived family & cabin features
df["FamilySize"] = df["SibSp"] + df["Parch"] + 1
df["IsAlone"] = (df["FamilySize"] == 1).astype(int)
df["HasCabin"] = df["Cabin"].notnull().astype(int)

# --- Handle Missing Values ---
# Embarked: Impute mode ('S')
df["Embarked"] = df["Embarked"].fillna("S")

# Fare: Impute median
fare_median = float(df["Fare"].median())
df["Fare"] = df["Fare"].fillna(fare_median)

# Age: Compute Title x Pclass group medians for precise imputation
age_medians_dict = {}
for (title, pclass), group in df.groupby(["Title", "Pclass"]):
    median_val = group["Age"].median()
    if not np.isnan(median_val):
        age_medians_dict[f"{title}_{pclass}"] = float(median_val)

global_age_median = float(df["Age"].median())

def impute_age(row):
    if pd.isna(row["Age"]):
        key = f"{row['Title']}_{row['Pclass']}"
        return age_medians_dict.get(key, global_age_median)
    return row["Age"]

df["Age"] = df.apply(impute_age, axis=1)

# Select features for the model
feature_cols = [
    "Pclass", "Age", "SibSp", "Parch", "Fare",
    "FamilySize", "IsAlone", "HasCabin",
    "Sex", "Embarked", "Title"
]

X_raw = df[feature_cols]
y = df["Survived"]

# One-hot encode categorical features
X = pd.get_dummies(X_raw, columns=["Sex", "Embarked", "Title"], drop_first=False)
training_columns = list(X.columns)
print(f"Total training features after encoding: {len(training_columns)}")
print(f"Features: {training_columns}")


# ==============================================================================
# 2. TRAIN / TEST SPLIT
# ==============================================================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)
print(f"Train split: {X_train.shape[0]} samples | Test split: {X_test.shape[0]} samples")


# ==============================================================================
# 3. CREATE AND TRAIN THE PIPELINE
# ==============================================================================
# Standardize features and train LinearSVC
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("svc", LinearSVC(C=0.1, dual=False, max_iter=10000, random_state=42))
])

pipeline.fit(X_train, y_train)

# Evaluate model
y_pred = pipeline.predict(X_test)
acc = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, output_dict=True)

print(f"\n==========================================")
print(f"Model Training Completed!")
print(f"Test Set Accuracy: {acc * 100:.2f}%")
print(f"==========================================")
print(classification_report(y_test, y_pred))


# ==============================================================================
# 4. PREDICTION FUNCTION WITH FEATURE ENGINEERING & SIGMOID CALIBRATION
# ==============================================================================
def sigmoid(x: float) -> float:
    """Numerically stable sigmoid function."""
    if x >= 0:
        return 1.0 / (1.0 + np.exp(-x))
    exp_x = np.exp(x)
    return exp_x / (1.0 + exp_x)


def predict_passenger(passenger_dict: dict):
    """
    Simulates production inference:
      1. Convert raw input dict to DataFrame
      2. Re-apply title extraction & derived features
      3. Impute missing Age, Fare, Embarked using training parameters
      4. One-hot encode and reindex to align exactly with training columns
      5. Predict using the trained Pipeline
      6. Compute calibrated probability via sigmoid on decision_function
    """
    row = pd.DataFrame([passenger_dict])
    
    # 1. Title extraction
    row["Title"] = row["Name"].apply(extract_title)
    
    # 2. Derived features
    sibsp = row.get("SibSp", pd.Series([0])).iloc[0] or 0
    parch = row.get("Parch", pd.Series([0])).iloc[0] or 0
    row["FamilySize"] = sibsp + parch + 1
    row["IsAlone"] = (row["FamilySize"] == 1).astype(int)
    row["HasCabin"] = row.get("Cabin", pd.Series([None])).notnull().astype(int)
    
    # 3. Imputation
    if row["Age"].isna().any():
        title = row["Title"].iloc[0]
        pclass = row["Pclass"].iloc[0]
        key = f"{title}_{pclass}"
        row["Age"] = age_medians_dict.get(key, global_age_median)
        
    row["Embarked"] = row["Embarked"].fillna("S")
    row["Fare"] = row["Fare"].fillna(fare_median)
    
    # 4. Encoding and column alignment
    row_encoded = pd.get_dummies(row[feature_cols], columns=["Sex", "Embarked", "Title"], drop_first=False)
    row_aligned = row_encoded.reindex(columns=training_columns, fill_value=0)
    
    # 5. Prediction
    pred = pipeline.predict(row_aligned)[0]
    decision_score = pipeline.decision_function(row_aligned)[0]
    prob = sigmoid(decision_score)
    
    return {
        "survived": bool(pred == 1),
        "survival_probability": round(float(prob), 4),
        "decision_score": round(float(decision_score), 4)
    }


# ==============================================================================
# 5. TEST WITH CUSTOM PASSENGERS
# ==============================================================================
print("\nTesting with Custom Passengers:")

rose = {
    "Pclass": 1,
    "Name": "DeWitt Bukater, Miss. Rose",
    "Sex": "female",
    "Age": 17,
    "SibSp": 0,
    "Parch": 1,
    "Fare": 512.0,
    "Cabin": "B20",
    "Embarked": "S"
}

jack = {
    "Pclass": 3,
    "Name": "Dawson, Mr. Jack",
    "Sex": "male",
    "Age": 20,
    "SibSp": 0,
    "Parch": 0,
    "Fare": 5.0,
    "Cabin": None,
    "Embarked": "S"
}

tommy = {
    "Pclass": 3,
    "Name": "Smith, Master. Tommy",
    "Sex": "male",
    "Age": 5,
    "SibSp": 1,
    "Parch": 1,
    "Fare": 15.0,
    "Cabin": None,
    "Embarked": "S"
}

res_rose = predict_passenger(rose)
res_jack = predict_passenger(jack)
res_tommy = predict_passenger(tommy)

print(f"Rose (1st class female):  Survived={res_rose['survived']} (Prob: {res_rose['survival_probability'] * 100:.1f}%)")
print(f"Jack (3rd class male):    Survived={res_jack['survived']} (Prob: {res_jack['survival_probability'] * 100:.1f}%)")
print(f"Tommy (3rd class child):  Survived={res_tommy['survived']} (Prob: {res_tommy['survival_probability'] * 100:.1f}%)")


# ==============================================================================
# 6. SAVE MODEL AND METADATA ARTIFACTS
# ==============================================================================
os.makedirs("models", exist_ok=True)

MODEL_PATH = "models/titanic_pipeline.joblib"
METADATA_PATH = "models/titanic_metadata.json"

joblib.dump(pipeline, MODEL_PATH)
print(f"\nTrained pipeline saved to: {MODEL_PATH}")

metadata = {
    "model_version": "1.0.3",
    "model_type": "LinearSVC",
    "accuracy": round(acc, 4),
    "classification_report": report,
    "feature_columns": training_columns,
    "age_medians": age_medians_dict,
    "global_age_median": global_age_median,
    "fare_median": fare_median,
    "hyperparameters": {
        "C": 0.1,
        "dual": False,
        "max_iter": 10000
    },
    "scaler": "StandardScaler",
    "dataset_size": int(len(df)),
    "train_size": int(len(X_train)),
    "test_size": int(len(X_test))
}

with open(METADATA_PATH, "w") as f:
    json.dump(metadata, f, indent=2)

print(f"Metadata saved to: {METADATA_PATH}")
print("Training workflow successfully finished!")
