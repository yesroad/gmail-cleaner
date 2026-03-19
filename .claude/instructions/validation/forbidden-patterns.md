# Forbidden Patterns

> 프로젝트에서 금지된 패턴 목록

---

## 언어 표현

| 금지                 | 대안                |
| -------------------- | ------------------- |
| "~할 것 같습니다"    | "~합니다"           |
| "아마도", "추측컨대" | 확인 후 명시적 진술 |
| "~일 수 있습니다"    | 조건 명시하여 단정  |

---

## 코드 품질

| 금지                  | 대안                  | 예시                  |
| --------------------- | --------------------- | --------------------- |
| `any` 타입            | `unknown` + 타입 가드 | `data: unknown`       |
| `@ts-ignore`          | 타입 수정             | -                     |
| `// @ts-expect-error` | 타입 수정             | -                     |
| 암시적 `any`          | 명시적 타입           | `(item: Item) => ...` |
| return type 생략      | 명시적 반환 타입      | `: Promise<Order>`    |

```typescript
// ❌ 금지
const getData = (id) => api.get(`/orders/${id}`);

// ✅ 허용
const getData = (id: string): Promise<OrderResponse> => api.get(`/orders/${id}`);
```

---

## 상태 관리

| 금지                    | 대안                  | 참조                                          |
| ----------------------- | --------------------- | --------------------------------------------- |
| 서버 상태에 useState    | TanStack Query        | `@../../rules/core/state-and-server-state.md` |
| 과도한 전역 상태        | 로컬 상태 우선        | -                                             |
| Query 내 직접 상태 변경 | mutation + invalidate | -                                             |

```typescript
// ❌ 금지: 서버 데이터를 useState로 관리
const [orders, setOrders] = useState([]);
useEffect(() => {
  fetchOrders().then(setOrders);
}, []);

// ✅ 허용: TanStack Query 사용
const { data: orders } = useItemListQuery(params);
```

---

## Barrel File Imports

아이콘/컴포넌트 라이브러리 barrel 파일은 수만 개의 re-export를 포함할 수 있어 개발 환경에서 **200-800ms** 추가 비용이 발생한다.

| 금지                           | 대안                           |
| ------------------------------ | ------------------------------ |
| barrel 파일을 통한 대량 import | 소스 파일 직접 경로로 import   |

```typescript
// ❌ 금지: barrel 파일 경유 (라이브러리에 따라 수천 개 re-export)
import { IconHome, IconSearch, IconUser } from 'some-icon-library';

// ✅ 허용: 직접 경로로 import
import { IconHome } from 'some-icon-library/icons/IconHome';
import { IconSearch } from 'some-icon-library/icons/IconSearch';
```

> **예외**: 프로젝트 디자인 시스템 패키지의 공식 barrel은 허용 (관리된 export)

---

## Import 순서

| 순서               | 예시                                               |
| ------------------ | -------------------------------------------------- |
| 1. 외부 라이브러리 | `import { useQuery } from '@tanstack/react-query'` |
| 2. 내부 패키지     | `import { Button } from '@/components'`            |
| 3. 상대 경로       | `import { Table } from './components'`             |

**ESLint 강제**: `@typescript-eslint/consistent-type-imports`

---

## Git/PR

| 금지                  | 이유          |
| --------------------- | ------------- |
| 커밋 메시지에 AI 표시 | 불필요한 노출 |
| 커밋 메시지에 이모지  | 일관성        |
| force push to master  | 히스토리 파괴 |
| --no-verify           | 검증 우회     |

```bash
# ❌ 금지
git commit -m "🚀 feat: add feature"
git commit -m "feat: add feature (by Claude)"
git push --force origin master

# ✅ 허용
git commit -m "feat: add feature"
```

---

## 보안

| 금지                       | 대안                         |
| -------------------------- | ---------------------------- |
| 토큰/비밀번호 하드코딩     | 환경변수 또는 로컬 env 파일  |
| 스크립트에 자격증명 직접 작성 | `.env.*.example` + 런타임 주입 |

```bash
# ❌ 금지
API_KEY="sk-abc123..."

# ✅ 허용
API_KEY="${MY_API_KEY:-}"
```

---

## 워크플로우

| 금지                | 대안                |
| ------------------- | ------------------- |
| 읽지 않은 파일 수정 | Read → Edit         |
| 정책 변경 시 테스트 누락 | 단위 테스트 작성 |
| 린트 오류 무시      | lint-fixer 실행     |
| 기존 정책 임의 변경 | 사용자 확인 후 변경 |

