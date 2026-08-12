# ============================================================================
# Mini NPU Simulator -- AI가 계산하는 방식을 흉내 내는 작은 계산기
#
# S01-codyssey Week3 Mission3 제출물
#
# NPU = Neural Processing Unit (신경망 처리 장치)
#   AI 연산만 전문으로 하는 칩. CPU가 "복잡한 일을 하나씩 순서대로" 처리한다면,
#   NPU는 "단순한 곱셈-덧셈을 수천 개 동시에" 처리한다.
#   비유: CPU는 만능 요리사 한 명, NPU는 감자만 깎는 알바생 1000명.
#         감자 1000개를 깎을 때 누가 빠른지는 명확하다.
#
# MAC = Multiply-Accumulate (곱하고-누적하다)
#   Multiply = 곱하다, Accumulate = 쌓아 모으다 (라틴어 accumulare = "쌓다")
#   두 숫자판을 겹쳐 놓고, 같은 자리끼리 곱한 뒤, 그 결과를 전부 더하는 연산.
#   이 프로그램이 흉내 내는 것이 바로 이 연산이다.
#
# 외부 라이브러리 사용 금지 (요구사항 6절).
#   NumPy, pandas 등은 물론 pip install이 필요한 모든 패키지를 쓰지 않는다.
#   아래 import 4개는 전부 Python에 기본 포함된 표준 라이브러리다.
# ============================================================================

import json  # json = JavaScript Object Notation (자바스크립트 객체 표기법)
             # data.json 파일을 Python dict로 읽어들이는 데 사용한다.
             # json.load(파일객체) = 파일 -> dict 변환

import os    # os = Operating System (운영체제)
             # 파일 경로를 운영체제에 맞게 계산하는 데 사용한다.
             # os.path.abspath / dirname / join / exists

import sys   # sys = System (시스템)
             # 명령줄 인자(--selftest)를 읽는 데 사용한다. sys.argv = 실행 시 넘어온 인자 목록

import time  # time = 시간
             # 연산 시간을 재는 데 사용한다. time.perf_counter() 설명은 measure_mac_ms() 참고


# ============================================================================
# 상수 (CONSTANT) 정의
# 상수 = 프로그램이 도는 동안 변하지 않는 값. 관례상 대문자로 쓴다.
# 왜 상수로 빼는가?
#   숫자가 코드 곳곳에 흩어져 있으면(= 매직 넘버) 나중에 기준을 바꿀 때
#   전부 찾아 고쳐야 하고, 하나라도 빠뜨리면 조용히 틀린다.
#   한 곳에 모아 두면 "정책을 바꾼다 = 이 줄을 고친다"가 된다.
# ============================================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# __file__ = 지금 실행 중인 이 파일(main.py) 자신을 가리키는 특수 변수
# os.path.abspath() = absolute path (절대 경로). 상대 경로를 전체 경로로 바꾼다.
# os.path.dirname() = directory name. 경로에서 파일명을 떼고 폴더 부분만 남긴다.
# 왜 이렇게 하는가?
#   사용자가 어느 폴더에서 `python main.py`를 실행하든,
#   data.json은 항상 main.py 옆에서 찾아야 하기 때문이다.

DATA_FILE = os.path.join(BASE_DIR, 'data.json')
# os.path.join() = 폴더 경로와 파일명을 운영체제 규칙에 맞게 이어 붙인다.
# 문자열 덧셈을 쓰지 않는 이유: Windows는 구분자가 \, macOS/Linux는 /라서
# 직접 이어 붙이면 한쪽 환경에서 깨진다. (이 과제는 Mac에서 동료평가를 받는다)

EPSILON = 1e-9
# epsilon(엡실론) = 그리스 문자 e. 수학에서 관례적으로 "아주 작은 양수"를 뜻한다.
# 여기서는 "이 정도 차이는 같은 값으로 친다"는 허용오차(tolerance) 기준이다.
# 1e-9 = 1 x 10의 -9제곱 = 0.000000001
# 요구사항 6절: abs(score_a - score_b) < 1e-9 이면 동점으로 간주한다.
# 왜 필요한가? -> decide() 함수의 주석에서 자세히 설명한다.

REPEAT = 10
# 성능 측정 시 MAC 연산을 몇 번 반복할지. 요구사항 최소 기준이 10회다.
# 왜 여러 번 재서 평균을 내는가?
#   컴퓨터는 이 프로그램만 돌리지 않는다. 다른 프로그램, 운영체제 작업이
#   끼어들면 어떤 한 번은 유난히 느리게 측정된다.
#   여러 번 재서 평균을 내면 이런 우연한 튐(noise)의 영향이 줄어든다.

LABEL_CROSS = 'Cross'  # 표준 라벨 1: 십자가 모양
LABEL_X = 'X'          # 표준 라벨 2: X 모양
LABEL_UNDECIDED = 'UNDECIDED'  # 판정 불가 (두 점수가 동점일 때)
# 표준 라벨(standard label) = 프로그램 내부에서 쓰기로 정한 "공식 이름"
# data.json에는 같은 뜻이 '+', 'x', 'cross' 등 여러 표기로 흩어져 있다.
# 이를 그대로 두고 비교하면 '+' == 'Cross'가 False가 되어 멀쩡한 정답이 오답이 된다.
# 그래서 읽어들이는 순간 두 가지 이름으로 통일한다. (normalize_label 참고)

LABEL_MAP = {
    '+': LABEL_CROSS,
    'cross': LABEL_CROSS,
    'plus': LABEL_CROSS,
    'x': LABEL_X,
}
# 정규화 대응표. 왼쪽(원본 표기) -> 오른쪽(표준 라벨)
# dict(딕셔너리) = 이름표(key)로 값(value)을 찾는 자료구조.
# 왜 if-elif 대신 dict를 쓰는가?
#   표기가 하나 늘어날 때 코드(분기문)가 아니라 데이터(표)만 고치면 되기 때문이다.

MANUAL_SIZE = 3
# 모드 1(사용자 입력)에서 다루는 행렬 크기. 요구사항이 3x3으로 지정.


# ----------------------------------------------------------------------------
# 3x3 내장 데이터
#
# 왜 코드 안에 넣는가?
#   요구사항은 성능 분석에 "3x3 포함, 5x5/13x13/25x25"를 요구한다.
#   그런데 data.json에는 size_5, size_13, size_25만 있고 size_3이 없다.
#   따라서 3x3 데이터는 프로그램이 직접 가지고 있어야 한다.
#   (보너스 과제인 "패턴 생성기"는 이번 범위에서 제외했으므로 고정 상수로 둔다)
#
# 십자가 필터: 가운데 세로줄과 가로줄이 1
#     0 1 0
#     1 1 1
#     0 1 0
# X 필터: 두 대각선이 1
#     1 0 1
#     0 1 0
#     1 0 1
# ----------------------------------------------------------------------------

BUILTIN_CROSS_3X3 = [
    [0.0, 1.0, 0.0],
    [1.0, 1.0, 1.0],
    [0.0, 1.0, 0.0],
]

BUILTIN_X_3X3 = [
    [1.0, 0.0, 1.0],
    [0.0, 1.0, 0.0],
    [1.0, 0.0, 1.0],
]


# ============================================================================
# 예외 클래스
#
# 예외(exception) = 정상 흐름에서 벗어난 상황을 알리는 신호.
# 사용자가 Ctrl+C를 누르거나 입력이 끊겼을 때, 프로그램을 죽이는 대신
# "사용자가 중단했다"는 신호로 바꿔 메뉴로 되돌리기 위해 직접 정의한다.
# ============================================================================

class UserAbort(Exception):
    """사용자가 입력 도중 중단(Ctrl+C 또는 입력 종료)했음을 알리는 예외."""
    pass


