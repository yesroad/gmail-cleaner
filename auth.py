"""Gmail OAuth 인증 모듈 - 다중 계정 지원"""

import json
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://mail.google.com/",
]

CREDENTIALS_DIR = Path("credentials")
TOKENS_DIR = Path("tokens")
CREDENTIALS_FILE = CREDENTIALS_DIR / "credentials.json"


def get_token_path(account: str) -> Path:
    """계정 이메일로 토큰 파일 경로 반환"""
    safe_name = account.replace("@", "_at_").replace(".", "_")
    return TOKENS_DIR / f"token_{safe_name}.json"


def get_meta_path(token_path: Path) -> Path:
    """토큰 파일에 대응하는 메타 파일 경로 반환"""
    return token_path.with_suffix("").with_suffix(".meta.json")


def get_account_email(service) -> str:
    """Gmail API로 실제 이메일 주소 조회"""
    profile = service.users().getProfile(userId="me").execute()
    return profile["emailAddress"]


def save_account_metadata(token_path: Path, email: str) -> None:
    """토큰에 대응하는 메타 파일에 실제 이메일 저장"""
    meta_path = get_meta_path(token_path)
    with open(meta_path, "w") as f:
        json.dump({"email": email}, f)


def authenticate(account: str) -> any:
    """계정별 Gmail API 서비스 객체 반환. 최초 실행 시 브라우저 인증."""
    TOKENS_DIR.mkdir(exist_ok=True)

    if not CREDENTIALS_FILE.exists():
        raise FileNotFoundError(
            f"[오류] credentials.json 파일이 없습니다.\n"
            f"GCP 콘솔에서 OAuth 2.0 클라이언트 ID를 다운로드하여\n"
            f"'{CREDENTIALS_FILE}' 경로에 저장하세요."
        )

    token_path = get_token_path(account)
    creds = None

    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(token_path, "w") as f:
            f.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)

    # 최초 인증 후 메타 파일이 없으면 실제 이메일 저장
    meta_path = get_meta_path(token_path)
    if not meta_path.exists():
        real_email = get_account_email(service)
        save_account_metadata(token_path, real_email)

    return service


def authenticate_new_account() -> tuple[any, str]:
    """새 계정 추가: 임시 토큰으로 인증 후 실제 이메일로 파일 재저장"""
    TOKENS_DIR.mkdir(exist_ok=True)

    if not CREDENTIALS_FILE.exists():
        raise FileNotFoundError("[오류] credentials.json 파일이 없습니다.")

    flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
    creds = flow.run_local_server(port=0)

    # 임시 파일에 저장 후 실제 이메일 확인
    temp_path = TOKENS_DIR / "token_temp.json"
    with open(temp_path, "w") as f:
        f.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)
    real_email = get_account_email(service)

    # 실제 이메일로 파일명 결정 후 이동
    token_path = get_token_path(real_email)
    temp_path.rename(token_path)
    save_account_metadata(token_path, real_email)

    return service, real_email


def list_authenticated_accounts() -> list[str]:
    """토큰 파일이 있는 계정 목록 반환 (meta 파일 우선)"""
    if not TOKENS_DIR.exists():
        return []

    accounts = []
    for token_path in TOKENS_DIR.glob("token_*.json"):
        if token_path.stem == "token_temp" or token_path.stem.endswith(".meta"):
            continue
        meta_path = get_meta_path(token_path)
        if meta_path.exists():
            with open(meta_path) as f:
                data = json.load(f)
                accounts.append(data["email"])
        else:
            # meta 파일 없을 경우 파일명에서 복원 시도
            raw = token_path.stem[len("token_") :]
            if "_at_" in raw:
                local, domain_raw = raw.split("_at_", 1)
                domain = domain_raw.replace("_", ".")
                accounts.append(f"{local}@{domain}")
            else:
                accounts.append(raw)

    return accounts
