#!/bin/bash
# Claude Code 보일러플레이트 초기 설정 스크립트

set -e

echo "Claude Code 설정을 시작합니다..."

# Homebrew 설치 확인
if ! command -v brew &>/dev/null; then
  echo "Homebrew가 없습니다. 설치 중..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
  echo "Homebrew 확인 완료"
fi

# terminal-notifier 설치 확인
if ! command -v terminal-notifier &>/dev/null; then
  echo "terminal-notifier 설치 중..."
  brew install terminal-notifier
else
  echo "terminal-notifier 확인 완료"
fi

# 훅 스크립트 실행 권한 부여
chmod +x .claude/hooks/notify.sh
echo "훅 스크립트 권한 설정 완료"

# 테스트 알림
echo "테스트 알림 발송 중..."
bash .claude/hooks/notify.sh

echo "설정 완료!"
