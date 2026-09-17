"""저장소 계층. 파일을 읽고 쓰는 방법만 안다.

여기서는 print() / input() 을 부르지 않는다. 화면에 무엇을 보여줄지는 CLI가 정한다.
읽기는 전부 제너레이터다. readlines() / list(reader) / f.read() 는 쓰지 않는다.
"""

from __future__ import annotations

import csv
import os
import shutil
from collections import deque
from pathlib import Path
from typing import Iterable, Iterator

from .errors import AppError
from .models import Budget, Category, RecurringRule, Transaction

TRANSACTION_HEADER: list[str] = ["id", "date", "type", "category", "amount", "memo", "tags"]
CATEGORY_HEADER: list[str] = ["name"]
BUDGET_HEADER: list[str] = ["month", "amount"]
RECURRING_HEADER: list[str] = ["id", "day", "type", "category", "amount", "memo"]

DEFAULT_CATEGORIES: tuple[str, ...] = ("food", "transport", "rent", "salary", "etc")

TAG_SEPARATOR = ","

# import / export 공용 스키마. id 는 넣지 않는다 -- 가져올 때 새로 채번한다.
EXCHANGE_HEADER: list[str] = ["date", "type", "category", "amount", "memo", "tags"]


def _read_rows(path: Path) -> Iterator[dict[str, str]]:
    """CSV를 한 줄씩 흘려보낸다. 파일이 없으면 아무것도 내보내지 않는다."""
    if not path.exists():
        return
    # newline="" 은 csv 모듈의 요구사항. 줄바꿈 처리를 csv 가 직접 한다.
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            yield row


def _create_with_header(path: Path, header: list[str], rows: list[list[str]] | None = None) -> None:
    """헤더(와 초기 행)만 있는 새 파일을 만든다. 이미 있으면 건드리지 않는다."""
    if path.exists():
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in rows or []:
            writer.writerow(row)


