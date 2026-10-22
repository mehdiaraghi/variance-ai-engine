# Autonomous Financial Variance Engine & AI Analyst

An enterprise-grade analytical microservice built with **FastAPI**, **Pydantic V2**, and **Google Gemini 2.5 Flash**. The service audits financial telemetry, isolates bad data entries without pipeline failure, calculates deterministic variances, and generates machine-readable, structured executive insights for underperforming cost centers.

---

## 🏛️ Architecture & Design Philosophy

The core design principle is **strict separation of concerns**:

1. **Deterministic Calculations First:** Financial formulas (PTD/YTD revenue variance, volume impacts, percentages) are computed strictly in Python domain models—never delegated to probabilistic LLMs to prevent mathematical hallucinations.
2. **Cost & Token Guardrails:** Generative model calls are guarded by business logic. If all cost centers perform within safe thresholds, external API calls are skipped entirely (0 token consumption).
3. **Structured Machine-Readable Output:** The LLM output is constrained to a strict Pydantic schema using Gemini's native JSON mode (`response_schema`), ensuring direct compatibility with downstream databases, message queues, and BI dashboards.
4. **Fault-Tolerant Resilience:** External network hiccups or upstream API outages (e.g., HTTP 503) fail gracefully without terminating the core calculation payload.

```text
[ Ingestion Layer: Batch Payload / Raw JSON ]
                      │
                      ▼
┌──────────────────────────────────────────────┐
│  Domain Entity (`models.py`)                 │
│  - Fail-fast input validation (PTD/YTD)      │
│  - Zero-division prevention & clean metrics  │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│  Orchestration Service (`processor.py`)      │
│  - Non-blocking error triage & audit logging │
│  - Threshold filtering (Critical flags)      │
│  - Consolidated payload compilation          │
└──────────────────────┬───────────────────────┘
                       │
             [ Critical Centers Detected? ]
                  ├── No  ──> Return Clean Payload (0 Tokens Used)
                  └── Yes ──> Route to AI Engine
                                   │
                                   ▼
┌──────────────────────────────────────────────┐
│  AI Engine (`ai_agent.py`)                   │
│  - Context-engineered FP&A system prompt     │
│  - Enforced Pydantic Schema (`response_schema`)
│  - Network timeout & 503 fallback handling   │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
[ Presentation Layer: FastAPI / Interactive Swagger Docs ]
```

---

## 📁 Project Structure

```text
Variance/
├── models.py           # Domain entity (Variance) & Pydantic response schemas
├── processor.py        # Batch orchestration, data triage, and calculations
├── ai_agent.py         # Cost guardrails, prompt builder, and Gemini API integration
├── api.py              # FastAPI endpoints (/health, /variance-report)
├── requirements.txt    # Locked project dependencies
├── Dockerfile          # Production container specification
├── .dockerignore       # Build exclusion patterns
├── .gitignore          # Git exclusion rules
├── .env.example        # Environment variable template
└── README.md           # Technical documentation
```

---

## 🛠️ Tech Stack

* **Language:** Python 3.12 (Object-Oriented Programming, Strict Type Hinting)
* **API Framework:** FastAPI, Uvicorn
* **Data Validation & Schemas:** Pydantic V2
* **Generative AI:** Google GenAI SDK (`gemini-2.5-flash`)
* **Containerization:** Docker
* **Configuration & Security:** Python-Dotenv, Git

---

## 🚀 Getting Started

### 1. Prerequisites
* Python 3.12+
* Docker (optional, for containerized execution)
* Google Gemini API Key ([Get an API key](https://aistudio.google.com/apikey))

### 2. Local Setup
```bash
# Clone the repository
git clone https://github.com/<your-username>/variance-ai-engine.git
cd variance-ai-engine

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

### 4. Running the Application
Start the Uvicorn development server:
```bash
python -m uvicorn api:app --reload
```
Access the interactive Swagger UI at:
**`http://127.0.0.1:8000/docs`**

---

## 🐳 Docker Deployment

Build the container image:
```bash
docker build -t variance-ai-engine .
```

Run the container:
```bash
docker run -p 8000:8000 --env-file .env variance-ai-engine
```

---

## 📡 API Reference

### Health Check
* **Method:** `GET`
* **Endpoint:** `/health`
* **Response:**
  ```json
  {
    "status": "healthy",
    "message": "Mehdi's server is alive!"
  }
  ```

### Variance Analysis & AI Audit
* **Method:** `POST`
* **Endpoint:** `/variance-report`
* **Sample Request Body:**
  ```json
  [
    {
      "cost_center": "CC-101",
      "time_period": "PTD",
      "revenue_actual": 10000,
      "revenue_forecast": 9000,
      "volume_actual": 5000,
      "volume_forecast": 5200
    },
    {
      "cost_center": "CC-102",
      "time_period": "PTD",
      "revenue_actual": 8000,
      "revenue_forecast": 9000,
      "volume_actual": 5000,
      "volume_forecast": 5200
    },
    {
      "cost_center": "CC-104",
      "time_period": "INVALID",
      "revenue_actual": 10000,
      "revenue_forecast": 9000,
      "volume_actual": 5000,
      "volume_forecast": 5200
    }
  ]
  ```

* **Sample Response:**
  ```json
  {
    "total_input_records": 3,
    "valid_count": 2,
    "failed_count": 1,
    "total_revenue_variance": 0,
    "critical_cost_centers": [
      {
        "cost_center": "CC-102",
        "time_period": "PTD",
        "revenue_actual": 8000,
        "revenue_forecast": 9000,
        "volume_actual": 5000,
        "volume_forecast": 5200,
        "revenue_variance": -1000,
        "revenue_percent": -11.11,
        "revenue_status": "Critical Situation"
      }
    ],
    "error_logs": [
      {
        "center": "CC-104",
        "error": "Time Period should be either PTD or YTD"
      }
    ],
    "ai_agent_output": {
      "call_llm": true,
      "ai_analysis": {
        "portfolio_summary": "Net zero portfolio variance driven by strong performance in CC-101 (+1,000) masking severe drag in CC-102 (-1,000).",
        "critical_insights": [
          {
            "cost_center": "CC-102",
            "primary_driver": "Price/Rate Erosion",
            "explanation": "Revenue fell 11.11% while volume missed by only 3.85%, confirming realized price degradation from 1.73 to 1.60 per unit.",
            "recommended_action": "Audit discounting policies and rate cards to recover average yield."
          }
        ]
      }
    }
  }
  ```

---

## 📄 License
This project is licensed under the MIT License.