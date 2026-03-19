# Pages Router 전용 패턴

> Next.js Pages Router (`pages/` 디렉토리 존재 시 적용)
> App Router 규칙과 뷰/서비스/쿼리 패턴은 동일 — 라우트 파일 위치만 다름

---

## 전체 폴더 구조

```
pages/                           # Next.js Pages Router 라우트
├── _app.tsx                     # 전역 레이아웃 (QueryProvider 등)
├── _document.tsx                # HTML 문서 커스텀
├── index.tsx                    # 홈 → HomeView 위임
└── {route}/
    └── index.tsx                # 페이지 → {Page}View 위임만

src/
├── views/                       # 뷰 레이어 (pages와 1:1 대응)
│   └── {page}/
│       ├── index.tsx            # {Page}View
│       ├── use{Page}View.ts     # 페이지 로직 훅
│       └── components/
│           └── {Component}/
│               ├── index.tsx
│               └── use{Component}.ts
│
├── components/                  # 앱 공통 컴포넌트
├── services/api/                # API 서비스
├── queries/                     # TanStack Query 훅
├── types/                       # 타입 정의
├── lib/                         # 순수 유틸리티
└── hooks/                       # 공통 커스텀 훅
```

---

## pages/{route}/index.tsx 패턴

```typescript
// pages/{route}/index.tsx
import type { NextPage } from 'next';
import {Page}View from '@/views/{page}';

const {Page}Page: NextPage = () => {
  return <{Page}View />;
};

export default {Page}Page;
```

### getServerSideProps / getStaticProps

서버 사이드 데이터가 필요한 경우:

```typescript
// pages/{route}/index.tsx
import type { GetServerSideProps, NextPage } from 'next';
import {Page}View from '@/views/{page}';

interface Props {
  initialData: {DataType};
}

const {Page}Page: NextPage<Props> = ({ initialData }) => {
  return <{Page}View initialData={initialData} />;
};

export const getServerSideProps: GetServerSideProps = async (context) => {
  const data = await fetch{Data}();
  return {
    props: { initialData: data },
  };
};

export default {Page}Page;
```

---

## views/{page}/ 패턴

App Router와 동일한 구조를 사용한다.

### index.tsx

```typescript
// src/views/{page}/index.tsx
import { use{Page}View } from './use{Page}View';

interface Props {
  initialData?: {DataType}; // getServerSideProps에서 받은 경우
}

export default function {Page}View({ initialData }: Props = {}) {
  const {
    data,
    isLoading,
    handleAction,
  } = use{Page}View({ initialData });

  if (isLoading) return <div>로딩 중...</div>;

  return (
    <main>
      {/* UI만 */}
    </main>
  );
}
```

### use{Page}View.ts

```typescript
// src/views/{page}/use{Page}View.ts
import { useState } from 'react';
import { use{Domain}Query } from '@/queries/{domain}';

interface Options {
  initialData?: {DataType};
}

export function use{Page}View({ initialData }: Options = {}) {
  const [input, setInput] = useState('');

  const { data, isLoading } = use{Domain}Query(input, {
    initialData, // getServerSideProps에서 받은 경우 hydration
  });

  return {
    data,
    isLoading,
    handleAction: setInput,
  };
}
```

---

## _app.tsx — QueryProvider 설정

```typescript
// pages/_app.tsx
import type { AppProps } from 'next/app';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useState } from 'react';
import '@/styles/globals.css';

export default function App({ Component, pageProps }: AppProps) {
  const [queryClient] = useState(() => new QueryClient());

  return (
    <QueryClientProvider client={queryClient}>
      <Component {...pageProps} />
    </QueryClientProvider>
  );
}
```

---

## API Routes 패턴

```
pages/api/
└── {domain}/
    └── index.ts      # GET, POST 등
```

```typescript
// pages/api/{domain}/index.ts
import type { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  try {
    const data = await externalApi.get(req.query.param as string);
    res.status(200).json(data);
  } catch (error) {
    res.status(500).json({ error: '요청 실패' });
  }
}
```

---

## SSR-safe localStorage (Pages Router)

Pages Router에서도 SSR 시 `localStorage`는 없다. App Router와 동일한 패턴 사용.

```typescript
// ❌ 금지
const [items, setItems] = useState<Item[]>(() =>
  JSON.parse(localStorage.getItem('items') ?? '[]')
);

// ✅ 필수
const [items, setItems] = useState<Item[]>([]);
useEffect(() => {
  const stored = localStorage.getItem('items');
  if (stored) setItems(JSON.parse(stored));
}, []);
```

---

## App Router vs Pages Router 비교

| 항목 | App Router | Pages Router |
|---|---|---|
| 라우트 파일 위치 | `src/app/{route}/page.tsx` | `pages/{route}/index.tsx` |
| 전역 레이아웃 | `src/app/layout.tsx` | `pages/_app.tsx` |
| Provider 주입 | `layout.tsx`에서 | `_app.tsx`에서 |
| 서버 데이터 | async Server Component | `getServerSideProps` / `getStaticProps` |
| API Routes | `src/app/api/{domain}/route.ts` | `pages/api/{domain}/index.ts` |
| 뷰 구조 | `src/views/` (동일) | `src/views/` (동일) |
| 서비스/쿼리 구조 | `src/services/`, `src/queries/` (동일) | (동일) |
