# Mission2 학습 가이드 - 동료평가 대비

> 이 가이드는 동료평가에서 "왜 이렇게 했는지" 설명할 수 있도록 구성되었습니다.
> 단계별로 읽고, 각 섹션 끝의 "설명 연습" 질문에 답할 수 있으면 준비 완료입니다.

---

## 1단계: Python 기초 - 변수와 타입

### 변수란?

값에 이름표를 붙이는 것입니다. 컴퓨터 메모리 어딘가에 저장된 값을, 이름으로 불러 사용합니다.

```python
score = 0          # int (정수) - 점수 계산에 사용
question = "문제"  # str (문자열) - 텍스트 데이터
is_correct = True  # bool (참/거짓) - 조건 판단에 사용
choices = ["A", "B", "C", "D"]  # list (목록) - 순서 있는 여러 값
quiz_data = {"question": "문제", "answer": 1}  # dict (사전) - 키-값 쌍
```

### 왜 타입이 중요한가?

타입에 따라 할 수 있는 연산이 다릅니다.

```python
# int끼리 더하면 숫자 덧셈
3 + 5  # 8

# str끼리 더하면 문자열 연결
"안녕" + "하세요"  # "안녕하세요"

# int와 str을 더하면? -> TypeError 발생!
3 + "5"  # 오류!
int("5")  # 문자열 "5"를 정수 5로 변환
```

### 우리 코드에서의 활용

```python
self.question = question  # str: 문제 텍스트
self.choices = choices    # list: 선택지 4개
self.answer = answer      # int: 정답 번호 (1~4)
self.best_score = 0       # int: 최고 점수
```

### 설명 연습

- "int, str, list, dict의 차이를 설명해 주세요."
- "왜 정답을 int로 저장하나요? str로 하면 안 되나요?"

---

## 2단계: 조건문과 반복문

### if/elif/else - 갈림길 만들기

프로그램이 조건에 따라 다른 길로 가게 합니다.

```python
if choice == 1:
    self.play()        # 1번이면 퀴즈 풀기
elif choice == 2:
    self.add_quiz()    # 2번이면 퀴즈 추가
elif choice == 5:
    break              # 5번이면 종료
```

**핵심**: `if`는 "만약 ~라면", `elif`는 "아니면 ~라면", `else`는 "그 외 전부"

### for vs while - 반복의 두 가지 방식

**for**: 정해진 횟수만큼 반복 ("목록의 각 항목에 대해")

```python
# 퀴즈 7개를 순서대로 출제
for i, quiz in enumerate(self.quizzes, start=1):
    print(f"[{i}/{total}]")
    quiz.display()
```

**while**: 조건이 참인 동안 계속 반복 ("언제 끝날지 모를 때")

```python
# 올바른 입력이 올 때까지 계속 반복
while True:
    raw = input(prompt).strip()
    if not raw:
        print("입력이 없습니다.")
        continue      # 루프 처음으로 돌아감
    return value       # 올바른 값이면 루프 탈출
```

**선택 기준**:
- 몇 번 반복할지 아는 경우 → `for` (퀴즈 출제, 선택지 4개 입력)
- 조건 충족까지 반복하는 경우 → `while` (메뉴 루프, 입력 검증)

### 설명 연습

- "for와 while을 각각 어디에 썼고, 왜 그렇게 선택했나요?"
- "continue와 break의 차이는?"

---

## 3단계: 함수 - 코드에 이름 붙이기

### 함수란?

반복되는 작업을 묶어서 이름을 붙인 것입니다. 한 번 정의하면 여러 번 호출할 수 있습니다.

```python
def get_int_input(self, prompt, min_val, max_val):
    # prompt: 사용자에게 보여줄 안내 문구
    # min_val, max_val: 허용 범위
    # 반환값: 유효한 정수
    ...
    return value
```

- **매개변수(parameter)**: 함수가 받는 입력 (`prompt`, `min_val`, `max_val`)
- **반환값(return value)**: 함수가 돌려주는 결과 (`value`)

### 왜 함수로 분리하나?

```python
# 함수 없이 매번 작성하면:
raw = input("선택: ").strip()
try:
    value = int(raw)
except ValueError:
    print("숫자만 입력해 주세요.")
# ... 이 코드를 메뉴/퀴즈 풀기/퀴즈 추가마다 반복?

# 함수로 만들면 한 줄로 끝:
choice = self.get_int_input("선택: ", 1, 5)
answer = self.get_int_input("정답 번호 입력: ", 1, 4)
```

