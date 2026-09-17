"""모델 계층. 데이터의 모양만 정의한다.

파일 접근, 화면 출력, 규칙 판단은 여기서 하지 않는다.
"""

from __future__ import annotations

from dataclasses import dataclass, field

INCOME = "income"
EXPENSE = "expense"
TRANSACTION_TYPES: tuple[str, str] = (INCOME, EXPENSE)


@dataclass
class Transaction:
    """거래 한 건. 이 프로그램에서 유일하게 계속 늘어나는 데이터다."""

    id: str
    date: str          # YYYY-MM-DD. 사전순 정렬 = 시간순 정렬이라 str로 둔다
    type: str          # income / expense
    category: str
    amount: int        # 양수 정수. 읽는 즉시 int로 변환한다
    memo: str = ""
    # list[str] = [] 로 쓰면 모든 인스턴스가 리스트 하나를 공유한다 (가변 기본값 함정)
    tags: list[str] = field(default_factory=list)


@dataclass
class Category:
    """분류. 이름만 가진다. 중복 불가."""

    name: str


@dataclass
class Budget:
    """월 예산. 같은 달은 한 건만 존재한다."""

    month: str         # YYYY-MM
    amount: int


@dataclass
class RecurringRule:
    """매달 같은 날 생기는 거래 규칙 (월급, 월세 등).

    day 를 1~28 로 제한한다. 2월은 28일까지라 31일 규칙은 2월에 만들 수 없고,
    "말일로 당긴다" 같은 보정을 넣으면 그 자체가 또 하나의 예외 처리 대상이 된다.
    """

    id: str            # RC- + 4자리
    day: int           # 1~28
    type: str
    category: str
    amount: int
    memo: str = ""


@dataclass
class SearchFilters:
    """검색 조건. 지정하지 않은 항목은 None 이고, 조건들은 AND 로 묶인다."""

    date_from: str | None = None
    date_to: str | None = None
    category: str | None = None
    type: str | None = None
    query: str | None = None       # 메모 키워드
    tag: str | None = None


@dataclass
class MonthlySummary:
    """한 달 집계 결과. 예산이 없는 달은 budget 이 None 이다 (0원이 아니다)."""

    month: str
    count: int
    total_income: int
    total_expense: int
    top_categories: list[tuple[str, int]]
    budget: int | None = None

    @property
    def balance(self) -> int:
        return self.total_income - self.total_expense

    @property
    def usage_percent(self) -> float | None:
        """예산 사용률. 예산이 없으면 None -- 0으로 나누지 않는다."""
        if not self.budget:
            return None
        return self.total_expense / self.budget * 100

    @property
    def is_over_budget(self) -> bool:
        return self.budget is not None and self.total_expense > self.budget
