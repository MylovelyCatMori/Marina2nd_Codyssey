# 발견 사항 & 공유 자료

> 팀: kkirikkiri-analysis-0812-mission3 (Week3 Mission3 산출물 검증)
> 이전 세션(Mission2 검증) 기록은 `archive/FINDINGS-2026-08-04-mission2.md`에 보관됨.

## 이슈 보고 형식 (모든 팀원 준수)

```
### [심각도] 제목
- 파일: 경로:라인
- 증상: 무엇이 잘못됐는지
- 요구사항 근거: Week3_Mission3.txt의 어느 항목을 위반하는지 (원문 인용)
- 재현: 어떻게 확인했는지 (명령어/입력값/출력)
- 제안 수정: 구체적으로
```

심각도 기준:
- **CRITICAL**: 요구사항 명시 위반, 계산 오류, 프로그램 중단 -- 제출 불가
- **HIGH**: 동료평가에서 지적당할 사실 오류/누락 -- 수정 필요
- **MEDIUM**: 개선하면 좋음
- **LOW**: 취향/스타일

**추측 금지**: 모든 이슈는 실제 실행 결과나 파일 인용으로 뒷받침한다. "그럴 것 같다"는 보고하지 않는다.

---

# T1 요구사항 전수 대조 (req-auditor, 2026-08-12)

**결론: CRITICAL 0건 / HIGH 0건.** 추출 항목 124개 중 PASS 120, 판단보류 1, N/A 3.
핵심 제약 8종(외부라이브러리·MAC반복문·epsilon·라벨정규화4종·성능표3열·케이스단위FAIL·모드1재입력·README리포트) 전부 충족.

### [MEDIUM] 모드 1에 "행 수 불일치" 검증 경로가 존재하지 않음

- 파일: `week3-mission3/main.py:596-607` (`read_matrix`), `main.py:547-593` (`read_matrix_line`)
- 증상: `read_matrix`가 `for row_index in range(size)`로 정확히 3회만 입력받으므로 행 수는 항상 3이다.
  `Matrix.from_rows`의 행 검증(`main.py:206` 빈 행, `main.py:216` 정사각형)은 모드 1 경로에서 절대 발동하지 않는다.
  즉 사용자에게 "행 수가 틀렸다"는 안내가 출력될 수 있는 경로가 없다.
- 요구사항 근거: Week3_Mission3.txt 90행 "행 수/열 수 불일치, 숫자 파싱 실패 시 안내 문구를 출력하고 재입력을 유도해야 한다",
  153행 "모드 1 입력은 "행/열 개수, 숫자 파싱" 최소 검증을 수행하고, 오류 시 재입력을 유도한다"
- 반론(제출 가능 근거): 요구사항이 스스로 제시한 예시 문구가 91행 "입력 형식 오류: 각 줄에 3개의 숫자를 공백으로 구분해 입력하세요."
  로 **줄 단위(열 수) 검증**을 가리키고, 8절 예시(190-198행)도 "필터 A (3줄 입력, 공백 구분)"로 줄 단위 프롬프트를 전제한다.
  한 줄에 9개를 몰아 넣어도 `main.py:570` 열 수 검증에 걸린다. 사용자가 행 수를 틀릴 방법 자체가 없다.
- 재현: `main.py:602-603` 확인. `read_matrix`는 항상 `len(rows) == size`인 리스트를 만든다.
- 제안 수정(코드 변경 불필요): README 10절 표 또는 `read_matrix` docstring에 한 줄 추가.
  "행 수는 프로그램이 3줄을 순차 요구하므로 구조적으로 불일치가 발생하지 않고, 열 수/파싱은 줄 단위로 검증한다."
  동료평가자가 "행 수 검증은 어디 있나"를 물었을 때 답이 문서에 있어야 한다.

### [LOW] 성능표 헤더가 "크기"뿐 (요구사항 문구는 "크기(N×N)")

- 파일: `main.py:512`
- 요구사항 근거: 124행 "표에는 "크기(N×N) / 평균 시간(ms) / 연산 횟수(N²)"가 포함되어야 한다"
- 판정: 값 열이 `3x3`/`25x25` 형태(`main.py:517`)로 N×N을 그대로 표기하고,
  173행 "아래는 정답이 아니라 참고 예시다. 실제 문구와 디자인은 달라도 된다"가 적용되므로 위반 아님. 참고용 기록.

### [LOW] 문서-코드 불일치 2건 (doc-verifier 영역, 교차 참고용)

- `README.md:80`이 `DATA_FILE`을 `main.py:36`이라 표기. 실제는 `main.py:54`.
- `PRD/01_PRD.md:145`가 3x3 내장 상수를 "모드 1의 기본 예시로도 재사용한다"고 서술.
  실제 `BUILTIN_CROSS_3X3`/`BUILTIN_X_3X3` 사용처는 `main.py:992-993`(모드 2 성능측정), `main.py:1068-1069`(selftest)뿐.
  모드 1은 항상 사용자 입력을 받는다. 요구사항 위반은 아니나 문서 주장이 코드와 다르다.

