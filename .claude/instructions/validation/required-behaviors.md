# Required Behaviors (필수 행동)

> 모든 작업에서 반드시 따라야 할 규칙

---

## 작업 시작

### 필수 0: 작업 범위 확인

- 작업 대상 파일/디렉토리를 먼저 확인한다
- 기본 스코프 외 수정은 **명시 요청이 있을 때만** 진행한다

### 필수 0.5: 인지 모델 기본 적용

- 모든 작업은 통합 사고 모델을 기본 적용한다 (`.claude/rules/core/thinking-model.md`)
- 코드 작성 전 READ 단계 체크리스트를 반드시 수행:
  - 기존 유사 구현 검색
  - 디자인 시스템 컴포넌트 사용 패턴 확인
  - 관련 스펙/룰 확인

### 필수 1: 복잡도 판단

| 복잡도 | 최소 단계 | 예시                    |
| ------ | --------- | ----------------------- |
| LOW    | 1-2       | 파일 읽기, 간단한 검색  |
| MEDIUM | 3-5       | 기능 구현, 버그 수정    |
| HIGH   | 7-10+     | 아키텍처 설계, 리팩토링 |

**참조**: `@../workflow-patterns/sequential-thinking.md`

### 필수 2: 파일 읽기 전 Read 사용

```typescript
// ✅ 필수 순서
Read({ file_path: "src/order/views/listV2/index.tsx" })  // 1. 읽기
Edit({ ... })  // 2. 수정

// ❌ 금지
Edit({ ... })  // 읽지 않고 수정
```

### 필수 3: 병렬 읽기

**3개 이상 독립 파일은 반드시 병렬로 읽기**

```typescript
// ✅ 필수: 병렬 읽기 (단일 메시지)
Read({ file_path: 'file1.ts' });
Read({ file_path: 'file2.ts' });
Read({ file_path: 'file3.ts' });
```

---

### 필수 3.5: 규칙 변경 요청 처리

- 사용자가 **규칙/정책 변경**을 요청하면 먼저 변경 범위를 확인한다
- **공통(core)** 변경인지 **프로젝트 전용** 변경인지 확인 후 진행한다

## 코드 작성

### 필수 4: TypeScript strict 모드

```typescript
// ✅ 필수: 명시적 타입
function getOrders(params: OrderParams): Promise<Order[]> {
  return orderService.getList(params);
}

// ❌ 금지: any 사용
function getOrders(params: any): any {
  return orderService.getList(params);
}
```

**참조**: `@forbidden-patterns.md`

### 필수 5: TanStack Query 사용

**서버 상태는 반드시 TanStack Query 사용**

```typescript
// ✅ 필수: useQuery/useMutation
const { data } = useItemListQuery(params);

const mutation = useUpdateMutation({
  onSuccess: () => queryClient.invalidateQueries(['items']),
});

// ❌ 금지: useState로 서버 상태 관리
const [items, setItems] = useState([]);
useEffect(() => fetchItems().then(setItems), []);
```

**참조**: `@../../rules/core/state-and-server-state.md`

### 필수 6: Import 순서

```typescript
// ✅ 필수 순서
import { useQuery } from '@tanstack/react-query'; // 1. 외부
import { Button } from '@/components'; // 2. 내부 패키지
import { useOrder } from '@/order/hooks'; // 3. @/ alias
import { Table } from './components'; // 4. 상대 경로
```

---

## 검증

### 필수 7: lint/build 검증

**코드 변경 후 반드시 검증**

```bash
{패키지매니저} lint
{패키지매니저} build
```

### 필수 8: 정책 변경 시 테스트

**비즈니스 정책 변경 시 테스트 필수**

| 정책 유형      | 테스트 필수 |
| -------------- | ----------- |
| 날짜/기간 계산 | ✅          |
| 가격/할인 계산 | ✅          |
| 필터 조건      | ✅          |
| disabled 조건  | ✅          |

**참조**: `@../../rules/core/unit-test-conventions.md`

---

## 에이전트 활용

### 필수 9: 에이전트 위임

**다음 조건 시 에이전트 위임**

- [ ] 독립적인 작업
- [ ] 전문 지식 필요
- [ ] 10분 이상 소요 예상

```typescript
// ✅ 필수: 적절한 에이전트 위임
Task(subagent_type="explore", model="haiku", ...)
Task(subagent_type="code-reviewer", model="sonnet", ...)
Task(subagent_type="lint-fixer", model="haiku", ...)
```

### 필수 10: 모델 선택

| 모델   | 사용 시점               |
| ------ | ----------------------- |
| haiku  | 탐색, 린트, 문서        |
| sonnet | 구현, 수정, 분석 (기본) |
| opus   | 아키텍처, 복잡한 분석   |

---

## Git 작업

### 필수 11: 커밋 메시지 형식

**`git-operator.md` 커밋 메시지 규칙을 따른다.**

```bash
# ✅ 필수
feat: 기능 설명

# ❌ 금지
🚀 feat: 기능 추가  # 이모지
feat: 기능 (by Claude)  # AI 표시
```

> 상세 형식, 허용 type, 본문 작성 기준은 `@../../agents/git-operator.md` 참조

### 필수 12: 해당 파일만 커밋

```bash
# ❌ 금지
git add .
git add -A

# ✅ 필수
git add src/{수정한 파일 경로}
```

### 필수 13: 출시 전 품질 게이트 통과

- 커밋/PR 전 `release-readiness-gate.md` 5개 게이트를 모두 점검한다
- 하나라도 FAIL이면 원인/리스크를 정리하고 수정 후 재검증한다
- 게이트 통과 전에는 커밋/PR을 진행하지 않는다

---

## 종합 체크리스트

**작업 시작 전:**

- [ ] 복잡도 판단
- [ ] 파일 읽기 계획 (병렬 여부)
- [ ] 에이전트 활용 계획

**코드 작성 시:**

- [ ] TypeScript strict 모드
- [ ] TanStack Query 사용
- [ ] Import 순서 준수

**검증 시:**

- [ ] lint/build 통과
- [ ] 정책 변경 시 테스트

**Git:**

- [ ] 커밋 메시지 형식 준수
- [ ] 해당 파일만 커밋
- [ ] release-readiness-gate PASS

---

## 참조 문서

| 문서                        | 관련 필수 항목 |
| --------------------------- | -------------- |
| `forbidden-patterns.md`     | 4, 5, 6        |
| `sequential-thinking.md`    | 1              |
| `state-and-server-state.md` | 5              |
| `unit-test-conventions.md`  | 8              |
| `coordination-guide.md`     | 3, 9, 10       |
| `release-readiness-gate.md` | 13             |
