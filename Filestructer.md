# Update the folder and file structer 

AI_ML/
│
├── 📂 ML_Model_KNN/                         # 🧠 ML Model Inference Microservice (:8000)
│   ├── 📂 app/
│   │   ├── 📄 __init__.py
│   │   ├── 📄 config.py                     # Model paths & environment settings
│   │   ├── 📄 main.py                       # Root FastAPI app mounting /iris and /titanic routers
│   │   │
│   │   ├── 📂 routers/                      # 🌐 Isolated API Endpoints
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 iris_router.py            # POST /iris/predict & GET /iris/metadata
│   │   │   └── 📄 titanic_router.py         # POST /titanic/predict & GET /titanic/metadata
│   │   │
│   │   ├── 📂 services/                     # ⚙️ Model Execution Engines (Singletons)
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 iris_service.py           # Loads iris_pipeline.joblib into memory
│   │   │   └── 📄 titanic_service.py        # Loads titanic_pipeline.joblib into memory
│   │   │
│   │   └── 📂 schemas/                      # 📋 Pydantic Request/Response Validation Contracts
│   │       ├── 📄 __init__.py
│   │       ├── 📄 iris_schemas.py           # IrisInput, IrisPredictionResponse
│   │       └── 📄 titanic_schemas.py        # TitanicInput, TitanicPredictionResponse
│   │
│   ├── 📂 models/                           # 📦 Serialized Scikit-Learn Pipeline Artifacts
│   │   ├── 📄 knn_pipeline.joblib           # Trained Iris model (StandardScaler + KNN)
│   │   ├── 📄 titanic_pipeline.joblib       # Trained Titanic model (Linear Support Vector Classification)
│   │   └── 📄 model_metadata.json           # Model versions, metrics, and training timestamps
│   │
│   ├── 📂 tests/                            # 🧪 Pytest Test Suite
│   │   ├── 📄 __init__.py
│   │   ├── 📄 test_iris_api.py              # Tests /iris/predict
│   │   └── 📄 test_titanic_api.py           # Tests /titanic/predict
│   │
│   ├── 📄 Dockerfile                        # Multi-stage production container build (uv + Gunicorn)
│   ├── 📄 docker-compose.yml                # Standalone test compose file
│   ├── 📄 iris.csv                          # Iris dataset
│   ├── 📄 Titanic.csv                       # Titanic dataset
│   ├── 📄 train_pipeline.py                 # Training script for Iris
|   |__ 📄 train_pipeline_titanic.py         # Training script for Titanic
│   ├── 📄 pyproject.toml                   
│   └── 📄 uv.lock                           
│
│
└── 📂 Call_ML_Model/                        # 🚀 AI Agent & React Visualizer Platform
    ├── 📄 docker-compose.yml                # 🐳 Orchestrates ML Model (:8000), Agent (:8001), Frontend (:80)
    ├── 📄 README.md                         # Complete project documentation
    │
    ├── 📂 backend/                          # 🤖 AI Agent Microservice (:8001)
    │   ├── 📂 app/
    │   │   ├── 📄 __init__.py
    │   │   ├── 📄 config.py                 # Loads GROQ_API_KEY, KNN_SERVICE_URL
    │   │   ├── 📄 main.py                   # FastAPI app instance, CORS, lifespan, logging
    │   │   │
    │   │   ├── 📂 agents/                   # 🧠 LangChain AI Agent & System Prompts
    │   │   │   ├── 📄 __init__.py
    │   │   │   ├── 📄 botanical_agent.py    # Multi-tool ReAct agent with auto-routing
    │   │   │   └── 📄 prompts.py            # Prompts with schema contracts for Iris & Titanic
    │   │   │
    │   │   ├── 📂 tools/                    # 🛠️ LangChain @tool Integrations
    │   │   │   ├── 📄 __init__.py
    │   │   │   ├── 📄 botanical_tools.py    # @tool predict_iris_species, @tool predict_titanic_survival
    │   │   │   └── 📄 knn_client.py         # Async HTTP client with retry logic connecting to :8000
    │   │   │
    │   │   ├── 📂 schemas/                  # 📊 Data Contracts & Schemas
    │   │   │   ├── 📄 __init__.py
    │   │   │   ├── 📄 request_schemas.py    # AnalyzeRequest (Natural language query)
    │   │   │   └── 📄 response_schemas.py   # Polymorphic VisualizationData (domain: "iris" | "titanic")
    │   │   │
    │   │   ├── 📂 core/                     # 🛡️ Core Infrastructure
    │   │   │   ├── 📄 __init__.py
    │   │   │   ├── 📄 exceptions.py         # Custom error handlers (KNNServiceUnavailable, LLMTimeout)
    │   │   │   └── 📄 logging_config.py     # Structured JSON logging with request correlation IDs
    │   │   │
    │   │   └── 📂 api/v1/                   # 🔌 REST Route Handlers
    │   │       ├── 📄 __init__.py
    │   │       ├── 📄 chat.py               # POST /api/v1/analyze
    │   │       └── 📄 health.py             # GET /health/live & GET /health/ready
    │   │
    │   ├── 📂 tests/                        # 🧪 Backend Pytest Suite
    │   │   ├── 📄 __init__.py
    │   │   ├── 📄 conftest.py
    │   │   └── 📄 test_api.py
    │   │
    │   ├── 📄 .env                          # Local secrets (GROQ_API_KEY, AGENT_MODEL)
    │   ├── 📄 .env.example                  # Environment template
    │   ├── 📄 Dockerfile                    # Multi-stage Python 3.13 production build
    │   ├── 📄 pyproject.toml
    │   └── 📄 uv.lock
    │
    │
    └── 📂 frontend/                         # 🎨 React 19 + Tailwind CSS + Recharts UI (:80 / :5173)
        ├── 📂 src/
        │   ├── 📄 main.jsx                  # React DOM mount point
        │   ├── 📄 App.jsx                   # Dynamic root layout switching between visualizers
        │   │
        │   ├── 📂 components/
        │   │   │
        │   │   ├── 📂 visualizer/           # 📊 Domain-Specific Visualizer Modules
        │   │   │   │
        │   │   │   ├── 📂 iris/             # 🌸 Dedicated Iris Components
        │   │   │   │   ├── 📄 IrisAIVisualizer.jsx       # Main Iris container card
        │   │   │   │   ├── 📄 FeatureRadar.jsx           # 4-axis radial baseline comparison
        │   │   │   │   ├── 📄 ProbabilityChart.jsx       # Horizontal distribution bar chart
        │   │   │   │   └── 📄 ConfidenceGauge.jsx        # Donut confidence meter
        │   │   │   │
        │   │   │   ├── 📂 titanic/          # 🚢 Dedicated Titanic Components
        │   │   │   │   ├── 📄 TitanicAIVisualizer.jsx    # Main Titanic container card
        │   │   │   │   ├── 📄 SurvivalGauge.jsx          # Donut survival likelihood meter
        │   │   │   │   ├── 📄 DemographicBenchmark.jsx   # Historical 1912 demographic bars
        │   │   │   │   └── 📄 PassengerProfileCard.jsx   # Passenger traits & positive/negative weights
        │   │   │   │
        │   │   │   └── 📂 common/           # 🧩 Shared UI Components
        │   │   │       └── 📄 AIExplanation.jsx          # LLM reasoning breakdown & latency badge
        │   │   │
        │   │   ├── 📂 chat/                 # 💬 Conversational Input
        │   │   │   └── 📄 ChatInput.jsx     # Input bar with Quick Preset buttons for Iris & Titanic
        │   │   │
        │   │   └── 📂 common/               # 🏷️ Header, Loaders & Alerts
        │   │       ├── 📄 Header.jsx        # Top navigation with live system status dot
        │   │       ├── 📄 LoadingSpinner.jsx # Animated pulse loader
        │   │       └── 📄 ErrorAlert.jsx    # Dismissible error banner
        │   │
        │   ├── 📂 services/                 # 🌐 API Communication
        │   │   ├── 📄 api.js                # Axios client with interceptors
        │   │   └── 📄 agentService.js       # Calls POST /api/v1/analyze & GET /health/ready
        │   │
        │   ├── 📂 hooks/                    # 🪝 Custom React Hooks
        │   │   └── 📄 useBotanicalAgent.js  # State management for queries, loading, errors, and result data
        │   │
        │   └── 📂 styles/
        │       └── 📄 index.css             # Tailwind imports & custom scrollbar
        │
        ├── 📄 index.html
        ├── 📄 package.json                  # Dependencies (React 19, Recharts, Lucide, Tailwind 4)
        ├── 📄 vite.config.js                # Dev proxy configuration to port 8001
        ├── 📄 nginx.conf                    # Production reverse proxy (Port 80)
        ├── 📄 Dockerfile                    # Multi-stage build (Node build ➔ Nginx)






