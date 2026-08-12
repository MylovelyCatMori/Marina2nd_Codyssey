# 끼리끼리 검증 리포트 -- Week3 Mission3 산출물

- 팀: kkirikkiri-analysis-0812-mission3 (팀장 + 요구사항 감사관 + 코드 검증관 + 문서 검증관)
- 일자: 2026-08-12
- 대상: `D:\Projects\S01-codyssey\week3-mission3\`
- 기준: `D:\Projects\S01-codyssey\Week3_Mission3.txt`
- 라운드: 1라운드로 종료 (품질 4기준 전부 PASS)

---

## 1. 종합 판정

**제출 가능.** CRITICAL 0건. HIGH 6건과 MEDIUM 5건은 전부 수정 완료.

| 관점 | 검증 규모 | 결과 |
|---|---|---|
| 요구사항 전수 대조 | 원문에서 124개 항목 추출 | PASS 120 / 판단보류 1 / N/A 3 / **FAIL 0** |
| 코드 정확성·예외 처리 | 62개 시나리오 실제 실행 | CRITICAL 0 / HIGH 1 / MEDIUM 1 / LOW 4 |
| 문서 사실 오류 | 라인참조 74건 + 수치 21건 + 사실주장 14건 | HIGH 5 / MEDIUM 5 / LOW 9 |
| 학습 주석 품질 | 전수 검토 | 틀린 설명 1건 (수정), 약어 미해제 0건 |

핵심 제약 8종은 전부 충족했다.
외부 라이브러리 금지(import 4개 전부 표준) / MAC 이중 for문 / epsilon 1e-9 / 라벨 정규화 4매핑 / 성능표 3열 / REPEAT 10 / 케이스 단위 FAIL / 모드1 재입력 유도.

---

## 2. 수정한 이슈

### HIGH 6건

| # | 이슈 | 조치 |
|---|---|---|
| H1 | `load_data`가 `UnicodeDecodeError`를 못 잡아 **프로그램이 트레이스백으로 죽음**. data.json이 CP949(한글 Windows 메모장 기본)·UTF-16이면 발생. 요구사항 "프로그램이 비정상 종료되면 안된다" 위반 | `except json.JSONDecodeError` -> `except ValueError`. 두 예외 모두 `ValueError`의 자식이라 한 줄로 덮인다. 메시지도 "인코딩 또는 JSON 형식 오류"로 확장 |
| H2 | `main.py`의 `decide()` 주석과 README 9-4절이 **"== 로 비교하면 X가 이긴 것처럼 처리된다"**고 서술. 실제로는 `0.9 > 0.8999999999999999`이므로 **Cross**가 이긴다. 게다가 README 11-2절은 정반대로 올바르게 서술하고 있어 자기모순 | 두 곳 모두 "대소만 따지면 Cross가 이긴 것으로 처리된다"로 정정 |
| H3 | README·PRD가 "`meta.version`은 출력만 한다"고 주장하나 코드에 `meta` 참조가 0회 | "읽지도 검증하지도 않는다"로 정정 + 필수 키가 `filters`/`patterns` 둘뿐임을 명시 |
| H4 | `README.md`가 `DATA_FILE`을 `main.py:36`이라 표기 (실제 54행) | 정정 |
| H5 | `README.md`가 `LABEL_CROSS`/`LABEL_X`를 `(76~77)`이라 표기 (실제 73~74) | 정정 |
| H6 | README 14절이 스크린샷 6장을 표로 참조하나 `docs/screenshots/`가 비어 있음 | "캡처 대기" 상태 열 추가 + 캡처 규칙 명시. **실제 캡처는 사용자 작업으로 남음** |

### MEDIUM 5건

| # | 이슈 | 조치 |
|---|---|---|
| M1 | `.isdigit()`가 통과시킨 유니코드 위첨자(`'²'`)를 `int()`가 거부해 크래시. `parse_case_size`는 `sorted()` 안에서 try 바깥으로 호출되어 아무도 못 잡음 | `.isdigit()` -> `.isdecimal()` (2곳). `isdecimal()`의 참 집합이 `int()` 수용 집합과 정확히 일치 |
| M2 | 요구사항 "행 수/열 수 불일치 검증"에서 **행 수 검증 경로가 코드에 없음**. 다만 3줄을 순차 요구하므로 구조적으로 불일치가 불가능 | `read_matrix` docstring + README 예외 표에 근거 명시. 동료평가에서 물었을 때 답이 문서에 있게 함 |
| M3 | PRD·STEPS가 "17자리 출력"이라 서술 (실제 `.16f` = 16자리) | 정정 |
| M4 | `PRD/04` 섹션 순서표에 `UserAbort`, `JudgeResult`가 누락 | 11개 섹션으로 재작성 |
| M5 | README Git 기록에 명령어 6종만 있고 필수 7종 표와 브랜치 전략이 누락 (LEARNING_RULES 요구) | 7종 표 + 브랜치 전략 + `--no-ff` 설명 추가 |

### 추가 조치

- 성능표 헤더를 `크기` -> `크기(N×N)`로 변경 (요구사항 문구와 일치). 표 정렬 42열 유지 확인
- README 트러블슈팅에 Case 5(인코딩 예외 상속 관계), Case 6(`isdigit` vs `isdecimal`) 추가 — 검증에서 나온 실제 버그이므로 학습 자산으로 남김
- README 내결함성 실측 표에 CP949·유니코드 위첨자 케이스 추가

---

## 3. 수정하지 않은 이슈 (LOW 4건)와 사유

| 이슈 | 사유 |
|---|---|
| `NaN`/`Infinity`가 검증을 통과해 판정이 항상 X로 쏠림 | 프로그램이 죽지 않고 FAIL로 보고한다. 요구사항 위반 아님. 원본 data.json에 해당 값 없음 |
| 같은 표준 라벨로 정규화되는 필터 키 2개가 있으면 조용히 덮어씀 (`cross` + `plus`) | 원본은 `cross`/`x` 한 쌍뿐. 방어 코드를 늘리는 비용이 이득보다 큼 |
| `sort_key_for_case`의 idx 정렬이 사전순 (`size_5_10` < `size_5_2`) | 원본 idx는 1, 2뿐. 크기 정렬 자체는 정확 |
| MAC 연산 중 Ctrl+C는 트레이스백 | 요구사항의 "비정상 종료 금지"는 데이터/스키마 오류 문맥. 연산 중 강제 중단은 대상 아님 |

**epsilon은 조정하지 않았다.** FAIL 3건은 데이터가 수학적으로 정확한 동점(9/10 = 9/10, 15/2 = 15/2, 49/10 = 49/10)으로 설계된 결과다. 통과시키려면 판정 규칙을 조작해야 하고, 그것은 판정기가 아니라 정답 맞추기다.

---

## 4. 회색지대 (동료평가에서 질문 나올 수 있는 지점)

| 항목 | 현재 선택 | 방어 논리 |
|---|---|---|
| 모드 1 행 수 검증 | 구조적 보장 (3줄 순차 요구) | 요구사항 예시 문구가 "각 줄에 3개의 숫자"로 **줄 단위 검증**을 가리킨다. 한 줄에 9개를 넣어도 열 수 검증에 걸린다 |
| FAIL 3건 | 정직하게 UNDECIDED로 보고 | 요구사항 8절 예시가 동일 상황을 `FAIL (동점 규칙)`으로 보여준다. 데이터 설계 의도 |
| 3×3 내장 상수 | `BUILTIN_*_3X3` | data.json에 `size_3`이 없는데 요구사항은 "성능 분석(3×3 포함)"을 요구. 보너스 "패턴 생성기"의 대체물이 아니다 |
| `--selftest` 옵션 추가 | 유지 | 요구사항이 금지하지 않고, 기본 실행(`python main.py`)은 요구사항대로 메뉴로 진입 |
| 보너스 미구현 | 제외 | 원문 137행이 "5. 보너스 과제 **(선택)**"으로 명시 |
| `--selftest` 안의 `==` 비교 | 유지 | 요구사항의 epsilon 규정은 **두 필터 점수 간 판정**을 규율한다. 테스트 단언은 대상 아니며 0.0/1.0 합은 정확 표현됨 |

---

## 5. 수정 후 재검증

| 항목 | 결과 |
|---|---|
| `python main.py --selftest` | 전 항목 통과 |
| 모드 1 예시 입력 | A=1.0 / B=5.0 / 판정 B |
| 모드 1 오류 3종 (개수 부족, 문자, 빈 줄) | 안내 후 그 줄만 재입력, 프로그램 유지 |
| 모드 2 총계 | **총 6 / 통과 3 / 실패 3** (정답표 일치, 회귀 없음) |
| CP949 data.json | 트레이스백 없이 안내 후 메뉴 복귀 |
| `size_²` 필터 키 | 트레이스백 없이 `[FAIL]` 안내 |
| 문서 코드참조 48건 자동 대조 | 전건 일치 |
| import | `json`, `os`, `sys`, `time` 4개뿐 |
| `mac()` 내 `sum(`/`zip(` | 없음 (주석 언급만) |
| `except: pass` | 0건 |
| `data.json` md5 | `214daadf7af39e8281aa03f5b058368d` — 작업 전후 동일 |

---

## 6. 남은 사용자 작업

- [ ] 스크린샷 6장 캡처 후 `docs/screenshots/`에 저장, README 14절 상태 열 갱신
- [ ] STEPS.md STEP 0~12 순서로 커밋 수행 후 `git push origin master`
- [ ] 동료평가 신청 시 저장소 URL + `week3-mission3/` 경로 병기

---

## 7. 산출물 목록

```
week3-mission3/
├── main.py            1192줄. 제출물 1
├── README.md          제출물 2. 17개 섹션
├── STEPS.md           STEP 0~12 커밋 가이드
├── data.json          과제 제공 (미변경)
├── .gitattributes     LF 강제
├── .gitignore         Python 표준
├── PRD/               01_PRD / 02_DATA_MODEL / 03_PHASES / 04_PROJECT_SPEC / README
└── docs/screenshots/  (비어 있음 -- 캡처 대기)
```

공유 메모리:
- `.kkirikkiri/TEAM_PLAN.md` — 계획, 결정사항, 검증 결과
- `.kkirikkiri/TEAM_FINDINGS.md` — 이슈 전문 (재현 명령어 포함)
- `.kkirikkiri/TEAM_PROGRESS.md` — 팀원별 진행 기록
- `.kkirikkiri/archive/FINDINGS-2026-08-04-mission2.md` — 이전 세션(Mission2 검증) 보관본
