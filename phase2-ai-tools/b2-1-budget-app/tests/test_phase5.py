"""Phase 5 자체 점검 (보너스). 실행: python tests/test_phase5.py"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from budget_app.errors import NotFoundError, ValidationError  # noqa: E402
from budget_app.models import RecurringRule  # noqa: E402
from budget_app.services import (  # noqa: E402
    add_recurring_rule,
    apply_recurring,
    next_recurring_id,
    remove_recurring_rule,
    summarize_month,
)
from budget_app.storage import (  # noqa: E402
    DataPaths,
    RecurringStore,
    TransactionRepository,
    copy_to_backup,
    ensure_files,
)
from budget_app.validators import validate_day  # noqa: E402


def _paths(tmp: str) -> DataPaths:
    paths = DataPaths(tmp)
    ensure_files(paths)
    return paths


def _rule(store: RecurringStore, day: int, amount: int, memo: str, type_: str) -> RecurringRule:
    return add_recurring_rule(
        store,
        RecurringRule(
            id=next_recurring_id(store),
            day=day,
            type=type_,
            category="salary" if type_ == "income" else "rent",
            amount=amount,
            memo=memo,
        ),
    )


def test_day_is_limited_to_1_through_28() -> None:
    assert validate_day("1") == 1
    assert validate_day(28) == 28
    for bad in ("0", "29", "31", "-1", "말일", "２"):
        try:
            validate_day(bad)
        except ValidationError as error:
            assert error.hint
        else:
            raise AssertionError(f"통과하면 안 되는 값: {bad}")


def test_recurring_ids_increase() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        store = RecurringStore(_paths(tmp).recurring)
        assert next_recurring_id(store) == "RC-0001"
        _rule(store, 25, 3000000, "월급", "income")
        assert next_recurring_id(store) == "RC-0002"


def test_apply_creates_transactions_for_the_month() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        paths = _paths(tmp)
        store = RecurringStore(paths.recurring)
        repository = TransactionRepository(paths.transactions)
        _rule(store, 25, 3000000, "월급", "income")
        _rule(store, 1, 500000, "월세", "expense")

        created, already = apply_recurring(repository, store, "2024-02")

        assert len(created) == 2 and already == []
        dates = sorted(tx.date for tx in created)
        assert dates == ["2024-02-01", "2024-02-25"]
        summary = summarize_month(repository, "2024-02", top=3)
        assert summary.total_income == 3000000
        assert summary.total_expense == 500000


def test_apply_twice_does_not_duplicate() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        paths = _paths(tmp)
        store = RecurringStore(paths.recurring)
        repository = TransactionRepository(paths.transactions)
        _rule(store, 25, 3000000, "월급", "income")

        apply_recurring(repository, store, "2024-02")
        created, already = apply_recurring(repository, store, "2024-02")

        assert created == [] and already == ["RC-0001"]
        assert sum(1 for _ in repository.stream()) == 1
        # 다른 달은 그대로 생성된다
        again, _ = apply_recurring(repository, store, "2024-03")
        assert len(again) == 1


def test_day_28_works_in_february() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        paths = _paths(tmp)
        store = RecurringStore(paths.recurring)
        repository = TransactionRepository(paths.transactions)
        _rule(store, 28, 100000, "구독료", "expense")

        created, _ = apply_recurring(repository, store, "2023-02")  # 평년 2월
        assert [tx.date for tx in created] == ["2023-02-28"]


def test_remove_rule_keeps_generated_transactions() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        paths = _paths(tmp)
        store = RecurringStore(paths.recurring)
        repository = TransactionRepository(paths.transactions)
        _rule(store, 25, 3000000, "월급", "income")
        apply_recurring(repository, store, "2024-02")

        removed = remove_recurring_rule(store, "RC-0001")
        assert removed.id == "RC-0001"
        assert list(store.stream()) == []
        # 이미 만들어진 거래는 남는다
        assert sum(1 for _ in repository.stream()) == 1

        try:
            remove_recurring_rule(store, "RC-0001")
        except NotFoundError as error:
            assert "찾을 수 없습니다" in error.message
        else:
            raise AssertionError("없는 규칙 삭제가 통과했다")


def test_backup_copies_files_with_timestamp() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        paths = _paths(tmp)
        copied = copy_to_backup(paths, "20260917-153000")

        names = sorted(path.name for path in copied)
        assert names == [
            "budgets-20260917-153000.csv",
            "categories-20260917-153000.csv",
            "recurring-20260917-153000.csv",
            "transactions-20260917-153000.csv",
        ]
        # 원본은 그대로 있다
        assert paths.transactions.exists()
        assert copied[0].read_bytes() == paths.transactions.read_bytes()


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
