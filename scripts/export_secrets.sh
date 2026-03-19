#!/bin/bash
# GitHub Secrets 설정용 base64 값 출력 스크립트
# 사용법: bash scripts/export_secrets.sh

set -e

echo "========================================"
echo "  GitHub Secrets 설정 가이드"
echo "========================================"
echo ""

# 1. credentials
if [ -f "credentials/credentials.json" ]; then
  echo "[1] Secret 이름: GMAIL_CREDENTIALS_B64"
  echo "    값 (아래 전체 복사):"
  base64 -i credentials/credentials.json
  echo ""
else
  echo "[1] credentials/credentials.json 파일이 없습니다."
  echo ""
fi

# 2. tokens bundle
if [ -d "tokens" ] && ls tokens/token_*.json 1>/dev/null 2>&1; then
  echo "[2] Secret 이름: GMAIL_TOKENS_BUNDLE_B64"
  echo "    값 (아래 전체 복사):"
  tar czf - tokens/ | base64
  echo ""
else
  echo "[2] tokens/ 디렉토리가 없거나 토큰 파일이 없습니다."
  echo "    python3 main.py 로 먼저 계정 인증을 완료하세요."
  echo ""
fi

# 3. emails 목록
if [ -d "tokens" ]; then
  EMAILS=""
  for meta in tokens/*.meta.json; do
    [ -f "$meta" ] || continue
    email=$(python3 -c "import json; print(json.load(open('$meta'))['email'])")
    if [ -z "$EMAILS" ]; then
      EMAILS="$email"
    else
      EMAILS="$EMAILS,$email"
    fi
  done

  if [ -n "$EMAILS" ]; then
    echo "[3] Secret 이름: GMAIL_EMAILS"
    echo "    값: $EMAILS"
    echo ""
  fi
fi

echo "[4] Secret 이름: CLEANUP_CATEGORIES (선택사항)"
echo "    기본값: 스팸 (SPAM) 프로모션"
echo "    선택 가능: '스팸 (SPAM)' '프로모션' '소셜' '업데이트' '휴지통 (TRASH)'"
echo ""
echo "========================================"
echo "  설정 위치: GitHub 저장소 → Settings → Secrets and variables → Actions"
echo "========================================"
