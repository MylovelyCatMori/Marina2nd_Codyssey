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

### Week3 Mission3 - CS 기초 (대기)
- [ ] `codyssey-p1-mission3` repo 공개 생성 (미션 수령 후)
- [ ] week3-mission3/ 폴더 세팅 (학습 이력용)

### Term-Project - 7개 도메인 아이디어톤 (대기)
- [ ] 제약/Physical AI 도메인 아이디어 사전 구상
- [ ] knowledge/pharma-ai-insights.md 축적 내용 활용
