import os
from pathlib import Path
from typing import TypedDict
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END

# Load .env
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

# LLM
llm = ChatGroq(model="openai/gpt-oss-20b",temperature=0,api_key=os.getenv("GROQ_API_KEY"))

# Agent State
class AgentState(TypedDict):
    question: str 
    code: str 
    attempt: int 
    has_error: bool

# Generate code
def generate_node(state):
    response = llm.invoke(
        f"""Write ONLY Python code to solve:
{state['question']}

Use input() to take input from the terminal.
Do not include explanations or markdown."""
    )

    code = response.content.replace("```python", "").replace("```", "").strip()

    return {
        **state,
        "code": code,
        "attempt": state["attempt"] + 1
    }


# Check code
def check_node(state):
    low = state["code"].lower()

    has_error = (
        "traceback" in low
        or "syntaxerror" in low
        or "nameerror" in low
        or "typeerror" in low
    )

    return {
        **state,
        "has_error": has_error
    }


# Revise code
def revise_node(state):
    response = llm.invoke(
        f"""Fix this Python code.
Return ONLY the corrected Python code.
Use input() for terminal input.

Code:
{state['code']}"""
    )

    code = response.content.replace("```python", "").replace("```", "").strip()

    return {
        **state,
        "code": code,
        "attempt": state["attempt"] + 1
    }


# Route
def route(state):
    if state["has_error"] and state["attempt"] <= 2:
        return "revise"

    return "end"


# Create graph
graph = StateGraph(AgentState)

graph.add_node("generate", generate_node)
graph.add_node("check", check_node)
graph.add_node("revise", revise_node)

graph.set_entry_point("generate")

graph.add_edge("generate", "check")

graph.add_conditional_edges(
    "check",
    route,
    {
        "revise": "revise",
        "end": END
    }
)

graph.add_edge("revise", "check")

agent = graph.compile()


# Main
def main():

    print("Self-Correction Coding Agent")

    while True:

        q = input("\nAsk a coding question: ")

        if q.strip().lower() == "exit":
            print("Agent stopped.")
            break

        result = agent.invoke({
            "question": q,
            "code": "",
            "attempt": 1,
            "has_error": False
        })

        print("\n[Final Code]")
        print(result["code"])

        print("\n[Program Output]")
        print("\nEnter Number: ")

        try:
            # Execute generated code
            exec(result["code"])

        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    main()