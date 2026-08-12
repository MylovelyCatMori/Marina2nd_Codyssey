# Mission3 단계별 가이드
## AI가 계산하는 방식을 흉내 내는 작은 계산기 -- Mini NPU Simulator

> 각 단계 완료 후 체크박스 표시. 커밋은 Conventional Commits 규칙.
> 설계 근거는 [PRD/](./PRD/) 4종 문서. 요구사항 대조표는 [PRD/04_PROJECT_SPEC.md](./PRD/04_PROJECT_SPEC.md).
> **레포**: Mission1/Mission2와 동일한 `Marina2nd_Codyssey` 단일 레포. 신규 repo 생성 없음.

---

## STEP 0: 폴더 초기 설정

**목표**: 필수 파일 배치 + 첫 커밋

### 생성 파일
- `week3-mission3/.gitattributes` -- LF 강제 (Mac 동료평가 대비)
- `week3-mission3/.gitignore` -- Python 표준
- `week3-mission3/data.json` -- 과제 제공 데이터 (수정 금지)
- `week3-mission3/PRD/` -- 설계 문서 4종
- `week3-mission3/STEPS.md` -- 이 파일

```bash
cd D:/Projects/S01-codyssey
git add week3-mission3/
git commit -m "chore: Mission3 폴더 초기 설정 및 PRD 4종 문서 추가"
git push origin master
```
- [ ] Commit #1 완료

---

## STEP 1: 상수 + Matrix 클래스

**목표**: n x n 숫자판을 저장하고 특정 위치를 읽고 쓸 수 있게 한다 (요구사항 F1)

### 구현할 것
- 상수: `BASE_DIR`, `DATA_FILE`, `EPSILON = 1e-9`, `REPEAT = 10`, `LABEL_CROSS = "Cross"`, `LABEL_X = "X"`
- 3x3 내장 상수: `BUILTIN_CROSS_3X3`, `BUILTIN_X_3X3` (data.json에 size_3이 없으므로 성능 측정용으로 내장)
- `class Matrix`
  - `__init__(rows)` -- 2차원 리스트 보관, `self.size` 계산
  - `get(r, c)` / `set(r, c, value)` -- 특정 위치 읽기/쓰기
  - `same_size_as(other)` -- 크기 일치 여부
  - `from_rows(rows)` classmethod -- 정방 여부 + 숫자 타입 검증 후 생성. 실패 시 `ValueError`

### 검증
- `Matrix.from_rows([[1,2],[3,4]]).get(1,0) == 3.0`
- `Matrix.from_rows([[1,2],[3]])` 가 `ValueError`
- `Matrix.from_rows([[1,"a"],[3,4]])` 가 `ValueError`

```bash
git add main.py
git commit -m "feat: Matrix 데이터 구조 및 상수 정의 (n x n 저장/위치별 읽기쓰기)"
```
- [ ] Commit #2 완료

---

## STEP 2: 라벨 정규화

**목표**: `+`, `x`, `cross` 를 표준 라벨 `Cross` / `X` 로 통일한다 (요구사항 F4)

### 구현할 것
- `normalize_label(raw)` -- 앞뒤 공백 제거 + 소문자 변환 후 매핑
  - `+`, `cross`, `plus` -> `Cross`
  - `x` -> `X`
  - 그 외 -> `None` (호출 측이 FAIL 처리)

### 왜 로드 시점에 한 번만 하는가
비교하는 지점마다 원본 값을 따지면 지점이 늘어날수록 빠뜨린다.
경계(파일 읽기 / 사용자 입력)에서 한 번 정규화하면 내부 코드는 두 값만 알면 된다.

### 검증
- `normalize_label("+") == "Cross"`
- `normalize_label(" X ") == "X"`
- `normalize_label("CROSS") == "Cross"`
- `normalize_label("?") is None`

```bash
git add main.py
git commit -m "feat: 라벨 정규화 함수 구현 (+/cross -> Cross, x -> X)"
```
- [ ] Commit #3 완료

---

## STEP 3: MAC 연산 + 성능 측정

**목표**: 위치별로 곱해서 전부 더한다. 외부 라이브러리 없이 (요구사항 F5, F8)

### 구현할 것
- `mac(a, b)` -- **명시적 이중 for 반복문**. `sum()` 축약이나 `zip` 사용 금지
- `measure_mac_ms(a, b, repeat=REPEAT)` -- `time.perf_counter()`로 repeat회 측정 후 평균 ms 반환
  - 측정 구간 안에 `print`, 파일 읽기 금지 (요구사항: I/O 제외)

### 검증
- 3x3 십자 필터 x 3x3 십자 패턴 = `5.0`
- 3x3 X 필터 x 3x3 십자 패턴 = `1.0`
- `measure_mac_ms(...)` 가 0보다 큰 실수 반환

