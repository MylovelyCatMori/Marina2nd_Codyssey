# 발견 사항 & 공유 자료

(팀원들이 발견한 내용을 여기에 기록)

## 2026-08-04 — 코드 분석가: main.py 코드 품질 검증

### 1. 클래스 설계 [PASS]
- Quiz/QuizGame 역할 분리 적절. Quiz는 단일 퀴즈 표현, QuizGame은 게임 진행 관리.
- to_dict/from_dict 직렬화 쌍 완비. 메서드 분리 과불족 없음.
- 불필요한 속성/메서드 없음.

### 2. 예외 처리 [PASS]
- 빈 입력: get_int_input에서 strip() 후 not raw 체크. PASS.
- 숫자 변환 실패: ValueError except. PASS.
- 범위 밖 숫자: min_val <= value <= max_val 체이닝 비교. PASS.
- Ctrl+C (KeyboardInterrupt): run()에서 try/except로 감싸고 save_state() 호출. PASS.
- EOFError: KeyboardInterrupt와 함께 처리. PASS.
- JSONDecodeError: load_state()에서 처리, 기본 데이터로 복구. PASS.
- 파일 없음: os.path.exists() 선행 체크. PASS.
- 퀴즈 목록 비어있을 때: play()와 show_list() 모두 빈 리스트 체크. load_state()에서도 빈 배열 시 _load_defaults() 호출. PASS.

### 3. 데이터 영속성 [PASS]
- with문 사용: 읽기/쓰기 모두 사용. PASS.
- encoding="utf-8": 읽기/쓰기 모두 명시. PASS.
- ensure_ascii=False: json.dump에 설정. PASS.
- indent=2: 사람 가독성 확보. PASS.
- 퀴즈 추가 시 즉시 저장, 최고점수 갱신 시 즉시 저장, 종료 시 저장, Ctrl+C 시에도 저장. 견고함.

### 4. 코드 중복 [PASS]
- get_int_input 재사용: 메뉴 선택, 정답 입력, 퀴즈 추가 정답 번호에서 3회 재사용. PASS.
- _load_defaults 재사용: 파일 없음, 파일 손상, 빈 목록 3곳에서 호출. PASS.
- 불필요한 복잡성 없음.

### 5. 표준 라이브러리 [PASS]
- import json, import os만 사용. 둘 다 Python 표준 라이브러리. 외부 패키지 없음.

### 6. 추가 발견사항
- **경미 이슈 1**: show_score()에서 best_score == 0이면 "기록 없음" 표시. 실제로 0점을 받은 경우와 미플레이를 구분 불가. 단, 미션 범위 내에서는 문제없음. 개선하려면 play_count 같은 별도 필드 필요.
- **경미 이슈 2**: add_quiz()에서 선택지 입력 중 KeyboardInterrupt 발생 시, run()의 외부 try/except가 잡아서 저장 후 종료. 부분 입력된 퀴즈는 추가되지 않으므로 데이터 무결성 문제 없음. 정상 동작.
- 잠재적 버그: 없음.

### 종합 판정: PASS
코드 구조, 예외 처리, 데이터 영속성 모두 미션 요구사항을 충족. 학습 주석도 정확하고 상세함.

---

## 2026-08-04 — 요구사항 검증자: Mission2 요구사항 충족 검증

### 1. 기능 요구사항 [PASS]
| 항목 | 판정 | 근거 |
|------|------|------|
| 메뉴 출력 + 기능 선택 + 종료 | PASS | show_menu() 5개 메뉴, run()에서 choice 분기, 5번 종료 |
| 잘못된 입력 처리 | PASS | get_int_input()에서 4가지 케이스 처리 |
| Quiz 클래스 (question/choices/answer + display/check_answer) | PASS | __init__에 3속성, display(), check_answer(), to_dict(), from_dict() |
| 기본 퀴즈 5개 이상 | PASS | DEFAULT_QUIZZES 7개 (AI/바이브코딩/Physical AI/AX/Agentic AI/MCP/LLM 환각) |
| 퀴즈 풀기 (출제/입력/판정/결과/빈목록) | PASS | play() 메서드 전체 구현 |
| 퀴즈 추가 (문제/선택지4개/정답/검증/저장) | PASS | add_quiz() 메서드, 빈 입력 처리, save_state() 호출 |
| 퀴즈 목록 (전체 표시/빈 목록) | PASS | show_list() 메서드, not self.quizzes 체크 |
| 점수 확인 (최고점수/갱신/저장/미플레이) | PASS | show_score(), play()에서 갱신 후 save_state() |
| QuizGame 클래스 (속성/메서드 전체) | PASS | quizzes/best_score 속성, 6개 메서드 완비 |

### 2. 코드 구조 요구사항 [PASS]
| 항목 | 판정 | 근거 |
|------|------|------|
| 최소 2개 클래스 | PASS | Quiz, QuizGame |
| 기능별 메서드 분리 | PASS | 입력(get_int_input)/진행(play)/저장(save_state/load_state) 등 |
| state.json UTF-8 인코딩 | PASS | open(..., encoding="utf-8") 읽기/쓰기 모두 명시 |

### 3. 공통 입력/예외 처리 [PASS]
| 항목 | 판정 | 근거 |
|------|------|------|
| .strip() 공백 제거 | PASS | get_int_input, add_quiz 문제/선택지 입력 |
| 숫자 변환 실패 안내 + 재입력 | PASS | except ValueError |
| 범위 밖 숫자 안내 + 재입력 | PASS | min_val <= value <= max_val 체크 |
| 빈 입력 안내 + 재입력 | PASS | if not raw 체크 |
| Ctrl+C / EOFError 안전 종료 + 저장 | PASS | run()에서 except (KeyboardInterrupt, EOFError) + save_state() |
| 파일 없음 -> 기본 퀴즈 | PASS | os.path.exists() 선행 체크 -> _load_defaults() |
| 파일 손상 -> 안내 + 복구 | PASS | except json.JSONDecodeError -> 메시지 + _load_defaults() |

### 4. README 필수 항목 [PASS]
| 항목 | 판정 | 근거 |
|------|------|------|
| 프로젝트 개요 | PASS | "프로젝트 개요" 섹션 존재 |
| 퀴즈 주제 선정 이유 | PASS | "퀴즈 주제 선정 이유" 섹션 존재 |
| 실행 방법 | PASS | "실행 방법" 섹션 존재 |
| 기능 목록 | PASS | "기능 목록" 섹션 존재 |
| 파일 구조 | PASS | "파일 구조" 섹션 존재 |
| 데이터 파일 설명 (state.json 경로/역할/스키마) | PASS | "데이터 파일 설명 (state.json)" 섹션 존재 |

### 5. 미충족 항목: 없음

### 종합 판정: PASS
4개 검증 영역 (기능/구조/예외처리/README) 모두 PASS. 미충족 항목 0건.

---

# DEAD_ENDS (시도했으나 실패한 접근)

(없음)
