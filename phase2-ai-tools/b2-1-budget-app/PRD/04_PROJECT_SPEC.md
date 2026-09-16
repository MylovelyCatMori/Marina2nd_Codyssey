# B2-1 나만의 용돈 기입장 -- 프로젝트 스펙 (AI 행동 규칙)

> 생성일: 2026-09-17
> 이 문서는 **구현 중 판단 기준**이다. 애매하면 여기를 본다.

---

## 기술 스택

| 항목 | 선택 | 제약 근거 |
|---|---|---|
| 언어 | **Python 3.10 이상** | 원문 6번 |
| 외부 라이브러리 | **전면 금지** | 원문 7번. `pip install` 필요한 것 전부 |
| 표준 라이브러리 | `argparse` `csv` `dataclasses` `datetime` `pathlib` `os` `typing` `functools` `shutil` `logging` | 전부 내장 |
| 저장 포맷 | **CSV** (UTF-8, 헤더 포함) | 원문 7번 중 택일 |
| 저장 파일 수 | **3개 이상** | 원문 7번 |
| 실행 방식 | `python -m budget_app <command> [options]` | 원문 4번 권장안 |
| 옵션 표기 | **`--` 통일** | 원문 4번 |

### 표준 라이브러리 사용처

| 모듈 | 용도 |
|---|---|
| `argparse` | 서브커맨드 + `--help` 자동 생성 |
| `csv` | CSV 읽기/쓰기. **쉼표·따옴표 처리를 직접 하지 않기 위해** |
| `dataclasses` | 데이터 모델 |
| `datetime` | 날짜 검증 (`strptime`) |
| `pathlib` | 경로 조작 |
| `os` | `os.replace` (원자적 교체) |
| `typing` | `Iterator`, `Optional` 등 |
| `functools` | `wraps` (데코레이터가 원본 함수 이름을 잃지 않게) |
| `shutil` | 백업 파일 복사 |

---

## 프로젝트 구조

```
b2-1-budget-app/
├── budget_app/
│   ├── __init__.py
│   ├── __main__.py         # 진입점. python -m budget_app 로 실행됨
│   ├── cli.py              # argparse 정의 + 명령 분기 (CLI 계층)
│   ├── models.py           # dataclass 정의 (모델 계층)
│   ├── storage.py          # 파일 읽기/쓰기 (저장소 계층)
│   ├── services.py         # 규칙 판단·집계 (서비스 계층)
│   ├── validators.py       # 입력 검증
│   ├── decorators.py       # 공통 관심사 (예외/로그/시간)
│   └── formatter.py        # 출력 정렬 (보너스)
├── data/                   # 실행 시 자동 생성
│   ├── transactions.csv
│   ├── categories.csv
│   ├── budgets.csv
│   ├── recurring.csv       # 보너스
│   └── backups/            # 보너스
├── PRD/                    # 설계 문서 4종
├── REQUIREMENTS.md         # 요구사항 전수 추적표
├── TODO.md                 # 단계별 작업 기록
└── README.md               # 제출물
```

**모듈이 8개인 이유** — 원문은 "최소 3개"를 요구하지만, 계층별로 나누면 자연히 이
정도가 됩니다. 한 파일이 500줄을 넘으면 다시 쪼갭니다.

---

## 계층별 책임 (이 경계를 넘지 않는다)

| 계층 | 파일 | 하는 일 | **하지 않는 일** |
|---|---|---|---|
| CLI | `cli.py` | 인자 파싱, 사용자 입출력 | 파일 접근, 계산 |
| 서비스 | `services.py` | 규칙 판단, 집계 | `print()`, `input()`, 파일 직접 열기 |
| 저장소 | `storage.py` | 파일 읽기/쓰기 | 업무 규칙 판단, `print()` |
| 모델 | `models.py` | 데이터 모양 정의 | 그 외 전부 |

> **가장 흔한 위반**: 저장소 안에서 `print()`를 부르는 것. 저장소는 값을 돌려줄
> 뿐이고, 화면에 무엇을 보여줄지는 CLI가 정합니다. 이 경계가 지켜져야
> "각 계층의 책임을 설명할 수 있다"(과제 목표 2번)에 답할 수 있습니다.

---

## 절대 하지 마 (DO NOT)

1. **외부 라이브러리 import 금지.** `pandas`, `rich`, `click`, `tabulate` 전부 금지
2. **`readlines()` / `list(reader)` / `f.read()` 금지.** 반드시 제너레이터
3. **`csv` 모듈 없이 `split(',')` 금지.** 메모·태그의 쉼표에서 즉시 깨진다
4. **스택트레이스 출력 금지.** `원인 + 힌트` 두 줄로 바꾼다
5. **오류인데 종료 코드 0 금지.** `sys.exit(1)` 이상
6. **한 파일에 몰아넣기 금지.** 최소 3개 모듈, 계층 경계 준수
7. **원본 파일에 직접 덮어쓰기 금지.** 임시 파일 + `os.replace`
8. **타입 힌트 생략 금지.** 모든 public 함수의 인자·반환
9. **`amount`를 문자열로 다루기 금지.** 읽는 즉시 `int()` 변환
10. **`day`를 29~31로 허용 금지** (반복 내역). 2월에 생성 불가
11. **예산 0원으로 나누기 금지.** 예산 없으면 그 줄을 출력하지 않는다
12. **저장소 계층에서 `print()` / `input()` 금지**
13. **`except:` 맨몸 금지.** 잡을 예외를 명시한다
14. **거래 0건을 에러로 처리 금지.** "데이터 없음"은 정상이다
15. **옵션에 `-` 단일 하이픈 금지.** `--`로 통일

