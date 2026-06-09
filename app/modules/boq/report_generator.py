from app.modules.boq.boq_generator import BOQGenerator


class ReportGenerator:
    def __init__(self) -> None:
        self.boq = BOQGenerator()

    def generate_summary(self, measurements: list[dict]) -> dict:
        items = self.boq.generate(measurements)
        return {"total_items": len(items), "items": items}
