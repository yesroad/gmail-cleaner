---
name: web-design
description: 2025-2026 트렌드를 반영한 웹/앱 UI를 Next.js + TailwindCSS + shadcn/ui로 구현하는 전문 디자인 스킬. 페이지, 컴포넌트, 사이트, 랜딩페이지, 대시보드, 앱 화면 등 시각적 UI 관련 작업이라면 반드시 이 스킬을 사용할 것. "만들어줘", "디자인해줘", "구현해줘", "예쁘게", "트렌디하게", "화면 만들어줘" 같은 요청 포함. Next.js, TailwindCSS, shadcn/ui가 언급되거나 웹/앱 UI를 다루는 상황 전반에 적용.
---

# Web Design Skill — 2025-2026 트렌드 기반 UI 구현

당신은 최신 디자인 트렌드를 깊이 이해하고 Next.js + TailwindCSS + shadcn/ui로 실제 동작하는 코드를 만드는 전문가입니다.

---

## Step 0: 프로젝트 환경 파악 (항상 먼저 실행)

작업 디렉토리의 `package.json`을 읽어 다음을 확인하세요:

| 항목               | 확인 내용                     | 영향                                                                |
| ------------------ | ----------------------------- | ------------------------------------------------------------------- |
| `next` 버전        | v14 vs v15                    | v15는 `params`, `searchParams`, `cookies()`, `headers()` 모두 async |
| `tailwindcss` 버전 | v3 vs v4                      | v4는 `tailwind.config.ts` 대신 `globals.css @theme` CSS-first 방식  |
| `framer-motion`    | 설치 여부                     | 고급 인터랙션(패럴랙스, 키네틱 타이포) 사용 가능 여부               |
| `shadcn/ui`        | 설치 여부 (`@/components/ui`) | 베이스 컴포넌트 사용 가능 여부                                      |

**이 스킬의 기본값은 Tailwind v4 + Next.js v15입니다.** package.json에서 다른 버전이 확인되면 해당 버전에 맞는 문법으로 전환하세요.

---

## Step 1: 컨텍스트 파악

사용자 요청에서 다음을 파악하세요:

- **타입**: 랜딩페이지 / 대시보드 / e-커머스 / 포트폴리오 / SaaS / 앱 화면 / 단일 컴포넌트 / 기타
- **업종/분야**: 테크, 라이프스타일, 뷰티, 푸드, 에이전시, 금융 등
- **분위기**: 사용자가 언급했다면 반영, 아니라면 Step 2에서 선택받기

**단일 컴포넌트나 간단한 요청**은 Step 2를 생략하고 가장 어울리는 스타일로 바로 진행해도 됩니다.

---

## Step 2: 디자인 스타일 선택 제안

**다음 중 하나라도 해당하면 Step 3으로 바로 진행하세요:**

- 스타일/분위기 키워드가 명시된 경우 (예: "어두운", "미니멀", "파스텔", "어스톤", "레트로")
- 단일 컴포넌트 요청
- 기존 프로젝트에 컴포넌트를 추가하는 경우

**"다크모드로 만들어줘"는 스타일 선택이 아닌 기능 요구사항입니다.** 다크모드 기능을 구현하되, 스타일(어스톤/다크테크/파스텔 등)은 별도로 결정하세요.

스타일이 불명확한 경우, Step 1에서 파악한 **업종과 타입을 기반으로 가장 어울리는 3가지**를 추려 제안하세요:

**업종별 스타일 궁합**

| 업종/분야                  | 어울리는 스타일 (우선순위 순)                   |
| -------------------------- | ----------------------------------------------- |
| 라이프스타일, 푸드, 웰니스 | 어스톤 미니멀 → 소프트 파스텔 → 레트로 리바이벌 |
| SaaS, 테크, 스타트업       | 다크 테크 → 볼드 브루탈리즘 → 어스톤 미니멀     |
| 뷰티, 패션, 럭셔리         | 소프트 파스텔 → 어스톤 미니멀 → 레트로 리바이벌 |
| 포트폴리오, 에이전시, 아트 | 볼드 브루탈리즘 → 다크 테크 → 레트로 리바이벌   |
| 금융, 기업, B2B            | 어스톤 미니멀 → 다크 테크                       |
| e-커머스, 쇼핑             | 어스톤 미니멀 → 소프트 파스텔 → 다크 테크       |

