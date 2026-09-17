"""CLI 계층. 인자 파싱과 명령 분기, 그리고 화면 입출력만 담당한다.

파일 접근은 저장소가, 규칙 판단은 서비스가 한다. (계층 경계: PRD/04_PROJECT_SPEC.md)
명령 12개: add / list / update / delete / search / summary / budget / category /
export / import / backup / recurring
"""

from __future__ import annotations

import argparse
import logging
import sys
from dataclasses import replace
from datetime import datetime
from pathlib import Path
from typing import Callable, Sequence

from . import exit_codes
from .decorators import handle_errors, log_call, measure_time
from .errors import ValidationError
from .formatter import format_amount, format_summary, format_table, format_transactions
from .models import Budget, RecurringRule, SearchFilters, Transaction
from .services import (
    add_category,
    add_recurring_rule,
    add_transaction,
    count_category_usage,
    delete_transaction,
    export_transactions,
    import_transactions,
    apply_recurring,
    newest_first,
    next_recurring_id,
    next_transaction_id,
    remove_category,
    remove_recurring_rule,
    search_transactions,
    summarize_month,
    update_transaction,
)
from .storage import (
    BudgetStore,
    CategoryStore,
    DataPaths,
    RecurringStore,
    TransactionRepository,
    copy_to_backup,
    ensure_files,
)
from .validators import (
    validate_amount,
    validate_category,
    validate_date,
    validate_day,
    validate_month,
    validate_tags,
    validate_type,
)

DEFAULT_DATA_DIR = "./data"
DEFAULT_LIST_LIMIT = 20

DEFAULT_TOP = 5


