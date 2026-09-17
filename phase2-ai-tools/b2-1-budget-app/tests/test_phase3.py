"""Phase 3 자체 점검. 실행: python tests/test_phase3.py"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from budget_app.errors import AppError, NotFoundError, ValidationError  # noqa: E402
from budget_app.models import Budget, SearchFilters, Transaction  # noqa: E402
from budget_app.services import (  # noqa: E402
    add_category,
    add_transaction,
    count_category_usage,
    newest_first,
    remove_category,
    search_transactions,
    summarize_month,
)
from budget_app.storage import (  # noqa: E402
    BudgetStore,
    CategoryStore,
    DataPaths,
    TransactionRepository,
    ensure_files,
)

ROWS = [
    ("TX-000001", "2024-01-05", "income", "salary", 3000000, "1월 월급", ["fixed"]),
    ("TX-000002", "2024-01-12", "expense", "food", 8000, "김밥, 라면", ["meal", "quick"]),
    ("TX-000003", "2024-01-20", "expense", "food", 15000, "점심", ["meal"]),
    ("TX-000004", "2024-01-25", "expense", "transport", 50000, "교통카드 충전", []),
    ("TX-000005", "2024-02-01", "expense", "food", 9000, "저녁", ["meal"]),
]


def _seed(tmp: str) -> DataPaths:
    paths = DataPaths(tmp)
    ensure_files(paths)
    repository = TransactionRepository(paths.transactions)
    for row in ROWS:
        add_transaction(repository, Transaction(*row))  # type: ignore[arg-type]
    return paths


def _ids(paths: DataPaths, filters: SearchFilters) -> list[str]:
    repository = TransactionRepository(paths.transactions)
    return [tx.id for tx in newest_first(search_transactions(repository, filters))]


def test_search_conditions_are_combined_with_and() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        paths = _seed(tmp)

        assert _ids(paths, SearchFilters(date_from="2024-01-12", date_to="2024-01-20")) == [
            "TX-000003",
            "TX-000002",
        ]
        assert _ids(paths, SearchFilters(category="food", type="expense")) == [
            "TX-000005",
            "TX-000003",
            "TX-000002",
        ]
        # 메모 키워드 + 태그 동시 적용
        assert _ids(paths, SearchFilters(query="김밥", tag="quick")) == ["TX-000002"]
        assert _ids(paths, SearchFilters(query="김밥", tag="fixed")) == []


def test_search_returns_newest_first() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        paths = _seed(tmp)
        assert _ids(paths, SearchFilters())[0] == "TX-000005"


def test_summary_totals_and_top_categories() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        paths = _seed(tmp)
        summary = summarize_month(TransactionRepository(paths.transactions), "2024-01", top=2)

        assert summary.count == 4
        assert summary.total_income == 3000000
        assert summary.total_expense == 73000
        assert summary.balance == 2927000
        # 지출 합계가 큰 순서: transport 50000 > food 23000
        assert summary.top_categories == [("transport", 50000), ("food", 23000)]
        # 2월 거래는 섞이지 않는다
        assert summarize_month(
            TransactionRepository(paths.transactions), "2024-02", top=2
        ).total_expense == 9000


def test_summary_without_budget_has_no_usage() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        paths = _seed(tmp)
        summary = summarize_month(TransactionRepository(paths.transactions), "2024-01", top=3)

        # 예산이 없으면 사용률은 None 이다. 0으로 나누지 않는다.
        assert summary.budget is None
        assert summary.usage_percent is None
        assert summary.is_over_budget is False


def test_summary_with_budget_reports_usage_and_overrun() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        paths = _seed(tmp)
        repository = TransactionRepository(paths.transactions)

        within = summarize_month(repository, "2024-01", top=3, budget=100000)
        assert round(within.usage_percent or 0, 1) == 73.0
        assert within.is_over_budget is False

        over = summarize_month(repository, "2024-01", top=3, budget=50000)
        assert over.is_over_budget is True


def test_empty_month_is_not_an_error() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        paths = _seed(tmp)
        summary = summarize_month(TransactionRepository(paths.transactions), "2023-12", top=3)

        assert summary.count == 0
        assert summary.total_income == 0 and summary.total_expense == 0
        assert summary.top_categories == []


def test_budget_set_overwrites_same_month() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        paths = _seed(tmp)
        store = BudgetStore(paths.budgets)

        store.put(Budget("2024-01", 500000))
        store.put(Budget("2024-02", 450000))
        store.put(Budget("2024-01", 300000))

        assert [(b.month, b.amount) for b in store.stream()] == [
            ("2024-01", 300000),
            ("2024-02", 450000),
        ]


def test_category_add_rejects_duplicate() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        paths = _seed(tmp)
        store = CategoryStore(paths.categories)

        assert add_category(store, "cafe") == "cafe"
        assert "cafe" in store.names()
        try:
            add_category(store, "food")
        except ValidationError as error:
            assert "이미 있는 카테고리" in error.message
        else:
            raise AssertionError("중복을 막지 못했다")


def test_category_remove_blocked_while_in_use() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        paths = _seed(tmp)
        store = CategoryStore(paths.categories)
        repository = TransactionRepository(paths.transactions)

        assert count_category_usage(repository, "food") == 3
        try:
            remove_category(store, repository, "food")
        except AppError as error:
            assert "3건" in error.message, error.message
        else:
            raise AssertionError("사용 중 카테고리가 삭제됐다")
        assert "food" in store.names()

        # 쓰이지 않는 카테고리는 지워진다
        assert remove_category(store, repository, "rent") == "rent"
        assert "rent" not in store.names()


def test_category_remove_unknown_name() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        paths = _seed(tmp)
        try:
            remove_category(
                CategoryStore(paths.categories), TransactionRepository(paths.transactions), "nope"
            )
        except NotFoundError as error:
            assert "등록되지 않은" in error.message
        else:
            raise AssertionError("없는 카테고리 삭제가 통과했다")


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
