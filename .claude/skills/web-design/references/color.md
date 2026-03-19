# 2025–2026 트렌드 컬러값

---

## 🟤 팬톤 2025 — 모카 무스 (Mocha Mousse)

| 이름          | HEX       | RGB           |
| ------------- | --------- | ------------- |
| Mocha Mousse  | `#9E7B5A` | 158, 123, 90  |
| 라이트 모카   | `#C4A882` | 196, 168, 130 |
| 딥 모카       | `#7D5F42` | 125, 95, 66   |
| 에스프레소    | `#5C3D2E` | 92, 61, 46    |
| 크림 (배경용) | `#FAF7F2` | 250, 247, 242 |

---

## 🌿 어스톤 (Earth Tones)

| 이름          | HEX       | RGB           |
| ------------- | --------- | ------------- |
| 올리브 그린   | `#6B7C45` | 107, 124, 69  |
| 세이지 그린   | `#8FAF7E` | 143, 175, 126 |
| 라이트 세이지 | `#C2D5B5` | 194, 213, 181 |
| 테라코타      | `#C4724A` | 196, 114, 74  |
| 번트 오렌지   | `#D4603A` | 212, 96, 58   |
| 머스타드      | `#D4A847` | 212, 168, 71  |
| 크림 베이지   | `#F5EFE0` | 245, 239, 224 |
| 오프화이트    | `#FDFAF5` | 253, 250, 245 |
| 웜 그레이     | `#A89880` | 168, 152, 128 |
| 다크 어스     | `#3B2218` | 59, 34, 24    |

---

## 🌑 다크 모드 (Dark Mode)

| 이름             | HEX       | RGB           |
| ---------------- | --------- | ------------- |
| 배경 (딥 네이비) | `#0A0E1A` | 10, 14, 26    |
| 서피스           | `#111827` | 17, 24, 39    |
| 카드             | `#1A2235` | 26, 34, 53    |
| 보더             | `#2D3A52` | 45, 58, 82    |
| 텍스트           | `#E2E8F0` | 226, 232, 240 |
| 뮤트 텍스트      | `#94A3B8` | 148, 163, 184 |

---

## ⚡ 네온 포인트 (다크 모드 포인트용)

| 이름          | HEX       | RGB          |
| ------------- | --------- | ------------ |
| 네온 그린     | `#00FF87` | 0, 255, 135  |
| 사이버 블루   | `#00D4FF` | 0, 212, 255  |
| 일렉트릭 퍼플 | `#BF5AF2` | 191, 90, 242 |
| 네온 옐로우   | `#F5FF00` | 245, 255, 0  |
| 핫 핑크       | `#FF2D78` | 255, 45, 120 |

---

## 🌸 소프트 파스텔 (웰니스 · 뷰티 · 라이프스타일)

| 이름        | HEX       | RGB           |
| ----------- | --------- | ------------- |
| 버터 크림   | `#FFF3D0` | 255, 243, 208 |
| 피치        | `#FFCBA4` | 255, 203, 164 |
| 더스티 로즈 | `#E8A0A0` | 232, 160, 160 |
| 라벤더      | `#C9B8E8` | 201, 184, 232 |
| 베이비 블루 | `#B8D8E8` | 184, 216, 232 |
| 민트        | `#B8E8D8` | 184, 232, 216 |
| 파우더 핑크 | `#F5D5E0` | 245, 213, 224 |

---

## 🔴 레트로 (Retro Revival)

| 이름            | HEX       | RGB           |
| --------------- | --------- | ------------- |
| 레트로 레드     | `#C0392B` | 192, 57, 43   |
| 머스타드 옐로우 | `#E8B84B` | 232, 184, 75  |
| 애비게일 그린   | `#2D6A4F` | 45, 106, 79   |
| 올드 블루       | `#2C5282` | 44, 82, 130   |
| 크림 화이트     | `#F5F0E8` | 245, 240, 232 |
| 다크 브라운     | `#4A2C2A` | 74, 44, 42    |
| 빈티지 오렌지   | `#E07B39` | 224, 123, 57  |

---

## 🎨 브루탈리즘 (Brutalism / Bold)

