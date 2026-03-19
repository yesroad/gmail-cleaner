# Multi-Agent Coordination Guide

> 멀티 에이전트 병렬 실행으로 작업 효율 극대화

---

## 핵심 원칙

| 원칙           | 방법                                  | 효과               |
| -------------- | ------------------------------------- | ------------------ |
| **TEAM FIRST** | 복잡한 병렬 작업은 Agent Teams 우선   | 협업 + 수명주기    |
| **PARALLEL**   | 독립 작업은 단일 메시지에서 동시 호출 | 5-10배 속도 향상   |
| **BACKGROUND** | 긴 작업은 백그라운드로 실행           | 메인 컨텍스트 보호 |
| **DELEGATE**   | 전문 에이전트에 즉시 위임             | 품질 향상          |

```typescript
// ❌ 순차 실행 (120초)
Task((subagent_type = "explore"), (prompt = "파일 구조 분석")); // 60초
Task((subagent_type = "explore"), (prompt = "API 패턴 분석")); // 60초

// ✅ 병렬 실행 (60초) - 단일 메시지에서 호출
Task(
  (subagent_type = "explore"),
  (model = "haiku"),
  (prompt = "파일 구조 분석"),
);
Task(
  (subagent_type = "explore"),
  (model = "haiku"),
  (prompt = "API 패턴 분석"),
);
```

---

## Agent Teams 우선 원칙

> 일반 플랜에서는 기존 Task 병렬 호출로 자동 폴백

### 적용 기준

| 조건                      | 실행 방식                     |
| ------------------------- | ----------------------------- |
| 3개+ 에이전트 병렬 협업   | **Agent Teams** (TeamCreate)  |
| 에이전트 간 통신 필요     | **Agent Teams** (SendMessage) |
| 2개 이하 독립 작업        | Task 병렬 호출 (팀 불필요)    |
| Agent Teams 미가용 (플랜) | Task 병렬 호출 (폴백)         |

### Agent Teams 모드 (기본)

```typescript
// 1. 팀 생성
TeamCreate({ team_name: "analysis-team", description: "코드 분석 및 리뷰" });

// 2. 팀원 spawn (병렬)
Task(
  (subagent_type = "explore"),
  (team_name = "analysis-team"),
  (name = "code-analyzer"),
  (model = "haiku"),
  (prompt = "코드 구조 분석"),
);
Task(
  (subagent_type = "explore"),
  (team_name = "analysis-team"),
  (name = "pattern-checker"),
  (model = "haiku"),
  (prompt = "패턴 분석"),
);
Task(
  (subagent_type = "code-reviewer"),
  (team_name = "analysis-team"),
  (name = "reviewer"),
  (model = "sonnet"),
  (prompt = "코드 리뷰"),
);
```

### 수명주기 관리 (필수)

| 단계     | 작업                                          |
| -------- | --------------------------------------------- |
| **생성** | TeamCreate → TaskCreate → Task(team_name=...) |
| **협업** | SendMessage로 팀원 간 통신                    |
| **완료** | 팀원 태스크 완료 → shutdown_request 전송      |
| **정리** | 모든 팀원 종료 확인 → TeamDelete로 팀 해산    |

### 폴백 모드 (Agent Teams 미가용 시)

```typescript
// Agent Teams 없이 병렬 실행
Task(
  (subagent_type = "explore"),
  (model = "haiku"),
  (prompt = "코드 구조 분석"),
);
Task((subagent_type = "explore"), (model = "haiku"), (prompt = "패턴 분석"));
Task(
  (subagent_type = "code-reviewer"),
  (model = "sonnet"),
  (prompt = "코드 리뷰"),
);
```

### 규칙/스킬 참조 범위

팀원(서브에이전트)은 spawn 시 자동으로 프로젝트 규칙을 로드한다:

| 항목                 | 자동 로드 | 비고                           |
| -------------------- | :-------: | ------------------------------ |
| CLAUDE.md            |     O     | 프로젝트 전체 규칙             |
| .claude/rules/       |     O     | 코딩 표준, 컨벤션 등           |
| .claude/agents/\*.md |     O     | 해당 subagent_type 정의만 적용 |
| Skill 도구 (/start)  |     X     | 메인 에이전트 전용             |
| MCP 도구             |     X     | 메인 에이전트 전용             |

