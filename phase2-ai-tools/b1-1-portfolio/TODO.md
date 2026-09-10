# B1-1 TODO -- 나를 소개하는 웹페이지

최종 업데이트: 2026-09-11
현재 위치: **개념 A 진행 중 (A3 완료 / A4 다음)**

> 상위 TODO: `D:\Projects\S01-codyssey\TODO.md`
> 계획 문서: `PRD/03_PHASES.md` · 요구사항: `REQUIREMENTS.md` (필수 86개)
> 금지 사항: `PRD/04_PROJECT_SPEC.md` "절대 하지 마" 13개

---

## 진행 현황

| 단계 | 기간 | 상태 |
|---|---|---|
| 설계 (요구사항 + PRD) | - | ✅ 2026-09-09 |
| 용어 훑기 (A그룹 38개) | - | ✅ 2026-09-09 |
| Phase 0 · 뼈대와 환경 | 0.5일 | ✅ 2026-09-09 |
| **개념 A · CSS 레이아웃** | 1일 | **▶ 진행 중 (3/8)** |
| Phase 1 · 시맨틱 + 반응형 | 1.5일 | 대기 |
| 개념 B · JavaScript 기초 | 1.5일 | 대기 |
| Phase 2 · DOM/이벤트/다크모드 | 1.5일 | 대기 |
| 개념 C · 비동기·네트워크 | 1.5일 | 대기 |
| Phase 3 · API + 4상태 ★ | 2일 | 대기 |
| Phase 4 · 폼 유효성 | 1일 | 대기 |
| Phase 5 · 보너스 + 배포 | 1일 | 대기 |
| Phase 6 · 문서 + 검증 | 1일 | 대기 |

용어 승급: **🟡 4 / 🔴 34** (A그룹 38개 기준) + 파생 2건(`box-sizing`, margin 상쇄)

---

## ✅ Phase 0 · 뼈대와 환경 (완료 2026-09-09)

- [x] 폴더 구조 생성 -- `index.html` `css/` `js/` `images/` (F-01)
- [x] 외부 CSS `<link>` + JS `<script defer>` 연결 (F-02, F-24)
- [x] `.gitignore` 웹 프로젝트용으로 교체 (Python 잔재 제거)
- [x] `.gitattributes` 웹 확장자 추가
- [x] `images/.gitkeep` 추가 -- Git은 빈 폴더를 추적하지 않음
- [x] Live Server 실행 확인 (`http://127.0.0.1:5500`)
- [x] CSS 연결 검증 -- 배경색 변경 확인
- [x] JS 연결 검증 -- Console 출력 + `textContent` 변경 확인
- [x] **`defer` 실험 1·2 완료** -- 학습 규칙 2 적용

### Phase 0 배운 것 (기록)

| 항목 | 내용 |
|---|---|
| `defer` 효과의 조건 | 스크립트 **위치**에 따라 다름. `head`에 둘 때만 효과 있음. `body` 끝이면 유무가 무관 |
| 에러 메시지 해부 | `Uncaught`(안 잡힘) / `TypeError`(값 종류 문제) / `set`vs`read`(대입인가 조회인가) |
| null 에러 원칙 | **에러가 난 줄과 원인이 있는 줄은 다르다.** `null` 관련 에러는 항상 위쪽을 본다 |
| 실험 설계 | 첫 실험이 아무 변화도 안 보여줬을 때 **결론이 아니라 설계를 의심**해야 했다 |

---

## ▶ 개념 A · CSS 레이아웃 (다음, 1일)

> 대상 용어 10개: 1 태그/요소/속성 · 5 앵커/alt/label · 7 선택자 · 8 박스모델 ·
> 9 CSS변수 · 10 Flexbox · 11 Grid · 12 반응형/미디어쿼리/뷰포트 · 13 모바일퍼스트 · 14 transition/shadow/hover

- [~] A1 태그 / 요소 / 속성 -- 실습 파일 준비 완료, **관찰 보류** (2026-09-10)
- [~] A2 선택자 -- 예측만 기록, **실행 대조 보류**
- [x] **A3 박스 모델** ★ 레이아웃 전체의 토대 -- 완료 2026-09-11
- [ ] **A4 CSS 변수 (`:root`)** ◀ 여기부터
- [ ] A5 Flexbox (1차원)
- [ ] A6 Grid + `auto-fit` / `minmax` (2차원)
- [ ] A7 뷰포트 / 미디어쿼리 / 모바일 퍼스트
- [ ] A8 `transition` / `box-shadow` / hover
- [ ] 완료 기준: **G-02(Flexbox vs Grid 선택 기준)를 3문장으로 답할 수 있다**
- [ ] 완료 기준: 해당 10개 🔴 → 🟡 승급

