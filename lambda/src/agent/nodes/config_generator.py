import logging
from agent.state import GraphState
from agent.chains.config_generator_node_chain import config_generator_chain

logger = logging.getLogger(__name__)


def config_generator_node(state: GraphState) -> GraphState:
    """Generate MCP tool configuration from Swagger content"""
    
    logger.info("🔧 Starting config generation...")
    
    # Get swagger content from state
    swagger_content = state.get("swagger_content", "")
    reflection_reason = state.get("reflection_reason")
    existing_tool_config = state.get("tool_config")  # Get existing config
    
    logger.info(f"📄 Swagger content length: {len(swagger_content)} chars")
    logger.info(f"🔄 Has existing config: {bool(existing_tool_config)}")
    logger.info(f"💭 Has reflection feedback: {bool(reflection_reason)}")
    
    if not swagger_content:
        logger.error("❌ No swagger_content found in state")
        raise ValueError("No swagger_content found in state")
    
    if reflection_reason:
        logger.info(f"🔍 Reflection feedback: {reflection_reason[:200]}...")
    
    # Call the LLM chain with optional reflection feedback and existing config
    logger.info("🤖 Calling LLM for config generation...")
    result = config_generator_chain.invoke(
        swagger_content, 
        reflection_reason, 
        existing_tool_config
    )
    
    logger.info(
        f"✅ Config generated - tool_config length: "
        f"{len(result.tool_config)} chars"
    )
    logger.info(f"📊 Analysis length: {len(result.analysis)} chars")
    
    # Update state with results
    state.update({
        "analysis": result.analysis,
        "tool_config": result.tool_config,
    })
    
    logger.info("🎯 Config generation completed successfully")
    return state 