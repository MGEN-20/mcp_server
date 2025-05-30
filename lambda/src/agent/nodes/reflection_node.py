from agent.state import GraphState
from agent.chains.reflection_node_chain import reflection_chain


def reflection_node(state: GraphState) -> GraphState:
    """Validate generated config and determine if everything is correct"""
    
    # Get required data from state
    swagger_content = state.get("swagger_content", "")
    tool_config = state.get("tool_config", "")
    documentation = state.get("documentation", "")
    
    if not swagger_content or not tool_config:
        raise ValueError("Missing swagger_content or tool_config in state")
    
    # Call the reflection chain
    result = reflection_chain.invoke(
        swagger_content, tool_config, documentation
    )
    
    # Update state with validation results
    state.update({
        "is_everything_correct": result.is_everything_correct,
        "reflection_reason": result.reason,
        "reflection_score": result.score,
    })
    
    return state