"""rich Console 래퍼 + 공통 출력 함수"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def print_header(title: str) -> None:
    console.print(Panel(f"[bold cyan]{title}[/]", expand=False))


def print_success(message: str) -> None:
    console.print(f"[bold green]✓[/] {message}")


def print_error(message: str) -> None:
    console.print(f"[bold red]✗[/] {message}")


def print_warning(message: str) -> None:
    console.print(f"[bold yellow]⚠[/] {message}")


def print_info(message: str) -> None:
    console.print(f"[dim]→[/] {message}")


def print_count(label: str, count: int) -> None:
    if count == 0:
        console.print(f"[dim]{label}: 해당 없음[/]")
    else:
        console.print(f"[bold]{label}:[/] [yellow]{count:,}[/]건")


def print_result(action: str, count: int) -> None:
    if count > 0:
        console.print(f"[bold green]✓ {action} 완료:[/] [yellow]{count:,}[/]건")
    else:
        console.print(f"[dim]{action}: 처리할 항목 없음[/]")


def print_auto_label_table(label_counts: dict[str, int]) -> None:
    table = Table(title="자동 라벨 분류 결과", show_lines=True)
    table.add_column("라벨", style="cyan")
    table.add_column("건수", style="yellow", justify="right")

    for label, count in label_counts.items():
        if count > 0:
            table.add_row(label, f"{count:,}")

    console.print(table)


def print_large_mail_table(messages: list[dict]) -> None:
    table = Table(title="대용량 메일 목록", show_lines=True)
    table.add_column("#", style="dim", width=4)
    table.add_column("크기(MB)", style="yellow", justify="right")
    table.add_column("발신자", style="cyan")
    table.add_column("제목")

    for i, msg in enumerate(messages, 1):
        table.add_row(
            str(i),
            str(msg["size_mb"]),
            msg["from"][:40],
            msg["subject"][:60],
        )
    console.print(table)
