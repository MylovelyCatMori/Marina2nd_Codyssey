# ============================================================================
# import (임포트) = 다른 파일에서 미리 만들어진 기능을 가져오는 것
# 비유: 도서관에서 필요한 책을 빌려오는 것. 직접 쓸 필요 없이 가져다 쓴다.
# ============================================================================

import json  # json = JavaScript Object Notation (자바스크립트 객체 표기법)
             # Python dict/list <-> JSON 텍스트 파일 변환을 담당하는 표준 라이브러리
             # json.load()  = JSON 파일 읽기 (파일 -> dict)
             # json.dump()  = JSON 파일 쓰기 (dict -> 파일)

import os    # os = Operating System (운영체제)
             # 파일 존재 여부 확인, 경로 조합 등 운영체제와 상호작용하는 표준 라이브러리
             # os.path.exists()  = 파일이 존재하는지 확인
             # os.path.dirname() = 경로에서 폴더 부분만 추출
             # os.path.join()    = 경로를 OS에 맞게 조합 (Windows: \, Mac/Linux: /)


# ============================================================================
# 상수 (CONSTANT) 정의
# 상수 = 프로그램 실행 중 변하지 않는 값. 관례상 대문자로 작성한다.
# 비유: 건물 주소처럼, 프로그램이 돌아가는 동안 바뀌지 않는 고정된 정보
# ============================================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# os.path.abspath(__file__)
#   __file__ = 현재 실행 중인 파이썬 파일 자체를 가리키는 특수 변수 (여기서는 main.py)
#   abspath = absolute path (절대 경로). 상대 경로를 전체 경로로 변환한다.
#   예: "main.py" -> "D:/Projects/Codyssey with Claude/week2-mission2/main.py"
# os.path.dirname(...)
#   dirname = directory name (디렉토리 이름). 파일명을 제외한 폴더 경로만 추출한다.
#   예: ".../week2-mission2/main.py" -> ".../week2-mission2"
# 왜 이렇게 하는가?
#   사용자가 어떤 폴더에서 `python main.py`를 실행하든,
#   항상 main.py가 있는 폴더 기준으로 state.json을 찾기 위해서이다.

STATE_FILE = os.path.join(BASE_DIR, "state.json")
# os.path.join() = 폴더 경로 + 파일명을 운영체제에 맞게 합친다.
# 예: "D:/.../week2-mission2" + "state.json" -> "D:/.../week2-mission2/state.json"
# 왜 문자열 덧셈("D:/" + "state.json")을 쓰지 않는가?
#   Windows는 경로 구분자가 \, Mac/Linux는 /이다.
#   os.path.join()은 이를 자동으로 처리해 준다.


# ============================================================================
# DEFAULT_QUIZZES = 기본 퀴즈 데이터 (프로그램 첫 실행 시 사용)
#
# 자료구조 설명:
#   - list (리스트) 안에 dict (딕셔너리) 7개가 들어 있다.
#   - list = 순서가 있는 목록. [항목1, 항목2, ...] 형태.
#     비유: 번호가 붙은 서류함. 0번 칸, 1번 칸... 순서대로 꺼낼 수 있다.
#   - dict = 이름표(key)로 값(value)을 찾는 구조. {"이름표": 값} 형태.
#     비유: 사전(dictionary)에서 단어(key)로 뜻(value)을 찾는 것과 같다.
#
# 각 dict의 구조:
#   "question": str  = 문제 텍스트 (문자열)
#   "choices": list   = 선택지 4개가 담긴 리스트
#   "answer": int     = 정답 번호 (1~4 중 하나, 정수)
# ============================================================================

