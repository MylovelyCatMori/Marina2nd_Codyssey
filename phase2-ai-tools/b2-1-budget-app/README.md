# 나만의 용돈 기입장 (B2-1)

콘솔에서 쓰는 가계부입니다. **표준 라이브러리만** 사용하며 설치할 외부 패키지가 없습니다.
거래를 CSV 파일에 저장하고, 검색·월별 요약·예산 관리·CSV 입출력을 제공합니다.

---

## 1. 실행 방법

필요 조건: **Python 3.10 이상** (개발·검증 환경 3.14.3)

```bash
cd b2-1-budget-app
python -m budget_app --help          # 명령 목록
python -m budget_app add             # 거래 추가 (대화형)
```

설치 과정이 없습니다. `pip install` 이 필요한 라이브러리를 쓰지 않습니다.

전역 옵션은 **명령 앞에** 붙입니다.

```bash
python -m budget_app --data-dir ./mydata list    # 저장 폴더 변경
python -m budget_app --verbose summary --month 2024-01   # 실행 로그 + 소요 시간
```

> argparse 는 서브커맨드가 앞쪽 전역 옵션 값을 자기 기본값으로 덮어씁니다.
> 그래서 `list --verbose` 가 아니라 `--verbose list` 순서로 씁니다.

자체 점검 실행:

```bash
python tests/test_phase1.py   # 모델·저장소·읽기
python tests/test_phase2.py   # 검증·데코레이터·쓰기
python tests/test_phase3.py   # 검색·집계·예산
python tests/test_phase4.py   # import / export
python tests/test_phase5.py   # 백업·반복 내역
bash tests/verify_all.sh      # 명령 12개 전수 실행 + 종료 코드 검증 (55건)
```

---

## 2. 저장 파일 위치와 형식

기본 저장 폴더는 `./data` 이고 `--data-dir` 로 바꿉니다. 첫 실행 때 자동으로 만들어집니다.

| 파일 | 내용 | 열 |
|---|---|---|
| `data/transactions.csv` | 거래 | `id,date,type,category,amount,memo,tags` |
| `data/categories.csv` | 카테고리 | `name` |
| `data/budgets.csv` | 월 예산 | `month,amount` |
| `data/recurring.csv` | 반복 규칙 (보너스) | `id,day,type,category,amount,memo` |
| `data/backups/` | 백업 복사본 (보너스) | `<원본이름>-YYYYMMDD-HHMMSS.csv` |

- 형식: **CSV, UTF-8, 헤더 포함**
- 첫 실행 시 기본 카테고리 5종(`food` `transport` `rent` `salary` `etc`)을 자동 등록합니다.
- 파일이 3개로 나뉜 이유: 거래는 계속 쌓이고, 카테고리는 거의 안 변하고, 예산은 달에 한 번
  바뀝니다. **변경 주기가 다른 데이터를 한 파일에 두면** 거래 한 건을 고칠 때 카테고리까지
  다시 써야 합니다.

`transactions.csv` 예시입니다.

```csv
id,date,type,category,amount,memo,tags
TX-000001,2024-01-05,income,salary,3000000,1월 월급,fixed
TX-000002,2024-01-12,expense,food,8000,"김밥, 라면","meal,quick"
```

두 번째 행은 메모에 쉼표가 있고 태그가 두 개입니다. 둘 다 따옴표로 감싸여 있으며
`csv` 모듈이 자동으로 처리합니다. 직접 `split(',')` 을 쓰면 이 행에서 깨집니다.

---

## 3. 주요 명령 예시

### 거래

```bash
python -m budget_app add                          # 대화형 입력 (잘못 넣으면 재입력 요구)
python -m budget_app list --limit 5               # 최신 5건
python -m budget_app update --id TX-000001        # 번호를 골라 필드별 수정
python -m budget_app delete --id TX-000001
```

### 검색 (조건은 AND로 묶입니다)

```bash
python -m budget_app search --from 2024-01-01 --to 2024-01-31
python -m budget_app search --category food --type expense
python -m budget_app search --q 김밥 --tag quick
```

### 요약과 예산

```bash
python -m budget_app budget set --month 2024-01 --amount 500000
python -m budget_app summary --month 2024-01 --top 3
```

