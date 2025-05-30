from pydantic import BaseModel, Field


class ToolExtractionResult(BaseModel):
    analysis: str = Field(
        description="Reasoning about how the Swagger was interpreted"
    )
    tool_config: str = Field(
        description="JSON configuration for MCP tools and server "
                    "with large_data_fetch flags"
    )


class SeniorResult(BaseModel):
    is_everything_correct: bool = Field(
        description="True if all endpoints were implemented correctly"
    )
    reason: str = Field(
        description="Reasoning of why the answer is what it is"
    )
    score: int = Field(
        description="Score from 0 to 100, 100 being the best"
    ) 