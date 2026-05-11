# AI Job Match Analyzer

AI-powered ATS resume analyzer using:
- FastAPI
- LangChain
- Qdrant
- Ollama
- Docker Compose

## Features

- Resume upload
- PDF ingestion
- Vector embeddings
- Semantic retrieval
- ATS-style scoring
- Local LLM inference
- Chrome extension integration

## Run

```bash
docker compose up --build
```

Pull model:

```bash
docker exec -it job-match-ai-ollama-1 ollama pull qwen2.5:1.5b
```

Backend:
http://localhost:8000/docs

Qdrant Dashboard:
http://localhost:6333/dashboard