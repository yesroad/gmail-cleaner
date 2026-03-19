# Sequential Thinking Pattern

> 복잡도에 따른 사고 단계 조절

**통합 사고 모델과 연계**: `@../../rules/core/thinking-model.md`

---

## 복잡도 판단

| 복잡도     | 기준                        | 예시                         |
| ---------- | --------------------------- | ---------------------------- |
| **LOW**    | 단일 파일, 명확한 수정      | 오타 수정, 단순 스타일 변경  |
| **MEDIUM** | 2-5개 파일, 기존 패턴 따름  | 새 컴포넌트 추가, 훅 작성    |
| **HIGH**   | 5개+ 파일, 새 패턴/아키텍처 | 도메인 리팩토링, 시스템 설계 |

---

## 복잡도별 사고 단계

### LOW (1-2 단계)

```
1. READ: 대상 파일 확인
2. REACT: 즉시 수정
```

**예시**: 버튼 텍스트 변경

```typescript
// 바로 수정
Edit('Button.tsx', '확인', '저장');
```

---

### MEDIUM (3-5 단계)

```
1. READ: 관련 파일 파악
2. ANALYZE: 기존 패턴 확인
3. STRUCTURE: 구현 방향 정리
4. REACT: 구현
5. REFLECT: 검증
```

**예시**: 새 컴포넌트 추가

```typescript
// 1. 유사 컴포넌트 확인
Read("src/order/components/OrderTable/index.tsx")

// 2. 패턴 분석
// - styled.ts 분리
// - Props 타입 정의
// - 테스트 파일 위치

// 3. 구조 결정
// - NewTable/index.tsx
// - NewTable/styled.ts
// - NewTable/__tests__/

// 4. 구현
Write("src/order/components/NewTable/index.tsx", ...)

// 5. 린트/테스트 검증
Bash("yarn lint")
```

---

### HIGH (7-10+ 단계)

```
1. READ: 전체 영역 파악
2. ANALYZE: 현재 상태 분석
3. RESEARCH: 유사 사례 조사
4. RESTRUCTURE: 아키텍처 설계
5. PLAN: 단계별 계획
6. VALIDATE: 계획 검증
7. IMPLEMENT: 단계적 구현
8. TEST: 테스트 작성
9. REVIEW: 코드 리뷰
10. REFLECT: 최종 검증
```

**예시**: 도메인 전체 리팩토링

```typescript
// Plan 에이전트 활용
Task((subagent_type = 'Plan'), (model = 'opus'), (prompt = '인증 모듈 리팩토링 계획'));
```

---

## thinking-model 통합

기존 thinking-model의 6단계와 연계:

| thinking-model | LOW | MEDIUM | HIGH |
| -------------- | --- | ------ | ---- |
| READ           | ✅  | ✅     | ✅   |
| REACT          | ✅  | ✅     | ✅   |
| ANALYZE        | -   | ✅     | ✅   |
| RESTRUCTURE    | -   | -      | ✅   |
| STRUCTURE      | -   | ✅     | ✅   |
| REFLECT        | -   | ✅     | ✅   |

---

## 에이전트 연계

| 복잡도 | 에이전트            | 모델          |
| ------ | ------------------- | ------------- |
| LOW    | - (직접 처리)       | -             |
| MEDIUM | explore, code-reviewer     | haiku, sonnet |
| HIGH   | Plan, code-reviewer | opus, sonnet  |

---

## 병렬 실행 결합

복잡도가 높아도 독립 작업은 병렬 실행:

```typescript
// HIGH 복잡도에서도 탐색은 병렬
Task((subagent_type = 'explore'), (model = 'haiku'), (prompt = '현재 구조 분석'));
Task((subagent_type = 'explore'), (model = 'haiku'), (prompt = '의존성 파악'));
Task((subagent_type = 'explore'), (model = 'haiku'), (prompt = '테스트 현황'));

// 결과 수집 후 순차적 계획
Task((subagent_type = 'Plan'), (model = 'opus'), (prompt = '분석 결과 기반 계획'));
```

---

## 자동 복잡도 판단

```typescript
const judgeComplexity = (task: string): 'LOW' | 'MEDIUM' | 'HIGH' => {
  // 파일 수 기반
  if (affectedFiles.length <= 1) return 'LOW';
  if (affectedFiles.length <= 5) return 'MEDIUM';
  return 'HIGH';

  // 또는 키워드 기반
  if (task.includes('리팩토링') || task.includes('아키텍처')) return 'HIGH';
  if (task.includes('추가') || task.includes('수정')) return 'MEDIUM';
  return 'LOW';
};
```

---

## 참조 문서

| 문서                                    | 연계           |
| --------------------------------------- | -------------- |
| `@../../rules/core/thinking-model.md`   | 사고 단계 상세 |
| `@../multi-agent/coordination-guide.md` | 병렬 실행      |
| `@../multi-agent/agent-roster.md`       | 에이전트 선택  |