DEFAULT_QUIZZES = [
    {
        "question": "바이브코딩(Vibe Coding)의 핵심 특징은 무엇인가?",
        "choices": [
            "컴파일러 없이 기계어를 직접 작성한다",
            "자연어 지시로 AI가 코드를 생성하고 개발자는 흐름을 제어한다",
            "마우스만 사용해 코드를 드래그 앤 드롭으로 작성한다",
            "팀원 없이 혼자 모든 개발을 완료하는 방식이다"
        ],
        "answer": 2
    },
    {
        "question": "Agentic AI의 가장 큰 특징은 무엇인가?",
        "choices": [
            "사람이 모든 단계를 직접 실행하고 AI는 결과만 검토한다",
            "인터넷 연결 없이 오프라인에서만 동작한다",
            "목표를 받으면 계획 수립부터 실행까지 자율적으로 수행한다",
            "텍스트 생성만 가능하고 외부 도구는 사용할 수 없다"
        ],
        "answer": 3
    },
    {
        "question": "Physical AI가 기존 소프트웨어 AI와 다른 핵심 차이는?",
        "choices": [
            "클라우드 서버에서만 실행된다",
            "물리 세계를 인식하고 로봇 등 하드웨어를 통해 직접 행동한다",
            "텍스트 데이터만 처리할 수 있다",
            "인터넷 검색 기능이 내장되어 있다"
        ],
        "answer": 2
    },
    {
        "question": "AX(AI Transformation)에서 가장 높은 성숙 단계의 특징은?",
        "choices": [
            "AI 도구를 처음 도입하여 단순 업무를 자동화한다",
            "부서별로 독립적인 AI 프로젝트를 시범 운영한다",
            "AI가 조직 전체 의사결정과 프로세스에 내재화되어 자기개선한다",
            "AI 윤리 가이드라인을 수립하고 교육을 시작한다"
        ],
        "answer": 3
    },
    {
        "question": "MCP(Model Context Protocol)의 역할은 무엇인가?",
        "choices": [
            "AI 모델의 학습 속도를 높이는 하드웨어 프로토콜이다",
            "AI 에이전트가 외부 도구·데이터에 표준화된 방식으로 연결하는 인터페이스다",
            "여러 AI 모델을 하나로 합치는 앙상블 알고리즘이다",
            "클라우드 서버 간 데이터를 암호화하는 보안 프로토콜이다"
        ],
        "answer": 2
    },
    {
        "question": "LLM(Large Language Model)이 '환각(Hallucination)'을 일으키는 근본 원인은?",
        "choices": [
            "인터넷 연결이 끊겼을 때 발생하는 오류다",
            "모델이 확률적으로 다음 토큰을 예측하는 방식이라 사실 검증 없이 그럴듯한 텍스트를 생성한다",
            "학습 데이터가 너무 많아 메모리가 초과되기 때문이다",
            "사용자가 질문을 너무 길게 입력하면 발생한다"
        ],
        "answer": 2
    },
    {
        "question": "AI 에이전트 설계에서 '검증 레이어(Validation Layer)'가 필요한 이유는?",
        "choices": [
            "에이전트 실행 속도를 높이기 위해서다",
            "AI 출력 비용을 줄이기 위해서다",
            "LLM 출력은 확률적이므로 자율 실행 전 결과의 정확성을 보장해야 한다",
            "사용자 인증을 처리하기 위해서다"
        ],
        "answer": 3
    },
]


# ============================================================================
# Quiz 클래스
#
# class (클래스) = 관련된 데이터(속성)와 기능(메서드)을 하나로 묶은 설계도
#   어원: class = "분류, 종류"라는 뜻의 라틴어 classis에서 유래.
#         같은 종류의 것들을 하나의 틀로 정의한다는 의미.
#   비유: 클래스는 "붕어빵 틀"이고, 객체(object)는 "틀로 찍어낸 붕어빵"이다.
#         틀(Quiz 클래스) 하나로 붕어빵(quiz1, quiz2, ...) 여러 개를 만들 수 있다.
#
# 이 클래스의 역할: 퀴즈 "1개"를 표현한다.
#   - 퀴즈 1개가 가지는 정보: 문제, 선택지, 정답
#   - 퀴즈 1개가 할 수 있는 행동: 자기를 화면에 보여주기, 정답 맞는지 확인하기
# ============================================================================