### 보너스 제외의 정당성 -- 위반 아님 확인

- 원문 137행 "5. 보너스 과제 (선택)". "(선택)"이 원문에 명시되어 있으므로 제외는 요구사항 위반이 아니다.
- 단, 5절이 4절 뒤에 배치된 편집 오류가 있음(원문 112행에 "6. 점수 비교 정책"이 4절 내부에 먼저 등장).
  절 번호 순서와 무관하게 내용 기준으로 전수 대조했다.

---

# T2 코드 정확성 및 예외 처리 검증 (code-verifier, 2026-08-12)

**결론: CRITICAL 0건 / HIGH 1건 / MEDIUM 1건 / LOW 4건.**
실행 시나리오 62개(모드1 20 + 모드2 36 + 인코딩/유니코드 6) 중 60개 무사, 2개 트레이스백 크래시.
정답표 6건은 `fractions.Fraction` 정확 연산으로 독립 재계산하여 **전건 일치**(6/3/3).
원본 `data.json` 무결성 확인: sha256 `1d5dc0f7...58d8c3e4` 검증 전후 동일.

### [HIGH] `load_data`가 `UnicodeDecodeError`를 못 잡아 모드 2가 트레이스백으로 죽는다

- 파일: `week3-mission3/main.py:685-697`
- 증상: `except json.JSONDecodeError` / `except OSError` 두 개만 잡는다.
  `UnicodeDecodeError`는 `ValueError`의 하위 클래스이고 `OSError`가 **아니므로**(실측 확인) 어느 쪽에도 걸리지 않는다.
  data.json이 UTF-8이 아닌 인코딩(CP949 = 한글 Windows 메모장 기본, UTF-16, 깨진 바이트 1개)이면
  `main.py:690` `json.load()`에서 예외가 그대로 위로 올라가 프로그램이 트레이스백을 뿜고 종료된다.
- 요구사항 근거: Week3_Mission3.txt 101행 "불일치 시, 해당 케이스를 FAIL로 처리하고 원인을 메시지로 남겨야 한다
  (프로그램이 비정상 종료되면 안된다)", 154행 "모드 2에서 스키마/크기 불일치가 발생해도 프로그램이 중단되지 않도록 처리한다"
- 문서 모순: `README.md:451` "**모드 2에서는 어떤 오류도 프로그램을 중단시키지 않는다.**" -- 이 주장이 반증된다.
- 재현:
  ```bash
  mkdir -p /c/Users/kimyh/AppData/Local/Temp/claude/m3enc && cd /c/Users/kimyh/AppData/Local/Temp/claude/m3enc
  cp "D:/Projects/S01-codyssey/week3-mission3/main.py" .
  python -c "import json;d={'filters':{'size_3':{'cross':[[0,1,0],[1,1,1],[0,1,0]],'x':[[1,0,1],[0,1,0],[1,0,1]]}},'patterns':{'size_3_1':{'input':[[0,1,0],[1,1,1],[0,1,0]],'expected':'+','note':'십자가'}}};open('data.json','wb').write(json.dumps(d,ensure_ascii=False).encode('cp949'))"
  printf "2\n0\n" | python main.py
  ```
- 실제 출력:
  ```
    File "<frozen codecs>", line 325, in decode
  UnicodeDecodeError: 'utf-8' codec can't decode byte 0xbd in position 206: invalid start byte
  ```
  (UTF-16 저장, 잘못된 바이트 `0xFF` 삽입 케이스도 동일하게 크래시. UTF-8 BOM은 정상 처리됨)
- 제안 수정 (1글자 수준): `main.py:692`
  `except json.JSONDecodeError as error:` -> `except ValueError as error:`
  `JSONDecodeError`와 `UnicodeDecodeError` 둘 다 `ValueError` 하위이므로 한 줄로 양쪽을 덮는다(실측 확인).
  메시지는 "data.json을 읽을 수 없습니다(인코딩 또는 JSON 형식 오류): {error}"처럼 넓히면 정확해진다.

### [MEDIUM] `.isdigit()`가 통과시키는 유니코드 숫자를 `int()`가 거부해 크래시

- 파일: `main.py:725`+`main.py:732` (`parse_case_size`), `main.py:814`+`main.py:817` (`parse_filter_size`)
- 증상: `'²'`(U+00B2), `'⁵'`(U+2075)는 `isdigit()`가 `True`인데 `int()`는 `ValueError`를 낸다(실측).
  `parse_case_size`는 `run_json_mode`의 `sorted(..., key=sort_key_for_case)`(`main.py:981`)에서
  try 블록 **바깥**으로 호출되므로 아무도 잡지 않는다. 스키마 오류가 프로그램을 중단시킨다.
