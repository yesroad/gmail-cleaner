# App Router 전용 패턴

> Next.js 13+ App Router (`src/app/` 디렉토리 존재 시 적용)

---

## 전체 폴더 구조

```
src/
├── app/                         # Next.js App Router 라우트
│   ├── layout.tsx               # 루트 레이아웃 (Server Component)
│   ├── page.tsx                 # 홈 페이지 → HomeView 위임
│   └── {route}/
│       ├── page.tsx             # 페이지 → {Page}View 위임만
│       └── layout.tsx           # (선택) 중첩 레이아웃
│
├── views/                       # 뷰 레이어 (페이지별 UI + 로직 훅)
│   └── {page}/
│       ├── index.tsx            # 기본 export: {Page}View
│       ├── use{Page}View.ts     # 페이지 로직 훅
│       └── components/          # 뷰 전용 컴포넌트
│           └── {Component}/
│               ├── index.tsx
│               └── use{Component}.ts
│
├── components/                  # 앱 공통 컴포넌트
├── services/api/                # API 서비스
├── queries/                     # TanStack Query 훅
├── types/                       # 타입 정의
├── lib/                         # 순수 유틸리티
├── hooks/                       # 공통 커스텀 훅
└── provider/                    # QueryProvider 등
```

---

## app/{route}/page.tsx 패턴

페이지 파일은 **뷰 위임만** 한다. 로직 없음.

```typescript
// app/{route}/page.tsx
import {Page}View from '@/views/{page}';

export default function Page() {
  return <{Page}View />;
}

// 메타데이터가 필요한 경우
export const metadata = {
  title: '{페이지 제목}',
  description: '{설명}',
};
```

---

## views/{page}/ 패턴

### index.tsx — UI 전담

```typescript
// views/{page}/index.tsx
'use client'; // 상태/이벤트가 있으면 필수

import { use{Page}View } from './use{Page}View';

export default function {Page}View() {
  const {
    data,
    isLoading,
    handleSubmit,
  } = use{Page}View();

  if (isLoading) return <div>로딩 중...</div>;

  return (
    <main>
      {/* UI만 */}
    </main>
  );
}
```

### use{Page}View.ts — 로직 훅

```typescript
// views/{page}/use{Page}View.ts
'use client';

import { useState } from 'react';
import { use{Domain}Query } from '@/queries/{domain}';

export function use{Page}View() {
  const [input, setInput] = useState('');
  const { data, isLoading } = use{Domain}Query(input);

  const handleSubmit = (value: string) => {
    setInput(value);
  };

  return {
    data,
    isLoading,
    handleSubmit,
  };
}
```

---

## Server Component vs Client Component 분기

| 상황 | 컴포넌트 종류 | 파일 상단 |
|---|---|---|
| 데이터 패칭만 (no state/event) | Server Component | 선언 불필요 |
| useState, useEffect, 이벤트 | Client Component | `'use client'` |
| TanStack Query 사용 | Client Component | `'use client'` |
| 뷰 로직 훅 파일 | Client Component | `'use client'` |

### 병렬 데이터 패칭 (Server Component)

```typescript
// views/{page}/index.tsx (Server Component — 'use client' 없음)
import { Suspense } from 'react';
import ProfileSection from './components/ProfileSection';
import PostsSection from './components/PostsSection';

export default function {Page}View() {
  return (
    <main>
      <Suspense fallback={<ProfileSkeleton />}>
        <ProfileSection />   {/* 독립적으로 fetch */}
      </Suspense>
      <Suspense fallback={<PostsSkeleton />}>
        <PostsSection />     {/* 독립적으로 fetch */}
      </Suspense>
    </main>
  );
}
```

---

## API Route 패턴

```
src/app/api/
└── {domain}/
    └── route.ts
```

```typescript
// app/api/{domain}/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const param = searchParams.get('param');

  try {
    const data = await externalApi.get(param);
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json({ error: '요청 실패' }, { status: 500 });
  }
}
```

---

## SSR-safe localStorage (App Router)

Client Component에서도 서버 렌더링 시 `localStorage`는 존재하지 않는다.

```typescript
// ❌ 금지: SSR에서 ReferenceError 발생
const [items, setItems] = useState<Item[]>(() =>
  JSON.parse(localStorage.getItem('items') ?? '[]')
);

// ✅ 필수: useEffect로 지연 로드
const [items, setItems] = useState<Item[]>([]);

useEffect(() => {
  const stored = localStorage.getItem('items');
  if (stored) setItems(JSON.parse(stored));
}, []);
```

---

## provider/ 구조

```typescript
// provider/QueryProvider.tsx
'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useState } from 'react';

export function QueryProvider({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient());
  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
}
```

```typescript
// app/layout.tsx
import { QueryProvider } from '@/provider/QueryProvider';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <body>
        <QueryProvider>{children}</QueryProvider>
      </body>
    </html>
  );
}
```
