## API Endpoints ML Models

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

---

## API Endpoints in Call ML Model (AI Agent Platform)

The `Call_ML_Model` service runs on port **`8001`** (or through the Nginx Ingress on port **`80`**). It exposes the autonomous AI agent reasoning pipeline and cluster health probes.

| Method | Path (Nginx Ingress :80) | Path (Direct Backend :8001) | Description |
|--------|--------------------------|-----------------------------|-------------|
| `POST` | `/api/v1/analyze` | `/api/v1/analyze` | Analyze natural language query for Iris or Titanic |
| `GET` | `/health/live` | `/health/live` | Liveness probe (container health) |
| `GET` | `/health/ready` | `/health/ready` | Readiness probe (checks Agent & ML microservice) |

---

### 1. Main Analysis Endpoint: `POST /api/v1/analyze`

Accepts a natural language query or structured measurements. The autonomous LangChain ReAct agent automatically detects the domain (**Iris** or **Titanic**), calls the respective tool on the ML microservice, and returns a polymorphic visualization schema.

#### Headers
* `Content-Type: application/json`

#### Request Body (`AnalyzeRequest`)
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `query` | `string` | **Yes** | Natural language text or measurements (min length: 1, max length: 1000) |
| `measurements` | `object` | *Optional* | Direct Iris measurements (`sepal_length`, `sepal_width`, `petal_length`, `petal_width`) |

---

#### Example 1: Iris Flower Classification Query

**cURL Request:**
```bash
# Through Nginx Reverse Proxy (:80)
curl -X POST http://localhost/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"query": "Classify: sepal 5.1, 3.5, petal 1.4, 0.2"}'

# Or Direct to Backend (:8001)
curl -X POST http://localhost:8001/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"query": "Classify: sepal 5.1, 3.5, petal 1.4, 0.2"}'
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "domain": "iris",
    "prediction": {
      "species": "setosa",
      "confidence": 1.0
    },
    "probabilities": [
      {
        "species": "setosa",
        "probability": 1.0
      },
      {
        "species": "versicolor",
        "probability": 0.0
      },
      {
        "species": "virginica",
        "probability": 0.0
      }
    ],
    "feature_comparison": [
      {
        "feature": "Sepal Length",
        "input_value": 5.1,
        "setosa_avg": 5.01,
        "versicolor_avg": 5.94,
        "virginica_avg": 6.59
      },
      {
        "feature": "Sepal Width",
        "input_value": 3.5,
        "setosa_avg": 3.42,
        "versicolor_avg": 2.77,
        "virginica_avg": 2.97
      },
      {
        "feature": "Petal Length",
        "input_value": 1.4,
        "setosa_avg": 1.46,
        "versicolor_avg": 4.26,
        "virginica_avg": 5.55
      },
      {
        "feature": "Petal Width",
        "input_value": 0.2,
        "setosa_avg": 0.24,
        "versicolor_avg": 1.33,
        "virginica_avg": 2.03
      }
    ],
    "analysis": "The flower is classified as Iris setosa with 100% confidence. Its petal length of 1.4 cm and petal width of 0.2 cm are distinctive characteristics exclusive to the setosa species.",
    "visualization_hints": {
      "chart_type": "radar",
      "highlight_species": "setosa"
    }
  },
  "raw_query": "Classify: sepal 5.1, 3.5, petal 1.4, 0.2",
  "processing_time_ms": 412.35,
  "error": null
}
```

---

#### Example 2: Titanic Survival Prediction Query

**cURL Request:**
```bash
# Through Nginx Reverse Proxy (:80)
curl -X POST http://localhost/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"query": "Would Rose survive? 1st class, female, age 17, fare 512, cabin B20, embarked S"}'

# Or Direct to Backend (:8001)
curl -X POST http://localhost:8001/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"query": "Would Rose survive? 1st class, female, age 17, fare 512, cabin B20, embarked S"}'
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "domain": "titanic",
    "survived": true,
    "survival_probability": 0.8177,
    "confidence": 0.8177,
    "risk_factors": {
      "passenger_class": "positive — 1st class passengers had priority access to lifeboats",
      "gender": "positive — women had significantly higher survival rates under maritime protocol",
      "family": "positive — traveling with small family increased survival likelihood",
      "fare": "positive — high fare correlated with higher deck accommodations and early warning"
    },
    "passenger_profile": {
      "title": "Miss",
      "class": 1,
      "age": 17.0,
      "sex": "female",
      "family_size": 2,
      "is_alone": false,
      "has_cabin": true,
      "embarked": "S",
      "fare": 512.0
    },
    "analysis": "Passenger Rose has a very high survival probability of 81.8%. Traveling as a 1st-class female passenger provided optimal access to lifeboats during the evacuation.",
    "visualization_hints": {
      "chart_type": "survival_gauge",
      "outcome": "survived"
    }
  },
  "raw_query": "Would Rose survive? 1st class, female, age 17, fare 512, cabin B20, embarked S",
  "processing_time_ms": 530.12,
  "error": null
}
```

---

### 2. Health Endpoints

#### A. Liveness Probe: `GET /health/live`
Used by Docker and Kubernetes to check if the Python FastAPI process is running.

**Request:**
```bash
curl http://localhost:8001/health/live
```

**Response (200 OK):**
```json
{
  "status": "alive"
}
```

---

#### B. Readiness Probe: `GET /health/ready`
Verifies that the Agent backend is active AND that the upstream `ML_Model_KNN` microservice (`:8000`) is reachable with both Iris and Titanic models initialized.

**Request:**
```bash
curl http://localhost/health/ready
# or
curl http://localhost:8001/health/ready
```

**Response (200 OK):**
```json
{
  "status": "ready",
  "agent": true,
  "knn_service": {
    "status": "ready",
    "models": {
      "iris": {
        "loaded": true,
        "version": "1.4.0",
        "model_type": "KNeighborsClassifier"
      },
      "titanic": {
        "loaded": true,
        "version": "1.0.3",
        "model_type": "LinearSVC"
      }
    }
  }
}
```

**Response (503 Service Unavailable — if ML service is down):**
```json
{
  "detail": "KNN service unavailable"
}
```

---

### 3. HTTP Status Codes & Error Handling

| Status Code | Reason | Example Response |
|-------------|--------|------------------|
| `200 OK` | Analysis completed successfully | Standard `AnalyzeResponse` JSON |
| `422 Unprocessable Entity` | Validation error (empty query, query too long, missing fields) | `{"detail": [{"loc": ["body", "query"], "msg": "String should have at least 1 characters", "type": "string_too_short"}]}` |
| `429 Too Many Requests` | Rate limit exceeded at Nginx level (> 10 req/sec) | Handled directly by Nginx |
| `503 Service Unavailable` | Downstream ML service (`ml-api:8000`) is offline or unreachable | `{"detail": "KNN Service Error: ..."}` |
| `500 Internal Server Error` | Groq API failure or unparseable LLM output | `{"detail": "Agent Error: ..."}` |

---

### 4. Custom Response Headers

Every response from the backend includes custom tracing and performance headers:
* **`X-Request-ID`**: Unique UUID4 string assigned to the request for correlation and log tracing.
* **`X-Process-Time`**: Server-side processing time in seconds (e.g., `0.5312`).
