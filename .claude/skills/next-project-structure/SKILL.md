---
name: next-project-structure
user-invocable: true
description: >
  Next.js 프로젝트에서 여러 레이어를 아우르는 도메인 전체를 스캐폴딩하거나, 파일 위치/폴더 구조를 안내할 때 사용.
  단일 컴포넌트·훅 생성은 component-creator를 사용. 이 스킬은 다음 상황에만 사용:
  "전체 도메인 추가" (service + query 훅 + view 한 번에),
  "API 서비스 파일 만들어" / "BaseServices 상속" / "서비스 클래스",
  "TanStack Query 훅 구조" / "queryKeys 분리" / "useQuery 어디에 만들어",
  "views 폴더 구조" / "어디에 파일 만들어야 해?" / "폴더 구조 어떻게?",
  "view + hook 분리 패턴" / "도메인 스캐폴딩" / "모노레포 구조".
  CLAUDE.md 없는 새 프로젝트나 문서가 부족한 프로젝트에서 특히 유용하다.
---

# next-project-structure

> Next.js 프로젝트에 일관된 폴더 구조와 코드 패턴을 적용하는 스킬.
> **이 스킬 자체가 패턴의 기준**이다 — CLAUDE.md에 의존하지 말고 이 스킬의 패턴을 따른다.
> 단, CLAUDE.md에 더 구체적인 프로젝트 패턴이 있다면 그것을 우선 참조한다.

---

## 워크플로우

### Step 1: 프로젝트 환경 파악

```bash
# 모노레포 여부 확인
ls packages/ 2>/dev/null && echo "Monorepo" || echo "Single app"

# App Router 여부 확인
ls src/app 2>/dev/null || ls app 2>/dev/null && echo "App Router" || echo "Pages Router"

# 기존 services/queries 패턴 확인 (있으면 그 패턴을 따름)
ls src/services/api/ 2>/dev/null
ls src/queries/ 2>/dev/null
```

**판단 결과에 따라 분기:**
- 모노레포 + `packages/services` 존재 → `import Services from '@workspace/services'` 사용
- 단일 앱 → `src/services/core/base.ts`에 BaseServices 직접 정의
- App Router → `references/app-router.md` 참조
- Pages Router → `references/pages-router.md` 참조

### Step 2: 기존 패턴 탐색 (신규 기능 전 필수)

새 도메인/파일을 만들기 전에 **유사한 기존 코드를 먼저 찾는다**. 기존 패턴이 있으면 그대로 따른다.

```bash
# 기존 서비스 패턴 참조
ls src/services/api/
# 기존 쿼리 패턴 참조
ls src/queries/
# 기존 뷰 패턴 참조
ls src/views/
```

### Step 3: 요청 종류에 따라 생성 대상 결정

| 요청 키워드 | 생성 대상 | 비고 |
|---|---|---|
| 서비스, API, service | `services/api/{domain}.ts` | |
| 쿼리, useQuery, TanStack, queryKeys | `queries/{domain}/` | |
| view, 뷰, view+hook 분리 | `views/{page}/` | |
| 전체 도메인, 도메인 추가 | services + queries + view + types 모두 | |
| 컴포넌트, 훅 단독 생성 | — | `component-creator` 스킬 사용 |

### Step 4: 파일 생성 + 배럴 index.ts 즉시 업데이트

파일을 만든 즉시 해당 폴더의 `index.ts` 배럴 export를 업데이트한다.
배럴 미업데이트는 import 에러의 주요 원인이다.

---

## 폴더 구조 원칙

```
src/
├── components/          # 앱 공통 UI 컴포넌트
│   └── {Name}/
│       ├── index.tsx           # UI만 (로직 없음)
│       └── use{Name}.ts        # 로직이 있으면 반드시 분리
├── hooks/               # 앱 공통 커스텀 훅
├── services/            # API 서비스
│   └── api/
│       ├── {domain}.ts         # BaseServices 상속
│       └── index.ts            # 배럴 export
├── queries/             # TanStack Query 훅
│   ├── {domain}/
│   │   ├── index.ts            # use{Domain}Query / use{Domain}Mutation
│   │   └── queryKeys.ts        # 쿼리 키 팩토리 (훅과 반드시 분리)
│   └── index.ts
├── types/
│   └── api/             # API 요청/응답 타입
├── lib/                 # 순수 함수 유틸리티
├── utils/               # 앱 유틸리티
└── provider/            # QueryProvider 등 전역 컨텍스트
```

**모노레포 추가 구조:**
```
packages/
├── services/            # BaseServices (axios wrapper) — 앱에서 상속
└── ui/                  # shadcn/ui 공통 컴포넌트
apps/
└── {app-name}/src/      # 위 src/ 구조와 동일
```

---

## 핵심 패턴

### Services (BaseServices 상속)

**모노레포 — `@workspace/services` 있을 때:**
```typescript
// src/services/api/{domain}.ts
import Services from '@workspace/services';
import type { {ResponseType} } from '@/types/api/{domain}';

class {Domain}Services extends Services {
  constructor() {
    super({ baseURL: '/api/{domain}' });
  }

  get{Resource}(params: {ParamsType}): Promise<{ResponseType}> {
    return this.get<{ResponseType}>('', params);
  }
}

export default new {Domain}Services(); // 싱글턴
```