---

### 개념 A 배운 것 (기록)

| 항목 | 내용 |
|---|---|
| 박스 모델 네 겹 | content → padding → border → margin |
| padding vs margin | **배경색이 칠해지는가**가 유일한 구분 기준. padding은 칠해지고 상자가 커진다. margin은 투명하고 이웃을 밀어낸다 |
| 오답 교정 | "차지한 자리"와 "배경색 면적"은 다르다. margin은 자리를 먹지만 색은 없다 |
| `box-sizing` 함정 | 기본값 `content-box`에서 `width:300 + padding:20 + border:10` → 실제 **360px**. 레이아웃이 터지는 최다 원인 |
| margin 상쇄 | 세로만 상쇄(큰 쪽 하나). **가로는 상쇄 안 됨** |

**Phase 1 착수 시 `css/style.css` 맨 위에 넣을 코드 (A3 결론)**

```css
*,
*::before,
*::after {
  box-sizing: border-box;
}
```

---

## ⚠ 관찰 보류 백로그 (테스트 환경 확보 시 일괄 처리)

> 예측과 해설은 마쳤으나 브라우저 실행 대조를 못 한 항목. 🟢 승급의 전제 조건이다.

- [ ] `concept-sandbox/a-css/a1-a2-selectors.html` -- 선택자 우선순위 / 클래스 다중 / id 중복 3실험
  - 예측 기록: Q1 green(id 최우선) · Q2 셋 다 적용 · Q3 id는 고유값이라 중복 불가
  - **Q3 미완**: 규칙만 답했고 "규칙 위반 시 브라우저의 실제 동작"은 미답
- [ ] `concept-sandbox/a-css/a3-box-model.html` -- box-sizing / margin 상쇄 / padding-margin 3실험
  - 예측 기록: Q1 300·360 · Q2 40px · Q3 margin(**오답**, 정답 padding)
- [ ] 확인 방법: Live Server로 열고 F12 Console 두 줄 + Elements→Computed 박스 그림

---

## Phase 1 · 시맨틱 + 반응형 (1.5일)

- [ ] `header` > `nav` (로고 / 메뉴 / 다크모드 버튼 / 햄버거 버튼)
- [ ] `main` 안에 5개 `section`: Hero, About, Skills, Projects, Contact (F-05~F-09)
- [ ] `footer` -- 저작권 + 소셜 링크 (F-10)
- [ ] Projects 카드는 `article` 태그 (F-04)
- [ ] nav 앵커 링크 (F-11) / 이미지 `alt` (F-12) / `label` for-id (F-13)
- [ ] `:root` CSS 변수 + `[data-theme="dark"]` 변수 세트 (F-15, F-16)
- [ ] nav = Flexbox (F-17) / Projects = Grid `auto-fit`+`minmax` (F-18)
- [ ] 모바일 퍼스트 + 768/1024 브레이크포인트 (F-19, F-20)
- [ ] 모바일에서 nav 숨김 + 햄버거 표시 (CSS만) (F-21)
- [ ] hover + `transition` + `box-shadow` (F-22, F-23)
- [ ] Projects에 더미 카드 3개 하드코딩 (Phase 3에서 **완전 제거**)
- [ ] 검증: 375 / 768 / 1440px 세 폭
- [ ] 검증: DevTools로 `data-theme="dark"` 수동 주입 시 색 변경
- [ ] 검증: 인라인 `style="` 0건
- [ ] **학습 규칙 2**: `minmax(280px, 1fr)`을 `1fr`로 바꾸면 좁은 화면에서 무슨 일이 나는가

---

## 개념 B · JavaScript 기초 (1.5일)

> 대상 용어 11개: 3 DOM · 4 렌더링 · 15 const/let/var · 16 querySelector ·
> 17 addEventListener/preventDefault · 19 classList · 20 화살표함수 · 27 localStorage ·
> 28 IntersectionObserver · 29 상태 · 38 prefers-color-scheme

- [ ] B1 `const` / `let` / `var` -- 재할당 시도해 어느 것이 에러 나는가
- [ ] B2 함수 / 화살표 함수
- [ ] B3 DOM -- `console.log(document.body)`로 HTML이 객체임을 확인
- [ ] B4 `querySelector`
- [ ] B5 `textContent` / `classList`
- [ ] B6 `addEventListener`
- [ ] **B7 상태(state)** ★ 이 미션의 심장. 카운터 만들기
- [ ] B8 `localStorage`
- [ ] B9 Intersection Observer
- [ ] B10 `prefers-color-scheme`
- [ ] **B7 예측 질문**: 상태만 바꾸고 렌더 함수를 호출하지 않으면 화면은?
- [ ] 완료 기준: G-03, G-06 설명 가능 + 11개 🟡 승급
- [ ] **주간 5분 점검 1회차** -- 개념 A 용어 5개 무작위