**제약**: Skill 도구(/start, /done 등)와 MCP 도구는 메인 에이전트에서만 사용 가능.
커스텀 에이전트(explore, lint-fixer 등)는 도구가 제한됨.

---

## 역할 기반 서브에이전트 원칙 (공용)

> Agent Teams / 일반 Task 병렬 **모두에 적용**되는 공통 원칙

### general-purpose + 역할 프롬프트

구현이 필요한 서브에이전트는 **항상 `general-purpose`로 spawn**한다.
역할별 전문 지식은 **프롬프트에서 스킬/규칙 파일 읽기를 지시**하여 주입한다.

```
general-purpose + "refactor 스킬 읽어" = 리팩토러 역할 + 전체 도구
general-purpose + "bug-fix 스킬 읽어" = 버그 수정 역할 + 전체 도구
```

**이유:**

- `explore`, `lint-fixer` 등은 Read/Grep만 가능 → 구현 불가
- `general-purpose`는 Read, Write, Edit, Bash, Grep, Glob 모두 가능
- 프롬프트에서 스킬 파일을 읽게 하면 전문 지식 + 전체 도구를 동시에 확보

### 에이전트 타입 선택 기준

| 작업 유형          | 에이전트 타입       | 이유                       |
| ------------------ | ------------------- | -------------------------- |
| 읽기 전용 탐색     | `explore`           | 빠르고 가볍다              |
| 린트/타입 수정만   | `lint-fixer`        | 규칙 기반 단순 수정        |
| 구현이 필요한 작업 | **general-purpose** | Write/Edit/Bash 필요       |
| 스킬 지식 필요     | **general-purpose** | 스킬 파일 읽기 + 구현 동시 |

### 역할별 필수 참조 파일

| 역할      | 스킬 파일                          | 규칙 파일                                                             |
| --------- | ---------------------------------- | --------------------------------------------------------------------- |
| UI 구현   | -                                  | `.claude/rules/core/react-nextjs-conventions.md`                      |
| API 연동  | -                                  | `.claude/rules/core/state-and-server-state.md`, `coding-standards.md` |
| 리팩토링  | `.claude/skills/refactor/SKILL.md` | `.claude/rules/core/unit-test-conventions.md`                         |
| 버그 수정 | `.claude/skills/bug-fix/SKILL.md`  | -                                                                     |

---

## Agent Teams 역할 템플릿

> 각 팀원이 **독립적으로 서브태스크를 처리**하는 모드
> 팀원은 Skill/MCP 사용 불가 → Read/Bash로 직접 접근

**UI 구현:**

```
Task(subagent_type='general-purpose', team_name='sprint-team', name='ui-implementor', model='sonnet',
  prompt=`
  ## 역할: UI 구현 담당
  ## 작업: {작업 내용}

  ### 사전 준비 (필수)
  1. .claude/rules/core/react-nextjs-conventions.md를 읽고 규칙을 숙지해

  ### 작업 흐름
  1. 기존 유사 컴포넌트 패턴 분석
  2. 컴포넌트 구현
  3. 검증: {패키지매니저} lint

  ### 완료 시 (필수)
  1. `.claude/instructions/multi-agent/teammate-done-process.md`를 읽고 done 프로세스 수행
`);
```

**API 연동:**

```
Task(subagent_type='general-purpose', team_name='sprint-team', name='api-integrator', model='sonnet',
  prompt=`
  ## 역할: API 연동 담당
  ## 작업: {작업 내용}

  ### 사전 준비 (필수)
  1. .claude/rules/core/state-and-server-state.md를 읽어
  2. .claude/rules/core/coding-standards.md도 읽어

  ### 작업 흐름
  1. 기존 서비스/쿼리 패턴 분석
  2. API 서비스 + TanStack Query 훅 구현
  3. 빌드 검증: {패키지매니저} build

  ### 완료 시 (필수)
  1. `.claude/instructions/multi-agent/teammate-done-process.md`를 읽고 done 프로세스 수행
`);
```

**리팩토링:**

