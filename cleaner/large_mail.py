"""N MB 이상 대용량 메일 인터랙티브 선택 삭제"""

from typing import Callable
from .base import BaseCleaner
from utils.batch import collect_message_ids, batch_delete
from utils.query_builder import larger_than

MB = 1024 * 1024


class LargeMailCleaner(BaseCleaner):
    def __init__(self, service, size_mb: int):
        super().__init__(service)
        self.size_mb = size_mb
        self._query = larger_than(size_mb)

    def _collect_ids(self) -> list[str]:
        return collect_message_ids(self.service, self._query)

    def preview(self) -> int:
        return len(self._collect_ids())

    def get_messages_with_info(self) -> list[dict]:
        """크기 정보와 함께 메시지 목록 반환"""
        ids = self._collect_ids()
        messages = []
        for msg_id in ids:
            try:
                msg = (
                    self.service.users()
                    .messages()
                    .get(
                        userId="me",
                        id=msg_id,
                        format="metadata",
                        metadataHeaders=["Subject", "From"],
                    )
                    .execute()
                )
                headers = {
                    h["name"]: h["value"]
                    for h in msg.get("payload", {}).get("headers", [])
                }
                size_mb = msg.get("sizeEstimate", 0) / MB
                messages.append(
                    {
                        "id": msg_id,
                        "subject": headers.get("Subject", "(제목 없음)"),
                        "from": headers.get("From", "(발신자 없음)"),
                        "size_mb": round(size_mb, 2),
                    }
                )
            except Exception:
                pass
        return sorted(messages, key=lambda x: x["size_mb"], reverse=True)

    def execute(
        self,
        selected_ids: list[str] | None = None,
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> int:
        ids = selected_ids if selected_ids is not None else self._collect_ids()
        if not ids:
            return 0
        return batch_delete(self.service, ids, progress_callback)
