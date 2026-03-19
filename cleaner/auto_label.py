"""받은편지함 자동 라벨 분류기"""

from typing import Callable

from utils.batch import collect_message_ids, batch_modify

LABEL_RULES: list[dict] = [
    {
        "label": "구매/배송",
        "categories": [],
        "sender_keywords": [
            "coupang", "baemin", "gmarket", "11st", "auction",
            "interpark", "ssg", "lotteon", "oliveyoung", "yes24",
        ],
        "subject_keywords": [
            "주문", "배송", "도착예정", "영수증", "결제완료",
            "출고", "택배", "배달",
        ],
    },
    {
        "label": "금융/결제",
        "categories": [],
        "sender_keywords": ["shinhan", "kbcard", "hanacard", "woori", "nhcard"],
        "subject_keywords": [
            "청구서", "납부", "입금", "출금", "카드대금", "보험료", "이체",
        ],
    },
    {
        "label": "인증/보안",
        "categories": [],
        "sender_keywords": [],
        "subject_keywords": [
            "인증번호", "인증코드", "otp", "보안코드", "verification", "[인증]",
        ],
    },
    {
        "label": "뉴스레터",
        "categories": ["CATEGORY_PROMOTIONS"],
        "sender_keywords": ["newsletter", "noreply", "no-reply", "mailer"],
        "subject_keywords": ["뉴스레터", "newsletter", "주간", "월간"],
    },
    {
        "label": "소셜",
        "categories": ["CATEGORY_SOCIAL"],
        "sender_keywords": [
            "facebook", "instagram", "twitter", "linkedin",
            "youtube", "tiktok", "discord",
        ],
        "subject_keywords": [],
    },
    {
        "label": "업데이트/알림",
        "categories": ["CATEGORY_UPDATES"],
        "sender_keywords": [],
        "subject_keywords": ["업데이트", "공지사항", "서비스 알림"],
    },
]

MAX_ANALYZE_RESULTS = 500


def _match_rule(
    rule: dict,
    categories: list[str],
    sender: str,
    subject: str,
) -> bool:
    """메시지가 분류 규칙에 해당하는지 확인한다."""
    if rule["categories"]:
        for cat in rule["categories"]:
            if cat in categories:
                return True

    sender_lower = sender.lower()
    if rule["sender_keywords"]:
        for kw in rule["sender_keywords"]:
            if kw in sender_lower:
                return True

    subject_lower = subject.lower()
    if rule["subject_keywords"]:
        for kw in rule["subject_keywords"]:
            if kw in subject_lower:
                return True

    return False


class AutoLabelCleaner:
    """받은편지함 메일을 분석해 자동으로 라벨을 분류한다."""

    def __init__(self, service) -> None:
        self.service = service
        self._label_id_cache: dict[str, str] = {}

    def fetch_message_ids(self, max_results: int = MAX_ANALYZE_RESULTS) -> list[str]:
        """받은편지함 메시지 ID 수집."""
        return collect_message_ids(self.service, "in:inbox")[:max_results]

    def analyze(
        self,
        msg_ids: list[str],
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> dict[str, list[str]]:
        """메시지 목록을 분석해 라벨별 ID 목록을 반환한다.

        Returns:
            {"구매/배송": ["id1", "id2"], "금융/결제": [...]}
        """
        classified: dict[str, list[str]] = {rule["label"]: [] for rule in LABEL_RULES}
        total = len(msg_ids)

        for i, msg_id in enumerate(msg_ids):
            try:
                msg = (
                    self.service.users()
                    .messages()
                    .get(
                        userId="me",
                        id=msg_id,
                        format="metadata",
                        metadataHeaders=["From", "Subject"],
                    )
                    .execute()
                )
            except Exception:
                if progress_callback:
                    progress_callback(i + 1, total)
                continue

            headers = {
                h["name"]: h.get("value", "")
                for h in msg.get("payload", {}).get("headers", [])
            }
            sender = headers.get("From", "")
            subject = headers.get("Subject", "")
            label_ids = msg.get("labelIds", [])

            for rule in LABEL_RULES:
                if _match_rule(rule, label_ids, sender, subject):
                    classified[rule["label"]].append(msg_id)
                    break  # 첫 번째 매칭 규칙만 적용

            if progress_callback:
                progress_callback(i + 1, total)

        return classified

    def _get_or_create_label(self, name: str) -> str:
        """라벨 ID를 반환한다. 없으면 새로 생성한다."""
        if name in self._label_id_cache:
            return self._label_id_cache[name]

        existing = (
            self.service.users().labels().list(userId="me").execute()
        )
        for label in existing.get("labels", []):
            if label["name"] == name:
                self._label_id_cache[name] = label["id"]
                return label["id"]

        created = (
            self.service.users()
            .labels()
            .create(userId="me", body={"name": name})
            .execute()
        )
        self._label_id_cache[name] = created["id"]
        return created["id"]

    def execute(
        self,
        classified: dict[str, list[str]],
        selected_labels: list[str],
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> dict[str, int]:
        """선택된 라벨에 해당하는 메시지에 라벨을 일괄 적용한다.

        Returns:
            {"구매/배송": 42, "금융/결제": 15}
        """
        results: dict[str, int] = {}
        total_labels = len(selected_labels)

        for idx, label_name in enumerate(selected_labels):
            msg_ids = classified.get(label_name, [])
            if not msg_ids:
                results[label_name] = 0
                if progress_callback:
                    progress_callback(idx + 1, total_labels)
                continue

            label_id = self._get_or_create_label(label_name)
            count = batch_modify(self.service, msg_ids, add_label_ids=[label_id])
            results[label_name] = count

            if progress_callback:
                progress_callback(idx + 1, total_labels)

        return results
