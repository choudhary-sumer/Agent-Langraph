"""No-op database module for in-memory testing."""


def create_tables() -> None:
    """No-op: database tables are not used in mock/in-memory mode."""
    return None
