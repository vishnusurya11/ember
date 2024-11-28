from typing import List
from langchain_core.messages import BaseMessage, ToolMessage
from langgraph.graph import END, MessageGraph


from refl_chains import revisor, first_responder


from tool_executor import execute_tools



MAX_ITERATIONS = 3

builder=MessageGraph()

builder.add_node("draft", first_responder)
builder.add_node("execute_tools", execute_tools)
builder.add_node("revise", revisor)


builder.add_edge("draft", "execute_tools")
builder.add_edge("execute_tools", "revise")

def event_loop(state: List[BaseMessage]) -> str:
    count_tool_visits = sum(isinstance(item, ToolMessage) for item in state)
    num_iterations = count_tool_visits
    if num_iterations > MAX_ITERATIONS:
        return END
    return "execute_tools"

builder.add_conditional_edges("revise", event_loop)
builder.set_entry_point("draft")


graph = builder.compile()


print(graph.get_graph().draw_ascii())

graph.get_graph().draw_mermaid_png(output_file_path="graph.png")

if __name__ == "__main__":
    print("Hello reflection")
    res = graph.invoke("""Write about all the story types in Save the Cat! Briefly describe each story type and provide 2-3 movie examples for each.

Ensure the exact names from the book are used, and include the key story beats for each type.""")


    print(res[-1].tool_calls[0]["args"]["answer"])