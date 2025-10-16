# 🤖 Enterprise AI Copilot

> An intelligent query routing system that automatically directs user questions to SQL databases, RAG document retrieval, or a hybrid approach combining both.

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-0.3-green.svg)](https://python.langchain.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Overview

Enterprise AI Copilot is a production-ready intelligent assistant that leverages Large Language Models (LLMs) to answer business questions by:

- **SQL Agent**: Translates natural language to SQL queries for structured data
- **RAG Agent**: Retrieves information from document knowledge bases
- **Hybrid Agent**: Combines SQL and RAG results and synthesizes a comprehensive answer using LLM-powered synthesis logic

### Key Features

✨ **Intelligent Query Classification** - Automatically determines whether to use SQL, RAG, or both
🔒 **Enterprise Security** - Azure OpenAI integration with secure credential management
📊 **Comprehensive Logging** - Full execution traces with timing and source attribution
🐳 **Production-Ready** - Dockerized deployment with PostgreSQL backend
🎯 **Modular Architecture** - Clean separation of concerns for easy maintenance and testing
🧠 **LLM-Powered Synthesis** - Hybrid agent synthesizes answers from both SQL and RAG sources for richer responses

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│          User Query (Natural Language)          │
└──────────────────┬──────────────────────────────┘
          │
     ┌──────────▼──────────┐
     │  Query Classifier   │
     │   (LLM-Powered)     │
     └──────────┬──────────┘
          │
  ┌─────────────┼─────────────┐
  │             │             │
┌────▼────┐  ┌────▼────┐  ┌─────▼─────────────┐
│   SQL   │  │   RAG   │  │  Hybrid Agent     │
│  Agent  │  │  Agent  │  │  (Synthesizer)    │
└─────────┘  └─────────┘  └─────────┬─────────┘
               │
           ┌─────────▼─────────┐
           │   Final Answer    │
           └───────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Docker & Docker Compose
- Azure OpenAI API access (or OpenAI API)
- PostgreSQL (included in Docker setup)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/WajdiHammami/ai-copilot.git
cd ai-copilot
```

2. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your Azure OpenAI credentials
```

3. **Run with Docker** (Recommended)
```bash
docker compose up -d
```

4. **Or run locally**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run src/api/streamlit_UI.py
```

5. **Access the web UI**
```
http://localhost:8501
```

## 💻 Usage Examples

### Command Line

**SQL Query**
```bash
python3 -m src.agents.hybrid_agent -q "Who are our top 5 customers by revenue?"
```

**RAG Query**
```bash
python3 -m src.agents.hybrid_agent -q "What is our refund policy?"
```

**Hybrid Query**
```bash
python3 -m src.agents.hybrid_agent -q "List our VIP customers and explain their benefits"
```

### Python API

```python
from src.agents.hybrid_agent import execute_hybrid_query

result = execute_hybrid_query("How many transactions were completed last month?")
print(result['answer'])
print(f"Route taken: {result['route']}")
```

## 📁 Project Structure

```
ai-copilot/
├── src/
│   ├── agents/           # AI agents (SQL, RAG, Hybrid)
│   ├── api/              # Web interfaces (Streamlit)
│   ├── config/           # Configuration and settings
│   ├── db/               # Database connection utilities
│   ├── prompts/          # LLM prompt templates
│   ├── rag/              # Document indexing and retrieval
│   └── utils.py          # Shared utilities and logging
├── data/
│   ├── embeddings/       # FAISS vector store
│   └── postgres/         # PostgreSQL data (Docker volume)
├── logs/                 # Execution logs (JSONL format)
├── tests/                # Unit and integration tests
├── docker-compose.yaml   # Multi-container orchestration
├── Dockerfile            # Container build instructions
└── requirements.txt      # Python dependencies
```

## 🛠️ Technology Stack

| Layer | Technology |
|-------|-----------|
| **LLM** | Azure OpenAI (GPT-3.5/4) |
| **Framework** | LangChain 0.3 |
| **Database** | PostgreSQL 15 |
| **Vector Store** | FAISS |
| **Embeddings** | Azure OpenAI text-embedding-ada-002 |
| **Web UI** | Streamlit |
| **Deployment** | Docker, Docker Compose |
| **Language** | Python 3.12 |

## ⚙️ Configuration

Key environment variables (see `.env.example`):

```bash
# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-35-turbo
AZURE_OPENAI_API_KEY=your-key

# Embeddings
AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME=text-embedding-ada-002

# Database
POSTGRES_HOST=localhost
POSTGRES_DB=copilotdb
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-password
```

## 📊 Logging & Monitoring

All agent executions are logged to `logs/` in JSONL format:

```json
{
  "timestamp": "2025-10-15T14:30:00.123456",
  "agent_type": "hybrid",
  "query": "Who is our most loyal customer?",
  "classification": "sql",
  "answer": "Customer ID 281 with 11 transactions",
  "duration_seconds": 2.45,
  "steps": [...]
}
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_hybrid_agent.py
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments
-
## 🔒 Security & Safety Notes


This project is designed for enterprise environments and follows best practices for credential management and data privacy. However, users should be aware of the following:

- **Read-Only Database Access:** The LLM agent operates using a read-only database account and cannot modify, insert, or delete data. This minimizes risk and ensures data integrity.
- **API Keys & Secrets:** Never commit your `.env` file or any secrets to version control. Use environment variables and secret managers in production.
- **Data Privacy:** Ensure that sensitive business data is not exposed to external LLMs or third-party services unless explicitly permitted.
- **LLM Risks:** Generated answers may contain inaccuracies or hallucinations. Always validate critical outputs before acting on them.
- **Logging:** Logs may contain sensitive queries or results. Secure log files and rotate them regularly.

## 🚧 Weaknesses & Future Improvements

While Enterprise AI Copilot is production-ready, there are areas for future enhancement:

- **Fine-Grained Query Auditing:** Add more granular logging and monitoring for compliance and security.
- **Advanced Access Control:** Integrate with enterprise IAM solutions for user-level permissions.
- **Explainability:** Improve transparency of agent decisions and query routing.
- **UI Enhancements:** Add more visualization and admin controls to the Streamlit UI.
- **Testing & CI:** Expand test coverage and automate with GitHub Actions.
- **Scalability:** Optimize for distributed deployments and larger datasets.


- Built with [LangChain](https://python.langchain.com/)
- Powered by [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
- Vector search via [FAISS](https://github.com/facebookresearch/faiss)

## 📧 Contact

Wajdi Hammami - wajdi1.hammami@gmail.com

---

**Built with ❤️ using Python, LangChain, and Azure OpenAI**
