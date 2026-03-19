---
name: bug-fix
description: 버그 분석 및 수정. "버그", "오류", "에러", "동작 안함", "왜 안되지", 에러 메시지/스택트레이스가 제공될 때 반드시 이 스킬을 활성화. 2-3가지 해결 옵션 제시 후 구현.
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, Edit
metadata:
  version: "1.0.0"
---

# Bug Fix Skill

> 버그를 분석하고 2-3가지 해결 옵션을 제시한 후 선택된 방법으로 수정

---

## 트리거 조건

| 트리거                        | 반응        |
| ----------------------------- | ----------- |
| "버그", "오류", "에러"        | 스킬 활성화 |
| 에러 메시지/스택트레이스 제공 | 분석 시작   |
| "동작 안함", "이상해"         | 스킬 활성화 |

---

## 사용 시점

| 상황            | 예시                                              |
| --------------- | ------------------------------------------------- |
| **타입 에러**   | Property 'X' does not exist on type 'Y'           |
| **런타임 에러** | Cannot read property of undefined, null reference |
| **논리 오류**   | 중복 렌더링, 잘못된 계산, 상태 관리 이슈          |
| **API 에러**    | 500 에러, 잘못된 응답, CORS 문제                  |
| **간헐적 버그** | 특정 조건에서만 발생                              |

---

## ARGUMENT 확인

```
$ARGUMENTS 없음 → 즉시 질문:

"어떤 버그를 수정해야 하나요? 구체적으로 알려주세요.

예시:
- 에러 메시지 및 발생 위치
- 예상 동작 vs 실제 동작
- 재현 방법
- 관련 파일 경로"

$ARGUMENTS 있음 → 다음 단계 진행
```

---

## 복잡도 판단

| 복잡도     | 기준                              | 접근                   |
| ---------- | --------------------------------- | ---------------------- |
| **LOW**    | 단일 파일, 명확한 에러, 재현 쉬움 | 바로 수정              |
| **MEDIUM** | 2-3개 파일, 원인 후보 2-3개       | 옵션 제시              |
| **HIGH**   | 5개+ 파일, 근본 원인 불명/간헐적  | 상세 분석 후 옵션 제시 |

> 복잡도가 불확실하면 한 단계 높게 판단.

---

## 실행 흐름

| 단계 | 작업           | 도구                   |
| ---- | -------------- | ---------------------- |
| 1    | 입력 확인      | -                      |
| 2    | 복잡도 판단    | sequential-thinking.md |
| 3    | 버그 재현/탐색 | Read/Grep/Glob         |
| 4    | 원인 분석      | Task (Explore)         |
| 5    | 옵션 도출      | 분석 결과 기반         |
| 6    | 옵션 제시/선택 | -                      |
| 7    | 구현           | Edit                   |
| 8    | 검증           | Bash                   |

---

## 워크플로우

### Phase 1: 증상 파악

```typescript
// 에러 관련 파일 탐색
Task(
  (subagent_type = "explore"),
  (model = "haiku"),
  (prompt = `
  에러 증상: {에러 메시지}
  관련 키워드로 코드베이스 검색
`),
);
```

**수집 항목:**

- 에러 메시지 전문
- 스택 트레이스 (가능하면 전체)
- 발생 조건 (재현 단계)
- 관련 파일/함수
- 최근 변경 내역 (`git log`)

---

### Phase 2: 원인 분석

**분석 체크리스트:**

- [ ] 타입 에러인가? (TypeScript)
- [ ] 런타임 에러인가? (null/undefined)
- [ ] 로직 에러인가? (조건문, 계산)
- [ ] 상태 관리 이슈인가? (Query, Atom)
- [ ] API 응답 이슈인가? (네트워크)
- [ ] 재현 조건이 명확한가? (항상 vs 간헐적)

**탐색 명령:**

```bash
# 에러 키워드 검색
rg "{에러키워드}" src/

# 최근 변경 확인
git log --oneline -10 -- {관련파일}

# git diff로 변경 내용 확인
git diff HEAD~5 -- {관련파일}
```

**런타임 에러 추가 체크:**

- null/undefined 경로 (초기 상태, 비동기 타이밍)
- 데이터 흐름 중 누락되는 값
- 가드(early return) 또는 optional chaining 필요 여부

**탐색 체크리스트:**

- 에러 발생 정확한 위치
- 관련 함수/컴포넌트 호출 체인
- 상태/데이터 흐름
- 외부 의존성 (라이브러리, API)
- 최근 변경 사항 (git log/blame)

---

### Phase 3: 해결 옵션 제시

**반드시 2-3가지 옵션 제시:**