# ============================================================================
# Matrix 클래스  --  요구사항 F1 (데이터 구조)
#
# class(클래스) = 관련된 데이터와 기능을 하나로 묶은 설계도.
#   비유: 클래스는 "붕어빵 틀", 객체는 "틀로 찍어낸 붕어빵".
#
# 이 클래스의 역할: n x n 크기의 숫자판 "한 장"을 표현한다.
#   필터든 입력 패턴이든 결국 "정사각형 숫자판"이라는 점에서 완전히 같다.
#   그래서 타입을 둘로 나누지 않고 하나로 통일했다.
#   덕분에 MAC 함수가 mac(a, b) 형태로 대칭이 되고, 검증 코드도 한 벌만 있으면 된다.
#
# 요구사항 대응:
#   - "n x n 크기의 2차원 패턴 및 필터를 저장할 수 있어야 한다"      -> __init__, from_rows
#   - "특정 위치의 값을 저장하고 읽어올 수 있어야 한다"              -> get(), set()
#   - "최소 3x3, 5x5, 13x13, 25x25 크기를 처리할 수 있어야 한다"     -> 크기 제한 없음
# ============================================================================

class Matrix:
    """n x n 크기의 2차원 숫자판을 저장하고 위치별로 읽고 쓰는 자료구조."""

    # ------------------------------------------------------------------------
    # __init__ (이닛) = 초기화 메서드. 객체가 만들어질 때 자동으로 한 번 호출된다.
    #   init = initialization(초기화)의 줄임말.
    #
    # self(셀프) = "이 객체 자신"을 가리키는 참조.
    #   비유: "나"라는 대명사. 숫자판 한 장이 "내 내용은 이것"이라고 자기를 가리킬 때 쓴다.
    #   모든 메서드의 첫 번째 매개변수로 들어가며, 호출할 때는 직접 넘기지 않는다.
    #
    # 매개변수:
    #   rows: list -- 숫자가 담긴 2차원 리스트. 예: [[0,1,0],[1,1,1],[0,1,0]]
    #
    # 주의: 이 생성자는 검증을 하지 않는다. 검증은 from_rows()가 담당한다.
    #   왜 나누는가? -> 검증은 "바깥에서 들어온 값"에만 필요하다.
    #   프로그램 내부에서 이미 안전이 보장된 값까지 매번 검사하면 낭비다.
    #   그래서 "경계(파일 읽기 / 사용자 입력)에서만 검증한다"는 원칙을 따른다.
    # ------------------------------------------------------------------------
    def __init__(self, rows):
        self.rows = rows          # 2차원 리스트 원본을 그대로 보관
        self.size = len(rows)     # len() = length(길이). 행의 개수 = N (정사각형이므로 열 개수와 같다)

    # ------------------------------------------------------------------------
    # from_rows() = 2차원 리스트를 검증한 뒤 Matrix 객체로 만들어 주는 메서드
    #
    # @classmethod (클래스메서드) = 객체가 아니라 "클래스 자체"에 붙는 메서드.
    #   첫 인자가 self(객체)가 아니라 cls(클래스)다. cls = class의 줄임말.
    #   왜 쓰는가? 아직 객체가 없는 상태에서 "객체를 만들어 주는" 역할이기 때문이다.
    #   호출: Matrix.from_rows([[1,2],[3,4]])   <- 객체 없이 클래스 이름으로 바로 호출
    #
    # 검증 항목 (요구사항: 스키마/크기 오류를 걸러내야 한다)
    #   1. 리스트인가
    #   2. 비어 있지 않은가
    #   3. 모든 행의 길이가 행 개수와 같은가 (= 정사각형인가)
    #   4. 모든 값이 숫자(int 또는 float)인가
    #
    # 검증 실패 시 ValueError를 일으킨다.
    #   ValueError = "값이 잘못됐다"는 뜻의 파이썬 표준 예외.
    #   호출한 쪽이 이 예외를 받아 케이스 단위 FAIL로 처리한다.
    #   (프로그램 전체를 중단시키지 않는다 -- 요구사항 제약사항)
    # ------------------------------------------------------------------------
    @classmethod
    def from_rows(cls, rows):
        if not isinstance(rows, list):
            # isinstance(값, 타입) = 값이 그 타입인지 확인하는 내장 함수
            raise ValueError('2차원 배열(list)이 아닙니다.')

        if len(rows) == 0:
            raise ValueError('행이 비어 있습니다.')

        size = len(rows)  # 행 개수를 기준 크기 N으로 삼는다

        # enumerate() = "번호를 붙여 열거하다". (인덱스, 값) 쌍을 돌려준다.
        for row_index, row in enumerate(rows):
            if not isinstance(row, list):
                raise ValueError('{0}번째 행이 리스트가 아닙니다.'.format(row_index + 1))

            if len(row) != size:
                # 정사각형(n x n)이 아니면 거부한다. 요구사항이 n x n으로 한정.
                raise ValueError(
                    '정사각형이 아닙니다. 행 수={0}, {1}번째 행의 열 수={2}'.format(
                        size, row_index + 1, len(row)
                    )
                )

            for col_index, value in enumerate(row):
                # bool을 먼저 걸러내는 이유:
                #   파이썬에서 True/False는 내부적으로 1/0인 정수다.
                #   isinstance(True, int)가 True라서 그냥 두면 숫자로 통과해 버린다.
                #   숫자판에 참/거짓이 섞이는 것은 데이터 오류이므로 명시적으로 막는다.
                if isinstance(value, bool) or not isinstance(value, (int, float)):
                    raise ValueError(
                        '{0}행 {1}열의 값이 숫자가 아닙니다: {2!r}'.format(
                            row_index + 1, col_index + 1, value
                        )
                    )

        # 검증을 통과했으므로 모든 값을 float(실수)로 통일해 새 리스트를 만든다.
        # 왜 float으로 통일하는가?
        #   요구사항이 "연산 결과(점수, float 가능)"를 요구하고,
        #   data.json의 값도 실수이므로 타입을 하나로 맞춰 두면 비교/출력이 일관된다.
        # 왜 원본을 고치지 않고 새 리스트를 만드는가?
        #   원본(호출한 쪽의 리스트)을 건드리면, 그 리스트를 쓰는 다른 코드가
        #   자기도 모르게 영향을 받는다(= 부수효과). 새로 만들면 그런 일이 없다.
        converted = []
        for row in rows:
            converted.append([float(value) for value in row])
            # [식 for 항목 in 반복대상] = 리스트 컴프리헨션. 새 리스트를 만드는 축약 표현.
            # 여기서는 "값 변환"일 뿐 MAC 연산이 아니므로 사용해도 요구사항 위반이 아니다.
            # (요구사항이 금지한 것은 MAC 연산의 벡터화/라이브러리 대체다)

        return cls(converted)  # cls = Matrix. 즉 Matrix(converted)와 같다.

    # ------------------------------------------------------------------------
    # get() = r행 c열의 값을 읽어 온다  (요구사항: "특정 위치의 값을 ... 읽어올 수 있어야")
    #   매개변수: row(행 번호), col(열 번호). 둘 다 0부터 시작한다.
    #   비유: 사물함에서 "3층 5번 칸"을 지정해 물건을 꺼내는 것.
    # ------------------------------------------------------------------------
    def get(self, row, col):
        return self.rows[row][col]

    # ------------------------------------------------------------------------
    # set() = r행 c열에 값을 저장한다  (요구사항: "특정 위치의 값을 저장하고 ...")
    #   set은 파이썬 내장 자료형 이름과 겹치지만, 메서드 이름이라 충돌하지 않는다.
    # ------------------------------------------------------------------------
    def set(self, row, col, value):
        self.rows[row][col] = float(value)

    # ------------------------------------------------------------------------
    # same_size_as() = 다른 숫자판과 크기가 같은지 확인한다
    #   요구사항: "필터와 패턴의 크기가 일치하는지 검증해야 한다"
    #   MAC은 같은 자리끼리 곱하는 연산이므로, 크기가 다르면 애초에 계산이 성립하지 않는다.
    # ------------------------------------------------------------------------
    def same_size_as(self, other):
        return self.size == other.size


