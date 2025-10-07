"""Main travel orchestrator agent graph."""
from datetime import datetime, UTC
from typing import Dict, List, Literal, cast
from langchain_core.messages import AIMessage
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.runtime import Runtime
from .context import Context
from .state import InputState, State
from .tools import TOOLS
from .utils import load_chat_model

async def call_model(
    state: State,
    runtime: Runtime[Context],
) -> Dict[str, List[AIMessage]]:
    """Call the LLM powering the travel orchestrator."""
    model = load_chat_model(runtime.context.model).bind_tools(TOOLS)
    # Format the system prompt
    system_message = runtime.context.system_prompt.format(
        system_time=datetime.now(tz=UTC).isoformat()
    )
    # Get the model's response
    response = cast(
        AIMessage,
        await model.ainvoke(
            [{"role": "system", "content": system_message}, *state.messages]
        ),
    )
    # Handle the case when it's the last step and the model still wants to use a tool
    if state.is_last_step and response.tool_calls:
        return {
            "messages": [
                AIMessage(
                    id=response.id,
                    content="I need more steps to complete your travel planning request. Please let me continue or provide more specific details.",
                )
            ]
        }
    return {"messages": [response]}

def route_model_output(state: State) -> Literal["__end__", "tools"]:
    """Determine the next node based on the model's output."""
    last_message = state.messages[-1]
    if not isinstance(last_message, AIMessage):
        raise ValueError(
            f"Expected AIMessage in output edges, but got {type(last_message).__name__}"
        )
    # If there is no tool call, then we finish
    if not last_message.tool_calls:
        return "__end__"
    # Otherwise we execute the requested actions
    return "tools"

# Define the graph
builder = StateGraph(State, input_schema=InputState, context_schema=Context)

# Add nodes
builder.add_node("call_model", call_model)
builder.add_node("tools", ToolNode(TOOLS))

# Set entrypoint
builder.add_edge("__start__", "call_model")

# Add conditional edges
builder.add_conditional_edges(
    "call_model",
    route_model_output,
)

# Add edge back to model after tools
builder.add_edge("tools", "call_model")

# Compile the graph
graph = builder.compile()

