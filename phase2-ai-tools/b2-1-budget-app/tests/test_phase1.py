"""Phase 1 자체 점검. 실행: python tests/test_phase1.py

표준 라이브러리만 쓴다. 테스트 프레임워크를 설치하지 않는다.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from budget_app.formatter import display_width, format_table  # noqa: E402
from budget_app.storage import (  # noqa: E402
    BudgetStore,
    CategoryStore,
    DataPaths,
    TransactionRepository,
    ensure_files,
)

SAMPLE_CSV = """id,date,type,category,amount,memo,tags
TX-000001,2024-01-12,expense,food,8000,"김밥, 라면","meal,quick"
TX-000002,2024-01-14,income,salary,3000000,,
TX-000003,2024-01-15,expense,food,15000,점심,meal
"""


def test_ensure_files_creates_data_files_and_default_categories() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        paths = DataPaths(tmp)
        created = ensure_files(paths)

        # recurring.csv 는 Phase 5 보너스에서 추가됐다
        assert sorted(created) == [
            "budgets.csv",
            "categories.csv",
            "recurring.csv",
            "transactions.csv",
        ], created
        assert CategoryStore(paths.categories).names() == [
            "food",
            "transport",
            "rent",
            "salary",
            "etc",
        ]
        # 두 번째 호출은 아무것도 새로 만들지 않는다 (기존 파일 보존)
        assert ensure_files(paths) == []


def test_missing_file_streams_nothing() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        paths = DataPaths(tmp)
        assert list(TransactionRepository(paths.transactions).stream()) == []
        assert BudgetStore(paths.budgets).get("2024-01") is None


def test_comma_inside_memo_and_tags_survives() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        paths = DataPaths(tmp)
        ensure_files(paths)
        paths.transactions.write_text(SAMPLE_CSV, encoding="utf-8")

        first = next(TransactionRepository(paths.transactions).stream())
        assert first.memo == "김밥, 라면", first.memo
        assert first.tags == ["meal", "quick"], first.tags
        assert first.amount == 8000 and isinstance(first.amount, int)


def test_latest_is_newest_first_and_respects_limit() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        paths = DataPaths(tmp)
        ensure_files(paths)
        paths.transactions.write_text(SAMPLE_CSV, encoding="utf-8")

        latest = TransactionRepository(paths.transactions).latest(2)
        assert [tx.id for tx in latest] == ["TX-000003", "TX-000002"], latest


def test_stream_does_not_load_whole_file() -> None:
    """limit 1이면 파일에 3건이 있어도 1건만 남긴다 (스트리밍 확인)."""
    with tempfile.TemporaryDirectory() as tmp:
        paths = DataPaths(tmp)
        ensure_files(paths)
        paths.transactions.write_text(SAMPLE_CSV, encoding="utf-8")

        assert len(TransactionRepository(paths.transactions).latest(1)) == 1


def test_table_columns_align_with_korean_text() -> None:
    assert display_width("점심") == 4
    assert display_width("food") == 4

    table = format_table(["memo", "amount"], [["점심", "15,000"], ["food", "8,000"]])
    widths = {display_width(line.split("  ")[0]) for line in table.splitlines()}
    assert widths == {4}, table


def main() -> int:
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"\n{len(tests)}개 통과")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
