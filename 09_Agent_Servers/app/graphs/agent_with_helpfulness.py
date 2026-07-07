from __future__ import annotations

from typing import Annotated, Literal

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from pydantic import BaseModel
from typing_extensions import TypedDict

from app.models import get_chat_model
from app.tools import get_tool_belt

MAX_ATTEMPTS = 3

SYSTEM_PROMPT = (
    "You are a helpful assistant specialized in feline (cat) health. "
    "Use the retrieve_information tool for cat-health questions, web search for "
    "current information, and Arxiv for research papers. Cite tool results when "
    "they inform your answer."
)


class State(TypedDict):
    messages: Annotated[list, add_messages]
    attempt_count: int
    is_helpful: bool


class Judgment(BaseModel):
    is_helpful: bool
    reason: str


_tools = get_tool_belt()
_model = get_chat_model().bind_tools(_tools)
_judge = get_chat_model().with_structured_output(Judgment)


def call_model(state: State) -> dict:
    msgs = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    return {"messages": [_model.invoke(msgs)]}


def run_judge(state: State) -> dict:
    questions = [m for m in state["messages"] if isinstance(m, HumanMessage)]
    ai_texts = [
        m for m in state["messages"]
        if m.type == "ai" and not getattr(m, "tool_calls", [])
    ]
    count = state.get("attempt_count", 0) + 1

    if not questions or not ai_texts:
        return {"attempt_count": count, "is_helpful": False}

    result = _judge.invoke([
        SystemMessage(content=(
            "Evaluate whether a cat health assistant's response is helpful: "
            "specific, actionable, and directly answers the question. "
            "Be strict — vague or generic answers are not helpful."
        )),
        HumanMessage(content=(
            f"Question: {questions[0].content}\n\n"
            f"Response: {ai_texts[-1].content}\n\n"
            "Is this response helpful?"
        )),
    ])

    updates: dict = {"attempt_count": count, "is_helpful": result.is_helpful}
    if not result.is_helpful:
        updates["messages"] = [
            HumanMessage(content=(
                f"Your previous answer was judged not helpful: {result.reason}. "
                "Please try again with more specific, actionable information."
            ))
        ]
    return updates


def route_after_model(state: State) -> Literal["tools", "judge"]:
    last = state["messages"][-1]
    if getattr(last, "tool_calls", []):
        return "tools"
    return "judge"


def route_after_judge(state: State) -> Literal["model", "__end__"]:
    if state.get("is_helpful", False) or state.get("attempt_count", 0) >= MAX_ATTEMPTS:
        return END
    return "model"


builder = StateGraph(State)
builder.add_node("model", call_model)
builder.add_node("tools", ToolNode(_tools))
builder.add_node("judge", run_judge)

builder.add_edge(START, "model")
builder.add_conditional_edges("model", route_after_model)
builder.add_edge("tools", "model")
builder.add_conditional_edges("judge", route_after_judge)

graph = builder.compile()
