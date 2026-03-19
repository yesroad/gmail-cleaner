# Gmail Cleaner

Gmail 계정의 메일을 대화형 CLI로 정리하는 Python 도구.

## 프로젝트 개요

- **언어**: Python 3.x
- **주요 라이브러리**: `google-api-python-client`, `rich`, `questionary`
- **인증**: Google OAuth 2.0 (다중 계정 지원)
- **실행**: `python main.py`

## 디렉토리 구조

```
gmail-cleaner/
├── main.py          # 진입점 + 6가지 작업 플로우 (flow_*)
├── auth.py          # OAuth 인증 + 다중 계정 토큰 관리
├── cleaner/         # BaseCleaner 추상 클래스 + 구현체들
│   ├── base.py      # preview() / execute() 인터페이스
│   ├── spam_promo.py, unread.py, sender.py
│   └── old_mail.py, large_mail.py, label.py
├── ui/              # 터미널 UI
│   ├── console.py   # Rich 기반 출력 (헤더, 메시지, 테이블)
│   ├── menu.py      # questionary 대화형 메뉴
│   └── progress.py  # 진행률 바
├── utils/           # 순수 유틸리티
│   ├── query_builder.py  # Gmail 쿼리 문자열 생성
│   └── batch.py          # Gmail API 배치 처리
└── requirements.txt
```

## 핵심 아키텍처

**BaseCleaner 패턴**: 새 정리 기능 추가 시 `cleaner/base.py`를 상속하고 `build_query()` + `execute()` 구현.

**플로우 구조** (`main.py`):
```
계정 선택 → 작업 선택 → preview(건수 확인) → 사용자 확인 → execute(진행률 표시)
```

**다중 계정 토큰**: `token_{safe_email}.json` + `token_{safe_email}.meta.json` 쌍으로 관리.

## 개발 도구

```bash
# 의존성 설치
pip install -r requirements.txt

# 실행
python main.py

# 린트/포맷 (ruff)
ruff check .
ruff format .

# 타입 체크 (mypy)
mypy .

# 테스트 (pytest)
pytest
pytest tests/utils/test_query_builder.py  # 특정 파일
```

## 코딩 규칙 참조

- `.claude/rules/core/coding-standards.md` — Python 코딩 표준
- `.claude/rules/core/unit-test-conventions.md` — pytest 테스트 규칙
- `.claude/rules/core/thinking-model.md` — 사고 모델

## 보안 주의사항

- `credentials.json`, `token_*.json` 파일은 절대 커밋하지 않는다 (`.gitignore` 적용됨)
- OAuth 스코프는 최소 권한 원칙 (`gmail.modify`만 사용)
