# Instructions Index

> Claude Code 작업 효율화를 위한 가이드 모음

---

## 개요

**목표**: 멀티 에이전트 협업, 병렬 실행, 검증 자동화를 통한 효율성 극대화

**핵심 효과**:

- 병렬 실행으로 5-10배 속도 향상
- 모델 라우팅으로 비용 최적화
- 전문 에이전트로 품질 보증

---

## 문서 구조

```
.claude/instructions/
├── index.md                          # 이 파일
├── multi-agent/
│   ├── coordination-guide.md         # 병렬 실행 핵심 원칙
│   ├── agent-roster.md               # 에이전트 카탈로그
│   ├── execution-patterns.md         # 실행 패턴 상세
│   ├── team-evaluation.md            # Agent Teams 평가 기준
│   └── teammate-done-process.md      # 팀원 완료 프로세스
├── validation/
│   ├── forbidden-patterns.md         # 금지 패턴 목록
│   ├── required-behaviors.md         # 필수 행동 규칙
│   └── release-readiness-gate.md     # 출시 품질 게이트
└── workflow-patterns/
    └── sequential-thinking.md        # 복잡도별 사고 단계
```

---

## 문서 카탈로그

### Multi-Agent

| 문서                       | 용도                                      | 사용 시점                |
| -------------------------- | ----------------------------------------- | ------------------------ |
| `coordination-guide.md`    | 병렬 실행, 모델 라우팅, 컨텍스트 보존     | 에이전트 조합 필요 시    |
| `agent-roster.md`          | 에이전트 상세 (explore, code-reviewer 등) | 에이전트 선택 시         |
| `execution-patterns.md`    | Fan-Out, 배치, 백그라운드 패턴            | 구체적 실행 방법 필요 시 |
| `team-evaluation.md`       | Agent Teams 팀원 평가 기준                | 팀 작업 완료 후          |
| `teammate-done-process.md` | 팀원 5단계 완료 프로세스                  | 팀원 spawn 시 참조       |

### Validation

| 문서                        | 용도                                  | 사용 시점         |
| --------------------------- | ------------------------------------- | ----------------- |
| `forbidden-patterns.md`     | any 타입, 정책 임의 변경 등 금지 항목 | 코드 작성/리뷰 시 |
| `required-behaviors.md`     | 필수 행동 규칙 (병렬 읽기, 검증 등)   | 모든 작업 시      |
| `release-readiness-gate.md` | 계획/구현/보안/사용자흐름 최종 게이트 | 커밋/PR 직전      |

### Workflow Patterns

| 문서                     | 용도                          | 사용 시점           |
| ------------------------ | ----------------------------- | ------------------- |
| `sequential-thinking.md` | LOW/MEDIUM/HIGH 복잡도별 단계 | 작업 복잡도 판단 시 |

---

## 스킬 맵 (상황 → 스킬)

| 상황                       | 스킬                         |
| -------------------------- | ---------------------------- |
| 커밋 메시지 생성           | `skills/commit-helper`       |
| 린트/포맷/타입 체크        | `skills/code-quality`        |
| 버그 수정                  | `skills/bug-fix`             |
| 코드 리팩토링              | `skills/refactor`            |
| 새 컴포넌트/페이지/훅 생성 | `skills/component-creator`   |
| 테스트 작성                | `skills/test-generator`      |
| PR 리뷰 코멘트 반영        | `skills/pr-review-responder` |
| 라이브러리 업그레이드      | `skills/migration-helper`    |
| AI 도구 문서 작성          | `skills/docs-creator`        |
| 프로젝트 루트 지시문 생성  | `skills/agents-generator`    |

---

## 상황별 참조 가이드

| 상황                       | 참조 문서                                  |
| -------------------------- | ------------------------------------------ |
| **여러 에이전트 협업**     | `multi-agent/coordination-guide.md`        |
| **어떤 에이전트 사용할지** | `multi-agent/agent-roster.md`              |
| **구체적 실행 방법**       | `multi-agent/execution-patterns.md`        |
| **코드 품질 검증**         | `validation/forbidden-patterns.md`         |
| **배포 전 최종 점검**      | `validation/release-readiness-gate.md`     |
| **작업 복잡도 판단**       | `workflow-patterns/sequential-thinking.md` |

---

## Quick Start

### 작업 시작 시

```
1. sequential-thinking.md → 복잡도 판단 (LOW/MEDIUM/HIGH)
2. agent-roster.md → 필요한 에이전트 선택
3. execution-patterns.md → 실행 패턴 결정
```

### 코드 작성 시

```
1. forbidden-patterns.md → 금지 패턴 확인
2. rules/core/*.md → 프론트엔드 규칙 참조
```

---

## 연결된 규칙

| 문서           | 경로                                     | 연결                     |
| -------------- | ---------------------------------------- | ------------------------ |
| 통합 사고 모델 | `rules/core/thinking-model.md`           | sequential-thinking 통합 |
| React/Next.js  | `rules/core/react-nextjs-conventions.md` | 코드 품질                |
| 상태 관리      | `rules/core/state-and-server-state.md`   | TanStack Query           |
| 테스트 규칙    | `rules/core/unit-test-conventions.md`    | lint-fixer 연계          |

---

## 핵심 원칙

| 원칙                     | 설명                                   |
| ------------------------ | -------------------------------------- |
| **Parallel First**       | 독립 작업은 병렬 실행                  |
| **Model Routing**        | 복잡도별 모델 선택 (haiku/sonnet/opus) |
| **Context Preservation** | 문서 기반 컨텍스트 전달                |
| **Error Isolation**      | 에이전트 실패 격리, 재시도 3회         |