```
[2024-01] 거래 4건

항목           금액
------  -----------
총수입  3,000,000원
총지출     73,000원
잔액    2,927,000원

카테고리별 지출 TOP 2
카테고리       지출
---------  --------
transport  50,000원
food       23,000원

예산 50,000원 / 사용률 146.0%
[경고] 예산을 23,000원 초과했습니다.
```

예산을 설정하지 않은 달은 **예산 줄 자체가 나오지 않습니다.** "예산 0원"으로 표시하면
사용률 계산에서 0으로 나누게 됩니다.

### 카테고리

```bash
python -m budget_app category list
python -m budget_app category add --name cafe
python -m budget_app category remove --name food
# [오류] 'food'를 사용하는 거래가 2건 있습니다.
# [힌트] 해당 거래를 먼저 수정하거나 삭제하세요
```

### 입출력

```bash
python -m budget_app export --out backup/jan.csv --month 2024-01
python -m budget_app export --out q1.csv --from 2024-01-01 --to 2024-03-31
python -m budget_app import --from jan.csv
```

### 보너스

```bash
python -m budget_app backup                                   # data/backups/ 로 복사
python -m budget_app recurring add --day 25 --type income \
    --category salary --amount 3000000 --memo "월급"
python -m budget_app recurring apply --month 2024-02          # 해당 달 거래 생성
python -m budget_app recurring list
python -m budget_app recurring remove --id RC-0001
```

---

## 4. import / export CSV 스키마

`export` 와 `import` 는 **같은 스키마**를 씁니다.

```csv
date,type,category,amount,memo,tags
2024-03-01,expense,food,12000,"떡볶이, 순대","meal,snack"
2024-03-02,income,salary,2500000,3월 월급,
```

| 열 | 필수 | 규칙 |
|---|---|---|
| `date` | O | `YYYY-MM-DD`. 달력에 실제로 있는 날짜여야 합니다 (`2024-02-30` 거부) |
| `type` | O | `income` 또는 `expense` |
| `category` | O | 등록된 카테고리여야 합니다 |
| `amount` | O | **1 이상의 정수**. 쉼표·0·음수 거부 |
| `memo` | X | 문자열. 쉼표가 있으면 따옴표로 감쌉니다 |
| `tags` | X | 쉼표 구분 문자열 (`meal,quick`) |

- **`id` 는 스키마에 없습니다.** 가져올 때 새로 채번합니다. 남의 파일에서 온 id가 기존 id와
  충돌하면 수정·삭제가 엉뚱한 행을 건드립니다.
- `export` 는 **기간 조건이 필수**입니다 (`--month` 또는 `--from` + `--to`). 조건 없이
  전체를 내보내는 실수를 막습니다.
- `import` 는 **행 단위로 판정**합니다. 잘못된 행은 건너뛰고 줄 번호와 사유를 알려 줍니다.

```
[완료] imported=1, skipped=2
  - 3번째 줄 건너뜀: 금액은 1 이상의 정수여야 합니다.
  - 4번째 줄 건너뜀: 존재하지 않는 날짜입니다.
```

- 단, **헤더가 스키마와 다르면 한 건도 쓰지 않고 중단**합니다. 파일 전체의 문제이므로
  절반만 가져온 상태를 만들지 않습니다.

---

## 5. 구조

```
budget_app/
├── __main__.py     진입점 (python -m budget_app)
├── cli.py          인자 파싱 + 화면 입출력
├── services.py     규칙 판단, 집계
├── storage.py      파일 읽기/쓰기
├── models.py       데이터 모양 (dataclass)
├── validators.py   입력 검증
├── decorators.py   공통 관심사 (예외/로그/시간)
├── formatter.py    출력 정렬
├── errors.py       오류 종류
└── exit_codes.py   종료 코드
```

| 계층 | 하는 일 | **하지 않는 일** |
|---|---|---|
| CLI | 인자 파싱, 사용자 입출력 | 파일 접근, 계산 |
| 서비스 | 규칙 판단, 집계 | `print()`, `input()`, 파일 직접 열기 |
| 저장소 | 파일 읽기/쓰기 | 업무 규칙 판단, `print()` |
| 모델 | 데이터 모양 정의 | 그 외 전부 |

### 종료 코드

