"""받은편지함 자동 라벨 분류기"""

from __future__ import annotations

from typing import Callable

from utils.batch import collect_message_ids, batch_modify, execute_with_backoff

SCORE_DOMAIN_MATCH = 100
SCORE_CATEGORY_MATCH = 70
SCORE_SENDER_KEYWORD_MATCH = 50
SCORE_SUBJECT_KEYWORD = 30
SCORE_SUBJECT_KEYWORD_MAX = 60
SCORE_CATCH_ALL = 1
SCORE_EXCLUDE = -1

LABEL_RULES: list[dict] = [
    {
        "label": "인증/보안",
        "categories": [],
        "sender_domains": [],
        "sender_keywords": [],
        "subject_keywords": [
            "인증번호",
            "인증코드",
            "otp",
            "보안코드",
            "verification",
            "[인증]",
            "본인확인",
            "2차인증",
            "2fa",
            "임시비밀번호",
            "비밀번호 재설정",
            "password reset",
            "verification code",
            "security alert",
            "login attempt",
            "새로운 로그인",
            "새 기기",
        ],
        "exclude_subject_keywords": [],
    },
    {
        "label": "구매/배송",
        "categories": [],
        "sender_domains": [
            "coupang.co.kr",
            "baemin.kr",
            "gmarket.co.kr",
            "11st.co.kr",
            "auction.co.kr",
            "interpark.com",
            "ssg.com",
            "lotteon.com",
            "oliveyoung.co.kr",
            "yes24.com",
            "tmon.co.kr",
            "wemakeprice.com",
            "aliexpress.com",
            "amazon.com",
            "shopify.com",
            "hanjin.co.kr",
            "cjlogistics.com",
        ],
        "sender_keywords": [
            "coupang",
            "baemin",
            "gmarket",
            "11st",
            "auction",
            "interpark",
            "ssg",
            "lotteon",
            "oliveyoung",
            "yes24",
            "tmon",
            "wemakeprice",
            "aliexpress",
            "amazon",
            "shopify",
        ],
        "subject_keywords": [
            "주문",
            "배송",
            "도착예정",
            "결제완료",
            "결제확인",
            "출고",
            "택배",
            "배달",
            "구매확정",
            "반품",
            "교환",
        ],
        "exclude_subject_keywords": [],
    },
    {
        "label": "금융/결제",
        "categories": [],
        "sender_domains": [
            "shinhan.com",
            "kbcard.com",
            "kb.co.kr",
            "hanabank.com",
            "wooribank.com",
            "nhcard.com",
            "nonghyup.com",
            "ibk.co.kr",
            "kakaobank.com",
            "tossbank.com",
            "toss.im",
            "paypal.com",
            "nicepay.co.kr",
            "inicis.com",
            "kcp.co.kr",
            "lottecardapp.com",
        ],
        "sender_keywords": [
            "shinhan",
            "kbcard",
            "hanacard",
            "woori",
            "nhcard",
            "ibk",
            "kakaobank",
            "tossbank",
            "paypal",
            "tosspay",
        ],
        "subject_keywords": [
            "청구서",
            "납부",
            "입금",
            "출금",
            "카드대금",
            "보험료",
            "이체",
            "결제",
            "정산",
            "세금계산서",
        ],
        "exclude_subject_keywords": ["주문", "배송", "배달"],
    },
    {
        "label": "여행/항공",
        "categories": [],
        "sender_domains": [
            "koreanair.com",
            "flyasiana.com",
            "jejuair.net",
            "twayair.com",
            "airbusan.com",
            "airbnb.com",
            "booking.com",
            "expedia.com",
            "agoda.com",
            "hotels.com",
            "yanolja.com",
            "goodchoice.co.kr",
        ],
        "sender_keywords": [
            "koreanair",
            "asiana",
            "jejuair",
            "twayair",
            "airbusan",
            "airbnb",
            "booking",
            "expedia",
            "agoda",
            "hotels",
            "yanolja",
            "goodchoice",
        ],
        "subject_keywords": [
            "항공권",
            "예약확인",
            "체크인",
            "탑승",
            "숙박",
            "호텔",
            "여행",
            "itinerary",
            "reservation",
        ],
        "exclude_subject_keywords": [],
    },
    {
        "label": "구독/멤버십",
        "categories": [],
        "sender_domains": [
            "netflix.com",
            "spotify.com",
            "watcha.com",
            "wavve.com",
            "coupangplay.com",
            "tving.com",
            "microsoft.com",
            "adobe.com",
            "notion.so",
            "slack.com",
            "dropbox.com",
            "github.com",
        ],
        "sender_keywords": [
            "netflix",
            "spotify",
            "watcha",
            "wavve",
            "tving",
            "coupangplay",
            "microsoft",
            "adobe",
            "notion",
            "slack",
            "dropbox",
        ],
        "subject_keywords": [
            "구독",
            "멤버십",
            "subscription",
            "갱신",
            "renewal",
            "월정액",
            "연간결제",
            "trial",
            "무료체험",
        ],
        "exclude_subject_keywords": [],
    },
    {
        "label": "채용/커리어",
        "categories": [],
        "sender_domains": [
            "wanted.co.kr",
            "saramin.co.kr",
            "jobkorea.co.kr",
            "linkedin.com",
            "rocketpunch.com",
            "programmers.co.kr",
            "rallit.com",
            "jumpit.co.kr",
        ],
        "sender_keywords": [
            "wanted",
            "saramin",
            "jobkorea",
            "linkedin",
            "rocketpunch",
            "programmers",
            "rallit",
            "jumpit",
        ],
        "subject_keywords": [
            "채용",
            "지원",
            "합격",
            "불합격",
            "면접",
            "이력서",
            "job",
            "recruit",
            "offer",
            "포지션",
        ],
        "exclude_subject_keywords": [],
    },
    {
        "label": "의료/건강",
        "categories": [],
        "sender_domains": [
            "nhis.or.kr",
            "nps.or.kr",
        ],
        "sender_keywords": [
            "nhis",
            "nps",
            "건강보험",
            "국민연금",
        ],
        "subject_keywords": [
            "진료",
            "처방",
            "건강검진",
            "예방접종",
            "병원",
            "의원",
            "약국",
            "건강",
            "검사결과",
        ],
        "exclude_subject_keywords": [],
    },
    {
        "label": "공공/행정",
        "categories": [],
        "sender_domains": [
            "nts.go.kr",
            "hometax.go.kr",
            "gov.kr",
        ],
        "sender_keywords": [
            "hometax",
            "정부24",
            "민원24",
        ],
        "subject_keywords": [
            "고지서",
            "납세",
            "세금",
            "민원",
            "행정",
            "공공",
            "국세",
            "지방세",
            "과태료",
            "공문",
        ],
        "exclude_subject_keywords": [],
    },
    {
        "label": "교육",
        "categories": [],
        "sender_domains": [
            "class101.net",
            "inflearn.com",
            "fastcampus.co.kr",
            "udemy.com",
            "coursera.org",
            "edx.org",
            "kmooc.kr",
        ],
        "sender_keywords": [
            "class101",
            "inflearn",
            "fastcampus",
            "udemy",
            "coursera",
            "edx",
            "kmooc",
            "megastudy",
        ],
        "subject_keywords": [
            "강의",
            "수료",
            "수강",
            "학습",
            "과제",
            "시험",
            "certificate",
            "completion",
            "교육",
        ],
        "exclude_subject_keywords": [],
    },
    {
        "label": "뉴스레터",
        "categories": ["CATEGORY_PROMOTIONS"],
        "sender_domains": [
            "mailchimp.com",
            "substack.com",
            "stibee.com",
            "mailerlite.com",
            "sendgrid.net",
        ],
        "sender_keywords": ["newsletter", "mailer", "digest"],
        "subject_keywords": ["뉴스레터", "newsletter", "주간", "월간", "digest"],
        "exclude_subject_keywords": [],
    },
    {
        "label": "소셜",
        "categories": ["CATEGORY_SOCIAL"],
        "sender_domains": [
            "facebookmail.com",
            "mail.instagram.com",
            "linkedin.com",
            "tiktok.com",
            "discord.com",
        ],
        "sender_keywords": [
            "facebook",
            "instagram",
            "twitter",
            "tiktok",
            "discord",
            "kakaotalk",
        ],
        "subject_keywords": [],
        "exclude_subject_keywords": [],
    },
    {
        "label": "업데이트/알림",
        "categories": ["CATEGORY_UPDATES"],
        "sender_domains": [],
        "sender_keywords": [],
        "subject_keywords": ["업데이트", "공지사항", "서비스 알림", "점검", "출시"],
        "exclude_subject_keywords": [],
    },
    {
        "label": "기타",
        "categories": [],
        "sender_domains": [],
        "sender_keywords": [],
        "subject_keywords": [],
        "exclude_subject_keywords": [],
        "catch_all": True,
    },
]

