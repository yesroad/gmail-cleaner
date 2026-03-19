---
name: setup-notifier
description: Claude Code 초기 환경 설정 (terminal-notifier 설치 및 훅 권한 설정)
---

아래 단계를 **순서대로 즉시 실행**하세요.

## Step 1. terminal-notifier 설치

`terminal-notifier`가 설치되어 있는지 확인하고, 없으면 설치하세요:

```bash
which terminal-notifier || brew install terminal-notifier
```

## Step 2. settings.local.json 훅 설정 (자동)

`.claude/settings.local.json` 파일을 확인해 아래 규칙에 따라 처리하세요:

**파일이 없는 경우** → `.claude/settings.local.json` 신규 생성:

```json
{
  "hooks": {
    "PermissionRequest": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash ./.claude/hooks/notify.sh",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

**파일이 이미 있는 경우** → 기존 내용에 `hooks` 키를 병합:

- 이미 `hooks.PermissionRequest` 항목이 있으면 → 중복 체크 후 아이템 추가
- `hooks` 키 자체가 없으면 → 최상위에 추가

병합할 내용:

```json
{
  "hooks": {
    "PermissionRequest": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash ./.claude/hooks/notify.sh",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

> 파일 수정 후 최종 내용을 출력해서 확인하세요.

## Step 3. 완료 확인

설정이 끝나면 아래를 출력하세요:

```
✓ terminal-notifier 설치 완료
✓ .claude/settings.local.json 훅 설정 완료
⚠ 설정 반영을 위해 Claude Code를 재시작하세요
```
