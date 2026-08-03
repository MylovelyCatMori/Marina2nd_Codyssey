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
