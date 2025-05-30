#!/usr/bin/env python3
"""
Test script for the Lambda function with integrated agent
"""

import json
import logging
import sys
from lambda_function import lambda_handler

# Configure logging to see all agent logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# Sample Swagger content for testing
SAMPLE_SWAGGER = """
openapi: 3.0.0
info:
  title: Simple E-Commerce API
  version: "1.0.0"
  description: A clean and simple e-commerce API

servers:
  - url: https://api.myshop.com/v1
    description: Production

paths:
  /users:
    get:
      summary: Get all users
      tags: [Users]
      responses:
        "200":
          description: List of users
    post:
      summary: Create user
      tags: [Users]
      responses:
        "201":
          description: User created

  /products:
    get:
      summary: Get all products
      tags: [Products]
      responses:
        "200":
          description: List of products
"""

def test_lambda_function():
    """Test the lambda function with sample Swagger content"""
    
    # Prepare test event
    event = {
        "body": {
            "swagger_content": SAMPLE_SWAGGER
        }
    }
    
    # Mock context
    context = {}
    
    print("=" * 80)
    print("🧪 TESTING LAMBDA FUNCTION WITH FULL LOGS")
    print("=" * 80)
    print(f"📄 Input Swagger length: {len(SAMPLE_SWAGGER)} chars")
    print("-" * 80)
    
    try:
        # Call the lambda handler
        response = lambda_handler(event, context)
        
        print("-" * 80)
        print("📊 FINAL RESULTS:")
        print(f"✅ Status Code: {response['statusCode']}")
        
        if response['statusCode'] == 200:
            body = json.loads(response['body'])
            print(f"🎯 Everything correct: {body.get('is_everything_correct')}")
            print(f"📈 Score: {body.get('score')}")
            print(f"🔧 Tool config keys: {list(body.get('tool_config', {}).keys())}")
            
            # Show analysis
            analysis = body.get('analysis', '')
            if analysis:
                print(f"\n📊 Analysis (first 300 chars):")
                print(f"   {analysis[:300]}...")
            
            # Show reflection reason
            reflection = body.get('reflection_reason', '')
            if reflection:
                print(f"\n💭 Reflection (first 300 chars):")
                print(f"   {reflection[:300]}...")
            
            # Show all tools generated
            tools = body.get('tool_config', {}).get('tools', {})
            if tools:
                print(f"\n🔧 Generated {len(tools)} tools:")
                for i, (tool_name, tool_data) in enumerate(tools.items(), 1):
                    print(f"   {i}. {tool_name}")
                    print(f"      Title: {tool_data.get('title')}")
                    print(f"      Method: {tool_data.get('method')}")
                    print(f"      URL: {tool_data.get('external_api')}")
                    if i >= 3:  # Show only first 3 tools
                        print(f"      ... and {len(tools) - 3} more tools")
                        break
        else:
            print(f"❌ Error response: {response['body']}")
            
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()

    print("=" * 80)

if __name__ == "__main__":
    test_lambda_function() 