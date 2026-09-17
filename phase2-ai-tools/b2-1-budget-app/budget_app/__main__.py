"""진입점. `python -m budget_app` 로 실행된다.

`-m` 으로 패키지를 실행하면 패키지 기준 import 경로가 유지되므로
`from .cli import main` 같은 상대 import가 깨지지 않는다.
"""

from __future__ import annotations

import sys

from . import exit_codes
from .cli import main

MIN_PYTHON = (3, 10)

# Windows 기본 인코딩(cp949)에서 한글이 깨지므로 입출력 모두 UTF-8로 맞춘다.
# 입력까지 맞춰야 파이프로 넣은 한글 메모가 깨진 채 파일에 저장되지 않는다.
sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

if sys.version_info < MIN_PYTHON:
    print(f"[오류] Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]} 이상이 필요합니다.")
    print(f"[힌트] 현재 버전: {sys.version.split()[0]}. 최신 Python으로 실행하세요.")
    sys.exit(exit_codes.SYSTEM_ERROR)

sys.exit(main())
