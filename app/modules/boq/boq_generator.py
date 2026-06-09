class BOQGenerator:
    def generate(self, measurements: list[dict]) -> list[dict]:
        return [
            {
                "item": m.get("label", "Item"),
                "quantity": m.get("value", 0),
                "unit": m.get("unit", "ea"),
                "type": m.get("measurement_type", "count"),
            }
            for m in measurements
        ]