```bash
git add main.py
git commit -m "feat: MAC 연산 및 반복 측정 함수 구현 (이중 반복문, 외부 라이브러리 없음)"
```
- [ ] Commit #4 완료

---

## STEP 4: 판정 로직 (epsilon)

**목표**: 점수가 거의 같으면 동점으로 본다 (요구사항 F6, F7)

### 구현할 것
- `decide(score_a, score_b, label_a, label_b, undecided_label)` 
  - `abs(score_a - score_b) < EPSILON` -> 동점 라벨 반환
  - 아니면 큰 쪽 라벨 반환
- 모드 1은 `label_a="A"`, `label_b="B"`, 동점은 `판정 불가`
- 모드 2는 `label_a="Cross"`, `label_b="X"`, 동점은 `UNDECIDED`

### 왜 `==`를 쓰면 안 되는가
`0.1`은 2진수로 정확히 표현되지 않는다. 같은 값을 더해도 **더하는 순서가 다르면** 마지막 자리가 어긋난다.
`0.9 == 0.8999999999999999`는 `False`지만, 실제로는 같은 값이다.

### 검증
- `decide(5.0, 1.0, "A", "B", "판정 불가") == "A"`
- `decide(0.9, 0.8999999999999999, ...) == "판정 불가"`

```bash
git add main.py
git commit -m "feat: epsilon(1e-9) 기반 동점 처리 판정 로직 구현"
```
- [ ] Commit #5 완료

---

## STEP 5: 자체 점검 (`--selftest`)

**목표**: STEP 1~4 코어가 맞는지 UI 없이 한 줄로 확인한다

### 구현할 것
- `run_selftest()` -- `assert` 기반. 통과 시 항목별 `[OK]` 출력
- `main()`에서 `--selftest` 인자 처리

### 검증
```bash
python main.py --selftest
# 기대: 모든 항목 [OK], 종료 코드 0
```

```bash
git add main.py
git commit -m "test: 코어 함수 자체 점검(--selftest) 추가"
```
- [ ] Commit #6 완료

---

## STEP 6: 모드 1 -- 사용자 입력 (3x3)

**목표**: 키보드로 필터 2개와 패턴을 받고, 잘못 넣어도 죽지 않게 한다 (요구사항 F2, F10-2)

### 구현할 것
- `read_matrix_line(size, row_index)` -- 한 줄 입력 + 열 개수 검증 + 숫자 파싱 검증
  - 오류 문구: `입력 형식 오류: 각 줄에 3개의 숫자를 공백으로 구분해 입력하세요.`
  - 오류 시 **그 줄만** 다시 받는다
- `read_matrix(name, size)` -- size줄 수집
- `print_matrix(title, matrix)` -- 저장 확인 출력용
- `run_manual_mode()` -- 흐름: 필터 A -> 필터 B -> **저장 확인** -> 패턴 -> MAC -> 판정 -> 3x3 성능표

### 요구사항의 실행 순서 (반드시 이 순서)
```
필터 A, B 입력 -> 저장 확인 -> 패턴 입력 -> MAC 연산 -> 결과 판정 -> 성능 분석(3x3)
```

### 검증
| 입력 | 기대 동작 |
|------|----------|
| 필터A `0 1 0`/`1 1 1`/`0 1 0`, 필터B `1 0 1`/`0 1 0`/`1 0 1`, 패턴 `1 0 1`/`0 1 0`/`1 0 1` | A=1.0, B=5.0, 판정 B |
| `1 2` | 안내 문구 후 그 줄 재입력 |
| `a b c` | 안내 문구 후 그 줄 재입력 |
| 빈 줄 | 안내 문구 후 그 줄 재입력 |
| Ctrl+C | 트레이스백 없이 안내 후 복귀 |

```bash
git add main.py
git commit -m "feat: 모드1 사용자 입력(3x3) 구현 및 행/열/숫자 검증 재입력 처리"
```
- [ ] Commit #7 완료

---

## STEP 7: 모드 2 -- data.json 로드 및 스키마 검증

**목표**: 파일을 읽고 구조를 확인한다. 망가진 데이터가 와도 프로그램이 끝까지 간다 (요구사항 F3)

### 구현할 것
- `load_data(path)` -- 구분된 오류 처리
  - 파일 없음 -> 안내 후 메뉴 복귀
  - JSON 문법 오류 -> 안내 후 메뉴 복귀
  - 최상위 `filters` / `patterns` 키 누락 -> 안내 후 메뉴 복귀
- `parse_case_size(case_id)` -- `size_{N}_{idx}`에서 N 추출. 실패 시 `None`
- `build_filter_sets(raw_filters)` -- 필터 로드 + 라벨 정규화. 손상된 크기는 건너뛰고 사유 기록

