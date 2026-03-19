---
name: refactor
description: 코드 리팩토링 분석 및 실행. "리팩토링", "구조 개선", "중복 제거", "분리", "정리", "클린업"이 언급될 때 이 스킬을 활성화. 정책 보호 테스트 포함.
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
metadata:
  version: "1.0.0"
---

# Refactor Skill

> 기존 정책을 보호하면서 코드 구조 개선

---

## 트리거 조건

| 트리거                       | 반응        |
| ---------------------------- | ----------- |
| "리팩토링", "구조 개선"      | 스킬 활성화 |
| "중복 제거", "분리"          | 스킬 활성화 |
| 코드 리뷰에서 구조 개선 제안 | 분석 시작   |

---

## 핵심 원칙

| 원칙            | 설명                         |
| --------------- | ---------------------------- |
| **정책 보호**   | 비즈니스 로직 동작 유지      |
| **점진적**      | 작은 단위로 단계적 진행      |
| **테스트 우선** | 리팩토링 전 정책 테스트 작성 |
| **최소 변경**   | 불필요한 개선 지양           |

---

## 복잡도 판단

| 복잡도     | 기준                     | 접근               |
| ---------- | ------------------------ | ------------------ |
| **LOW**    | 변수명 변경, 단순 추출   | 바로 실행          |
| **MEDIUM** | 함수 분리, 파일 구조화   | 계획 후 실행       |
| **HIGH**   | 아키텍처 변경, 패턴 도입 | Plan 에이전트 활용 |

---

## 워크플로우

### Phase 1: 현황 분석

**Agent Teams 모드:**

```typescript
TeamCreate({
  team_name: "refactor-team",
  description: "리팩토링 분석 및 실행",
});
Task(
  (subagent_type = "explore"),
  (team_name = "refactor-team"),
  (name = "code-analyzer"),
  (model = "haiku"),
  (prompt = "리팩토링 대상 코드 분석"),
);
Task(
  (subagent_type = "explore"),
  (team_name = "refactor-team"),
  (name = "test-checker"),
  (model = "haiku"),
  (prompt = "관련 테스트 현황 파악"),
);
Task(
  (subagent_type = "explore"),
  (team_name = "refactor-team"),
  (name = "dep-analyzer"),
  (model = "haiku"),
  (prompt = "의존성 파일 목록 추출"),
);
// 완료 후 → shutdown_request → TeamDelete
```

**Task 병렬 모드 (폴백):**

```typescript
Task(
  (subagent_type = "explore"),
  (model = "haiku"),
  (prompt = "리팩토링 대상 코드 분석"),
);
Task(
  (subagent_type = "explore"),
  (model = "haiku"),
  (prompt = "관련 테스트 현황 파악"),
);
Task(
  (subagent_type = "explore"),
  (model = "haiku"),
  (prompt = "의존성 파일 목록 추출"),
);
```

**수집 항목:**

- 현재 코드 구조
- 문제점 (중복, 복잡도, 책임 분리)
- 영향 받는 파일 목록
- 기존 테스트 유무

---

### Phase 2: 리팩토링 계획

**HIGH 복잡도 시 Plan 에이전트 활용:**

```typescript
Task(
  (subagent_type = "Plan"),
  (model = "opus"),
  (prompt = `
  대상: {리팩토링 대상}
  목표: {개선 목표}
  제약: 기존 정책 유지

  단계별 계획 수립 요청
`),
);
```

**계획 템플릿:**

```markdown
## 리팩토링 계획

### 목표

{한 문장}

### 현재 문제

- {문제1}
- {문제2}

### 변경 계획

| #   | 단계   | 파일   | 리스크     |
| --- | ------ | ------ | ---------- |
| 1   | {작업} | {파일} | {상/중/하} |
| 2   | {작업} | {파일} | {상/중/하} |

### 정책 보호 항목

- {보호할 정책1}
- {보호할 정책2}

### 롤백 전략

{실패 시 복구 방법}
```

---

### Phase 3: 정책 보호 테스트 작성

**리팩토링 전 반드시 테스트 작성:**

```typescript
// 정책 함수에 대한 테스트
describe("리팩토링 전 정책 캡처", () => {
  beforeAll(() => {
    jest.useFakeTimers().setSystemTime(new Date("2025-01-15"));
  });

  // 현재 동작을 "캡처"
  it("formatDate: 유효한 날짜 포맷 정책", () => {
    expect(formatDate(new Date("2025-01-15"))).toBe("2025-01-15");
  });

  it("clamp: 범위 초과 시 최댓값 반환 정책", () => {
    expect(clamp(11, 0, 10)).toBe(10);
  });
});
```

**테스트 대상:**

- 날짜/기간 계산
- 가격/할인 계산
- 필터 조건
- disabled/readonly 조건
- 기본값/초기값

---

### Phase 4: 단계적 실행

**작은 단위로 실행:**

> **패키지 매니저**: lock 파일 기준 자동 감지 — `yarn.lock` → yarn, `pnpm-lock.yaml` → pnpm, `package-lock.json` → npm (없으면 npm)

```typescript
// 1단계: 함수 추출
Edit("파일.ts", "{원본코드}", "{추출된함수호출}");
Write("utils/extracted.ts", "{추출된함수}");

// 테스트 실행 (앱 test 스크립트가 있을 때)
Bash("{패키지매니저} test -- --testPathPattern='정책'");

// 2단계: 다음 리팩토링
// ...
```

**각 단계 후:**

- [ ] 린트 통과
- [ ] 빌드 통과
- [ ] 정책 테스트 통과
- [ ] 기존 테스트 통과

---

### Phase 5: 검증

```typescript
// 병렬 검증
Task(
  (subagent_type = "lint-fixer"),
  (model = "haiku"),
  (prompt = "린트 오류 수정"),
);
Task((subagent_type = "code-reviewer"), (prompt = "리팩토링 결과 리뷰"));
```

**최종 체크:**

- [ ] 모든 정책 테스트 통과
- [ ] 린트/빌드 통과
- [ ] 코드 리뷰 통과
- [ ] 기능 동작 확인

---

## 금지 패턴

| 금지                 | 이유                |
| -------------------- | ------------------- |
| 테스트 없이 리팩토링 | 정책 변경 감지 불가 |
| 한 번에 큰 변경      | 롤백 어려움         |
| 정책 임의 변경       | 비즈니스 영향       |
| 불필요한 추상화      | 복잡도 증가         |

---

## 리팩토링 판단 기준

| 리팩토링 필요         | 리팩토링 불필요  |
| --------------------- | ---------------- |
| 동일 로직 3곳+ 중복   | 1-2곳 유사 코드  |
| 명백한 책임 분리 위반 | 단순 가독성 개선 |
| 테스트 불가능한 구조  | 취향 차이 수준   |
| 500줄+ 파일           | 200줄 이하 파일  |

---

## 완료 전 출시 게이트

최종 결과는 `release-readiness-gate.md` 5개 게이트를 모두 통과해야 한다.
통과 전에는 커밋/PR을 진행하지 않는다.

---

## 참조 문서

| 문서                                                           | 용도             |
| -------------------------------------------------------------- | ---------------- |
| `@../../instructions/workflow-patterns/sequential-thinking.md` | 복잡도 판단      |
| `@../../instructions/multi-agent/agent-roster.md`              | Plan 에이전트    |
| `@../../instructions/validation/release-readiness-gate.md`     | 출시 게이트      |
| `@../../rules/core/unit-test-conventions.md`                   | 테스트 규칙      |
| `@../../rules/core/thinking-model.md`                          | RESTRUCTURE 단계 |
