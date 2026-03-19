---
name: quality
description: 린트 → 포맷 → 타입 체크 순서로 실행하고 오류 자동 수정.
---

**[즉시 실행]** 아래 순서대로 코드 품질 검사를 수행한다.

**옵션**: $ARGUMENTS

| 옵션 | 설명 |
|------|------|
| `--lint-only` | 린트(ruff)만 실행 |
| `--type-only` | 타입 체크(mypy)만 실행 |
| `--no-fix` | 자동 수정 없이 오류 목록만 출력 |

---

## 실행 순서

### 1. 린트 + 포맷 (ruff)

```bash
# 자동 수정 포함
ruff check . --fix
ruff format .
```

수정 불가 오류가 있으면 목록을 출력하고 수동 수정을 안내한다.

### 2. 타입 체크 (mypy)

```bash
mypy .
```

타입 오류가 있으면 목록을 출력하고 수정한다.

### 3. 결과 요약

```
✅ ruff: 통과 (N개 자동 수정)
✅ mypy: 통과
```

또는

```
❌ mypy: 3개 오류
  main.py:42: error: Argument 1 to "execute" has incompatible type ...
```
