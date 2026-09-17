"""Phase 4 자체 점검. 실행: python tests/test_phase4.py"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from budget_app.errors import AppError, NotFoundError  # noqa: E402
from budget_app.models import SearchFilters, Transaction  # noqa: E402
from budget_app.services import (  # noqa: E402
    add_transaction,
    export_transactions,
    import_transactions,
)
from budget_app.storage import (  # noqa: E402
    CategoryStore,
    DataPaths,
    TransactionRepository,
    ensure_files,
)

ROWS = [
    ("TX-000001", "2024-01-05", "income", "salary", 3000000, "1월 월급", ["fixed"]),
    ("TX-000002", "2024-01-12", "expense", "food", 8000, "김밥, 라면", ["meal", "quick"]),
    ("TX-000003", "2024-02-01", "expense", "food", 9000, "저녁", ["meal"]),
]

GOOD_CSV = """date,type,category,amount,memo,tags
2024-03-01,expense,food,12000,"떡볶이, 순대","meal,snack"
2024-03-02,income,salary,2500000,3월 월급,
"""

MIXED_CSV = """date,type,category,amount,memo,tags
2024-03-01,expense,food,12000,정상 행,meal
2024-03-02,expense,food,만이천원,금액이 문자열,
2024-02-30,expense,food,5000,없는 날짜,
2024-03-04,expense,cafe,5000,없는 카테고리,
2024-03-05,sponsor,food,5000,잘못된 타입,
2024-03-06,expense,food,0,0원,
"""

WRONG_HEADER_CSV = """날짜,종류,분류,금액
2024-03-01,expense,food,12000
"""


def _seed(tmp: str) -> DataPaths:
    paths = DataPaths(tmp)
    ensure_files(paths)
    repository = TransactionRepository(paths.transactions)
    for row in ROWS:
        add_transaction(repository, Transaction(*row))  # type: ignore[arg-type]
    return paths


def test_export_writes_only_matching_period() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        paths = _seed(tmp)
        out = Path(tmp) / "out" / "jan.csv"

        written = export_transactions(
            TransactionRepository(paths.transactions),
            SearchFilters(date_from="2024-01-01", date_to="2024-01-31"),
            out,
        )

        assert written == 2
        lines = out.read_text(encoding="utf-8").splitlines()
        assert lines[0] == "date,type,category,amount,memo,tags"
        assert len(lines) == 3  # 헤더 + 2건
        assert "2024-02-01" not in out.read_text(encoding="utf-8")


def test_export_import_round_trip_keeps_count_and_commas() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        source_paths = _seed(tmp)
        out = Path(tmp) / "all.csv"
        export_transactions(
            TransactionRepository(source_paths.transactions),
            SearchFilters(),
            out,
        )

        with tempfile.TemporaryDirectory() as tmp2:
            target = DataPaths(tmp2)
            ensure_files(target)
            repository = TransactionRepository(target.transactions)
            result = import_transactions(repository, CategoryStore(target.categories), out)

            assert result.imported == len(ROWS)
            assert result.skipped == []
            restored = {tx.date: tx for tx in repository.stream()}
            # 쉼표가 든 메모와 태그 2개가 왕복 후에도 그대로다
            assert restored["2024-01-12"].memo == "김밥, 라면"
            assert restored["2024-01-12"].tags == ["meal", "quick"]
            assert restored["2024-01-05"].amount == 3000000
            # id 는 새로 채번된다
            assert sorted(tx.id for tx in repository.stream()) == [
                "TX-000001",
                "TX-000002",
                "TX-000003",
            ]


def test_import_continues_numbering_after_existing_rows() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        paths = _seed(tmp)
        source = Path(tmp) / "more.csv"
        source.write_text(GOOD_CSV, encoding="utf-8")

        repository = TransactionRepository(paths.transactions)
        result = import_transactions(repository, CategoryStore(paths.categories), source)

        assert result.imported == 2
        assert [tx.id for tx in repository.stream()][-2:] == ["TX-000004", "TX-000005"]


def test_import_skips_bad_rows_with_reasons() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        paths = _seed(tmp)
        source = Path(tmp) / "mixed.csv"
        source.write_text(MIXED_CSV, encoding="utf-8")

        repository = TransactionRepository(paths.transactions)
        result = import_transactions(repository, CategoryStore(paths.categories), source)

        assert result.imported == 1
        assert result.skipped_count == 5
        # 행 번호는 파일에서 보이는 줄 번호와 같다 (헤더가 1번)
        assert [line for line, _ in result.skipped] == [3, 4, 5, 6, 7]
        reasons = dict(result.skipped)
        assert "금액은 1 이상" in reasons[3]
        assert "존재하지 않는 날짜" in reasons[4]
        assert "등록되지 않은 카테고리" in reasons[5]
        assert "income 또는 expense" in reasons[6]
        assert "금액은 1 이상" in reasons[7]
        # 건너뛴 행은 저장되지 않았다
        assert sum(1 for _ in repository.stream()) == len(ROWS) + 1


def test_import_rejects_wrong_header_before_writing() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        paths = _seed(tmp)
        source = Path(tmp) / "wrong.csv"
        source.write_text(WRONG_HEADER_CSV, encoding="utf-8")
        repository = TransactionRepository(paths.transactions)
        before = repository.path.read_bytes()

        try:
            import_transactions(repository, CategoryStore(paths.categories), source)
        except AppError as error:
            assert "CSV 헤더" in error.message
            assert "date,type,category,amount,memo,tags" in error.hint
        else:
            raise AssertionError("헤더 불일치를 막지 못했다")

        assert repository.path.read_bytes() == before


def test_import_missing_file_is_user_error() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        paths = _seed(tmp)
        try:
            import_transactions(
                TransactionRepository(paths.transactions),
                CategoryStore(paths.categories),
                Path(tmp) / "nope.csv",
            )
        except NotFoundError as error:
            assert "찾을 수 없습니다" in error.message
        else:
            raise AssertionError("없는 파일이 통과했다")


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
