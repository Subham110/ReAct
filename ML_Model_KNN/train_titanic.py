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

DATA_PATH = "Titanic.csv"

df = pd.read_csv(DATA_PATH)

#  Feature Engineering 
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

# Handle Missing Values
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
    "Pclass", 
    "Age",
    "SibSp", 
    "Parch", 
    "Fare",
    "FamilySize", 
    "IsAlone",
    "HasCabin",
    "Sex", 
    "Embarked",
    "Title"
]

X_raw = df[feature_cols]
y = df["Survived"]

# One-hot encode categorical features
X = pd.get_dummies(X_raw, columns=["Sex", "Embarked", "Title"], drop_first=False)
training_columns = list(X.columns)
print(f"Total training features after encoding: {len(training_columns)}")
print(f"Features: {training_columns}")


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)

print(f"Train split: {X_train.shape[0]} samples | Test split: {X_test.shape[0]} samples")

# create pipline
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("svc", LinearSVC(C=0.1, dual=False, max_iter=10000, random_state=42))
])

pipeline.fit(X_train, y_train)

# Evaluate model
y_pred = pipeline.predict(X_test)
acc = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, output_dict=True)

print(f"Model Training Completed!")
print(f"Test Set Accuracy: {acc * 100:.2f}%")
print(classification_report(y_test, y_pred))

# 5.SAVE MODEL AND METADATA ARTIFACTS
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