BATCH_FETCH_SIZE = 100  # HTTP 배치 요청당 메시지 수 (Google API 최대값)


def _extract_sender_domain(sender: str) -> str:
    """'Display Name <user@domain.com>' 또는 'user@domain.com' 에서 도메인 추출."""
    if "<" in sender:
        email_part = sender.split("<")[-1].rstrip(">").strip()
    else:
        email_part = sender.strip()
    return email_part.split("@")[-1].lower() if "@" in email_part else ""


def _score_rule(
    rule: dict,
    categories: list[str],
    sender: str,
    subject: str,
) -> int:
    """규칙 적합도 점수 반환. SCORE_EXCLUDE(-1)이면 exclude 조건 매칭."""
    if rule.get("catch_all"):
        return SCORE_CATCH_ALL

    subject_lower = subject.lower()

    for kw in rule.get("exclude_subject_keywords", []):
        if kw in subject_lower:
            return SCORE_EXCLUDE

    score = 0

    sender_domain = _extract_sender_domain(sender)
    if sender_domain:
        for domain in rule.get("sender_domains", []):
            if sender_domain == domain or sender_domain.endswith("." + domain):
                score += SCORE_DOMAIN_MATCH
                break

    for cat in rule.get("categories", []):
        if cat in categories:
            score += SCORE_CATEGORY_MATCH
            break

    sender_lower = sender.lower()
    for kw in rule.get("sender_keywords", []):
        if kw in sender_lower:
            score += SCORE_SENDER_KEYWORD_MATCH
            break

    subject_score = 0
    for kw in rule.get("subject_keywords", []):
        if kw in subject_lower:
            subject_score += SCORE_SUBJECT_KEYWORD
            if subject_score >= SCORE_SUBJECT_KEYWORD_MAX:
                break
    score += subject_score

    return score


