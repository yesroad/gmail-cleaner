"""스팸/프로모션/소셜/업데이트/휴지통 비우기"""

from typing import Callable
from .base import BaseCleaner
from utils.batch import collect_message_ids, batch_delete
from utils.query_builder import combine, in_category


CATEGORY_QUERIES = {
    "스팸 (SPAM)": "in:spam",
    "프로모션": "in:promotions",
    "소셜": "in:social",
    "업데이트": "in:updates",
    "휴지통 (TRASH)": "in:trash",
}


class SpamPromoCleaner(BaseCleaner):
    def __init__(self, service, categories: list[str]):
        super().__init__(service)
        self.categories = categories
        self._queries = [CATEGORY_QUERIES[c] for c in categories if c in CATEGORY_QUERIES]

    def _collect_ids(self) -> list[str]:
        ids = []
        for query in self._queries:
            ids.extend(collect_message_ids(self.service, query))
        return list(set(ids))

    def preview(self) -> int:
        return len(self._collect_ids())

    def execute(
        self, progress_callback: Callable[[int, int], None] | None = None
    ) -> int:
        ids = self._collect_ids()
        if not ids:
            return 0
        return batch_delete(self.service, ids, progress_callback)


def get_available_categories() -> list[str]:
    return list(CATEGORY_QUERIES.keys())
