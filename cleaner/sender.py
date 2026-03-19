"""특정 발신자 메일 일괄 삭제"""

from typing import Callable
from .base import BaseCleaner
from utils.batch import collect_message_ids, batch_delete
from utils.query_builder import from_sender


class SenderCleaner(BaseCleaner):
    def __init__(self, service, sender_email: str):
        super().__init__(service)
        self.sender_email = sender_email
        self._query = from_sender(sender_email)

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