def build_parser() -> argparse.ArgumentParser:
    """최상위 파서와 서브커맨드 10개를 만든다."""
    parser = argparse.ArgumentParser(
        prog="python -m budget_app",
        description="나만의 용돈 기입장 -- 표준 라이브러리만 사용하는 콘솔 가계부",
    )
    # 전역 옵션. 옵션 표기는 '--'로 통일한다. (C-05)
    parser.add_argument(
        "--data-dir",
        default=DEFAULT_DATA_DIR,
        metavar="PATH",
        help=f"저장 폴더 경로 (기본값: {DEFAULT_DATA_DIR})",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="실행 로그와 소요 시간을 함께 출력",
    )

    subparsers = parser.add_subparsers(dest="command", metavar="<command>")

    add_help = "거래 추가 (대화형 입력)"
    subparsers.add_parser("add", help=add_help, description=add_help)

    list_help = "최근 거래 목록 출력"
    list_parser = subparsers.add_parser("list", help=list_help, description=list_help)
    list_parser.add_argument(
        "--limit",
        type=int,
        default=DEFAULT_LIST_LIMIT,
        metavar="N",
        help=f"출력할 건수 (기본값: {DEFAULT_LIST_LIMIT})",
    )

    update_help = "거래 수정 (--id 지정 후 대화형 입력)"
    update_parser = subparsers.add_parser("update", help=update_help, description=update_help)
    update_parser.add_argument("--id", required=True, metavar="ID", help="수정할 거래 id")

    delete_help = "거래 삭제"
    delete_parser = subparsers.add_parser("delete", help=delete_help, description=delete_help)
    delete_parser.add_argument("--id", required=True, metavar="ID", help="삭제할 거래 id")

    search_help = "조건으로 거래 검색 (조건은 AND로 묶인다)"
    search_parser = subparsers.add_parser("search", help=search_help, description=search_help)
    search_parser.add_argument("--from", dest="date_from", metavar="YYYY-MM-DD", help="시작 날짜")
    search_parser.add_argument("--to", dest="date_to", metavar="YYYY-MM-DD", help="끝 날짜")
    search_parser.add_argument("--category", metavar="NAME", help="카테고리")
    search_parser.add_argument("--type", metavar="income|expense", help="수입/지출")
    search_parser.add_argument("--q", dest="query", metavar="TEXT", help="메모 키워드")
    search_parser.add_argument("--tag", metavar="TAG", help="태그")

    summary_help = "월별 수입·지출·예산 요약"
    summary_parser = subparsers.add_parser("summary", help=summary_help, description=summary_help)
    summary_parser.add_argument("--month", required=True, metavar="YYYY-MM", help="집계할 달")
    summary_parser.add_argument(
        "--top", type=int, default=DEFAULT_TOP, metavar="N",
        help=f"카테고리별 지출 상위 N개 (기본값: {DEFAULT_TOP})",
    )

    budget_help = "월 예산 설정"
    budget_parser = subparsers.add_parser("budget", help=budget_help, description=budget_help)
    budget_sub = budget_parser.add_subparsers(dest="subcommand", metavar="<subcommand>")
    budget_set = budget_sub.add_parser("set", help="월 예산 저장 (같은 달은 덮어쓴다)")
    budget_set.add_argument("--month", required=True, metavar="YYYY-MM", help="대상 달")
    budget_set.add_argument("--amount", required=True, metavar="원", help="예산 금액 (1 이상)")

    category_help = "카테고리 추가·목록·삭제"
    category_parser = subparsers.add_parser(
        "category", help=category_help, description=category_help
    )
    category_sub = category_parser.add_subparsers(dest="subcommand", metavar="<subcommand>")
    category_add = category_sub.add_parser("add", help="카테고리 추가")
    category_add.add_argument("--name", required=True, metavar="NAME", help="추가할 이름")
    category_sub.add_parser("list", help="카테고리 목록")
    category_remove = category_sub.add_parser("remove", help="카테고리 삭제 (사용 중이면 차단)")
    category_remove.add_argument("--name", required=True, metavar="NAME", help="삭제할 이름")

    export_help = "기간 거래를 CSV로 내보내기 (기간 조건 필수)"
    export_parser = subparsers.add_parser("export", help=export_help, description=export_help)
    export_parser.add_argument("--out", required=True, metavar="FILE", help="내보낼 CSV 경로")
    export_parser.add_argument("--month", metavar="YYYY-MM", help="대상 달")
    export_parser.add_argument("--from", dest="date_from", metavar="YYYY-MM-DD", help="시작 날짜")
    export_parser.add_argument("--to", dest="date_to", metavar="YYYY-MM-DD", help="끝 날짜")

    import_help = "CSV에서 거래 가져오기 (잘못된 행은 건너뛴다)"
    import_parser = subparsers.add_parser("import", help=import_help, description=import_help)
    import_parser.add_argument(
        "--from", dest="source", required=True, metavar="FILE", help="가져올 CSV 경로"
    )

    backup_help = "저장 파일을 타임스탬프 붙은 이름으로 복사 (보너스)"
    subparsers.add_parser("backup", help=backup_help, description=backup_help)

    recurring_help = "반복 내역 규칙 관리 (보너스)"
    recurring_parser = subparsers.add_parser(
        "recurring", help=recurring_help, description=recurring_help
    )
    recurring_sub = recurring_parser.add_subparsers(dest="subcommand", metavar="<subcommand>")
    recurring_add = recurring_sub.add_parser("add", help="반복 규칙 추가")
    recurring_add.add_argument("--day", required=True, metavar="1-28", help="매월 며칠")
    recurring_add.add_argument("--type", required=True, metavar="income|expense", help="수입/지출")
    recurring_add.add_argument("--category", required=True, metavar="NAME", help="카테고리")
    recurring_add.add_argument("--amount", required=True, metavar="원", help="금액 (1 이상)")
    recurring_add.add_argument("--memo", default="", metavar="TEXT", help="메모 (선택)")
    recurring_sub.add_parser("list", help="반복 규칙 목록")
    recurring_remove = recurring_sub.add_parser("remove", help="반복 규칙 삭제")
    recurring_remove.add_argument("--id", required=True, metavar="ID", help="삭제할 규칙 id")
    recurring_apply = recurring_sub.add_parser("apply", help="해당 월 거래 생성")
    recurring_apply.add_argument("--month", required=True, metavar="YYYY-MM", help="대상 달")
    return parser


