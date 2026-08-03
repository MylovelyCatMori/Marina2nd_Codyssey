import json
import os

STATE_FILE = "state.json"

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


class Quiz:
    """퀴즈 1개를 표현하는 클래스."""

    def __init__(self, question, choices, answer):
        self.question = question  # 문제 텍스트 (str)
        self.choices = choices    # 선택지 4개 (list[str])
        self.answer = answer      # 정답 번호 1~4 (int)

    def display(self):
        """문제와 선택지를 출력한다."""
        print(f"\n문제: {self.question}")
        for i, choice in enumerate(self.choices, start=1):
            print(f"  {i}. {choice}")

    def check_answer(self, user_input):
        """사용자 입력이 정답인지 확인한다. bool 반환."""
        return user_input == self.answer

    def to_dict(self):
        """직렬화용 dict 반환."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    @classmethod
    def from_dict(cls, data):
        """dict에서 Quiz 인스턴스 생성."""
        return cls(data["question"], data["choices"], data["answer"])


class QuizGame:
    """퀴즈 게임 전체를 관리하는 클래스."""

    def __init__(self):
        self.quizzes = []
        self.best_score = 0
        self.load_state()

    def load_state(self):
        """state.json에서 퀴즈 목록과 최고 점수를 불러온다."""
        if not os.path.exists(STATE_FILE):
            self._load_defaults()
            return
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.quizzes = [Quiz.from_dict(q) for q in data.get("quizzes", [])]
            self.best_score = data.get("best_score", 0)
            if not self.quizzes:
                self._load_defaults()
        except json.JSONDecodeError:
            print("저장 파일이 손상되었습니다. 기본 데이터로 초기화합니다.")
            self._load_defaults()

    def save_state(self):
        """현재 퀴즈 목록과 최고 점수를 state.json에 저장한다."""
        data = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "best_score": self.best_score,
        }
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _load_defaults(self):
        """기본 퀴즈 데이터를 불러온다."""
        self.quizzes = [Quiz(**q) for q in DEFAULT_QUIZZES]
        self.best_score = 0

    def show_menu(self):
        """메인 메뉴를 출력한다."""
        print("\n=== AI 지식 퀴즈 게임 ===")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")

    def get_int_input(self, prompt, min_val, max_val):
        """정수 입력을 받는다. 범위 밖/빈 입력/문자 입력 시 재입력 안내."""
        while True:
            raw = input(prompt).strip()
            if not raw:
                print("입력이 없습니다. 다시 입력해 주세요.")
                continue
            try:
                value = int(raw)
            except ValueError:
                print("숫자만 입력해 주세요.")
                continue
            if not (min_val <= value <= max_val):
                print(f"{min_val}~{max_val} 범위의 숫자를 입력해 주세요.")
                continue
            return value

    def run(self):
        """메인 루프. KeyboardInterrupt/EOFError 발생 시 저장 후 종료."""
        try:
            while True:
                self.show_menu()
                choice = self.get_int_input("선택: ", 1, 5)
                if choice == 1:
                    self.play()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.show_list()
                elif choice == 4:
                    self.show_score()
                elif choice == 5:
                    print("저장 중...")
                    self.save_state()
                    print("종료합니다.")
                    break
        except (KeyboardInterrupt, EOFError):
            print("\n저장 중...")
            self.save_state()
            print("종료합니다.")

    def play(self):
        """퀴즈를 순서대로 출제하고 결과를 표시한다."""
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return

        score = 0
        total = len(self.quizzes)
        print(f"\n총 {total}문제를 시작합니다.\n")

        for i, quiz in enumerate(self.quizzes, start=1):
            print(f"[{i}/{total}]", end="")
            quiz.display()
            answer = self.get_int_input("정답 번호 입력: ", 1, 4)
            if quiz.check_answer(answer):
                print("정답입니다!")
                score += 1
            else:
                print(f"오답입니다. 정답은 {quiz.answer}번이었습니다.")

        print(f"\n결과: {total}문제 중 {score}개 정답")

        if score > self.best_score:
            print(f"최고 점수 갱신! {self.best_score} -> {score}")
            self.best_score = score
            self.save_state()

    def add_quiz(self):
        """새 퀴즈를 입력받아 목록에 추가하고 저장한다."""
        print("\n=== 퀴즈 추가 ===")
        question = input("문제를 입력하세요: ").strip()
        if not question:
            print("문제를 입력하지 않아 취소합니다.")
            return

        choices = []
        for i in range(1, 5):
            while True:
                choice = input(f"선택지 {i}: ").strip()
                if choice:
                    choices.append(choice)
                    break
                print("선택지를 입력해 주세요.")

        answer = self.get_int_input("정답 번호 (1~4): ", 1, 4)

        new_quiz = Quiz(question, choices, answer)
        self.quizzes.append(new_quiz)
        self.save_state()
        print("퀴즈가 추가되었습니다.")

    def show_list(self):
        """저장된 퀴즈 전체 목록을 출력한다."""
        print("\n=== 퀴즈 목록 ===")
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return
        for i, quiz in enumerate(self.quizzes, start=1):
            print(f"{i}. {quiz.question}")

    def show_score(self):
        """최고 점수를 표시한다."""
        print("\n=== 점수 확인 ===")
        if self.best_score == 0:
            print("아직 플레이 기록이 없습니다.")
        else:
            print(f"최고 점수: {self.best_score} / {len(self.quizzes)}")


if __name__ == "__main__":
    game = QuizGame()
    game.run()
