"""계정/작업 선택 메뉴 (questionary)"""

import questionary
from questionary import Style

MENU_STYLE = Style([
    ("qmark", "fg:#00bcd4 bold"),
    ("question", "bold"),
    ("answer", "fg:#00bcd4 bold"),
    ("pointer", "fg:#00bcd4 bold"),
    ("highlighted", "fg:#00bcd4 bold"),
    ("selected", "fg:#00bcd4"),
])

TASK_CHOICES = [
    "스팸/프로모션/소셜/업데이트/휴지통 비우기",
    "읽지 않은 메일 전체 읽음 처리",
    "특정 발신자 메일 삭제",
    "N일 이상 오래된 메일 삭제",
    "N MB 이상 대용량 메일 삭제",
    "라벨 기준 정리",
    "자동 라벨 분류",
    "─────────────────",
    "다른 계정으로 전환",
    "종료",
]


def select_account(accounts: list[str]) -> str | None:
    """인증된 계정 중 선택 또는 새 계정 추가"""
    choices = []
    if accounts:
        choices.append("⚡ 전체 계정 일괄 작업")
    choices += accounts + ["+ 새 계정 추가", "종료"]
    answer = questionary.select(
        "Gmail 계정을 선택하세요:",
        choices=choices,
        style=MENU_STYLE,
    ).ask()
    return answer


BULK_TASK_CHOICES = [
    "스팸/프로모션/소셜/업데이트/휴지통 비우기",
    "읽지 않은 메일 전체 읽음 처리",
    "특정 발신자 메일 삭제",
    "N일 이상 오래된 메일 삭제",
    "취소",
]


def select_task_bulk() -> str | None:
    """일괄 작업용 작업 선택"""
    answer = questionary.select(
        "일괄 적용할 작업을 선택하세요:",
        choices=BULK_TASK_CHOICES,
        style=MENU_STYLE,
    ).ask()
    return None if answer == "취소" else answer


def select_accounts_checkbox(accounts: list[str]) -> list[str]:
    """일괄 적용할 계정 다중 선택"""
    choices = [{"name": a, "value": a, "checked": True} for a in accounts]
    selected = questionary.checkbox(
        "적용할 계정을 선택하세요 (스페이스바로 선택/해제):",
        choices=choices,
        style=MENU_STYLE,
    ).ask()
    return selected or []


def select_task() -> str | None:
    """수행할 작업 선택"""
    answer = questionary.select(
        "수행할 작업을 선택하세요:",
        choices=[c for c in TASK_CHOICES if c != "─────────────────"],
        style=MENU_STYLE,
    ).ask()
    return answer


def select_categories(available: list[str]) -> list[str]:
    """비울 카테고리 다중 선택"""
    return questionary.checkbox(
        "비울 카테고리를 선택하세요 (스페이스바로 선택):",
        choices=available,
        style=MENU_STYLE,
    ).ask() or []


def input_sender_email() -> str | None:
    """발신자 이메일 입력"""
    return questionary.text(
        "삭제할 발신자 이메일 주소:",
        style=MENU_STYLE,
    ).ask()


def input_days() -> int | None:
    """날짜 수 입력"""
    answer = questionary.text(
        "몇 일 이상 오래된 메일을 삭제할까요? (예: 365):",
        style=MENU_STYLE,
        validate=lambda x: x.isdigit() and int(x) > 0 or "양의 정수를 입력하세요",
    ).ask()
    return int(answer) if answer else None


def input_size_mb() -> int | None:
    """크기(MB) 입력"""
    answer = questionary.text(
        "몇 MB 이상 대용량 메일을 대상으로 할까요? (예: 10):",
        style=MENU_STYLE,
        validate=lambda x: x.isdigit() and int(x) > 0 or "양의 정수를 입력하세요",
    ).ask()
    return int(answer) if answer else None


def select_large_mails(messages: list[dict]) -> list[str]:
    """대용량 메일 다중 선택"""
    choices = [
        {
            "name": f"[{msg['size_mb']}MB] {msg['from'][:30]} - {msg['subject'][:40]}",
            "value": msg["id"],
        }
        for msg in messages
    ]
    selected = questionary.checkbox(
        "삭제할 메일을 선택하세요:",
        choices=choices,
        style=MENU_STYLE,
    ).ask()
    return selected or []


def select_label(labels: list[dict]) -> dict | None:
    """라벨 선택"""
    if not labels:
        return None
    choices = [{"name": l["name"], "value": l} for l in labels]
    return questionary.select(
        "대상 라벨을 선택하세요:",
        choices=choices,
        style=MENU_STYLE,
    ).ask()


def select_label_action() -> str | None:
    """라벨 작업 선택"""
    return questionary.select(
        "라벨 내 메일을 어떻게 처리할까요?",
        choices=["삭제", "아카이브", "읽음 처리"],
        style=MENU_STYLE,
    ).ask()


def select_labels_for_apply(label_counts: dict[str, int]) -> list[str]:
    """라벨 분류 결과에서 적용할 라벨 다중 선택."""
    choices = [
        {
            "name": f"{label} ({count:,}건)",
            "value": label,
            "checked": True,
        }
        for label, count in label_counts.items()
        if count > 0
    ]
    if not choices:
        return []
    selected = questionary.checkbox(
        "적용할 라벨을 선택하세요 (스페이스바로 선택/해제):",
        choices=choices,
        style=MENU_STYLE,
    ).ask()
    return selected or []


def confirm(message: str) -> bool:
    """확인 프롬프트"""
    return questionary.confirm(message, style=MENU_STYLE).ask() or False