# --------------------------------------------------------------------------- 입력 보조


def prompt_until_valid(label: str, convert: Callable[[str], object], default: object = None) -> object:
    """올바른 값이 들어올 때까지 다시 묻는다.

    검증 실패를 예외로 올리고 여기서 한 번만 받아내므로,
    필드마다 같은 모양의 try/except 를 반복하지 않는다.
    """
    while True:
        raw = input(f"{label}: ")
        if not raw.strip() and default is not None:
            return default
        try:
            return convert(raw)
        except ValidationError as error:
            print(f"[오류] {error.message}")
            if error.hint:
                print(f"[힌트] {error.hint}")


EDITABLE_FIELDS: tuple[str, ...] = ("date", "type", "category", "amount", "memo", "tags")


def _ask_field(name: str, known_categories: list[str]) -> object:
    """필드 하나를 올바른 값이 들어올 때까지 입력받는다."""
    if name == "date":
        return prompt_until_valid("날짜 (YYYY-MM-DD)", validate_date)
    if name == "type":
        return prompt_until_valid("타입 (income/expense)", validate_type)
    if name == "category":
        return prompt_until_valid(
            f"카테고리 [{', '.join(known_categories)}]",
            lambda raw: validate_category(raw, known_categories),
        )
    if name == "amount":
        return prompt_until_valid("금액 (원)", validate_amount)
    if name == "memo":
        return input("메모 (선택, 엔터로 건너뜀): ").strip()
    return validate_tags(input("태그 (쉼표 구분, 선택): "))


def _input_all_fields(known_categories: list[str]) -> dict[str, object]:
    """새 거래의 모든 필드를 순서대로 입력받는다."""
    return {name: _ask_field(name, known_categories) for name in EDITABLE_FIELDS}


# --------------------------------------------------------------------------- 명령 실행


@handle_errors
@log_call
@measure_time
def run_add(paths: DataPaths) -> int:
    """거래를 대화형으로 입력받아 저장한다."""
    repository = TransactionRepository(paths.transactions)
    categories = CategoryStore(paths.categories).names()

    fields = _input_all_fields(categories)
    transaction = Transaction(id=next_transaction_id(repository), **fields)  # type: ignore[arg-type]
    add_transaction(repository, transaction)

    print(f"\n저장했습니다. id: {transaction.id}")
    print(f"{transaction.date} {transaction.type} {transaction.category} "
          f"{format_amount(transaction.amount)}원")
    return exit_codes.OK


@handle_errors
@log_call
@measure_time
def run_list(paths: DataPaths, limit: int) -> int:
    """최신 거래를 limit 건 출력한다."""
    if limit < 1:
        raise ValidationError("--limit 은 1 이상이어야 합니다.", "예: --limit 5")

    transactions = TransactionRepository(paths.transactions).latest(limit)
    if not transactions:
        # 거래 0건은 오류가 아니다. 정상 종료한다.
        print("데이터 없음. 등록된 거래가 없습니다.")
        return exit_codes.OK

    print(format_transactions(transactions))
    print(f"\n총 {len(transactions)}건 (최신순, 최대 {limit}건)")
    return exit_codes.OK


