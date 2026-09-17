"""입력 검증. 값을 확인하고 정규화해서 돌려준다.

규칙에 맞지 않으면 ValidationError 를 올린다. 여기서는 print() / input() 을 쓰지 않는다.
검증을 한곳에 모아 두면 대화형(add)과 옵션형(import)이 같은 규칙을 공유한다.
"""

from __future__ import annotations

from datetime import datetime

from .errors import ValidationError
from .models import TRANSACTION_TYPES

DATE_FORMAT = "%Y-%m-%d"
MONTH_FORMAT = "%Y-%m"
TAG_SEPARATOR = ","


def validate_date(raw: str) -> str:
    """YYYY-MM-DD 이면서 달력에 실제로 있는 날짜인지 확인한다."""
    text = raw.strip()
    try:
        parsed = datetime.strptime(text, DATE_FORMAT)
    except ValueError as error:
        # strptime 은 형식 오류와 존재하지 않는 날짜를 모두 ValueError 로 올린다.
        # 둘은 사용자가 고쳐야 할 내용이 다르므로 메시지를 갈라 준다.
        if "unconverted data" in str(error) or "does not match format" in str(error):
            raise ValidationError(
                "날짜 형식이 올바르지 않습니다 (YYYY-MM-DD).", "예: 2024-01-15"
            ) from error
        raise ValidationError(
            "존재하지 않는 날짜입니다.", "2월은 28일(윤년 29일)까지입니다"
        ) from error
    return parsed.strftime(DATE_FORMAT)


def validate_month(raw: str) -> str:
    """YYYY-MM 형식인지 확인한다."""
    text = raw.strip()
    try:
        parsed = datetime.strptime(text, MONTH_FORMAT)
    except ValueError as error:
        raise ValidationError(
            "월 형식이 올바르지 않습니다 (YYYY-MM).", "예: 2024-01"
        ) from error
    return parsed.strftime(MONTH_FORMAT)


def validate_type(raw: str) -> str:
    """income / expense 만 허용한다."""
    text = raw.strip().lower()
    if text not in TRANSACTION_TYPES:
        raise ValidationError(
            "타입은 income 또는 expense 만 가능합니다.", f"입력값: {raw.strip()}"
        )
    return text


def validate_amount(raw: str | int) -> int:
    """1 이상의 정수만 허용한다. 0과 음수는 거부한다."""
    text = str(raw).strip()
    hint = "쉼표 없이 숫자만 입력하세요"
    # int() 는 '１２３'(전각 숫자)도 123 으로 받아들인다. 파일에 남는 값과
    # 사용자가 친 글자가 달라지므로 ASCII 숫자만 통과시킨다.
    if not text.isascii():
        raise ValidationError("금액은 1 이상의 정수여야 합니다.", hint)
    try:
        amount = int(text)
    except ValueError as error:
        raise ValidationError("금액은 1 이상의 정수여야 합니다.", hint) from error
    if amount < 1:
        raise ValidationError("금액은 1 이상의 정수여야 합니다.", hint)
    return amount


def validate_category(raw: str, known: list[str]) -> str:
    """등록된 카테고리 목록에 있는 이름인지 확인한다."""
    text = raw.strip()
    if text not in known:
        raise ValidationError(
            f"등록되지 않은 카테고리입니다: {text}",
            f"사용 가능: {', '.join(known) if known else '(없음)'}",
        )
    return text


MIN_RECURRING_DAY = 1
MAX_RECURRING_DAY = 28


def validate_day(raw: str | int) -> int:
    """반복 규칙의 날짜. 1~28 만 허용한다 (2월에도 반드시 존재하는 날)."""
    hint = f"{MIN_RECURRING_DAY}~{MAX_RECURRING_DAY} 사이로 입력하세요 (2월은 28일까지입니다)"
    text = str(raw).strip()
    if not text.isascii():
        raise ValidationError("반복 일자는 정수여야 합니다.", hint)
    try:
        day = int(text)
    except ValueError as error:
        raise ValidationError("반복 일자는 정수여야 합니다.", hint) from error
    if not MIN_RECURRING_DAY <= day <= MAX_RECURRING_DAY:
        raise ValidationError(
            f"반복 일자는 {MIN_RECURRING_DAY}~{MAX_RECURRING_DAY} 만 가능합니다.", hint
        )
    return day


def validate_tags(raw: str) -> list[str]:
    """쉼표로 구분한 태그 문자열을 목록으로 바꾼다. 빈 입력은 빈 목록이다."""
    return [tag.strip() for tag in raw.split(TAG_SEPARATOR) if tag.strip()]
