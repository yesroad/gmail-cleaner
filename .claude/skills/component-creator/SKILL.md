---
name: component-creator
description: >
  React/Next.js 단일 컴포넌트 또는 훅을 신규 생성. 기존 프로젝트 패턴(스타일링 방식, export 형태, props 타입 위치)을 분석하여 일관된 보일러플레이트 생성.
  "컴포넌트 만들어", "새 컴포넌트", "훅 만들어", "페이지 추가" 가 언급될 때 사용.
  단, service+query+view를 함께 만드는 도메인 전체 스캐폴딩이나 "어디에 파일 만들어야 해?" 같은 폴더 구조 질문은 next-project-structure를 사용.
user-invocable: true
allowed-tools: Read, Grep, Glob, Write, Edit, Bash
metadata:
  version: '1.0.0'
  category: development
  priority: high
---

# Component Creator

> 기존 프로젝트 패턴을 분석하여 일관된 컴포넌트/훅을 생성

---

## 스킬 경계

| 요청 유형 | 사용할 스킬 |
|---|---|
| 단일 컴포넌트/훅 생성 | **component-creator** (이 스킬) |
| service + query + view 전체 도메인 | **next-project-structure** |
| "어디에 파일 만들어야 해?" 폴더 구조 질문 | **next-project-structure** |
| 기존 컴포넌트 구조 개선 | **refactor** |

---

## 트리거 조건

| 트리거                           | 반응        |
| -------------------------------- | ----------- |
| "컴포넌트 만들어", "새 컴포넌트" | 스킬 활성화 |
| "훅 만들어", "커스텀 훅 추가"    | 스킬 활성화 |
| "페이지 컴포넌트 추가"           | 스킬 활성화 |
| "보일러플레이트 생성"            | 스킬 활성화 |

---

## ARGUMENT 확인

```
$ARGUMENTS 없음 → 질문:
"어떤 컴포넌트를 만들까요?
- 이름 (예: UserCard, useProductFilter)
- 역할/기능 설명
- 위치 (경로 힌트, 없으면 자동 판단)"

$ARGUMENTS 있음 → 다음 단계 진행
```

---

## 컴포넌트 유형 판단

| 유형                | 기준                               | 생성 파일                              |
| ------------------- | ---------------------------------- | -------------------------------------- |
| **UI 컴포넌트**     | `Button`, `Card`, `Modal` 등 범용  | `index.tsx` + `styled.ts`              |
| **도메인 컴포넌트** | 특정 기능 종속                     | `index.tsx` + `styled.ts` + `types.ts` |
| **페이지**          | `page.tsx` (App Router) / `pages/` | `page.tsx` + 관련 컴포넌트             |
| **커스텀 훅**       | `use` 접두사                       | `use{Name}.ts` + `__tests__/`          |
| **레이아웃**        | `Layout`, `Shell`                  | `layout.tsx`                           |

---

## 워크플로우

### Phase 1: 프로젝트 패턴 추출

기존 컴포넌트를 직접 읽어 패턴을 확정한다. 이 단계의 결과가 Phase 3의 실제 템플릿이 된다.

**1-1. 컴포넌트 후보 탐색 (병렬):**

```typescript
// 유사한 컴포넌트가 있을 법한 경로를 병렬 탐색
Task(
  (subagent_type = 'explore'),
  (model = 'sonnet'),
  (prompt = `
  아래 경로에서 가장 최근에 수정된 컴포넌트 2개를 찾아 전체 코드를 읽어라:
  - src/components/
  - src/features/ 또는 src/domains/ 또는 src/views/
  - src/app/ 또는 src/pages/ (페이지 요청 시)
  - src/hooks/ (훅 요청 시)

  없으면 src/ 전체에서 가장 일반적인 .tsx 파일 2개를 찾아라.
`),
);
```

**1-2. 패턴 스펙 확정:**

탐색 결과를 바탕으로 아래 항목을 확정한다. 불명확하면 실제 코드에서 보이는 대로 따른다.