| 이름          | HEX       | RGB           |
| ------------- | --------- | ------------- |
| 퓨어 블랙     | `#0D0D0D` | 13, 13, 13    |
| 오프 화이트   | `#F5F5F0` | 245, 245, 240 |
| 브루탈 레드   | `#FF2800` | 255, 40, 0    |
| 브루탈 옐로우 | `#FFE500` | 255, 229, 0   |
| 브루탈 블루   | `#0057FF` | 0, 87, 255    |

---

## 🌙 다크모드 구현 (Tailwind + CSS Variables)

### 방법 1 — CSS 변수 + Tailwind `dark:` prefix (권장)

```ts
// tailwind.config.ts
export default {
  darkMode: 'class',  // HTML에 .dark 클래스 토글 방식
  theme: {
    extend: {
      colors: {
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        card: 'hsl(var(--card))',
        border: 'hsl(var(--border))',
        muted: 'hsl(var(--muted))',
        'muted-foreground': 'hsl(var(--muted-foreground))',
        primary: 'hsl(var(--primary))',
        'primary-foreground': 'hsl(var(--primary-foreground))',
      }
    }
  }
}
```

```css
/* app/globals.css */
:root {
  --background: 250 247 242;      /* 크림 오프화이트 */
  --foreground: 28 20 14;         /* 다크 브라운 */
  --card: 255 255 255;
  --border: 220 210 200;
  --muted: 245 239 224;
  --muted-foreground: 120 100 80;
  --primary: 158 123 90;          /* 모카 무스 */
  --primary-foreground: 255 255 255;
}

.dark {
  --background: 10 14 26;         /* 딥 네이비 */
  --foreground: 226 232 240;
  --card: 26 34 53;
  --border: 45 58 82;
  --muted: 17 24 39;
  --muted-foreground: 148 163 184;
  --primary: 0 255 135;           /* 네온 그린 포인트 */
  --primary-foreground: 10 14 26;
}
```

```tsx
// 다크모드 토글 버튼
'use client'
import { useEffect, useState } from 'react'

export function DarkModeToggle() {
  const [dark, setDark] = useState(false)
  useEffect(() => {
    document.documentElement.classList.toggle('dark', dark)
  }, [dark])
  return (
    <button onClick={() => setDark(!dark)}
      className="p-2 rounded-full transition-colors hover:bg-muted">
      {dark ? '☀️' : '🌙'}
    </button>
  )
}
```

### 방법 2 — next-themes 활용 (Next.js 권장)

```bash
npm install next-themes
```

```tsx
// app/providers.tsx
'use client'
import { ThemeProvider } from 'next-themes'
export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      {children}
    </ThemeProvider>
  )
}

// app/layout.tsx
import { Providers } from './providers'
export default function RootLayout({ children }) {
  return (
    <html lang="ko" suppressHydrationWarning>
      <body><Providers>{children}</Providers></body>
    </html>
  )
}
```

```tsx
// 다크모드 토글 컴포넌트
'use client'
import { useTheme } from 'next-themes'
export function ThemeToggle() {
  const { theme, setTheme } = useTheme()
  return (
    <button onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
      className="p-2 rounded-full hover:bg-muted transition-colors">
      {theme === 'dark' ? '☀️' : '🌙'}
    </button>
  )
}
```

### Tailwind에서 다크모드 색상 적용

```tsx
// 컴포넌트에서 dark: prefix 사용
<div className="bg-background text-foreground">
  <div className="bg-card border border-border rounded-xl p-6">
    <h2 className="text-foreground font-bold">제목</h2>
    <p className="text-muted-foreground text-sm">설명 텍스트</p>
    <button className="bg-primary text-primary-foreground px-4 py-2 rounded-lg
      hover:opacity-90 transition-opacity">
      버튼
    </button>
  </div>
</div>

// CSS 변수 방식을 쓰면 dark: prefix 없이 자동 전환됨
// 스타일별 추천 다크모드 컬러:
// 어스톤 라이트 → 다크 네이비 배경 + 크림 텍스트
// 소프트 파스텔 → 딥 퍼플/네이비 배경 + 라이트 파스텔 포인트
// 브루탈리즘 → 퓨어 블랙 배경 + 오프화이트 텍스트 (이미 다크 친화적)
```
