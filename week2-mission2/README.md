# AI 지식 퀴즈 게임

## 프로젝트 개요

터미널에서 동작하는 AI 주제 퀴즈 게임입니다.
바이브코딩, Physical AI, AI Transformation, Agentic AI 등 현재 AI 트렌드를 주제로 한 퀴즈를 풀고, 등록하고, 점수를 관리합니다.
Python 기본 문법과 클래스 설계, JSON 파일 입출력, Git 버전 관리를 학습하는 Codyssey Mission2 과제입니다.

## 퀴즈 주제 선정 이유

제약 생산 현장에서 AI 전환(AX)을 직접 목격하면서, AI 관련 핵심 개념을 체계적으로 정리할 필요성을 느꼈습니다.
단순한 퀴즈가 아니라, 스스로 공부한 내용을 문제화하여 기억에 남기는 학습 도구로 활용합니다.

주제 목록: 바이브코딩, Agentic AI, Physical AI, AX(AI Transformation), MCP, LLM 환각, 검증 레이어

## 실행 방법

```bash
python main.py
```

Python 3.10 이상 필요. 외부 라이브러리 없음 (표준 라이브러리만 사용).

## 기능 목록

| 번호 | 기능 | 설명 |
|------|------|------|
| 1 | 퀴즈 풀기 | 저장된 퀴즈를 순서대로 풀고 점수 확인 |
| 2 | 퀴즈 추가 | 새로운 퀴즈를 등록하고 저장 |
| 3 | 퀴즈 목록 | 등록된 모든 퀴즈 문제 목록 확인 |
| 4 | 점수 확인 | 최고 점수 조회 |
| 5 | 종료 | 데이터 저장 후 프로그램 종료 |

## 파일 구조

```
week2-mission2/
├── main.py            # 메인 프로그램 (Quiz, QuizGame 클래스 포함)
├── state.json         # 퀴즈 데이터 및 최고 점수 저장 파일 (실행 시 자동 생성)
├── README.md          # 프로젝트 문서
├── STEPS.md           # 단계별 구현 가이드
├── STUDY_GUIDE.md     # 동료평가 대비 학습 가이드
├── .gitattributes     # LF 강제 (Windows/Mac 호환)
├── .gitignore         # Python 빌드 파일 제외
└── docs/
    └── screenshots/   # 실행 화면 스크린샷
        ├── manu.png         # 메뉴 화면
        ├── play1.png        # 퀴즈 풀기 1
        ├── play2.png        # 퀴즈 풀기 2
        ├── add quiz.png     # 퀴즈 추가 1
        ├── add quiz2.png    # 퀴즈 추가 2
        ├── add quiz3.png    # 퀴즈 추가 3
        ├── score.png        # 점수 확인
        ├── exit.png         # 종료
        ├── restart.png      # 재실행 시 데이터 유지 확인
        ├── git config.png   # Git 설정 확인
        └── git log.png      # Git 커밋 이력
```

## 데이터 파일 설명 (state.json)

- **경로**: `week2-mission2/state.json` (main.py 기준 동일 디렉토리)
- **역할**: 퀴즈 데이터와 최고 점수를 프로그램 종료 후에도 유지 (데이터 영속성)
- **인코딩**: UTF-8
- **스키마**:

```json
{
    "quizzes": [
        {
            "question": "문제 텍스트",
            "choices": ["선택지1", "선택지2", "선택지3", "선택지4"],
            "answer": 1
        }
    ],
    "best_score": 0
}
```

| 필드 | 타입 | 설명 |
|------|------|------|
| `quizzes` | list | 퀴즈 객체 배열 |
| `quizzes[].question` | str | 문제 텍스트 |
| `quizzes[].choices` | list[str] | 선택지 4개 |
| `quizzes[].answer` | int | 정답 번호 (1~4) |
| `best_score` | int | 역대 최고 정답 수 |

## 코드 구조와 설계 의도

### 클래스 구조

이 프로그램은 2개의 클래스로 역할을 분리하여 설계하였습니다.