class Quiz:
    """퀴즈 1개를 표현하는 클래스."""

    # --------------------------------------------------------------------------
    # __init__ (이닛/이니트) = 초기화 메서드 (initialize = 처음 상태로 설정하다)
    #   어원: init = initialization의 줄임. 객체가 "태어날 때" 자동 호출된다.
    #   비유: 신입사원 첫날 사원증(이름, 부서, 사번)을 발급받는 것.
    #         Quiz 객체가 생성될 때 question, choices, answer를 "발급"받는다.
    #
    # 호출 시점: Quiz("문제", ["A","B","C","D"], 1) 이렇게 쓰면 자동으로 실행된다.
    #   Python이 내부적으로 Quiz.__init__(새객체, "문제", [...], 1)을 호출한다.
    #
    # self (셀프) = "이 객체 자신"을 가리키는 참조 변수
    #   비유: "나"라는 대명사. Quiz 카드 1장이 "내 문제는 이것, 내 정답은 저것"이라고
    #         자기 자신을 가리킬 때 사용한다.
    #   모든 메서드의 첫 번째 매개변수로 반드시 들어간다.
    #   호출할 때는 직접 넣지 않는다. Python이 자동으로 넣어 준다.
    #
    # 매개변수 (parameter) = 함수가 외부에서 받아들이는 입력값의 이름표
    #   question: str  = 문제 텍스트 (문자열 타입)
    #   choices: list  = 선택지 4개 (리스트 타입, 예: ["A", "B", "C", "D"])
    #   answer: int    = 정답 번호 (정수 타입, 1~4 중 하나)
    # --------------------------------------------------------------------------
    def __init__(self, question, choices, answer):
        self.question = question  # self.question = 이 퀴즈 객체의 "문제" 속성(attribute)에 전달받은 question 값을 저장
        self.choices = choices    # self.choices  = 이 퀴즈 객체의 "선택지" 속성에 전달받은 choices 값을 저장
        self.answer = answer      # self.answer   = 이 퀴즈 객체의 "정답" 속성에 전달받은 answer 값을 저장
        # 속성(attribute) = 객체가 가지고 있는 데이터. self.이름 형태로 저장하면
        #   이 객체가 살아있는 동안 어디서든 self.이름으로 꺼내 쓸 수 있다.

    # --------------------------------------------------------------------------
    # display() = 이 퀴즈의 문제와 선택지를 터미널에 출력하는 메서드
    # 메서드(method) = 클래스 안에 정의된 함수. 객체의 "행동"을 정의한다.
    #   비유: 퀴즈 카드의 "자기소개" 기능. "내 문제는 이것이고, 선택지는 이것입니다."
    # --------------------------------------------------------------------------
    def display(self):
        print(f"\n문제: {self.question}")
        # f"..." = f-string (formatted string literal, 포맷 문자열)
        #   중괄호 {} 안에 변수를 넣으면 그 값으로 치환된다.
        #   예: self.question이 "바이브코딩이란?"이면 -> "문제: 바이브코딩이란?"
        # \n = newline (줄바꿈 문자). 출력 전에 빈 줄을 하나 넣어 가독성을 높인다.

        for i, choice in enumerate(self.choices, start=1):
            print(f"  {i}. {choice}")
        # for = 반복문. self.choices 리스트의 각 항목을 하나씩 꺼내며 반복한다.
        # enumerate() = "열거하다". 리스트 항목에 번호를 자동으로 붙여 준다.
        #   enumerate(["A","B","C","D"], start=1) 결과:
        #   -> (1, "A"), (2, "B"), (3, "C"), (4, "D")
        #   i = 번호, choice = 해당 선택지 텍스트
        #   start=1: 번호를 0이 아니라 1부터 시작 (사용자에게 보여줄 때 자연스러움)
        #
        # 왜 for를 사용하는가?
        #   선택지가 4개로 정해져 있고, 각각에 대해 같은 동작(출력)을 반복하므로.
        #   print(f"  1. {self.choices[0]}") ... 4번 쓰는 것보다 깔끔하다.

    # --------------------------------------------------------------------------
    # check_answer() = 사용자가 입력한 번호가 정답과 일치하는지 확인하는 메서드
    # 반환값: bool (True = 정답, False = 오답)
    #   bool = Boolean (불리언). 참(True) 또는 거짓(False) 두 가지 값만 가지는 타입.
    #   어원: 19세기 수학자 George Boole의 이름에서 유래.
    # --------------------------------------------------------------------------
    def check_answer(self, user_input):
        return user_input == self.answer
        # == 비교 연산자: 왼쪽과 오른쪽이 같으면 True, 다르면 False를 반환한다.
        # 예: user_input이 2이고 self.answer가 2이면 -> True (정답)
        #     user_input이 3이고 self.answer가 2이면 -> False (오답)
        #
        # 왜 answer를 int로 저장하는가?
        #   str "2"와 int 2는 다르다. "2" == 2 -> False가 된다.
        #   get_int_input()에서 사용자 입력을 int로 변환하므로, 정답도 int로 맞춘다.

    # --------------------------------------------------------------------------
    # to_dict() = 이 Quiz 객체를 dict(딕셔너리)로 변환하는 메서드
    # 직렬화(Serialization) = 객체를 저장/전송 가능한 형태(텍스트)로 변환하는 것
    #   비유: 3D 물체를 택배로 보내려면 납작하게 분해해서 포장해야 한다.
    #         Quiz 객체(3D 물체)를 dict(납작한 포장)로 변환해야 JSON 파일에 저장할 수 있다.
    # 왜 필요한가?
    #   json.dump()는 Python 객체를 직접 저장할 수 없다.
    #   dict, list, str, int 같은 기본 타입만 JSON으로 변환 가능하다.
    #   Quiz 객체 -> dict로 변환 -> JSON으로 저장하는 2단계 과정이 필요하다.
    # --------------------------------------------------------------------------
    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    # --------------------------------------------------------------------------
    # @classmethod = 클래스 메서드 데코레이터
    #   decorator (데코레이터) = 함수/메서드에 추가 기능을 부여하는 문법. @로 표기.
    #     비유: 선물 포장. 내용물(함수)은 그대로인데, 포장지(@classmethod)를 씌우면
    #           "이 메서드는 객체가 아니라 클래스 자체에서 호출하는 것"이라는 의미가 추가된다.
    #
    # 일반 메서드 vs 클래스 메서드:
    #   일반 메서드: self (이미 만들어진 객체) 를 첫 매개변수로 받는다.
    #     예: quiz1.display()  -> quiz1이라는 "기존 객체"가 자기를 출력
    #   클래스 메서드: cls (클래스 자체) 를 첫 매개변수로 받는다.
    #     예: Quiz.from_dict(data)  -> Quiz "설계도" 자체에서 새 객체를 생성
    #
    # from_dict() = dict에서 Quiz 객체를 새로 만드는 "공장 메서드"
    #   비유: to_dict()가 "분해 포장"이라면, from_dict()는 "조립 설명서".
    #         택배로 받은 부품(dict)을 다시 원래 물체(Quiz 객체)로 조립한다.
    #   용도: state.json에서 읽어온 dict 데이터를 Quiz 객체로 복원할 때 사용한다.
    # --------------------------------------------------------------------------
    @classmethod
    def from_dict(cls, data):
        return cls(data["question"], data["choices"], data["answer"])
        # cls = Quiz 클래스 자체. cls(...) = Quiz(...)와 같다.
        # data["question"] = dict에서 "question" 키(key)에 해당하는 값(value)을 꺼낸다.
        # 결과적으로 Quiz(question값, choices값, answer값)을 호출하여 새 객체를 생성한다.