---

## Modal/Dialog 내부 Context 접근 금지

Modal/Dialog content 컴포넌트 내부에서는 상위 Context에 직접 접근하지 않는다.

| 금지                                 | 대안                         |
| ------------------------------------ | ---------------------------- |
| 모달 내부에서 context hook 직접 호출 | 상위에서 콜백을 props로 전달 |
| 모달 내부에서 상태 직접 변경         | onClose, onConfirm 등 전달   |

```typescript
// ❌ 금지: Modal content 내부에서 context 의존
const Content = () => {
  const { close } = useModalContext(); // 상위 context 직접 참조
  return <Button onClick={close} />;
};

// ✅ 허용: 상위에서 콜백 전달
const Content = ({ onClose }: { onClose: () => void }) => {
  return <Button onClick={onClose} />;
};
```

---

## API/서비스

| 금지             | 대안                          |
| ---------------- | ----------------------------- |
| 수동 axios 호출  | 프로젝트 api 래퍼 사용        |
| 직접 에러 핸들링 | Query의 onError               |
| 하드코딩된 URL   | 환경 변수                     |

```typescript
// ❌ 금지
const res = await axios.get('https://api.example.com/orders');

// ✅ 허용
const res = await api.get('/api/orders');
```

---

## 테스트

| 금지                       | 대안                           | 참조                                         |
| -------------------------- | ------------------------------ | -------------------------------------------- |
| 테스트 삭제                | 테스트 수정                    | -                                            |
| 하드코딩된 날짜            | `jest.useFakeTimers()`         | `@../../rules/core/unit-test-conventions.md` |
| 구현 상세 테스트           | 동작 중심 테스트               | -                                            |

---

## 스타일링

| 금지              | 대안                       |
| ----------------- | -------------------------- |
| inline style 객체 | Emotion styled/css         |
| !important        | `&&` specificity           |
| px 하드코딩       | 디자인 토큰/변수 사용      |
| 하드코딩 색상값   | 디자인 토큰/변수 사용      |

```typescript
// ❌ 금지
<div style={{ marginTop: 20 }}>

// ✅ 허용: styled 컴포넌트
const Container = styled.div`
  margin-top: 8px;
`;

// ✅ 허용: Emotion css prop (inline style이 아님)
<Typography css={{ marginTop: '4px' }}>
```

### !important 대신 `&&` specificity 패턴

`&&`는 Emotion이 생성한 자기 자신의 클래스를 한번 더 참조하여 specificity를 높이는 기법이다.
`!important`는 이후 override가 불가능해지므로 금지한다.

```typescript
// ❌ 금지
background-color: ${theme.colors.secondary} !important;

// ✅ 허용: && 사용 (specificity 0,1,0 → 0,2,0)
&& {
  background-color: ${theme.colors.secondary};
}
```

### transient props (`$` prefix)

styled 컴포넌트에 전달하는 custom prop은 `$` prefix를 붙인다.
`$` 없이 전달하면 DOM에 unknown attribute가 전달되어 React warning이 발생한다.

```typescript
// ❌ 금지: DOM에 isActive가 전달됨 → React warning
const Chip = styled.button<{ isActive: boolean }>`...`;
<Chip isActive={true}>

// ✅ 허용: $prefix로 DOM 전달 방지
const Chip = styled.button<{ $isActive: boolean }>`...`;
<Chip $isActive={true}>
```

### inline style vs css prop 구분

| 구문                    | 판정    | 이유                                        |
| ----------------------- | ------- | ------------------------------------------- |
| `style={{ margin: 8 }}` | ❌ 금지 | React의 inline style (정적 스타일에 비효율) |
| `css={{ margin: 8 }}`   | ✅ 허용 | Emotion의 css prop (컴파일 타임 처리)       |

---

## 체크리스트

PR 전 확인:

- [ ] `any` 타입 없음
- [ ] return type 명시
- [ ] Import 순서 준수
- [ ] TanStack Query로 서버 상태 관리
- [ ] 정책 변경 시 테스트 작성/실행
- [ ] 린트 오류 없음

---

## 참조 문서

| 문서                                            | 관련 금지 항목 |
| ----------------------------------------------- | -------------- |
| `@../../rules/core/react-nextjs-conventions.md` | 코드, Import   |
| `@../../rules/core/state-and-server-state.md`   | 상태 관리      |
| `@../../rules/core/unit-test-conventions.md`    | 테스트         |
| `@../../rules/core/thinking-model.md`           | 워크플로우     |