# ============================================================================
# 라벨 정규화  --  요구사항 F4 (라벨 정규화 필수 구현)
#
# normalize(노멀라이즈) = "정상화하다, 표준으로 맞추다"
#   norm = 라틴어 norma("직각자, 기준")에서 유래. 즉 "기준에 맞춘다"는 뜻이다.
#
# 왜 필요한가?
#   data.json은 같은 개념을 여러 이름으로 부른다.
#     - 패턴의 정답(expected)은 '+' 와 'x'
#     - 필터의 키(key)는 'cross' 와 'x'
#   이 상태로 비교하면 '+' == 'cross' 가 False다. 정답인데 오답으로 나온다.
#   즉 "로직은 맞는데 이름이 달라서 틀리는" 유형의 버그가 생긴다.
#
#   그래서 파일을 읽는 순간(= 시스템 경계에서) 이름을 두 가지로 통일한다.
#   그 뒤 내부 코드는 'Cross'와 'X'만 알면 된다.
#   비유: 여러 나라에서 온 서류의 날짜 표기를 접수처에서 한 형식으로 바꿔 두는 것.
#         부서마다 형식을 해석하게 두면 반드시 어딘가에서 어긋난다.
# ============================================================================

def normalize_label(raw):
    """원본 라벨 문자열을 표준 라벨(Cross/X)로 변환한다. 알 수 없으면 None을 돌려준다."""
    if not isinstance(raw, str):
        # 문자열이 아니면(숫자, None 등) 정규화할 수 없다.
        return None

    key = raw.strip().lower()
    # .strip()  = 문자열 앞뒤의 공백을 제거한다. (' X ' -> 'X')
    # .lower()  = 모두 소문자로 바꾼다. ('CROSS' -> 'cross')
    # 왜 하는가? 사람이 만든 데이터에는 공백과 대소문자가 섞이기 마련이다.
    #            이 두 줄로 그런 사소한 차이 때문에 생기는 오답을 미리 없앤다.

    return LABEL_MAP.get(key)
    # dict.get(키) = 키가 있으면 값을, 없으면 None을 돌려준다.
    # dict[키]와 달리 없는 키에서 예외를 일으키지 않는다.
    # 여기서는 "모르는 라벨"을 예외가 아니라 None으로 다뤄야 하므로 get()이 맞다.
    # (예외로 던지면 케이스 하나 때문에 프로그램 전체가 멈출 수 있다)


# ============================================================================
# MAC 연산  --  요구사항 F5 (외부 라이브러리 금지, 반복문 직접 구현)
# ============================================================================

def mac(matrix_a, matrix_b):
    """두 숫자판을 위치별로 곱한 뒤 전부 더한 값(MAC 점수)을 돌려준다.

    MAC = Multiply-Accumulate (곱하고 누적하다)

    계산 예 (3x3 십자 패턴 x 3x3 십자 필터):
        입력      필터       위치별 곱
        0 1 0     0 1 0      0  1  0
        1 1 1  x  1 1 1  =   1  1  1     -> 전부 더하면 5.0
        0 1 0     0 1 0      0  1  0

    비유: 두 장의 투명 필름을 정확히 겹쳐 놓고,
          같은 칸끼리 곱한 값을 하나씩 저금통에 넣어 마지막에 세는 것.
          "겹치는 부분이 많을수록 점수가 높다" = "모양이 비슷하다"

    주의: sum(), zip(), NumPy 등으로 축약하지 않는다.
          요구사항이 "반복문으로 직접 구현"을 명시하고 있고,
          축약하면 내부에서 무슨 일이 일어나는지 눈에 보이지 않기 때문이다.
    """
    total = 0.0  # accumulate(누적)할 그릇. 실수 덧셈이므로 0이 아니라 0.0으로 시작한다.
    size = matrix_a.size

    # 바깥 반복문: 행(row)을 위에서 아래로 훑는다
    for row in range(size):
        # 안쪽 반복문: 그 행의 열(col)을 왼쪽에서 오른쪽으로 훑는다
        for col in range(size):
            # Multiply(곱하기): 같은 위치의 두 값을 곱한다
            product = matrix_a.get(row, col) * matrix_b.get(row, col)
            # Accumulate(누적하기): 곱한 결과를 그릇에 더한다
            total = total + product

    # 반복 횟수 = size x size = N^2 번.
    # 이것이 시간 복잡도가 O(N^2)인 직접적인 이유다. (README 성능 분석 참고)
    return total


def measure_mac_ms(matrix_a, matrix_b, repeat=REPEAT):
    """MAC 연산을 repeat회 반복 측정하고, 1회 평균 소요 시간을 밀리초(ms)로 돌려준다.

    요구사항:
      - "크기별 MAC 연산 시간을 ms 단위로 측정해야 한다"
      - "각 크기별로 MAC 연산을 10회 반복 측정 후 평균 시간을 출력한다"
      - "I/O(입력/출력/파일 읽기) 시간을 제외하고 연산 함수 호출 구간 중심으로 측정"

    그래서 이 함수 안에는 print도, 파일 읽기도 없다. 오직 mac() 호출만 시간에 포함된다.

    time.perf_counter() = performance counter(성능 계수기)
      - 단조 증가(monotonic): 시스템 시계를 사람이 바꿔도 값이 뒤로 가지 않는다.
      - 고해상도: 아주 짧은 구간도 잴 수 있다.
      - time.time()을 쓰지 않는 이유: 그것은 "현재 몇 시인가"를 재는 함수라
        시계 보정이나 해상도 문제로 짧은 구간 측정에는 부적합하다.
      - 반환 단위는 초(second)다. 1초 = 1000밀리초이므로 1000을 곱해 ms로 바꾼다.
    """
    durations = []  # 매 회 측정값을 담을 리스트

    for _ in range(repeat):
        # _(밑줄) = "이 변수는 쓰지 않는다"는 관례적 이름. 반복 횟수만 필요할 때 쓴다.
        start = time.perf_counter()   # 측정 시작 시각
        mac(matrix_a, matrix_b)       # 측정 대상: MAC 연산 딱 한 번
        end = time.perf_counter()     # 측정 종료 시각
        durations.append((end - start) * 1000.0)  # 초 -> 밀리초 변환 후 기록

    return sum(durations) / len(durations)  # 평균 = 합계 / 개수
    # 여기서 sum()을 쓰는 것은 요구사항 위반이 아니다.
    # 금지 대상은 "MAC 연산"의 축약이며, 이것은 측정값의 평균 계산이다.


# ============================================================================
# 판정  --  요구사항 F6, F7 (epsilon 기반 동점 처리)
# ============================================================================