**제안 형식** (3가지만 추려서):

```
🎨 어떤 스타일로 만들까요?

A. 어스톤 미니멀
   따뜻한 모카·테라코타·크림 팔레트, 깔끔한 여백 중심 레이아웃
   → 라이프스타일, 브랜드, 웰니스, 푸드 사이트에 어울려요

B. 다크 테크
   딥 네이비 배경 + 네온 포인트 컬러, 날카롭고 현대적인 인상
   → SaaS, 테크 스타트업, 게임, 크리에이티브 에이전시에 어울려요

C. 소프트 파스텔
   라벤더·피치·버터크림 계열, 부드럽고 친근한 느낌
   → 뷰티, 웰니스, 교육, 아동 서비스에 어울려요

⭐ 클로드 추천: [선택지 + 이유 1줄]
```

---

## Step 3: 레이아웃 패턴 결정

`references/layout.md`를 참고해 타입에 맞는 패턴을 선택하세요:

| 타입                | 권장 패턴                                     |
| ------------------- | --------------------------------------------- |
| 랜딩페이지          | Above-the-fold CTA + Storytelling 스크롤 구조 |
| 대시보드/앱         | 벤토 박스 레이아웃                            |
| 포트폴리오/에이전시 | 탈구축 히어로 + Bold Kinetic Typography       |
| e-커머스            | 그리드 중심 + 마이크로인터랙션 강조           |
| 단일 컴포넌트       | 해당 컴포넌트의 용도에 맞는 스타일            |

### 반응형 설계 원칙

Mobile-First로 설계하세요. Tailwind 브레이크포인트 기준:

| 접두사 | min-width | 대상                  |
| ------ | --------- | --------------------- |
| (기본) | 0px       | 모바일                |
| `sm`   | 640px     | 대형 폰 / 소형 태블릿 |
| `md`   | 768px     | 태블릿                |
| `lg`   | 1024px    | 소형 데스크톱         |
| `xl`   | 1280px    | 대형 데스크톱         |
| `2xl`  | 1536px    | 울트라와이드          |

Tailwind v4에서는 `@container` 쿼리가 기본 내장됩니다. 컴포넌트가 부모 크기에 따라 레이아웃을 바꿔야 할 때 `@container` + `@sm:` / `@md:` 활용을 적극 검토하세요.

---

## Step 3.5: HTML 목업 작성 및 사용자 확인 (필수)

> **왜 필수인가?** HTML 목업은 "디자인 계약서"입니다. React 구현 전에 색상·레이아웃·상태(state)·인터랙션을 사용자와 합의해두면, 컴포넌트 구현 중 방향 수정이 없어집니다. 작은 수정(텍스트 정렬, 색상 변경, 요소 제거)을 HTML에서 하는 것이 React 코드를 고치는 것보다 훨씬 빠릅니다.

**다음 경우에만 생략 가능:**

- 단일 버튼/뱃지처럼 명백히 단순한 컴포넌트 1개 추가
- 사용자가 "목업 없이 바로 구현해줘"라고 명시한 경우

### 목업 파일 생성 규칙

파일 위치: `docs/{project-name}-mockup.html`
(docs 폴더가 없으면 프로젝트 루트에 `{project-name}-mockup.html`로 저장)

### 목업에 반드시 포함할 내용

**1. 상단 목업 네비게이션 바**

```html
<!-- 목업임을 명확히 표시 -->
<nav
  style="position:fixed; top:0; background:#1a1a1a; color:#fff; padding:8px 16px; font-size:13px; z-index:9999; display:flex; gap:8px; align-items:center;"
>
  <span
    style="background:#c4724a; color:#fff; padding:2px 8px; border-radius:99px; font-size:11px; font-weight:700;"
    >MOCKUP</span
  >
  <span>{프로젝트명} — UI 목업</span>
</nav>
```

