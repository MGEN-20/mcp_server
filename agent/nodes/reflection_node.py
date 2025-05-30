import logging
from agent.state import GraphState
from agent.chains.reflection_node_chain import reflection_chain

logger = logging.getLogger(__name__)


def reflection_node(state: GraphState) -> GraphState:
    """Validate generated config and determine if everything is correct"""
    
    logger.info("🔍 Starting reflection validation...")
    
    # Get required data from state
    swagger_content = state.get("swagger_content", "")
    tool_config = state.get("tool_config", "")
    
    logger.info(f"📄 Swagger content length: {len(swagger_content)} chars")
    logger.info(f"🔧 Tool config length: {len(tool_config)} chars")
    
    if not swagger_content or not tool_config:
        logger.error("❌ Missing swagger_content or tool_config in state")
        raise ValueError("Missing swagger_content or tool_config in state")
    
    # Call the reflection chain
    logger.info("🤖 Calling LLM for validation...")
    result = reflection_chain.invoke(
        swagger_content, tool_config
    )
    
    logger.info("✅ Validation completed")
    logger.info(f"🎯 Everything correct: {result.is_everything_correct}")
    logger.info(f"📈 Score: {result.score}/100")
    logger.info(f"💭 Reason length: {len(result.reason)} chars")
    
    if not result.is_everything_correct:
        logger.warning("⚠️ Issues found, will need another iteration")
        logger.info(f"🔍 Feedback preview: {result.reason[:200]}...")
    else:
        logger.info("🎉 All validation checks passed!")
    
    # Update state with validation results
    state.update({
        "is_everything_correct": result.is_everything_correct,
        "reflection_reason": result.reason,
        "reflection_score": result.score,
    })
    
    logger.info("🎯 Reflection validation completed")
    return state