| 항목              | 확인 방법                                                          |
| ----------------- | ------------------------------------------------------------------ |
| **파일 분리**     | `index.tsx`만 있나? `styled.ts`, `types.ts` 분리되나?              |
| **스타일링**      | import 문에서 `@emotion`, `styled-components`, `*.module.css` 확인 |
| **Props 타입**    | `interface` vs `type`, 같은 파일인지 `types.ts` 분리인지           |
| **export**        | `export function` (named) vs `export default`                      |
| **'use client'**  | 기존 컴포넌트에 있나? 없나?                                        |
| **import 순서**   | 외부 → 내부 패키지 → 상대경로 패턴 확인                            |
| **barrel export** | 상위 `index.ts`에 re-export 하는 패턴인지                          |

---

### Phase 2: 생성 계획 출력

Phase 1에서 확정된 패턴 스펙을 포함해서 출력한다:

```markdown
## 생성 계획: {컴포넌트명}

- 유형: {UI 컴포넌트 / 도메인 컴포넌트 / 페이지 / 훅}
- 경로: {생성 위치}
- 참조한 기존 컴포넌트: {경로}

### 적용할 패턴 스펙

- 파일 구조: {index.tsx 단일 / index.tsx + styled.ts / index.tsx + styled.ts + types.ts}
- 스타일링: {@emotion/styled / styled-components / css modules / 없음}
- Props 타입: {interface / type} → {같은 파일 / types.ts 분리}
- export: {named / default}
- 'use client': {있음 / 없음}

### 생성 파일

- {파일1}: {역할}
- {파일2}: {역할}

생성할까요? [Y/n]
```

---

### Phase 3: 파일 생성

**Phase 1에서 추출한 패턴 스펙을 그대로 따른다.** 아래 예시는 참고용이며, 실제 파일은 스펙에 따라 다르게 생성된다.

예: Phase 1에서 `named export`, `@emotion/styled`, `types.ts 분리`, `'use client' 없음` 패턴이 확인됐다면:

```typescript
// {Name}/index.tsx  ← 'use client' 없음 (스펙에 따라)
import type { {Name}Props } from './types'    // types.ts 분리 (스펙에 따라)
import * as S from './styled'

export function {Name}({ ... }: {Name}Props) {  // named export (스펙에 따라)
  return <S.Container>...</S.Container>
}
```

```typescript
// {Name}/styled.ts  ← @emotion/styled (스펙에 따라)
import styled from '@emotion/styled';
export const Container = styled.div``;
```

```typescript
// {Name}/types.ts  ← 분리 (스펙에 따라)
export interface {Name}Props { ... }  // interface (스펙에 따라)
```

훅인 경우도 동일하게 기존 훅 파일을 읽어 패턴을 따른다.

---

### Phase 4: 연관 파일 업데이트

생성 후 필요 시:

- `index.ts` (barrel export) 업데이트
- 라우트 파일 등록 (페이지인 경우)
- 스토리북 파일 생성 (프로젝트에 storybook이 있는 경우)

---

### Phase 5: 검증

> **패키지 매니저**: lock 파일 기준 자동 감지 — `yarn.lock` → yarn, `pnpm-lock.yaml` → pnpm, `package-lock.json` → npm (없으면 npm)

```bash
{패키지매니저} tsc --noEmit
{패키지매니저} lint
```

타입 오류나 import 누락이 없는지 확인한다.

---

## 금지 패턴

| 금지                                | 이유                    |
| ----------------------------------- | ----------------------- |
| 기존 패턴 무시하고 새 스타일 도입   | 코드베이스 일관성 깨짐  |
| `'use client'` 무조건 추가          | 서버 컴포넌트 이점 상실 |
| Props 없이 하드코딩                 | 재사용 불가             |
| 컴포넌트 내 비즈니스 로직 직접 작성 | 책임 분리 위반          |

---

## 참조 문서

| 문서                                            | 용도                 |
| ----------------------------------------------- | -------------------- |
| `@../../rules/core/react-nextjs-conventions.md` | React/Next.js 컨벤션 |
| `@../../rules/core/nextjs-app-router.md`        | App Router 규칙      |
| `@../../rules/core/react-hooks-patterns.md`     | 훅 패턴              |
| `@../../rules/core/coding-standards.md`         | TypeScript 표준      |
