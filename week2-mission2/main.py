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