| 클래스 | 역할 | 속성 | 메서드 |
|--------|------|------|--------|
| `Quiz` | 퀴즈 **1개**를 표현 | `question`(str), `choices`(list), `answer`(int) | `display()`, `check_answer()`, `to_dict()`, `from_dict()` |
| `QuizGame` | 게임 **전체** 관리 | `quizzes`(list), `best_score`(int) | `run()`, `play()`, `add_quiz()`, `show_list()`, `show_score()`, `load_state()`, `save_state()` |

### 왜 2개의 클래스로 나누었는가?

- **Quiz**: "나는 문제 하나다. 나를 보여주고(`display`), 정답을 확인해 줄 수 있다(`check_answer`)."
- **QuizGame**: "나는 게임 진행자다. 여러 퀴즈를 관리하고, 점수를 기록하고, 파일에 저장한다."
- 퀴즈가 100개가 되어도 Quiz 클래스 코드는 바뀌지 않습니다.
- 게임 규칙이 바뀌어도 Quiz 클래스는 영향받지 않습니다.
- 각 클래스가 **하나의 역할만 담당**하므로, 수정할 때 어디를 고쳐야 하는지 명확합니다.

### 주요 설계 결정

| 결정 | 이유 |
|------|------|
| `get_int_input()` 메서드 분리 | 메뉴 선택(1~5), 정답 입력(1~4), 퀴즈 추가 시 정답 번호 입력 등 "정수 입력 검증"이 3곳에서 반복되므로 한 번 정의하고 재사용 |
| `to_dict()` / `from_dict()` 쌍 | Quiz 객체는 JSON으로 직접 저장할 수 없으므로, dict로 변환(직렬화)하는 메서드와 dict에서 복원하는 메서드를 쌍으로 구현 |
| `_load_defaults()` 밑줄 접두사 | 클래스 내부에서만 사용하는 메서드라는 관례적 표기. 외부에서 직접 호출하지 않는다는 신호 |
| `STATE_FILE` 절대경로 | `os.path.abspath(__file__)` 기준으로 경로를 구성하여, 어떤 디렉토리에서 실행해도 state.json이 main.py와 같은 폴더에 생성됨 |

---

## 핵심 개념 정리

> 과제 목표: "이 과제를 마친 후, 학습자는 아래를 스스로 설명할 수 있어야 한다."

### Python 기초

| 개념 | 설명 | 코드 위치 예시 |
|------|------|----------------|
| **변수** | 값에 이름표를 붙여 메모리에 저장하고 재사용하는 것 | `score = 0`, `total = len(self.quizzes)` |
| **int, str, bool, list, dict 차이** | int=정수, str=문자열, bool=참/거짓, list=순서 있는 목록, dict=키-값 쌍 | `answer`(int), `question`(str), `check_answer` 반환값(bool), `choices`(list), `DEFAULT_QUIZZES` 내 각 항목(dict) |
| **if/elif/else** | 조건에 따라 다른 동작을 수행 | `run()`의 메뉴 분기: `if choice == 1: self.play()` |
| **for vs while** | for=정해진 횟수 반복, while=조건 충족까지 반복 | for: `play()`의 퀴즈 출제 루프 / while: `get_int_input()`의 입력 검증 루프 |
| **함수(매개변수, 반환값)** | 반복 작업을 묶어 이름 붙이고 재사용. 입력(매개변수)을 받아 결과(반환값)를 돌려줌 | `get_int_input(prompt, min_val, max_val)` -> `return value` |

### 클래스와 객체

| 개념 | 설명 | 코드 위치 예시 |
|------|------|----------------|
| **클래스** | 관련된 데이터(속성)와 기능(메서드)을 묶은 설계도. 비유: 붕어빵 틀 | `class Quiz:`, `class QuizGame:` |
| **객체** | 클래스(틀)로 만든 실제 인스턴스. 비유: 틀로 찍은 붕어빵 | `Quiz("문제", [...], 2)`, `QuizGame()` |
| **`__init__`** | 객체 생성 시 자동 호출되는 초기화 메서드. 속성에 초기값을 설정 | `def __init__(self, question, choices, answer):` |
| **`self`** | "이 객체 자신"을 가리키는 참조. 모든 메서드의 첫 매개변수 | `self.question = question` (이 퀴즈의 문제에 값을 저장) |
| **속성과 메서드** | 속성=객체가 가진 데이터, 메서드=객체가 할 수 있는 행동 | 속성: `self.best_score` / 메서드: `self.play()` |

