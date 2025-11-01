"""Agent factory using LangChain's latest create_agent API with structured output."""

import ast
import json
from typing import Any, Optional

from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI

from app.memory import get_conversation_memory
from app.models.response_models import AgentResponse
from app.prompts.agent_prompts import get_agent_prompt
from app.tools import (
    fetch_account_details,
    fetch_facility_details,
    fetch_notes,
    save_notes,
)

# Global agent instance
_agent = None


def create_agent_instance(openai_api_key: str, model_name: str = "gpt-4o-mini") -> Any:
    """
    Create the agent using LangChain's create_agent API with structured output.

    Args:
        openai_api_key: OpenAI API key
        model_name: Model name to use (default: gpt-4o-mini)

    Returns:
        Configured agent
    """
    # Initialize the language model
    llm = ChatOpenAI(
        api_key=openai_api_key, model=model_name, temperature=0.1, max_tokens=2000
    )

    # Get the tools
    tools = [fetch_account_details, fetch_facility_details, save_notes, fetch_notes]

    # Get the prompt template
    prompt = get_agent_prompt()

    # Create agent using the latest create_agent API
    # Pass the Pydantic class directly for structured output
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=prompt.format_messages()[0].content,
        response_format=AgentResponse,
    )

    return agent


def get_agent(openai_api_key: str) -> Any:
    """
    Get the global agent instance, creating it if necessary.

    Args:
        openai_api_key: OpenAI API key

    Returns:
        Agent instance
    """
    global _agent
    if _agent is None:
        _agent = create_agent_instance(openai_api_key)
    return _agent