@handle_errors
@log_call
@measure_time
def run_update(paths: DataPaths, transaction_id: str) -> int:
    """거래를 대화형으로 수정한다. 현재 값을 보여 주고 빈 입력은 유지로 본다."""
    repository = TransactionRepository(paths.transactions)
    current = repository.find(transaction_id)
    if current is None:
        raise ValidationError(
            f"해당 id의 거래를 찾을 수 없습니다: {transaction_id}",
            "list 명령으로 id를 확인하세요",
        )

    categories = CategoryStore(paths.categories).names()
    updated = replace(current)  # 원본을 그대로 두고 사본을 고친다
    changed = False

    while True:
        print(format_transactions([updated]))
        print("\n수정할 항목 번호를 고르세요.")
        for number, name in enumerate(EDITABLE_FIELDS, start=1):
            print(f"  {number}. {name} = {getattr(updated, name)}")
        print("  0. 수정 마치기")

        choice = input("번호: ").strip()
        if choice == "0":
            break
        if not (choice.isascii() and choice.isdigit()) or not 1 <= int(choice) <= len(EDITABLE_FIELDS):
            print(f"[오류] 0부터 {len(EDITABLE_FIELDS)} 사이의 번호를 입력하세요.")
            print(f"[힌트] 입력값: {choice}")
            continue

        name = EDITABLE_FIELDS[int(choice) - 1]
        setattr(updated, name, _ask_field(name, categories))
        changed = True
        print()

    if not changed:
        # 고친 것이 없으면 파일을 다시 쓰지 않는다.
        print("변경한 내용이 없습니다.")
        return exit_codes.OK

    update_transaction(repository, updated)
    print(f"\n수정했습니다. id: {updated.id}")
    print(format_transactions([updated]))
    return exit_codes.OK


@handle_errors
@log_call
@measure_time
def run_search(paths: DataPaths, args: argparse.Namespace) -> int:
    """조건에 맞는 거래를 최신순으로 출력한다."""
    known = CategoryStore(paths.categories).names()
    filters = SearchFilters(
        date_from=validate_date(args.date_from) if args.date_from else None,
        date_to=validate_date(args.date_to) if args.date_to else None,
        category=validate_category(args.category, known) if args.category else None,
        type=validate_type(args.type) if args.type else None,
        query=args.query,
        tag=args.tag,
    )

    repository = TransactionRepository(paths.transactions)
    found = newest_first(search_transactions(repository, filters))
    if not found:
        print("데이터 없음. 조건에 맞는 거래가 없습니다.")
        return exit_codes.OK

    print(format_transactions(found))
    print(f"\n총 {len(found)}건 (최신순)")
    return exit_codes.OK


@handle_errors
@log_call
@measure_time
def run_summary(paths: DataPaths, month: str, top: int) -> int:
    """한 달 수입·지출·잔액과 카테고리별 지출 TOP N을 출력한다."""
    if top < 1:
        raise ValidationError("--top 은 1 이상이어야 합니다.", "예: --top 3")

    target_month = validate_month(month)
    budget = BudgetStore(paths.budgets).get(target_month)
    summary = summarize_month(
        TransactionRepository(paths.transactions),
        target_month,
        top,
        budget.amount if budget else None,
    )

    if summary.count == 0:
        print(f"데이터 없음. {target_month} 에 등록된 거래가 없습니다.")
        return exit_codes.OK

    print(format_summary(summary))
    return exit_codes.OK


@handle_errors
@log_call
@measure_time
def run_budget_set(paths: DataPaths, month: str, amount: str) -> int:
    """월 예산을 저장한다. 같은 달이 있으면 덮어쓴다."""
    budget = Budget(month=validate_month(month), amount=validate_amount(amount))
    BudgetStore(paths.budgets).put(budget)
    print(f"{budget.month} 예산을 {format_amount(budget.amount)}원으로 설정했습니다.")
    return exit_codes.OK


@handle_errors
@log_call
@measure_time
def run_category(paths: DataPaths, args: argparse.Namespace) -> int:
    """카테고리를 추가·조회·삭제한다."""
    store = CategoryStore(paths.categories)
    repository = TransactionRepository(paths.transactions)

    if args.subcommand == "add":
        name = add_category(store, args.name.strip())
        print(f"카테고리를 추가했습니다: {name}")
        return exit_codes.OK

    if args.subcommand == "remove":
        name = remove_category(store, repository, args.name.strip())
        print(f"카테고리를 삭제했습니다: {name}")
        return exit_codes.OK

    names = store.names()
    rows = [[name, str(count_category_usage(repository, name))] for name in names]
    print(format_table(["카테고리", "사용 건수"], rows, right_align={1}))
    print(f"\n총 {len(names)}개")
    return exit_codes.OK