---

## Phase 2 · DOM / 이벤트 / 다크모드 (1.5일)

- [ ] 임계값 상수 정의 -- `SCROLL_TOP=300`, `NAV_SCROLL=60`, `OBSERVER=0.2`
- [ ] `AppState` 객체 뼈대 (`PRD/02_DATA_MODEL.md` 참조)
- [ ] 햄버거 메뉴 토글 (F-30)
- [ ] 부드러운 스크롤 (F-31)
- [ ] 스크롤탑 버튼 300px (F-32)
- [ ] nav 배경 변경 60px (F-33)
- [ ] **다크모드 토글 + localStorage** ← 흐름 1 (F-34, F-35)
- [ ] 시스템 다크모드 감지 (보너스 B-04)
- [ ] 스크롤 애니메이션 threshold 0.2 (F-36)
- [ ] 검증: 다크모드 켜고 새로고침 → 유지
- [ ] 검증: `var` 0건, `onclick=` 0건
- [ ] **학습 규칙 2**: `localStorage.setItem` 줄을 지우고 새로고침 → 무엇이 사라지는가

---

## 개념 C · 비동기와 네트워크 (1.5일) ★ 최난이도

> 대상 용어 12개: 18 textContent vs innerHTML · 21 템플릿리터럴 · 22 구조분해할당 ·
> 23 map/filter/forEach · 24 fetch · 25 비동기/async/await/Promise · 26 try-catch ·
> 30 클라이언트vs서버 · 32 API/엔드포인트 · 33 레이트리밋 · 34 HTTP상태코드 · 36 CORS

- [ ] C1 클라이언트 vs 서버 -- 브라우저 주소창에 API 주소 직접 입력해 JSON 보기
- [ ] C2 API / 엔드포인트 / HTTP 상태 코드
- [ ] C3 `forEach` → `map` → `filter`
- [ ] C4 구조분해 할당
- [ ] C5 템플릿 리터럴
- [ ] C6 `textContent` vs `innerHTML` -- XSS 원리 관찰
- [ ] **C7 동기 vs 비동기** ★ `setTimeout(…, 0)` 출력 순서 예측 후 실행
- [ ] **C8 Promise / `await`** ★ `await` 없이 출력 → `Promise {<pending>}` 확인
- [ ] C9 `try` / `catch`
- [ ] C10 레이트 리밋 / CORS
- [ ] 완료 기준: C7 출력 순서(`1` `3` `2`)를 **이유와 함께** 설명 가능
- [ ] 완료 기준: G-05 설명 가능 + 12개 🟡 승급
- [ ] **주간 5분 점검 2회차** -- 개념 B 용어 5개 무작위

---

## Phase 3 · API 연동 + 4상태 렌더링 (2일) ★ 채점 중심

- [ ] `repoState = { status, data, error }` 선언
- [ ] `fetchRepos()` -- `fetch` + `async/await` + `try/catch` (F-48, F-54)
- [ ] 엔드포인트 `https://api.github.com/users/MylovelyCatMori/repos` (F-49)
- [ ] `response.ok` 검사 → 403 레이트 리밋 분기 (F-55)
- [ ] `renderProjects()` -- **하나의 함수가 status로 4갈래 분기** ← 흐름 2
  - [ ] loading (F-50) / success (F-51) / error+재시도 (F-52) / empty (F-53)
- [ ] 템플릿 리터럴로 카드 생성 (F-43) + 구조분해 할당 (F-44) + `map` (F-45)
- [ ] `description` / `language` **null 기본값 처리**
- [ ] 재시도 버튼 → `fetchRepos()` 재호출
- [ ] 검증: Network **Offline** → 에러 UI + 재시도 버튼
- [ ] 검증: 없는 아이디로 변경 → 에러 UI
- [ ] 검증: 저장소 0개 계정 → **빈 상태**(에러 아님)
- [ ] 검증: 화면에 `null` / `undefined` 미표시
- [ ] **학습 규칙 2 (최우선)**: `await` / `response.ok` / `try-catch` **각각 지우고 실행**
- [ ] Phase 1 더미 카드 **완전 제거** 확인

---

