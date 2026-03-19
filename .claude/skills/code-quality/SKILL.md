---
name: code-quality
description: 린트, 포맷, 타입 체크 실행 및 자동 수정. "린트", "포맷", "타입체크", "code quality" 입력 시 사용.
user-invocable: true
allowed-tools: Bash(*)
metadata:
  version: 1.0.0
  category: development
  priority: high
---

# Code Quality Checker

lint, prettier, 타입 체크를 순서대로 실행하고 오류를 자동 수정한다.

## 기본 원칙

- 패키지 매니저는 lock 파일 기준으로 자동 감지
- 각 단계는 순차 실행 (포맷 → 린트 → 타입 체크)
- 스크립트가 없는 항목은 스킵
- 자동 수정 후 재검증하여 최종 결과 확인

---

## 실행 플로우

### 0. 실행 경로 감지

변경된 파일이 서브패키지(모노레포) 내에 있는 경우 해당 패키지 경로에서 실행한다:

```bash
# 변경 파일 경로 확인
git diff --name-only HEAD

# 예: apps/web/src/... → apps/web/에서 실행
# 예: packages/ui/src/... → packages/ui/에서 실행
# 루트에 package.json이 없거나 scripts가 없으면 서브패키지 탐색
```

| 상황 | 실행 위치 |
|------|-----------|
| 루트에 lint/format 스크립트 있음 | 루트 |
| 변경 파일이 서브패키지에만 있음 | 해당 서브패키지 경로 |
| 모노레포 전체 검증 요청 | 루트 turbo/nx 명령 우선 |

### 1. 패키지 매니저 감지

```bash
# lock 파일 기준으로 판단
ls yarn.lock 2>/dev/null && echo "yarn"
ls pnpm-lock.yaml 2>/dev/null && echo "pnpm"
ls package-lock.json 2>/dev/null && echo "npm"
```

| lock 파일        | 패키지 매니저 |
| ---------------- | ------------- |
| `yarn.lock`      | yarn          |
| `pnpm-lock.yaml` | pnpm          |
| `package-lock.json` | npm        |
| 없음             | npm (기본)    |

### 2. 사용 가능한 스크립트 확인

```bash
cat package.json | grep -E '"(format|prettier|lint|type-check|typecheck|tsc|build)"'
```

스크립트 존재 여부에 따라 실행 여부 결정:

| 확인 대상         | 스크립트 키 예시                        |
| ----------------- | --------------------------------------- |
| Prettier          | `format`, `prettier`, `fmt`             |
| Lint              | `lint`, `eslint`                        |
| 타입 체크         | `type-check`, `typecheck`, `tsc`, `build` |

### 3. 포맷 (Prettier)

```bash
# 스크립트 있는 경우
{패키지매니저} format

# 스크립트 없고 prettier 설치된 경우
{패키지매니저} exec prettier --write "src/**/*.{ts,tsx,js,jsx}"
```

- 스크립트도 없고 prettier도 없으면 스킵

### 4. 린트 (ESLint)

```bash
# --fix 포함하여 자동 수정
{패키지매니저} lint --fix

# lint 스크립트가 --fix를 지원하지 않는 경우
{패키지매니저} exec eslint --fix "src/**/*.{ts,tsx,js,jsx}"
```

- 자동 수정 불가한 오류는 목록으로 출력

### 5. 타입 체크

```bash
# type-check 스크립트 있는 경우
{패키지매니저} type-check

# 없으면 build로 대체 (타입 오류 포함)
{패키지매니저} build
```

- 타입 오류는 자동 수정 불가 → 오류 목록 출력 후 사용자 확인 필요

---

## 자동 수정 불가 오류 처리

린트/타입 오류 중 자동 수정이 안 되는 경우:

1. 오류 목록 출력
2. 각 오류에 대해 수정 방법 제안
3. 수정 후 해당 단계만 재실행하여 검증

---

## 출력 형식

```
## 코드 품질 검사 결과

| 항목      | 결과        | 비고                    |
| --------- | ----------- | ----------------------- |
| Prettier  | ✅ PASS     | 3개 파일 포맷           |
| Lint      | ✅ PASS     | 2개 자동 수정           |
| 타입 체크 | ❌ FAIL     | 1개 오류 (수동 수정 필요) |

### 수동 수정 필요

{오류 목록 및 수정 제안}
```

---

## 예외 처리

### package.json 없음

```
❌ package.json을 찾을 수 없습니다. Node.js 프로젝트인지 확인하세요.
```

### 모든 스크립트 없음

```
⚠️ lint/format/type-check 스크립트가 없습니다. package.json scripts를 확인하세요.
```
