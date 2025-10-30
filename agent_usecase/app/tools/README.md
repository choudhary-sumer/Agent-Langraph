# Tools Module

- Tools are simple LangChain `@tool` functions that read from JSON via `DataLoader`.
- They accept IDs as arguments and also fall back to `config.configurable` via `RunnableConfig`.

Available tools:
- `fetch_account_details(account_id)`
- `fetch_facility_details(account_id, facility_id=None)`
- `save_notes(user_id, title, content)`
- `fetch_notes(user_id, date=None, limit=5)`
