"""Gmail Cleaner 진입점"""

import sys
from auth import (
    authenticate,
    authenticate_new_account,
    list_authenticated_accounts,
)
from cleaner.spam_promo import SpamPromoCleaner, get_available_categories
from cleaner.unread import UnreadCleaner
from cleaner.sender import SenderCleaner
from cleaner.old_mail import OldMailCleaner
from cleaner.large_mail import LargeMailCleaner
from cleaner.label import LabelCleaner
from cleaner.auto_label import AutoLabelCleaner
from ui.console import (
    console,
    print_header,
    print_success,
    print_error,
    print_warning,
    print_info,
    print_count,
    print_result,
    print_large_mail_table,
    print_auto_label_table,
)
from ui.progress import progress_bar
from ui import menu


def flow_spam_promo(service, *, categories: list[str] | None = None) -> None:
    if categories is None:
        available = get_available_categories()
        categories = menu.select_categories(available)
        if not categories:
            print_warning("선택된 카테고리 없음")
            return

    cleaner = SpamPromoCleaner(service, categories)
    print_info("대상 메일 수 확인 중...")
    count = cleaner.preview()
    print_count("삭제 대상", count)

    if count == 0 or not menu.confirm(f"{count:,}건을 삭제할까요?"):
        return

    with progress_bar("삭제 중", total=count) as update:
        deleted = cleaner.execute(progress_callback=update)
    print_result("삭제", deleted)


def flow_unread(service) -> None:
    cleaner = UnreadCleaner(service)
    print_info("읽지 않은 메일 수 확인 중...")
    count = cleaner.preview()
    print_count("읽음 처리 대상", count)

    if count == 0 or not menu.confirm(f"{count:,}건을 읽음 처리할까요?"):
        return

    with progress_bar("읽음 처리 중", total=count) as update:
        done = cleaner.execute(progress_callback=update)
    print_result("읽음 처리", done)


def flow_sender(service, *, sender: str | None = None) -> None:
    if sender is None:
        sender = menu.input_sender_email()
        if not sender:
            return

    cleaner = SenderCleaner(service, sender)
    print_info(f"'{sender}' 발신 메일 수 확인 중...")
    count = cleaner.preview()
    print_count("삭제 대상", count)

    if count == 0 or not menu.confirm(f"{count:,}건을 삭제할까요?"):
        return

    with progress_bar("삭제 중", total=count) as update:
        deleted = cleaner.execute(progress_callback=update)
    print_result("삭제", deleted)


def flow_old_mail(service, *, days: int | None = None) -> None:
    if days is None:
        days = menu.input_days()
        if not days:
            return

    cleaner = OldMailCleaner(service, days)
    print_info(f"{days}일 이상 오래된 메일 수 확인 중...")
    count = cleaner.preview()
    print_count("삭제 대상", count)

    if count == 0 or not menu.confirm(f"{count:,}건을 삭제할까요?"):
        return

    with progress_bar("삭제 중", total=count) as update:
        deleted = cleaner.execute(progress_callback=update)
    print_result("삭제", deleted)


def flow_large_mail(service) -> None:
    size_mb = menu.input_size_mb()
    if not size_mb:
        return

    cleaner = LargeMailCleaner(service, size_mb)
    print_info(f"{size_mb}MB 이상 메일 목록 수집 중...")
    messages = cleaner.get_messages_with_info()

    if not messages:
        print_warning("해당하는 메일이 없습니다.")
        return

    print_large_mail_table(messages)
    selected_ids = menu.select_large_mails(messages)

    if not selected_ids:
        print_warning("선택된 메일 없음")
        return

    if not menu.confirm(f"{len(selected_ids)}건을 삭제할까요?"):
        return

    with progress_bar("삭제 중", total=len(selected_ids)) as update:
        deleted = cleaner.execute(selected_ids=selected_ids, progress_callback=update)
    print_result("삭제", deleted)


def flow_label(service) -> None:
    cleaner = LabelCleaner(service, "")
    labels = cleaner.get_labels()

    if not labels:
        print_warning("사용자 정의 라벨이 없습니다.")
        return

    label = menu.select_label(labels)
    if not label:
        return

    # 선택된 라벨로 cleaner 재생성
    cleaner = LabelCleaner(service, label["name"])
    action = menu.select_label_action()
    if not action:
        return

    print_info(f"'{label['name']}' 라벨 메일 수 확인 중...")
    count = cleaner.preview()
    print_count(f"{action} 대상", count)

    if count == 0 or not menu.confirm(f"{count:,}건을 {action}할까요?"):
        return

    with progress_bar(f"{action} 중", total=count) as update:
        if action == "삭제":
            done = cleaner.execute(progress_callback=update)
        elif action == "아카이브":
            done = cleaner.archive(progress_callback=update)
        else:
            done = cleaner.mark_read(progress_callback=update)
    print_result(action, done)


