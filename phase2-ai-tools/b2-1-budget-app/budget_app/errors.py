"""이 프로그램이 스스로 만들어 내는 오류 종류.

사용자에게 보여 줄 `원인 + 힌트` 두 줄을 예외가 직접 들고 다닌다.
그래야 스택트레이스를 찍지 않고도 어디서 난 오류든 같은 형식으로 출력할 수 있다.
"""

from __future__ import annotations


class AppError(Exception):
    """사용자 오류. 종료 코드 1로 이어진다."""

    def __init__(self, message: str, hint: str = "") -> None:
        super().__init__(message)
        self.message = message
        self.hint = hint


class ValidationError(AppError):
    """입력값이 규칙에 맞지 않을 때. 대화형에서는 재입력을 요구한다."""


class NotFoundError(AppError):
    """지정한 데이터가 없을 때."""