### 파일 입출력

| 개념 | 설명 | 코드 위치 예시 |
|------|------|----------------|
| **파일 열기/읽기/쓰기** | `open()` -> 읽기(`"r"`) 또는 쓰기(`"w"`) -> `with`문으로 자동 닫기 | `with open(STATE_FILE, "r", encoding="utf-8") as f:` |
| **JSON** | JavaScript Object Notation. 사람이 읽을 수 있는 텍스트 기반 데이터 형식. Python dict/list와 구조가 거의 같음 | `json.load(f)` = 파일->dict, `json.dump(data, f)` = dict->파일 |
| **try/except** | 오류가 발생할 수 있는 코드를 시도하고, 실패 시 대비책을 실행 | `try: json.load(f)` / `except json.JSONDecodeError: self._load_defaults()` |
| **데이터 영속성** | 프로그램 종료 후에도 데이터가 유지되는 성질. 변수(메모리)는 종료 시 사라지지만, 파일(디스크)은 남아있음 | `save_state()` = 메모리->디스크, `load_state()` = 디스크->메모리 |

### Git 기초

| 개념 | 설명 |
|------|------|
| **Git** | 코드의 변경 이력을 기록하는 버전 관리 도구. 비유: 변경 내용만 기록하는 타임머신 |
| **원격 저장소** | GitHub에 있는 저장소. 로컬 작업을 push로 업로드하고, pull로 다운로드 |
| **브랜치** | 메인 코드에 영향 없이 별도 공간에서 작업. 완료 후 merge로 합침 |
| **커밋 메시지 컨벤션** | `Feat:` 새 기능, `Fix:` 버그 수정, `Docs:` 문서, `Refactor:` 코드 정리 |

---

## 예외 및 에러 처리

| 상황 | 처리 방법 | 코드 위치 |
|------|-----------|-----------|
| 빈 입력 (그냥 Enter) | `"입력이 없습니다"` 안내 후 재입력 | `get_int_input()` - `if not raw:` |
| 숫자가 아닌 입력 (abc) | `"숫자만 입력해 주세요"` 안내 후 재입력 | `get_int_input()` - `except ValueError:` |
| 범위 밖 숫자 (0, 9 등) | `"1~5 범위의 숫자를 입력해 주세요"` 안내 후 재입력 | `get_int_input()` - `if not (min_val <= value <= max_val):` |
| Ctrl+C 강제 종료 | 데이터 저장 후 안전하게 종료 | `run()` - `except (KeyboardInterrupt, EOFError):` |
| state.json 파일 없음 | 기본 퀴즈 7개로 자동 시작 | `load_state()` - `if not os.path.exists(STATE_FILE):` |
| state.json 파일 손상 | `"저장 파일이 손상되었습니다"` 안내 후 기본 데이터로 복구 | `load_state()` - `except json.JSONDecodeError:` |
| 퀴즈 없는 상태에서 풀기 시도 | `"등록된 퀴즈가 없습니다"` 안내 후 메뉴로 복귀 | `play()` - `if not self.quizzes:` |
| 퀴즈 추가 시 빈 문제 입력 | `"문제를 입력하지 않아 취소합니다"` 안내 후 메뉴로 복귀 | `add_quiz()` - `if not question:` |
| 퀴즈 추가 시 빈 선택지 입력 | `"선택지를 입력해 주세요"` 안내 후 재입력 | `add_quiz()` - `if choice:` 검증 루프 |

---
<img width="507" height="335" alt="image" src="https://github.com/user-attachments/assets/1c48d667-5df5-4ad6-9789-7b74184bda82" />
<img width="558" height="289" alt="image" src="https://github.com/user-attachments/assets/fd7e9495-2e5d-4956-bfb2-f2449df492dd" />



