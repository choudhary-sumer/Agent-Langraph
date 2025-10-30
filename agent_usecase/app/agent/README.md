# Agent Module

- `agent_factory.py` builds the LangChain agent via `create_agent_instance` and processes requests with `process_agent_request`.
- Uses `ChatOpenAI` and LangChain tools from `app.tools`.
- Passes `thread_id`, `user_id`, `account_id`, `facility_id` via runnable config.
- Parses agent output and validates against `AgentResponse` Pydantic model.

Key exports:
- `create_agent_instance(api_key: str, model_name: str = "gpt-4o-mini")`
- `get_agent(api_key: str)` (singleton)
- `process_agent_request(...) -> AgentResponse`