### 설명 연습

- "get_int_input 함수는 왜 만들었나요?"
- "매개변수와 반환값이 각각 무엇인지 설명해 주세요."

---

## 4단계: 클래스와 객체 - 역할별 묶음

### 클래스란?

관련된 데이터(속성)와 기능(메서드)을 하나로 묶은 설계도입니다.

**비유**: 클래스는 "퀴즈 카드 양식"이고, 객체는 "실제 작성된 퀴즈 카드 한 장"입니다.

```python
# 클래스 = 설계도
class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

# 객체 = 설계도로 만든 실제 물건
quiz1 = Quiz("바이브코딩이란?", ["A", "B", "C", "D"], 2)
quiz2 = Quiz("Agentic AI란?", ["A", "B", "C", "D"], 3)
```

### __init__과 self

- **`__init__`**: 객체가 생성될 때 자동으로 호출되는 메서드. "초기화 메서드"
  - `Quiz("문제", [...], 1)` 하면 자동으로 `__init__` 실행
- **`self`**: "이 객체 자신"을 가리키는 참조
  - `self.question = question` → "이 퀴즈 카드의 문제란에 question을 적어라"

### 왜 클래스를 2개로 나누었나?

| 클래스 | 역할 | 속성 | 메서드 |
|--------|------|------|--------|
| Quiz | 퀴즈 1개 표현 | question, choices, answer | display(), check_answer() |
| QuizGame | 게임 전체 관리 | quizzes, best_score | play(), add_quiz(), save_state() 등 |

**분리 이유**: 각 클래스가 하나의 역할만 담당합니다.
- Quiz는 "문제 하나"만 책임집니다 (출력, 정답 확인).
- QuizGame은 "게임 진행"만 책임집니다 (메뉴, 점수, 저장).
- 퀴즈가 100개가 되어도 Quiz 클래스는 바뀌지 않습니다.

### @classmethod란?

```python
@classmethod
def from_dict(cls, data):
    return cls(data["question"], data["choices"], data["answer"])
```

- 일반 메서드: 이미 만들어진 객체(`self`)에서 호출
- 클래스 메서드: 클래스 자체(`cls`)에서 호출하여 새 객체 생성
- `Quiz.from_dict(data)` → dict 데이터로 Quiz 객체를 만드는 "공장 메서드"

### 설명 연습

- "왜 클래스를 2개로 나누었나요? 하나로 하면 안 되나요?"
- "`__init__`은 언제 호출되나요?"
- "`self`는 무엇을 가리키나요?"

---

## 5단계: 파일 입출력과 JSON

### 파일 읽기/쓰기 기본 과정

1. **열기** (`open`) → 2. **읽기/쓰기** (`read`/`write`) → 3. **닫기** (`close`)

```python
# with 문을 쓰면 자동으로 닫힘 (닫기 실수 방지)
with open("state.json", "r", encoding="utf-8") as f:
    data = json.load(f)  # JSON 파일 → Python dict로 변환
```

### JSON이란? 왜 사용하나?

**JSON (JavaScript Object Notation)**: 데이터를 텍스트로 저장하는 표준 형식입니다.

```json
{
    "quizzes": [
        {
            "question": "바이브코딩이란?",
            "choices": ["A", "B", "C", "D"],
            "answer": 2
        }
    ],
    "best_score": 5
}
```

**왜 JSON인가?**
- 사람이 읽을 수 있음 (메모장으로 열어서 확인 가능)
- Python dict/list와 구조가 거의 같음 (변환이 쉬움)
- 거의 모든 프로그래밍 언어에서 지원함

### try/except - 오류 대비

```python
try:
    data = json.load(f)           # 시도: JSON 파싱
except json.JSONDecodeError:      # 실패 시: 파일이 깨진 경우
    print("저장 파일이 손상되었습니다.")
    self._load_defaults()         # 기본 데이터로 복구
```

**왜 필요한가?**: state.json을 사용자가 직접 편집하다 깨뜨릴 수 있습니다. 프로그램이 그 상황에서 죽지 않고 복구해야 합니다.

### 데이터 영속성이란?

프로그램을 껐다 켜도 데이터가 살아있는 것입니다.

