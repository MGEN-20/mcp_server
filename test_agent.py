import json
import sys
from agent.graph import graph
from agent.state import GraphState
from agent.utils.swagger_fetcher import sync_get_swagger_content


def test_agent(source: str = None):
    """Test the LangGraph agent with config generator and reflection"""
    
    # Determine swagger source
    if source is None:
        if len(sys.argv) > 1:
            source = sys.argv[1]
        else:
            source = "swagger_simple.yaml"  # default file
    
    try:
        # Load swagger content from file or URL
        swagger_content = sync_get_swagger_content(source)
    except ValueError as e:
        print(f"❌ Error loading swagger: {e}")
        return None
    
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
        
        # Save tool config to tools_config.json
        try:
            config_data = json.loads(tool_config)
            with open("tools_config.json", "w", encoding="utf-8") as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            print("💾 Config saved to: tools_config.json")
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse tool config as JSON: {e}")
    
    return final_state


if __name__ == "__main__":
    print("🔧 MCP Swagger Agent")
    print("Usage:")
    print("  python test_agent.py                           "
          "# Use default swagger_simple.yaml")
    print("  python test_agent.py path/to/swagger.yaml      "
          "# Use local file")
    print("  python test_agent.py https://example.com/api   "
          "# Fetch from URL")
    print()
    
    test_agent()