**2. 디자인 시스템 섹션 (컬러 팔레트 스와치)**
선택한 스타일의 주요 컬러를 시각적으로 표시

**3. 모든 컴포넌트를 개별 섹션으로**
각 섹션마다 점선 테두리 + 라벨로 구분:

```html
<div
  style="border: 2px dashed #ddd; border-radius:12px; padding:24px; margin-bottom:32px; position:relative;"
>
  <span
    style="position:absolute; top:-12px; left:16px; background:#333; color:#fff; font-size:11px; padding:3px 10px; border-radius:99px; text-transform:uppercase;"
    >ComponentName</span
  >
  <!-- 컴포넌트 내용 -->
</div>
```

**4. 각 컴포넌트의 주요 상태 표시**

| 상태          | 설명                                |
| ------------- | ----------------------------------- |
| 기본          | 기본 렌더링 상태                    |
| hover         | CSS `:hover`로 마우스 오버 효과     |
| 로딩/스켈레톤 | shimmer 애니메이션 (데이터 패칭 UI) |
| 비어있음      | 결과 없음 / 초기 상태               |
| 에러          | 실패/경고 상태 (해당하는 경우)      |

**5. 전체 레이아웃 미리보기 섹션**
실제 페이지처럼 조합된 최종 레이아웃을 마지막에 표시

### 목업 CSS 원칙

- **외부 의존성 없이** 순수 HTML + CSS + 인라인 스타일만 사용 (브라우저에서 즉시 열 수 있어야 함)
- CSS 변수로 컬러 토큰 정의 (`--color-primary` 등)
- hover 효과는 CSS만으로 구현 (JS 최소화)
- `break-keep: always`로 한국어 줄바꿈 처리
- 스켈레톤 shimmer는 `@keyframes` + `background: linear-gradient(90deg, ...)` 패턴 사용

### 사용자 확인 절차

목업 파일 생성 후 **반드시 다음 메시지로 사용자에게 확인을 요청**하세요:

```
docs/{파일명}.html 에 목업을 생성했습니다.
브라우저에서 열어서 확인해보세요.

수정하고 싶은 부분이 있으면 말씀해 주세요.
확정되면 React 컴포넌트 구현을 시작하겠습니다.
```

**사용자가 수정을 요청하면:**

- HTML 파일만 수정 (React 코드 작성 금지)
- 수정 완료 후 다시 확인 요청

**사용자가 확인("좋아", "진행하자", "OK" 등)하면:**
→ Step 4로 진행

---

## Step 4: 구현

### Tailwind v4 설정 (CSS-first)

`tailwind.config.ts` 대신 `globals.css`에서 `@theme`으로 커스텀 토큰을 정의합니다. `references/color.md`에서 선택된 스타일의 정확한 HEX값을 사용하세요.

```css
/* app/globals.css */
@import "tailwindcss";

/* 다크모드 variant — next-themes의 .dark 클래스 방식 */
@custom-variant dark (&:where(.dark, .dark *));

@theme {
  /* 어스톤 스타일 예시 — 선택된 스타일에 맞게 교체 */
  --color-mocha: #9e7b5a;
  --color-mocha-light: #c4a882;
  --color-mocha-dark: #7d5f42;
  --color-mocha-deep: #5c3d2e;
  --color-cream: #faf7f2;
  --color-sage: #8faf7e;
  --color-terracotta: #c4724a;

  /* 폰트 (next/font 변수와 연결) */
  --font-sans: var(--font-pretendard), sans-serif;
  --font-display: var(--font-fraunces), serif;

  /* 커스텀 애니메이션 */
  --animate-shake: shake 0.3s ease-in-out;

  @keyframes shake {
    0%,
    100% {
      transform: translateX(0);
    }
    25% {
      transform: translateX(-4px);
    }
    75% {
      transform: translateX(4px);
    }
  }
}

/* 다크모드 CSS 변수 전환 */
:root {
  --background: #faf7f2;
  --foreground: #1c140e;
  --card: #ffffff;
  --border: #dcd2c8;
  --muted: #f5efe0;
  --muted-foreground: #78644f;
  --primary: #9e7b5a;
  --primary-foreground: #ffffff;
}

.dark {
  --background: #0a0e1a;
  --foreground: #e2e8f0;
  --card: #1a2235;
  --border: #2d3a52;
  --muted: #111827;
  --muted-foreground: #94a3b8;
  --primary: #00ff87;
  --primary-foreground: #0a0e1a;
}
```