@handle_errors
@log_call
@measure_time
def run_export(paths: DataPaths, args: argparse.Namespace) -> int:
    """조건에 맞는 거래를 교환용 CSV로 내보낸다. 기간 조건이 없으면 거부한다."""
    if args.month:
        month = validate_month(args.month)
        # 문자열 비교라 -31 로 잡아도 짧은 달이 안전하다 (2월 30일 같은 날짜는 없다)
        filters = SearchFilters(date_from=f"{month}-01", date_to=f"{month}-31")
    elif args.date_from and args.date_to:
        filters = SearchFilters(
            date_from=validate_date(args.date_from), date_to=validate_date(args.date_to)
        )
    else:
        # 조건 없이 전체를 내보내면 파일이 통째로 새어 나간다. 기간을 반드시 받는다.
        raise ValidationError(
            "기간 조건이 필요합니다.", "--month YYYY-MM 또는 --from/--to 를 지정하세요"
        )

    out_path = Path(args.out)
    written = export_transactions(TransactionRepository(paths.transactions), filters, out_path)
    print(f"[완료] exported={written} -> {out_path}")
    if written == 0:
        print("[안내] 조건에 맞는 거래가 없어 헤더만 있는 파일을 만들었습니다.")
    return exit_codes.OK


@handle_errors
@log_call
@measure_time
def run_import(paths: DataPaths, source: str) -> int:
    """CSV에서 거래를 가져온다. 잘못된 행은 건너뛰고 사유를 알려 준다."""
    result = import_transactions(
        TransactionRepository(paths.transactions),
        CategoryStore(paths.categories),
        Path(source),
    )

    print(f"[완료] imported={result.imported}, skipped={result.skipped_count}")
    for line_number, reason in result.skipped:
        print(f"  - {line_number}번째 줄 건너뜀: {reason}")
    return exit_codes.OK


@handle_errors
@log_call
@measure_time
def run_backup(paths: DataPaths) -> int:
    """저장 파일을 백업 폴더로 복사한다."""
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    copied = copy_to_backup(paths, stamp)
    print(f"[완료] backup={len(copied)}개 -> {paths.backups}")
    for target in copied:
        print(f"  - {target.name}")
    return exit_codes.OK


@handle_errors
@log_call
@measure_time
def run_recurring(paths: DataPaths, args: argparse.Namespace) -> int:
    """반복 규칙을 관리하고, 지정한 달의 거래를 생성한다."""
    store = RecurringStore(paths.recurring)
    repository = TransactionRepository(paths.transactions)

    if args.subcommand == "add":
        rule = RecurringRule(
            id=next_recurring_id(store),
            day=validate_day(args.day),
            type=validate_type(args.type),
            category=validate_category(args.category, CategoryStore(paths.categories).names()),
            amount=validate_amount(args.amount),
            memo=args.memo.strip(),
        )
        add_recurring_rule(store, rule)
        print(f"반복 규칙을 추가했습니다. id: {rule.id} (매월 {rule.day}일)")
        return exit_codes.OK

    if args.subcommand == "remove":
        removed = remove_recurring_rule(store, args.id)
        print(f"반복 규칙을 삭제했습니다: {removed.id}")
        return exit_codes.OK

    if args.subcommand == "apply":
        month = validate_month(args.month)
        created, already = apply_recurring(repository, store, month)
        print(f"[완료] created={len(created)}, skipped={len(already)}")
        for transaction in created:
            print(f"  + {transaction.id} {transaction.date} {transaction.category} "
                  f"{format_amount(transaction.amount)}원")
        for rule_id in already:
            print(f"  - {rule_id}: 이미 {month} 에 생성되어 있습니다")
        return exit_codes.OK

    rules = list(store.stream())
    if not rules:
        print("데이터 없음. 등록된 반복 규칙이 없습니다.")
        return exit_codes.OK

    print(format_table(
        ["id", "day", "type", "category", "amount", "memo"],
        [[r.id, str(r.day), r.type, r.category, format_amount(r.amount), r.memo] for r in rules],
        right_align={4},
    ))
    print(f"\n총 {len(rules)}개")
    return exit_codes.OK


