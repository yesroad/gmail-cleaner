"""읽지 않은 메일 일괄 읽음 처리"""

from typing import Callable
from .base import BaseCleaner
from utils.batch import collect_message_ids, batch_modify
from utils.query_builder import is_unread


class UnreadCleaner(BaseCleaner):
    def __init__(self, service):
        super().__init__(service)
        self._query = is_unread()

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
        return batch_modify(
            self.service,
            ids,
            remove_label_ids=["UNREAD"],
            progress_callback=progress_callback,
        )
