# Python 코딩 표준

이 프로젝트의 Python 코드 작성 규칙. PEP 8 기반, ruff + mypy 환경.

---

## 핵심 원칙

| 원칙 | 설명 |
|------|------|
| **KISS** | 가장 단순한 해결책 |
| **DRY** | 중복 코드 함수로 추출 |
| **YAGNI** | 지금 필요한 것만 구현 |
| **명확성** | 코드는 의도를 드러낸다 |

---

## 네이밍 규칙

```python
# 변수/함수: snake_case
user_email = "test@gmail.com"
message_count = 0

def fetch_messages(service, query: str) -> list[dict]:
    ...

# 클래스: PascalCase
class SpamPromoCleaner(BaseCleaner):
    ...

# 상수: UPPER_SNAKE_CASE
MAX_BATCH_SIZE = 1000
DEFAULT_DAYS_THRESHOLD = 30

# 불리언: is_/has_/can_ 접두사
is_authenticated = False
has_unread_messages = True
```

---

## 타입 힌트 (필수)

Python 3.9+ 기준. 모든 함수에 입력/반환 타입을 명시한다.

```python
# ✅ 올바른 예
def build_query(older_than_days: int, label: str = "INBOX") -> str:
    ...

def get_accounts() -> list[str]:
    ...

def execute(
    self,
    service,
    progress_callback: Callable[[int, int], None] | None = None,
) -> int:
    ...

# ❌ 타입 없이 작성 금지
def build_query(older_than_days, label="INBOX"):
    ...
```

**내장 타입 활용** (Python 3.9+, `from __future__ import annotations` 불필요):

```python
# ✅ 내장 타입 직접 사용
def process(items: list[str]) -> dict[str, int]:
    ...

# Optional 대신 union 문법
def find_account(email: str) -> str | None:
    ...
```

---

## 에러 처리

```python
# ✅ 구체적인 예외 타입 사용
try:
    response = service.users().messages().list(userId="me", q=query).execute()
except HttpError as e:
    if e.resp.status == 429:
        raise RateLimitError("Gmail API 요청 한도 초과") from e
    raise

# ❌ 광범위한 except 금지
try:
    ...
except Exception:
    pass  # 절대 금지

# ✅ 리소스는 with 문으로 관리
with open(token_path, "w") as f:
    json.dump(creds.to_json(), f)
```

---

## 클래스 설계 (BaseCleaner 패턴)

새 Cleaner 추가 시:

```python
from cleaner.base import BaseCleaner

class OldMailCleaner(BaseCleaner):
    """N일 이상 된 메일을 삭제한다."""

    def __init__(self, days: int) -> None:
        self.days = days

    def build_query(self) -> str:
        return f"older_than:{self.days}d"

    def preview(self, service) -> int:
        """삭제 대상 건수를 반환한다."""
        ...

    def execute(
        self,
        service,
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> int:
        """실제 삭제를 수행하고 처리된 건수를 반환한다."""
        ...
```

---

## Immutability

```python
# ✅ 새 객체 반환 (원본 변경 금지)
updated_config = {**original_config, "max_results": 500}

# ✅ 리스트 수정 시 복사본 사용
filtered = [m for m in messages if m["id"] != excluded_id]

# ❌ 직접 변형 금지 (공유 상태 오염 가능)
original_config["max_results"] = 500  # 금지
messages.append(new_message)           # 공유 리스트라면 금지
```

---

## 매직 넘버 처리

```python
# ❌ 설명 없는 숫자
if len(message_ids) > 1000:
    ...
time.sleep(0.5)

# ✅ 상수로 추출
MAX_BATCH_SIZE = 1000
RATE_LIMIT_SLEEP_SEC = 0.5

if len(message_ids) > MAX_BATCH_SIZE:
    ...
time.sleep(RATE_LIMIT_SLEEP_SEC)
```

---

## Gmail API 패턴

이 프로젝트 전용 규칙:

```python
# ✅ 배치 처리는 utils/batch.py 활용
from utils.batch import collect_message_ids, batch_delete

message_ids = collect_message_ids(service, query)
deleted = batch_delete(service, message_ids, progress_callback)

# ✅ 쿼리 빌딩은 utils/query_builder.py 활용
from utils.query_builder import build_older_than_query

query = build_older_than_query(days=30, label="INBOX")

# ✅ 인증은 auth.py 통해서만
from auth import get_credentials

creds = get_credentials(email)
service = build("gmail", "v1", credentials=creds)
```

---

## Code Smell 기준

| Smell | 기준 | 해결 |
|-------|------|------|
| 긴 함수 | 40줄 이상 | 작은 함수로 분할 |
| 긴 파일 | 250줄 이상 | 모듈 분리 |
| 깊은 중첩 | 4레벨 이상 | 조기 반환(early return) |
| 매직 넘버 | 설명 없는 숫자 | 상수로 추출 |
| 중복 코드 | 3회 이상 | 함수 추출 |

---

## 검증 명령어

코드 수정 후 반드시 실행:

```bash
# 린트 + 자동 수정
ruff check . --fix
ruff format .

# 타입 체크
mypy .

# 테스트
pytest
```
