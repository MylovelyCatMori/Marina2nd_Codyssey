"""공통 관심사 데코레이터. 명령마다 반복되는 처리를 한곳에 모은다.

데코레이터는 함수를 감싸 앞뒤에 공통 동작을 끼워 넣는 장치다.
try/except 를 명령 10개에 복사하는 대신 @handle_errors 한 줄을 붙인다.
"""

from __future__ import annotations

import functools
import logging
import time
from typing import Callable, TypeVar

from . import exit_codes
from .errors import AppError

logger = logging.getLogger(__name__)

Command = TypeVar("Command", bound=Callable[..., int])


def handle_errors(func: Command) -> Command:
    """예외를 `[오류]` + `[힌트]` 두 줄로 바꾸고 종료 코드를 돌려준다.

    스택트레이스는 개발자용이다. 사용자에게는 원인과 다음 행동만 보여 준다.
    """

    @functools.wraps(func)  # 원본 함수의 이름과 docstring 을 보존한다
    def wrapper(*args: object, **kwargs: object) -> int:
        try:
            return func(*args, **kwargs)
        except AppError as error:
            print(f"[오류] {error.message}")
            if error.hint:
                print(f"[힌트] {error.hint}")
            return exit_codes.USER_ERROR
        except (KeyboardInterrupt, EOFError):
            # 대화형 입력 중 Ctrl+C 또는 입력 종료(Ctrl+Z/Ctrl+D).
            # 저장은 입력이 전부 끝난 뒤에만 하므로 원본은 그대로다.
            print("\n[안내] 입력을 취소했습니다. 저장된 내용은 없습니다.")
            return exit_codes.USER_ERROR
        except OSError as error:
            print(f"[오류] 파일을 다루지 못했습니다: {error.filename}")
            print(f"[힌트] 경로와 접근 권한을 확인하세요. ({error.strerror})")
            return exit_codes.SYSTEM_ERROR
        except Exception as error:  # noqa: BLE001 - 마지막 그물. 맨몸 except: 는 쓰지 않는다
            # 예상하지 못한 오류도 스택트레이스 대신 두 줄로 바꾼다.
            # 개발자용 상세 내용은 로그로만 남기고 --verbose 일 때 보여 준다.
            logger.debug("unhandled in %s", func.__name__, exc_info=True)
            print(f"[오류] 처리하지 못한 문제가 생겼습니다: {type(error).__name__}")
            print("[힌트] 명령 앞에 --verbose 를 붙이면 자세한 내용이 보입니다. "
                  "예: python -m budget_app --verbose list")
            return exit_codes.SYSTEM_ERROR

    return wrapper  # type: ignore[return-value]


def log_call(func: Command) -> Command:
    """어떤 명령이 어떤 인자로 불렸는지 로그로 남긴다 (--verbose 일 때만 보인다)."""

    @functools.wraps(func)
    def wrapper(*args: object, **kwargs: object) -> int:
        logger.debug("call %s args=%s kwargs=%s", func.__name__, args, kwargs)
        result = func(*args, **kwargs)
        logger.debug("done %s exit=%s", func.__name__, result)
        return result

    return wrapper  # type: ignore[return-value]


def measure_time(func: Command) -> Command:
    """실행 시간을 로그로 남긴다 (--verbose 일 때만 보인다)."""

    @functools.wraps(func)
    def wrapper(*args: object, **kwargs: object) -> int:
        # perf_counter 는 시계 보정에 흔들리지 않는 단조 증가 타이머다.
        started = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed_ms = (time.perf_counter() - started) * 1000
            logger.debug("%s 소요 %.1fms", func.__name__, elapsed_ms)

    return wrapper  # type: ignore[return-value]
