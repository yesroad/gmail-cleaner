"""Gmail API 페이지네이션 + 일괄 처리 유틸"""

from typing import Callable

MAX_LIST_RESULTS = 500
BATCH_CHUNK_SIZE = 1000


def collect_message_ids(
    service,
    query: str,
    progress_callback: Callable[[int], None] | None = None,
) -> list[str]:
    """쿼리에 해당하는 모든 메시지 ID 수집 (페이지네이션)"""
    ids = []
    page_token = None

    while True:
        params = {
            "userId": "me",
            "q": query,
            "maxResults": MAX_LIST_RESULTS,
        }
        if page_token:
            params["pageToken"] = page_token

        result = service.users().messages().list(**params).execute()
        messages = result.get("messages", [])
        ids.extend(msg["id"] for msg in messages)

        if progress_callback:
            progress_callback(len(ids))

        page_token = result.get("nextPageToken")
        if not page_token:
            break

    return ids


def batch_delete(
    service,
    message_ids: list[str],
    progress_callback: Callable[[int, int], None] | None = None,
) -> int:
    """메시지 ID 목록 일괄 삭제. 삭제된 총 건수 반환."""
    deleted = 0
    total = len(message_ids)

    for i in range(0, total, BATCH_CHUNK_SIZE):
        chunk = message_ids[i : i + BATCH_CHUNK_SIZE]
        service.users().messages().batchDelete(
            userId="me", body={"ids": chunk}
        ).execute()
        deleted += len(chunk)
        if progress_callback:
            progress_callback(deleted, total)

    return deleted


def batch_modify(
    service,
    message_ids: list[str],
    add_label_ids: list[str] | None = None,
    remove_label_ids: list[str] | None = None,
    progress_callback: Callable[[int, int], None] | None = None,
) -> int:
    """메시지 ID 목록 라벨 일괄 수정. 처리된 총 건수 반환."""
    modified = 0
    total = len(message_ids)
    body = {}
    if add_label_ids:
        body["addLabelIds"] = add_label_ids
    if remove_label_ids:
        body["removeLabelIds"] = remove_label_ids

    for i in range(0, total, BATCH_CHUNK_SIZE):
        chunk = message_ids[i : i + BATCH_CHUNK_SIZE]
        service.users().messages().batchModify(
            userId="me", body={"ids": chunk, **body}
        ).execute()
        modified += len(chunk)
        if progress_callback:
            progress_callback(modified, total)

    return modified
