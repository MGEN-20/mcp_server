import openai
import os
import yaml
from pathlib import Path

from agent.utils.models import ToolExtractionResult


class ConfigGeneratorChain:
    def __init__(self, model: str = "gpt-4o"):
        self.client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
        self._load_prompts()
        
    def _load_prompts(self):
        """Load prompts from YAML file"""
        prompts_path = Path(__file__).parent.parent / "data" / "prompts.yaml"
        with open(prompts_path, 'r') as f:
            prompts = yaml.safe_load(f)
        self.system_prompt = prompts["config_generator"]["system_prompt"]
        
    def invoke(self, swagger_content: str, 
               reflection_reason: str = None) -> ToolExtractionResult:
        """Generate MCP tool configuration from Swagger/OpenAPI spec"""
        
        # Build the prompt
        prompt = self.system_prompt
        if reflection_reason:
            prompt += f"\n\nPrevious feedback to improve: {reflection_reason}"
        
        prompt += f"\n\nSwagger/OpenAPI spec:\n{swagger_content}"
        
        # Call OpenAI with structured output
        response = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=[
                {"role": "system", "content": prompt}
            ],
            response_format=ToolExtractionResult,
        )
        
        return response.choices[0].message.parsed


# Create instance for import
config_generator_chain = ConfigGeneratorChain()

