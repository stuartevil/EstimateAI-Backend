class NavigationService:
    def next_page(self, current: int, total: int) -> int:
        return min(current + 1, total - 1)

    def prev_page(self, current: int) -> int:
        return max(current - 1, 0)

    def go_to_page(self, page: int, total: int) -> int:
        return max(0, min(page, total - 1))
