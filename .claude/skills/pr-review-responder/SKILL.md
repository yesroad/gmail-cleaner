---
name: pr-review-responder
description: PR 리뷰 코멘트 분석 및 대응. "리뷰 반영", "코멘트 처리", "리뷰어 피드백", PR 번호/URL이 제공될 때 이 스킬을 활성화. 수용/거절/질문으로 분류 후 수용 항목 자동 구현.
user-invocable: true
allowed-tools: Bash, Read, Edit, Grep, Glob
metadata:
  version: "1.0.0"
  category: development
  priority: high
---

# PR Review Responder

> PR 리뷰 코멘트를 분류하고, 수용 항목을 체계적으로 반영

---

## 트리거 조건

| 트리거 | 반응 |
|--------|------|
| "리뷰 반영해줘", "코멘트 처리" | 스킬 활성화 |
| PR 번호/URL 제공 | 코멘트 자동 조회 |
| 리뷰 코멘트 직접 붙여넣기 | 분류 시작 |

---

## ARGUMENT 확인

```
$ARGUMENTS 없음 → 질문:
"어떤 PR의 리뷰를 반영할까요?
- PR 번호 (예: 42)
- PR URL
- 또는 리뷰 코멘트를 직접 붙여넣기"

$ARGUMENTS 있음 → 다음 단계 진행
```

---

## 워크플로우

### Phase 1: 리뷰 코멘트 수집

**PR 번호/URL 제공 시 (gh CLI 사용):**

```bash
# PR 코멘트 조회
gh pr view {PR번호} --comments

# 리뷰 코멘트(인라인) 조회
gh api repos/{owner}/{repo}/pulls/{PR번호}/reviews
gh api repos/{owner}/{repo}/pulls/{PR번호}/comments
```

**직접 붙여넣기 시:** 제공된 텍스트를 그대로 사용

---

### Phase 2: 코멘트 분류

각 코멘트를 아래 3가지로 분류:

| 분류 | 기준 | 처리 |
|------|------|------|
| ✅ **수용** | 버그, 명백한 개선, 컨벤션 위반 | 즉시 구현 |
| ❌ **거절** | 스코프 밖, 의도된 설계, 주관적 취향 | 근거 정리 |
| ❓ **질문** | 의도 불명확, 추가 맥락 필요 | 확인 후 결정 |

**분류 출력 형식:**

```markdown
## 리뷰 코멘트 분류

### ✅ 수용 (N개)
1. [파일:라인] 코멘트 내용 → 수용 이유
2. ...

### ❌ 거절 (N개)
1. [파일:라인] 코멘트 내용 → 거절 이유

### ❓ 질문 (N개)
1. 코멘트 내용 → 확인 필요 사항

수용 항목을 구현할까요? [Y/n]
```

---

### Phase 3: 수용 항목 구현

사용자 확인 후 수용 항목 구현:

**파일별 그룹화 후 순차 처리:**

```typescript
// 같은 파일 수정은 한 번에 처리
Task(subagent_type="explore", model="haiku", prompt="변경 대상 파일 분석")
```

**구현 순서:**
1. 단순 변경 (네이밍, 타입) → 즉시 수정
2. 로직 변경 → 영향 범위 확인 후 수정
3. 구조 변경 → 계획 수립 후 단계적 수정

---

### Phase 4: 거절 코멘트 응답 초안 작성

리뷰어에게 전달할 응답 초안 생성:

```markdown
## PR 리뷰 응답 초안

### 반영 완료
- [파일:라인] {변경 내용 요약}

### 미반영 (의견 있음)
- {코멘트 내용}: {거절 이유 및 대안}

### 추가 확인 필요
- {코멘트 내용}: {질문 내용}
```

---

### Phase 5: 검증

구현 완료 후:

> **패키지 매니저**: lock 파일 기준 자동 감지 — `yarn.lock` → yarn, `pnpm-lock.yaml` → pnpm, `package-lock.json` → npm (없으면 npm)

```bash
# 린트/타입 체크
{패키지매니저} lint
{패키지매니저} tsc --noEmit

# 관련 테스트
{패키지매니저} test -- --testPathPattern="{관련 파일}"
```

---

## 금지 패턴

| 금지 | 이유 |
|------|------|
| 모든 코멘트 무조건 수용 | 설계 의도 훼손 가능 |
| 거절 시 응답 없이 무시 | 리뷰어와 소통 단절 |
| 사용자 확인 없이 대규모 변경 | 의도치 않은 변경 위험 |
| 리뷰와 무관한 추가 수정 | 스코프 크립 |

---

## 완료 전 출시 게이트

`release-readiness-gate.md` 5개 게이트 점검 후 커밋.

---

## 참조 문서

| 문서 | 용도 |
|------|------|
| `@../../skills/commit-helper/SKILL.md` | 커밋 메시지 생성 |
| `@../../skills/code-quality/SKILL.md` | 린트/타입 검증 |
| `@../../instructions/validation/release-readiness-gate.md` | 출시 게이트 |
