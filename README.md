# IncidentIQ: AI-Powered Incident Investigation Platform

An autonomous incident investigation and root-cause analysis platform powered by Google Gemini 2.5, LangGraph, and hybrid retrieval-augmented generation (RAG).

## 🎯 Project Overview

IncidentIQ is an enterprise-grade AI system that automates incident investigation through:

- **Autonomous Investigation**: LangGraph-based agent autonomously investigates incidents across multiple data sources
- **Hybrid RAG**: Combines vector semantic search (pgvector + sentence-transformers) with BM25 keyword search for optimal retrieval
- **Root Cause Analysis**: Google Gemini 2.5 identifies probable root causes with confidence scoring and evidence-based reasoning
- **Interactive Reports**: Generate comprehensive investigation reports with timeline reconstruction and remediation recommendations
- **Evaluation Framework**: Built-in evaluation metrics (recall@k, MRR, faithfulness, context precision) for continuous improvement

## 📋 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (React + TypeScript)           │
│                    http://localhost:3000                     │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│              Backend API (FastAPI + LangGraph)              │
│                    http://localhost:8000                    │
├─────────────────────────────────────────────────────────────┤
│  • Investigation Agent                                       │
│  • RAG Pipeline (Hybrid: Vector + BM25)                     │
│  • Tool Definitions & Integrations                          │
│  • Observability & Tracing                                  │
│  • Evaluation Framework                                      │
└──────────┬──────────────────┬──────────────────┬────────────┘
           │                  │                  │
    ┌──────▼──────┐   ┌──────▼──────┐   ┌──────▼──────┐
    │  PostgreSQL  │   │    Redis     │   │  Gemini 2.5 │
    │  (pgvector)  │   │   (Caching)  │   │   (LLM)     │
    │ :5432        │   │  :6379       │   │             │
    └──────────────┘   └──────────────┘   └─────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.12+ (for local development)
- Node.js 20+ (for frontend)
- Google Gemini API key

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/TheUnhackableOne/IncidentIQ-AI.git
   cd IncidentIQ-AI
   ```

2. **Configure environment variables**
   ```bash
   cd backend
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

3. **Start services with Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Local Development

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 📁 Project Structure

```
IncidentIQ-AI/
├── backend/
│   ├── app/
│   │   ├── api/              # FastAPI route handlers
│   │   ├── agents/           # LangGraph investigation agent
│   │   ├── llm/              # Google Gemini integration
│   │   ├── rag/              # RAG pipeline orchestration
│   │   ├── retrieval/        # Vector + BM25 retrieval
│   │   ├── reranking/        # Cross-encoder reranking
│   │   ├── models/           # Pydantic request/response models
│   │   ├── services/         # Business logic layer
│   │   ├── tools/            # Agent tool definitions
│   │   ├── evaluation/       # Evaluation metrics framework
│   │   ├── observability/    # Logging, tracing, metrics
│   │   ├── config/           # Configuration management
│   │   └── main.py           # FastAPI application entry point
│   ├── tests/
│   │   ├── unit/             # Unit tests
│   │   └── integration/      # Integration tests
│   ├── requirements.txt      # Python dependencies
│   ├── Dockerfile            # Backend container image
│   └── .env.example          # Environment variables template
│
├── frontend/
│   ├── src/
│   │   ├── api/              # API client setup
│   │   ├── types/            # TypeScript type definitions
│   │   ├── components/       # React components
│   │   ├── pages/            # Page components
│   │   ├── hooks/            # Custom React hooks
│   │   └── App.tsx           # Root component
│   ├── package.json          # Node.js dependencies
│   ├── tsconfig.json         # TypeScript configuration
│   ├── vite.config.ts        # Vite build configuration
│   └── Dockerfile            # Frontend container image
│
├── docker/
│   └── postgres-init.sql     # PostgreSQL initialization
├── docker-compose.yml        # Docker Compose orchestration
├── .github/
│   └── workflows/
│       └── ci.yml            # GitHub Actions CI/CD pipeline
│
├── data/                     # Data storage (git-ignored)
├── evaluation/               # Evaluation results (git-ignored)
├── logs/                     # Application logs (git-ignored)
└── README.md                 # This file
```

## 🔧 Core Components

### Investigation Agent (LangGraph)
- Autonomous multi-step reasoning over incident data
- Iterative hypothesis generation and testing
- Tool integration for data retrieval and analysis
- Configurable investigation depth and timeout

