import os
import json
import sys
from dotenv import load_dotenv

# Try to load environment variables from local .env file first
local_env_loaded = load_dotenv(dotenv_path="./.env", override=True)

# If local .env wasn't found, try to load from root .env
if not local_env_loaded:
    root_env_loaded = load_dotenv(dotenv_path="../.env", override=True)
    if root_env_loaded:
        print("Using environment variables from root .env file")
    else:
        print("Warning: No .env file found")

# Import the lambda function from src directory
from src.lambda_function import lambda_handler

def load_sample_swagger():
    """Load sample swagger content for testing"""
    try:
        # Try to load from the root directory
        with open("../swagger_simple.yaml", "r") as f:
            return f.read()
    except FileNotFoundError:
        try:
            # Try to load from current directory
            with open("swagger_simple.yaml", "r") as f:
                return f.read()
        except FileNotFoundError:
            # Return a minimal swagger example if file not found
            return """
openapi: 3.0.0
info:
  title: Test API
  version: "1.0.0"
  description: A simple test API

paths:
  /users:
    get:
      summary: Get all users
      responses:
        "200":
          description: List of users
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    id:
                      type: integer
                    name:
                      type: string
"""

def test_lambda_with_input():
    """
    Test the Lambda handler with user-provided swagger content
    """
    print("Choose an option:")
    print("1. Use sample swagger file")
    print("2. Enter swagger content manually")
    print("3. Load from file path")
    
    choice = input("Enter your choice (1-3): ").strip()
    
    swagger_content = ""
    
    if choice == "1":
        print("Loading sample swagger content...")
        swagger_content = load_sample_swagger()
        print(f"Loaded swagger content ({len(swagger_content)} characters)")
    
    elif choice == "2":
        print("Enter your swagger content (press Ctrl+D when finished):")
        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            swagger_content = "\n".join(lines)
    
    elif choice == "3":
        file_path = input("Enter the path to your swagger file: ").strip()
        try:
            with open(file_path, "r") as f:
                swagger_content = f.read()
            print(f"Loaded swagger content from {file_path} ({len(swagger_content)} characters)")
        except FileNotFoundError:
            print(f"Error: File {file_path} not found")
            return
        except Exception as e:
            print(f"Error reading file: {str(e)}")
            return
    
    else:
        print("Invalid choice")
        return
    
    if not swagger_content.strip():
        print("Error: No swagger content provided")
        return
    
    # Create a test event that mimics the AWS Lambda event
    test_event = {
        "body": json.dumps({
            "swagger_content": swagger_content
        })
    }
    
    # Empty context object (Lambda uses this for runtime information)
    context = {}
    
    print(f"\nRunning Lambda function with swagger content ({len(swagger_content)} chars)")
    print("-" * 70)
    
    # Call the Lambda handler function
    response = lambda_handler(test_event, context)
    
    # Print the response
    print("\nLambda Response:")
    print(f"Status Code: {response.get('statusCode')}")
    print("-" * 70)
    
    # Parse and pretty print the response body
    try:
        response_body = json.loads(response.get('body', '{}'))
        print("Response Body:")
        print(json.dumps(response_body, indent=2))
        
        # If successful, show key results
        if response_body.get('success'):
            print("\n" + "="*70)
            print("🎯 AGENT RESULTS SUMMARY")
            print("="*70)
            print(f"✅ Everything Correct: {response_body.get('is_everything_correct')}")
            print(f"📈 Reflection Score: {response_body.get('reflection_score')}")
            print(f"💭 Reflection Reason: {response_body.get('reflection_reason')}")
            
            if response_body.get('analysis'):
                print(f"\n📊 Analysis Preview:")
                analysis = response_body.get('analysis', '')
                print(f"{analysis[:300]}{'...' if len(analysis) > 300 else ''}")
            
            if response_body.get('tool_config'):
                print(f"\n🔧 Tool Config Generated: ✅")
                tool_config = response_body.get('tool_config')
                if isinstance(tool_config, dict):
                    print(f"   - Tools count: {len(tool_config.get('tools', []))}")
                    print(f"   - Server name: {tool_config.get('server', {}).get('name', 'N/A')}")
                else:
                    print(f"   - Config length: {len(str(tool_config))} characters")
            
            # Save tool config to file for inspection
            if response_body.get('tool_config'):
                try:
                    with open("test_output_tool_config.json", "w", encoding="utf-8") as f:
                        if isinstance(response_body['tool_config'], dict):
                            json.dump(response_body['tool_config'], f, indent=2, ensure_ascii=False)
                        else:
                            f.write(str(response_body['tool_config']))
                    print(f"\n💾 Tool config saved to: test_output_tool_config.json")
                except Exception as e:
                    print(f"\n❌ Failed to save tool config: {e}")
        
    except json.JSONDecodeError as e:
        print(f"Error parsing response body: {e}")
        print("Raw response body:")
        print(response.get('body', ''))

def test_lambda_direct():
    """
    Test the Lambda handler with direct event (no JSON body)
    """
    swagger_content = load_sample_swagger()
    
    # Create a test event with direct swagger_content
    test_event = {
        "swagger_content": swagger_content
    }
    
    context = {}
    
    print(f"Running Lambda function with direct event...")
    print("-" * 50)
    
    response = lambda_handler(test_event, context)
    
    print("\nDirect Event Response:")
    print(json.dumps(response, indent=2))

if __name__ == "__main__":
    print("🧪 Lambda Function Local Tester")
    print("="*50)
    
    # Check if required environment variables are set
    required_vars = [
        "OPENAI_API_KEY"
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("\n⚠️  WARNING: The following required environment variables are not set:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease make sure they are correctly set in your .env file.")
        print("The Lambda function may fail without these variables.")
        
        continue_anyway = input("\nContinue anyway? (y/n): ").lower().strip()
        if continue_anyway != 'y':
            sys.exit(1)
    else:
        print("✅ All required environment variables are set!")
    
    print("\nChoose test method:")
    print("1. Interactive test (recommended)")
    print("2. Direct event test")
    
    method = input("Enter your choice (1-2): ").strip()
    
    if method == "1":
        test_lambda_with_input()
    elif method == "2":
        test_lambda_direct()
    else:
        print("Invalid choice")
        sys.exit(1) 