---

## 항상 해 (ALWAYS DO)

1. 새 명령을 만들면 `--help` 문구를 함께 쓴다
2. 검증 실패는 **재입력 요구**(대화형) 또는 **오류 + 힌트**(옵션)로 처리한다
3. 오류 메시지는 `[오류] 원인` + `[힌트] 해결 방법` 두 줄 형식을 지킨다
4. 파일을 쓰기 전에 `data/` 폴더 존재를 확인하고 없으면 만든다
5. 금액은 천 단위 구분 기호로 출력한다 (`15,000원`)
6. 날짜 비교는 `YYYY-MM-DD` 문자열 그대로 한다 (사전순 = 시간순)
7. 커밋 메시지는 Conventional Commits를 따른다
8. Phase마다 `feature/b2-1-phaseN` 브랜치 → `--no-ff` 병합

---

## 오류 메시지 형식 (고정)

```
[오류] 날짜 형식이 올바르지 않습니다 (YYYY-MM-DD).
[힌트] 예: 2024-01-15
```

| 상황 | 원인 문구 | 힌트 문구 |
|---|---|---|
| 날짜 형식 | 날짜 형식이 올바르지 않습니다 (YYYY-MM-DD). | 예: 2024-01-15 |
| 존재하지 않는 날짜 | 존재하지 않는 날짜입니다. | 2월은 28일(윤년 29일)까지입니다 |
| 타입 오류 | 타입은 income 또는 expense 만 가능합니다. | 입력값: {입력} |
| 금액 오류 | 금액은 1 이상의 정수여야 합니다. | 쉼표 없이 숫자만 입력하세요 |
| 없는 카테고리 | 등록되지 않은 카테고리입니다: {이름} | 사용 가능: food, transport, ... |
| 없는 id | 해당 id의 거래를 찾을 수 없습니다: {id} | list 명령으로 id를 확인하세요 |
| 사용 중 카테고리 삭제 | '{이름}'를 사용하는 거래가 {N}건 있습니다. | 해당 거래를 먼저 수정하거나 삭제하세요 |
| export 조건 누락 | 기간 조건이 필요합니다. | --month YYYY-MM 또는 --from/--to 를 지정하세요 |
| CSV 헤더 불일치 | CSV 헤더가 스키마와 다릅니다. | 필요한 열: date,type,category,amount,memo,tags |

---

## 종료 코드

| 코드 | 의미 | 예시 |
|---|---|---|
| `0` | 정상 | 저장 성공, 데이터 없음(정상 상태) |
| `1` | 사용자 오류 | 잘못된 입력, 없는 id, 삭제 차단 |
| `2` | 시스템 오류 | 파일 권한 없음, 디스크 오류 |

---

## 테스트 방법

자동 테스트 프레임워크는 쓰지 않습니다(외부 라이브러리 금지, `unittest`는 허용되나
과제 요구가 아님). **수동 검증 시나리오**를 `TODO.md`에 체크리스트로 둡니다.

```bash
# 정상 경로
python -m budget_app add                      # 대화형 입력
python -m budget_app list --limit 5
python -m budget_app summary --month 2026-09 --top 3

# 오류 경로
python -m budget_app delete --id NOPE         # 없는 id → 코드 1
python -m budget_app export --out a.csv       # 조건 누락 → 코드 1
python -m budget_app category remove          # 사용 중 → 코드 1

# 종료 코드 확인 (Git Bash)
echo $?
```

---

## 배포 방법

**배포하지 않습니다.** 콘솔 프로그램이므로 GitHub Pages 대상이 아닙니다.
제출물은 **저장소 URL + 하위 경로**입니다.

```
https://github.com/MylovelyCatMori/Marina2nd_Codyssey
└── phase2-ai-tools/b2-1-budget-app/
```

---

## 환경변수

**사용하지 않습니다.** 저장 위치는 `--data-dir` 옵션으로 바꿉니다.

---

## [NEEDS CLARIFICATION]

| 항목 | 현재 가정 | 확정 시점 |
|---|---|---|
| `data/`를 git에 올릴 것인가 | **올린다** (샘플 데이터로 동료평가 시연용) | Phase 0 |
| 로그 파일 위치 | `data/app.log` 또는 stderr | Phase 2 |
| `--data-dir` 기본값 | 실행 위치 기준 `./data` | Phase 0 |
