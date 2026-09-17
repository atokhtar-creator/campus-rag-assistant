# Campus RAG Assistant

A lightweight retrieval-augmented assistant for university FAQs and internal knowledge bases.

The project is intentionally designed to run **without paid APIs**: it uses TF-IDF retrieval locally and exposes a small FastAPI service. An external LLM can be connected later through the service layer.

## Features

- FastAPI REST API
- Local TF-IDF knowledge retrieval
- JSON knowledge-base ingestion
- Source-aware answers
- Health endpoint
- Unit tests
- Docker support
- GitHub Actions CI

## Architecture

```text
Client
  |
  v
FastAPI
  |
  +--> Retriever (TF-IDF)
  |      |
  |      +--> Knowledge Base (JSON)
  |
  +--> Answer Service
```

## Quick start

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:

- API docs: `http://127.0.0.1:8000/docs`
- Health: `http://127.0.0.1:8000/health`

## Example

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d "{\"question\":\"How do I reset my university password?\"}"
```

Example response:

```json
{
  "answer": "Use the university password reset procedure...",
  "sources": [
    {"title": "Password reset", "score": 0.64}
  ]
}
```

## Project structure

```text
app/
  main.py
  models.py
  retriever.py
  service.py
data/
  knowledge_base.json
tests/
  test_api.py
Dockerfile
requirements.txt
```

## Why this project exists

Many support bots fail because they answer from a language model alone. This repository demonstrates a safer pattern: retrieve an approved source first, then generate or return an answer based on that source.

## Roadmap

- [ ] PostgreSQL / pgvector support
- [ ] Hybrid keyword + vector search
- [ ] Authentication
- [ ] Conversation memory
- [ ] LLM provider adapters
- [ ] Admin interface for knowledge-base updates

## License

MIT
