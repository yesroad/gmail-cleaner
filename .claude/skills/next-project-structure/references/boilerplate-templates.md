# 보일러플레이트 템플릿 모음

> 복사해서 즉시 사용 가능한 코드 스니펫
> `{Domain}`, `{domain}`, `{Resource}` 등은 실제 이름으로 치환

---

## 1. Service 템플릿

```typescript
// src/services/api/{domain}.ts
import Services from '@workspace/services';
import type { {ResponseType} } from '@/types/api/{domain}';

class {Domain}Services extends Services {
  constructor() {
    super({ baseURL: '/api/{domain}' });
  }

  get{Resource}(param: string): Promise<{ResponseType}> {
    return this.get<{ResponseType}>('', { param });
  }

  create{Resource}(body: {CreateType}): Promise<{ResponseType}> {
    return this.post<{ResponseType}>('', body);
  }
}

export default new {Domain}Services();
```

```typescript
// src/services/api/index.ts (배럴 — 추가분)
export { default as {domain}Services } from './{domain}';
```

---

## 2. QueryKeys 템플릿

```typescript
// src/queries/{domain}/queryKeys.ts
export const {domain}Keys = {
  all: ['{domain}'] as const,
  lists: () => [...{domain}Keys.all, 'list'] as const,
  list: (param: string) => [...{domain}Keys.lists(), param] as const,
  details: () => [...{domain}Keys.all, 'detail'] as const,
  detail: (id: string) => [...{domain}Keys.details(), id] as const,
};
```

---

## 3. Query Hook 템플릿

```typescript
// src/queries/{domain}/index.ts
'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {domain}Services from '@/services/api/{domain}';
import { {domain}Keys } from './queryKeys';

// 목록 조회
export function use{Domain}ListQuery(param: string) {
  return useQuery({
    queryKey: {domain}Keys.list(param),
    queryFn: () => {domain}Services.get{Resource}(param),
    staleTime: 5 * 60 * 1000,
    enabled: !!param,
  });
}

// 단건 조회
export function use{Domain}DetailQuery(id: string) {
  return useQuery({
    queryKey: {domain}Keys.detail(id),
    queryFn: () => {domain}Services.get{Resource}ById(id),
    staleTime: 5 * 60 * 1000,
    enabled: !!id,
  });
}

// 생성 뮤테이션
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

```typescript
// src/queries/index.ts (배럴 — 추가분)
export * from './{domain}';
```

---

## 4. View 템플릿

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

  return {
    data,
    isLoading,
    isError,
    searchParam,
    handleSearch,
  };
}
```

```typescript
// src/views/{page}/index.tsx
'use client';

import { use{Page}View } from './use{Page}View';

export default function {Page}View() {
  const {
    data,
    isLoading,
    isError,
    handleSearch,
  } = use{Page}View();

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p>로딩 중...</p>
      </div>
    );
  }

  if (isError) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p>오류가 발생했습니다.</p>
      </div>
    );
  }

  return (
    <main className="container mx-auto px-4 py-8">
      {/* UI 구현 */}
    </main>
  );
}
```

---

## 5. Component 템플릿

```typescript
// src/components/{Name}/use{Name}.ts
import { useState, useCallback } from 'react';

interface Use{Name}Props {
  // props
}

export function use{Name}({ }: Use{Name}Props = {}) {
  const [state, setState] = useState(false);

  const handleAction = useCallback(() => {
    setState((prev) => !prev);
  }, []);

  return {
    state,
    handleAction,
  };
}
```

```typescript
// src/components/{Name}/index.tsx
import { use{Name} } from './use{Name}';

interface {Name}Props {
  // props
}

export default function {Name}(props: {Name}Props) {
  const { state, handleAction } = use{Name}(props);

  return (
    <div>
      {/* UI */}
    </div>
  );
}
```

```typescript
// src/components/index.ts (배럴 — 추가분)
export { default as {Name} } from './{Name}';
```

---

## 6. Type 템플릿

```typescript
// src/types/api/{domain}.ts

export interface {Resource} {
  id: string;
  // 필드
  createdAt: string;
  updatedAt: string;
}

export interface {Resource}ListResponse {
  items: {Resource}[];
  total: number;
  page: number;
  pageSize: number;
}

export interface Create{Resource}Request {
  // 생성 필드
}
```

---

## 7. App Router page.tsx 템플릿

```typescript
// src/app/{route}/page.tsx
import type { Metadata } from 'next';
import {Page}View from '@/views/{page}';

export const metadata: Metadata = {
  title: '{페이지 제목}',
  description: '{설명}',
};

export default function Page() {
  return <{Page}View />;
}
```

---

## 8. Pages Router page.tsx 템플릿

```typescript
// pages/{route}/index.tsx
import type { NextPage } from 'next';
import {Page}View from '@/views/{page}';

const {Page}Page: NextPage = () => {
  return <{Page}View />;
};

export default {Page}Page;
```

---

## 9. SSR-safe localStorage Hook 템플릿

```typescript
// src/hooks/useLocalStorage.ts
import { useState, useEffect, useCallback } from 'react';

export function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(initialValue);

  useEffect(() => {
    try {
      const item = localStorage.getItem(key);
      if (item) setStoredValue(JSON.parse(item));
    } catch (error) {
      console.error(`localStorage 읽기 실패 [${key}]:`, error);
    }
  }, [key]);

  const setValue = useCallback(
    (value: T | ((prev: T) => T)) => {
      try {
        const valueToStore =
          value instanceof Function ? value(storedValue) : value;
        setStoredValue(valueToStore);
        localStorage.setItem(key, JSON.stringify(valueToStore));
      } catch (error) {
        console.error(`localStorage 저장 실패 [${key}]:`, error);
      }
    },
    [key, storedValue]
  );

  return [storedValue, setValue] as const;
}
```

---

## 10. QueryProvider 템플릿 (App Router)

```typescript
// src/provider/QueryProvider.tsx
'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { useState } from 'react';

export function QueryProvider({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 60 * 1000,
            retry: 1,
          },
        },
      })
  );

  return (
    <QueryClientProvider client={queryClient}>
      {children}
      {process.env.NODE_ENV === 'development' && (
        <ReactQueryDevtools initialIsOpen={false} />
      )}
    </QueryClientProvider>
  );
}
```
