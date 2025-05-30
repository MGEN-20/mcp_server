import json
import os
import sys

# Add the src directory to Python path for local testing
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from agent.graph import graph
from agent.state import GraphState


def run_agent(swagger_content: str):
    """Run the LangGraph agent with config generator and reflection"""
    
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
    
    print("🚀 Starting LangGraph agent...")
    
    # Invoke the graph
    final_state = graph.invoke(initial_state)
    
    print("✅ Agent completed!")
    print(f"🎯 Everything correct: {final_state.get('is_everything_correct')}")
    print(f"📈 Score: {final_state.get('reflection_score')}")
    print(f"💭 Reason: {final_state.get('reflection_reason')}")
    
    # Show analysis if available
    analysis = final_state.get('analysis', '')
    if analysis:
        print(f"📊 Analysis: {analysis[:200]}...")
    
    # Show tool config if available
    tool_config = final_state.get('tool_config', '')
    if tool_config:
        print(f"🔧 Tool config length: {len(tool_config)} characters")
    
    return final_state


def lambda_handler(event, context):
    """AWS Lambda handler function"""
    print("Lambda handler started")
    
    try:
        # Extract swagger content from event
        swagger_content = None
        
        # Handle API Gateway POST requests with JSON body
        if event.get('body'):
            try:
                body = json.loads(event.get('body'))
                swagger_content = body.get('swagger_content')
            except json.JSONDecodeError as e:
                print(f"Error parsing request body: {str(e)}")
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Invalid JSON in request body'})
                }
        
        # If swagger_content wasn't in the body, check other locations
        if not swagger_content:
            swagger_content = event.get('swagger_content')
        
        if not swagger_content:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': "Missing 'swagger_content' parameter"})
            }
        
        print(f"Processing swagger content (length: {len(swagger_content)} chars)")
        
        # Run the agent
        final_state = run_agent(swagger_content)
        
        # Prepare response
        response_data = {
            'success': True,
            'is_everything_correct': final_state.get('is_everything_correct'),
            'reflection_score': final_state.get('reflection_score'),
            'reflection_reason': final_state.get('reflection_reason'),
            'analysis': final_state.get('analysis'),
            'tool_config': final_state.get('tool_config'),
            'documentation': final_state.get('documentation'),
            'requirements': final_state.get('requirements')
        }
        
        # Parse tool_config as JSON if it's a string
        tool_config = final_state.get('tool_config')
        if tool_config and isinstance(tool_config, str):
            try:
                response_data['tool_config'] = json.loads(tool_config)
            except json.JSONDecodeError:
                # Keep as string if it's not valid JSON
                pass
        
        return {
            'statusCode': 200,
            'body': json.dumps(response_data, ensure_ascii=False),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
        
    except Exception as e:
        print(f"Error in Lambda handler: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'success': False
            })
        }
