"""N일 이상 오래된 메일 삭제"""

from typing import Callable
from .base import BaseCleaner
from utils.batch import collect_message_ids, batch_delete
from utils.query_builder import older_than


class OldMailCleaner(BaseCleaner):
    def __init__(self, service, days: int):
        super().__init__(service)
        self.days = days
        self._query = older_than(days)

    def _collect_ids(self) -> list[str]:
        return collect_message_ids(self.service, self._query)

    def preview(self) -> int:
        return len(self._collect_ids())

    def execute(
        self, progress_callback: Callable[[int, int], None] | None = None
    ) -> int:
        ids = self._collect_ids()
        if not ids:
            return 0
        return batch_delete(self.service, ids, progress_callback)