def flow_auto_label(service, **_) -> None:
    cleaner = AutoLabelCleaner(service)
    print_info("받은편지함 메시지 ID 수집 중...")
    msg_ids = cleaner.fetch_message_ids()
    print_count("분석 대상", len(msg_ids))

    if not msg_ids:
        return

    with progress_bar("분석 중", total=len(msg_ids)) as update:
        classified = cleaner.analyze(msg_ids, progress_callback=update)

    label_counts = {label: len(ids) for label, ids in classified.items()}
    matched = {k: v for k, v in label_counts.items() if v > 0}

    if not matched:
        print_warning("분류된 메일이 없습니다.")
        return

    print_auto_label_table(matched)
    selected_labels = menu.select_labels_for_apply(matched)

    if not selected_labels:
        print_warning("선택된 라벨 없음")
        return

    total_count = sum(len(classified[l]) for l in selected_labels)
    if not menu.confirm(f"{total_count:,}건에 라벨을 적용할까요?"):
        return

    with progress_bar("라벨 적용 중", total=len(selected_labels)) as update:
        results = cleaner.execute(classified, selected_labels, progress_callback=update)

    for label_name, count in results.items():
        print_result(f"[{label_name}] 라벨 적용", count)


TASK_FLOWS = {
    "스팸/프로모션/소셜/업데이트/휴지통 비우기": flow_spam_promo,
    "읽지 않은 메일 전체 읽음 처리": flow_unread,
    "특정 발신자 메일 삭제": flow_sender,
    "N일 이상 오래된 메일 삭제": flow_old_mail,
    "N MB 이상 대용량 메일 삭제": flow_large_mail,
    "라벨 기준 정리": flow_label,
    "자동 라벨 분류": flow_auto_label,
}


def collect_bulk_params(task: str) -> dict | None:
    """일괄 작업용 파라미터 수집. None이면 취소."""
    if task == "스팸/프로모션/소셜/업데이트/휴지통 비우기":
        categories = menu.select_categories(get_available_categories())
        return {"categories": categories} if categories else None
    elif task == "읽지 않은 메일 전체 읽음 처리":
        return {}
    elif task == "특정 발신자 메일 삭제":
        sender = menu.input_sender_email()
        return {"sender": sender} if sender else None
    elif task == "N일 이상 오래된 메일 삭제":
        days = menu.input_days()
        return {"days": days} if days else None
    return None


def run_bulk_mode(accounts: list[str]) -> None:
    """전체 계정 일괄 작업 모드: 작업 선택 → 파라미터 수집 → 계정 선택 → 순차 실행"""
    task = menu.select_task_bulk()
    if not task:
        return

    params = collect_bulk_params(task)
    if params is None:
        print_warning("입력 취소됨")
        return

    selected_accounts = menu.select_accounts_checkbox(accounts)
    if not selected_accounts:
        print_warning("선택된 계정 없음")
        return

    flow_fn = TASK_FLOWS[task]
    for email in selected_accounts:
        print_header(f"Gmail Cleaner — {email}")
        try:
            service = authenticate(email)
            flow_fn(service, **params)
        except Exception as e:
            print_error(f"[{email}] 오류: {e}")
        console.print()


def run_account_session(service, email: str) -> bool:
    """한 계정에 대한 작업 루프. True면 계정 전환, False면 종료."""
    print_header(f"Gmail Cleaner — {email}")

    while True:
        task = menu.select_task()
        if not task:
            return False

        if task == "종료":
            return False
        elif task == "다른 계정으로 전환":
            return True

        flow_fn = TASK_FLOWS.get(task)
        if flow_fn:
            try:
                flow_fn(service)
            except KeyboardInterrupt:
                print_warning("작업 취소됨")
            except Exception as e:
                print_error(f"오류 발생: {e}")
        console.print()


def main() -> None:
    print_header("Gmail Cleaner")

    while True:
        accounts = list_authenticated_accounts()

        account_choice = menu.select_account(accounts)
        if not account_choice or account_choice == "종료":
            print_info("종료합니다.")
            break

        if account_choice == "⚡ 전체 계정 일괄 작업":
            run_bulk_mode(accounts)
            continue

        try:
            if account_choice == "+ 새 계정 추가":
                print_info("브라우저에서 Google 계정 인증을 완료하세요...")
                service, email = authenticate_new_account()
                print_success(f"새 계정 추가: {email}")
            else:
                email = account_choice
                print_info(f"'{email}' 계정 인증 중...")
                service = authenticate(email)
                print_success(f"인증 완료: {email}")
        except FileNotFoundError as e:
            print_error(str(e))
            break
        except Exception as e:
            print_error(f"인증 실패: {e}")
            continue

        switch = run_account_session(service, email)
        if not switch:
            print_info("종료합니다.")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n종료합니다.")
        sys.exit(0)