def decide(score_a, score_b, label_a, label_b, tie_label):
    """두 점수를 비교해 판정 라벨을 돌려준다. 차이가 EPSILON 미만이면 동점으로 본다.

    매개변수:
      score_a, score_b -- 비교할 두 MAC 점수 (실수)
      label_a, label_b -- 각각이 이겼을 때 돌려줄 이름 (모드1은 'A'/'B', 모드2는 'Cross'/'X')
      tie_label        -- 동점일 때 돌려줄 이름 (모드1은 '판정 불가', 모드2는 'UNDECIDED')

    왜 == 로 비교하면 안 되는가? (요구사항 과제목표 4번)
      컴퓨터는 실수를 2진법으로 저장한다. 그런데 0.1이나 0.9 같은 값은
      2진법으로 정확히 떨어지지 않는다. 10진법에서 1/3을 0.3333...으로밖에
      못 쓰는 것과 같은 문제다.
      그래서 저장할 때 아주 미세한 오차가 생기고, 이 오차는 더할수록 쌓인다.
      더하는 "순서"가 다르면 쌓이는 방식도 달라진다.

      실제로 이 과제의 data.json에는 수학적으로 정확히 같은 값인데
      계산 순서 때문에 다음처럼 어긋나는 케이스가 들어 있다.
          Cross 점수 = 0.9
          X     점수 = 0.8999999999999999
      두 값의 차이는 약 0.0000000000000001 (1.1e-16)이다.
      == 로 비교하면 "다르다"가 되고, 대소만 따지면 Cross가 이긴 것으로 처리된다.
      실제로는 어느 쪽도 이기지 않았으므로 이는 사실 왜곡이다.

      그래서 "이 정도 차이는 같다고 본다"는 허용오차(EPSILON) 기준을 세우고,
      그 안이면 어느 쪽도 이기지 않았다(동점)고 판정한다.
      비유: 100m 달리기에서 1억분의 1초 차이를 승부로 인정하지 않고 공동 1위로 두는 것.
    """
    difference = abs(score_a - score_b)
    # abs() = absolute value(절댓값). 부호를 떼고 크기만 본다.
    #         어느 쪽이 크든 "얼마나 떨어져 있는가"만 알면 되기 때문이다.

    if difference < EPSILON:
        return tie_label   # 동점: 판정 불가

    if score_a > score_b:
        return label_a     # A가 더 비슷하다

    return label_b         # B가 더 비슷하다


# ============================================================================
# 판정 결과 보관용 구조
#
# 계산 결과를 곧바로 화면에 뿌리지 않고 객체에 담아 두는 이유:
#   1) 마지막에 "총 몇 건 / 통과 몇 건 / 실패 몇 건"을 세려면 결과 목록이 필요하다.
#      화면에 출력만 하고 버리면 다시 계산해야 한다.
#   2) 계산 코드와 출력 코드를 분리하면, 출력 서식을 바꿔도 계산 로직은 그대로다.
# ============================================================================

class JudgeResult:
    """케이스 1건의 판정 결과."""

    def __init__(self, case_id, score_cross, score_x, verdict, expected, passed, reason):
        self.case_id = case_id          # 케이스 식별자 (예: 'size_5_1')
        self.score_cross = score_cross  # Cross 필터와의 MAC 점수 (오류 시 None)
        self.score_x = score_x          # X 필터와의 MAC 점수 (오류 시 None)
        self.verdict = verdict          # 판정 결과 ('Cross' / 'X' / 'UNDECIDED' / 'ERROR')
        self.expected = expected        # 정규화된 정답 라벨 (알 수 없으면 None)
        self.passed = passed            # 통과 여부 (True/False)
        self.reason = reason            # 실패 사유 요약 (통과 시 빈 문자열)


# ============================================================================
# 출력 서식 도우미
#
# 화면에 찍는 일만 담당하는 함수들을 한 곳에 모았다.
# 계산 함수(mac, decide 등)는 print를 절대 호출하지 않는다.
#   -> 성능 측정 구간에 화면 출력이 섞이면 측정값이 오염되기 때문이다.
# ============================================================================

def print_section(title):
    """요구사항 예시와 같은 형태의 구역 제목을 출력한다."""
    print('')
    print('#' + '-' * 45)
    print('# ' + title)
    print('#' + '-' * 45)


def format_score(value, expand=False):
    """점수를 문자열로 만든다.

    expand=True이면 소수점 이하 16자리까지 펼쳐 보여 준다.
    왜 펼치는가?
      동점 케이스에서 0.9와 0.8999999999999999를 그냥 반올림해 '0.9'로 찍으면
      두 값이 똑같아 보인다. 그러면 "왜 동점 판정이 났는지"를 화면에서 확인할 수 없다.
      부동소수점 오차를 눈으로 보는 것이 이 과제의 학습 목표 중 하나이므로 펼쳐서 보여 준다.
    """
    if value is None:
        return '-'
    if expand:
        return '{0:.16f}'.format(value)  # 소수점 이하 16자리 고정 표기
    return repr(value)
    # repr() = representation(표현). 파이썬이 그 값을 코드로 되살릴 수 있는 형태로 보여 준다.
    # float에 대해서는 "원래 값을 복원할 수 있는 최소 자릿수"로 출력한다.
    #   repr(5.0)                -> '5.0'
    #   repr(0.8999999999999999) -> '0.8999999999999999'
    # str()이나 반올림 서식과 달리 오차를 숨기지 않는다.


def print_matrix(title, matrix):
    """숫자판 내용을 화면에 보여 준다. 모드 1의 '저장 확인' 단계에서 사용한다."""
    print(title)
    for row in range(matrix.size):
        cells = []
        for col in range(matrix.size):
            # {0:g} = 불필요한 0을 떼고 간결하게 표시한다. 1.0 -> 1, 0.5 -> 0.5
            cells.append('{0:g}'.format(matrix.get(row, col)))
        print('  ' + ' '.join(cells))
        # ' '.join(리스트) = 리스트의 문자열들을 공백으로 이어 붙인다.


def print_perf_table(entries):
    """성능 분석표를 출력한다.  요구사항 F8-4

    표에 반드시 들어가야 하는 열 (요구사항):
      크기(N x N) / 평균 시간(ms) / 연산 횟수(N^2)

    entries: (크기N, 평균시간ms) 튜플의 리스트

    표 정렬에 대한 참고:
      한글은 터미널에서 두 칸을 차지하지만 파이썬의 문자열 길이 계산은 한 글자로 센다.
      그래서 제목 줄은 폭을 직접 계산해 고정 문자열로 두고,
      값 줄은 영문/숫자(한 칸짜리 문자)만 써서 어긋남이 생기지 않게 했다.
    """
    header = '크기(N×N)' + ' ' + ' ' * 3 + '평균 시간(ms)' + ' ' * 2 + '연산 횟수(N^2)'
    print(header)
    print('-' * 42)

    for size, avg_ms in entries:
        size_label = '{0}x{0}'.format(size)          # 예: '25x25'
        avg_label = '{0:.4f}'.format(avg_ms)          # 소수점 4자리. 3x3은 매우 짧아 3자리로는 0.000이 된다
        ops_label = '{0}'.format(size * size)         # 연산 횟수 = N^2
        print('{0:<10}{1:>16}{2:>16}'.format(size_label, avg_label, ops_label))
        # {0:<10} = 왼쪽 정렬, 폭 10칸
        # {1:>16} = 오른쪽 정렬, 폭 16칸 (숫자는 오른쪽 정렬이 자릿수 비교에 편하다)


# ============================================================================
# 모드 1: 사용자 입력 (3x3)  --  요구사항 F2, F10-2
# ============================================================================

def prompt(message):
    """한 줄 입력을 받는다. 사용자가 중단하면 UserAbort 예외로 바꿔 던진다.

    왜 감싸는가?
      input()은 Ctrl+C에서 KeyboardInterrupt를, 입력이 끊기면 EOFError를 일으킨다.
      그대로 두면 빨간 오류 메시지(트레이스백)가 쏟아지며 프로그램이 죽는다.
      요구사항은 "프로그램이 비정상 종료되면 안 된다"이므로,
      우리가 정의한 UserAbort로 바꿔 메뉴로 안전하게 되돌린다.
    """
    try:
        return input(message)
    except (EOFError, KeyboardInterrupt):
        # EOFError = End Of File(파일 끝). 입력이 더 이상 없을 때 발생한다.
        # KeyboardInterrupt = 사용자가 Ctrl+C를 눌렀을 때 발생한다.
        print('')
        raise UserAbort('사용자가 입력을 중단했습니다.')


