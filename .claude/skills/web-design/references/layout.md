# 레이아웃 패턴 치트시트 (2025–2026)

트렌드 배경 및 상세 설명은 `trend.md` 참고. 이 파일은 **어떤 타입에 어떤 패턴을 쓸지** 빠르게 결정하기 위한 치트시트입니다.

---

## 타입별 권장 패턴

| 타입 | 주 패턴 | 보조 패턴 |
|------|---------|-----------|
| 랜딩페이지 | Above-the-fold CTA | 스토리텔링 스크롤 + Kinetic Typography |
| SaaS 랜딩 | Above-the-fold CTA | 벤토 박스 (피처 소개) |
| 대시보드 | 벤토 박스 | 사이드바 + 그리드 |
| 앱 화면 | 카드 그리드 | 탭 내비게이션 |
| 포트폴리오 | 탈구축 히어로 | Bold Kinetic Typography |
| 에이전시 사이트 | 탈구축 히어로 | 풀스크린 스크롤 |
| e-커머스 | 카드 그리드 | 필터 사이드바 |
| 블로그/미디어 | 에디토리얼 그리드 | 카드 리스트 |

---

## 패턴별 핵심 구조

### 벤토 박스 레이아웃

다양한 크기의 카드를 격자에 빈틈 없이 배치. 레이아웃 자체가 정보 위계를 표현.

```tsx
// CSS Grid로 구현
<div className="grid grid-cols-4 grid-rows-3 gap-4 auto-rows-[200px]">
  <div className="col-span-2 row-span-2 bg-card rounded-2xl p-6">히어로 카드</div>
  <div className="col-span-1 row-span-1 bg-card rounded-2xl p-4">작은 카드</div>
  <div className="col-span-1 row-span-1 bg-card rounded-2xl p-4">작은 카드</div>
  <div className="col-span-2 row-span-1 bg-card rounded-2xl p-4">와이드 카드</div>
  <div className="col-span-1 row-span-1 bg-card rounded-2xl p-4">작은 카드</div>
  <div className="col-span-1 row-span-1 bg-card rounded-2xl p-4">작은 카드</div>
</div>

// 반응형: 모바일은 1열
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
```

**어울리는 곳:** Apple 제품 소개, Linear, Vercel, iOS 위젯 스타일 대시보드

---

### Above-the-fold CTA

핵심 정보와 CTA를 스크롤 없이 보이는 영역에 집중. fold 위 CTA는 아래 대비 전환율 304% 우위.

```tsx
<section className="min-h-screen flex flex-col justify-center items-center text-center px-4">
  <h1 className="text-[clamp(3rem,8vw,7rem)] font-black break-keep leading-tight">
    핵심 헤드라인
  </h1>
  <p className="text-lg text-muted-foreground mt-4 max-w-xl break-keep">
    서브 메시지 (간결하게)
  </p>
  <div className="mt-8 flex gap-4">
    <Button size="lg">지금 시작하기</Button>
    <Button size="lg" variant="outline">더 알아보기</Button>
  </div>
</section>
```

**어울리는 곳:** SaaS 랜딩, 제품 소개, 프로모션 페이지

---

### 탈구축(Deconstructed) 히어로

대칭·정렬을 의도적으로 깨서 실험적·독창적 인상. 텍스트·이미지·요소가 겹치고 기울어지며 배치됨.

```tsx
<section className="relative min-h-screen overflow-hidden">
  {/* 대형 배경 텍스트 */}
  <h1 className="absolute top-8 left-0 text-[20vw] font-black text-foreground/10 leading-none select-none">
    BRAND
  </h1>
  {/* 메인 이미지 (비대칭 배치) */}
  <div className="absolute top-16 right-8 w-1/2 aspect-square rounded-2xl overflow-hidden">
    <Image src="..." fill className="object-cover" alt="" />
  </div>
  {/* 오버레이 텍스트 */}
  <div className="relative z-10 mt-40 ml-12 max-w-sm">
    <p className="text-sm uppercase tracking-widest text-muted-foreground">브랜드 레이블</p>
    <h2 className="text-5xl font-bold mt-2 leading-tight break-keep">
      당신의<br />이야기를<br />만듭니다
    </h2>
    <Button className="mt-6">작업 보기</Button>
  </div>
</section>
```

**어울리는 곳:** 포트폴리오, 크리에이티브 에이전시, 아트 프로젝트

---

### Bold Kinetic Typography

타이포그래피 자체가 비주얼. 이미지 없이도 임팩트 있는 첫인상.

```tsx
// 정적 버전
<section className="min-h-screen flex items-center overflow-hidden bg-black text-white">
  <div>
    <h1 className="text-[clamp(5rem,15vw,12rem)] font-black uppercase leading-none whitespace-nowrap">
      MAKE IT
    </h1>
    <h1 className="text-[clamp(5rem,15vw,12rem)] font-black uppercase leading-none whitespace-nowrap
      -mt-4 ml-[10vw] text-transparent [-webkit-text-stroke:2px_white]">
      HAPPEN
    </h1>
  </div>
</section>

// 스크롤 연동 버전 → interaction.md의 KineticHeadline 컴포넌트 참고
```

**어울리는 곳:** 포트폴리오 히어로, 에이전시 랜딩, 브루탈리즘 디자인

---

### 스토리텔링 스크롤 구조

스크롤에 따라 콘텐츠가 서서히 드러나며 서사를 만드는 구조.

```
스크롤 ↓ 순서:
1. 공감 — "이런 문제 있으신가요?" (히어로)
2. 긴장감 — 문제 심화 + 데이터 (reveal on scroll)
3. 해소 — "저희가 해결했습니다" (솔루션 소개)
4. 신뢰 — 사례/리뷰 (소셜 프루프)
5. 행동 — CTA (마지막 섹션)
```

→ 각 섹션에 RevealOnScroll 컴포넌트 적용 (`interaction.md` 참고)

---

### 에디토리얼 그리드 (블로그/미디어)

```tsx
// 피처 아티클 + 서브 아티클 혼합 그리드
<div className="grid grid-cols-1 md:grid-cols-3 gap-6">
  {/* 피처 아티클 - 넓게 */}
  <article className="md:col-span-2 group cursor-pointer">
    <div className="aspect-[16/9] rounded-xl overflow-hidden">
      <Image src="..." fill className="object-cover group-hover:scale-105 transition-transform duration-500" alt="" />
    </div>
    <h2 className="text-2xl font-bold mt-4 break-keep">피처 아티클 제목</h2>
  </article>
  {/* 서브 아티클 목록 */}
  <div className="flex flex-col gap-4">
    {articles.map(a => <ArticleCard key={a.id} {...a} />)}
  </div>
</div>
```

---

## 레이아웃 선택 흐름도

```
타입 파악
  │
  ├── 랜딩/소개 → CTA가 핵심인가?
  │     ├── YES → Above-the-fold CTA
  │     └── NO (브랜드 경험) → 탈구축 히어로 or Kinetic Typography
  │
  ├── 대시보드/앱 → 정보 밀도가 높은가?
  │     ├── YES → 벤토 박스
  │     └── NO (심플) → 카드 그리드
  │
  ├── 포트폴리오 → 개성 표현이 중요한가?
  │     └── YES → 탈구축 히어로 + Kinetic Typography
  │
  └── e-커머스/블로그 → 콘텐츠 목록 중심
        └── 카드 그리드 or 에디토리얼 그리드
```
