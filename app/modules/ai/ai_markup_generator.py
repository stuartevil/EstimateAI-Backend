from app.modules.ai.gemma_client import GemmaClient
from app.modules.ai.prompt_builder import PromptBuilder


class AIMarkupGenerator:
    def __init__(self) -> None:
        self.client = GemmaClient()
        self.prompts = PromptBuilder()

    async def generate(self, page_context: str) -> dict:
        prompt = self.prompts.build_markup_prompt(page_context)
        response = await self.client.generate(prompt)
        return {"markups": [], "raw_response": response}
