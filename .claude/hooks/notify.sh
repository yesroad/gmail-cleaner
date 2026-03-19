#!/bin/bash
# AI 코딩 에이전트 - 사용자 입력 필요 시 Mac 알림
# Claude Code / Cursor / OpenCode 훅에서 자동 호출됨
#
# 환경변수:
#   NOTIFIER_TITLE   - 알림 제목 (기본값: AI Agent)
#   NOTIFIER_MESSAGE - 알림 메시지
#   CLAUDE_NOTIFICATION_TITLE - Claude Code 전용 메시지 (하위 호환)

TITLE="${NOTIFIER_TITLE:-AI Agent}"
MESSAGE="${NOTIFIER_MESSAGE:-${CLAUDE_NOTIFICATION_TITLE:-확인이 필요합니다}}"

# terminal-notifier를 사용한 배너 알림 (macOS 15 Sequoia 호환)
NOTIFIER=$(command -v terminal-notifier || echo "/opt/homebrew/bin/terminal-notifier")
"$NOTIFIER" -title "$TITLE" -message "$MESSAGE" -sound Glass

# 터미널 벨 소리 (터미널 포커스 없을 때 추가 알림)
echo -e "\a"