def _append_row(path: Path, header: list[str], row: list[str]) -> None:
    """파일 끝에 한 줄을 덧붙인다. 기존 내용은 건드리지 않는다."""
    with open(path, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(row)


def _rewrite_all(path: Path, header: list[str], rows: Iterable[list[str]]) -> None:
    """임시 파일에 전부 쓴 뒤 이름을 바꿔 원본을 갈아 끼운다 (원자적 교체).

    원본에 직접 쓰다가 중간에 죽으면 파일이 반쪽으로 남는다. os.replace 는
    성공하거나 실패하거나 둘 중 하나여서 중간 상태가 없다.
    임시 파일을 같은 폴더에 두는 이유는, 다른 디스크로 옮기면 교체가 원자적이지 않기 때문이다.
    """
    tmp = path.with_suffix(".tmp")
    with open(tmp, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
    os.replace(tmp, path)


def write_exchange_csv(path: Path, transactions: Iterable[Transaction]) -> int:
    """거래를 교환용 스키마로 내보낸다. 쓴 건수를 돌려준다.

    임시 파일에 다 쓴 뒤 교체하므로, 내보내다 실패해도 반쪽 파일이 남지 않는다.
    """
    written = 0

    def rows() -> Iterator[list[str]]:
        nonlocal written
        for transaction in transactions:
            written += 1
            yield [
                transaction.date,
                transaction.type,
                transaction.category,
                str(transaction.amount),
                transaction.memo,
                TAG_SEPARATOR.join(transaction.tags),
            ]

    path.parent.mkdir(parents=True, exist_ok=True)
    _rewrite_all(path, EXCHANGE_HEADER, rows())
    return written


def read_exchange_csv(path: Path) -> Iterator[tuple[int, dict[str, str]]]:
    """교환용 CSV를 (행 번호, 행) 으로 흘려보낸다. 행 번호는 헤더를 1로 센다.

    헤더가 스키마와 다르면 첫 줄에서 바로 멈춘다. 절반만 가져온 상태를 만들지 않는다.
    """
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing = [column for column in EXCHANGE_HEADER if column not in (reader.fieldnames or [])]
        if missing:
            raise AppError(
                "CSV 헤더가 스키마와 다릅니다.",
                f"필요한 열: {','.join(EXCHANGE_HEADER)}",
            )
        for line_number, row in enumerate(reader, start=2):
            yield line_number, row


class DataPaths:
    """저장 폴더 안의 파일 경로를 모아 둔다."""

    def __init__(self, data_dir: str | Path) -> None:
        self.root = Path(data_dir)
        self.transactions = self.root / "transactions.csv"
        self.categories = self.root / "categories.csv"
        self.budgets = self.root / "budgets.csv"
        self.recurring = self.root / "recurring.csv"      # 보너스 B-04
        self.backups = self.root / "backups"


def ensure_files(paths: DataPaths) -> list[str]:
    """없는 파일을 만든다. 새로 만든 파일 이름을 돌려준다 (안내 출력은 CLI 몫)."""
    created: list[str] = []
    paths.root.mkdir(parents=True, exist_ok=True)

    for path, header in (
        (paths.transactions, TRANSACTION_HEADER),
        (paths.budgets, BUDGET_HEADER),
        (paths.recurring, RECURRING_HEADER),
    ):
        if not path.exists():
            _create_with_header(path, header)
            created.append(path.name)

    if not paths.categories.exists():
        # 카테고리가 비어 있으면 아무 거래도 등록할 수 없으므로 기본 5종을 함께 넣는다.
        _create_with_header(
            paths.categories, CATEGORY_HEADER, [[name] for name in DEFAULT_CATEGORIES]
        )
        created.append(paths.categories.name)

    return created


class TransactionRepository:
    """거래 저장소."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def stream(self) -> Iterator[Transaction]:
        """거래를 파일에 기록된 순서대로 한 건씩 내보낸다."""
        for row in _read_rows(self.path):
            yield self._to_transaction(row)

    def latest(self, limit: int) -> list[Transaction]:
        """최신 거래를 최대 limit 건 돌려준다 (최신순).

        deque(maxlen=limit) 은 항상 마지막 limit 건만 들고 있으므로,
        파일이 아무리 커도 메모리 사용량은 limit 에만 비례한다.

        ponytail: 파일 뒤쪽 limit 건 안에서만 날짜순으로 다시 세운다.
        limit 보다 더 깊은 곳에 과거 날짜로 끼워 넣은 거래가 있으면 목록에 안 잡힌다.
        전수 정렬이 필요해지면 search 명령(Phase 3)의 기간 조건을 쓴다.
        """
        recent = deque(self.stream(), maxlen=limit)
        return sorted(recent, key=lambda tx: (tx.date, tx.id), reverse=True)

    def find(self, transaction_id: str) -> Transaction | None:
        """id로 거래 한 건을 찾는다. 없으면 None."""
        for transaction in self.stream():
            if transaction.id == transaction_id:
                return transaction
        return None

    def append(self, transaction: Transaction) -> None:
        """거래 한 건을 파일 끝에 덧붙인다."""
        _append_row(self.path, TRANSACTION_HEADER, self._to_row(transaction))

    def rewrite(self, transactions: Iterable[Transaction]) -> None:
        """전체를 새로 쓴다. 수정·삭제에 쓰이며 원자적으로 교체된다."""
        _rewrite_all(self.path, TRANSACTION_HEADER, (self._to_row(tx) for tx in transactions))

    @staticmethod
    def _to_row(transaction: Transaction) -> list[str]:
        return [
            transaction.id,
            transaction.date,
            transaction.type,
            transaction.category,
            str(transaction.amount),
            transaction.memo,
            TAG_SEPARATOR.join(transaction.tags),
        ]

    @staticmethod
    def _to_transaction(row: dict[str, str]) -> Transaction:
        raw_tags = row.get("tags") or ""
        return Transaction(
            id=row["id"],
            date=row["date"],
            type=row["type"],
            category=row["category"],
            amount=int(row["amount"]),  # 금액은 읽는 즉시 int 로 바꾼다
            memo=row.get("memo") or "",
            tags=[tag for tag in raw_tags.split(TAG_SEPARATOR) if tag],
        )


class CategoryStore:
    """카테고리 저장소."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def stream(self) -> Iterator[Category]:
        for row in _read_rows(self.path):
            yield Category(name=row["name"])

    def names(self) -> list[str]:
        """등록된 카테고리 이름 목록. 개수가 적어 전부 모아도 무방하다."""
        return [category.name for category in self.stream()]

    def append(self, name: str) -> None:
        _append_row(self.path, CATEGORY_HEADER, [name])

    def rewrite(self, names: Iterable[str]) -> None:
        _rewrite_all(self.path, CATEGORY_HEADER, ([name] for name in names))


class BudgetStore:
    """예산 저장소."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def stream(self) -> Iterator[Budget]:
        for row in _read_rows(self.path):
            yield Budget(month=row["month"], amount=int(row["amount"]))

    def get(self, month: str) -> Budget | None:
        """해당 월 예산. 없으면 None (0원이 아니다)."""
        for budget in self.stream():
            if budget.month == month:
                return budget
        return None

    def put(self, budget: Budget) -> None:
        """해당 월 예산을 저장한다. 같은 달이 이미 있으면 덮어쓴다.

        월 단위 데이터라 건수가 많아야 수십 개다. 전체를 다시 쓰는 편이
        '그 줄만 고치기'보다 단순하고, 원자적 교체 덕에 안전하다.
        """
        others = [item for item in self.stream() if item.month != budget.month]
        merged = sorted(others + [budget], key=lambda item: item.month)
        _rewrite_all(
            self.path, BUDGET_HEADER, ([item.month, str(item.amount)] for item in merged)
        )


class RecurringStore:
    """반복 규칙 저장소 (보너스 B-04)."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def stream(self) -> Iterator[RecurringRule]:
        for row in _read_rows(self.path):
            yield RecurringRule(
                id=row["id"],
                day=int(row["day"]),
                type=row["type"],
                category=row["category"],
                amount=int(row["amount"]),
                memo=row.get("memo") or "",
            )

    def append(self, rule: RecurringRule) -> None:
        _append_row(self.path, RECURRING_HEADER, self._to_row(rule))

    def rewrite(self, rules: Iterable[RecurringRule]) -> None:
        _rewrite_all(self.path, RECURRING_HEADER, (self._to_row(rule) for rule in rules))

    @staticmethod
    def _to_row(rule: RecurringRule) -> list[str]:
        return [rule.id, str(rule.day), rule.type, rule.category, str(rule.amount), rule.memo]


def copy_to_backup(paths: DataPaths, stamp: str) -> list[Path]:
    """저장 파일들을 타임스탬프가 붙은 이름으로 backups/ 에 복사한다 (보너스 B-03).

    복사본이므로 원본은 그대로다. 잘못된 일괄 수정을 되돌릴 마지막 수단이다.
    """
    paths.backups.mkdir(parents=True, exist_ok=True)
    copied: list[Path] = []
    for source in (paths.transactions, paths.categories, paths.budgets, paths.recurring):
        if not source.exists():
            continue
        target = paths.backups / f"{source.stem}-{stamp}{source.suffix}"
        shutil.copy2(source, target)   # copy2 는 수정 시각까지 함께 복사한다
        copied.append(target)
    return copied
