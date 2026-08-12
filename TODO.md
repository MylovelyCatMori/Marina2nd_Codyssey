# TODO - Codyssey with Claude

최종 업데이트: 2026-08-03

---

## 일반사항 (프로젝트 운영)

### 즉시
- [x] GitHub 저장소 생성 후 이 프로젝트 연동 (동료평가 제출 필수) -- Marina2nd_Codyssey
- [x] git config core.autocrlf false 설정 확인

### 운영 중 지속
- [ ] 미션 완료시 decision-log/phase1-decisions.md에 트러블슈팅 append
- [ ] 단계(phase) 완료 후 archive/ 이관
- [ ] knowledge/ 개념 파일 미션별 누적 기록 유지

### 레포 전략 (재검토 필요)
- 기본: 단일 레포 `Marina2nd_Codyssey` (master 브랜치)
- 동료평가용: 미션별 별도 레포 `codyssey-p1-mission2` 등 (main 브랜치, 평가 시스템 연동)
- 미결정: 앞으로도 별도 레포를 매번 만들지, 단일 레포로 통일할지 추후 결정

---

## Week & Mission

### Week1 Mission1 - 개발 워크스페이스 구축 (완료)

**실습 수행** (캡쳐 규칙: 명령어 입력 + 출력 결과 반드시 함께 포함)
- [x] 터미널 기본 조작 (pwd, ls -la, mkdir, cp, mv, rm) -- 출력 결과 README 코드블록 기록
- [x] 권한 변경 실습 (chmod 644/755) -- [📸필수] 변경 전/후 ls -la 비교 (ubuntu 컨테이너에서 수행)
- [x] Docker 설치 확인 (docker --version, docker info) -- v29.6.2, README에 출력 기록
- [x] hello-world 컨테이너 실행 -- 출력 결과 README 코드블록 기록
- [x] ubuntu 컨테이너 진입 및 ls, echo 실행 -- 출력 결과 기록
- [x] docker images / docker ps -a / docker logs / docker stats -- 출력 결과 기록
- [x] Dockerfile 빌드 (my-web:1.0) -- 빌드 명령+출력 기록, [📸선택] 터미널 스크린샷
- [x] 포트 매핑 실행 -- [📸필수] 브라우저 화면 (주소창에 포트 포함, localhost:8080)
- [x] 바인드 마운트 반영 확인 -- [📸필수] 호스트 파일 변경 전/후 브라우저/curl 비교
- [x] Docker 볼륨 영속성 검증 -- [📸필수] 컨테이너 삭제 전/후 데이터 유지 증명
- [x] git config --list 출력 결과 기록 -- README 코드블록 또는 터미널 스크린샷
- [x] GitHub 저장소 연동 -- [📸필수] VSCode GitHub 로그인 + 저장소 연동 화면 -- 2026-07-29 완료

**문서 완성**
- [x] week1-mission1/README.md 실제 출력 결과 채우기
- [x] 트러블슈팅 Case 최소 2건 작성
- [x] 프로젝트 개요 섹션 추가
- [x] 컨테이너 종료/유지 차이 정리 추가
- [x] 스크린샷 4장 README에 첨부

**검증 & 제출**
- [x] 위 커밋+push 완료 (프로젝트 개요/컨테이너 차이 추가분)
- [x] `/grill-with-docs` 로 핵심 개념 검증 + MD 저장 (Docker 컨테이너/볼륨/포트매핑) -- 2026-07-29 Q1~Q6 완료
- [x] knowledge/phase1-concepts.md 실제 내용으로 업데이트 -- 2026-07-29 grill-with-docs Q1~Q6 반영
- [x] 동료 평가 신청 (500pt 보유 확인 후)
- [x] 동료 평가 3회 PASS -- 완료 2026-08-03

---

### 보충 학습 (동료평가 피드백 기반)

- [x] 듀얼부팅 + Ubuntu 개념 -- general-concepts.md 저장 완료 (2026-07-31)
- [x] 포트 개념 (Well-known / Registered / Dynamic) -- general-concepts.md 저장 완료 (2026-07-31)
- [x] 동료평가 항목 전체 점검 -- 완료 (2026-07-31)
- [ ] Database ports -- 대기
- [ ] 메모리 계층별 작동 구조와 성능 비교, 캐시메모리 -- 대기

### Week1 Mission1 - 보너스 과제 (선택, 언제든 가능)
- [ ] Docker Compose 기초 (단일 서비스 compose로 실행)
- [ ] Docker Compose 멀티 컨테이너 (웹서버 + 보조 서비스)
- [ ] Compose 운영 명령어 (up/down/ps/logs)
- [ ] 환경 변수 활용 (Dockerfile/Compose에서 주입)
- [ ] GitHub SSH 키 설정