## 실행 화면

### 메뉴 화면
![메뉴 화면](docs/screenshots/manu.png)

### 퀴즈 풀기
![퀴즈 풀기 1](docs/screenshots/play1.png)
![퀴즈 풀기 2](docs/screenshots/play2.png)

### 퀴즈 추가
![퀴즈 추가 1](docs/screenshots/add%20quiz.png)
![퀴즈 추가 2](docs/screenshots/add%20quiz2.png)
![퀴즈 추가 3](docs/screenshots/add%20quiz3.png)

### 점수 확인
![점수 확인](docs/screenshots/score.png)

### 종료
![종료](docs/screenshots/exit.png)

### 재실행 시 데이터 저장 확인
![재실행 시 데이터 저장 확인](docs/screenshots/restart.png)

## 개발 환경

### Git 설정
![Git 설정](docs/screenshots/git%20config.png)

### Git 커밋 이력
![Git 로그](docs/screenshots/git%20log.png)

## Git 사용 기록

### 필수 명령어 7종 사용 내역

| 명령어 | 사용 위치 | 설명 |
|--------|-----------|------|
| `git init` | Mission1에서 수행 (단일 레포 전략) | 현재 폴더를 Git 저장소로 초기화 |
| `git add` | 모든 STEP | 변경 파일을 스테이징 영역에 올림 |
| `git commit` | 모든 STEP (15개+) | 스테이징된 변경사항을 확정 기록 |
| `git push` | STEP 5, 9, 10 | 로컬 커밋을 GitHub에 업로드 |
| `git pull` | STEP 10 | 원격 변경사항을 로컬로 가져옴 |
| `git checkout` | STEP 5 | `feature/play` 브랜치 생성 및 전환 |
| `git clone` | STEP 10 | 원격 저장소를 별도 디렉토리에 복제 |

### 브랜치 전략

```
master:        C1 --- C2 --- C3 --- C4 --- C5 --- C7 (merge) --- C8 ...
                                            \         /
feature/play:                                C6 -----
```

- `git checkout -b feature/play`: STEP 5에서 퀴즈 풀기 기능 개발용 브랜치 생성
- `git merge feature/play`: 기능 완성 후 master에 병합 (Fast-forward)
- **왜 브랜치를 사용하는가?**: 새 기능 개발 도중 버그가 생겨도 master는 안전하게 유지됨

### 커밋 메시지 컨벤션

| 접두사 | 의미 | 예시 |
|--------|------|------|
| `Feat:` | 새 기능 추가 | `Feat: Quiz 클래스 구현` |
| `Fix:` | 버그 수정 | `Fix: state.json 경로를 main.py 기준으로 변경` |
| `Docs:` | 문서 작성/수정 | `Docs: README 완성 및 스크린샷 추가` |
| `Chore:` | 설정/운영 관련 | `Chore: Mission2 초기 세팅` |

### Clone/Pull 실습 기록

```bash
# 1. 별도 디렉토리에 저장소 복제 (clone)
#    clone = 원격 저장소의 전체 이력을 포함한 완전한 사본을 만드는 명령어
git clone https://github.com/MylovelyCatMori/Marina2nd_Codyssey.git D:/Projects/Marina2nd_Codyssey-clone

# 2. 복제된 저장소에서 README 수정 후 commit + push
cd D:/Projects/Marina2nd_Codyssey-clone
git add week2-mission2/README.md    # 변경 파일을 스테이징
git commit -m "Docs: clone/pull 실습용 변경"  # 변경사항 확정
git push origin master              # GitHub에 업로드

# 3. 원래 작업 디렉토리에서 변경사항 가져오기 (pull)
#    pull = 원격 저장소의 새로운 커밋을 로컬에 가져와 병합하는 명령어
#    clone과의 차이: clone은 "처음 복사", pull은 "이미 있는 저장소를 최신으로 갱신"
cd "D:/Projects/Codyssey with Claude"
git pull origin master
# -> Fast-forward 병합으로 변경사항 정상 반영 확인
```