def process_agent_request(
    agent: Any,
    text: str,
    user_id: str,
    account_id: str,
    facility_id: Optional[str] = None,
    conversation_id: Optional[str] = None,
) -> AgentResponse:
    """
    Process a request through the agent and return structured response.

    Args:
        agent: The agent instance
        text: User's message
        user_id: User ID
        account_id: Account ID
        facility_id: Optional facility ID
        conversation_id: Optional conversation ID

    Returns:
        Structured agent response
    """
    # Get or create conversation ID
    conv_memory = get_conversation_memory()
    final_conversation_id = conv_memory.get_or_create_conversation_id(
        user_id, conversation_id
    )

    # Build concise context and include brief recent history for follow-ups
    recent_history = conv_memory.get_conversation_history(final_conversation_id, 6)
    recent_history_text = "\n".join(
        [str(m) for m in recent_history[-5:]]
    ) if recent_history else ""

    message_content = (
        "User Query: "
        + text
        + "\n\nContext:\n"
        + f"- Account ID: {account_id}\n"
        + f"- User ID: {user_id}\n"
        + (f"- Facility ID: {facility_id}\n" if facility_id else "")
        + ("\nRecent conversation (most recent last):\n" + recent_history_text if recent_history_text else "")
        + "\nRespond with a single JSON object matching the required schema."
    )

    # Prepare input for the agent
    human_message = HumanMessage(content=message_content)
    agent_input = {"messages": [human_message]}

    # Save the human message to conversation memory
    conv_memory.add_message(final_conversation_id, human_message)

    # Run the agent with conversation memory
    try:
        result = agent.invoke(
            agent_input,
            config={
                "configurable": {
                    "thread_id": final_conversation_id,
                    "user_id": user_id,
                    "account_id": account_id,
                    "facility_id": facility_id or "",
                },
                "recursion_limit": 50,
            },
        )

        # Attempt to parse a structured JSON response from the final AI message
        response_payload: Optional[dict] = None
        
        # Case 1: Check for structured_response in result dict (from create_agent with response_format)
        if isinstance(result, dict):
            # Check for structured_response key first
            if "structured_response" in result:
                structured = result["structured_response"]
                if isinstance(structured, dict) and {
                    "final_response",
                    "card_key",
                }.issubset(structured.keys()):
                    response_payload = structured
            
            # Check if result itself is the payload
            if response_payload is None:
                keys = set(result.keys())
                if {"final_response", "card_key"}.issubset(keys):
                    response_payload = result
            
            # Case 1b: result has messages list - look for tool calls and ToolMessages
            if response_payload is None and "messages" in result:
                messages = result["messages"]
                # PRIORITY 1: Check AIMessage tool_calls FIRST (structured data is in tool_call args)
                for msg in reversed(messages):
                    msg_type = getattr(msg, "__class__", None).__name__ if hasattr(msg, "__class__") else None
                    
                    if msg_type == "AIMessage":
                        tool_calls = getattr(msg, "tool_calls", None) or []
                        for tool_call in tool_calls:
                            # Handle both dict and object tool_call formats
                            if isinstance(tool_call, dict):
                                tool_name = tool_call.get("name")
                                args = tool_call.get("args")
                            else:
                                tool_name = getattr(tool_call, "name", None)
                                args = getattr(tool_call, "args", None)
                            
                            if tool_name == "AgentResponse":
                                # Extract args from tool call - this is the structured response
                                if isinstance(args, dict) and {
                                    "final_response",
                                    "card_key",
                                }.issubset(args.keys()):
                                    response_payload = args
                                    break
                        
                        if response_payload:
                            break
                
                # PRIORITY 2: If not found in tool_calls, check ToolMessage
                if response_payload is None:
                    for msg in reversed(messages):
                        msg_type = getattr(msg, "__class__", None).__name__ if hasattr(msg, "__class__") else None
                        
                        # Check ToolMessage for AgentResponse tool result
                        if msg_type == "ToolMessage":
                            tool_name = getattr(msg, "name", None)
                            if tool_name == "AgentResponse":
                                content = getattr(msg, "content", None)
                                if isinstance(content, str):
                                    # Try to parse JSON from ToolMessage content
                                    try:
                                        # Remove prefix if present (e.g., "Returning structured response: ")
                                        clean_content = content
                                        if ":" in content and content.count("{") > 0:
                                            # Find the dict part after colon
                                            colon_idx = content.find(":")
                                            if colon_idx >= 0:
                                                dict_part = content[colon_idx + 1:].strip()
                                                if dict_part.startswith("{") or dict_part.startswith("'"):
                                                    clean_content = dict_part
                                        
                                        # Try to parse as JSON or Python dict string
                                        if clean_content.startswith("{") or clean_content.startswith("'"):
                                            # Try ast.literal_eval first (handles Python dict strings)
                                            try:
                                                parsed = ast.literal_eval(clean_content)
                                                if isinstance(parsed, dict) and {
                                                    "final_response",
                                                    "card_key",
                                                }.issubset(parsed.keys()):
                                                    response_payload = parsed
                                                    break
                                            except (ValueError, SyntaxError):
                                                pass
                                            
                                            # Try JSON parsing
                                            try:
                                                parsed = json.loads(clean_content)
                                                if isinstance(parsed, dict) and {
                                                    "final_response",
                                                    "card_key",
                                                }.issubset(parsed.keys()):
                                                    response_payload = parsed
                                                    break
                                            except json.JSONDecodeError:
                                                pass
                                    except Exception:
                                        continue
                        
                        if response_payload:
                            break

        # Case 2: direct AIMessage (if result is not a dict)
        if response_payload is None and isinstance(result, AIMessage):
            # Check tool_calls first
            tool_calls = getattr(result, "tool_calls", None) or []
            for tool_call in tool_calls:
                tool_name = tool_call.get("name") if isinstance(tool_call, dict) else getattr(tool_call, "name", None)
                if tool_name == "AgentResponse":
                    args = tool_call.get("args") if isinstance(tool_call, dict) else getattr(tool_call, "args", None)
                    if isinstance(args, dict) and {
                        "final_response",
                        "card_key",
                    }.issubset(args.keys()):
                        response_payload = args
                        break
            
            # Check content
            if response_payload is None:
                if isinstance(result.content, dict):
                    if {
                        "final_response",
                        "card_key",
                    }.issubset(result.content.keys()):
                        response_payload = result.content
                elif isinstance(result.content, str):
                    try:
                        response_payload = json.loads(result.content)
                        if not isinstance(response_payload, dict) or not {
                            "final_response",
                            "card_key",
                        }.issubset(response_payload.keys()):
                            response_payload = None
                    except json.JSONDecodeError:
                        pass

        # Absolute fallback to plain text
        if response_payload is None:
            plain_text = str(result)
            ai_message = AIMessage(content=plain_text)
            conv_memory.add_message(final_conversation_id, ai_message)
            return AgentResponse(
                conversation_id=final_conversation_id,
                final_response=plain_text,
                card_key="other",
                account_overview=[],
                facility_overview=None,
                note_overview=[],
            )

        # Ensure conversation_id is set
        response_payload.setdefault("conversation_id", final_conversation_id)

        # Persist the final_response to conversation memory
        ai_message = AIMessage(content=response_payload.get("final_response", ""))
        conv_memory.add_message(final_conversation_id, ai_message)

        # Validate and coerce via Pydantic model to ensure schema correctness
        try:
            validated = AgentResponse.model_validate(response_payload)
            return validated
        except Exception:
            # Normalize optional arrays and return best-effort
            account_overview = response_payload.get("account_overview") or []
            facility_overview = response_payload.get("facility_overview") or None
            note_overview = response_payload.get("note_overview") or []

            return AgentResponse(
                conversation_id=response_payload.get(
                    "conversation_id", final_conversation_id
                ),
                final_response=response_payload.get("final_response", ""),
                card_key=response_payload.get("card_key", "other"),
                account_overview=account_overview,
                facility_overview=facility_overview,
                note_overview=note_overview,
            )

    except Exception as e:
        # Error fallback
        error_response = (
            f"I apologize, but I encountered an error processing your request: {str(e)}"
        )

        # Save the error response to conversation memory
        ai_message = AIMessage(content=error_response)
        conv_memory.add_message(final_conversation_id, ai_message)

        return AgentResponse(
            conversation_id=final_conversation_id,
            final_response=error_response,
            card_key="other",
            account_overview=[],
            facility_overview=None,
            note_overview=[],
        )