def read_matrix_line(size, row_index):
    """행 한 줄을 입력받아 숫자 리스트로 돌려준다. 형식이 틀리면 안내 후 그 줄만 다시 받는다.

    요구사항 F2-3 검증 항목:
      - 열 개수 불일치  -> 안내 문구 출력 후 재입력
      - 숫자 파싱 실패  -> 안내 문구 출력 후 재입력

    왜 그 줄만 다시 받는가?
      한 줄 틀렸다고 처음부터 다시 시키면 사용자가 앞의 멀쩡한 줄까지 또 쳐야 한다.
      틀린 지점만 고치게 하는 것이 오류 복구의 기본이다.
    """
    error_message = '입력 형식 오류: 각 줄에 {0}개의 숫자를 공백으로 구분해 입력하세요.'.format(size)

    while True:  # 올바른 입력이 들어올 때까지 무한 반복 (return을 만나야 빠져나간다)
        raw = prompt('  [{0}행] '.format(row_index + 1))

        tokens = raw.split()
        # .split() = 문자열을 공백 기준으로 잘라 리스트로 만든다.
        #   '0 1 0'      -> ['0', '1', '0']
        #   '0    1   0' -> ['0', '1', '0']   (공백이 몇 개든 알아서 처리한다)
        #   ''           -> []                (빈 줄은 빈 리스트가 되어 개수 검증에서 걸린다)

        # 검증 1: 열 개수가 맞는가
        if len(tokens) != size:
            print(error_message)
            print('  (입력한 숫자 개수: {0}개)'.format(len(tokens)))
            continue  # continue = 이번 회차를 건너뛰고 while의 처음으로 돌아간다 -> 재입력

        # 검증 2: 전부 숫자로 바꿀 수 있는가
        values = []
        parse_failed = False
        for token in tokens:
            try:
                values.append(float(token))
                # float('0')   -> 0.0    (성공)
                # float('0.5') -> 0.5    (성공)
                # float('a')   -> ValueError 발생 (실패)
            except ValueError:
                print(error_message)
                print('  (숫자로 바꿀 수 없는 값: {0!r})'.format(token))
                parse_failed = True
                break  # break = 이 for 반복문을 즉시 빠져나간다 (나머지 토큰은 볼 필요 없다)

        if parse_failed:
            continue  # 재입력

        return values  # 두 검증을 모두 통과했으므로 결과를 돌려주고 while을 끝낸다


def read_matrix(name, size):
    """size줄을 입력받아 Matrix 객체로 만들어 돌려준다.

    행 수 검증에 대하여 (요구사항 "행 수/열 수 불일치 ... 재입력을 유도해야 한다"):
      이 함수는 size줄을 순차적으로 요구하고, 각 줄이 통과할 때까지 다음 줄로 넘어가지 않는다.
      따라서 사용자가 행 수를 틀릴 방법 자체가 없다(항상 정확히 size행이 만들어진다).
      한 줄에 숫자를 몰아 넣는 경우(예: 3x3인데 한 줄에 9개)는 열 수 검증에 걸려 재입력을 요구한다.
      즉 행 수는 구조적으로 보장하고, 열 수와 숫자 파싱은 read_matrix_line()이 줄 단위로 검증한다.
    """
    print('')
    print('{0} ({1}줄 입력, 공백 구분)'.format(name, size))

    rows = []
    for row_index in range(size):
        rows.append(read_matrix_line(size, row_index))

    # 각 줄이 이미 검증을 통과했으므로 from_rows는 사실상 통과가 보장된다.
    # 그래도 from_rows를 거치는 이유: 값 변환(float 통일)과 검증 경로를 한 곳으로 모으기 위해서다.
    return Matrix.from_rows(rows)


def run_manual_mode():
    """모드 1 전체 흐름을 실행한다.

    요구사항이 지정한 순서 (F10-2):
      필터 A, B 입력 -> 저장 확인 -> 패턴 입력 -> MAC 연산 -> 결과 판정 -> 성능 분석(3x3)
    """
    try:
        # ---- [1] 필터 입력 ----
        print_section('[1] 필터 입력')
        filter_a = read_matrix('필터 A', MANUAL_SIZE)
        filter_b = read_matrix('필터 B', MANUAL_SIZE)

        # ---- 저장 확인 (요구사항 실행 흐름에 명시된 단계) ----
        print('')
        print('[저장 확인] 입력한 필터가 아래와 같이 저장되었습니다.')
        print_matrix('필터 A ({0}x{0})'.format(filter_a.size), filter_a)
        print_matrix('필터 B ({0}x{0})'.format(filter_b.size), filter_b)

        # ---- [2] 패턴 입력 ----
        print_section('[2] 패턴 입력')
        pattern = read_matrix('패턴', MANUAL_SIZE)
        print('')
        print('[저장 확인] 입력한 패턴이 아래와 같이 저장되었습니다.')
        print_matrix('패턴 ({0}x{0})'.format(pattern.size), pattern)

    except UserAbort:
        print('입력을 중단했습니다. 메뉴로 돌아갑니다.')
        return

    # ---- [3] MAC 연산 및 판정 ----
    score_a = mac(pattern, filter_a)
    score_b = mac(pattern, filter_b)

    # 두 점수 차이가 EPSILON 미만이면 동점 -> 자릿수를 펼쳐 이유를 보여 준다
    is_tie = abs(score_a - score_b) < EPSILON
    verdict = decide(score_a, score_b, 'A', 'B', '판정 불가')

    # 연산 시간 측정 (요구사항: 평균/10회)
    avg_ms = measure_mac_ms(pattern, filter_a)

    print_section('[3] MAC 결과')
    print('A 점수: {0}'.format(format_score(score_a, expand=is_tie)))
    print('B 점수: {0}'.format(format_score(score_b, expand=is_tie)))
    print('연산 시간(평균/{0}회): {1:.4f} ms'.format(REPEAT, avg_ms))

    if is_tie:
        print('판정: {0} (|A-B| < {1})'.format(verdict, EPSILON))
    else:
        print('판정: {0}'.format(verdict))

    # ---- [4] 성능 분석 (3x3) ----
    print_section('[4] 성능 분석 (평균/{0}회)'.format(REPEAT))
    print_perf_table([(MANUAL_SIZE, avg_ms)])


# ============================================================================
# 모드 2: data.json 분석  --  요구사항 F3, F7, F8, F9, F10-3
# ============================================================================

