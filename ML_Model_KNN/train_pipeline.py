import json
import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score,classification_report

MODEL_DIR = "models"
os.makedirs(MODEL_DIR,exist_ok=True)

def train_and_export():
    data_path = "iris.csv"
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset Not found at {data_path}")
    
    df = pd.read_csv(data_path).dropna().drop_duplicates()
    
    feature_cols = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    X = df[feature_cols]
    y = df['species']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    #Build Full ML Pipeline (Scaling + Classifier)
    k=7
    pipeline = Pipeline([
        ('scaler', StandardScaler()),              #weights: closer neighbore get higher power
        ('knn', KNeighborsClassifier(n_neighbors=k,weights='distance',metric='minkowski', p=1)) #p=1 : Manhattan distance (less sensitive to noise)
        ])
    
    # Train Model
    pipeline.fit(X_train, y_train)
    
    #Evaluate
    y_pred = pipeline.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)
    
    print(f"Model Training Finished. Test Accuracy: {acc * 100:.2f}%")
    
    #save the pipeline and Metadata
    model_path = os.path.join(MODEL_DIR, "knn_pipeline.joblib")
    meta_path = os.path.join(MODEL_DIR, "model_metadata.json")
    
    #creates a new binary file at that path, overwriting any previous model object stored there.
    joblib.dump(pipeline, model_path) 
    
    metadata = {
        "model_version": "1.4.0",
        "model_type": "KNeighborsClassifier",
        "features": feature_cols,
        "classes": list(pipeline.classes_),
        "accuracy": acc,
        "n_neighbors": k,
        "scaler": "StandardScaler"
        }
    
    with open(meta_path, "w") as f:
        json.dump(metadata, f, indent=2)
        
    print(f"Artifacts saved to:\n - {model_path}\n - {meta_path}")

if __name__ == "__main__":
    train_and_export()