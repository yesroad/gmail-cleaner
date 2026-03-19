---
name: test-generator
description: 기존 함수/컴포넌트에 대한 테스트 생성. "테스트 작성", "테스트 추가", "커버리지 올려", "테스트 없는 파일" 언급 시 이 스킬을 활성화. 순수 함수 우선, 정책 케이스 포함.
user-invocable: true
allowed-tools: Read, Grep, Glob, Write, Bash
metadata:
  version: "1.0.0"
  category: testing
  priority: medium
---

# Test Generator

> 기존 코드를 분석하여 정책 케이스를 포함한 테스트를 생성

---

## 트리거 조건

| 트리거 | 반응 |
|--------|------|
| "테스트 작성해줘", "테스트 추가" | 스킬 활성화 |
| "커버리지 올려", "테스트 없어" | 스킬 활성화 |
| 파일 경로 + 테스트 언급 | 해당 파일 대상 |

---

## ARGUMENT 확인

```
$ARGUMENTS 없음 → 질문:
"어떤 파일의 테스트를 작성할까요?
- 파일 경로 (예: src/utils/date.ts)
- 또는 테스트가 없는 영역 설명"

$ARGUMENTS 있음 → 다음 단계 진행
```

---

## 테스트 대상 분류

| 유형 | 기준 | 테스트 전략 |
|------|------|-------------|
| **순수 함수** | utils, helpers, lib, adapters | 유닛 테스트 (Jest) |
| **커스텀 훅** | `use` 접두사 | renderHook + act |
| **서버 액션** | Next.js Server Actions | 단위 테스트 (mocking) |
| **React 컴포넌트** | UI 렌더링 | 기본 렌더 스모크 테스트 |
| **API 핸들러** | route.ts, api/ | 통합 테스트 |

> 순수 함수를 우선 타겟으로 한다. 비즈니스 정책이 담긴 곳이 가장 가치 있는 테스트 대상이다.

---

## 워크플로우

### Phase 1: 대상 파일 분석

```typescript
Task(subagent_type="explore", model="haiku", prompt=`
  {파일 경로} 분석:
  1. export된 함수/클래스 목록
  2. 각 함수의 입력/출력 타입
  3. 날짜, 계산, 정책 로직 포함 여부
  4. 기존 테스트 파일 유무
  5. 외부 의존성 (API 호출, DB 등)
`)
```

---

### Phase 2: 테스트 케이스 도출

각 함수에 대해 아래 카테고리를 도출한다:

| 카테고리 | 설명 | 우선순위 |
|----------|------|----------|
| **정상 케이스** | 일반 유효 입력 | 필수 |
| **경계값** | 0, 빈 배열, null, undefined | 필수 |
| **에러 케이스** | 잘못된 타입, 범위 초과 | 필수 |
| **정책 케이스** | 비즈니스 규칙 반영 | 정책 함수에 필수 |

**도출 결과 출력:**

```markdown
## 테스트 케이스 계획

### {함수명}
- 정상: {케이스}
- 경계값: {케이스}
- 에러: {케이스}
- 정책: {케이스 (있는 경우)}

생성할까요? [Y/n]
```

---

### Phase 3: 테스트 파일 생성

`unit-test-conventions.md` 규칙을 따른다:

**파일 위치:**
```
{파일경로}/__tests__/{파일명}.test.ts
```

**기본 구조:**

```typescript
import { 함수명 } from '../파일명'

describe('함수명', () => {
  // 날짜 의존 함수는 필수
  beforeAll(() => {
    jest.useFakeTimers().setSystemTime(new Date('2024-01-15T00:00:00.000Z'))
  })

  afterAll(() => {
    jest.useRealTimers()
  })

  describe('정상 케이스', () => {
    it('일반적인 입력에 대해 올바른 결과 반환', () => {
      expect(함수(입력)).toEqual(기대값)
    })
  })

  describe('경계값', () => {
    it('null 입력 시 기본값 반환', () => {})
    it('빈 배열 입력 시 처리', () => {})
  })

  describe('에러 케이스', () => {
    it('잘못된 입력 시 에러 또는 기본값 반환', () => {})
  })
})
```

**외부 의존성이 있는 경우 모킹:**

```typescript
// API 호출 모킹
jest.mock('@/lib/api', () => ({
  fetchUser: jest.fn().mockResolvedValue({ id: '1', name: 'Alice' }),
}))
```

---

### Phase 4: 테스트 실행 및 검증

> **패키지 매니저**: lock 파일 기준 자동 감지 — `yarn.lock` → yarn, `pnpm-lock.yaml` → pnpm, `package-lock.json` → npm (없으면 npm)

```bash
# 커버리지 포함 실행 (항상)
{패키지매니저} test -- --coverage --testPathPattern="{파일명}.test" --coverageReporters=text
```

**실패 시 처리:**
- 타입 불일치 → 모킹 또는 테스트 케이스 수정
- 로직 오류 발견 → 사용자에게 알리고 원본 코드 버그 여부 확인

---

### Phase 5: 완료 요약 출력

테스트 실행 후 반드시 아래 형식으로 요약을 출력한다:

```markdown
## 테스트 생성 완료

### 생성된 파일
- {테스트 파일 경로}

### 테스트 케이스
| 함수 | 정상 | 경계값 | 에러 | 정책 | 합계 |
|------|:----:|:------:|:----:|:----:|:----:|
| {함수명} | {N} | {N} | {N} | {N} | {N} |
| **합계** | | | | | **{N}** |

### 커버리지
| 항목 | 커버리지 |
|------|---------|
| Statements | {N}% |
| Branches | {N}% |
| Functions | {N}% |
| Lines | {N}% |

### 미커버 항목
- {커버되지 않은 라인/브랜치 (있는 경우)}

### 다음 단계 제안
- {커버리지가 낮은 경우: 추가 케이스 제안}
- {정책 로직 발견 시: 추가 정책 테스트 제안}
```

커버리지 80% 미만인 항목이 있으면 추가 케이스를 제안한다.

---

## 커버리지 부족 파일 탐색

테스트가 없는 중요 파일을 찾는 경우:

```bash
# 테스트 파일 없는 utils 탐색
find src/utils src/helpers src/lib src/adapters -name "*.ts" ! -name "*.test.ts" ! -name "*.d.ts"
```

발견된 파일 중 비즈니스 로직이 있는 것을 우선 타겟으로 제안한다.

---

## 금지 패턴

| 금지 | 이유 |
|------|------|
| 구현 상세 의존 (private 메서드 spy) | 리팩토링 시 테스트 깨짐 |
| 테스트 간 상태 공유 | 실행 순서 의존성 |
| 하드코딩 날짜 | 시간 경과 시 실패 |
| 외부 API 실제 호출 | 불안정한 테스트 |

---

## 참조 문서

| 문서 | 용도 |
|------|------|
| `@../../rules/core/unit-test-conventions.md` | 테스트 구조/규칙 |