@handle_errors
@log_call
@measure_time
def run_delete(paths: DataPaths, transaction_id: str) -> int:
    """거래를 삭제한다. 없는 id는 오류로 알린다."""
    repository = TransactionRepository(paths.transactions)
    removed = delete_transaction(repository, transaction_id)
    print(f"삭제했습니다. id: {removed.id} "
          f"({removed.date} {removed.category} {format_amount(removed.amount)}원)")
    return exit_codes.OK


# --------------------------------------------------------------------------- 진입


def _announce_created(created: list[str]) -> None:
    if created:
        print(f"[안내] 저장 파일을 새로 만들었습니다: {', '.join(created)}")
        print("[안내] 기본 카테고리 5종(food, transport, rent, salary, etc)을 등록했습니다.")


def main(argv: Sequence[str] | None = None) -> int:
    """명령을 실행하고 종료 코드를 돌려준다."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.verbose:
        # 로그는 표준 오류로 내보낸다. 표준 출력을 파이프로 넘겨도 결과가 섞이지 않는다.
        logging.basicConfig(level=logging.DEBUG, stream=sys.stderr, format="[log] %(message)s")

    if args.command is None:
        parser.print_help()
        return exit_codes.OK

    paths = DataPaths(args.data_dir)
    try:
        created = ensure_files(paths)
    except OSError as error:
        print(f"[오류] 저장 폴더를 준비하지 못했습니다: {paths.root}")
        print(f"[힌트] 경로와 쓰기 권한을 확인하세요. ({error.strerror})")
        return exit_codes.SYSTEM_ERROR
    _announce_created(created)

    if args.command == "add":
        return run_add(paths)
    if args.command == "list":
        return run_list(paths, args.limit)
    if args.command == "update":
        return run_update(paths, args.id)
    if args.command == "delete":
        return run_delete(paths, args.id)
    if args.command == "search":
        return run_search(paths, args)
    if args.command == "summary":
        return run_summary(paths, args.month, args.top)
    if args.command == "budget":
        if args.subcommand != "set":
            print("[오류] budget 은 하위 명령이 필요합니다.")
            print("[힌트] 예: python -m budget_app budget set --month 2024-01 --amount 500000")
            return exit_codes.USER_ERROR
        return run_budget_set(paths, args.month, args.amount)
    if args.command == "export":
        return run_export(paths, args)
    if args.command == "import":
        return run_import(paths, args.source)
    if args.command == "backup":
        return run_backup(paths)
    if args.command == "recurring":
        if args.subcommand not in ("add", "list", "remove", "apply"):
            print("[오류] recurring 은 하위 명령이 필요합니다.")
            print("[힌트] add / list / remove / apply 중 하나를 쓰세요")
            return exit_codes.USER_ERROR
        return run_recurring(paths, args)
    if args.command == "category":
        if args.subcommand not in ("add", "list", "remove"):
            print("[오류] category 는 하위 명령이 필요합니다.")
            print("[힌트] add / list / remove 중 하나를 쓰세요")
            return exit_codes.USER_ERROR
        return run_category(paths, args)

    # argparse 가 등록되지 않은 명령을 먼저 걸러내므로 여기에는 도달하지 않는다.
    parser.print_help()
    return exit_codes.USER_ERROR
