from typing import TypedDict, Optional


class GraphState(TypedDict):
    # Input
    swagger_content: str
    
    # Config generation results
    analysis: Optional[str]
    tool_config: Optional[str]
    documentation: Optional[str]
    requirements: Optional[str]
    
    # Reflection results
    is_everything_correct: Optional[bool]
    reflection_reason: Optional[str]
    reflection_score: Optional[int] 