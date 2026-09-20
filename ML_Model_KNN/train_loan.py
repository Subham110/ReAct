import json
import joblib
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
#from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score

DATA_PATH = Path("loan_approval_dataset.csv")
MODEL_DIR = Path("models")
MODEL_DIR.mkdir(exist_ok=True)

MODEL_FILE = MODEL_DIR / "loan_pipeline.joblib"
METADATA_FILE = MODEL_DIR / "loan_metadata.json"

FEATURE_COLS = [
    "no_of_dependents",
    "education",
    "self_employed",
    "income_annum",
    "loan_amount",
    "loan_term",
    "cibil_score",
    "residential_assets_value",
    "commercial_assets_value",
    "luxury_assets_value",
    "bank_asset_value",
]


def train():
    df = pd.read_csv(DATA_PATH)

    # Strip whitespace from column names and string values
    df.columns = df.columns.str.strip()
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()

    # Encode categoricals
    df["education"] = (df["education"] == "Graduate").astype(int)
    df["self_employed"] = (df["self_employed"] == "Yes").astype(int)
    df["target"] = (df["loan_status"] == "Approved").astype(int)

    X = df[FEATURE_COLS]
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    pipeline = Pipeline([
        #("scaler", StandardScaler()),
        ("classifier", RandomForestClassifier(
            n_estimators=200,
            max_depth=12,
            min_samples_split=5,
            min_samples_leaf=2,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1,
        ))
    ])

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"\nLoan Approval Model Accuracy: {acc * 100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=["Rejected", "Approved"]))

    #Feature importance from RandomForest
    rf_model = pipeline.named_steps["classifier"]
    feature_importance = {
        col: round(float(imp), 4)
        for col, imp in zip(FEATURE_COLS, rf_model.feature_importances_)
    }

    # Save artifacts
    joblib.dump(pipeline, MODEL_FILE)

    metadata = {
        "model_version": "1.0.5",
        "model_type": "RandomForestClassifier",
        "algorithm": "RandomForestClassifier",
        "accuracy": round(float(acc), 4),
        "features": FEATURE_COLS,
        "feature_importance": feature_importance,
        "cibil_thresholds": {
            "poor": [300, 549],
            "fair": [550, 649],
            "good": [650, 749],
            "excellent": [750, 900],
        },
        "training_samples": len(X_train),
        "test_samples": len(X_test),
    }
    with open(METADATA_FILE, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"\n✓ Saved pipeline to {MODEL_FILE}")
    print(f"✓ Saved metadata to {METADATA_FILE}")
    print(f"\nTop 5 most important features:")
    for feat, imp in sorted(feature_importance.items(), key=lambda x: -x[1])[:5]:
        print(f"  {feat}: {imp:.4f}")


if __name__ == "__main__":
    train()

