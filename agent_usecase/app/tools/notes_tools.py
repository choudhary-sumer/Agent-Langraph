"""Notes-related tools for the agent."""

import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig

from app.data.mock_store import mock_store


@tool
def save_notes(
    user_id: Optional[str] = None,
    title: str = "",
    content: str = "",
    *,
    config: Optional[RunnableConfig] = None,
) -> Dict[str, Any]:
    """
    Save MOM (Minutes of Meeting) or notes given by user.

    Args:
        user_id: The user ID who is saving the notes. If not provided, fallback to
            config.configurable["user_id"].
        title: Title of the notes
        content: Content of the notes

    Returns:
        Dictionary containing the saved note information
    """
    # Fallback to runnable config
    if not user_id and config and getattr(config, "configurable", None):
        user_id = config.configurable.get("user_id")
    account_id = None
    if config and getattr(config, "configurable", None):
        account_id = config.configurable.get("account_id")

    note_id = str(uuid.uuid4())
    current_time = datetime.now().isoformat()

    note_data = {
        "id": note_id,
        "user_id": user_id,
        "title": title,
        "content": content,
        "created_at": current_time,
        "updated_at": current_time,
    }

    # Save via mock store under account scope if available
    saved = None
    if account_id:
        saved = mock_store.save_note(account_id, f"{title}: {content}" if title else content)
    success = saved is not None

    if success:
        return {
            "success": True,
            "note_id": note_id,
            "message": f"Note '{title}' saved successfully",
            "note": saved or note_data,
        }
    else:
        return {
            "success": False,
            "message": "Failed to save note",
            "note": saved or note_data,
        }


@tool
def fetch_notes(
    user_id: Optional[str] = None,
    date: Optional[str] = None,
    limit: int = 5,
    *,
    config: Optional[RunnableConfig] = None,
) -> Dict[str, Any]:
    """
    Retrieve notes based on user_id, date, or last N notes.

    Args:
        user_id: The user ID to fetch notes for. If not provided, fallback to
            config.configurable["user_id"].
        date: Optional date filter (YYYY-MM-DD format)
        limit: Maximum number of notes to return (default: 5)

    Returns:
        Dictionary containing the fetched notes
    """
    # Fallback to runnable config
    if not user_id and config and getattr(config, "configurable", None):
        user_id = config.configurable.get("user_id")
    account_id = None
    if config and getattr(config, "configurable", None):
        account_id = config.configurable.get("account_id")

    notes = mock_store.get_notes(account_id=account_id, date=date, last_n=limit)

    return {
        "success": True,
        "note_overview": notes,
        "total_count": len(notes),
        "message": (
            f"Retrieved {len(notes)} notes for account {account_id}" if account_id else f"Retrieved {len(notes)} notes"
        ),
    }