> **Tailwind v3인 경우**: `globals.css @theme` 대신 기존 `tailwind.config.ts`의 `theme.extend.colors`에 커스텀 컬러를 정의하세요. 다크모드는 `darkMode: 'class'` 설정 후 CSS variables 방식 사용.

### 컴포넌트 코드 원칙

- **shadcn/ui를 베이스**로 사용하고 Tailwind로 커스터마이징
- **Next.js App Router** 기준 작성 (서버 컴포넌트 우선, 클라이언트 인터랙션 필요 시 `'use client'`)
- **Next.js v15**: `params`, `searchParams`는 async props, `cookies()`·`headers()`는 await 필요
- **`next/image`** 사용, **`next/font`**로 폰트 최적화 (`references/fonts.md` 참고)
- 이미지 포맷은 WebP/AVIF 우선 권장

### 타이포그래피

`references/typography.md`를 참고해 다음을 적용하세요:

- **줄 간격**: 본문은 1.5~1.6 (단위 없는 상대값, px 금지)
- **폰트 크기 스케일**: `clamp()`를 활용한 유체 타이포그래피, 본문 최소 16px
- **자간**: 대형 헤드라인은 -0.01em~-0.02em
- **정렬**: 본문은 왼쪽 정렬 기본, 중앙 정렬은 히어로 섹션/짧은 캡션만
- **최적 콘텐츠 너비**: 한국어 본문 `max-width: 600px`, 영문 본문 `max-width: 720px`

```tsx
// ✅ 타이포그래피 예
<p className="text-base leading-relaxed max-w-[600px]">  {/* 한국어 본문 */}</p>

<h1 className="text-[clamp(1.75rem,5vw,3rem)] leading-tight tracking-tight">
  {/* 유체 타이포그래피 */}
</h1>
```

### 스페이싱 (간격 시스템)

`references/spacing.md`를 참고해 8px 그리드 기반으로 설계하세요:

- **기본 토큰**: XS(4px) → S(8px) → M(16px) → L(32px) → XL(64px)
- **모바일 여백**: 사이드 16px, 섹션 32px
- **데스크톱 여백**: 사이드 24~32px, 섹션 64~96px
- **핵심 원칙**: 내부 패딩 ≤ 외부 마진 (게슈탈트 근접성 법칙)

### 인터랙션

`references/interaction.md`를 읽어 요청 복잡도에 따라 적용하세요:

- **기본 (항상 포함)**: 버튼 hover/active 피드백, 폼 에러 흔들림
- **중간 (일반 페이지/컴포넌트)**: 스켈레톤 UI, 스크롤 reveal, 완료 애니메이션
- **고급 (랜딩페이지, 포트폴리오 등)**: 패럴랙스 스크롤, 다이나믹 커서, Bold Kinetic Typography 스크롤 연동

고급 인터랙션은 **Framer Motion**이 필요합니다. package.json에 없으면 Step 5 설치 패키지에 포함하세요.

### 접근성 — 타협 불가

```tsx
// 색상 대비 4.5:1 이상 유지
<Button aria-label="장바구니에 추가">

// 터치 타깃 최소 44×44px
className="min-h-[44px] min-w-[44px]"

// 포커스 인디케이터
className="focus-visible:ring-2 focus-visible:ring-offset-2"

// 애니메이션 접근성
<motion.div className="motion-reduce:animate-none">

// 한국어 텍스트 줄바꿈
className="break-keep"
```

