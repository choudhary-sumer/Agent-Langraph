"""Agent prompt templates with structured output enforcement."""

from typing import Any, Dict

from langchain_core.prompts import ChatPromptTemplate


def get_response_schema() -> Dict[str, Any]:
    """Get the JSON schema for structured responses from the Pydantic model."""
    from app.models.response_models import AgentResponse

    return AgentResponse.model_json_schema()


def get_agent_prompt() -> ChatPromptTemplate:
    """Get the main agent prompt template with structured output enforcement."""

    system_prompt = """You are a helpful AI assistant for account, facility, and notes
management. Decide which tools to call based on the user's intent. Do not rely on
hardcoded rules; use the context and the user's query to choose tools and arguments.

Capabilities:
- Account Information: details, loyalty, rewards, billing, tiers, points
- Facility Information: facility details, medical licenses, agreements
- Notes: save new notes and fetch existing notes

Instructions:
1. Read the user's query and the provided context (account_id, user_id, facility_id).
2. After receiving tool results, STOP and immediately return the final response.
3. Do NOT call tools again after you have the information needed.
4. Return a concise summary (max 2 sentences) in your final response.

IMPORTANT:
- After calling tools and getting results, STOP immediately and return the response.
- Do not call tools multiple times for the same query.
- Keep your final response concise and to-the-point.
"""

    return ChatPromptTemplate.from_messages([("system", system_prompt)])