# Docker HUB set UP 

Prerequisites
Make sure Docker Desktop is open and running on your computer.
Have your Docker Hub username and password (create a free account at hub.docker.com
 if you don't have one).
# # Step 1: Open Terminal in the ML_Model_KNN Folder
Open PowerShell or your terminal and navigate to the project directory:

powershell


cd C:\Users\subha\Downloads\AI_ML\ML_Model_KNN
# Step 2: Log In to Docker Hub
Authenticate your Docker CLI with your Docker Hub account:

bash


docker login
It will ask for your Username 
→
→ enter your Docker Hub username.
It will ask for your Password 
→
→ enter your password (characters will not show as you type, this is normal).
You should see: Login Succeeded.
# Step 3: Build the Docker Image
Docker Hub requires image names in the format:
YOUR_DOCKERHUB_USERNAME/REPOSITORY_NAME:TAG

Run this command (replace <username> with your actual Docker Hub username):

bash


docker build -t <username>/ml-model-api:2.0.0 .
Example: If your Docker Hub username is subham123:
docker build -t subham123/ml-model-api:2.0.0 .

# Step 4 (Optional): Test It Locally First
Before pushing, ensure the container boots up and serves predictions properly:

bash


# 1. Run container in background on port 8000
docker run -d -p 8000:8000 --name test-ml-api <username>/ml-model-api:2.0.0
# 2. Check health endpoint in PowerShell
curl http://localhost:8000/health/ready
# 3. Clean up the test container
docker stop test-ml-api
docker rm test-ml-api
# Step 5: Tag as latest (Best Practice)
It is standard practice to tag your release both with a version (2.0.0) and latest:

bash


docker tag <username>/ml-model-api:2.0.0 <username>/ml-model-api:latest
# Step 6: Push the Image to Docker Hub
Push both tags to your Docker Hub repository:

bash


# Push version 2.0.0
docker push <username>/ml-model-api:2.0.0
# Push latest tag
docker push <username>/ml-model-api:latest
This will upload all the container layers to your Docker Hub account.

Step 7: Verify on Docker Hub
Open your browser and go to hub.docker.com/repositories
.
You will see ml-model-api listed with both 2.0.0 and latest tags.
Now anyone (or your deployment server) can pull and run your model with:
bash


docker run -p 8000:8000 <username>/ml-model-api:latest
3:49 PM