def load_data(path):
    """data.json을 읽어 dict로 돌려준다. 실패하면 (None, 사유) 형태로 돌려준다.

    요구사항: 스키마 문제로 프로그램이 비정상 종료되면 안 된다.
    그래서 아래 세 가지 실패를 각각 구분해 사람이 읽을 수 있는 사유로 바꾼다.
      1) 파일이 없다
      2) JSON 문법이 깨졌다
      3) 최상위 키(filters / patterns)가 없다

    왜 구분하는가?
      "실패했습니다" 한 줄만 보여 주면 사용자는 무엇을 고쳐야 할지 알 수 없다.
      원인을 나누면 그대로 조치 방법이 된다. (파일 위치 확인 / 문법 확인 / 스키마 확인)
    """
    if not os.path.exists(path):
        return None, 'data.json 파일을 찾을 수 없습니다. 경로: {0}'.format(path)

    try:
        # with = 컨텍스트 매니저. 블록을 벗어나면 파일을 자동으로 닫아 준다.
        #        중간에 오류가 나도 닫히므로 파일이 열린 채 남지 않는다.
        # encoding='utf-8' = 한글이 포함될 수 있으므로 인코딩을 명시한다.
        #        생략하면 운영체제 기본값을 쓰는데, Windows와 Mac이 서로 달라 깨질 수 있다.
        with open(path, 'r', encoding='utf-8') as file_object:
            data = json.load(file_object)
    except ValueError as error:
        # ValueError를 잡는 이유: 여기서 나올 수 있는 예외가 두 종류이고, 둘 다 ValueError의 자식이다.
        #   1) json.JSONDecodeError -- JSON 문법이 깨졌을 때 (쉼표 누락, 괄호 불일치 등)
        #   2) UnicodeDecodeError   -- 파일이 UTF-8이 아닐 때
        #      (예: Windows 메모장이 기본 CP949로 저장한 경우, UTF-16으로 저장한 경우)
        # JSONDecodeError만 잡으면 인코딩이 다른 파일에서 프로그램이 트레이스백을 뿜고 죽는다.
        # 요구사항: "프로그램이 비정상 종료되면 안된다"
        return None, 'data.json을 읽을 수 없습니다 (인코딩 또는 JSON 형식 오류): {0}'.format(error)
    except OSError as error:
        # OSError = 권한 없음, 디스크 오류 등 파일 시스템 관련 문제
        return None, 'data.json을 읽는 중 오류가 발생했습니다: {0}'.format(error)

    if not isinstance(data, dict):
        return None, 'data.json의 최상위 구조가 객체(dict)가 아닙니다.'

    if 'filters' not in data or 'patterns' not in data:
        return None, "data.json에 필수 키가 없습니다. 'filters'와 'patterns'가 모두 필요합니다."

    return data, ''


def parse_case_size(case_id):
    """패턴 키에서 크기 N을 뽑아낸다. 'size_13_2' -> 13. 형식이 다르면 None.

    요구사항: "patterns의 각 항목에 대해, 키에서 N을 추출하여 해당 size_N 필터를 선택해야 한다"

    이 데이터에서는 키 이름 자체가 "어느 필터를 쓸지"를 가리키는 연결고리다.
    (데이터베이스로 치면 별도의 참조 컬럼이 없고 키 문자열 안에 들어 있는 구조다)
    """
    if not isinstance(case_id, str):
        return None

    parts = case_id.split('_')
    # 'size_13_2'.split('_') -> ['size', '13', '2']

    if len(parts) != 3 or parts[0] != 'size':
        return None  # 약속된 형식(size_{N}_{idx})이 아니다

    if not parts[1].isdecimal():
        # .isdecimal() = 문자열이 전부 "10진 숫자"로만 이루어졌는지 확인한다.
        #   '13'.isdecimal()  -> True
        #   '1a'.isdecimal()  -> False
        # int()로 바로 바꾸지 않고 먼저 확인하는 이유: 예외를 흐름 제어에 쓰지 않기 위해서다.
        #
        # 비슷한 .isdigit()을 쓰지 않는 이유:
        #   isdigit()은 위첨자 '²'(제곱 기호) 같은 문자도 True로 판정하는데,
        #   int('²')는 오류를 낸다. 즉 검사를 통과하고도 변환에서 죽는다.
        #   isdecimal()이 통과시키는 집합은 int()가 받는 집합과 정확히 일치한다.
        return None

    return int(parts[1])


def build_filter_sets(raw_filters):
    """필터를 로드하고 라벨을 정규화한다.

    돌려주는 값: (filter_sets, messages)
      filter_sets -- {5: {'Cross': Matrix, 'X': Matrix}, 13: {...}, 25: {...}}
      messages    -- 화면에 출력할 로드 결과 문자열 목록

    한 크기의 필터가 깨져 있어도 나머지는 계속 로드한다.
    (요구사항: 스키마 문제로 프로그램이 중단되면 안 된다)
    """
    filter_sets = {}
    messages = []

    if not isinstance(raw_filters, dict):
        messages.append('[FAIL] filters 항목이 객체(dict)가 아닙니다.')
        return filter_sets, messages

    # sorted() = 정렬. 출력 순서를 매 실행마다 같게 만들어 재현성을 확보한다.
    #   key=... 는 정렬 기준. size_5, size_13, size_25를 문자열로 정렬하면
    #   '13' < '25' < '5' 처럼 사전순이 되어 이상해지므로, 숫자 크기로 정렬한다.
    for size_key in sorted(raw_filters.keys(), key=lambda k: parse_filter_size(k) or 0):
        size = parse_filter_size(size_key)
        if size is None:
            messages.append('[FAIL] 필터 키 형식이 올바르지 않습니다: {0}'.format(size_key))
            continue

        raw_set = raw_filters[size_key]
        if not isinstance(raw_set, dict):
            messages.append('[FAIL] {0} 필터가 객체(dict)가 아닙니다.'.format(size_key))
            continue

        loaded = {}
        failed_reason = ''

        for raw_label in raw_set:
            # 라벨 정규화: 'cross' -> 'Cross', 'x' -> 'X'   (요구사항 F4-3)
            label = normalize_label(raw_label)
            if label is None:
                failed_reason = "알 수 없는 필터 라벨: '{0}'".format(raw_label)
                break

            try:
                loaded[label] = Matrix.from_rows(raw_set[raw_label])
            except ValueError as error:
                failed_reason = '{0} 필터 구조 오류: {1}'.format(raw_label, error)
                break

            # 필터 크기가 키에 적힌 크기와 실제로 같은지 확인한다.
            if loaded[label].size != size:
                failed_reason = '{0} 필터 크기 불일치: 키={1}, 실제={2}'.format(
                    raw_label, size, loaded[label].size
                )
                break

        if failed_reason:
            messages.append('[FAIL] {0} 필터 로드 실패 ({1})'.format(size_key, failed_reason))
            continue

        # 표준 라벨 두 개가 모두 있어야 판정이 가능하다.
        if LABEL_CROSS not in loaded or LABEL_X not in loaded:
            messages.append(
                '[FAIL] {0} 필터에 Cross/X가 모두 있어야 합니다. 발견: {1}'.format(
                    size_key, ', '.join(sorted(loaded.keys())) or '없음'
                )
            )
            continue

        filter_sets[size] = loaded
        messages.append('[OK] {0} 필터 로드 완료 (Cross, X)'.format(size_key))

    return filter_sets, messages


def parse_filter_size(filter_key):
    """필터 키에서 크기를 뽑아낸다. 'size_13' -> 13. 형식이 다르면 None."""
    if not isinstance(filter_key, str):
        return None

    parts = filter_key.split('_')
    # .isdecimal()을 쓰는 이유는 parse_case_size()의 주석 참고 (int()가 받는 집합과 정확히 일치)
    if len(parts) != 2 or parts[0] != 'size' or not parts[1].isdecimal():
        return None

    return int(parts[1])


