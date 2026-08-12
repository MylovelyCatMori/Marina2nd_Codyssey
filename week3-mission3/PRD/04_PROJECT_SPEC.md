# Mini NPU Simulator -- 프로젝트 스펙

> AI가 코드를 짤 때 지켜야 할 규칙과 절대 하면 안 되는 것.
> 이 문서를 AI에게 항상 함께 공유한다.
> **요구사항 원본**: `D:\Projects\S01-codyssey\Week3_Mission3.txt` -- 충돌 시 원본이 최우선이다.

---

## 기술 스택

| 영역 | 선택 | 이유 |
|------|------|------|
| 언어 | Python 3.8 이상 | 요구사항 6절에 명시. `f-string`, `dict` 순서 보장 등 3.8 기능만 사용 |
| 표준 라이브러리 | `json`, `time`, `os`, `sys` | `json`=데이터 로드(요구사항 명시), `time`=성능 측정(요구사항 명시), `os`=실행 위치 무관 경로 계산, `sys`=`--selftest` 인자 처리 |
| 외부 라이브러리 | **없음** | 요구사항 6절 "외부 라이브러리 사용 금지(NumPy, pandas 등)". MAC은 반복문 직접 구현 |
| 시간 측정 함수 | `time.perf_counter()` | `time.time()`은 시스템 시계 보정에 영향받고 해상도가 낮다. `perf_counter`는 단조 증가 고해상도 카운터라 짧은 구간 측정에 적합 |
| 테스트 | `--selftest` 내장 자체 점검 | pytest는 외부 라이브러리. 제출물이 `main.py` 단일 파일이므로 내장 방식 |
| 실행 환경 | 로컬 터미널 (Windows 작업 / macOS 평가) | 동료평가가 Mac에서 이뤄지므로 줄바꿈은 `.gitattributes`로 LF 강제 |

---

## 프로젝트 구조

```
week3-mission3/
├── main.py            # 제출물 1: 실행 파일 전체 (요구사항이 단일 main.py를 요구)
├── data.json          # 과제 제공 데이터 (읽기 전용, 절대 수정 금지)
├── README.md          # 제출물 2: 실행 방법 + 구현 요약 + 결과 리포트
├── STEPS.md           # 단계별 구현 가이드 (커밋 단위)
├── .gitattributes     # LF 강제 (Mac 동료평가 호환)
├── .gitignore         # Python 표준
├── PRD/               # 설계 문서 4종 (이 폴더)
└── docs/screenshots/  # 실행 화면 캡처
```

### main.py 내부 섹션 순서

```
 1. import 및 상수          -- EPSILON, REPEAT, LABEL_CROSS/LABEL_X, DATA_FILE, 3x3 내장 데이터
 2. 예외 클래스             -- UserAbort (사용자 중단을 안전하게 되돌리기 위한 신호)
 3. Matrix 클래스           -- 데이터 구조 (요구사항 F1)
 4. 라벨 정규화             -- normalize_label (요구사항 F4)
 5. MAC 연산                -- mac, measure_mac_ms (요구사항 F5, F8)
 6. 판정                    -- decide (요구사항 F6, F7)
 7. 결과 구조 + 출력 서식   -- JudgeResult, print_section, format_score, print_matrix, print_perf_table
 8. 모드 1 (사용자 입력)    -- prompt, read_matrix_line, read_matrix, run_manual_mode
 9. 모드 2 (data.json)      -- load_data, parse_case_size, build_filter_sets, parse_filter_size,
                               judge_case, print_case_result, print_summary, run_json_mode, sort_key_for_case
10. 자체 점검               -- run_selftest
11. 진입점                 -- print_menu, main() + if __name__ == "__main__"
```

계산(3~6)과 출력(7~9)을 섹션으로 분리한다. 계산 함수는 `print`를 호출하지 않는다.
이유: 성능 측정 구간에 I/O가 섞이면 측정값이 오염된다 (요구사항 "I/O 시간을 제외하고 연산 함수 호출 구간 중심으로 측정").

