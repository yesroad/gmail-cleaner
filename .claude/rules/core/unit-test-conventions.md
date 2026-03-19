# pytest 테스트 규칙

순수 함수(utils, query_builder, cleaner 로직)에 대한 pytest 테스트 작성 규칙.

---

## 적용 대상

- `utils/` — `query_builder.py`, `batch.py`
- `cleaner/` — `build_query()` 등 순수 로직
- `auth.py` — 토큰 파일 경로 생성 등 순수 함수

---

## 파일 위치

```
tests/
├── utils/
│   ├── test_query_builder.py
│   └── test_batch.py
├── cleaner/
│   ├── test_spam_promo.py
│   └── test_old_mail.py
└── conftest.py   # 공통 fixture
```

---

## 테스트 구조 (필수 준수)

```python
import pytest
from utils.query_builder import build_older_than_query


class TestBuildOlderThanQuery:
    """build_older_than_query 함수 테스트"""

    def test_기본_쿼리_생성(self):
        result = build_older_than_query(days=30)
        assert result == "older_than:30d"

    def test_라벨_포함_쿼리(self):
        result = build_older_than_query(days=14, label="INBOX")
        assert "older_than:14d" in result
        assert "label:INBOX" in result

    class TestEdgeCases:
        def test_0일_입력(self):
            result = build_older_than_query(days=0)
            assert result == "older_than:0d"

        def test_빈_라벨_무시(self):
            result = build_older_than_query(days=30, label="")
            assert "label:" not in result
```

---

## 테스트 케이스 도출

| 카테고리 | 설명 | 예시 |
|----------|------|------|
| 정상 케이스 | 일반적인 유효 입력 | `build_older_than_query(30)` |
| 경계값 | 0, 빈 문자열, None | `build_older_than_query(0)` |
| 에러 케이스 | 음수, 잘못된 타입 | `build_older_than_query(-1)` |
| 정책 케이스 | 비즈니스 규칙 | Gmail 쿼리 문법 정확성 |

---

## Gmail API 목킹

실제 API 호출은 테스트에서 항상 목킹한다:

```python
from unittest.mock import MagicMock, patch
import pytest


@pytest.fixture
def mock_service():
    service = MagicMock()
    # messages().list().execute() 체인 설정
    service.users().messages().list().execute.return_value = {
        "messages": [{"id": "abc123"}, {"id": "def456"}],
        "resultSizeEstimate": 2,
    }
    return service


class TestCollectMessageIds:
    def test_메시지_id_수집(self, mock_service):
        from utils.batch import collect_message_ids

        ids = collect_message_ids(mock_service, query="older_than:30d")
        assert ids == ["abc123", "def456"]

    def test_빈_결과_처리(self, mock_service):
        mock_service.users().messages().list().execute.return_value = {}

        from utils.batch import collect_message_ids

        ids = collect_message_ids(mock_service, query="nothing")
        assert ids == []
```

---

## conftest.py 패턴

```python
# tests/conftest.py
import pytest
from unittest.mock import MagicMock


@pytest.fixture
def mock_gmail_service():
    """Gmail API 서비스 목 객체"""
    return MagicMock()


@pytest.fixture
def sample_message_ids():
    return ["id001", "id002", "id003"]
```

---

## 금지 사항

- **실제 Gmail API 호출 금지** — 모든 API 호출은 `MagicMock` 또는 `patch`로 목킹
- **실제 토큰/자격증명 사용 금지** — 테스트에 credentials.json 절대 포함 금지
- **테스트 간 상태 공유 금지** — 각 테스트는 독립적으로 실행 가능해야 함
- **하드코딩된 이메일/계정 정보 금지** — fixture로 추상화

---

## 테스트 실행

```bash
# 전체 테스트
pytest

# 특정 파일
pytest tests/utils/test_query_builder.py

# 특정 클래스/함수
pytest tests/utils/test_query_builder.py::TestBuildOlderThanQuery

# 상세 출력
pytest -v

# 커버리지
pytest --cov=utils --cov=cleaner --cov-report=term-missing
```

---

## 체크리스트

- [ ] 정상 케이스 포함?
- [ ] 경계값 (0, 빈 문자열, None) 포함?
- [ ] Gmail API 호출을 목킹했는가?
- [ ] fixture를 conftest.py에 정의했는가?
- [ ] 테스트가 독립적으로 실행 가능한가?