```markdown
## 버그 분석 결과

### 증상

{증상 설명}

### 원인

{근본 원인 분석}

### 해결 옵션

| #   | 방법    | 장점   | 단점   | 영향 범위 |
| --- | ------- | ------ | ------ | --------- |
| 1   | {방법1} | {장점} | {단점} | {파일 수} |
| 2   | {방법2} | {장점} | {단점} | {파일 수} |
| 3   | {방법3} | {장점} | {단점} | {파일 수} |

### 권장

{권장 옵션 번호} - {이유}

어떤 방법으로 수정할까요? [1/2/3]
```

**옵션 작성 시 포함:**

- 리스크 (상/중/하)
- 수정 파일과 라인 (가능하면)
- 임시 해결 vs 근본 해결 구분

---

### Phase 4: 수정 구현

선택된 옵션에 따라 수정 (사용자 선택 후 진행):

> **패키지 매니저**: lock 파일 기준 자동 감지 — `yarn.lock` → yarn, `pnpm-lock.yaml` → pnpm, `package-lock.json` → npm (없으면 npm)

```typescript
// 수정 전 테스트 확인
Bash("{패키지매니저} test -- --testPathPattern='{관련테스트}'");

// 수정 적용
Edit("{파일}", "{old_string}", "{new_string}");

// 린트/타입 검증
Bash("{패키지매니저} lint");
Bash("{패키지매니저} build");
```

---

### Phase 5: 검증

**검증 체크리스트:**

- [ ] 원래 에러가 해결되었는가?
- [ ] 새로운 에러가 발생하지 않았는가?
- [ ] 기존 동작이 유지되는가?
- [ ] 린트/빌드 통과하는가?
- [ ] 관련 테스트 통과하는가?

**검증 명령 예시:**

```bash
{패키지매니저} lint
{패키지매니저} tsc --noEmit
{패키지매니저} test -- --testPathPattern="{관련 테스트}"
```

---

## 병렬 실행 패턴

### Agent Teams 우선 원칙

- Agent Teams 가용 시 TeamCreate로 팀 구성 → 병렬 협업
- 미가용 시 Task 병렬 호출로 폴백
- 같은 파일 동시 수정은 금지 (충돌 위험)

### Agent Teams 모드

복잡한 버그 (HIGH) 분석 시 팀 기반 병렬 협업:

```typescript
TeamCreate({ team_name: "bugfix-team", description: "버그 분석 및 수정" });
Task(
  (subagent_type = "explore"),
  (team_name = "bugfix-team"),
  (name = "root-cause"),
  (model = "sonnet"),
  (prompt = "근본 원인 분석"),
);
Task(
  (subagent_type = "explore"),
  (team_name = "bugfix-team"),
  (name = "impact-check"),
  (model = "haiku"),
  (prompt = "영향 범위 파악"),
);
// 완료 후 → shutdown_request → TeamDelete
```

### Task 병렬 모드 (폴백)

독립적인 버그 수정은 병렬로:

```typescript
Task(
  (subagent_type = "lint-fixer"),
  (model = "haiku"),
  (prompt = "파일1 린트 에러 수정"),
);
Task(
  (subagent_type = "lint-fixer"),
  (model = "haiku"),
  (prompt = "파일2 린트 에러 수정"),
);
```

### 심각도별 병렬 전략

| 심각도          | 전략                                 |
| --------------- | ------------------------------------ |
| **CRITICAL**    | 즉시 수정(순차) + 영향도 분석만 병렬 |
| **HIGH/MEDIUM** | 독립 버그는 병렬 수정                |

---

## 금지 패턴

| 금지                  | 이유          |
| --------------------- | ------------- |
| 원인 파악 없이 수정   | 재발 위험     |
| 단일 옵션만 제시      | 선택권 없음   |
| 사용자 선택 없이 수정 | 요구 불일치   |
| 테스트 삭제로 해결    | 품질 저하     |
| 정책 임의 변경        | 비즈니스 영향 |

---

## 정책 영향 버그

**비즈니스 정책 관련 버그 수정 시:**

```typescript
// 기존 동작 캡처 테스트 작성
describe("버그 수정 후 정책 유지", () => {
  it("기존 정책이 그대로 동작해야 함", () => {
    // 수정 전 동작 테스트
  });
});
```

---

## 완료 전 출시 게이트

수정 완료 후 `release-readiness-gate.md` 5개 게이트를 점검한다.
하나라도 FAIL이면 원인 정리 후 수정하고 재검증한다.

---

## 참조 문서

| 문서                                                           | 용도        |
| -------------------------------------------------------------- | ----------- |
| `@../../instructions/workflow-patterns/sequential-thinking.md` | 복잡도 판단 |
| `@../../instructions/multi-agent/coordination-guide.md`        | 병렬 협업   |
| `@../../instructions/multi-agent/execution-patterns.md`        | 실행 패턴   |
| `@../../instructions/validation/forbidden-patterns.md`         | 금지 패턴   |
| `@../../instructions/validation/release-readiness-gate.md`     | 출시 게이트 |
| `@../../rules/core/unit-test-conventions.md`                   | 테스트 규칙 |