---

## 절대 하지 마 (DO NOT)

- [ ] **NumPy, pandas 등 외부 라이브러리를 import하지 마** -- 요구사항 6절 명시적 금지. `pip install`이 필요한 것은 전부 금지
- [ ] **MAC을 내장 함수로 우회하지 마** -- `sum(x*y for ...)`, `math.fsum`, `zip` 축약 등으로 대체하지 말고 **명시적 이중 for 반복문**으로 구현. 요구사항 "반복문으로 직접 구현"
- [ ] **`data.json`을 수정하거나 덮어쓰지 마** -- 과제 제공 원본. 프로그램은 읽기 전용
- [ ] **원본 라벨(`+`, `x`, `cross`)로 직접 비교하지 마** -- 비교는 반드시 정규화된 `Cross`/`X`로만. 요구사항 "PASS/FAIL 비교는 표준 라벨 기준"
- [ ] **점수를 `==`로 비교하지 마** -- 반드시 `abs(a - b) < EPSILON`. 부동소수점 등가 비교는 금지
- [ ] **모드 2에서 예외로 프로그램을 죽이지 마** -- 스키마/크기 불일치는 케이스 단위 FAIL로 흡수. 요구사항 "프로그램이 비정상 종료되면 안 된다"
- [ ] **`except:` 또는 `except Exception: pass`로 오류를 삼키지 마** -- 반드시 사유 문자열을 남겨 리포트에 표시
- [ ] **실패 케이스를 통과시키려고 epsilon을 조정하지 마** -- `1e-9`는 요구사항 기준값. 동점은 동점으로 보고한다
- [ ] **성능 측정 구간에 `print`나 파일 읽기를 넣지 마** -- 측정 대상은 `mac()` 호출 구간뿐
- [ ] **하드코딩된 정답으로 PASS를 만들지 마** -- 판정은 반드시 실제 MAC 점수에서 유도
- [ ] **`✓`, `•` 같은 문자를 콘솔에 출력하지 마** -- Windows 기본 콘솔 인코딩(cp949)에서 인코딩 오류가 난다. `[OK]`, `-` 로 대체 (`×`, `→`, `─`는 cp949에 존재하므로 사용 가능)
- [ ] **모드 1 입력 오류에서 프로그램을 종료하지 마** -- 안내 문구 출력 후 해당 줄 재입력 유도

---

## 항상 해 (ALWAYS DO)

- [ ] **요구사항 추적표(아래)의 모든 항목에 구현 위치를 남길 것**
- [ ] **경계에서 검증할 것** -- 파일 로드 시점, 사용자 입력 시점에 검증. 내부 함수는 이미 검증된 값을 받는다고 가정
- [ ] **주석은 LEARNING_RULES.md 규칙을 따를 것** -- 약어 풀기(MAC = Multiply-Accumulate), 어원, 비유, 모든 옵션 주석, 격식체. week2-mission2/main.py와 동일한 밀도
- [ ] **모든 경로는 `os.path` 기준으로 계산할 것** -- `BASE_DIR = os.path.dirname(os.path.abspath(__file__))`. 어느 폴더에서 실행해도 data.json을 찾아야 한다
- [ ] **실패 사유는 사람이 읽는 한 문장으로 남길 것** -- `동점(UNDECIDED) 처리 규칙`처럼 요약본이 그대로 리포트에 실린다
- [ ] **점수는 `repr` 수준으로 보일 것** -- `0.8999999999999999`가 반올림되어 `0.9`로 보이면 부동소수점 학습 목적이 사라진다. 동점 케이스는 소수점 이하 16자리(`{0:.16f}`)로 펼쳐 출력
- [ ] **커밋은 Conventional Commits로** -- `feat:` `fix:` `docs:` `refactor:` `test:` `chore:`

---

