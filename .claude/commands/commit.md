---
name: commit
description: main 최신화 → 작업 브랜치 생성 → 커밋/푸시 → main 머지 → main 최신화 전체 플로우 자동 실행. staged 변경사항으로 커밋 메시지 생성 후 커밋.
---

**참조 규칙**: `@../skills/commit-helper/SKILL.md`

**[즉시 실행]** 아래 6단계 플로우를 순서대로 실행한다.

**옵션**: $ARGUMENTS

| 옵션              | 설명                         |
| ----------------- | ---------------------------- |
| `--branch <name>` | 기준 브랜치 (기본값: `main`) |
| `--no-gate`       | 출시 게이트 점검 스킵        |

---

## 사전 확인

1. `git diff --staged --name-only`로 staged 변경사항이 있는지 확인
2. 없으면: `❌ staged 변경사항이 없습니다. git add를 먼저 실행하세요.` 출력 후 **중단**

---

## Step 1. 기준 브랜치 최신화

`$ARGUMENTS`에서 `--branch <name>` 값 파싱. 없으면 기준 브랜치는 `main`.

```bash
git checkout <기준브랜치>
git pull origin <기준브랜치>
```

> staged 변경사항은 git 인덱스에 보존되므로 브랜치 전환 후에도 유지된다.

---

## Step 2. 작업 브랜치 생성

staged 변경사항을 분석해 브랜치명을 자동 생성한다.

**형식**: `{type}/{kebab-case-brief-description}` (최대 4단어)

예시:

- `feat/login-form-validation`
- `fix/date-format-bug`
- `chore/update-dependencies`
- `refactor/auth-middleware`

```bash
git checkout -b <생성된-브랜치명>
```

---

## Step 3. 커밋 메시지 생성 및 커밋

commit-helper 스킬 규칙으로 staged 변경사항 분석 후 커밋 메시지 생성:

- 타입 프리픽스: **영어** (`feat`, `fix`, `chore` 등)
- 제목 / Body: **한글**

```bash
git commit -m "$(cat <<'EOF'
{생성된 커밋 메시지}

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"
```

---

## Step 4. 푸시

```bash
git push -u origin <작업브랜치명>
```

---

## Step 5. 기준 브랜치에 머지

```bash
git checkout <기준브랜치>
git merge <작업브랜치명>
git push origin <기준브랜치>
```

머지 충돌 발생 시:

- 충돌 파일 목록 표시
- 사용자에게 충돌 해결 요청 후 플로우 재개

---

## Step 6. 작업 브랜치 삭제

머지 완료 후 작업 브랜치를 로컬 및 원격에서 삭제한다.

```bash
git branch -d <작업브랜치명>
git push origin --delete <작업브랜치명>
```

---

## Step 7. 기준 브랜치 최신화

```bash
git pull origin <기준브랜치>
```

---

## 완료 요약

플로우 완료 후 아래 형식으로 출력:

```
✅ 기준 브랜치 : <기준브랜치>
✅ 작업 브랜치 : <작업브랜치명>
✅ 커밋        : <커밋 메시지 한 줄 요약>
✅ 현재 위치   : <기준브랜치> (최신화 완료)
```