### 검증
- 정상 파일: `[OK] size_5 필터 로드 완료 (Cross, X)` 3줄
- data.json 이름 변경 후 실행: 안내 메시지 + 메뉴 복귀 (트레이스백 없음)

```bash
git add main.py
git commit -m "feat: 모드2 data.json 로드 및 스키마 검증 구현 (예외 시 프로그램 중단 없음)"
```
- [ ] Commit #8 완료

---

## STEP 8: 모드 2 -- 판정 / PASS-FAIL / 요약

**목표**: 6건을 일괄 판정하고 실패를 숨기지 않는다 (요구사항 F7, F9)

### 구현할 것
- `judge_case(case_id, raw_case, filter_sets)` -> `JudgeResult`
  - 케이스 단위 `try/except`로 예외 격리. 사유 문자열 필수
  - 크기 불일치 -> FAIL + 사유
  - expected 정규화 실패 -> FAIL + 사유
  - 필터 없음 -> FAIL + 사유
- `print_case_result(result)` -- Cross 점수 / X 점수 / 판정 / expected / PASS-FAIL
  - **동점 케이스는 소수점 이하 16자리로 펼쳐 출력** (`{0:.16f}`, 부동소수점 학습 목적)
- `print_summary(results)` -- 총 / 통과 / 실패 + 실패 케이스 식별자와 사유

### 검증 (PRD/04_PROJECT_SPEC.md 정답표 대조)
```
총 6 / 통과 3 / 실패 3
FAIL: size_5_1, size_13_2, size_25_1  (전부 "동점(UNDECIDED) 처리 규칙")
```

```bash
git add main.py
git commit -m "feat: 모드2 케이스별 판정/PASS-FAIL 출력 및 결과 요약 구현"
```
- [ ] Commit #9 완료

---

## STEP 9: 성능 분석표

**목표**: O(N^2)를 말이 아니라 실측으로 보인다 (요구사항 F8)

### 구현할 것
- `print_perf_table(entries)` -- 열: `크기(N×N)` / `평균 시간(ms)` / `연산 횟수(N^2)`
- 모드 1: 3x3 한 줄
- 모드 2: 3x3(내장) / 5x5 / 13x13 / 25x25 네 줄

### 검증
- 4행 3열 표 출력
- 25x25 시간 / 5x5 시간 비율이 대략 20~30배 (연산 횟수 비 625/25 = 25배)

```bash
git add main.py
git commit -m "feat: 크기별 성능 분석표 구현 (10회 평균, 연산 횟수 N^2 표기)"
```
- [ ] Commit #10 완료

---

## STEP 10: 메뉴 흐름 완성

**목표**: 요구사항 실행 흐름을 그대로 만든다 (요구사항 F10)

### 구현할 것
- `main()` -- 모드 선택 루프. `1` / `2` / `0`(종료). 잘못된 입력은 안내 후 재입력
- 각 모드 종료 후 메뉴 복귀
- `KeyboardInterrupt` / `EOFError` 전역 처리

### 검증
- 모드 1 -> 메뉴 -> 모드 2 -> 메뉴 -> 0 종료 연속 수행 시 오류 없음

```bash
git add main.py
git commit -m "feat: 모드 선택 메뉴 및 실행 흐름 완성"
```
- [ ] Commit #11 완료

---

## STEP 11: 검증 결과 반영 (결함 수정)

**목표**: kkirikkiri 검증 팀이 실행으로 찾아낸 결함을 고친다

> 학습 주석(LEARNING_RULES 규칙: 약어 풀기, 어원, 비유, 옵션 전부 주석)은 STEP 1~10에서
> 코드와 함께 작성한다. 주석을 나중에 몰아 다는 방식은 쓰지 않는다 --
> 왜 그렇게 짰는지는 짤 때가 가장 정확하기 때문이다.

### 수정할 것

| # | 결함 | 수정 |
|---|---|---|
| 1 | `load_data`가 `UnicodeDecodeError`를 못 잡아 **프로그램이 트레이스백으로 죽음**. data.json이 CP949(한글 Windows 메모장 기본)나 UTF-16이면 발생 | `except json.JSONDecodeError` -> `except ValueError`. 두 예외 모두 `ValueError`의 자식이라 한 줄로 덮인다 |
| 2 | `.isdigit()`가 통과시킨 `'²'`를 `int()`가 거부해 크래시. `parse_case_size`는 `sorted()` 안에서 try 바깥으로 호출되어 아무도 못 잡음 | `.isdigit()` -> `.isdecimal()` (2곳). `isdecimal()`의 참 집합이 `int()` 수용 집합과 정확히 일치 |
| 3 | `decide()` 주석이 "`==`로 비교하면 X가 이긴 것처럼 처리된다"고 서술. 실제로는 `0.9 > 0.8999999999999999`이므로 **Cross**가 이긴다 | 주석 정정 |
| 4 | 성능표 헤더가 `크기`뿐 (요구사항 문구는 `크기(N×N)`) | 헤더 변경 + 표 정렬 42열 유지 확인 |
| 5 | 요구사항의 "행 수 불일치 검증"이 코드에 없는 것처럼 보임 (실제로는 3줄 순차 요구로 구조적 보장) | `read_matrix` docstring에 근거 명시 |