## 요구사항 추적표 (Week3_Mission3.txt 전수 대조)

> **이 표가 이 프로젝트의 합격 기준이다.** 구현 후 각 행의 "구현 위치"를 실제 함수명으로 채우고 README에 옮긴다.

### 2절. 최종 결과물

| ID | 요구사항 | 구현 위치 | 검증 방법 |
|----|----------|----------|----------|
| R2-1 | Python 콘솔 애플리케이션 1개 | `main.py` | `python main.py` 실행 |
| R2-2 | 3x3 필터 2개 + 패턴 콘솔 입력 | `run_manual_mode()` | 모드 1 실행 |
| R2-3 | 두 필터 MAC 점수 / 연산 시간(ms) / 판정(A/B/판정 불가) 출력 | `run_manual_mode()` | 모드 1 출력 확인 |
| R2-4 | data.json에서 필터(5/13/25)+패턴 로드 후 일괄 판정 | `run_json_mode()` | 모드 2 실행 |
| R2-5 | 케이스별 판정(Cross/X/UNDECIDED) + expected 비교(PASS/FAIL) | `judge_case()` | 모드 2 출력 6줄 |
| R2-6 | 크기별 MAC 시간 측정 (최소 반복 포함) | `measure_mac_ms()` | 성능표 |
| R2-7 | 크기별 평균 시간(ms) + 연산 횟수(N^2) 표 | `print_perf_table()` | 성능표 3개 열 |
| R2-8 | 콘솔: 전체/통과/실패 + 실패 케이스 목록 | `print_summary()` | 결과 요약 |
| R2-9 | README: 실패 원인 분석 + 시간 복잡도 분석 | `README.md` "결과 리포트" | 10줄 이상 |

### 3절. 과제 목표 (README에 개념 정리 필수)

| ID | 설명할 수 있어야 하는 것 | README 위치 |
|----|------------------------|------------|
| G1 | MAC 연산이 무엇이고 AI에서 왜 중요한가 | 핵심 개념 1 |
| G2 | 곱하고 더해서 유사도를 계산하는 원리 | 핵심 개념 2 |
| G3 | data.json 키/라벨 규칙 해석과 정규화가 필요한 이유 | 핵심 개념 3 |
| G4 | 부동소수점 오차가 판정에 주는 영향, epsilon 정책 필요성 | 핵심 개념 4 |
| G5 | 크기별 시간 측정과 O(N^2) 근거 | 핵심 개념 5 |
| G6 | 실패 원인을 데이터/스키마 vs 로직 vs 수치비교로 분리 진단 | 결과 리포트 |

### 4절. 기능 요구사항