## Phase 4 · 폼 유효성 검사 (1일)

- [ ] `formValues` / `formErrors` 객체 (F-37)
- [ ] `submit`에 `preventDefault()` (F-29, F-41)
- [ ] 필수값 검증 -- 공백 제거 후 빈 값 차단 (F-38)
- [ ] 이메일 형식 검증 -- **빈 값 검사를 먼저** (F-39)
- [ ] 에러 메시지를 **해당 필드 바로 아래** 표시 ← 흐름 3 (F-40)
- [ ] `input` 이벤트로 입력 중 에러 해제 (F-28)
- [ ] 성공 메시지 + 폼 초기화 (F-41)
- [ ] (선택) Formspree 연동 -- 미채택해도 **감점 없음**
- [ ] 검증: 빈 칸 제출 / `abc` 입력 / 정상 제출 시 새로고침 안 됨
- [ ] **주간 5분 점검 3회차** -- 개념 C 용어 5개 무작위

---

## Phase 5 · 보너스 + 배포 (1일)

- [ ] **언어별 필터링** ← 흐름 4 (F-47, B-01)
  - [ ] `language`가 null인 저장소는 `'Unknown'`으로 묶기
  - [ ] **원본 `repoState.data` 변형 금지**
- [ ] Hero 타이핑 효과 (B-02)
- [ ] GitHub Pages 배포 (F-58)
- [ ] **배포 URL에서** 전 기능 재검증 (F-59)
- [ ] 배포 함정 점검: 상대경로 / 파일명 대소문자 / 캐시(Ctrl+Shift+R)
- [ ] **학습 규칙 2**: 원본 배열을 `splice`로 바꾸면 "전체" 버튼이 왜 망가지는가

---

## Phase 6 · 문서화 + 검증 (1일)

- [ ] 금지 패턴 grep 0건 -- `var ` / `onclick=` / `style="` / `node_modules`
- [ ] **README 13개 섹션** (`LEARNING_RULES.md`)
  - [ ] 8번 핵심 개념에 **G-01~G-06 전부**
  - [ ] **임계값 3종(300 / 60 / 0.2) 명시** ← 요구사항 자체
  - [ ] 배포 URL + 사용 기술 + 스크린샷 (F-60)
- [ ] 스크린샷 3종 -- 데스크톱 / 모바일 / 다크모드 (S-03~S-05)
- [ ] `REQUIREMENTS.md` 86개 상태 갱신
- [ ] `glossary.md` 🟡 → 🟢 승급 시도
- [ ] `decision-log/`에 설계 결정 + 트러블슈팅 기록
- [ ] **kkirikkiri 검증** -- CRITICAL 0건
- [ ] **3문장 리허설** 5개 (`PRD/03_PHASES.md` Phase 6 후보)
- [ ] Smart Factory 연결 한 줄 (Step 4 회수용)
- [ ] 동료평가 신청 -- 레포 URL + 하위 경로 병기

---

## 미결 사항 (구현 전 결정 필요)

### 콘텐츠 (직접 정해야 함)
- [ ] About 프로필 이미지 -- 사진 / 일러스트 / 이니셜 도형
- [ ] Skills 섹션 기술과 수준 표기 (**과장 금지** -- 인터뷰에서 되치기당함)
- [ ] Hero 인사말 문구 (타이핑 효과용)
- [ ] Footer 소셜 링크 (GitHub 외)

### 기술 결정
- [ ] **GitHub Pages 배포 방식** -- `gh-pages` 브랜치 vs `/docs` 폴더
      (단일 레포 원칙과 충돌. `PRD/04_PROJECT_SPEC.md` 배포 섹션 참조)
- [ ] Font Awesome 사용 여부 (인라인 SVG로 대체하면 외부 의존 0)
- [ ] Formspree 채택 여부 (미채택 시 감점 없음)

### 데이터 표시 정책
- [ ] 저장소 표시 개수 제한 (전부 vs 상위 6~9개)
- [ ] 정렬 기준 (`updated_at` 최신순 vs `stargazers_count`)
- [ ] 포크한 저장소 제외 여부
- [ ] 이메일 검증 정규식 엄격도

### 검증 방법
- [ ] 403 레이트 리밋을 개발 중 어떻게 강제 유발할 것인가

---

## 변경 이력

| 날짜 | 내용 |
|---|---|
| 2026-09-09 | 최초 생성. 설계 + 용어 훑기 + Phase 0 완료 반영 |
| 2026-09-11 | A1·A2 실습 파일 생성(관찰 보류), **A3 박스 모델 완료**. 관찰 보류 백로그 신설 |