class AutoLabelCleaner:
    """받은편지함 메일을 분석해 자동으로 라벨을 분류한다."""

    def __init__(self, service) -> None:
        self.service = service
        self._label_id_cache: dict[str, str] = {}

    def fetch_message_ids(self) -> list[str]:
        """받은편지함 메시지 ID 전체 수집."""
        return collect_message_ids(self.service, "in:inbox")

    def analyze(
        self,
        msg_ids: list[str],
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> dict[str, list[str]]:
        """메시지 목록을 분석해 라벨별 ID 목록을 반환한다.

        HTTP 배치 요청(100개/요청)으로 메시지 헤더를 효율적으로 수집한다.

        Returns:
            {"구매/배송": ["id1", "id2"], "금융/결제": [...]}
        """
        classified: dict[str, list[str]] = {rule["label"]: [] for rule in LABEL_RULES}
        total = len(msg_ids)
        processed = 0

        for chunk_start in range(0, total, BATCH_FETCH_SIZE):
            chunk = msg_ids[chunk_start : chunk_start + BATCH_FETCH_SIZE]
            chunk_results: dict[str, dict] = {}

            def _make_callback(mid: str) -> Callable:
                def _cb(
                    request_id: str, response: dict | None, exception: Exception | None
                ) -> None:
                    if exception is None and response is not None:
                        chunk_results[mid] = response

                return _cb

            batch = self.service.new_batch_http_request()
            for msg_id in chunk:
                batch.add(
                    self.service.users()
                    .messages()
                    .get(
                        userId="me",
                        id=msg_id,
                        format="metadata",
                        metadataHeaders=["From", "Subject"],
                    ),
                    callback=_make_callback(msg_id),
                )
            execute_with_backoff(batch)

            for msg_id in chunk:
                msg = chunk_results.get(msg_id)
                if msg is not None:
                    headers = {
                        h["name"]: h.get("value", "")
                        for h in msg.get("payload", {}).get("headers", [])
                    }
                    sender = headers.get("From", "")
                    subject = headers.get("Subject", "")
                    label_ids = msg.get("labelIds", [])

                    best_score = 0
                    best_label: str | None = None
                    for rule in LABEL_RULES:
                        score = _score_rule(rule, label_ids, sender, subject)
                        if score != SCORE_EXCLUDE and score > best_score:
                            best_score = score
                            best_label = rule["label"]
                    if best_label:
                        classified[best_label].append(msg_id)

                processed += 1
                if progress_callback:
                    progress_callback(processed, total)

        return classified

    def _get_or_create_label(self, name: str) -> str:
        """라벨 ID를 반환한다. 없으면 새로 생성한다."""
        if name in self._label_id_cache:
            return self._label_id_cache[name]

        existing = execute_with_backoff(self.service.users().labels().list(userId="me"))
        for label in existing.get("labels", []):
            if label["name"] == name:
                self._label_id_cache[name] = label["id"]
                return label["id"]

        created = execute_with_backoff(
            self.service.users().labels().create(userId="me", body={"name": name})
        )
        self._label_id_cache[name] = created["id"]
        return created["id"]

    def reset_labels(
        self,
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> int:
        """이전에 적용된 자동 분류 라벨을 모두 제거한다."""
        our_label_names = {
            rule["label"] for rule in LABEL_RULES if not rule.get("catch_all")
        }

        existing = execute_with_backoff(self.service.users().labels().list(userId="me"))
        our_labels = [
            label
            for label in existing.get("labels", [])
            if label["name"] in our_label_names
        ]

        if not our_labels:
            return 0

        all_msg_ids: set[str] = set()
        for label in our_labels:
            page_token = None
            while True:
                params: dict = {
                    "userId": "me",
                    "labelIds": [label["id"]],
                    "maxResults": 500,
                }
                if page_token:
                    params["pageToken"] = page_token
                result = execute_with_backoff(
                    self.service.users().messages().list(**params)
                )
                all_msg_ids.update(msg["id"] for msg in result.get("messages", []))
                page_token = result.get("nextPageToken")
                if not page_token:
                    break

        if not all_msg_ids:
            return 0

        label_ids_to_remove = [label["id"] for label in our_labels]
        return batch_modify(
            self.service,
            list(all_msg_ids),
            remove_label_ids=label_ids_to_remove,
            progress_callback=progress_callback,
        )

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