- 요구사항 근거: 154행 "모드 2에서 스키마/크기 불일치가 발생해도 프로그램이 중단되지 않도록 처리한다"
- 재현: 임시폴더에 main.py 복사 후 data.json의 패턴 키를 `size_²_1`(또는 필터 키를 `size_²`)로 저장하고 `printf "2\n0\n" | python main.py`
- 실제 출력: `ValueError: invalid literal for int() with base 10: '²'` (main.py:732 / main.py:817)
- 제안 수정: `isdigit()` -> `isdecimal()` (두 곳). `isdecimal()`의 참 집합이 `int()`가 받는 집합과 정확히 일치함을 실측 확인
  (`'3'`/`'٣'`/`'༤'` 통과+int OK, `'²'`/`'⁵'` 차단).
- 현실성: 채점용 원본 data.json에는 해당 키가 없어 제출 실행에는 영향 없음. 그래서 CRITICAL이 아니라 MEDIUM.

### [LOW] NaN/Infinity가 조용히 통과해 판정이 항상 X(뒤쪽 라벨)로 쏠린다

- 파일: `main.py:229` (`Matrix.from_rows` 숫자 검증), `main.py:419-425` (`decide`)
- 증상: 파이썬 `json`은 표준 JSON에 없는 `NaN`/`Infinity` 리터럴을 기본으로 허용한다.
  `isinstance(float('nan'), float)`가 True라 검증을 통과하고, `mac()` 결과가 `nan`이 된다.
  `decide`는 `nan < EPSILON` False, `nan > nan` False -> 무조건 `label_b`(=`X`)를 돌려준다.
  모드 1도 `float('nan')`/`float('inf')` 토큰을 그대로 받는다(`main.py:580`).
- 재현: 임시폴더 data.json에 `"input":[[NaN,1,0],[1,1,1],[0,1,0]]` -> 출력 `판정: X | expected: Cross | FAIL (판정(X)과 expected(Cross) 불일치)`
  모드 1: `printf "1\nnan 1 0\n1 1 1\n0 1 0\n1 0 1\n0 1 0\n1 0 1\n1 0 1\n0 1 0\n1 0 1\n0\n" | python main.py`
- 판정: 프로그램이 죽지 않고 FAIL로 보고하므로 요구사항 위반은 아님. 다만 "사유가 실제 원인(비수치 데이터)을 가리키지 않는다".
- 제안 수정(선택): `main.py:229` 검증에 `value != value or value in (float('inf'), float('-inf'))` 거부 추가. 요구사항 밖이므로 미수정도 무방.

### [LOW] 같은 표준 라벨로 정규화되는 필터 키가 둘이면 조용히 덮어쓴다

- 파일: `main.py:769-777` (`build_filter_sets`)
- 증상: `LABEL_MAP`은 `'+'`,`'cross'`,`'plus'`를 모두 `Cross`로 보낸다. 한 size 안에 `cross`와 `plus`가 동시에 있으면
  `loaded['Cross']`가 경고 없이 뒤쪽 값으로 덮인다. Cross/X가 둘 다 채워지면 아무 메시지도 남지 않는다.
- 재현: `{"size_3":{"cross":C3,"plus":X3,"x":X3}}` -> `[OK] size_3 필터 로드 완료`만 출력되고 cross가 X3로 바뀐 채 판정됨.
- 판정: 원본 data.json은 `cross`/`x` 한 쌍뿐(실측)이라 제출 실행에는 영향 없음.

### [LOW] `sort_key_for_case`의 idx 정렬이 문자열 사전순

- 파일: `main.py:1025` (`return (size, case_id)`)
- 증상: 같은 크기 안에서 `size_5_10`이 `size_5_2`보다 앞에 온다(실측:
  `['size_3_1','size_5_10','size_5_2','size_13_1','size_25_1','size_100_1','bad_key']`).
- 판정: 원본 data.json은 idx가 1,2뿐이라 영향 없음. 크기 정렬 자체는 정확히 동작.

### [LOW] `prompt()` 바깥 구간의 Ctrl+C는 여전히 트레이스백

- 파일: `main.py:538-544`
- 증상: `input()` 대기 중 Ctrl+C는 `UserAbort`로 변환되지만, MAC 연산/성능 측정 중(`main.py:994-1001` 등) Ctrl+C는 잡히지 않는다.
- 판정: 요구사항의 "비정상 종료 금지"는 데이터/스키마 오류 문맥이므로 위반 아님. 참고용.

### 검증 완료 -- 결함 없음으로 확인한 항목

