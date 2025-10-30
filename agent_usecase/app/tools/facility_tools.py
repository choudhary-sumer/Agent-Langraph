"""Facility-related tools for the agent."""

from typing import Any, Dict, Optional

from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig

from app.data import get_data_loader


@tool
def fetch_facility_details(
    account_id: Optional[str] = None,
    facility_id: Optional[str] = None,
    *,
    config: Optional[RunnableConfig] = None,
) -> Dict[str, Any]:
    """
    Retrieve facility related information for a given account ID.
    If facility_id is provided, returns specific facility details.
    If facility_id is not provided, returns all facilities for the account.

    Args:
        account_id: The account ID associated with the facility. If not provided,
            fallback to config.configurable["account_id"].
        facility_id: Optional facility ID (falls back to config.configurable["facility_id"]).

    Returns:
        Dictionary containing facility overview data
    """
    # Fallbacks to runnable config
    if not account_id and config and getattr(config, "configurable", None):
        account_id = config.configurable.get("account_id")
    if not facility_id and config and getattr(config, "configurable", None):
        facility_id = config.configurable.get("facility_id")

    data_loader = get_data_loader()

    if facility_id:
        # Fetch specific facility
        facility_data = data_loader.get_facility_by_id(facility_id)
        if facility_data:
            return {"facility_overview": [facility_data]}
        else:
            return {"facility_overview": []}
    else:
        # Fetch all facilities for the account
        facilities = data_loader.get_facilities_by_account_id(account_id)
        return {"facility_overview": facilities}