# ============================================================================
# QuizGame 클래스
#
# 이 클래스의 역할: 퀴즈 게임 "전체"를 관리한다.
#   - Quiz 클래스가 "퀴즈 카드 1장"이라면, QuizGame은 "카드 뭉치 + 게임 진행자"이다.
#   - 담당: 메뉴 표시, 퀴즈 풀기 진행, 퀴즈 추가, 목록 보기, 점수 관리, 파일 저장/불러오기
#
# 왜 Quiz와 QuizGame을 분리하는가? (역할 분리 원칙)
#   - Quiz: "나는 문제 하나다. 나를 보여주고, 정답을 확인해 줄 수 있다."
#   - QuizGame: "나는 게임 진행자다. 여러 퀴즈를 관리하고, 점수를 기록하고, 파일에 저장한다."
#   - 퀴즈가 100개가 되어도 Quiz 클래스 코드는 바뀌지 않는다.
#   - 게임 규칙이 바뀌어도 Quiz 클래스는 영향받지 않는다.
# ============================================================================

class QuizGame:
    """퀴즈 게임 전체를 관리하는 클래스."""

    def __init__(self):
        self.quizzes = []      # 퀴즈 목록. 빈 리스트로 시작. Quiz 객체들이 담긴다.
                               # [] = 빈 리스트 (empty list). 아직 아무것도 없는 상태.
        self.best_score = 0    # 역대 최고 점수. 0으로 시작 (아직 플레이 기록 없음).
        self.load_state()      # 생성 즉시 state.json에서 데이터를 불러온다.
                               # __init__ 안에서 다른 메서드를 호출할 수 있다.

    # --------------------------------------------------------------------------
    # load_state() = state.json 파일에서 데이터를 불러오는 메서드
    # "state" = 상태. 프로그램의 현재 상태(퀴즈 목록 + 최고 점수)를 의미한다.
    #
    # 3가지 상황을 처리한다:
    #   1. 파일 없음 (첫 실행)     -> 기본 퀴즈 데이터 사용
    #   2. 파일 있고 정상          -> 파일에서 읽어서 복원
    #   3. 파일 있지만 손상됨       -> 안내 메시지 출력 후 기본 데이터로 복구
    # --------------------------------------------------------------------------
    def load_state(self):
        if not os.path.exists(STATE_FILE):
            # os.path.exists() = 파일이 존재하는지 확인. True/False 반환.
            # not True = False, not False = True (논리 반전)
            # "파일이 존재하지 않으면" 이 블록 실행
            self._load_defaults()
            # _load_defaults(): 앞에 밑줄(_)이 붙은 메서드 = "내부용" 메서드
            #   관례상 "이 클래스 안에서만 쓰는 메서드"라는 의미.
            #   외부에서 호출하면 안 되는 것은 아니지만, "건드리지 마세요" 신호.
            print(f"기본 퀴즈 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개)")
            # len() = length (길이). 리스트 안의 항목 개수를 반환한다.
            return
            # return = 함수 실행을 여기서 중단하고 호출한 곳으로 돌아간다.
            # 파일이 없으면 아래 코드를 실행할 필요가 없으므로 여기서 끝낸다.

        # --- 파일이 존재하는 경우 ---
        try:
            # try/except = 오류가 발생할 수 있는 코드를 "시도"하는 구문
            #   비유: "일단 해보고, 문제가 생기면 대비책을 실행하자"
            #   try 블록: 정상 실행을 시도
            #   except 블록: 특정 오류가 발생했을 때 실행할 대비 코드

            with open(STATE_FILE, "r", encoding="utf-8") as f:
                # open() = 파일 열기 함수
                #   STATE_FILE = 열 파일의 경로
                #   "r" = read mode (읽기 모드). 파일을 읽기만 한다. (쓰기 불가)
                #         다른 모드: "w" = write (쓰기), "a" = append (추가)
                #   encoding="utf-8" = 파일의 문자 인코딩 방식 지정
                #     UTF-8 = Unicode Transformation Format 8-bit
                #     한글, 영어, 이모지 등 전 세계 문자를 표현하는 표준 인코딩.
                #     지정하지 않으면 Windows에서 한글이 깨질 수 있다.
                #   as f = 열린 파일 객체를 f라는 이름으로 사용하겠다.
                #
                # with 문 = 컨텍스트 매니저 (context manager)
                #   비유: "자동 문 닫기 장치". with 블록이 끝나면 파일이 자동으로 닫힌다.
                #   with 없이 open()을 쓰면 f.close()를 직접 호출해야 하는데,
                #   깜빡 잊으면 파일이 계속 열려 있어 문제가 생길 수 있다.
                #   with를 쓰면 오류가 발생하더라도 자동으로 닫아 준다.

                data = json.load(f)
                # json.load(f) = JSON 파일의 내용을 읽어 Python dict/list로 변환한다.
                # 예: {"quizzes": [...], "best_score": 3} -> Python dict

            self.quizzes = [Quiz.from_dict(q) for q in data.get("quizzes", [])]
            # 리스트 컴프리헨션 (list comprehension) = 리스트를 한 줄로 만드는 문법
            #   풀어쓰면:
            #   result = []
            #   for q in data.get("quizzes", []):
            #       result.append(Quiz.from_dict(q))
            #   self.quizzes = result
            #
            # data.get("quizzes", [])
            #   .get(키, 기본값) = dict에서 키에 해당하는 값을 꺼낸다.
            #   키가 없으면 기본값([])을 반환. data["quizzes"]와 다른 점:
            #   data["quizzes"]는 키가 없으면 KeyError 오류가 발생한다.
            #   .get()은 오류 없이 기본값을 반환하므로 더 안전하다.
            #
            # Quiz.from_dict(q) = 각 dict를 Quiz 객체로 변환 (위에서 설명한 "조립")

            self.best_score = data.get("best_score", 0)
            # best_score 키가 없으면 0을 기본값으로 사용

            if not self.quizzes:
                # 퀴즈 목록이 비어있으면 (파일에 quizzes가 빈 배열인 경우)
                self._load_defaults()

            print(f"저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {self.best_score}점)")

        except json.JSONDecodeError:
            # JSONDecodeError = JSON 파싱(해석) 실패 오류
            #   원인: state.json 파일이 손상된 경우
            #   예: 사용자가 메모장으로 열어 실수로 내용을 깨뜨렸을 때
            #   예: {"quizzes": [  <-- 여기서 끝나버린 불완전한 JSON
            print("저장 파일이 손상되었습니다. 기본 데이터로 초기화합니다.")
            self._load_defaults()

    # --------------------------------------------------------------------------
    # save_state() = 현재 퀴즈 목록과 최고 점수를 state.json 파일에 저장하는 메서드
    # 데이터 영속성(Data Persistence)을 담당한다.
    #   영속성 = 프로그램을 종료해도 데이터가 사라지지 않고 유지되는 성질.
    #   비유: 메모를 머릿속(메모리/변수)에만 두면 잠들면 잊어버린다.
    #         노트(파일)에 적어두면 다음날에도 볼 수 있다.
    #   save_state() = 머릿속 -> 노트 (변수 -> 파일)
    #   load_state() = 노트 -> 머릿속 (파일 -> 변수)
    # --------------------------------------------------------------------------
    def save_state(self):
        data = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            # 리스트 컴프리헨션: 각 Quiz 객체를 dict로 변환하여 리스트로 만든다.
            # Quiz 객체는 JSON으로 직접 저장할 수 없으므로 dict로 변환이 필요하다.
            "best_score": self.best_score,
        }
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            # "w" = write mode (쓰기 모드). 파일이 있으면 덮어쓰고, 없으면 새로 만든다.
            json.dump(data, f, ensure_ascii=False, indent=2)
            # json.dump(데이터, 파일, ...) = Python dict를 JSON 텍스트로 변환하여 파일에 쓴다.
            # ensure_ascii=False
            #   기본값 True이면 한글이 "\uD55C\uAE00" 같은 유니코드 코드로 저장된다.
            #   False로 설정하면 한글이 그대로 "한글"로 저장되어 사람이 읽을 수 있다.
            # indent=2
            #   JSON 출력 시 들여쓰기를 2칸으로 설정. 사람이 읽기 편하게 정리된다.
            #   없으면 한 줄로 쭉 이어붙여 저장되어 읽기 어렵다.

    # --------------------------------------------------------------------------
    # _load_defaults() = 기본 퀴즈 데이터를 불러오는 내부용 메서드
    # 호출 시점: 파일이 없거나, 파일이 손상되었을 때
    # --------------------------------------------------------------------------
    def _load_defaults(self):
        self.quizzes = [Quiz(**q) for q in DEFAULT_QUIZZES]
        # ** (더블 스타, double asterisk) = dict 언패킹 (unpacking, 풀기)
        #   Quiz(**{"question": "문제", "choices": [...], "answer": 2})
        #   이것은 아래와 완전히 같다:
        #   Quiz(question="문제", choices=[...], answer=2)
        #
        #   비유: 택배 상자(**)를 열어서 내용물을 하나하나 꺼내 전달하는 것.
        #   dict의 각 키-값 쌍을 함수의 매개변수로 풀어서 전달한다.
        self.best_score = 0

    # --------------------------------------------------------------------------
    # show_menu() = 메인 메뉴를 터미널에 출력하는 메서드
    # --------------------------------------------------------------------------
    def show_menu(self):
        print("\n=== AI 지식 퀴즈 게임 ===")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")

    # --------------------------------------------------------------------------
    # get_int_input() = 사용자에게서 정수(int) 입력을 안전하게 받는 메서드
    #
    # 왜 별도 메서드로 분리했는가?
    #   메뉴 선택(1~5), 정답 입력(1~4), 퀴즈 추가 시 정답 번호 입력(1~4) 등
    #   "숫자를 입력받고 검증하는 로직"이 여러 곳에서 반복된다.
    #   같은 코드를 3번 쓰는 대신, 한 번 정의하고 3번 호출한다.
    #   비유: 공장의 품질 검사 라인. 어떤 제품이든 같은 검사를 거치게 한다.
    #
    # 매개변수:
    #   prompt: str    = 사용자에게 보여줄 안내 문구 (예: "선택: ", "정답 번호 입력: ")
    #   min_val: int   = 허용 최솟값 (예: 1)
    #   max_val: int   = 허용 최댓값 (예: 5)
    # 반환값: int = 검증을 통과한 유효한 정수
    #
    # 처리하는 예외 케이스 4가지:
    #   1. 빈 입력 (그냥 Enter)          -> "입력이 없습니다"
    #   2. 숫자가 아닌 입력 (abc)        -> "숫자만 입력해 주세요"
    #   3. 범위 밖 숫자 (0, 9 등)        -> "1~5 범위의 숫자를 입력해 주세요"
    #   4. 정상 입력                     -> 값 반환 (루프 탈출)
    # --------------------------------------------------------------------------
    def get_int_input(self, prompt, min_val, max_val):
        while True:
            # while True = 무한 반복. 올바른 입력이 올 때까지 계속 반복한다.
            # 왜 while인가? 사용자가 언제 올바른 값을 입력할지 모르므로.
            # for는 "정해진 횟수"만큼 반복할 때 사용한다. 여기서는 부적합하다.

            raw = input(prompt).strip()
            # input(prompt) = 터미널에 prompt를 출력하고, 사용자 입력을 문자열로 받는다.
            # .strip() = 문자열 양쪽 끝의 공백/줄바꿈을 제거한다.
            #   예: "  2  " -> "2", "  " -> "" (빈 문자열)
            #   왜? 사용자가 실수로 스페이스를 넣어도 정상 처리하기 위해.

            if not raw:
                # not raw = raw가 "거짓 같은 값(falsy)"이면 True
                # 빈 문자열 ""은 Python에서 falsy(거짓 취급)이다.
                # 즉, 사용자가 아무것도 입력하지 않고 Enter만 누른 경우.
                print("입력이 없습니다. 다시 입력해 주세요.")
                continue
                # continue = 루프의 나머지 코드를 건너뛰고 while True 처음으로 돌아간다.
                # break과의 차이:
                #   continue = "이번 회차만 건너뛰고 루프 계속"
                #   break    = "루프 자체를 완전히 빠져나감"

            try:
                value = int(raw)
                # int() = 문자열을 정수로 변환하는 내장 함수
                #   예: "3" -> 3 (성공), "abc" -> ValueError 오류 발생
            except ValueError:
                # ValueError = 값 오류. int()가 변환할 수 없는 문자열일 때 발생.
                #   예: int("abc"), int("3.5"), int("")
                print("숫자만 입력해 주세요.")
                continue

            if not (min_val <= value <= max_val):
                # 파이썬 체이닝 비교: min_val <= value <= max_val
                # 풀어쓰면: min_val <= value and value <= max_val
                # 예: 1 <= 9 <= 5 -> 1 <= 9(True) and 9 <= 5(False) -> False
                # not False = True -> "범위 밖" 메시지 출력
                print(f"{min_val}~{max_val} 범위의 숫자를 입력해 주세요.")
                continue

            return value
            # 모든 검증을 통과한 값만 여기에 도달한다.
            # return = 함수를 종료하고 value를 호출한 곳에 돌려준다.
            # return이 실행되면 while True 루프도 자동으로 끝난다.

    # --------------------------------------------------------------------------
    # run() = 프로그램의 메인 루프. 프로그램 시작점.
    # 역할: 메뉴 출력 -> 사용자 입력 -> 해당 기능 실행 -> 반복
    # 비유: 음식점 카운터 직원. "주문하세요" -> 주문 받음 -> 주방에 전달 -> 다시 "주문하세요"
    # --------------------------------------------------------------------------
    def run(self):
        try:
            while True:
                # 무한 루프: 사용자가 "5. 종료"를 선택할 때까지 계속 반복
                self.show_menu()
                choice = self.get_int_input("선택: ", 1, 5)
                # get_int_input이 1~5 사이의 유효한 정수를 반환할 때까지
                # 내부에서 반복하므로, 여기서 choice는 항상 1~5 중 하나이다.

                if choice == 1:
                    self.play()         # 퀴즈 풀기
                elif choice == 2:
                    self.add_quiz()     # 퀴즈 추가
                elif choice == 3:
                    self.show_list()    # 퀴즈 목록
                elif choice == 4:
                    self.show_score()   # 점수 확인
                elif choice == 5:
                    print("저장 중...")
                    self.save_state()   # 종료 전 현재 상태를 파일에 저장
                    print("종료합니다.")
                    break               # while True 루프를 빠져나가 프로그램 종료

        except (KeyboardInterrupt, EOFError):
            # KeyboardInterrupt = 사용자가 Ctrl+C를 눌렀을 때 발생하는 예외
            #   Ctrl+C = 프로그램 강제 종료 단축키
            # EOFError = End Of File Error. 입력 스트림이 끝났을 때 발생.
            #   EOF = End Of File (파일 끝). 더 이상 읽을 데이터가 없다는 신호.
            #   예: 파이프된 입력이 끝났을 때, 또는 Ctrl+D(Mac/Linux)를 눌렀을 때
            #
            # 왜 처리하는가?
            #   처리하지 않으면 프로그램이 "비정상 종료"되어 에러 메시지가 출력된다.
            #   처리하면 데이터를 저장하고 깔끔하게 종료할 수 있다.
            print("\n저장 중...")
            self.save_state()
            print("종료합니다.")

    # --------------------------------------------------------------------------
    # play() = 퀴즈를 순서대로 출제하고 결과를 표시하는 메서드
    # --------------------------------------------------------------------------
    def play(self):
        if not self.quizzes:
            # 퀴즈 목록이 비어있으면 (빈 리스트 [] = falsy)
            print("등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return  # 메서드 즉시 종료. 아래 코드 실행하지 않음.

        score = 0                      # 이번 판의 점수. 0에서 시작.
        total = len(self.quizzes)      # 전체 문제 수
        print(f"\n총 {total}문제를 시작합니다.\n")

        for i, quiz in enumerate(self.quizzes, start=1):
            # i = 현재 문제 번호 (1부터), quiz = 현재 Quiz 객체
            print(f"[{i}/{total}]", end="")
            # end="" = print() 끝에 줄바꿈(\n) 대신 아무것도 넣지 않는다.
            # 기본값은 end="\n" (줄바꿈). ""로 바꾸면 다음 출력이 같은 줄에 이어진다.
            # 결과: "[1/7]" 다음에 quiz.display()의 출력이 바로 이어짐.

            quiz.display()             # 이 퀴즈의 문제와 선택지를 출력
            answer = self.get_int_input("정답 번호 입력: ", 1, 4)
            # 1~4 사이의 유효한 정수를 받을 때까지 내부에서 반복

            if quiz.check_answer(answer):
                # check_answer()가 True를 반환하면 (정답)
                print("정답입니다!")
                score += 1             # score = score + 1 의 축약. 1점 추가.
            else:
                # check_answer()가 False를 반환하면 (오답)
                print(f"오답입니다. 정답은 {quiz.answer}번이었습니다.")

        # for 루프가 끝난 후 (모든 문제를 다 풀었을 때)
        print(f"\n결과: {total}문제 중 {score}개 정답")

        if score > self.best_score:
            # 이번 점수가 역대 최고 점수보다 높으면
            print(f"최고 점수 갱신! {self.best_score} -> {score}")
            self.best_score = score    # 최고 점수 갱신
            self.save_state()          # 갱신된 점수를 파일에 즉시 저장

    # --------------------------------------------------------------------------
    # add_quiz() = 사용자에게 새 퀴즈를 입력받아 목록에 추가하는 메서드
    # --------------------------------------------------------------------------
    def add_quiz(self):
        print("\n=== 퀴즈 추가 ===")
        question = input("문제를 입력하세요: ").strip()
        # 문제 텍스트를 입력받고 양쪽 공백 제거

        if not question:
            # 빈 문자열이면 (사용자가 그냥 Enter를 누른 경우)
            print("문제를 입력하지 않아 취소합니다.")
            return  # 퀴즈 추가를 취소하고 메뉴로 돌아감

        choices = []  # 선택지를 담을 빈 리스트
        for i in range(1, 5):
            # range(1, 5) = [1, 2, 3, 4] 생성. 5는 포함하지 않는다.
            # 선택지 4개를 순서대로 입력받는다.
            while True:
                # 빈 입력 방지: 유효한 선택지가 들어올 때까지 반복
                choice = input(f"선택지 {i}: ").strip()
                if choice:
                    # 빈 문자열이 아니면 (무언가 입력했으면)
                    choices.append(choice)
                    # .append() = 리스트 맨 뒤에 항목을 추가하는 메서드
                    #   비유: 줄 맨 뒤에 사람이 서는 것.
                    #   choices가 ["A"]일 때 choices.append("B") -> ["A", "B"]
                    break  # while 루프 탈출. 다음 선택지 입력으로 넘어감.
                print("선택지를 입력해 주세요.")

        answer = self.get_int_input("정답 번호 (1~4): ", 1, 4)
        # 정답 번호를 1~4 범위에서 안전하게 입력받음

        new_quiz = Quiz(question, choices, answer)
        # 입력받은 데이터로 새 Quiz 객체를 생성한다.
        # Quiz.__init__(new_quiz, question, choices, answer)가 자동 호출된다.

        self.quizzes.append(new_quiz)
        # 기존 퀴즈 목록 뒤에 새 퀴즈를 추가

        self.save_state()
        # 추가된 퀴즈를 포함한 전체 데이터를 파일에 저장
        # 왜 바로 저장하는가? 프로그램이 갑자기 꺼져도 추가한 퀴즈가 살아있도록.

        print("퀴즈가 추가되었습니다.")

    # --------------------------------------------------------------------------
    # show_list() = 저장된 퀴즈 전체 목록을 출력하는 메서드
    # --------------------------------------------------------------------------
    def show_list(self):
        print("\n=== 퀴즈 목록 ===")
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        for i, quiz in enumerate(self.quizzes, start=1):
            print(f"{i}. {quiz.question}")
            # 각 퀴즈의 번호와 문제 텍스트만 출력 (선택지는 생략)

    # --------------------------------------------------------------------------
    # show_score() = 최고 점수를 표시하는 메서드
    # --------------------------------------------------------------------------
    def show_score(self):
        print("\n=== 점수 확인 ===")
        if self.best_score == 0:
            # 아직 한 번도 퀴즈를 풀지 않은 경우
            print("아직 플레이 기록이 없습니다.")
        else:
            print(f"최고 점수: {self.best_score} / {len(self.quizzes)}")
            # 예: "최고 점수: 5 / 7" (7문제 중 5개 정답)


# ============================================================================
# 프로그램 진입점 (Entry Point)
#
# if __name__ == "__main__":
#   이 조건의 의미: "이 파일이 직접 실행될 때만 아래 코드를 실행하라"
#
#   __name__ = Python이 자동으로 설정하는 특수 변수
#     - 파일을 직접 실행하면 (python main.py) : __name__ = "__main__"
#     - 다른 파일에서 import하면 (import main) : __name__ = "main"
#
#   왜 필요한가?
#     다른 파일에서 Quiz 클래스만 가져다 쓰고 싶을 때,
#     import만 했는데 게임이 바로 실행되면 곤란하다.
#     이 조건이 있으면 import 시에는 클래스 정의만 불러오고, 게임은 실행하지 않는다.
#
#   비유: 요리책의 "만드는 법" 페이지.
#     책을 읽기만 하면(import) 레시피 정보만 얻고,
#     직접 요리를 시작하면(python main.py) 실제로 음식을 만든다.
# ============================================================================

if __name__ == "__main__":
    game = QuizGame()
    # QuizGame() = QuizGame 클래스의 객체를 하나 생성한다.
    # __init__() 자동 호출 -> load_state() 실행 -> 데이터 불러오기 완료
    # game = 생성된 QuizGame 객체를 가리키는 변수

    game.run()
    # game 객체의 run() 메서드를 호출하여 게임 시작
    # run() 안의 while True 루프가 돌아가며, 사용자가 "5. 종료"를 선택하면 끝난다.
