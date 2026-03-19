"""BaseCleaner 추상 클래스"""

from abc import ABC, abstractmethod
from typing import Callable


class BaseCleaner(ABC):
    def __init__(self, service):
        self.service = service

    @abstractmethod
    def preview(self) -> int:
        """삭제/수정 대상 건수 반환 (실제 동작 없음)"""
        ...

    @abstractmethod
    def execute(
        self, progress_callback: Callable[[int, int], None] | None = None
    ) -> int:
        """실제 작업 수행. 처리된 총 건수 반환."""
        ...

    def _get_message_subject(self, message_id: str) -> str:
        """메시지 ID로 제목 조회"""
        try:
            msg = (
                self.service.users()
                .messages()
                .get(userId="me", id=message_id, format="metadata",
                     metadataHeaders=["Subject"])
                .execute()
            )
            headers = msg.get("payload", {}).get("headers", [])
            for h in headers:
                if h["name"] == "Subject":
                    return h["value"]
            return "(제목 없음)"
        except Exception:
            return "(조회 실패)"

    def _get_message_size(self, message_id: str) -> int:
        """메시지 ID로 크기(bytes) 조회"""
        try:
            msg = (
                self.service.users()
                .messages()
                .get(userId="me", id=message_id, format="minimal")
                .execute()
            )
            return msg.get("sizeEstimate", 0)
        except Exception:
            return 0
