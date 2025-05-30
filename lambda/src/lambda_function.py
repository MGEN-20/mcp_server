import json
import os
import logging
from agent.graph import graph
from agent.state import GraphState

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """
    AWS Lambda handler that processes Swagger content and returns MCP tool configuration
    
    Expected input:
    {
        "swagger_content": "openapi: 3.0.0\n..."
    }
    
    Returns:
    {
        "statusCode": 200,
        "body": {
            "tool_config": {...},
            "analysis": "...",
            "score": 95,
            "is_everything_correct": true
        }
    }
    """
    
    try:
        logger.info("🚀 Lambda function started")
        
        # Parse input
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event.get('body', event)
        
        swagger_content = body.get('swagger_content')
        if not swagger_content:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Missing swagger_content in request body'
                })
            }
        
        logger.info(f"📄 Received Swagger content: {len(swagger_content)} chars")
        
        # Initialize state for the graph
        initial_state: GraphState = {
            "swagger_content": swagger_content,
            "analysis": None,
            "tool_config": None,
            "documentation": None,
            "requirements": None,
            "is_everything_correct": None,
            "reflection_reason": None,
            "reflection_score": None,
        }
        
        logger.info("🤖 Starting LangGraph agent...")
        
        # Invoke the graph
        final_state = graph.invoke(initial_state)
        
        logger.info("✅ Agent completed!")
        logger.info(f"🎯 Everything correct: {final_state.get('is_everything_correct')}")
        logger.info(f"📈 Score: {final_state.get('reflection_score')}")
        
        # Parse tool config JSON
        tool_config_str = final_state.get('tool_config', '{}')
        try:
            tool_config_json = json.loads(tool_config_str)
        except json.JSONDecodeError as e:
            logger.error(f"❌ Failed to parse tool config as JSON: {e}")
            tool_config_json = {"error": "Invalid JSON generated"}
        
        # Prepare response
        response_body = {
            "tool_config": tool_config_json,
            "analysis": final_state.get('analysis', ''),
            "score": final_state.get('reflection_score', 0),
            "is_everything_correct": final_state.get('is_everything_correct', False),
            "reflection_reason": final_state.get('reflection_reason', '')
        }
        
        logger.info("💾 Returning successful response")
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(response_body, indent=2)
        }
        
    except Exception as e:
        logger.error(f"❌ Lambda function error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': str(e),
                'message': 'Internal server error'
            })
        } 