| ID | 요구사항 | 구현 위치 | 비고 |
|----|----------|----------|------|
| F1-1 | n x n 2차원 패턴/필터 저장 | `class Matrix` | |
| F1-2 | 특정 위치 값 저장/읽기 | `Matrix.get()` / `Matrix.set()` | |
| F1-3 | 최소 3/5/13/25 크기 처리 | `Matrix` + 3x3 내장 상수 | 3x3은 data.json에 없으므로 내장 |
| F2-1 | 3x3 필터 2개를 한 줄씩 공백 구분 입력 | `read_matrix()` | |
| F2-2 | 3x3 패턴 동일 방식 입력 | `read_matrix()` | |
| F2-3 | 행/열 개수 불일치, 숫자 파싱 실패 시 안내 + 재입력 | `read_matrix_line()` | 안내 문구는 요구사항 예시 문구 사용 |
| F3-1 | filters: size_5 / size_13 / size_25 로드 | `build_filter_sets()` | |
| F3-2 | patterns: `size_{N}_{idx}` 키 + input + expected 로드 | `run_json_mode()` | |
| F3-3 | 키에서 N 추출해 해당 size_N 필터 선택 | `parse_case_size()` | |
| F3-4 | 필터-패턴 크기 일치 검증 | `Matrix.same_size_as()` | |
| F3-5 | 불일치 시 케이스 FAIL + 사유 메시지, 비정상 종료 금지 | `judge_case()` try/except | |
| F4-1 | 표준 라벨 2종: Cross, X | `LABEL_CROSS`, `LABEL_X` 상수 | |
| F4-2 | expected `+`->Cross, `x`->X | `normalize_label()` | |
| F4-3 | filter 키 `cross`->Cross, `x`->X | `normalize_label()` | |
| F4-4 | 출력·PASS/FAIL 비교는 표준 라벨 기준 | `judge_case()` | |
| F5-1 | 위치별 곱 후 전체 합 | `mac()` | |
| F5-2 | 외부 라이브러리 없이 반복문 직접 구현 | `mac()` 이중 for | |
| F5-3 | 점수(float) 반환 | `mac()` 반환값 | |
| F6-1 | epsilon 기반 비교 정책 | `decide()` | |
| F6-2 | `abs(a-b) < 1e-9`이면 동점 | `EPSILON = 1e-9` | |
| F7-1 | A/B 판정, 동점은 UNDECIDED | `decide()` | 모드 1은 A/B/판정 불가로 표기 |
| F7-2 | 각 패턴에 Cross 점수 / X 점수 / 판정 출력 | `print_case_result()` | |
| F7-3 | expected와 같으면 PASS, 다르면 FAIL | `judge_case()` | |
| F8-1 | 크기별 MAC 시간 ms 단위 측정 | `measure_mac_ms()` | |
| F8-2 | 각 크기별 10회 반복 후 평균 | `REPEAT = 10` | |
| F8-3 | I/O 제외, 연산 함수 호출 구간 중심 측정 | `measure_mac_ms()` 내부에 print 없음 | |
| F8-4 | 표에 크기(NxN) / 평균 시간(ms) / 연산 횟수(N^2) | `print_perf_table()` | |
| F9-1 | 콘솔에 전체/통과/실패 출력 | `print_summary()` | |
| F9-2 | 실패 케이스 식별자 + 사유 출력 | `print_summary()` | |
| F9-3 | README 결과 리포트 10줄 이상 | `README.md` | |
| F9-4 | 실패 0개여도 왜 0인지 요약 | `README.md` | 이번 데이터는 실패 3건이므로 원인 분석 |
| F10-1 | 실행 시 모드 선택 | `main()` | |
| F10-2 | 모드1 순서: 필터A,B -> 저장 확인 -> 패턴 -> MAC -> 판정 -> 성능(3x3) | `run_manual_mode()` | "저장 확인" 출력 필수 |
| F10-3 | 모드2 순서: 필터 로드 -> 패턴 검증 -> MAC/판정/PASS-FAIL -> 성능(3x3,5,13,25) -> 요약 | `run_json_mode()` | |

### 7절. 제약 사항 / 제출물

| ID | 요구사항 | 확인 |
|----|----------|------|
| C-1 | MAC은 반복문 직접 구현 (벡터화 금지) | `mac()` 소스 확인 |
| C-2 | 모드 1 최소 검증 + 재입력 유도 | 오류 입력 테스트 |
| C-3 | 모드 2 스키마/크기 불일치에도 중단 없음 | 손상 JSON 사본 테스트 |
| C-4 | epsilon 기반 비교 | `decide()` 소스 확인 |
| C-5 | 제출물: `main.py` | 존재 |
| C-6 | 제출물: `README.md` (실행 방법 + 결과 리포트) | 존재 |
| C-7 | README: 실행 방법 / 구현 요약 / 결과 리포트 / 재현성 4개 섹션 | 목차 확인 |
| C-8 | 재현성: 모드 1 예시 입력 정상 출력 | 스크린샷 |
| C-9 | 재현성: 모드 2 PASS/FAIL 총합 일치 | 스크린샷 |
| C-10 | 재현성: 의도적 오류 입력 처리 동작 | 스크린샷 |

