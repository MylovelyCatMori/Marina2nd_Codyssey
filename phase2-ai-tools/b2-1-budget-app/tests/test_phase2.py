"""Phase 2 자체 점검. 실행: python tests/test_phase2.py"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from budget_app import exit_codes  # noqa: E402
from budget_app.decorators import handle_errors  # noqa: E402
from budget_app.errors import NotFoundError, ValidationError  # noqa: E402
from budget_app.models import Transaction  # noqa: E402
from budget_app.services import (  # noqa: E402
    add_transaction,
    delete_transaction,
    next_transaction_id,
    update_transaction,
)
from budget_app.storage import DataPaths, TransactionRepository, ensure_files  # noqa: E402
from budget_app.validators import (  # noqa: E402
    validate_amount,
    validate_category,
    validate_date,
    validate_tags,
    validate_type,
)


def _repository(tmp: str) -> TransactionRepository:
    paths = DataPaths(tmp)
    ensure_files(paths)
    return TransactionRepository(paths.transactions)


def _sample(transaction_id: str = "TX-000001", **overrides: object) -> Transaction:
    fields: dict[str, object] = {
        "date": "2024-01-15",
        "type": "expense",
        "category": "food",
        "amount": 15000,
        "memo": "점심, 김밥",
        "tags": ["meal"],
    }
    fields.update(overrides)
    return Transaction(id=transaction_id, **fields)  # type: ignore[arg-type]


def _expect_validation_error(call, expected: str) -> None:
    try:
        call()
    except ValidationError as error:
        assert expected in error.message, error.message
        assert error.hint, "힌트가 비어 있다"
        return
    raise AssertionError(f"ValidationError 가 나지 않았다: {expected}")


def test_date_format_and_calendar_are_separate_errors() -> None:
    assert validate_date(" 2024-01-15 ") == "2024-01-15"
    _expect_validation_error(lambda: validate_date("2024/01/15"), "날짜 형식")
    _expect_validation_error(lambda: validate_date("2024-01-15x"), "날짜 형식")
    # 달력에 없는 날짜는 형식이 아니라 값이 틀린 것이다
    _expect_validation_error(lambda: validate_date("2024-02-30"), "존재하지 않는 날짜")
    assert validate_date("2024-02-29") == "2024-02-29"  # 2024년은 윤년


def test_amount_rejects_zero_negative_and_non_digits() -> None:
    assert validate_amount("15000") == 15000
    for bad in ("0", "-1", "15,000", "만원", "１２３"):
        _expect_validation_error(lambda bad=bad: validate_amount(bad), "금액은 1 이상")


def test_type_and_category_are_checked_against_known_values() -> None:
    assert validate_type("INCOME") == "income"
    _expect_validation_error(lambda: validate_type("소득"), "income 또는 expense")
    assert validate_category("food", ["food", "etc"]) == "food"
    _expect_validation_error(
        lambda: validate_category("cafe", ["food", "etc"]), "등록되지 않은 카테고리"
    )


def test_tags_split_and_trim() -> None:
    assert validate_tags(" meal , quick ,, ") == ["meal", "quick"]
    assert validate_tags("") == []


def test_id_numbering_starts_at_one_and_continues() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        repository = _repository(tmp)
        assert next_transaction_id(repository) == "TX-000001"

        add_transaction(repository, _sample("TX-000001"))
        add_transaction(repository, _sample("TX-000009"))
        assert next_transaction_id(repository) == "TX-000010"


def test_memo_with_comma_survives_write_and_read() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        repository = _repository(tmp)
        add_transaction(repository, _sample(memo="김밥, 라면", tags=["meal", "quick"]))

        saved = repository.find("TX-000001")
        assert saved is not None
        assert saved.memo == "김밥, 라면"
        assert saved.tags == ["meal", "quick"]


def test_delete_removes_only_the_target() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        repository = _repository(tmp)
        add_transaction(repository, _sample("TX-000001"))
        add_transaction(repository, _sample("TX-000002"))

        removed = delete_transaction(repository, "TX-000001")
        assert removed.id == "TX-000001"
        assert [tx.id for tx in repository.stream()] == ["TX-000002"]


def test_missing_id_raises_and_leaves_file_untouched() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        repository = _repository(tmp)
        add_transaction(repository, _sample("TX-000001"))
        before = repository.path.read_bytes()

        for call in (
            lambda: delete_transaction(repository, "NOPE"),
            lambda: update_transaction(repository, _sample("NOPE")),
        ):
            try:
                call()
            except NotFoundError as error:
                assert "찾을 수 없습니다" in error.message
            else:
                raise AssertionError("NotFoundError 가 나지 않았다")

        assert repository.path.read_bytes() == before


def test_update_replaces_fields_and_keeps_others() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        repository = _repository(tmp)
        add_transaction(repository, _sample("TX-000001"))
        add_transaction(repository, _sample("TX-000002", category="etc"))

        update_transaction(repository, _sample("TX-000001", amount=99000))
        rows = {tx.id: tx for tx in repository.stream()}
        assert rows["TX-000001"].amount == 99000
        assert rows["TX-000002"].category == "etc"


def test_rewrite_leaves_no_temp_file() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        repository = _repository(tmp)
        add_transaction(repository, _sample("TX-000001"))
        delete_transaction(repository, "TX-000001")

        assert list(Path(tmp).glob("*.tmp")) == []


def test_handle_errors_maps_exceptions_to_exit_codes() -> None:
    @handle_errors
    def raise_validation() -> int:
        raise ValidationError("잘못된 값입니다.", "다시 입력하세요")

    @handle_errors
    def raise_os() -> int:
        raise OSError(13, "Permission denied", "data/transactions.csv")

    @handle_errors
    def succeed() -> int:
        return exit_codes.OK

    assert raise_validation() == exit_codes.USER_ERROR
    assert raise_os() == exit_codes.SYSTEM_ERROR
    assert succeed() == exit_codes.OK
    # functools.wraps 로 원본 이름이 보존되는지
    assert succeed.__name__ == "succeed"


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