### Week2 Mission2 - Python & Git 기초

**레포 전략 확정**: Mission1과 동일한 `Marina2nd_Codyssey` 단일 레포 사용. 별도 repo 없음.
**제출**: 동료평가 시 Marina2nd_Codyssey URL + week2-mission2/ 경로 명시

**세팅:**
- [x] week2-mission2/ 폴더 세팅 -- 2026-07-31 완료
- [x] .gitattributes, .gitignore, README.md, STEPS.md 생성 -- 2026-07-31
- [x] 첫 커밋 + push (STEP 0) -- 2026-07-31
- [ ] knowledge/ 미션 개념 누적

**구현 (STEPS.md 기준):**
- [x] STEP 1: Quiz 클래스 -- 2026-08-03
- [x] STEP 2: 기본 퀴즈 데이터 7개 (주제: AI/바이브코딩/Physical AI/AX/Agentic AI) -- 2026-08-03
- [x] STEP 3: QuizGame 클래스 + state.json -- 2026-08-03
- [x] STEP 4: 메뉴 + 입력 예외 처리 -- 2026-08-03
- [x] STEP 5: 퀴즈 풀기 (브랜치 feature/play) -- 2026-08-03
- [x] STEP 6: 퀴즈 추가 -- 2026-08-03
- [x] STEP 7: 퀴즈 목록 -- 2026-08-03
- [x] STEP 8: 점수 확인 -- 2026-08-03
- [x] STEP 9: README 완성 + 스크린샷 8장 -- 2026-08-03
- [x] STEP 10: clone/pull 실습 -- 2026-08-03

**문서 보강 (2026-08-03):**
- [x] main.py 상세 학습 주석 작성 (LEARNING_RULES 적용)
- [x] STUDY_GUIDE.md 7단계 학습 가이드 작성
- [x] README 대원칙 기반 전면 보강 (코드 구조/핵심 개념/예외 처리/Git 기록)
- [x] LEARNING_RULES.md에 README 작성 대원칙 추가 (모든 미션 공통 적용)
- [x] 파일 손상 테스트 스크린샷 GitHub 업로드

**문서 정정 (2026-08-07):**
- [x] README 브랜치 전략 섹션 정정 -- 커밋 `74d0d4f`
  - 기존 다이어그램이 존재하지 않는 머지 커밋(C7)을 그리면서 본문엔 Fast-forward라 표기 (자기모순)
  - 실측: `feature/play`는 0883b3c에서 분기, 5d5d369 1커밋 후 **FF 병합** -- 부모 1개, 갈래 안 남음
  - FF 3단계 다이어그램 + FF vs 3-way merge 비교 다이어그램 추가
  - reflog를 브랜치 사용 증거로 인용 (`git reflog show feature/play`)
  - 실제 3-way merge 사례 추가: 2183b83 -> 9302138(로컬)/ff25306(GitHub 웹) -> 282c532(부모 2개)
- [ ] `feature/play` 브랜치 삭제 -- 동료평가 종료 후. README가 reflog를 증거로 인용 중이라 보류

**동료평가 준비:**
- [x] grill-me 세션으로 핵심 개념 학습 (Python/클래스/파일IO/Git) -- 2026-08-04 R1+R2 완료
  - R1: Q3 정답, Q1/Q2/Q4/Q6 모름/반만 → 약한 영역 3개 도출
  - R2: with문 정답, 직렬화 거의 정답(저장 순서 실수), self/cls 아직 약함
  - R2 Q4 진행 중 (QuizGame() 호출 시 내부 동작)
- [x] kkirikkiri 코드+요구사항 검증 -- 2026-08-04 종합 PASS (코드품질 PASS, 요구사항 충족 PASS, 수정사항 0건)
- [ ] 동료평가 신청
- [ ] 2차 과제 동료평가 피드백 리뷰 -- 원본 `Week2_Mission2_FB.txt` (레포 루트, 미추적)

### Week3 Mission3 - Mini NPU Simulator (MAC 연산)

**레포 전략 확정 (2026-08-12)**: 신규 repo 생성 취소. Mission1/2와 동일한 `Marina2nd_Codyssey` 단일 레포의 `week3-mission3/` 하위 사용.
사유: `D:\Projects\CLAUDE.md` 5항 "미션·기능별 별도 레포 금지". 제출 시 레포 URL + 경로 병기.

