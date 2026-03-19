# 모델 라우팅 전략

> 작업 복잡도와 비즈니스 로직 포함 여부에 따라 적절한 모델을 선택한다.

---

## 기본 복잡도 기준

| 복잡도     | 모델   | 사용 케이스                               | 비용   |
| ---------- | ------ | ----------------------------------------- | ------ |
| **LOW**    | haiku  | 파일 탐색, 단순 검색, 린트 수정           | 💰     |
| **MEDIUM** | sonnet | 코드 리뷰, 테스트 생성, 구현              | 💰💰   |
| **HIGH**   | opus   | 아키텍처 설계, 복잡한 버그, 리팩토링 분석 | 💰💰💰 |

---

## 비즈니스 로직 관련 = 상향 조정

**비즈니스 로직이 포함되면 무조건 sonnet 이상:**

| 작업 성격                             | 최소 모델  | 이유                       |
| ------------------------------------- | ---------- | -------------------------- |
| 날짜/금액/수량 계산 로직              | **opus**   | 정확성 중요, 엣지케이스 多 |
| 상태 전이 / 상태 머신                 | **opus**   | 전체 흐름 이해 필요        |
| 조건부 렌더링, disabled/readonly 조건 | **sonnet** | 상태 의존성 파악           |
| 필터/정렬/검색 로직                   | **sonnet** | 연쇄 영향 분석             |
| 아키텍처 변경, 모듈 간 의존성 재설계  | **opus**   | 전체 구조 파악             |

---

## 모델 선택 예시

```typescript
// haiku - 구조 파악, 파일 목록, 단순 검색
Task(subagent_type="explore", model="haiku", prompt="src/ 폴더 구조 파악");
Task(subagent_type="lint-fixer", model="haiku", prompt="린트 오류 수정");

// sonnet - 구현, 코드 리뷰, 분석 (기본값)
Task(subagent_type="explore", model="sonnet", prompt="조건부 렌더링 로직 분석");
Task(subagent_type="code-reviewer", model="sonnet", prompt="코드 리뷰");
Task(subagent_type="implementation-executor", model="sonnet", prompt="기능 구현");

// opus - 비즈니스 로직 분석, 아키텍처 설계, 복잡한 리팩토링
Task(subagent_type="explore", model="opus", prompt="결제 플로우 상태 전이 전체 분석");
Task(subagent_type="Plan", model="opus", prompt="인증 모듈 리팩토링 계획 수립");
```

---

## 작업 유형별 빠른 참조

### 탐색/분석

```typescript
// 단순 구조 탐색: haiku
Task(subagent_type="explore", model="haiku", prompt="src/ 폴더 구조");

// 비즈니스 로직 분석: sonnet/opus
Task(subagent_type="explore", model="sonnet", prompt="조건부 렌더링 로직 분석");
Task(subagent_type="explore", model="opus", prompt="결제 상태 전이 전체 흐름 분석");
```

### 구현

```typescript
// 순차: 정책 분석 (opus) → 구현 (sonnet)
Task(subagent_type="explore", model="opus", prompt="기존 비즈니스 로직 분석");
// 결과 확인 후
Task(subagent_type="implementation-executor", model="sonnet", prompt="분석 기반 구현 - 정책 유지");
```

### 검증

```typescript
// 병렬: 린트 + 리뷰
Task(subagent_type="lint-fixer", model="haiku", prompt="린트 오류 수정");
Task(subagent_type="code-reviewer", model="sonnet", prompt="정책 준수 코드 리뷰");
```