**단일 앱 — BaseServices 없을 때:**
```typescript
// src/services/api/{domain}.ts
import axios from 'axios';
import type { {ResponseType} } from '@/types/api/{domain}';

// 또는 기존 http 클라이언트 패턴 확인 후 따름
const {domain}Api = axios.create({ baseURL: '/api/{domain}' });

export const {domain}Services = {
  get{Resource}: (params: {ParamsType}) =>
    {domain}Api.get<{ResponseType}>('', { params }).then(r => r.data),
};
```

### QueryKeys (반드시 별도 파일)

```typescript
// src/queries/{domain}/queryKeys.ts
export const {domain}Keys = {
  all: ['{domain}'] as const,
  lists: () => [...{domain}Keys.all, 'list'] as const,
  list: (param: string) => [...{domain}Keys.lists(), param] as const,
  detail: (id: string) => [...{domain}Keys.all, 'detail', id] as const,
};
```

queryKeys를 별도 파일로 분리하는 이유: 훅 파일이 커지면 쿼리 키만 교체하거나
다른 도메인에서 참조하기 쉽다. 또한 `invalidateQueries`에서 일관성을 보장한다.

### Query Hook

```typescript
// src/queries/{domain}/index.ts
'use client'; // 반드시 최상단 — Client Component에서만 훅 실행 가능

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {domain}Services from '@/services/api/{domain}';
import { {domain}Keys } from './queryKeys';

export function use{Domain}ListQuery(param: string) {
  return useQuery({
    queryKey: {domain}Keys.list(param),
    queryFn: () => {domain}Services.get{Resource}(param),
    staleTime: 5 * 60 * 1000,
    enabled: !!param, // param 없으면 실행 안 함
  });
}

export function useCreate{Domain}Mutation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (body: {CreateType}) => {domain}Services.create{Resource}(body),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: {domain}Keys.lists() });
    },
  });
}
```

### View (UI와 로직 분리)

뷰를 UI와 로직으로 분리하는 이유: 로직만 단독으로 테스트할 수 있고,
UI 변경 시 로직을 건드리지 않아도 된다. 또한 여러 UI가 같은 로직을 공유할 수 있다.

```typescript
// src/views/{page}/use{Page}View.ts
'use client';

import { useState, useCallback } from 'react';
import { use{Domain}ListQuery } from '@/queries/{domain}';

export function use{Page}View() {
  const [searchParam, setSearchParam] = useState('');
  const { data, isLoading, isError } = use{Domain}ListQuery(searchParam);

  const handleSearch = useCallback((value: string) => {
    setSearchParam(value);
  }, []);

  return { data, isLoading, isError, searchParam, handleSearch };
}
```

```typescript
// src/views/{page}/index.tsx
'use client';

import { use{Page}View } from './use{Page}View';

export default function {Page}View() {
  const { data, isLoading, isError, handleSearch } = use{Page}View();

  if (isLoading) return <div>로딩 중...</div>;
  if (isError) return <div>오류가 발생했습니다.</div>;

  return (
    <main>
      {/* UI만 — 비즈니스 로직 없음 */}
    </main>
  );
}
```

### Component (로직 있으면 훅 분리)

```typescript
// src/components/{Name}/use{Name}.ts
import { useState, useCallback } from 'react';

export function use{Name}() {
  const [state, setState] = useState(false);
  const handleAction = useCallback(() => setState(prev => !prev), []);
  return { state, handleAction };
}

// src/components/{Name}/index.tsx
import { use{Name} } from './use{Name}';

interface {Name}Props { /* props */ }

export default function {Name}(props: {Name}Props) {
  const { state, handleAction } = use{Name}();
  return <div>{/* UI */}</div>;
}
```

---

## 주요 금지 패턴

| 금지 | 이유 | 대안 |
|---|---|---|
| `useState(() => localStorage.getItem(...))` | SSR에서 ReferenceError | `useEffect`에서 로드 |
| `any` 타입 | 런타임 에러 미감지 | 명시적 `interface`/`type` |
| 배럴 index.ts 미업데이트 | import 경로 불일치 | 파일 생성 즉시 추가 |
| 뷰에 비즈니스 로직 직접 작성 | UI/로직 책임 혼재 | `use{Page}View` 훅으로 분리 |
| 훅 파일 상단에 `'use client'` 누락 | TanStack Query 서버 실행 오류 | 모든 훅 파일 최상단에 추가 |
| queryKeys를 훅 파일에 인라인 작성 | invalidate/prefetch 재사용 불가 | 별도 `queryKeys.ts` 파일 |

---

## 새 도메인 추가 체크리스트

- [ ] `types/api/{domain}.ts` — 요청/응답 타입 정의
- [ ] `services/api/{domain}.ts` — API 서비스 (BaseServices 상속 또는 기존 패턴)
- [ ] `services/api/index.ts` — 배럴 업데이트
- [ ] `queries/{domain}/queryKeys.ts` — 쿼리 키 팩토리
- [ ] `queries/{domain}/index.ts` — 훅 (`'use client'` 필수)
- [ ] `queries/index.ts` — 배럴 업데이트
- [ ] `views/{page}/use{Page}View.ts` — 로직 훅
- [ ] `views/{page}/index.tsx` — UI 컴포넌트
- [ ] App Router: `app/{route}/page.tsx` 에서 뷰 위임

---

## 상세 참조

| 파일 | 내용 |
|---|---|
| `references/app-router.md` | App Router 전용 패턴 (Server Component, Suspense 등) |
| `references/pages-router.md` | Pages Router 전용 패턴 |
| `references/boilerplate-templates.md` | 복사 즉시 사용 가능한 전체 보일러플레이트 |