```
Task(subagent_type='general-purpose', team_name='sprint-team', name='refactorer', model='opus',
  prompt=`
  ## 역할: 리팩토링 담당
  ## 작업: {작업 내용}

  ### 사전 준비 (필수)
  1. .claude/skills/refactor/SKILL.md를 읽고 정책 보호 원칙 숙지
  2. .claude/rules/core/unit-test-conventions.md도 읽어

  ### 작업 흐름
  1. refactor 스킬의 Phase 1~5 따라 진행
  2. 정책 보호 테스트 먼저 작성 → 리팩토링 → 테스트 통과 확인

  ### 완료 시 (필수)
  1. `.claude/instructions/multi-agent/teammate-done-process.md`를 읽고 done 프로세스 수행
`);
```

### Agent Teams 워크플로우

```
1. 메인(팀 리드): /start 실행
   → 작업 분석, 서브태스크 분리

2. 팀 생성 + 역할별 팀원 spawn:
   TeamCreate({ team_name: 'sprint-team', description: '서브태스크 병렬 처리' });
   Task(... name='ui-implementor' ...);  // UI 구현
   Task(... name='api-integrator' ...);  // API 연동
   Task(... name='refactorer' ...);      // 리팩토링

3. 팀원 작업 (병렬):
   각 팀원:
   ① 스킬/규칙 읽기 → ② 코드 분석 → ③ 구현 → ④ 보고

4. 팀 리드: 결과 취합, 충돌 해결, 빌드 검증

5. 평가: team-evaluation.md 기준으로 각 팀원 평가 (90+ A등급 목표)

6. 정리: 팀원별 shutdown_request → TeamDelete
```

### 팀 리드 완료 체크리스트 (필수)

> **shutdown 전에 반드시 이 체크리스트를 확인한다.**
> 팀원 관리에 집중하다 후반 단계를 누락하는 것을 방지하기 위한 장치.

```
□ 1. 각 팀원이 teammate-done-process.md done 프로세스를 수행했는지 확인
     - git diff 분석, 린트, 커밋, SendMessage 보고 모두 포함
     - 미수행 항목이 있으면 팀원에게 SendMessage로 재요청
□ 2. 각 팀원 커밋 검증 (git log로 커밋 존재 + git diff로 범위 확인)
□ 3. 통합 린트/빌드 검증 ({패키지매니저} lint)
□ 3.5 release-readiness-gate 기준 최종 PASS 확인
□ 4. team-evaluation.md 기준 각 팀원 평가 작성 → 사용자에게 공유
□ 5. 평가 완료 후 → shutdown_request → TeamDelete
```

**핵심**: 1번에서 팀원의 done 프로세스 수행 여부를 먼저 확인한다.
팀원이 done 프로세스를 안 했으면 shutdown하지 말고 SendMessage로 수행을 요청한다.
shutdown/TeamDelete를 먼저 실행하면 팀원 컨텍스트가 소실되어 보완이 불가능하다.

### Agent Teams 도구 매핑

| 기능      | 메인 에이전트     | 팀원 (general-purpose)     |
| --------- | ----------------- | -------------------------- |
| 스킬 지식 | Skill 도구로 로드 | Read로 스킬 파일 직접 읽기 |
| 이슈 조회 | Skill → Bash      | Bash (이슈 트래커 CLI)     |
| 코드 분석 | Read, Grep, Glob  | Read, Grep, Glob (동일)    |
| 구현      | Edit, Write       | Edit, Write (동일)         |
| 팀 보고   | -                 | SendMessage                |

---

## 일반 Task 병렬 역할 템플릿

> 메인이 `/start`로 분석을 완료한 후, **분석 결과를 프롬프트에 전달**하여 병렬 실행
> 서브에이전트는 **구현에 집중**

**UI 구현:**

```
Task(subagent_type='general-purpose', model='sonnet',
  prompt=`
  ## 역할: UI 구현 담당

  ### 사전 준비 (필수)
  1. .claude/rules/core/react-nextjs-conventions.md를 읽고 규칙을 숙지해

  ### 작업 내용
  {구체적 구현 지시}
`);
```

**API 연동:**

