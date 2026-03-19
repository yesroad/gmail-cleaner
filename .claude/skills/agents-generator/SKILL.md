---
name: agents-generator
description: 프로젝트를 분석하고 도구 우선순위에 맞는 루트 지시문(CLAUDE.md 또는 AGENTS.md)을 생성/업데이트합니다. "루트 지시문 생성", "CLAUDE.md 만들어줘", "AGENTS.md 업데이트", "프로젝트 규칙 파일 만들어줘" 같은 요청에 반드시 사용하세요. 모노레포 자동 감지 및 워크스페이스별 중첩 파일 생성 지원.
user-invocable: true
disable-model-invocation: false
argument-hint: "[선택사항: 특정 워크스페이스 경로]"
metadata:
  version: 1.1.0
  category: documentation
  priority: high
---

# Instruction File Generator

## 목적

프로젝트를 분석하고 최적화된 루트 지시문 시스템을 생성하거나 업데이트합니다:

1. **신규 생성** — 대상 파일(CLAUDE.md 또는 AGENTS.md)이 없으면 자동 생성
2. **자동 업데이트** — 기존 파일이 있으면 diff 분석 후 개선사항 적용
3. **모노레포 지원** — 각 워크스페이스마다 중첩 지시문 파일 생성
4. **프레임워크 감지** — Next.js, TypeScript/Node.js 패턴 자동 적용

## AGENTS.md에 무엇을 넣을지 판단 기준

**핵심 질문: "에이전트가 코드베이스를 탐색해서 알 수 있는가?"**

알 수 있으면 → 넣지 않는다. 알 수 없으면 → 넣는다.

### 반드시 포함

- **비직관적 도구/명령어** — 표준과 다른 것. 예: `npm` 대신 `pnpm` 필수, `python` 대신 `uv run` 필수
- **필수 플래그** — 없으면 오작동하는 플래그. 예: `jest --no-cache`, `vitest --run`
- **삭제/수정 금지 목록** — 레거시 코드, 하위 호환성 레이어 등 손대면 안 되는 파일/함수
- **비직관적 경로 규칙** — `api/`가 아니라 `server/routes/`를 수정해야 하는 등 탐색만으로 파악 어려운 구조적 함정
- **반복 실수 패턴** — 에이전트가 자주 틀리는 패턴. 예: "이 프로젝트에서 Server Component에 useState 사용 금지"

### 포함하지 않음

- **디렉토리 구조 전체** — 에이전트가 직접 탐색 가능
- **기술 스택 목록** — package.json, requirements.txt에서 알 수 있음
- **README와 동일한 내용** — 중복은 신뢰를 떨어트림
- **일반적인 코딩 스타일 가이드** — rules/core/ 파일로 분리하거나 별도 @참조로 처리

## 실행 프로토콜

### Step 0: 모드 판단

```bash
ls CLAUDE.md AGENTS.md 2>/dev/null | head -n 1 >/dev/null && echo "UPDATE_MODE" || echo "CREATE_MODE"
```

### Step 1: 프로젝트 분석

```bash
ls package.json tsconfig.json pyproject.toml Cargo.toml go.mod 2>/dev/null
find . -maxdepth 3 -type d ! -path "*/node_modules/*" ! -path "*/.git/*" ! -path "*/.next/*"
cat package.json 2>/dev/null | grep -A 10 '"workspaces"'
ls pnpm-workspace.yaml turbo.json 2>/dev/null
ls README.md CLAUDE.md AGENTS.md 2>/dev/null
```

판단 항목:

1. 프로젝트 유형 (Monorepo / Backend / Frontend / Fullstack)
2. 패키지 매니저 (npm / pnpm / yarn / uv / cargo)
3. 워크스페이스 구조 (apps/_, packages/_, services/\*)
4. 기존 컨벤션 (.eslintrc, .prettierrc, Makefile의 커스텀 명령어)

> Makefile, justfile, scripts/ 디렉토리가 있으면 반드시 확인하세요.
> 비직관적 명령어(커스텀 wrapper, alias)가 숨어있을 수 있습니다.

### Step 2: 비직관적 요소 발굴

다음을 적극적으로 탐색해서 AGENTS.md에 담을 핵심 정보를 수집합니다:

```bash
# 패키지 매니저 확인 (표준이 아닌 것 우선)
cat package.json | grep -E '"packageManager"'
ls .nvmrc .node-version 2>/dev/null && cat .nvmrc 2>/dev/null

# 테스트 실행 방식 (숨겨진 플래그 확인)
cat package.json | grep -A 5 '"scripts"' | grep -E 'test|jest|vitest'
cat jest.config.* vitest.config.* 2>/dev/null | head -30

# 삭제 금지 파일/함수 단서 (레거시 주석 탐색)
grep -r "DO NOT DELETE\|LEGACY\|deprecated\|하위 호환\|breaking" --include="*.ts" --include="*.js" -l . 2>/dev/null | head -10

# 환경변수 필수 여부
ls .env.example .env.local.example 2>/dev/null && cat .env.example 2>/dev/null | head -20
```

### Step 3: 프로젝트 유형 감지

**MONOREPO 신호:**
- 루트 package.json에 "workspaces" 필드
- pnpm-workspace.yaml 또는 turbo.json 존재
- apps/, packages/, services/ 폴더에 자체 package.json

