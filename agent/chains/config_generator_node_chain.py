import openai
import os
import yaml
from pathlib import Path
from string import Template

from agent.utils.models import ToolExtractionResult


class ConfigGeneratorChain:
    def __init__(self, model: str = "o3-mini-2025-01-31"):
        self.client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
        self._load_prompts()
        
    def _load_prompts(self):
        """Load prompts from YAML file"""
        prompts_path = Path(__file__).parent.parent / "data" / "prompts.yaml"
        with open(prompts_path, 'r') as f:
            prompts = yaml.safe_load(f)
        prompt_text = prompts["config_generator"]["system_prompt"]
        self.system_prompt_template = Template(prompt_text)
        
    def invoke(self, swagger_content: str, 
               reflection_reason: str = None,
               existing_tool_config: str = None) -> ToolExtractionResult:
        """Generate MCP tool configuration from Swagger/OpenAPI spec"""
        
        # Prepare template variables
        reflection_feedback = ""
        if reflection_reason:
            reflection_feedback = (
                f"Previous feedback to improve:\n{reflection_reason}"
            )
        
        existing_config = ""
        if existing_tool_config:
            existing_config = (
                f"Existing tool configuration to build upon:\n"
                f"{existing_tool_config}"
            )
        
        # Format the prompt with variables using Template
        prompt = self.system_prompt_template.substitute(
            reflection_feedback=reflection_feedback,
            existing_config=existing_config,
            swagger_content=swagger_content
        )
        
        # Call OpenAI with structured output
        response = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=[{"role": "system", "content": prompt}],
            response_format=ToolExtractionResult,
        )
        
        return response.choices[0].message.parsed


# Create instance for import
config_generator_chain = ConfigGeneratorChain()

