from agent.state import GraphState
from agent.chains.config_generator_node_chain import config_generator_chain


def config_generator_node(state: GraphState) -> GraphState:
    """Generate MCP tool configuration from Swagger content"""
    
    # Get swagger content from state
    swagger_content = state.get("swagger_content", "")
    reflection_reason = state.get("reflection_reason")
    
    if not swagger_content:
        raise ValueError("No swagger_content found in state")
    
    # Call the LLM chain with optional reflection feedback
    result = config_generator_chain.invoke(swagger_content, reflection_reason)
    
    # Update state with results
    state.update({
        "analysis": result.analysis,
        "tool_config": result.tool_config,
        "documentation": result.documentation,
        "requirements": result.requirements,
    })
    
    return state