| 점검 항목 | 결과 |
|---|---|
| 정답표 6건 실측 | **전건 일치**. Fraction 정확연산 판정과 float 판정이 6/6 동일 |
| `mac()` 손계산 3x3 | 십자x십자=5.0, 십자xX=1.0, XxX=5.0. 별도 수기 이중루프 기준값과 일치 |
| `decide()` epsilon | `<` 사용(`<=` 아님). 차이 정확히 `1e-9`면 동점 아님 -> 요구사항 문구 `abs(a-b) < 1e-9`와 정확히 동일 |
| `measure_mac_ms` I/O 배제 | 함수 본문에 `print`/`open`/`json` 전무(소스 검사). `mac()` 호출만 계측 |
| `format_score(None)` | `'-'` 반환. `expand=True`에서도 안전 |
| `judge_case` expected가 dict/list/int/None/bool | 5종 전부 `ERROR`+FAIL, 예외 누출 없음 |
| `build_filter_sets`의 `parse_filter_size(k) or 0` 정렬 | None 반환 키가 섞여도 크래시 없음(int끼리 비교). `or 0` 안전 |
| `Matrix.set()` | 프로덕션 경로에서는 미사용. `main.py:1045` selftest가 유일 호출자.
요구사항 F1 "특정 위치의 값을 저장하고 읽어올 수 있어야 한다"가 존재를 요구하고 selftest가 실제로 검증하므로 죽은 코드 아님 |
| `except: pass` 조용한 삼킴 | **없음**. try/except 8쌍 전부 구체 예외 지정. `main.py:1054` `except ValueError: pass`는 selftest의 "예외가 나야 정상" 단언 |
| `read_matrix_line` 무한루프 | EOF에서 `prompt()`가 `UserAbort`를 던져 while을 탈출, `run_manual_mode`가 잡아 메뉴 복귀(실측 #13) |
| 성능표 열 정렬(한글 2칸) | 헤더/구분선/값 줄 **전부 42 표시열**로 일치. 한글 폭 때문에 깨지지 않음 |
| 성능 재현성 3회 | 3회 모두 6/3/3 동일. 셀당 시간 478/476/407/366 ns로 크기 무관하게 평탄(증가 아님) -> O(N²) 주장 성립 |

---

# T3 문서 사실 오류 및 주석 품질 검증 (doc-verifier, 2026-08-12)

**결론: CRITICAL 0 / HIGH 5 / MEDIUM 5 / LOW 9.**
라인번호 참조 74건 대조(정확 67 / 오류 3 / 범위끝 부정확 4). 수치 주장 21건 검산(정확 20 / 과일반화 1).
사실 주장 14건 코드 대조(참 12 / 거짓 2). 학습 주석에 **틀린 설명 1건** 발견.

### [HIGH] "X가 이긴 것처럼 처리된다"는 서술이 사실과 반대 (README + main.py 주석 동시)

- 파일: `README.md:389`, `main.py:409`
- 문서 주장: "`==`로 비교하면 "다르다"가 되어 **X가 이긴 것처럼** 처리된다. 이건 사실 왜곡이다."
- 실제: Cross=0.9, X=0.8999999999999999. `0.9 > 0.8999999999999999` -> **True**.
  epsilon 없이 단순 대소 비교하면 이기는 쪽은 **Cross**다. `decide()`의 `if score_a > score_b: return label_a` 경로.
- **README 자기모순**: `README.md:517`은 정반대로 올바르게 서술한다 --
  "만약 `==` 대신 단순 대소 비교만 했다면 `0.9 > 0.8999999999999999`이므로 **Cross가 이겼다고** 판정했을 것이다."
  같은 문서 안에서 128줄 떨어진 두 문장이 충돌한다. 9절은 "인터뷰에서 그대로 답할 수 있는 수준"으로 쓴 핵심 개념 섹션이라 노출도가 가장 높다.
- 재현: `python -c "print(0.9 > 0.8999999999999999)"` -> `True`
- 제안 수정 (README.md:389, 그대로 교체):
  `` `==`로 비교하면 "다르다"가 되어 Cross가 이긴 것처럼 처리된다. **이건 사실 왜곡이다.** 실제로는 어느 쪽도 이기지 않았다. ``
- 제안 수정 (main.py:409, 그대로 교체):
  `      == 로 비교하면 "다르다"가 되어 Cross가 이긴 것처럼 처리된다. 이는 사실 왜곡이다.`

### [HIGH] `meta.version`을 "출력만 한다"고 적었으나 코드는 meta를 전혀 참조하지 않는다

- 파일: `README.md:189`, `PRD/02_DATA_MODEL.md:153`
- 문서 주장: "`meta.version`은 출력만 하고 검증에 사용하지 않는다."
- 실제: `main.py` 전체에 `meta`/`version` 문자열이 **0회** 등장한다. 출력도 검증도 하지 않는다.
- 재현: `Grep "meta|version" main.py -i` -> No matches found
- 제안 수정 (README.md:189, 그대로 교체):
  `` `meta`는 읽지도 검증하지도 않는다. 과제에 버전 분기 규칙이 없는데 임의 규칙을 만들면 정상 데이터를 거부할 위험이 있고, 출력해도 판정에 기여하지 않기 때문이다. 프로그램이 요구하는 최상위 키는 `filters`와 `patterns` 둘뿐이다(`main.py:702`). ``
- PRD/02:153도 같은 문장이므로 "결정: **읽지 않는다**(검증도 출력도 하지 않는다)"로 동일 수정.

### [HIGH] `DATA_FILE` 라인번호 오류 -- `main.py:36`은 빈 줄

- 파일: `README.md:80`
- 문서 주장: "(`main.py:36` `DATA_FILE`)"
- 실제: `DATA_FILE = os.path.join(BASE_DIR, 'data.json')`은 **`main.py:54`**. 36행은 빈 줄이다.
- 제안 수정: `main.py:36` -> `main.py:54`

### [HIGH] `LABEL_CROSS`/`LABEL_X` 라인번호 오류 -- 76~77행은 주석

- 파일: `README.md:635` (13절 기능 요구사항 표)
- 문서 주장: "| 표준 라벨 Cross / X | O | `LABEL_CROSS`, `LABEL_X` (76~77) |"
- 실제: `LABEL_CROSS = 'Cross'`는 **73행**, `LABEL_X = 'X'`는 **74행**. 76~77행은 표준 라벨 설명 주석이다.
- 제안 수정: `(76~77)` -> `(73~74)`

### [HIGH] README 14절이 참조하는 스크린샷 6장이 실제로 존재하지 않는다

- 파일: `README.md:678-691`, `docs/screenshots/`
- 문서 주장: `mode1_normal.png` / `mode1_error.png` / `mode2_judge.png` / `mode2_perf.png` / `mode2_summary.png` / `selftest.png`
- 실제: `docs/screenshots/` 디렉터리가 **비어 있다**(`ls -la` 확인).
- 규칙 근거: `S01-codyssey/LEARNING_RULES.md` README 필수 섹션 10번 "실행 화면 스크린샷 -- 기능별 캡처",
  `PRD/04_PROJECT_SPEC.md:229` "최소 5장", `STEPS.md:322-328` 체크리스트.
- 제안: 캡처 후 배치. 캡처 전이면 14절 표에 `(캡처 예정)` 명시. 현재 상태로 제출하면 필수 섹션 1종 미충족이다.

### [MEDIUM] README가 존재하지 않는 "행 수 불일치" 검증을 있다고 주장

- 파일: `README.md:100`("행/열 개수 불일치"), `README.md:630`("행/열 개수, 숫자 파싱 검증")
- 실제: `read_matrix_line`(`main.py:547`) docstring 자체가 "열 개수 불일치 / 숫자 파싱 실패" 두 가지만 명시한다(`main.py:551-552`).
  `read_matrix`(`main.py:602`)가 `for row_index in range(size)`로 정확히 3줄만 받으므로 행 수 불일치 경로가 없다.
- req-auditor의 MEDIUM과 동일 사안이며, **문서 쪽 표현이 코드보다 넓게 적혀 있다**는 점이 추가 문제다.
- 제안 수정 (README.md:100 우측 열에 추가):
  `행 수는 프로그램이 3줄을 순차 요구하므로 구조적으로 불일치가 생기지 않는다. 검증 대상은 줄 단위 열 개수와 숫자 파싱이다.`

### [MEDIUM] "17자리" vs "16자리" -- PRD/STEPS와 README·코드가 어긋난다

- 파일: `PRD/04_PROJECT_SPEC.md:80`("동점 케이스는 **17자리**로 출력"), `STEPS.md:225`("동점 케이스는 **17자리**로 출력")
- 실제: `format_score`는 `'{0:.16f}'.format(value)`(`main.py:478`) -- 소수점 이하 **16자리**.
  출력 실측 `0.9000000000000000`(소수점 16자리). README(`:319`, `:777`)는 "16자리"로 정확하다.
- 제안 수정: PRD/04:80과 STEPS.md:225의 `17자리` -> `소수점 이하 16자리`

### [MEDIUM] `PRD/04_PROJECT_SPEC.md:39-49` 섹션 순서가 실제 main.py와 다르다

- 문서 주장: 1 상수 / 2 Matrix / 3 라벨정규화 / 4 MAC / 5 판정 / 6 출력서식 / 7 모드1 / 8 모드2 / 9 자체점검 / 10 진입점
- 실제(`# ===` 배너 기준): 1 import·상수(22) / 2 예외클래스 UserAbort(136) / 3 Matrix(158) / 4 라벨정규화(295) /
  5 MAC·성능측정(318,354) / 6 판정(389) / 7 JudgeResult+출력서식(437) / 8 모드1(529) / 9 모드2(669) / 10 자체점검·진입점(1036,1132)
  -> `UserAbort`와 `JudgeResult` 두 섹션이 PRD 목록에 없다. README 7절 표는 실제와 일치한다.
- 파생 오류: `PRD/04:51` "계산(2~5)과 출력(6~8)을 섹션으로 분리한다"의 번호도 실제와 어긋난다.
- 제안: PRD/04:39-49를 README 7절 표와 같은 10개 항목으로 교체하고, 51행을 "계산(3~6)과 출력(7~9)"로 수정.

### [MEDIUM] `PRD/03_PHASES.md:34`가 `STEPS.md:46` 및 실제 코드와 모순

- PRD/03:34 "`Matrix.from_rows([[1,2],[3]])` 가 **예외가 아닌 검증 실패를 반환**"
- STEPS.md:46 "`Matrix.from_rows([[1,2],[3]])` 가 `ValueError`"
- 실제: `ValueError: 정사각형이 아닙니다. 행 수=2, 2번째 행의 열 수=1` -- **예외를 던진다**(실측).
- 제안 수정 (PRD/03:34): `` - [ ] `Matrix.from_rows([[1,2],[3]])` 가 `ValueError`를 던지고, 호출 측이 이를 케이스 단위 FAIL로 흡수한다 ``

### [MEDIUM] README 16절 Git 명령어 6종 + 브랜치 전략 누락

- 파일: `README.md:748-757`
- 규칙 근거: `LEARNING_RULES.md` 필수 섹션 12 "Git 사용 기록 -- 사용한 명령어 **7종** + **브랜치/커밋 전략**",
  섹션별 상세 규칙 "Git 기록 | ... + **브랜치 전략** + 커밋 메시지 컨벤션"
- 실제: `git add` / `commit` / `push` / `status` / `log` / `diff` = **6종**. 브랜치 전략 서술 없음(저장소 전략만 있음).
- 제안 수정 (README.md:757 뒤에 추가):
  ```bash
  git branch                       # 현재 브랜치 목록과 작업 중인 브랜치를 확인한다
  ```
  그리고 16절에 소제목 추가:
  `### 브랜치 전략` / `` 솔로 작업이므로 `main` 하나만 유지한다. 미션 단위 작업은 규모가 작고 되돌릴 지점이 커밋으로 충분히 확보되므로 `feature/` 브랜치를 만들지 않았다 (`D:\Projects\CLAUDE.md` 5항 "솔로: develop/staging 불필요"). ``

### [LOW] 9건

1. `README.md:316` "`==`는 **어디에도 사용하지 않는다**" -- 판정 경로에는 없으나 selftest `main.py:1070-1072`에
   `assert mac(cross, cross) == 5.0` 등 float `==`가 3곳 있다. 정확한 표현은 "**점수 비교(판정)에는** 어디에도 사용하지 않는다".
2. `README.md:199,205,206,207` 섹션 범위 끝값이 다음 섹션 배너 안쪽을 가리킨다.
   `22~124` -> `22~125`, `437~527` -> `437~522`, `529~666` -> `529~662`, `669~1033` -> `669~1026`.
3. `README.md:521` "Cross 필터의 중앙값이 `1.0`이 아니라 `0.9`이고 X 필터 전체가 `0.1`" -- **size_5에만 해당**.
   실측: size_13 cross 중앙=0.3, size_13 x 중앙=7.5, size_25 cross 중앙=4.9. "`size_5_1`의 경우"로 한정 필요.
4. `README.md:577` 모드 1 "기대 출력"에 `연산 시간(평균/10회): 0.0031 ms`가 단정형으로 박혀 있다. 실측 재현 시 0.0026 ms.
   `연산 시간(평균/10회): 0.00xx ms  (장비마다 다름)`로 완화 권장. A=1.0 / B=5.0 / 판정 B는 실행으로 **일치 확인**.
5. `PRD/01_PRD.md:120` "(`json`, `os`, `time`만 사용)" -- `sys` 누락. 실제 4개(`main.py:22,26,30,33`). README·PRD/04·STEPS는 4개로 정확.
6. `PRD/01_PRD.md:119` "25x25 / 5x5 시간비가 대략 **25배** 근방" -- 실측 20.6배(README표) / 22.6배(재실행).
   README 11-3이 "시간은 연산 횟수보다 덜 늘어난다(69.4배 vs 45.4배)"고 정확히 설명하는 것과 방향이 어긋난다.
   `STEPS.md:253`의 "대략 20~30배"가 정확한 표현이다.
7. `PRD/04_PROJECT_SPEC.md:13` "`f-string`, `dict` 순서 보장 등 3.8 기능만 사용" -- main.py에 f-string **0개**, `.format()` 56회.
   (f-string은 3.6, dict 순서 보장은 3.7 기능이기도 하다.)
8. `PRD/02_DATA_MODEL.md:115-122` JudgeResult 필드 표에 `expected`가 빠져 있다(실제 7필드: case_id, score_cross, score_x, verdict, expected, passed, reason).
9. `README.md:124-128` 파일 구조 트리가 `PRD/`를 4개 파일로만 표기. 실제로는 `PRD/README.md`가 더 있다(총 5개).

### 라인번호 대조 결과 (74건)

| 구분 | 건수 | 결과 |
|---|---|---|
| README 명시 `main.py:N` | 33 | 32 일치 / **1 불일치(`main.py:36`)** |
| README 7절 섹션 표 | 16 | 12 일치 / 4 범위끝 부정확 |
| README 13절 대조표 괄호 | 25 | 23 일치 / **2 불일치(76,77)** |
| STEPS.md | 0 | 라인 참조 없음 |
| PRD 4종 | 0 | 라인 참조 없음(함수명만 사용, 함수명은 전부 실제와 일치) |

`PRD/04_PROJECT_SPEC.md` 요구사항 추적표의 구현 위치 함수명 **44개 전부** 실제 main.py에 존재하며 이름이 일치한다.

### 수치 검산 결과 (21건, 오류 0)

| 주장 | 검산 | 결과 |
|---|---|---|
| main.py 1173줄 | `wc -l` = 1173 | 일치 |
| 유리수 정확값 9/10, 15/2, 49/10 | `Fraction` 재계산 -> size_5_1 9/10=9/10, size_13_2 15/2=15/2, size_25_1 49/10=49/10 | 일치 |
| 6건 점수/판정/expected 표 (11-1) | 실행 출력과 12개 값 전부 문자 단위 일치 | 일치 |
| 총 6 / 통과 3 / 실패 3 | 실행 확인 | 일치 |
| 차이 1.1e-16 | `0.9-0.8999999999999999` = 1.1102230246251565e-16 | 일치 |
| 셀당 0.00032/0.00026/0.00023/0.00021 | 0.0029/9, 0.0064/25, 0.0392/169, 0.1316/625 = 0.000322/0.000256/0.000232/0.000211 | 일치 |
| 연산 배수 2.8/18.8/69.4 | 25/9, 169/9, 625/9 = 2.778/18.778/69.444 | 일치 |
| 시간 배수 2.2/13.5/45.4 | 0.0064/0.0029, 0.0392/0.0029, 0.1316/0.0029 = 2.207/13.517/45.379 | 일치 |
| 25x25=625회, 3x3 대비 69배 | 625/9 = 69.4 | 일치 |
| 224x224에 3x3 필터 64개 = 약 2,900만 MAC | 224*224*9*64 = **28,901,376** (valid conv 222²면 28,387,584) | 일치 |
| 한 층 약 6초 / 50층 5분 | 28,901,376 x 0.0002ms = 5,780ms = 5.78초. 6x50 = 300초 = 5분 | 일치 |
| cp949: `✓`(U+2713) 없음, `×`(U+00D7) 있음 | `.encode('cp949')` -> ✓ 실패 / • 실패 / × 성공 | 일치 |
| PRD/04:68 `→`,`─`도 cp949 사용 가능 | U+2192 성공 / U+2500 성공 | 일치 |
| PRD/02:74-79 size_5 필터 25칸 값 | data.json 원본과 50칸 전부 일치 | 일치 |
| 모드 1 A=1.0 B=5.0 판정 B | 실제 입력 주입 실행 | 일치 |
| 성능표 절대값(0.0029/0.0064/0.0392/0.1316) | 재실행 0.0022/0.0048/0.0287/0.1085 | 장비 의존. README:555가 변동성을 명시하므로 허위 아님 |

### 사실 주장 코드 대조 (14건)

| 주장 | 검증 방법 | 결과 |
|---|---|---|
| import는 json/os/sys/time 4개뿐 | 정규식 스캔 -> `main.py:22,26,30,33` | **참** |
| 점수 비교에 `==` 없음 | 전 라인 `==` 추출 -> 판정 경로 `main.py:885,889,902,908`은 전부 라벨/문자열 비교 | **참**(selftest 예외는 LOW 1) |
| `except: pass` 없음 | bare except 0건. `pass`는 `main.py:138` UserAbort 본문 1건 | **참** |
| 계산 함수는 print를 호출하지 않음 | AST로 mac/decide/measure_mac_ms/normalize_label/format_score/parse_*/sort_key + Matrix 5메서드 검사 -> **전부 0회** | **참** |
| 동점일 때만 16자리로 펼침 | `format_score(expand=)` 호출 4곳: `main.py:651,652`(is_tie), `910,911`(verdict==UNDECIDED) | **참** |
| 출력 순서 크기 오름차순 고정 | `main.py:981` `sorted(..., key=sort_key_for_case)` | **참** |
| Python 3.8 호환 | AST 검사: walrus/match/`dict\|`/`list[int]`/타입힌트/f-string **전부 0건**, `.format()` 56회 | **참** |
| PASS/FAIL은 `verdict == expected` 한 줄 | `main.py:885` `passed = (verdict == expected)` | **참** |
| 로드 시점 1회 정규화 | `main.py:771`(필터 키), `main.py:864`(expected) | **참** |
| LABEL_MAP 4매핑 | 실행 확인 `{'+':'Cross','cross':'Cross','plus':'Cross','x':'X'}` -- README 8-1 코드 인용과 문자 단위 일치 | **참** |
| PRD/02:154 bool 거부 | `Matrix.from_rows([[True,False],[False,True]])` -> `ValueError: 1행 1열의 값이 숫자가 아닙니다: True` | **참** |
| 내결함성 실측 7종(README 10절) | 임시 사본 7종 전부 재현. 원본 data.json 미변경 | **7/7 참** |
| `meta.version` 출력만 함 | `main.py`에 meta/version 0회 | **거짓 (HIGH 2)** |
| `==`면 X가 이긴다 | `0.9 > 0.899...9` = True -> Cross | **거짓 (HIGH 1)** |

### LEARNING_RULES 필수 섹션 13종 점검

| # | 섹션 | 상태 | README 위치 |
|---|---|---|---|
| 1 | 프로젝트 개요 | O | 1절 |
| 2 | 주제/선정 이유 | O | 2절 (지정 과제라 "미션 배경"으로 대체) |
| 3 | 실행 방법 | O | 3절 |
| 4 | 기능 목록 | O | 4절 |
| 5 | 파일 구조 | O | 5절 (PRD/README.md 1개 누락 -- LOW 9) |
| 6 | 데이터/설정 파일 설명 | O | 6절 (스키마·경로·역할·인코딩 4항 전부) |
| 7 | 코드 구조와 설계 의도 | O | 7절 |
| 8 | 핵심 개념 정리 | O | 9절 (과제 목표 6항 전부) |
| 9 | 예외/에러 처리 | O | 10절 (17행 표 + 내결함성 실측 7종) |
| 10 | 실행 화면 스크린샷 | **X** | 14절 표만 존재, 파일 0개 (HIGH 5) |
| 11 | 개발 환경 | △ | 15절 있음. 규칙이 요구하는 "스크린샷"은 없음 |
| 12 | Git 사용 기록 | △ | 16절. 명령어 6/7종, 브랜치 전략 없음 (MEDIUM) |
| 13 | 트러블슈팅(선택) | O | 17절 Case 1~4 |

작성 체크리스트 5문항: 1~3번 "예"(13절 대조표가 최종결과물/기능요구사항/과제목표 전항 커버), 4~5번 "예".

### 학습 주석 품질 평가 (main.py)

- **틀린 설명**: `main.py:409` 1건 (HIGH 1). 그 외 전수 검토한 어원/비유/동작 설명은 전부 정확했다.
  - 정확 확인: `norma`=직각자(`:280`), `accumulare`=쌓다(`:13`), NPU 확장(`:6`), MAC 확장(`:12`),
    `perf_counter` 단조·고해상도·초 단위 반환(`:364-369`), `repr` 최소 복원 자릿수(`:480-484`),
    `@classmethod`/`cls`(`:184-187`), `EOFError`/`KeyboardInterrupt`(`:541-542`), `.isdigit()`(`:726-728`),
    `dict.get` None 반환(`:308-310`), `_` 관례(`:374`), `continue`/`break`(`:573`/`:588`), `abs`(`:416`)
  - 2진 부동소수점 설명(`:398-402`)과 3x3 계산 예시(`:323-327`, 합=5.0)는 실측과 일치.
  - `main.py:381-382`가 `sum()` 사용을 스스로 변호("금지 대상은 MAC 연산의 축약")한 것은 정확하다. MAC 본체(`:341-347`)는 이중 for.
- **약어 미해제**: 없음. MAC/NPU/JSON/OS/EOF/epsilon/repr/classmethod/self/cls/init/ValueError 전부 최초 등장 시 풀림.
- **week2 대비 밀도**: week2 62.6% vs week3 52.5%(전체 주석+독스트링 / 비공백 라인).
  단 인라인 주석은 week3 39개 vs week2 24개로 더 많고, week3는 독스트링 167줄을 별도 보유한다.
  절대 주석량은 week3가 497줄로 week2 380줄보다 많다. **밀도 저하는 코드량 증가(229 -> 616줄) 때문이며 규칙 위반 수준 아님.**

---

# DEAD_ENDS (시도했으나 실패한 접근)

- (code-verifier) 모드 1의 "행 수 불일치" 크래시 유도 시도 -> 불가능. `read_matrix`가 정확히 3줄만 순차 요구하므로
  사용자가 행 수를 틀릴 입력 경로 자체가 없다. req-auditor의 MEDIUM 항목과 동일 결론에 독립 도달.
- (code-verifier) `data.json`을 디렉터리로 만들어 크래시 유도 -> 실패. `OSError`(PermissionError)가 `main.py:695`에 잡혀 정상 메시지 출력.
- (code-verifier) 200x200 대형 패턴으로 성능/재귀 한계 유도 -> 실패. 정상 판정 완료, 크래시 없음.
