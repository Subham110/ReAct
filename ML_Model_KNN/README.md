# ML Model Inference API v2.0.0

Multi-model ML inference microservice serving **Iris classification** and **Titanic survival prediction** on a single FastAPI instance.

## Architecture

```
ML_Model_KNN/
├── app/
│   ├── __init__.py
│   ├── config.py                     # Environment & dual-model path settings
│   ├── main.py                       # Root FastAPI mounting /iris and /titanic routers
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── iris_router.py            # POST /iris/predict, POST /iris/predict/batch, GET /iris/metadata
│   │   └── titanic_router.py         # POST /titanic/predict, GET /titanic/metadata
│   ├── services/
│   │   ├── __init__.py
│   │   ├── iris_service.py           # KNN pipeline singleton — loads knn_pipeline.joblib
│   │   └── titanic_service.py        # LinearSVC pipeline singleton — loads titanic_pipeline.joblib
│   └── schemas/
│       ├── __init__.py
│       ├── iris_schemas.py           # IrisInput, IrisPredictionResponse
│       ├── titanic_schemas.py        # TitanicInput, TitanicPredictionResponse
│       └── health_schemas.py         # HealthResponse, ModelStatusDetail
├── models/
│   ├── knn_pipeline.joblib           # Trained Iris model (StandardScaler + KNN k=7)
│   ├── titanic_pipeline.joblib       # Trained Titanic model (StandardScaler + LinearSVC)
│   ├── model_metadata.json           # Iris metadata (v1.4.0, accuracy: 100%)
│   └── titanic_metadata.json         # Titanic metadata (v1.0.0, accuracy: 84.92%)
├── tests/
│   ├── __init__.py
│   ├── conftest.py                   # Session-scoped TestClient with lifespan
│   ├── test_iris_api.py              # 6 tests for /iris/* endpoints
│   └── test_titanic_api.py           # 11 tests for /titanic/* + /health/* endpoints
├── Dockerfile                        # Multi-stage production container (uv + Gunicorn)
├── docker-compose.yml                # Container orchestration with all model paths
├── iris.csv                          # Iris dataset (150 samples)
├── Titanic.csv                       # Titanic dataset (891 passengers)
├── train_pipeline.py                 # Iris KNN training script
├── train_titanic.py                  # Titanic LinearSVC training script
├── pyproject.toml                    # Python >= 3.13 dependencies
└── uv.lock                          # Reproducible dependency lockfile
```

## Quick Start

### 1. Install Dependencies
```bash
uv sync
```

### 2. Train Models (if needed)
```bash
# Train Iris KNN (produces models/knn_pipeline.joblib)
uv run python train_pipeline.py

# Train Titanic LinearSVC (produces models/titanic_pipeline.joblib)
uv run python train_titanic.py
```

### 3. Run Development Server
```bash
uv run uvicorn app.main:app --reload --port 8000
```

### 4. Run Tests
```bash
uv run python -m pytest tests/ -v
```

### 5. Docker Deployment
```bash
docker compose up --build -d
```

## API Endpoints

### Global Health
| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health/live` | Liveness probe — process alive check |
| `GET` | `/health/ready` | Readiness probe — all models loaded |

### Iris Classification (`/iris/*`)
| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/iris/predict` | Classify single Iris sample |
| `POST` | `/iris/predict/batch` | Classify multiple samples |
| `GET` | `/iris/metadata` | Model version, accuracy, features |

**Example Request:**
```bash
curl -X POST http://localhost:8000/iris/predict \
  -H "Content-Type: application/json" \
  -d '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'
```

### Titanic Survival Prediction (`/titanic/*`)
| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/titanic/predict` | Predict passenger survival |
| `GET` | `/titanic/metadata` | Model version, accuracy, features |

**Example Request:**
```bash
curl -X POST http://localhost:8000/titanic/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Pclass": 1,
    "Name": "DeWitt Bukater, Miss. Rose",
    "Sex": "female",
    "Age": 17,
    "SibSp": 0,
    "Parch": 1,
    "Fare": 512.0,
    "Cabin": "B20",
    "Embarked": "S"
  }'
```

## Model Details

### Iris — KNN Classifier
- **Algorithm:** K-Nearest Neighbors (k=7, Manhattan distance, distance-weighted)
- **Pipeline:** StandardScaler → KNeighborsClassifier
- **Accuracy:** 100% on test set
- **Features:** sepal_length, sepal_width, petal_length, petal_width

### Titanic — Linear SVC
- **Algorithm:** Linear Support Vector Classification (C=0.1, dual=False)
- **Pipeline:** StandardScaler → LinearSVC
- **Accuracy:** 84.92% on test set
- **Feature Engineering:** Title extraction, FamilySize, IsAlone, HasCabin, Age/Fare/Embarked imputation, one-hot encoding
- **Probability:** Sigmoid-calibrated via `decision_function()`

## Interactive API Docs

Once running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
