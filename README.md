# Gmail Cleaner

Gmail 계정을 대화형 CLI로 정리하는 Python 도구. 다중 계정을 지원하며 GitHub Actions로 자동화할 수 있습니다.

## 주요 기능

| 기능 | 설명 |
|------|------|
| 스팸/프로모션 비우기 | 스팸·프로모션·소셜·업데이트·휴지통 일괄 삭제 |
| 읽음 처리 | 받은편지함 전체 읽음 처리 |
| 발신자별 삭제 | 특정 발신자의 모든 메일 삭제 |
| 오래된 메일 삭제 | N일 이상 된 메일 삭제 |
| 대용량 메일 삭제 | N MB 이상 메일 선택 삭제 |
| 라벨 기준 정리 | 특정 라벨 메일 삭제·아카이브·읽음 처리 |
| 빈 라벨 삭제 | 메일이 없는 라벨 일괄 삭제 |
| **자동 라벨 분류** | 받은편지함을 분석해 카테고리별 라벨 자동 적용 |

### 자동 라벨 분류 규칙

받은편지함 **전체**를 분석해 아래 라벨을 자동 생성합니다. 발신자 도메인 정확 매칭(100점) → Gmail 카테고리(70점) → 발신자 키워드(50점) → 제목 키워드(30점) 순서로 점수를 합산해 가장 높은 규칙으로 분류합니다.

| 라벨 | 분류 기준 |
|------|-----------|
| 인증/보안 | 인증번호·OTP·비밀번호 재설정·새로운 로그인 등 제목 키워드 |
| 구매/배송 | coupang.co.kr·baemin.kr·amazon.com 등 도메인, 주문·배송·택배 등 제목 키워드 |
| 금융/결제 | shinhan.com·kbcard.com·kakaobank.com 등 도메인, 청구서·이체·카드대금 등 제목 키워드 |
| 여행/항공 | koreanair.com·airbnb.com·booking.com 등 도메인, 항공권·예약·숙박 등 제목 키워드 |
| 구독/멤버십 | netflix.com·spotify.com·notion.so 등 도메인, 구독·갱신·subscription 등 제목 키워드 |
| 채용/커리어 | wanted.co.kr·linkedin.com·programmers.co.kr 등 도메인, 채용·합격·면접 등 제목 키워드 |
| 의료/건강 | nhis.or.kr·nps.or.kr 도메인, 진료·건강검진·처방 등 제목 키워드 |
| 공공/행정 | nts.go.kr·hometax.go.kr 등 도메인, 고지서·세금·민원 등 제목 키워드 |
| 교육 | inflearn.com·udemy.com·coursera.org 등 도메인, 강의·수료·certificate 등 제목 키워드 |
| 뉴스레터 | 프로모션 탭, mailchimp.com·substack.com·stibee.com 등 도메인 |
| 소셜 | 소셜 탭, facebookmail.com·discord.com 등 도메인 |
| 업데이트/알림 | 업데이트 탭, 공지사항·점검·출시 등 제목 키워드 |
| 기타 | 위 규칙에 미매칭 |

---

## 시작하기

### 1. GCP OAuth 설정

1. [Google Cloud Console](https://console.cloud.google.com) → 새 프로젝트 생성
2. **API 및 서비스 → Gmail API 활성화**
3. **사용자 인증 정보 → OAuth 2.0 클라이언트 ID 생성** (데스크톱 앱)
4. 다운로드한 JSON 파일을 `credentials/credentials.json`으로 저장

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 실행

```bash
python3 main.py
```

최초 실행 시 브라우저가 열리며 Google 계정 인증을 요청합니다. 완료되면 `tokens/` 디렉토리에 토큰이 저장됩니다.

---

## GitHub Actions 자동화

### 스케줄

| 워크플로우 | 주기 | 작업 |
|-----------|------|------|
| `auto-label.yml` | 매주 일요일 (한국 오전 11시) | 자동 라벨 분류 |
| `cleanup.yml` | 매월 1일 (한국 오전 11시) | 스팸·프로모션 삭제 |

### 설정 방법

**1단계 — 토큰 준비**

로컬에서 먼저 인증을 완료합니다.

```bash
python3 main.py   # 계정 인증 완료
```

**2단계 — Secrets 값 추출**

```bash
bash scripts/export_secrets.sh
```

**3단계 — GitHub Secrets 등록**

저장소 → **Settings → Secrets and variables → Actions**

| Secret 이름 | 내용 |
|-------------|------|
| `GMAIL_CREDENTIALS_B64` | `credentials.json` base64 인코딩 값 |
| `GMAIL_TOKENS_BUNDLE_B64` | `tokens/` 디렉토리 tar.gz base64 인코딩 값 |
| `GMAIL_EMAILS` | Gmail 주소 (여러 개면 콤마로 구분: `a@gmail.com,b@gmail.com`) |
| `CLEANUP_CATEGORIES` | (선택) 삭제 대상 카테고리, 기본값: `spam promotions` / 선택 가능: `spam promotions social updates trash` |

**4단계 — 수동 테스트**

저장소 → **Actions** 탭 → 워크플로우 선택 → **Run workflow**

> 토큰은 6개월 미사용 시 만료됩니다. 만료 시 로컬 재인증 후 `GMAIL_TOKENS_BUNDLE_B64`만 다시 등록하세요.

---

## 디렉토리 구조

```
gmail-cleaner/
├── main.py                  # 진입점 + 대화형/headless 실행
├── auth.py                  # OAuth 인증 + 다중 계정 토큰 관리
├── cleaner/
│   ├── base.py              # BaseCleaner 추상 클래스
│   ├── auto_label.py        # 자동 라벨 분류 (도메인 fallback 포함)
│   ├── spam_promo.py        # 스팸/프로모션 삭제
│   ├── unread.py            # 읽음 처리
│   ├── sender.py            # 발신자별 삭제
│   ├── old_mail.py          # 오래된 메일 삭제
│   ├── large_mail.py        # 대용량 메일 삭제
│   └── label.py             # 라벨 기준 정리
├── ui/
│   ├── console.py           # Rich 기반 출력
│   ├── menu.py              # questionary 대화형 메뉴
│   └── progress.py          # 진행률 바
├── utils/
│   ├── query_builder.py     # Gmail 쿼리 문자열 생성
│   └── batch.py             # Gmail API 배치 처리
├── .github/workflows/
│   ├── auto-label.yml       # 매주 자동 라벨 분류
│   └── cleanup.yml          # 매월 불필요한 메일 삭제
├── scripts/
│   └── export_secrets.sh    # GitHub Secrets 설정 헬퍼
└── requirements.txt
```

---

## Headless 모드 (CLI)

GitHub Actions 또는 스크립트에서 직접 실행할 때 사용합니다.

```bash
# 자동 라벨 분류
python3 main.py --headless --task auto-label --email user@gmail.com

# 기존 라벨 초기화 후 재분류 (규칙 변경 시 권장)
python3 main.py --headless --task auto-label --reset --email user@gmail.com

# 스팸/프로모션 삭제
python3 main.py --headless --task cleanup --email user@gmail.com

# 삭제 카테고리 직접 지정
python3 main.py --headless --task cleanup --email user@gmail.com \
  --categories spam promotions social
```

---

## 보안 주의사항

- `credentials/`, `tokens/` 디렉토리는 `.gitignore`에 등록되어 있습니다. **절대 커밋하지 마세요.**
- OAuth 스코프: `https://mail.google.com/` (읽기·수정·삭제 권한 포함)
