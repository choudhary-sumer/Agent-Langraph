# App Package

This directory contains the application code organized by responsibility:

- `agent/`: Agent construction and request processing
- `api/`: FastAPI application and endpoints
- `data/`: Mock JSON datasets and the `DataLoader`
- `memory/`: Conversation memory implementation and DB models
- `models/`: Pydantic request/response schemas
- `prompts/`: System prompt and JSON schema for structured output
- `tools/`: LangChain tools (accounts, facilities, notes)

Entry point for running the server is `../main.py` (uvicorn uses `app.api.main:app`).

Notes:
- Conversation memory is in-memory; no database is required.
- Mock business data is served from `app/data/mock_store.py`.