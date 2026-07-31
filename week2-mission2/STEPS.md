# Mission2 단계별 가이드
## 컴퓨터에게 명령 내리는 말(파이썬) — 나만의 퀴즈 게임

> 각 단계 완료 후 체크박스 표시. 커밋 번호 기준 최소 10개 필요.

---

## STEP 0: 저장소 초기 설정
**목표**: 필수 파일 생성 + 첫 커밋
**레포**: Mission1과 동일한 `Marina2nd_Codyssey` 사용 (별도 repo 생성 없음)

### 0-1. 생성된 파일 확인
- `week2-mission2/.gitattributes` — LF 강제 (Mac 동료평가 대비)
- `week2-mission2/.gitignore` — Python 표준
- `week2-mission2/README.md` — 스켈레톤 (STEP 9에서 완성)
- `week2-mission2/STEPS.md` — 이 가이드 파일

### 0-2. 첫 커밋 + push
```bash
cd "D:/Projects/Codyssey with Claude"
git add week2-mission2/
git commit -m "Init: Mission2 week2-mission2 초기 설정 파일 추가"
git push origin main
```
- [ ] Commit #1 완료

---

## STEP 1: Quiz 클래스 구현
**목표**: 퀴즈 1개를 표현하는 클래스 작성

### 파일: `main.py`
구현할 것:
- `Quiz` 클래스
  - 속성: `question` (str), `choices` (list, 4개), `answer` (int, 1~4)
  - 메서드: `display()` — 문제+선택지 출력
  - 메서드: `check_answer(user_input)` — 정답 여부 bool 반환

```bash
git add main.py
git commit -m "Feat: Quiz 클래스 구현 (question/choices/answer/display/check)"
```
- [ ] Commit #2 완료

---

## STEP 2: 기본 퀴즈 데이터 작성
**목표**: 본인 주제 퀴즈 5개 이상 직접 작성

### 퀴즈 주제 결정 (먼저 정할 것)
- 제약/GMP 추천 (현장 배경 활용)
- 또는 자유 선택

### 구현할 것
- `main.py` 내 `DEFAULT_QUIZZES` 리스트 또는 함수
- `Quiz` 인스턴스 5개 이상 생성
- 각각 문제/선택지 4개/정답 번호 포함

```bash
git add main.py
git commit -m "Feat: 기본 퀴즈 데이터 5개 추가 (주제: [주제명])"
```
- [ ] Commit #3 완료

---

## STEP 3: QuizGame 클래스 뼈대 + state.json 입출력
**목표**: 게임 전체 관리 클래스 + 파일 저장/불러오기

### 구현할 것
- `QuizGame` 클래스
  - 속성: `quizzes` (list), `best_score` (int)
  - 메서드: `load_state()` — state.json 읽기
  - 메서드: `save_state()` — state.json 쓰기
- 예외 처리:
  - 파일 없음 → 기본 데이터 사용
  - 파일 손상(JSONDecodeError) → 안내 메시지 + 기본 데이터로 초기화

### state.json 스키마
```json
{
    "quizzes": [...],
    "best_score": 0
}
```

```bash
git add main.py
git commit -m "Feat: QuizGame 클래스 뼈대 및 state.json 저장/불러오기 구현"
```
- [ ] Commit #4 완료

---

## STEP 4: 메뉴 기능 + 공통 입력 예외 처리
**목표**: 실행 시 메뉴 출력, 입력 처리, 안전한 종료

### 구현할 것
- `QuizGame.show_menu()` — 메뉴 출력
- `QuizGame.run()` — 메인 루프 (while True)
- 공통 입력 처리:
  - 앞뒤 공백 제거 (`.strip()`)
  - 빈 입력 → 재입력 안내
  - 문자 입력(abc) → 재입력 안내
  - 범위 밖 숫자 → 재입력 안내
- `KeyboardInterrupt` / `EOFError` → 저장 후 안전 종료

```bash
git add main.py
git commit -m "Feat: 메뉴 기능 및 공통 입력/예외 처리 구현"
```
- [ ] Commit #5 완료

---

## STEP 5: 퀴즈 풀기 기능 (브랜치 필수)
**목표**: 브랜치 생성 후 퀴즈 출제 기능 구현, main으로 병합

### 브랜치 생성
```bash
git checkout -b feature/play
```

### 구현할 것
- `QuizGame.play()` 메서드
  - 퀴즈 없을 때 처리
  - 각 문제 표시 → 정답 입력 → 정답/오답 알림
  - 전체 완료 후 결과 표시 (총점)
  - 최고 점수 갱신 시 알림

