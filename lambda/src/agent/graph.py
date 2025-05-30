from langgraph.graph import StateGraph, START, END
from agent.state import GraphState
from agent.nodes.config_generator import config_generator_node
from agent.nodes.reflection_node import reflection_node


def should_continue(state: GraphState) -> str:
    """Determine whether to continue with reflection or end"""
    if state.get("is_everything_correct"):
        return END
    else:
        return "config_generator"


# Create the workflow
workflow = StateGraph(GraphState)

# Add nodes
workflow.add_node("config_generator", config_generator_node)
workflow.add_node("reflection", reflection_node)

# Add edges
workflow.add_edge(START, "config_generator")
workflow.add_edge("config_generator", "reflection")
workflow.add_conditional_edges(
    "reflection",
    should_continue,
    {
        "config_generator": "config_generator",
        END: END,
    },
)

# Compile the graph
graph = workflow.compile() 