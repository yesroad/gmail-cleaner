---
name: migration-helper
description: 라이브러리 버전 업그레이드 및 패턴 마이그레이션. "업그레이드", "마이그레이션", "v4→v5", "Pages Router→App Router", "의존성 업데이트" 언급 시 이 스킬을 활성화. 영향 파일 분석 후 단계적 실행.
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Bash
metadata:
  version: "1.0.0"
  category: development
  priority: medium
---

# Migration Helper

> 기존 정책을 유지하면서 라이브러리/패턴을 안전하게 마이그레이션

---

## 트리거 조건

| 트리거 | 반응 |
|--------|------|
| "업그레이드해줘", "마이그레이션" | 스킬 활성화 |
| "v4 → v5", "버전 올려" | 스킬 활성화 |
| "Pages Router → App Router" | 스킬 활성화 |
| "의존성 업데이트" | 스킬 활성화 |

---

## ARGUMENT 확인

```
$ARGUMENTS 없음 → 질문:
"어떤 마이그레이션을 진행할까요?
- 라이브러리명 + 현재/목표 버전 (예: react-query v4 → v5)
- 패턴 변경 (예: Pages Router → App Router)
- 또는 package.json을 첨부해 주세요"

$ARGUMENTS 있음 → 다음 단계 진행
```

---

## 마이그레이션 유형

| 유형 | 예시 |
|------|------|
| **라이브러리 버전 업** | TanStack Query v4→v5, Next.js 13→14 |
| **프레임워크 패턴** | Pages Router → App Router |
| **런타임/도구** | Node 18→20, TypeScript 4→5 |
| **상태 관리** | Redux → Jotai, Recoil → Jotai |
| **스타일링** | styled-components → emotion |

---

## 복잡도 판단

| 복잡도 | 기준 | 접근 |
|--------|------|------|
| **LOW** | 단순 API 이름 변경, 10개 이하 파일 | 직접 실행 |
| **MEDIUM** | 동작 방식 변경, 10-50개 파일 | 계획 후 단계적 실행 |
| **HIGH** | 아키텍처 변경, 50개+ 파일 | Plan 에이전트 + 단계 분리 |

---

## 워크플로우

### Phase 1: 현황 분석

```bash
# 현재 버전 확인
cat package.json | grep -A 2 '"dependencies"'
cat package.json | grep -A 2 '"devDependencies"'
```

```typescript
// 영향 파일 탐색
Task(subagent_type="explore", model="haiku", prompt=`
  {마이그레이션 대상} 관련 사용 현황:
  1. import 패턴 (어떤 API를 쓰는지)
  2. 영향받는 파일 목록과 수
  3. 변경 필요한 패턴 종류
  4. 기존 테스트 유무
`)
```

---

### Phase 2: 마이그레이션 계획 수립

```markdown
## 마이그레이션 계획

### 대상
- 라이브러리/패턴: {이름}
- 현재 버전: {버전}
- 목표 버전: {버전}
- 영향 파일: {N}개

### 변경 패턴 요약
| 현재 | 변경 후 | 파일 수 |
|------|---------|---------|
| {API명} | {새 API명} | {N} |

### 단계별 계획
| 단계 | 작업 | 예상 파일 수 | 리스크 |
|------|------|-------------|--------|
| 1 | 패키지 업그레이드 | 1 | 낮음 |
| 2 | 타입 변경 | {N} | 낮음 |
| 3 | API 변경 | {N} | 중간 |
| 4 | 동작 변경 | {N} | 높음 |

### 롤백 전략
git stash 또는 feature 브랜치 분리

진행할까요? [Y/n]
```

---

### Phase 3: 정책 보호 테스트 작성

마이그레이션 전, 현재 동작을 캡처하는 테스트 작성:

```typescript
// 마이그레이션 전 동작 캡처
describe('마이그레이션 전 정책 보호', () => {
  it('기존 훅이 동일한 데이터 형태를 반환해야 함', () => {
    // 마이그레이션 후 이 테스트가 통과해야 성공
  })
})
```

테스트가 이미 있으면 현재 통과 여부 먼저 확인:

> **패키지 매니저**: lock 파일 기준 자동 감지 — `yarn.lock` → yarn, `pnpm-lock.yaml` → pnpm, `package-lock.json` → npm (없으면 npm)

```bash
{패키지매니저} test
```

---

### Phase 4: 단계적 실행

**각 단계 후 검증을 반복:**

```bash
# 패키지 업그레이드
{패키지매니저} add {라이브러리}@{버전}

# 타입 체크 (즉각 피드백)
{패키지매니저} tsc --noEmit

# 린트
{패키지매니저} lint

# 테스트
{패키지매니저} test
```

**HIGH 복잡도 시 Plan 에이전트 활용:**

```typescript
Task(subagent_type="Plan", model="opus", prompt=`
  마이그레이션: {내용}
  영향 파일: {목록}
  제약: 기존 정책 동작 유지, 기능 회귀 없음

  파일별 단계 계획 수립
`)
```

---

### Phase 5: 검증 및 정리

```bash
# 전체 빌드
{패키지매니저} build

# 전체 테스트
{패키지매니저} test

# 타입 체크
{패키지매니저} tsc --noEmit
```

**완료 후 정리:**
- 마이그레이션용 임시 호환 코드 제거
- deprecated 패턴 잔존 여부 재확인
- CHANGELOG 또는 PR 설명에 변경 내용 기록

---

## 주요 마이그레이션 참고 패턴

### TanStack Query v4 → v5

| v4 | v5 |
|----|----|
| `useQuery({ queryKey, queryFn })` | 동일 (호환) |
| `status === 'loading'` | `isPending` |
| `isLoading` | `isPending && !isFetching` |
| `onSuccess / onError` 콜백 | 제거됨 → useEffect로 대체 |
| `cacheTime` | `gcTime` |

### Next.js Pages Router → App Router

| Pages | App Router |
|-------|------------|
| `pages/` | `app/` |
| `getServerSideProps` | `async` 서버 컴포넌트 |
| `getStaticProps` | `fetch` + `cache` |
| `_app.tsx` | `layout.tsx` |
| `useRouter().query` | `useSearchParams()` / `params` |

---

## 금지 패턴

| 금지 | 이유 |
|------|------|
| 테스트 없이 전체 일괄 변경 | 회귀 감지 불가 |
| 한 커밋에 모든 변경 포함 | 롤백 어려움 |
| 동작 차이 무시하고 기계적 치환 | 런타임 버그 발생 |
| 마이그레이션 중 기능 추가 | 변경 추적 어려움 |

---

## 완료 전 출시 게이트

`release-readiness-gate.md` 5개 게이트 점검 후 커밋.

---

## 참조 문서

| 문서 | 용도 |
|------|------|
| `@../../instructions/workflow-patterns/sequential-thinking.md` | 복잡도 판단 |
| `@../../instructions/validation/release-readiness-gate.md` | 출시 게이트 |
| `@../../rules/core/unit-test-conventions.md` | 정책 보호 테스트 |
| `@../../skills/refactor/SKILL.md` | 점진적 변경 원칙 |
