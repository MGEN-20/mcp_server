import openai
import os
import yaml
from pathlib import Path

from agent.utils.models import SeniorResult


class ReflectionChain:
    def __init__(self, model: str = "gpt-4o"):
        self.client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
        self._load_prompts()
        
    def _load_prompts(self):
        """Load prompts from YAML file"""
        prompts_path = Path(__file__).parent.parent / "data" / "prompts.yaml"
        with open(prompts_path, 'r') as f:
            prompts = yaml.safe_load(f)
        self.system_prompt = prompts["reflection"]["system_prompt"]
        
    def invoke(self, swagger_content: str, tool_config: str, 
               documentation: str) -> SeniorResult:
        """Validate generated config against original Swagger spec"""
        
        prompt = f"""{self.system_prompt}

Original Swagger spec:
{swagger_content}

Generated tool config:
{tool_config}

Generated documentation:
{documentation}
"""
        
        # Call OpenAI with structured output
        response = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=[
                {"role": "system", "content": prompt}
            ],
            response_format=SeniorResult,
        )
        
        return response.choices[0].message.parsed


# Create instance for import
reflection_chain = ReflectionChain() 