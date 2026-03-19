"""라벨 기준 분류/삭제/아카이브"""

from typing import Callable
from .base import BaseCleaner
from utils.batch import collect_message_ids, batch_delete, batch_modify
from utils.query_builder import in_label


class LabelCleaner(BaseCleaner):
    def __init__(self, service, label_name: str):
        super().__init__(service)
        self.label_name = label_name
        self._query = in_label(label_name)

    def get_labels(self) -> list[dict]:
        """사용자 정의 라벨 목록 반환"""
        result = self.service.users().labels().list(userId="me").execute()
        labels = result.get("labels", [])
        # 시스템 라벨 제외
        return [l for l in labels if l["type"] == "user"]

    def _collect_ids(self) -> list[str]:
        return collect_message_ids(self.service, self._query)

    def preview(self) -> int:
        return len(self._collect_ids())

    def execute(
        self, progress_callback: Callable[[int, int], None] | None = None
    ) -> int:
        """라벨 내 메일 삭제"""
        ids = self._collect_ids()
        if not ids:
            return 0
        return batch_delete(self.service, ids, progress_callback)

    def archive(
        self, progress_callback: Callable[[int, int], None] | None = None
    ) -> int:
        """라벨 내 메일 아카이브 (INBOX 라벨 제거)"""
        ids = self._collect_ids()
        if not ids:
            return 0
        return batch_modify(
            self.service,
            ids,
            remove_label_ids=["INBOX"],
            progress_callback=progress_callback,
        )

    def mark_read(
        self, progress_callback: Callable[[int, int], None] | None = None
    ) -> int:
        """라벨 내 메일 읽음 처리"""
        ids = self._collect_ids()
        if not ids:
            return 0
        return batch_modify(
            self.service,
            ids,
            remove_label_ids=["UNREAD"],
            progress_callback=progress_callback,
        )