- 변수: 프로그램 종료 시 사라짐 (메모리에만 존재)
- 파일: 프로그램 종료 후에도 남아있음 (디스크에 저장)
- `save_state()`: 메모리 → 디스크 (변수 → state.json)
- `load_state()`: 디스크 → 메모리 (state.json → 변수)

### 설명 연습

- "JSON이 뭐고, 왜 데이터 저장에 사용했나요?"
- "state.json이 없거나 깨지면 어떻게 되나요?"
- "데이터 영속성이란 무엇인가요?"

---

## 6단계: Git 기초 - 변경 이력 관리

### Git이란? 왜 필요한가?

코드의 **변경 이력을 기록**하는 도구입니다.

**비유**: 문서 작성 시 "다른 이름으로 저장" 대신, 변경 내용만 기록하는 타임머신.

- 코드가 잘 돌아갈 때 저장해두면, 망쳐도 되돌릴 수 있음
- 누가, 언제, 무엇을, 왜 바꿨는지 기록됨
- 팀원과 같은 코드를 동시에 작업할 수 있음

### 7개 명령어 정리

| 명령어 | 하는 일 | 비유 |
|--------|---------|------|
| `git init` | 현재 폴더를 Git 저장소로 초기화 | 빈 일지 노트를 처음 만듦 |
| `git add` | 변경된 파일을 "스테이징 영역"에 올림 | 택배 상자에 물건 담기 |
| `git commit` | 스테이징된 변경사항을 확정 기록 | 택배 상자 테이핑 + 라벨 붙이기 |
| `git push` | 로컬 커밋을 원격 저장소(GitHub)에 업로드 | 택배 발송 |
| `git pull` | 원격 저장소의 변경사항을 로컬로 가져옴 | 택배 수령 |
| `git checkout` | 브랜치 전환 또는 생성 | 작업 공간 이동 |
| `git clone` | 원격 저장소를 로컬에 복제 | 친구 프로젝트 사본 받기 |

### 브랜치란?

메인 코드에 영향 없이 별도 공간에서 작업하는 것입니다.

```
main:         C1 --- C2 --- C3 --- C5 (merge)
                       \         /
feature/play:           C4 -----
```

- `git checkout -b feature/play`: 새 브랜치 생성 + 이동
- 작업 완료 후 `git merge feature/play`: main에 합침
- **왜?**: 기능 개발 도중 버그가 생겨도 main은 안전함

### 커밋 메시지 규칙

```
Feat: 퀴즈 풀기 기능 구현       (새 기능)
Fix: 점수 계산 오류 수정         (버그 수정)
Docs: README 실행 방법 추가      (문서)
Refactor: QuizGame 책임 분리    (코드 정리)
```

**왜 이렇게 쓰나?**: `git log`로 이력을 볼 때 "무엇을 했는지" 한눈에 파악하기 위해.

### 설명 연습

- "Git이 왜 필요한가요?"
- "add, commit, push의 차이를 설명해 주세요."
- "브랜치를 왜 만들었고, 어떻게 합쳤나요?"
- "clone과 pull의 차이는?"

---

## 7단계: 코드 흐름 전체 이해

### 프로그램 실행 순서

```
python main.py
  └─ QuizGame() 생성
       └─ __init__() 호출
            └─ load_state() 호출
                 ├─ state.json 있음 → 파일에서 로드
                 └─ state.json 없음 → DEFAULT_QUIZZES 사용
       └─ run() 호출
            └─ while True 루프
                 ├─ show_menu() → 메뉴 출력
                 ├─ get_int_input() → 사용자 입력
                 ├─ 1 → play()
                 ├─ 2 → add_quiz() → save_state()
                 ├─ 3 → show_list()
                 ├─ 4 → show_score()
                 └─ 5 → save_state() → break
```

### 데이터 흐름

```
DEFAULT_QUIZZES (dict 목록)
  ↓ Quiz(**q)
Quiz 객체 목록 (self.quizzes)
  ↓ q.to_dict()
dict 목록
  ↓ json.dump()
state.json (파일)
  ↓ json.load()
dict 목록
  ↓ Quiz.from_dict()
Quiz 객체 목록 (다시 self.quizzes)
```

### 설명 연습

- "프로그램을 처음 실행하면 어떤 일이 일어나나요?"
- "퀴즈를 추가하면 데이터가 어떤 경로로 저장되나요?"
- "프로그램을 재시작하면 추가한 퀴즈가 어떻게 복원되나요?"
