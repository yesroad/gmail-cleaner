"""rich Progress Bar 래퍼"""

from contextlib import contextmanager
from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TaskProgressColumn,
    TimeElapsedColumn,
)
from ui.console import console


@contextmanager
def progress_bar(description: str, total: int):
    """
    진행 상황 표시 컨텍스트 매니저.

    사용법:
        with progress_bar("삭제 중", total=1000) as update:
            batch_delete(service, ids, progress_callback=update)
    """
    with Progress(
        SpinnerColumn(),
        "[progress.description]{task.description}",
        BarColumn(),
        TaskProgressColumn(),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task(description, total=total)

        def update(done: int, total: int):
            progress.update(task, completed=done, total=total)

        yield update