---

## 예상 실행 결과 (사전 계산 -- 구현 정답 대조용)

> data.json을 `Fraction` 정확 연산으로 미리 계산한 값이다. 구현 결과가 이와 다르면 구현이 틀린 것이다.

| case_id | Cross 점수 | X 점수 | 수학적 차이 | 판정 | expected | 결과 |
|---------|-----------|--------|------------|------|----------|------|
| size_5_1 | 0.9 | 0.8999999999999999 | **0 (정확히 동점)** | UNDECIDED | X | FAIL |
| size_5_2 | 8.9 | 0.1 | 8.8 | Cross | Cross | PASS |
| size_13_1 | 0.3 | 14.700000000000008 | 14.4 | X | X | PASS |
| size_13_2 | 7.499999999999997 | 7.5 | **0 (정확히 동점)** | UNDECIDED | Cross | FAIL |
| size_25_1 | 4.9 | 4.899999999999999 | **0 (정확히 동점)** | UNDECIDED | X | FAIL |
| size_25_2 | 52.9 | 0.1 | 52.8 | Cross | Cross | PASS |

**총 6 / 통과 3 / 실패 3**

동점 3건은 유리수 정확 연산(`Fraction`)으로 확인한 결과 각각 `9/10 = 9/10`, `15/2 = 15/2`, `49/10 = 49/10`로 **수학적으로 완전히 같은 값**이다.
즉 이 FAIL은 구현 버그가 아니라 **데이터가 의도적으로 동점으로 설계된 결과**이며, 부동소수점 누적 순서 차이로 마지막 자리만 어긋난 것이다.
요구사항 8절 예시 출력도 동일한 상황(`판정: UNDECIDED | expected: X | FAIL (동점 규칙)`)을 보여준다.

---

## 테스트 방법

```bash
# 자체 점검 (Phase 1 코어 검증)
python main.py --selftest

# 정상 실행
python main.py

# 모드 1 재현 입력 (십자 필터 A / X 필터 B / X 패턴)
#   1 -> 0 1 0 / 1 1 1 / 0 1 0 -> 1 0 1 / 0 1 0 / 1 0 1 -> 1 0 1 / 0 1 0 / 1 0 1
#   기대: A 점수 1.0, B 점수 5.0, 판정 B

# 모드 1 오류 입력 테스트
#   "1 2"      -> 열 개수 오류 안내 후 재입력
#   "a b c"    -> 숫자 파싱 오류 안내 후 재입력

# 모드 2 정상 실행
#   기대: 총 6 / 통과 3 / 실패 3

# 모드 2 내결함성 테스트 (원본 보존 -- 반드시 사본으로)
cp data.json data_broken.json    # 사본에서 input 행 1개 삭제 후 파일명을 data.json으로 임시 교체
#   기대: 해당 케이스만 FAIL, 나머지 정상, 트레이스백 없음
```

---

## 환경변수

없음. 이 프로그램은 환경변수, API 키, 네트워크 접근을 일절 사용하지 않는다.
`data.json` 경로만 `main.py` 위치 기준으로 자동 계산한다.

---

## [NEEDS CLARIFICATION]

- [x] 성능 측정 반복 횟수 -- 요구사항 "최소 10회". 결정: `REPEAT = 10` 상수. 늘리려면 상수만 수정
- [x] `--selftest`가 제출물 요구사항 위반인가 -- 아니다. 요구사항은 `main.py` 존재를 요구할 뿐 추가 실행 옵션을 금지하지 않으며, 기본 실행(`python main.py`)은 요구사항대로 모드 선택 메뉴로 진입한다
- [ ] 스크린샷 캡처 항목 최종 확정 -- 최소 5장(모드1 정상 / 모드1 오류 / 모드2 판정 / 성능표 / 결과 요약). 동료평가 안내에 추가 요구가 있으면 반영
