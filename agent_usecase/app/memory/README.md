# Memory Module

- `database.py`: SQLAlchemy engine, session, and ORM models (`Conversation`, `ConversationMessage`).
- `conversation_memory.py`: PostgreSQL-backed conversation memory with CRUD, cleanup, and stats.
- Exported helpers: `create_tables()`, `get_conversation_memory()`.
- Stores messages and metadata; keyed by conversation ID and user ID.
