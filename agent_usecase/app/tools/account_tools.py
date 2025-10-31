"""Account-related tools for the agent."""

from typing import Any, Dict, Optional

from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig

from app.data.mock_store import mock_store


@tool
def fetch_account_details(
    account_id: Optional[str] = None, *, config: Optional[RunnableConfig] = None
) -> Dict[str, Any]:
    """
    Retrieve account related information for a given account ID.

    Args:
        account_id: The account ID to fetch details for. If not provided, fallback to
            config.configurable["account_id"].

    Returns:
        Dictionary containing account overview data
    """
    # Fallback to runnable config if account_id not provided
    if not account_id and config and getattr(config, "configurable", None):
        account_id = config.configurable.get("account_id")

    account_data = mock_store.get_account(account_id)

    if account_data:
        return {"account_overview": [account_data]}
    else:
        # Return empty if account not found
        return {"account_overview": []}