def judge_case(case_id, raw_case, filter_sets):
    """케이스 1건을 판정해 JudgeResult로 돌려준다.

    요구사항:
      - 키에서 N을 추출해 해당 size_N 필터를 선택 (F3-3)
      - 필터와 패턴의 크기 일치 검증 (F3-4)
      - 불일치 시 FAIL 처리 + 원인 메시지, 프로그램 중단 금지 (F3-5)
      - 판정은 표준 라벨(Cross/X) 기준, expected와 비교해 PASS/FAIL (F4-4, F7-3)

    이 함수는 어떤 경우에도 예외를 바깥으로 내보내지 않는다.
    한 케이스가 깨져도 나머지 케이스는 계속 판정되어야 하기 때문이다.
    """
    # --- 검증 1: 케이스 구조 ---
    if not isinstance(raw_case, dict):
        return JudgeResult(case_id, None, None, 'ERROR', None, False,
                           '케이스 데이터가 객체(dict)가 아님')

    if 'input' not in raw_case:
        return JudgeResult(case_id, None, None, 'ERROR', None, False,
                           "필수 키 'input' 누락")

    if 'expected' not in raw_case:
        return JudgeResult(case_id, None, None, 'ERROR', None, False,
                           "필수 키 'expected' 누락")

    # --- 검증 2: 키에서 크기 N 추출 ---
    size = parse_case_size(case_id)
    if size is None:
        return JudgeResult(case_id, None, None, 'ERROR', None, False,
                           '패턴 키 형식 오류 (size_{N}_{idx} 형태여야 함)')

    # --- 검증 3: 해당 크기의 필터가 로드되어 있는가 ---
    if size not in filter_sets:
        return JudgeResult(case_id, None, None, 'ERROR', None, False,
                           'size_{0} 필터를 사용할 수 없음'.format(size))

    # --- 검증 4: 입력 패턴 구조 ---
    try:
        pattern = Matrix.from_rows(raw_case['input'])
    except ValueError as error:
        return JudgeResult(case_id, None, None, 'ERROR', None, False,
                           'input 구조 오류: {0}'.format(error))

    # --- 검증 5: 라벨 정규화 (expected: '+' -> Cross, 'x' -> X) ---
    expected = normalize_label(raw_case['expected'])
    if expected is None:
        return JudgeResult(case_id, None, None, 'ERROR', None, False,
                           "expected 라벨을 해석할 수 없음: {0!r}".format(raw_case['expected']))

    filter_cross = filter_sets[size][LABEL_CROSS]
    filter_x = filter_sets[size][LABEL_X]

    # --- 검증 6: 필터와 패턴의 크기 일치 (요구사항 F3-4) ---
    if not pattern.same_size_as(filter_cross):
        return JudgeResult(case_id, None, None, 'ERROR', expected, False,
                           '크기 불일치: 패턴={0}, 필터={1}'.format(pattern.size, filter_cross.size))

    # --- MAC 연산 (요구사항 F5) ---
    score_cross = mac(pattern, filter_cross)
    score_x = mac(pattern, filter_x)

    # --- 판정 (요구사항 F6, F7) ---
    verdict = decide(score_cross, score_x, LABEL_CROSS, LABEL_X, LABEL_UNDECIDED)

    # --- PASS/FAIL 비교는 반드시 표준 라벨끼리 (요구사항 F4-4) ---
    passed = (verdict == expected)

    if passed:
        reason = ''
    elif verdict == LABEL_UNDECIDED:
        reason = '동점(UNDECIDED) 처리 규칙 -- |Cross-X| < {0}'.format(EPSILON)
    else:
        reason = '판정({0})과 expected({1}) 불일치'.format(verdict, expected)

    return JudgeResult(case_id, score_cross, score_x, verdict, expected, passed, reason)


def print_case_result(result):
    """케이스 1건의 판정 결과를 출력한다. 요구사항 F7-2"""
    print('')
    print('--- {0} ---'.format(result.case_id))

    if result.verdict == 'ERROR':
        print('처리 실패: {0}'.format(result.reason))
        print('판정: ERROR | expected: {0} | FAIL'.format(result.expected or '-'))
        return

    # 동점일 때만 자릿수를 펼쳐 부동소수점 차이를 눈에 보이게 한다
    expand = (result.verdict == LABEL_UNDECIDED)

    print('Cross 점수: {0}'.format(format_score(result.score_cross, expand=expand)))
    print('X 점수: {0}'.format(format_score(result.score_x, expand=expand)))

    status = 'PASS' if result.passed else 'FAIL'
    line = '판정: {0} | expected: {1} | {2}'.format(result.verdict, result.expected, status)

    if not result.passed:
        line = line + ' ({0})'.format(result.reason)

    print(line)


def print_summary(results):
    """전체 결과를 요약해 출력한다. 요구사항 F9-1, F9-2"""
    total = len(results)
    passed = 0
    for result in results:
        if result.passed:
            passed = passed + 1
    failed = total - passed

    print('총 테스트: {0}개'.format(total))
    print('통과: {0}개'.format(passed))
    print('실패: {0}개'.format(failed))

    if failed == 0:
        print('')
        print('실패 케이스: 없음')
        return

    print('')
    print('실패 케이스:')
    for result in results:
        if not result.passed:
            print('- {0}: {1}'.format(result.case_id, result.reason))


def run_json_mode():
    """모드 2 전체 흐름을 실행한다.

    요구사항이 지정한 순서 (F10-3):
      필터 로드 -> 패턴 로드/검증 -> MAC 연산/판정/PASS-FAIL 출력
      -> 성능 분석(3x3 포함, 5x5/13x13/25x25) -> 결과 요약
    """
    # ---- [1] 필터 로드 ----
    print_section('[1] 필터 로드')

    data, error_message = load_data(DATA_FILE)
    if data is None:
        print(error_message)
        print('메뉴로 돌아갑니다.')
        return

    filter_sets, messages = build_filter_sets(data['filters'])
    for message in messages:
        print(message)

    if not filter_sets:
        print('')
        print('사용 가능한 필터가 없어 분석을 진행할 수 없습니다. 메뉴로 돌아갑니다.')
        return

    # ---- [2] 패턴 분석 ----
    print_section('[2] 패턴 분석 (라벨 정규화 적용)')

    raw_patterns = data['patterns']
    if not isinstance(raw_patterns, dict):
        print('patterns 항목이 객체(dict)가 아닙니다. 메뉴로 돌아갑니다.')
        return

    results = []
    for case_id in sorted(raw_patterns.keys(), key=sort_key_for_case):
        result = judge_case(case_id, raw_patterns[case_id], filter_sets)
        results.append(result)
        print_case_result(result)

    # ---- [3] 성능 분석 ----
    print_section('[3] 성능 분석 (평균/{0}회)'.format(REPEAT))

    entries = []

    # 3x3: data.json에 size_3이 없으므로 프로그램에 내장한 필터를 사용한다
    builtin_cross = Matrix.from_rows(BUILTIN_CROSS_3X3)
    builtin_x = Matrix.from_rows(BUILTIN_X_3X3)
    entries.append((MANUAL_SIZE, measure_mac_ms(builtin_cross, builtin_x)))

    # 5x5 / 13x13 / 25x25: 로드된 필터 쌍(Cross x X)으로 측정한다.
    # 어떤 값이 들어 있든 MAC의 연산 횟수는 N^2로 같으므로,
    # 크기에 따른 시간 변화를 보는 목적에는 이 조합으로 충분하다.
    for size in sorted(filter_sets.keys()):
        pair = filter_sets[size]
        entries.append((size, measure_mac_ms(pair[LABEL_CROSS], pair[LABEL_X])))

    print_perf_table(entries)

    # ---- [4] 결과 요약 ----
    print_section('[4] 결과 요약')
    print_summary(results)

    print('')
    print('(상세 원인 분석 및 복잡도 설명은 README.md의 "결과 리포트" 섹션 참고)')


def sort_key_for_case(case_id):
    """케이스 출력 순서를 정하는 기준. 크기 오름차순, 같은 크기면 이름순.

    왜 필요한가?
      dict의 키를 그냥 정렬하면 문자열 사전순이라 size_13이 size_5보다 앞에 온다.
      크기 순서대로 보여야 성능/난이도 흐름이 자연스럽다.
      또한 매 실행마다 순서가 같아야 재현성(같은 입력 -> 같은 출력)이 보장된다.
    """
    size = parse_case_size(case_id)
    if size is None:
        # 형식이 깨진 키는 맨 뒤로 보낸다. 큰 수를 주면 정렬에서 뒤로 밀린다.
        return (10 ** 9, case_id)
    return (size, case_id)