```
Task(subagent_type='general-purpose', model='sonnet',
  prompt=`
  ## 역할: API 연동 담당

  ### 사전 준비 (필수)
  1. .claude/rules/core/state-and-server-state.md를 읽어
  2. .claude/rules/core/coding-standards.md도 읽어

  ### 작업 내용
  {API 스펙, 엔드포인트, 타입 정보 등 구체적 지시}
`);
```

**리팩토링:**

```
Task(subagent_type='general-purpose', model='opus',
  prompt=`
  ## 역할: 리팩토링 담당

  ### 사전 준비 (필수)
  1. .claude/skills/refactor/SKILL.md를 읽고 정책 보호 원칙 숙지
  2. .claude/rules/core/unit-test-conventions.md도 읽어

  ### 작업 내용
  {리팩토링 대상, 목표, 제약 조건}
`);
```

**버그 수정:**

```
Task(subagent_type='general-purpose', model='sonnet',
  prompt=`
  ## 역할: 버그 수정 담당

  ### 사전 준비 (필수)
  1. .claude/skills/bug-fix/SKILL.md를 읽고 분석 → 옵션 → 수정 흐름 숙지

  ### 작업 내용
  {에러 증상, 발생 조건, 관련 파일}
`);
```

---

## 모델 라우팅 전략

**상세**: `@./model-routing.md`

| 복잡도     | 모델   | 사용 케이스                     |
| ---------- | ------ | ------------------------------- |
| **LOW**    | haiku  | 파일 탐색, 단순 검색, 린트 수정 |
| **MEDIUM** | sonnet | 코드 리뷰, 테스트 생성, 구현    |
| **HIGH**   | opus   | 아키텍처 설계, 복잡한 버그      |

> 비즈니스 로직(날짜·금액·상태 전이 등)이 포함되면 한 단계 상향 조정

---

## 컨텍스트 보존 전략

### 1. 문서 기반 핸드오프

에이전트 간 컨텍스트는 파일로 전달:

```typescript
// Agent 1: 분석 결과를 파일에 저장
Task(
  (subagent_type = "explore"),
  (prompt = "분석 후 .claude/temp/analysis.md에 저장"),
);

// Agent 2: 파일 읽어서 작업 수행
Task(
  (subagent_type = "implementation-executor"),
  (prompt = ".claude/temp/analysis.md 읽고 구현"),
);
```

### 2. 프롬프트 내 컨텍스트 명시

```typescript
Task(
  (subagent_type = "test-generator"),
  (prompt = `
  대상: src/{대상파일}
  테스트 위치: __tests__/{파일명}.test.ts
`),
);
```

---

## 에러 핸들링

| 전략              | 설명                        | 적용         |
| ----------------- | --------------------------- | ------------ |
| **실패 격리**     | 에이전트 실패가 전체 영향 X | 병렬 실행 시 |
| **재시도**        | 최대 3회, 지수 백오프       | 일시적 실패  |
| **서킷 브레이커** | 연속 실패 시 중단           | API 호출     |

```typescript
// 병렬 실행 중 일부 실패해도 나머지 결과 활용
Task(...) // 성공 → 결과 사용
Task(...) // 실패 → 무시하고 진행
Task(...) // 성공 → 결과 사용
```

---

---

## TODO: 툴별 가이드 분기 (미완료)

> 현재 `TeamCreate`, `SendMessage` 패턴은 Claude Code 전용이다.
> Cursor / Codex 사용자에게는 데드코드가 된다.

- [ ] 각 패턴 블록에 `[Claude Code 전용]` 레이블 명시
- [ ] `## 폴백 모드 (Agent Teams 미가용 시)` 패턴을 범용 기본값으로 재포지셔닝
- [ ] 툴별 가이드 파일 분기 또는 조건부 섹션 도입 검토

---

## 참조 문서

| 문서               | 경로                                  |
| ------------------ | ------------------------------------- |
| 에이전트 목록      | `./agent-roster.md`                   |
| 실행 패턴          | `./execution-patterns.md`             |
| 모델 라우팅        | `./model-routing.md`                  |
| 팀원 Done 프로세스 | `./teammate-done-process.md`          |
| 팀 평가 템플릿     | `./team-evaluation.md`                |
| 금지 패턴          | `../validation/forbidden-patterns.md` |