---

## Step 4.5: 여백·간격·개행 품질 체크

코드 생성 직후, Step 5 출력 전에 반드시 점검하세요. `references/spacing.md` 참고.

**스페이싱 체크:**

- 모든 여백/패딩/간격이 4 또는 8의 배수인가? (4, 8, 16, 24, 32, 40, 48, 64, 96px)
- 컴포넌트 내부 패딩 ≤ 컴포넌트 간 여백인가?
- 헤드라인 주변 여백이 충분한가? (기존 대비 20% 이상)
- 모바일/태블릿/데스크톱 여백이 단계별로 올바른가?

**타이포그래피 체크:**

- 버튼 padding이 텍스트에 비례하는가? (최소 44×44px 터치 타겟)
- 본문 줄 간격이 1.5 이상인가?
- 폰트 크기가 `clamp()`로 유체 대응하는가?
- 나란히 배치된 요소들의 `gap`이 일관적인가?

**레이아웃 체크:**

- 가격·버튼 등 밀도 높은 영역에서 요소가 잘리거나 넘치지 않는가?
- 한국어 텍스트에 `break-keep`이 적용되었는가?
- `text-center` 단락 마지막 줄에 단어 한두 개만 남지 않는가?
- 모바일(375px) 기준 레이아웃이 깨지지 않는가?
- 울트라와이드(1440px+)에서 콘텐츠 너비가 고정되고 여백이 확장되는가?

---

## Step 5: 출력물 구성

**항상 다음 순서로 출력하세요:**

### 1. 디자인 결정 요약 (텍스트, 코드 전에 먼저)

코드를 출력하기 전에 다음을 간략히 설명하세요. 사용자가 방향을 확인하고 수정 요청할 수 있는 기회를 줍니다:

```
스타일: [선택된 스타일] — [선택 이유 1줄]
레이아웃: [사용한 패턴] — [이유 1줄]
컬러: [주요 컬러 3~4개]
인터랙션: [적용 수준 + 주요 효과]
폰트: [헤드라인 폰트] + [본문 폰트]
```

### 2. `globals.css` (Tailwind v4 @theme 포함)

커스텀 컬러 토큰, 다크모드 CSS 변수, 커스텀 애니메이션, 폰트 연결.

### 3. 컴포넌트/페이지 코드

완성된 Next.js + Tailwind + shadcn/ui 코드. 실제로 복사해서 쓸 수 있는 수준으로.

### 4. `design-summary.md` 파일 저장

```md
# Design Summary

## 스타일

[선택된 스타일과 선택 이유]

## 레이아웃

[사용한 레이아웃 패턴과 이유]

## 컬러 팔레트

[주요 컬러와 선택 이유]

## 인터랙션

[적용한 인터랙션과 이유]
```

### 5. 추가 설치 패키지 (있을 경우)

```bash
yarn add framer-motion        # 고급 인터랙션 시
yarn add next-themes          # 다크모드 시
npx shadcn@latest add [컴포넌트]
```

---

## 레퍼런스 파일

필요할 때 해당 파일을 읽어 정확한 값을 사용하세요:

- **컬러 팔레트 HEX값 + 다크모드 구현**: `references/color.md`
- **인터랙션 패턴 + 구현 코드**: `references/interaction.md`
- **레이아웃 패턴 치트시트**: `references/layout.md`
- **트렌드 종합 보고서**: `references/trend.md`
- **폰트 추천 / 업종별 조합 / 구현**: `references/fonts.md`
- **타이포그래피 (줄간격, 자간, 폰트 크기 스케일)**: `references/typography.md`
- **스페이싱 시스템 (8px 그리드, 여백 브레이크포인트)**: `references/spacing.md`
- **반응형 브레이크포인트**: `references/responsive.md`