### 검증
```bash
python main.py --selftest          # 전 항목 통과
printf "2\n0\n" | python main.py   # 총 6 / 통과 3 / 실패 3 (회귀 없음)
```

```bash
git add main.py
git commit -m "fix: 인코딩 예외 미포착 및 숫자 검증 결함 수정 (검증 반영)"
```
- [ ] Commit #12 완료

---

## STEP 12: README.md 완성 + 스크린샷

**목표**: 동료가 README만 보고 이해하고 인터뷰 질문을 만들 수 있는 상태

### README 필수 항목 (과제 지정 + LEARNING_RULES 대원칙)
- [ ] 프로젝트 개요
- [ ] 실행 방법 (`python main.py`, 모드 선택, data.json 위치)
- [ ] 기능 목록
- [ ] 파일 구조
- [ ] data.json 스키마 설명
- [ ] 코드 구조와 설계 의도 (왜 이렇게 나눴는지)
- [ ] 구현 요약 -- 라벨 정규화 방식 / MAC 구현 개요 / 동점 처리 정책(epsilon)
- [ ] 핵심 개념 정리 -- 과제 목표 6개 항목 전부
- [ ] 예외/에러 처리 표
- [ ] **결과 리포트** -- FAIL 원인 분석(데이터/로직/수치비교 분류) + 성능표 해석 + O(N^2) 근거, **10줄 이상**
- [ ] 재현성 -- 모드1 예시 / 모드2 총합 / 의도적 오류 입력
- [ ] 요구사항 대조표
- [ ] 실행 화면 스크린샷
- [ ] 개발 환경
- [ ] Git 사용 기록

### 스크린샷 (docs/screenshots/)
- [ ] `mode1_normal.png` -- 모드1 정상 실행
- [ ] `mode1_error.png` -- 모드1 입력 오류 재입력 유도
- [ ] `mode2_judge.png` -- 모드2 케이스별 판정
- [ ] `mode2_perf.png` -- 성능 분석표
- [ ] `mode2_summary.png` -- 결과 요약
- [ ] `selftest.png` -- `--selftest` 통과 (선택)

```bash
git add README.md TODO.md docs/ PRD/ STEPS.md
git commit -m "docs: README 완성 및 PRD/STEPS 정합성 정정"
git pull origin master     # 원격의 새 커밋을 가져와 병합한다 (필수 명령어 7종)
git push origin master
```
- [ ] Commit #13 완료

> 스크린샷은 캡처 후 별도 커밋으로 추가한다:
> `git add docs/screenshots/ && git commit -m "docs: 실행 화면 스크린샷 6장 추가"`

---

## 제출 전 최종 체크리스트

### 요구사항 대조
- [ ] [PRD/04_PROJECT_SPEC.md](./PRD/04_PROJECT_SPEC.md) 요구사항 추적표 전 항목 확인
- [ ] 예상 결과 정답표와 실제 출력 일치 (총 6 / 통과 3 / 실패 3)

### 금지사항 확인
- [ ] `import` 목록이 `json`, `os`, `sys`, `time` 뿐인가
- [ ] `mac()`이 명시적 이중 for문인가 (`sum()`/`zip()` 축약 아님)
- [ ] 점수 비교에 `==`가 없는가
- [ ] `data.json`이 수정되지 않았는가 (`git diff data.json` 비어 있음)
- [ ] `except: pass`가 없는가

### 동작 확인
- [ ] `python main.py --selftest` 전항 통과
- [ ] 모드 1 예시 입력 -> A=1.0, B=5.0, 판정 B
- [ ] 모드 1 오류 입력 3종 -> 안내 후 재입력
- [ ] 모드 2 -> 총 6 / 통과 3 / 실패 3
- [ ] data.json 숨긴 상태 실행 -> 트레이스백 없이 안내

### 제출물
- [ ] `main.py`
- [ ] `README.md` (실행 방법 + 결과 리포트)
- [ ] GitHub 저장소 URL + `week3-mission3/` 경로 병기
- [ ] 실행 화면 스크린샷 5장 이상
