from app.modules.ai.gemma_client import GemmaClient
from app.modules.ai.prompt_builder import PromptBuilder


class AITakeoffGenerator:
    def __init__(self) -> None:
        self.client = GemmaClient()
        self.prompts = PromptBuilder()

    async def generate(self, drawing_context: str) -> dict:
        prompt = self.prompts.build_takeoff_prompt(drawing_context)
        response = await self.client.generate(prompt)
        return {"measurements": [], "raw_response": response}
