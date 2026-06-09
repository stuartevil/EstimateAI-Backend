class PromptBuilder:
    def build_markup_prompt(self, page_context: str) -> str:
        return f"Generate construction drawing markups for:\n{page_context}"

    def build_takeoff_prompt(self, drawing_context: str) -> str:
        return f"Generate quantity takeoff from drawing:\n{drawing_context}"
