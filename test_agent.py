import json
from agent.graph import graph
from agent.state import GraphState


def test_agent():
    """Test the LangGraph agent with config generator and reflection"""
    
    # Load swagger content
    with open("swagger_simple.yaml", "r") as f:
        swagger_content = f.read()
    
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
    test_agent()