| 코드 | 의미 | 예 |
|---|---|---|
| `0` | 정상 | 저장 성공, **데이터 없음**(정상 상태) |
| `1` | 사용자 오류 | 잘못된 입력, 없는 id, 삭제 차단 |
| `2` | 시스템 오류 | 파일 권한 없음, 디스크 오류 |

거래 0건은 오류가 아닙니다. "데이터 없음"을 출력하고 `0` 으로 끝냅니다.

### 오류 출력 형식

스택트레이스를 찍지 않습니다. 원인과 다음 행동만 두 줄로 보여 줍니다.

```
[오류] 날짜 형식이 올바르지 않습니다 (YYYY-MM-DD).
[힌트] 예: 2024-01-15
```

---

## 6. 과제 목표별 설명 (G-01 ~ G-05)

### G-01. 파일 기반 저장으로 CRUD / 검색 / 요약 / 입출력

CSV 3개로 나눠 영구 저장하고, 추가(`add`) · 조회(`list` `search`) · 수정(`update`) ·
삭제(`delete`) · 요약(`summary`) · 입출력(`import` `export`)을 제공합니다.

수정과 삭제는 **원자적 교체**로 처리합니다.

```python
tmp = path.with_suffix(".tmp")
with open(tmp, "w", newline="", encoding="utf-8") as f:
    ...쓰기...
os.replace(tmp, path)   # 이 한 줄이 원자적이다
```

원본에 직접 쓰다가 프로그램이 죽으면 파일이 반쪽으로 남습니다. 임시 파일에 전부 쓴 뒤
이름을 바꾸면 교체는 성공하거나 실패하거나 둘 중 하나이고, 중간 상태가 없습니다.
임시 파일을 같은 폴더에 두는 이유는 다른 디스크로 옮기면 교체가 원자적이지 않기 때문입니다.

### G-02. 계층별 책임

위 표가 경계입니다. **가장 흔한 위반은 저장소 안에서 `print()` 를 부르는 것**입니다.
저장소는 값을 돌려줄 뿐이고, 화면에 무엇을 보여줄지는 CLI가 정합니다.

예를 들어 `ensure_files()` 는 새로 만든 파일 이름의 목록만 돌려주고, "기본 카테고리를
등록했습니다" 라는 안내는 `cli.py` 가 출력합니다. 이 경계 덕분에 저장 형식을 JSONL이나
SQLite로 바꿔도 CLI와 서비스는 그대로 둘 수 있습니다.

또한 CSV에는 외래키 제약이 없어 "없는 카테고리", "사용 중 카테고리" 같은 정합성은
**서비스 계층이 대신 지킵니다**. 이것이 저장소와 서비스를 나누는 실질적 이유입니다.

### G-03. `yield` 기반 제너레이터

```python
def stream(self) -> Iterator[Transaction]:
    with open(self.path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            yield self._to_transaction(row)
```

`readlines()` 나 `list(reader)` 는 파일 전체를 메모리에 올립니다. 거래가 10만 건이면
10만 건이 전부 올라갑니다. `yield` 는 한 건씩 꺼내 주므로 **파일 크기와 무관하게 메모리
사용량이 일정**합니다.

이 성질을 실제로 쓰는 곳이 두 군데 있습니다.

- **검색**: 걸러내기를 제너레이터 안에서 합니다. 목록으로 만든 뒤 거르면 전부 올라가지만,
  안에서 거르면 조건에 맞는 것만 밖으로 나옵니다.
- **`list --limit N`**: `deque(maxlen=N)` 에 흘려 넣어 항상 마지막 N건만 들고 있습니다.
  메모리는 N에만 비례합니다.

한계도 있습니다. **정렬은 스트리밍으로 할 수 없습니다.** 전체 순서를 알아야 하기 때문입니다.
그래서 정렬은 걸러낸 결과에만 적용합니다.

### G-04. 데코레이터로 공통 관심사 분리

`@handle_errors` `@log_call` `@measure_time` 세 개를 만들어 명령 함수마다 붙였습니다.

```python
@handle_errors
@log_call
@measure_time
def run_list(paths: DataPaths, limit: int) -> int:
    ...
```

같은 `try/except` 를 명령 12개에 복사하는 대신 한 줄을 붙입니다. 오류 출력 형식을 바꿀 때
고칠 곳이 `decorators.py` 한 군데뿐입니다.

