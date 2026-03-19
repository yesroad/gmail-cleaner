"""Gmail 검색 쿼리 생성 순수 함수 모음"""


def from_sender(email: str) -> str:
    """특정 발신자 메일 쿼리"""
    return f"from:{email}"


def older_than(days: int) -> str:
    """N일 이상 오래된 메일 쿼리"""
    return f"older_than:{days}d"


def larger_than(size_mb: int) -> str:
    """N MB 이상 대용량 메일 쿼리"""
    return f"larger_than:{size_mb}M"


def in_label(label: str) -> str:
    """특정 라벨 내 메일 쿼리"""
    return f"label:{label}"


def is_unread() -> str:
    """읽지 않은 메일 쿼리"""
    return "is:unread"


def in_category(category: str) -> str:
    """카테고리(promotions, social, updates, forums) 내 메일 쿼리"""
    return f"category:{category}"


def combine(*queries: str) -> str:
    """여러 쿼리를 AND로 결합"""
    return " ".join(q for q in queries if q)
