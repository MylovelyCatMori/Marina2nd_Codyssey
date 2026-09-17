"""서비스 계층. 업무 규칙을 판단하고 저장소에 일을 시킨다.

print() / input() 을 부르지 않고, 파일을 직접 열지도 않는다.
CSV에는 외래키 제약이 없으므로 "없는 id", "사용 중 카테고리" 같은 무결성 판단을
이 계층이 대신한다.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

from .errors import AppError, NotFoundError, ValidationError
from .models import INCOME, MonthlySummary, RecurringRule, SearchFilters, Transaction
from .storage import (
    CategoryStore,
    RecurringStore,
    TransactionRepository,
    read_exchange_csv,
    write_exchange_csv,
)
from .validators import (
    validate_amount,
    validate_category,
    validate_date,
    validate_tags,
    validate_type,
)

ID_PREFIX = "TX-"
ID_DIGITS = 6


@dataclass
class ImportResult:
    """가져오기 결과. 건너뛴 행은 (행 번호, 사유)로 남긴다."""

    imported: int = 0
    skipped: list[tuple[int, str]] = field(default_factory=list)

    @property
    def skipped_count(self) -> int:
        return len(self.skipped)


def next_transaction_id(repository: TransactionRepository) -> str:
    """파일 안의 가장 큰 번호 + 1. 없으면 TX-000001 부터.

    ponytail: 채번할 때마다 전체를 한 번 훑는다. 스트리밍이라 메모리는 일정하지만
    건수에 비례해 느려진다. 수만 건을 넘기면 마지막 id만 따로 보관하는 방식으로 바꾼다.
    """
    largest = 0
    for transaction in repository.stream():
        number = _parse_id(transaction.id)
        largest = max(largest, number)
    return f"{ID_PREFIX}{largest + 1:0{ID_DIGITS}d}"


def _parse_id(transaction_id: str) -> int:
    """TX-000012 -> 12. 형식이 다른 id는 채번 대상에서 제외한다(0으로 본다)."""
    if not transaction_id.startswith(ID_PREFIX):
        return 0
    tail = transaction_id[len(ID_PREFIX) :]
    return int(tail) if tail.isascii() and tail.isdigit() else 0


def add_transaction(repository: TransactionRepository, transaction: Transaction) -> Transaction:
    """거래를 추가한다. 덧붙이기라 기존 내용은 다시 쓰지 않는다."""
    repository.append(transaction)
    return transaction


def delete_transaction(repository: TransactionRepository, transaction_id: str) -> Transaction:
    """거래를 삭제하고 삭제된 거래를 돌려준다. 없으면 NotFoundError."""
    target = _require(repository, transaction_id)
    repository.rewrite(tx for tx in repository.stream() if tx.id != transaction_id)
    return target


def update_transaction(repository: TransactionRepository, updated: Transaction) -> Transaction:
    """거래를 수정한다. 없으면 NotFoundError."""
    _require(repository, updated.id)
    repository.rewrite(updated if tx.id == updated.id else tx for tx in repository.stream())
    return updated


def matches(transaction: Transaction, filters: SearchFilters) -> bool:
    """거래 한 건이 모든 조건을 만족하는가 (조건들은 AND).

    날짜는 YYYY-MM-DD 라 문자열 비교가 그대로 시간 비교가 된다.
    """
    if filters.date_from and transaction.date < filters.date_from:
        return False
    if filters.date_to and transaction.date > filters.date_to:
        return False
    if filters.category and transaction.category != filters.category:
        return False
    if filters.type and transaction.type != filters.type:
        return False
    if filters.query and filters.query.lower() not in transaction.memo.lower():
        return False
    if filters.tag and filters.tag not in transaction.tags:
        return False
    return True


def search_transactions(
    repository: TransactionRepository, filters: SearchFilters
) -> Iterator[Transaction]:
    """조건에 맞는 거래만 흘려보낸다. 걸러내기를 제너레이터 안에서 한다.

    파일 전체를 목록으로 만든 뒤 거르면 메모리에 전부 올라간다.
    여기서 거르면 조건에 맞는 것만 밖으로 나간다.
    """
    for transaction in repository.stream():
        if matches(transaction, filters):
            yield transaction


def newest_first(transactions: Iterator[Transaction]) -> list[Transaction]:
    """최신순 정렬. 정렬은 걸러낸 결과에만 적용한다."""
    return sorted(transactions, key=lambda tx: (tx.date, tx.id), reverse=True)


def summarize_month(
    repository: TransactionRepository, month: str, top: int, budget: int | None = None
) -> MonthlySummary:
    """한 달치를 집계한다. 파일은 한 번만 훑는다."""
    filters = SearchFilters(date_from=f"{month}-01", date_to=f"{month}-31")
    total_income = 0
    total_expense = 0
    count = 0
    expense_by_category: Counter[str] = Counter()

    for transaction in search_transactions(repository, filters):
        count += 1
        if transaction.type == INCOME:
            total_income += transaction.amount
        else:
            total_expense += transaction.amount
            expense_by_category[transaction.category] += transaction.amount

    return MonthlySummary(
        month=month,
        count=count,
        total_income=total_income,
        total_expense=total_expense,
        top_categories=expense_by_category.most_common(top),
        budget=budget,
    )


def add_category(store: CategoryStore, name: str) -> str:
    """카테고리를 추가한다. 이미 있으면 오류."""
    if name in store.names():
        raise ValidationError(f"이미 있는 카테고리입니다: {name}", "category list 로 목록을 확인하세요")
    store.append(name)
    return name


def count_category_usage(repository: TransactionRepository, name: str) -> int:
    """해당 카테고리를 쓰는 거래 건수."""
    return sum(1 for transaction in repository.stream() if transaction.category == name)


def remove_category(store: CategoryStore, repository: TransactionRepository, name: str) -> str:
    """카테고리를 삭제한다. 쓰는 거래가 한 건이라도 있으면 막는다.

    CSV에는 외래키 제약이 없다. 이 확인이 없으면 목록에 없는 카테고리를 가진
    거래가 파일에 남는다.
    """
    names = store.names()
    if name not in names:
        raise NotFoundError(
            f"등록되지 않은 카테고리입니다: {name}", f"사용 가능: {', '.join(names)}"
        )

    used = count_category_usage(repository, name)
    if used:
        raise AppError(
            f"'{name}'를 사용하는 거래가 {used}건 있습니다.",
            "해당 거래를 먼저 수정하거나 삭제하세요",
        )

    store.rewrite(item for item in names if item != name)
    return name


def export_transactions(
    repository: TransactionRepository, filters: SearchFilters, out_path: Path
) -> int:
    """조건에 맞는 거래를 교환용 CSV로 내보낸다. 건수를 돌려준다."""
    return write_exchange_csv(out_path, search_transactions(repository, filters))


def import_transactions(
    repository: TransactionRepository, store: CategoryStore, source: Path
) -> ImportResult:
    """CSV에서 거래를 가져온다. 잘못된 행은 건너뛰고 사유를 남긴다.

    한 행이 틀렸다고 전체를 버리면 사용자가 손으로 고칠 곳을 알 수 없다.
    행 단위로 판정하고 결과를 함께 알려 준다.

    ponytail: 중복 판단은 하지 않는다. 같은 파일을 두 번 가져오면 두 번 들어간다.
    중복을 막아야 하면 (date, type, category, amount, memo) 조합으로 거르면 된다.
    """
    if not source.exists():
        raise NotFoundError(f"파일을 찾을 수 없습니다: {source}", "경로를 다시 확인하세요")

    known = store.names()
    result = ImportResult()
    next_number = _parse_id(next_transaction_id(repository))

    for line_number, row in read_exchange_csv(source):
        try:
            transaction = _row_to_transaction(row, known, next_number)
        except ValidationError as error:
            result.skipped.append((line_number, error.message))
            continue

        repository.append(transaction)
        result.imported += 1
        next_number += 1

    return result


def _row_to_transaction(row: dict[str, str], known: list[str], number: int) -> Transaction:
    """CSV 한 행을 거래로 바꾼다. 검증은 대화형 입력과 같은 규칙을 쓴다."""
    return Transaction(
        id=f"{ID_PREFIX}{number:0{ID_DIGITS}d}",
        date=validate_date(row.get("date") or ""),
        type=validate_type(row.get("type") or ""),
        category=validate_category(row.get("category") or "", known),
        amount=validate_amount(row.get("amount") or ""),
        memo=(row.get("memo") or "").strip(),
        tags=validate_tags(row.get("tags") or ""),
    )


RECURRING_PREFIX = "RC-"
RECURRING_DIGITS = 4


def _recurring_marker(rule_id: str) -> str:
    """반복으로 생성된 거래임을 메모에 남길 표시.

    별도 열을 만들지 않는다. 생성된 거래는 일반 거래와 똑같이 다뤄야 하고,
    같은 달에 두 번 만들지 않았는지 확인할 단서만 있으면 된다.
    """
    return f"[반복 {rule_id}]"


def next_recurring_id(store: RecurringStore) -> str:
    largest = 0
    for rule in store.stream():
        tail = rule.id[len(RECURRING_PREFIX) :]
        if rule.id.startswith(RECURRING_PREFIX) and tail.isascii() and tail.isdigit():
            largest = max(largest, int(tail))
    return f"{RECURRING_PREFIX}{largest + 1:0{RECURRING_DIGITS}d}"


def add_recurring_rule(store: RecurringStore, rule: RecurringRule) -> RecurringRule:
    store.append(rule)
    return rule


def remove_recurring_rule(store: RecurringStore, rule_id: str) -> RecurringRule:
    """반복 규칙을 지운다. 이미 생성된 거래는 건드리지 않는다."""
    target = next((rule for rule in store.stream() if rule.id == rule_id), None)
    if target is None:
        raise NotFoundError(
            f"해당 id의 반복 규칙을 찾을 수 없습니다: {rule_id}",
            "recurring list 명령으로 id를 확인하세요",
        )
    store.rewrite(rule for rule in store.stream() if rule.id != rule_id)
    return target


def apply_recurring(
    repository: TransactionRepository, store: RecurringStore, month: str
) -> tuple[list[Transaction], list[str]]:
    """규칙대로 해당 월 거래를 만든다. 이미 만든 규칙은 건너뛴다.

    같은 달에 두 번 실행해도 거래가 두 배가 되지 않아야 한다.
    """
    month_filter = SearchFilters(date_from=f"{month}-01", date_to=f"{month}-31")
    existing_memos = [tx.memo for tx in search_transactions(repository, month_filter)]

    created: list[Transaction] = []
    already: list[str] = []
    next_number = _parse_id(next_transaction_id(repository))

    for rule in store.stream():
        marker = _recurring_marker(rule.id)
        if any(marker in memo for memo in existing_memos):
            already.append(rule.id)
            continue

        transaction = Transaction(
            id=f"{ID_PREFIX}{next_number:0{ID_DIGITS}d}",
            date=f"{month}-{rule.day:02d}",
            type=rule.type,
            category=rule.category,
            amount=rule.amount,
            memo=f"{marker} {rule.memo}".strip(),
        )
        repository.append(transaction)
        created.append(transaction)
        next_number += 1

    return created, already


def _require(repository: TransactionRepository, transaction_id: str) -> Transaction:
    """있어야 하는 거래를 찾는다. 파일을 고치기 전에 먼저 확인한다."""
    found = repository.find(transaction_id)
    if found is None:
        raise NotFoundError(
            f"해당 id의 거래를 찾을 수 없습니다: {transaction_id}",
            "list 명령으로 id를 확인하세요",
        )
    return found
