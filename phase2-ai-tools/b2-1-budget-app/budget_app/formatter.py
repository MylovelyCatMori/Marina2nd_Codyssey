"""출력 포맷 계층. 값을 사람이 읽을 문자열로 바꾼다 (보너스 B-02).

외부 라이브러리(tabulate, rich)를 쓰지 않고 표준 라이브러리만으로 표를 맞춘다.
"""

from __future__ import annotations

import unicodedata

from .models import MonthlySummary, Transaction

COLUMN_GAP = "  "


def display_width(text: str) -> int:
    """터미널에서 차지하는 칸 수. 한글·한자는 두 칸이다.

    len()은 글자 수만 세므로 '점심'(2글자, 4칸)과 'food'(4글자, 4칸)를 같게 본다.
    그대로 쓰면 한글이 섞인 표의 세로줄이 어긋난다.
    """
    return sum(2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1 for ch in text)


def _pad(text: str, width: int, right_align: bool = False) -> str:
    space = " " * max(0, width - display_width(text))
    return space + text if right_align else text + space


def format_table(
    header: list[str], rows: list[list[str]], right_align: set[int] | None = None
) -> str:
    """헤더와 행들을 열 너비에 맞춰 정렬한 표 문자열로 만든다.

    right_align 에 들어간 열 번호는 오른쪽으로 붙인다. 숫자는 자릿수를 맞춰야
    크기를 눈으로 비교할 수 있다.
    """
    columns = right_align or set()
    widths = [display_width(name) for name in header]
    for row in rows:
        for index, cell in enumerate(row):
            widths[index] = max(widths[index], display_width(cell))

    def line(cells: list[str]) -> str:
        return COLUMN_GAP.join(
            _pad(cell, widths[i], i in columns) for i, cell in enumerate(cells)
        ).rstrip()

    lines = [line(header), COLUMN_GAP.join("-" * width for width in widths)]
    lines.extend(line(row) for row in rows)
    return "\n".join(lines)


def format_amount(amount: int) -> str:
    """천 단위 쉼표를 넣는다."""
    return f"{amount:,}"


def format_transactions(transactions: list[Transaction]) -> str:
    """거래 목록을 표로 만든다."""
    header = ["id", "date", "type", "category", "amount", "memo", "tags"]
    rows = [
        [
            tx.id,
            tx.date,
            tx.type,
            tx.category,
            format_amount(tx.amount),
            tx.memo,
            ",".join(tx.tags),
        ]
        for tx in transactions
    ]
    return format_table(header, rows, right_align={4})  # amount 열만 오른쪽 정렬


def format_summary(summary: MonthlySummary) -> str:
    """월 요약을 여러 줄로 만든다. 예산이 없으면 예산 줄 자체를 넣지 않는다."""
    lines = [
        f"[{summary.month}] 거래 {summary.count}건",
        "",
        format_table(
            ["항목", "금액"],
            [
                ["총수입", f"{format_amount(summary.total_income)}원"],
                ["총지출", f"{format_amount(summary.total_expense)}원"],
                ["잔액", f"{format_amount(summary.balance)}원"],
            ],
            right_align={1},
        ),
    ]

    if summary.top_categories:
        lines.append("")
        lines.append(f"카테고리별 지출 TOP {len(summary.top_categories)}")
        lines.append(
            format_table(
                ["카테고리", "지출"],
                [[name, f"{format_amount(amount)}원"] for name, amount in summary.top_categories],
                right_align={1},
            )
        )

    usage = summary.usage_percent
    if usage is not None and summary.budget is not None:
        lines.append("")
        lines.append(f"예산 {format_amount(summary.budget)}원 / 사용률 {usage:.1f}%")
        if summary.is_over_budget:
            over = summary.total_expense - summary.budget
            lines.append(f"[경고] 예산을 {format_amount(over)}원 초과했습니다.")

    return "\n".join(lines)
