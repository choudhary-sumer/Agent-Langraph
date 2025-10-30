# API Module

- `main.py` defines the FastAPI application, CORS, startup DB table creation, and endpoints.
- Endpoints: `/`, `/health`, `/chat`, `/postman`, `/conversations/*`, `/cleanup`.
- Settings via `pydantic-settings` (`.env`): `openai_api_key`, `model_name`, debug and DB config.
- Injects the agent using `get_agent(settings.openai_api_key)`.
