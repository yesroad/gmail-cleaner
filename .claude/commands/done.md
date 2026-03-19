---
name: done
description: 작업 완료 후 검증 → 테스트 → 커밋 → PR 생성까지 전체 플로우 수행.
---

# /done - 작업 완료 및 PR 생성

구현 완료 후 사용합니다. 검증 → 테스트 → 커밋 → PR 생성 → 정리까지 전체 플로우를 수행합니다.

**참조 규칙**:

- `@../rules/core/unit-test-conventions.md` (유닛 테스트)
- `@../skills/commit-helper/SKILL.md` (커밋 메시지 생성)
- `@../skills/code-quality/SKILL.md` (린트/포맷/타입 체크)
- `@../instructions/validation/release-readiness-gate.md` (출시 품질 게이트)

## 사용법

```
/done
```

---

## 완료 조건 (빠른 참조)

> 모든 항목이 체크되어야 완료로 간주한다.

- [ ] 변경 내용 분석 완료 (정책 영향 여부 판단 포함)
- [ ] 테스트 전략 결정 및 실행/스킵 완료 (사유 명시)
- [ ] ruff / mypy 통과
- [ ] 출시 품질 게이트 9개 항목 PASS
- [ ] 이번 작업 파일만 선별하여 커밋 생성
- [ ] PR 생성 및 URL 출력

---

## 수행 작업

### 1. 변경 내용 분석

```bash
git status
git diff --staged
git diff
```

**분석 항목:**

- 변경된 파일 목록
- 주요 변경 내용 요약
- 정책 영향 여부 판단 (아래 기준표 참조)

---

### 2. 테스트 전략 판단

> **의도치 않은 정책 변경**을 방지하기 위한 테스트 전략

#### 2-1. 변경 파일 분류

| 경로 패턴                                 | 분류      | 테스트 도구          |
| ----------------------------------------- | --------- | -------------------- |
| `utils/`, `helpers/`, `lib/`, `adapters/` | 순수 함수 | **Claude 직접 작성** |
| `styled.ts`, `constants.ts`, `types.ts`   | UI/타입   | 스킵                 |

#### 2-2. 정책 영향 판단 기준

| 변경 내용           | 대상 유형 | 테스트 전략 | 도구            |
| ------------------- | --------- | ----------- | --------------- |
| 날짜/기간 계산 변경 | 순수 함수 | 유닛 테스트 | **Claude 직접** |
| 계산/변환 로직 변경 | 순수 함수 | 유닛 테스트 | **Claude 직접** |
| 상태 전이 로직 변경 | 순수 함수 | 유닛 테스트 | **Claude 직접** |
| 텍스트/라벨 변경    | UI only   | 스킵        | -               |
| 스타일/레이아웃     | UI only   | 스킵        | -               |

#### 2-3. 정책 키워드 탐지

Grep 도구로 변경된 파일에서 비즈니스 로직 키워드를 검색한다:

- 패턴: `(calculate|compute|format)` → 계산/변환 로직
- 패턴: `(disabled|isDisabled|readonly)` → 상태 제어 정책
- 패턴: `(filter|sort|defaultValue|initialValue)` → 목록/기본값 정책

---

### 3. 테스트 실행

#### Case A: 순수 함수 + 정책 영향 → Claude 직접 유닛 테스트 작성

```
ℹ️ 순수 함수 변경이 감지되었습니다. 유닛 테스트를 작성합니다.

실행:
1. 대상 파일 분석
2. `.claude/rules/core/unit-test-conventions.md` 규칙 참조
3. tests/{모듈}/test_{파일명}.py 생성
4. pytest 실행
```

#### Case B: 기존 테스트 있음 → 실행만

```bash
pytest tests/{관련 테스트 경로}
```

#### Case C: UI only (정책 무관) → 스킵

---

### 4. 코드 검증

`code-quality` 스킬을 실행하여 포맷 → 린트 → 타입 체크를 순서대로 수행한다.

> `@../skills/code-quality/SKILL.md` 규칙에 따라 실행

- Prettier: 자동 포맷 적용
- ESLint: `--fix`로 자동 수정
- 타입 체크: 오류 목록 출력 및 수동 수정 안내

**모두 PASS 후 다음 단계 진행.**

---

### 4-1. 출시 품질 게이트 검토 (필수)

커밋 전 아래 항목을 반드시 점검:

- 계획 검토/재검토가 타당한가?
- 구현이 목적과 정확히 맞는가?
- 잠재 버그/크리티컬/보안 이슈는 없는가?
- 개선 내용에 회귀나 사이드 이펙트는 없는가?
- 큰 함수/파일은 분리됐는가?
- 재사용/통합 가능한 기존 코드를 활용했는가?
- 불필요 코드가 정리됐는가?
- 사용자 흐름에서 막히는 구간은 없는가?
- "지금 배포 가능한가?" 질문에 근거로 답할 수 있는가?

**하나라도 FAIL이면 커밋/PR 진행 금지.**

---

### 5. 커밋 생성

#### ⚠️ 중요: 이번 작업에서 수정한 파일만 커밋

```bash
# ❌ 절대 금지
git add .
git add -A

# ✅ 올바른 방법
git add {수정한 파일 경로}
```

**커밋 전 확인:**

```bash
git diff --staged --name-only

# 불필요한 파일 포함 시
git reset HEAD {제외할 파일}
```

**커밋 메시지**: `commit-helper` 스킬로 생성한다.

> `@../skills/commit-helper/SKILL.md` 규칙에 따라 커밋 메시지를 생성하고 커밋한다.

---

### 6. PR 생성 (GitHub)

```bash
git push -u origin {현재브랜치}
gh pr create \
  --title "{type}: {제목}" \
  --body "$(cat <<'EOF'
## 작업 내용

- {변경 내용 bullet points}

## 디자인 (optional)

{디자인 URL (있는 경우)}

## 특이사항 (optional)

-
EOF
)"
```

**사전 준비:**

```bash
# gh CLI 설치 (최초 1회)
brew install gh

# GitHub 인증 (최초 1회)
gh auth login
```

---

### 7. 정리

작업 중 생성한 임시 파일이나 스크린샷이 있으면 정리한다.

---

### 8. 최종 요약 출력

```markdown
## ✅ 작업 완료

### 검증 결과

- [x] ruff check + format
- [x] mypy
- [x] 테스트 {통과/스킵}

### 커밋

- {커밋 해시}: {커밋 메시지}

### PR

- URL: {PR URL}
- 상태: Open

### 다음 단계

1. 코드 리뷰 반영
2. 머지
```

---

## 옵션

| 옵션           | 설명                            | 사용 예시            |
| -------------- | ------------------------------- | -------------------- |
| `--skip-test`  | 테스트 스킵 (정책 무관 확인 후) | `/done --skip-test`  |
| `--force-test` | 정책 무관이어도 테스트 강제실행 | `/done --force-test` |
| `--draft`      | Draft PR로 생성                 | `/done --draft`      |

---

## 완료 조건

- [ ] 변경 내용 분석 완료
- [ ] 테스트 전략 판단됨
- [ ] 테스트 실행/스킵 완료 (사유 명시)
- [ ] Prettier/lint/타입 체크 통과
- [ ] 커밋 생성됨
- [ ] PR 생성됨 (URL 출력)
- [ ] 최종 요약 출력됨