# ============================================================================
# 자체 점검 (--selftest)
#
# 요구사항이 요구하는 기능은 아니지만, 코어 로직이 맞는지 UI 없이 확인하는 수단이다.
# 외부 테스트 라이브러리(pytest 등)는 금지이므로 assert만 사용한다.
#   assert 조건, 메시지  ->  조건이 거짓이면 그 자리에서 오류를 내며 멈춘다.
# ============================================================================

def run_selftest():
    """코어 함수들이 정상 동작하는지 점검한다. 실패하면 assert가 즉시 알려 준다."""
    print('=== 자체 점검 (--selftest) ===')
    print('')

    # --- Matrix ---
    matrix = Matrix.from_rows([[1, 2], [3, 4]])
    assert matrix.size == 2, 'size 계산 오류'
    assert matrix.get(1, 0) == 3.0, 'get() 오류'
    matrix.set(1, 0, 9)
    assert matrix.get(1, 0) == 9.0, 'set() 오류'
    print('[OK] Matrix 저장 / get / set')

    # --- Matrix 검증 (정사각형이 아니거나 숫자가 아니면 거부) ---
    for bad_rows in ([[1, 2], [3]], [[1, 'a'], [3, 4]], [], [[True, 1], [0, 1]]):
        try:
            Matrix.from_rows(bad_rows)
            raise AssertionError('잘못된 입력을 통과시킴: {0!r}'.format(bad_rows))
        except ValueError:
            pass  # 기대한 동작: ValueError가 나야 정상
    print('[OK] Matrix 구조 검증 (비정사각/비숫자/빈값/bool 거부)')

    # --- 라벨 정규화 ---
    assert normalize_label('+') == LABEL_CROSS, "'+' 정규화 오류"
    assert normalize_label('cross') == LABEL_CROSS, "'cross' 정규화 오류"
    assert normalize_label(' X ') == LABEL_X, '공백 포함 정규화 오류'
    assert normalize_label('CROSS') == LABEL_CROSS, '대문자 정규화 오류'
    assert normalize_label('?') is None, '알 수 없는 라벨 처리 오류'
    assert normalize_label(None) is None, '문자열 아닌 값 처리 오류'
    print('[OK] 라벨 정규화 (+/cross -> Cross, x -> X)')

    # --- MAC ---
    cross = Matrix.from_rows(BUILTIN_CROSS_3X3)
    x_filter = Matrix.from_rows(BUILTIN_X_3X3)
    assert mac(cross, cross) == 5.0, '십자 x 십자 = 5.0 이어야 함'
    assert mac(cross, x_filter) == 1.0, '십자 x X = 1.0 이어야 함'
    assert mac(x_filter, x_filter) == 5.0, 'X x X = 5.0 이어야 함'
    print('[OK] MAC 연산 (십자x십자=5.0, 십자xX=1.0)')

    # --- 판정 ---
    assert decide(5.0, 1.0, 'A', 'B', 'TIE') == 'A', 'A 승리 판정 오류'
    assert decide(1.0, 5.0, 'A', 'B', 'TIE') == 'B', 'B 승리 판정 오류'
    assert decide(0.9, 0.8999999999999999, 'A', 'B', 'TIE') == 'TIE', '동점 판정 오류'
    assert decide(0.9, 0.8, 'A', 'B', 'TIE') == 'A', '유의미한 차이를 동점 처리함'
    print('[OK] epsilon({0}) 기반 동점 판정'.format(EPSILON))

    # --- 키 파싱 ---
    assert parse_case_size('size_13_2') == 13, '패턴 키 파싱 오류'
    assert parse_case_size('size_5_1') == 5, '패턴 키 파싱 오류'
    assert parse_case_size('bad_key') is None, '잘못된 키를 통과시킴'
    assert parse_case_size('size_a_1') is None, '숫자가 아닌 크기를 통과시킴'
    assert parse_filter_size('size_25') == 25, '필터 키 파싱 오류'
    assert parse_filter_size('size_') is None, '잘못된 필터 키를 통과시킴'
    print('[OK] 키 파싱 (size_{N}_{idx} -> N)')

    # --- 성능 측정 ---
    elapsed = measure_mac_ms(cross, x_filter, repeat=3)
    assert elapsed >= 0.0, '측정 시간이 음수'
    print('[OK] 성능 측정 (3회 평균 {0:.4f} ms)'.format(elapsed))

    # --- 케이스 판정 (정상 / 오류 흐름) ---
    sample_filters = {3: {LABEL_CROSS: cross, LABEL_X: x_filter}}

    good = judge_case('size_3_1', {'input': BUILTIN_CROSS_3X3, 'expected': '+'}, sample_filters)
    assert good.verdict == LABEL_CROSS and good.passed, '정상 케이스 판정 오류'

    bad_size = judge_case('size_3_2', {'input': [[1, 0], [0, 1]], 'expected': '+'}, sample_filters)
    assert not bad_size.passed and bad_size.verdict == 'ERROR', '크기 불일치 처리 오류'
    assert '크기' in bad_size.reason or '정사각' in bad_size.reason, '크기 오류 사유 누락'

    bad_label = judge_case('size_3_3', {'input': BUILTIN_CROSS_3X3, 'expected': '@'}, sample_filters)
    assert not bad_label.passed, '알 수 없는 expected를 통과시킴'

    missing = judge_case('size_9_1', {'input': BUILTIN_CROSS_3X3, 'expected': '+'}, sample_filters)
    assert not missing.passed, '없는 필터 크기를 통과시킴'
    print('[OK] 케이스 판정 및 오류 격리 (예외 없이 FAIL 처리)')

    print('')
    print('자체 점검 전 항목 통과.')


# ============================================================================
# 진입점 (entry point)
#
# 프로그램이 시작되는 지점. 요구사항 F10-1의 모드 선택 흐름을 담당한다.
# ============================================================================

def print_menu():
    """모드 선택 메뉴를 출력한다."""
    print('')
    print('[모드 선택]')
    print('1. 사용자 입력 (3x3)')
    print('2. data.json 분석')
    print('0. 종료')


def main():
    """프로그램 전체 흐름을 제어한다."""
    # sys.argv = 실행할 때 넘어온 인자 목록. sys.argv[0]은 파일 이름 자체다.
    # 예: python main.py --selftest  ->  ['main.py', '--selftest']
    if len(sys.argv) > 1 and sys.argv[1] == '--selftest':
        run_selftest()
        return

    print('=== Mini NPU Simulator ===')

    while True:
        print_menu()

        try:
            choice = prompt('선택: ').strip()
        except UserAbort:
            print('프로그램을 종료합니다.')
            return

        if choice == '1':
            run_manual_mode()
        elif choice == '2':
            run_json_mode()
        elif choice == '0':
            print('프로그램을 종료합니다.')
            return
        else:
            print("입력 오류: 0, 1, 2 중 하나를 입력하세요. (입력값: {0!r})".format(choice))


# ============================================================================
# if __name__ == '__main__':
#   __name__ = 파이썬이 자동으로 넣어 주는 특수 변수.
#     - 이 파일을 직접 실행하면 값이 '__main__'이 된다.
#     - 다른 파일에서 import하면 값이 모듈 이름('main')이 된다.
#   따라서 이 조건문은 "직접 실행할 때만 main()을 돌려라"는 뜻이다.
#   왜 필요한가? 나중에 이 파일의 함수를 다른 곳에서 가져다 쓸 때
#   프로그램이 제멋대로 실행되는 것을 막아 준다.
# ============================================================================

if __name__ == '__main__':
    main()