```bash
git add main.py
git commit -m "Feat: 퀴즈 풀기 기능 구현 (정답 확인/결과 표시/최고점수 갱신)"
git checkout main
git merge feature/play
git push origin main
```
- [ ] Commit #6 (브랜치) + Commit #7 (merge) 완료
- [ ] `checkout` 명령어 사용 체크
- [ ] `merge` 사용 체크

---

## STEP 6: 퀴즈 추가 기능
**목표**: 새 퀴즈 등록 후 state.json에 저장

### 구현할 것
- `QuizGame.add_quiz()` 메서드
  - 문제 입력
  - 선택지 4개 입력
  - 정답 번호(1~4) 입력 + 예외 처리
  - `Quiz` 인스턴스 생성 후 `self.quizzes`에 추가
  - `save_state()` 호출

```bash
git add main.py
git commit -m "Feat: 퀴즈 추가 기능 구현 및 state.json 자동 저장"
```
- [ ] Commit #8 완료

---

## STEP 7: 퀴즈 목록 기능
**목표**: 저장된 퀴즈 전체 목록 출력

### 구현할 것
- `QuizGame.show_list()` 메서드
  - 퀴즈 없을 때: 안내 메시지
  - 있을 때: 번호 + 문제 텍스트 목록 출력

```bash
git add main.py
git commit -m "Feat: 퀴즈 목록 기능 구현"
```
- [ ] Commit #9 완료

---

## STEP 8: 점수 확인 기능
**목표**: 최고 점수 표시

### 구현할 것
- `QuizGame.show_score()` 메서드
  - 아직 플레이 안 한 경우(best_score == 0) 처리
  - 최고 점수 + 총 문제 수 표시

```bash
git add main.py
git commit -m "Feat: 점수 확인 기능 구현 (최고 점수 표시)"
```
- [ ] Commit #10 완료 (최소 요구 달성!)

---

## STEP 9: README.md 완성 + 스크린샷
**목표**: 제출 체크리스트 모든 항목 채우기

### README.md 필수 항목
- [ ] 프로젝트 개요
- [ ] 퀴즈 주제 선정 이유
- [ ] 실행 방법 (`python main.py`)
- [ ] 기능 목록
- [ ] 파일 구조
- [ ] state.json 설명 (경로/역할/스키마)

### 스크린샷 (docs/screenshots/)
- [ ] `menu.png` — 메뉴 화면
- [ ] `play.png` — 퀴즈 풀기 화면
- [ ] `add_quiz.png` — 퀴즈 추가 화면
- [ ] `score.png` — 점수 확인 화면

```bash
git add README.md docs/
git commit -m "Docs: README 완성 및 실행 화면 스크린샷 추가"
git push origin main
```
- [ ] Commit #11 완료

---

## STEP 10: Clone/Pull 실습
**목표**: `clone`과 `pull` 각 1회 이상 사용 기록

### 순서
```bash
# 1. 별도 디렉토리에 clone
cd D:/Projects
git clone https://github.com/<계정>/codyssey-p1-mission2.git codyssey-p1-mission2-clone

# 2. clone된 폴더에서 변경 후 commit + push
cd codyssey-p1-mission2-clone
# README.md 맨 아래에 한 줄 추가 (예: "# Clone/Pull 실습 완료")
git add README.md
git commit -m "Docs: clone/pull 실습용 변경"
git push origin main

# 3. 원래 작업 폴더에서 pull
cd "D:/Projects/Codyssey with Claude/week2-mission2"
git pull origin main
```
- [ ] `clone` 사용 체크
- [ ] `pull` 사용 체크

---

## 제출 전 최종 체크리스트

### Git 필수 명령어 7종 사용 확인
- [ ] `git init` (STEP 0)
- [ ] `git add` (전 단계)
- [ ] `git commit` (전 단계)
- [ ] `git push` (STEP 0, 5, 9)
- [ ] `git pull` (STEP 10)
- [ ] `git checkout` (STEP 5)
- [ ] `git clone` (STEP 10)

### 최소 요구사항 확인
- [ ] 커밋 10개 이상
- [ ] 브랜치 생성 + merge 1회 이상
- [ ] 퀴즈 5개 이상
- [ ] Quiz + QuizGame 클래스 2개 이상
- [ ] state.json 영속성 동작
- [ ] README.md 항목 완비

### 제출물
- [ ] GitHub 저장소 URL
- [ ] 개발 환경 스크린샷 (Python 버전, Git 설정)
- [ ] 실행 결과 스크린샷 4장
- [ ] `git log --oneline --graph` 스크린샷