### RAG Pipeline (Hybrid)
- **Vector Retrieval**: Sentence-transformers embeddings (all-MiniLM-L6-v2) stored in pgvector
- **Keyword Retrieval**: BM25 full-text search on PostgreSQL
- **Reranking**: Cross-encoder (ms-marco-MiniLM-L-6-v2) for final ranking
- **Adaptive Chunking**: Configurable chunk size and overlap

### LLM Integration (Google Gemini 2.5)
- Flash model for fast inference
- Tool calling for structured output
- Streaming support for real-time feedback
- Token usage tracking and optimization

### Evaluation Framework
- **Retrieval Metrics**: Recall@K, MRR, NDCG
- **RAG Metrics**: Context Precision, Context Recall, Faithfulness
- **LLM Metrics**: Answer Relevance, Evidence Accuracy
- **Performance Metrics**: Latency, Token Usage

## 📚 API Endpoints

### Investigation
- `POST /api/v1/incidents` - Create new incident
- `GET /api/v1/incidents/{id}` - Get incident details
- `POST /api/v1/incidents/{id}/investigate` - Start investigation
- `GET /api/v1/incidents/{id}/report` - Get investigation report
- `GET /api/v1/investigations/{id}/progress` - Stream investigation progress

### Evaluation
- `POST /api/v1/evaluation/run` - Run evaluation on sample incidents
- `GET /api/v1/evaluation/results` - Get evaluation metrics

## 🧪 Testing

```bash
# Run unit tests
cd backend
pytest tests/unit -v

# Run with coverage
pytest tests/unit --cov=app --cov-report=html

# Run integration tests
pytest tests/integration -v
```

## 🔍 Monitoring & Observability

- **Logging**: JSON structured logging with python-json-logger
- **Tracing**: OpenTelemetry-ready instrumentation
- **Metrics**: Prometheus-compatible metric collection
- **Health Checks**: Docker compose health probes for all services

## 📦 Dependencies

### Backend
- **Framework**: FastAPI 0.104.1
- **Agent Framework**: LangGraph 0.0.20, LangChain 0.1.0
- **LLM**: google-genai 0.3.0 (Gemini 2.5)
- **Embeddings**: sentence-transformers 2.2.2
- **Database**: psycopg 3.1.12 (PostgreSQL driver)
- **Vector DB**: pgvector 0.2.5
- **Search**: rank-bm25 0.2.2
- **Testing**: pytest 7.4.3, pytest-asyncio 0.21.1

### Frontend
- **Framework**: React 18.2.0
- **Language**: TypeScript 5.3.2
- **Build**: Vite 5.0.7
- **HTTP**: Axios 1.6.2
- **Routing**: React Router 6.20.0

## 🚢 Deployment

### Docker
```bash
# Build images
docker-compose build

# Run services
docker-compose up -d

# Check logs
docker-compose logs -f backend
```

### Environment Configuration
See `backend/.env.example` for all configurable options:
- Gemini API credentials
- Database connection strings
- Redis connection
- RAG parameters (chunk size, retrieval top-k)
- Agent configuration (max steps, timeout)

## 📊 Performance Tuning

### RAG Optimization
- Adjust `CHUNK_SIZE` and `CHUNK_OVERLAP` for better context preservation
- Tune `RETRIEVAL_TOP_K` and `RETRIEVAL_SCORE_THRESHOLD` for recall vs precision
- Use reranking for critical queries

### Agent Optimization
- Increase `MAX_INVESTIGATION_STEPS` for complex incidents
- Adjust timeout based on average incident complexity
- Monitor `MAX_TOOL_RETRIES` for reliability

### Database Optimization
- Create indexes on vector columns: `CREATE INDEX ON incidents USING ivfflat (embedding vector_cosine_ops)`
- Vacuum PostgreSQL regularly for optimal performance

## 🤝 Contributing

1. Create feature branch: `git checkout -b feature/amazing-feature`
2. Commit changes: `git commit -m 'Add amazing feature'`
3. Push to branch: `git push origin feature/amazing-feature`
4. Open Pull Request

## 📜 License

This project is licensed under the MIT License - see LICENSE file for details.

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review evaluation results for performance insights

---

**Built with ❤️ using Google Gemini, LangGraph, and FastAPI**
