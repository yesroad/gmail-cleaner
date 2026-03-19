# Agent Roster

> 프로젝트에 최적화된 전문 에이전트 카탈로그

**모델 선택 기준**: `./coordination-guide.md` 참조 (단일 진실 공급원)

---

## 에이전트 목록

| 에이전트                    | 기본 모델 | 병렬 | 용도                          |
| --------------------------- | --------- | ---- | ----------------------------- |
| **explore**                 | haiku     | ✅   | 코드베이스 탐색, 패턴 분석    |
| **code-reviewer**           | sonnet    | ✅   | 코드 리뷰, 품질 검증          |
| **lint-fixer**              | haiku     | ✅   | 린트/포맷 오류 수정           |
| **Plan** (빌트인)           | opus      | ❌   | 아키텍처 설계, 구현 계획      |
| **implementation-executor** | sonnet    | ⚠️   | 코드 구현, 수정               |
| **git-operator**            | sonnet    | ❌   | Git 커밋/브랜치/PR 관리       |

> 비즈니스 로직(날짜 계산, 상태 조건, 수치 계산 등) 포함 시 모델 상향 - `coordination-guide.md` 참조

---

## 에이전트 상세

### explore

**목적**: 코드베이스 빠른 탐색, 파일 구조 파악

```typescript
// 단순 구조 탐색: haiku
Task(
  (subagent_type = "explore"),
  (model = "haiku"),
  (prompt = "src/ 폴더 구조 파악"),
);

// 정책/로직 분석: sonnet
Task(
  (subagent_type = "explore"),
  (model = "sonnet"),
  (prompt = "필터 disabled 조건 분석"),
);

// 복잡한 비즈니스 로직: opus
Task(
  (subagent_type = "explore"),
  (model = "opus"),
  (prompt = "날짜 계산 로직 분석 - 비즈니스 규칙 파악"),
);
```

**참조**: `@../workflow-patterns/sequential-thinking.md` (탐색 단계)

---

### code-reviewer

**목적**: PR 전 코드 품질 검증

```typescript
Task(
  (subagent_type = "code-reviewer"),
  (model = "sonnet"),
  (prompt = `
     대상: src/
     기준:
     - @../../rules/core/react-nextjs-conventions.md
     - @../../rules/core/state-and-server-state.md
     `),
);
```

**검토 항목**:
| 항목 | 확인 |
|------|------|
| Import 순서 | 외부 → 내부 패키지 → 상대경로 |
| 상태 관리 경계 | 서버/전역/폼/로컬 분리 |
| 타입 명시 | return type 필수 |

---

### lint-fixer

**목적**: ESLint/Prettier 오류 자동 수정

```typescript
Task(
  (subagent_type = "lint-fixer"),
  (model = "haiku"),
  (prompt = "src/ 린트 오류 수정"),
);
```

**실행 명령**:

```bash
yarn lint --fix
yarn format
```

---

### Plan

**목적**: 복잡한 작업의 아키텍처 설계 및 구현 계획

```typescript
Task(
  (subagent_type = "Plan"),
  (model = "opus"),
  (prompt = "인증 모듈 리팩토링 계획 수립"),
);
```

**참조**: `@../workflow-patterns/sequential-thinking.md` (HIGH 복잡도 단계)

---

### implementation-executor

**목적**: 계획된 코드 구현 실행

```typescript
// Plan 결과 후 실행
Task(
  (subagent_type = "implementation-executor"),
  (model = "sonnet"),
  (prompt = `
     규칙: @../../rules/core/react-nextjs-conventions.md
     작업: {구현 내용}
     `),
);
```

**⚠️ 병렬 제한**: 같은 파일 수정 시 순차 실행 필수

---

## 조합 패턴

### 탐색 → 구현 (정책 고려)

```typescript
// 1. 복잡도 판단 (haiku)
Task(
  (subagent_type = "explore"),
  (model = "haiku"),
  (prompt = "영향 파일 수, 정책 키워드 확인"),
);

// 2. 정책 분석 (sonnet/opus - 키워드에 따라)
Task(
  (subagent_type = "explore"),
  (model = "sonnet"),
  (prompt = "기존 패턴 분석 - 정책 영향 확인"),
);
Task(
  (subagent_type = "explore"),
  (model = "opus"),
  (prompt = "날짜 계산 로직 분석"),
); // 정책 키워드 포함

// 3. 계획 수립 (opus - 정책 관련)
Task(
  (subagent_type = "Plan"),
  (model = "opus"),
  (prompt = "분석 결과 기반 구현 계획"),
);

// 4. 구현 (sonnet)
Task(
  (subagent_type = "implementation-executor"),
  (model = "sonnet"),
  (prompt = "계획대로 구현"),
);
```

### 구현 → 검증 (정책 보호)

```typescript
// 병렬 검증
Task((subagent_type = "lint-fixer"), (model = "haiku"), (prompt = "린트 수정"));
Task(
  (subagent_type = "code-reviewer"),
  (model = "sonnet"),
  (prompt = "코드 리뷰 - 정책 준수 확인"),
);
```

---

## 에이전트 파일 위치

```
.claude/agents/
├── explore.md              # 코드베이스 탐색
├── code-reviewer.md        # 코드 리뷰
├── lint-fixer.md           # 린트 수정
├── implementation-executor.md  # 구현 전문가
└── git-operator.md         # Git 커밋/PR 관리
```

> 스킬은 에이전트보다 상위 워크플로우. 상황에 맞는 스킬을 먼저 확인 후 내부에서 에이전트 조합.

---

## 스킬 카탈로그

| 스킬 | 트리거 | 에이전트 조합 |
|------|--------|--------------|
| **commit-helper** | "커밋 메시지" | git-operator |
| **code-quality** | "린트", "포맷", "타입체크" | lint-fixer |
| **bug-fix** | "버그", "오류", "에러" | explore → implementation-executor |
| **refactor** | "리팩토링", "구조 개선" | explore → Plan → implementation-executor |
| **docs-creator** | "문서 작성", "CLAUDE.md" | explore |
| **agents-generator** | "루트 지시문 생성" | explore |
| **component-creator** | "컴포넌트 만들어", "페이지 추가" | explore → implementation-executor |
| **test-generator** | "테스트 작성", "커버리지" | explore |
| **pr-review-responder** | "리뷰 반영", PR 번호 | explore → implementation-executor |
| **migration-helper** | "업그레이드", "마이그레이션" | explore → Plan → implementation-executor |

### 스킬 연결 흐름

```
component-creator (컴포넌트 생성)
  └→ test-generator (생성한 컴포넌트 테스트 작성)

bug-fix (버그 수정)
  └→ test-generator (수정 후 회귀 방지 테스트)

refactor (리팩토링)
  └→ test-generator (정책 보호 테스트)

/done (작업 완료)
  └→ PR 생성 후 pr-review-responder (리뷰 대응)

migration-helper (라이브러리 업그레이드)
  └→ test-generator (마이그레이션 검증 테스트)
```

---

## 참조 문서

| 문서                                  | 용도           |
| ------------------------------------- | -------------- |
| `./coordination-guide.md`             | 병렬 실행 원칙 |
| `./execution-patterns.md`             | 실행 패턴 상세 |
| `../validation/forbidden-patterns.md` | 금지 패턴      |
| `../validation/required-behaviors.md` | 필수 행동      |
| `../../rules/core/thinking-model.md`  | 사고 모델      |