`functools.wraps` 를 반드시 씁니다. 없으면 감싼 뒤 모든 함수 이름이 `wrapper` 가 되어
로그와 오류 메시지에서 어느 명령이었는지 알 수 없습니다.

예외를 잡는 순서에도 이유가 있습니다.

| 잡는 대상 | 종료 코드 | 이유 |
|---|---|---|
| `AppError` (검증·없는 데이터) | 1 | 사용자가 고칠 수 있는 문제 |
| `KeyboardInterrupt` / `EOFError` | 1 | 입력 취소. 저장 전이라 원본은 그대로 |
| `OSError` | 2 | 권한·디스크 문제. 사용자 입력 탓이 아님 |
| 그 밖의 `Exception` | 2 | 마지막 그물. 스택트레이스 대신 두 줄로 바꾼다 |

맨몸 `except:` 는 쓰지 않습니다. `SystemExit` 같은 제어용 예외까지 삼켜 버립니다.

### G-05. 타입 힌트

모든 공개 함수의 인자와 반환에 타입을 붙였습니다. 실제로 도움이 된 예를 듭니다.

```python
def get(self, month: str) -> Budget | None:
```

반환이 `Budget | None` 이므로 **호출부는 "없을 수도 있다"를 반드시 처리하게 됩니다.**
예산이 없는 달에 `budget.amount` 를 그냥 꺼내면 실행 중에 터지지만, 타입이 그 가능성을
미리 말해 줍니다. 그래서 요약은 예산이 없으면 예산 줄 자체를 출력하지 않습니다.

```python
tags: list[str] = field(default_factory=list)
```

`tags: list[str] = []` 로 쓰면 **모든 인스턴스가 리스트 하나를 공유합니다.** 한 거래에
태그를 추가하면 다른 거래에도 붙습니다. 파이썬의 유명한 가변 기본값 함정이며,
`field(default_factory=list)` 로 인스턴스마다 새 리스트를 만듭니다.

---

## 7. 설계 판단 기록

| 판단 | 선택 | 이유 |
|---|---|---|
| 저장 포맷 | CSV | import/export 스키마와 같아 변환 코드가 필요 없다 |
| `date` 타입 | `str` | `YYYY-MM-DD` 는 **사전순 정렬 = 시간순 정렬**이라 문자열 비교로 충분하다 |
| `amount` 타입 | `int` (읽는 즉시 변환) | 문자열로 두면 덧셈이 문자열 이어붙이기가 된다 |
| 반복 규칙 `day` | 1~28 만 허용 | 2월은 28일까지다. "말일로 당긴다" 규칙은 그 자체가 또 하나의 예외 처리 대상이 된다 |
| 반복 생성 표시 | 메모의 `[반복 RC-0001]` | 열을 늘리지 않는다. 생성된 거래는 일반 거래와 똑같이 다뤄야 한다 |
| `import` 중복 판단 | 하지 않는다 | 같은 파일을 두 번 넣으면 두 번 들어간다. 필요하면 `(date, type, category, amount, memo)` 조합으로 거른다 |
| 금액 열 정렬 | 오른쪽 | 자릿수가 맞아야 크기를 눈으로 비교할 수 있다 |
| 한글 표 정렬 | `east_asian_width` | `len()` 은 '점심'(2글자, 4칸)과 'food'(4글자, 4칸)를 같게 봐서 세로줄이 어긋난다 |

### 알려진 한계

- `list --limit N` 은 파일 뒤쪽 N건 안에서만 날짜순으로 다시 세웁니다. N보다 깊은 곳에
  과거 날짜로 끼워 넣은 거래는 목록에 잡히지 않습니다. 그럴 때는 `search` 의 기간 조건을
  씁니다.
- id 채번은 매번 파일 전체를 훑습니다. 스트리밍이라 메모리는 일정하지만 건수에 비례해
  느려집니다. 수만 건을 넘기면 마지막 id를 따로 보관하는 방식으로 바꿉니다.

---

## 8. 출처

과제 원문: `B2-1. 나만의 용돈 기입장 프로그램 만들기.txt`
리허설 질문지: `REHEARSAL.md`
설계 문서: `PRD/01_PRD.md` · `PRD/02_DATA_MODEL.md` · `PRD/03_PHASES.md` · `PRD/04_PROJECT_SPEC.md`
요구사항 추적표: `REQUIREMENTS.md` (102개)
