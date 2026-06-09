from pathlib import Path


class ExcelExporter:
    def export(self, boq_items: list[dict], output_path: Path) -> Path:
        # Placeholder — integrate openpyxl in production
        output_path.write_text("BOQ export placeholder\n")
        return output_path