**FRONTEND (Next.js) 신호:**
- 프레임워크: next
- 파일: app/, pages/, components/

**BACKEND (Node.js) 신호:**
- 프레임워크: express, nestjs, fastify
- 파일: src/, routes/, controllers/

### Step 4: 업데이트 모드 (기존 파일 존재 시)

```bash
cat CLAUDE.md AGENTS.md 2>/dev/null
```

기존 내용 중 보존할 것:
- 이미 문서화된 비직관적 규칙
- 삭제 금지 목록
- 프로젝트 고유 명령어

제거할 것:
- 기술 스택 단순 목록 (package.json 중복)
- 전체 디렉토리 트리
- 일반적 코딩 스타일 가이드

### Step 5: 루트 지시문 생성 스키마

````markdown
# [프로젝트명] 규칙

## 개요

[1-2문장: 무엇을, 누구를 위해, 왜]

## 명령어

```bash
dev:   [명령어]
build: [명령어]
test:  [명령어]  # 필수 플래그 포함. 예: pnpm test --no-cache
lint:  [명령어]
```

## 비직관적 도구 규칙

<!-- package.json만 봐서는 알 수 없는 것만 작성 -->
- [표준 도구] 대신 [실제 사용 도구] 사용. 예: `npm` 대신 `pnpm`, `python` 대신 `uv run`
- [명령어]는 반드시 [필수 플래그]와 함께 실행. 이유: [한 줄 설명]

## 수정/삭제 금지

<!-- 손대면 안 되는 파일, 함수, 패턴 목록 -->
- `[경로/파일]` — [이유: 레거시 호환, 외부 의존 등]

## 에이전트 주의사항

<!-- 이 프로젝트에서 반복 발생하는 실수 방지 지침 -->
- [구체적인 금지 패턴] — [왜 안 되는지 한 줄]

## 컨텍스트 라우팅

- **[작업/영역](./경로/AGENTS.md 또는 ./경로/CLAUDE.md)** — [언제 읽어야 하는지]
````

> `## 기술 스택` 섹션은 생성하지 않습니다. package.json이 있습니다.
> `## 아키텍처` 전체 트리도 생성하지 않습니다. 탐색 가능합니다.
> 비직관적인 경로 규칙이 있다면 `## 에이전트 주의사항`에 1줄로만 추가합니다.

### Step 6: 중첩 파일 생성 규칙

다음 중 하나라도 존재하면 중첩 지시문 파일 생성:

- 별도 package.json 존재 (모노레포 워크스페이스)
- 프레임워크 경계 (apps/web vs services/api)
- 고유 런타임 환경 (Edge Functions, Workers)

중첩 파일에는 해당 워크스페이스 고유의 비직관적 규칙만 담습니다.
루트 파일과 중복되는 내용은 제외합니다.

### Step 7: 출력 파일 선택

```bash
echo "claude   -> CLAUDE.md"
echo "codex    -> AGENTS.md"
echo "opencode -> AGENTS.md"
echo "cursor   -> .cursor/rules/frontend.mdc (+ .cursorrules)"
echo "copilot  -> .github/copilot-instructions.md"
echo "gemini   -> GEMINI.md"
```

### Step 8: 검증

```bash
for f in CLAUDE.md AGENTS.md; do
  [ -f "$f" ] || continue
  wc -l "$f"
  grep -c '기술 스택\|Tech Stack\|Dependencies:' "$f" && echo "WARN: 기술 스택 목록 발견 → 제거 검토" || true
  grep -o '\./[^)]*' "$f" | while read path; do
    ls "$path" 2>/dev/null || echo "BROKEN($f): $path"
  done
done
```

체크리스트:

- [ ] 파일당 500줄 미만
- [ ] 이모지 없음
- [ ] 모든 명령어 실행 가능 (필수 플래그 포함)
- [ ] 기술 스택 단순 목록 없음
- [ ] 전체 디렉토리 트리 없음
- [ ] 비직관적 도구/플래그 명시됨
- [ ] 컨텍스트 라우팅 경로 유효

## 예외 처리

| 상황                     | 조치                                                          |
| ------------------------ | ------------------------------------------------------------- |
| 기술 스택 판단 불가      | 사용자에게 확인 요청                                          |
| 비직관적 요소 없음       | `## 비직관적 도구 규칙` 섹션 생략, 명령어 + 주의사항만 작성  |
| 혼합/불명확한 컨벤션     | 충돌 문서화, 명시적 규칙 선택                                 |
| 최소 프로젝트 (< 5 파일) | 단일 간결한 루트 지시문 파일 (100줄 미만)                     |
| 기존 규칙 파일 존재      | 유용한 내용 보존, 기술 스택 목록·디렉토리 트리는 정리        |
| 기존 파일이 최신 상태    | "변경사항 없음" 메시지 출력 후 종료                           |

## Related Files

| File                    | Purpose                      |
| ----------------------- | ---------------------------- |
| `/CLAUDE.md`            | Claude Code 루트 규칙 파일   |
| `/AGENTS.md`            | 루트 규칙 파일               |
| `/apps/*/CLAUDE.md`     | 앱별 Claude 규칙             |
| `/apps/*/AGENTS.md`     | 앱별 Codex/OpenCode 규칙     |
| `/packages/*/CLAUDE.md` | 패키지별 Claude 규칙         |
| `/packages/*/AGENTS.md` | 패키지별 Codex/OpenCode 규칙 |