**설계 (2026-08-12):**
- [x] week3-mission3/ 폴더 세팅 (.gitattributes, .gitignore, docs/screenshots/)
- [x] show-me-the-prd로 PRD 4종 생성 -- `PRD/01_PRD.md` ~ `04_PROJECT_SPEC.md` + `PRD/README.md`
  - `04_PROJECT_SPEC.md`에 요구사항 추적표 전수(124항목 기준) + 예상 결과 정답표 수록
- [x] STEPS.md 작성 -- STEP 0~12 커밋 단위 가이드
- [x] 보너스 과제 제외 결정 (1D 최적화, 패턴 생성기) -- 원문 "(선택)" 명시, 필수 완성도 우선

**구현 (2026-08-12):**
- [x] main.py 1192줄 -- Matrix / normalize_label / mac / decide / measure_mac_ms / 모드1 / 모드2 / --selftest
- [x] 3x3 내장 상수 (data.json에 size_3 없음. 요구사항은 3x3 성능 측정 요구)
- [x] README.md 17개 섹션 -- LEARNING_RULES 필수 13종 + 과제 지정 템플릿(실행방법/구현요약/결과리포트/재현성) + 요구사항 대조표
- [x] 실행 결과 확정: **총 6 / 통과 3 / 실패 3** (FAIL 3건은 데이터가 수학적 동점으로 설계된 결과, Fraction 정확연산으로 교차검증)

**검증 (2026-08-12):**
- [x] kkirikkiri 4명 팀 검증 -- 요구사항 감사관 + 코드 검증관 + 문서 검증관
  - 요구사항 124항목 전수 대조: PASS 120 / FAIL 0
  - 코드 62 시나리오 실행, 문서 라인참조 74건 + 수치 21건 검산
  - **CRITICAL 0 / HIGH 6 / MEDIUM 5** -- HIGH·MEDIUM 전부 수정 완료
  - 리포트: `kkirikkiri-report-20260812-mission3.md`
- [x] 수정 완료: `UnicodeDecodeError` 미포착(트레이스백 크래시), `isdigit`->`isdecimal`,
      `==` 비교 설명 오류(X가 아니라 Cross가 이김), meta.version 허위 주장, 라인번호 3건, Git 7종/브랜치 전략 누락
- [x] 수정 후 재검증 -- selftest 통과, 6/3/3 회귀 없음, data.json md5 불변

**커밋/배포 (2026-08-12):**
- [x] STEP 0~12 커밋 수행 후 push -- 커밋 15개, `origin/master` 동기화 완료
  - 사전정리 1 + STEP 0~12 13개 + `feature/json-mode` `--no-ff` 병합 1
  - 각 STEP마다 실행 검증 후 커밋. 중간 커밋으로 되돌려도 프로그램이 동작함
  - 재구성 결과를 최종본과 `diff` 대조: 1줄(주석 표현)만 차이, 나머지 1191줄 동일
  - Git 필수 명령어 7종 전부 사용: init(M1)/add/commit/push/checkout/pull/clone(M2)
- [x] 문서 코드참조 48건 자동 재대조 -- 전건 일치

**남은 작업:**
- [ ] 스크린샷 6장 캡처 -> `week3-mission3/docs/screenshots/`
  - `selftest.png` : `python main.py --selftest`
  - `mode1_normal.png` : 모드1 예시 입력 (A=1.0 / B=5.0 / 판정 B)
  - `mode1_error.png` : 모드1 오류 입력 3종 (`1 2` / `a b c` / 빈 줄) 재입력 유도
  - `mode2_judge.png` : 모드2 케이스별 판정 + PASS/FAIL
  - `mode2_perf.png` : 성능 분석표 (3x3/5x5/13x13/25x25)
  - `mode2_summary.png` : 결과 요약 (총 6 / 통과 3 / 실패 3)
  - 캡처 규칙: 입력 명령어와 출력이 한 화면에 함께 보이게
- [ ] 캡처 후 README 14절 "캡처 대기" 상태 열 갱신 + 이미지 삽입
- [ ] 스크린샷 커밋: `git add docs/screenshots/ && git commit -m "docs: 실행 화면 스크린샷 6장 추가" && git push origin master`
- [ ] grill-me 세션으로 핵심 개념 검증 (MAC / 라벨 정규화 / 부동소수점 epsilon / O(N²))
  - 예상 질문: "왜 3건이 FAIL인가?" -> 답은 README 11-2절 (데이터가 수학적 동점으로 설계됨, 구현 버그 아님)
- [ ] 동료평가 신청 -- 제출 시 레포 URL + `week3-mission3/` 경로 병기 필수 (단일 레포이므로)

### Term-Project - 7개 도메인 아이디어톤 (대기)
- [ ] 제약/Physical AI 도메인 아이디어 사전 구상
- [ ] knowledge/pharma-ai-insights.md 축적 내용 활용
