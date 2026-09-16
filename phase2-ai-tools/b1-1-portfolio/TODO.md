# B1-1 TODO -- 나를 소개하는 웹페이지

최종 업데이트: 2026-09-16
현재 위치: **Phase 4 완료 / Phase 5 착수 대기 (보너스 + 배포)**

> **운영 방식 변경 (2026-09-16)**: `LEARNING_RULES.md` **규칙 5 · 구현 우선** 적용.
> 개념 블록을 별도 세션으로 잡지 않는다. 해당 개념을 실제로 쓰는 Phase에서 5줄로 설명한다.
> 깊은 이해와 샌드박스 관찰 대조는 Phase 6(동료평가 준비)으로 이연.

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
| 개념 A · CSS 레이아웃 | - | ⏸ Phase 내 인라인 처리로 전환 |
| **Phase 1 · 시맨틱 + 반응형** | 1.5일 | ✅ 2026-09-16 |
| 개념 B · JavaScript 기초 | - | ⏸ Phase 2 내 인라인 처리 |
| **Phase 2 · DOM/이벤트/다크모드** | 1.5일 | ✅ 2026-09-16 |
| 개념 C · 비동기·네트워크 | - | ⏸ Phase 3 내 인라인 처리 |
| **Phase 3 · API + 4상태 ★** | 2일 | ✅ 2026-09-16 |
| **Phase 4 · 폼 유효성** | 1일 | ✅ 2026-09-16 |
| **Phase 5 · 보너스 + 배포** | 1일 | **▶ 다음** |
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

## ⏸ 개념 A · CSS 레이아웃 (인라인 처리로 전환)

- [x] A3 박스 모델 -- 완료 2026-09-11
- [x] A4 CSS 변수 -- 예측·해설 완료 (관찰 보류)
- [x] A5 Flexbox -- 5줄 요약으로 마무리 2026-09-16. 실습 페이지 별도 제공
- [x] A6 Grid `auto-fit`/`minmax` -- Phase 1에서 구현하며 처리
- [x] A7 미디어쿼리 / 모바일 퍼스트 -- Phase 1에서 구현하며 처리
- [x] A8 transition / box-shadow / hover -- Phase 1에서 구현하며 처리
- [ ] 완료 기준(G-02 3문장 · 용어 승급)은 **Phase 6으로 이연**

### 개념 A 배운 것 (기록)

| 항목 | 내용 |
|---|---|
| 박스 모델 네 겹 | content → padding → border → margin |
| padding vs margin | **배경색이 칠해지는가**가 유일한 구분 기준. padding은 칠해지고 상자가 커진다. margin은 투명하고 이웃을 밀어낸다 |
| 오답 교정 | "차지한 자리"와 "배경색 면적"은 다르다. margin은 자리를 먹지만 색은 없다 |
| `box-sizing` 함정 | 기본값 `content-box`에서 `width:300 + padding:20 + border:10` → 실제 **360px**. 레이아웃이 터지는 최다 원인 |
| margin 상쇄 | 세로만 상쇄(큰 쪽 하나). **가로는 상쇄 안 됨** |
| `var()`는 값이 아니라 빈칸 | 규칙에 적힌 순간 색이 정해지지 않는다. **각 요소가 자기 위치에서** 변수를 찾아 채운다 |
| 변수 탐색 순서 | 자신 → 부모 → ... → `html`. **처음 찾은 곳에서 멈춘다.** 그래서 `.zone` 안의 B는 dark 전환에도 초록 유지 |
| 오답 교정 (Q1·Q2) | ".swatch에 선언됐으니 우선"은 오답. `.swatch`가 직접 가진 것은 `border`이고 `--color-accent`는 물려받는다. 비교는 **같은 속성끼리** |
| 오답 교정 (Q3) | 값 오타 `blu`는 읽기 단계에서 버려져 앞 줄 orange 생존. 변수 이름 오타는 읽기 단계를 통과해 orange를 덮은 뒤 계산 단계에서 실패 → **투명** |
| 대체값 | `var(--x, orange)` -- 변수 이름 오타 방어 |

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
- [ ] `concept-sandbox/a-css/a4-css-variables.html` -- 범위 / 테마 전환 / 오타 3실험
  - 예측 기록: Q1 A·B·C 파랑(**B 오답**, 정답 초록) · Q2 전부 주황(**B 오답**, 정답 초록) · Q3 D orange · E orange(**오답**, 정답 투명)
  - Console 기대값: B `#2f9e44` · E `rgba(0, 0, 0, 0)` · 토글 후 B만 초록 유지
  - **확인 질문 미답**: ① `.swatch`에 `--color-accent: red` 추가 시 A·B·C와 dark 전환 결과 ② B를 `section`으로 한 겹 더 감쌌을 때 B 색과 탐색 순서
- [ ] 확인 방법: Live Server로 열고 F12 Console 두 줄 + Elements→Computed 박스 그림

---

## ✅ Phase 1 · 시맨틱 + 반응형 (완료 2026-09-16)

- [x] `header` > `nav` (로고 / 메뉴 / 다크모드 버튼 / 햄버거 버튼)
- [x] `main` 안에 5개 `section`: Hero, About, Skills, Projects, Contact (F-05~F-09)
- [x] `footer` -- 저작권 + 소셜 링크 (F-10)
- [x] Projects 카드는 `article` 태그 (F-04)
- [x] nav 앵커 링크 (F-11) / 이미지 `alt` (F-12) / `label` for-id (F-13)
- [x] `:root` CSS 변수 + `[data-theme="dark"]` 변수 세트 (F-15, F-16)
- [x] nav = Flexbox (F-17) / Projects = Grid `auto-fit`+`minmax(260px, 1fr)` (F-18)
- [x] 모바일 퍼스트 + 768/1024 브레이크포인트 (F-19, F-20)
- [x] 모바일에서 nav 숨김 + 햄버거 표시 (CSS만) (F-21)
- [x] hover + `transition` + `box-shadow` (F-22, F-23)
- [x] Projects에 더미 카드 3개 하드코딩 (Phase 3에서 **완전 제거**)
- [x] `images/profile.svg` 생성 (외부 의존 0)
- [x] 검증: 375 / 768 / 1440px 세 폭 -- 가로 스크롤 0건
- [x] 검증: `data-theme="dark"` 주입 시 배경 #12171d / 글자 #e7ecf2 전환 확인
- [x] 검증: 인라인 `style="` 0건, `onclick=` 0건, `var ` 0건
- [ ] **학습 규칙 2**: `minmax(260px, 1fr)`을 `1fr`로 바꾸면 좁은 화면에서 무슨 일이 나는가 → **Phase 6 이연**

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

## ✅ Phase 2 · DOM / 이벤트 / 다크모드 (완료 2026-09-16)

- [x] 임계값 상수 정의 -- `SCROLL_TOP_THRESHOLD=300`, `NAV_SCROLL_THRESHOLD=60`, `OBSERVER_THRESHOLD=0.2`
- [x] `AppState` 객체 (`PRD/02_DATA_MODEL.md` 구조 그대로: theme / repoState / activeLanguage / formValues / formErrors / uiState)
- [x] `storage` 안전 래퍼 -- 시크릿 창에서 localStorage 접근 예외 차단
- [x] 햄버거 메뉴 토글 + `aria-expanded` 갱신 (F-30)
- [x] 부드러운 스크롤 + `preventDefault` + 메뉴 자동 닫힘 (F-31, F-29)
- [x] 스크롤탑 버튼 300px (F-32)
- [x] nav 배경 변경 60px (F-33)
- [x] **다크모드 토글 + localStorage** ← 흐름 1 (F-34, F-35, F-57a)
- [x] 시스템 다크모드 감지 (보너스 B-04 채택)
- [x] 스크롤 애니메이션 threshold 0.2 + `unobserve` (F-36)
- [x] scroll 이벤트 `requestAnimationFrame` 묶음 처리
- [x] 검증: 다크모드 켜고 새로고침 → 유지 (`theme=dark`, 배경 `#12171d`)
- [x] 검증: 50px → 변화 없음 / 100px → nav 배경 / 400px → 스크롤탑 표시
- [x] 검증: 모바일 폭에서 메뉴 `none` → 햄버거 클릭 시 `flex`, 링크 클릭 시 자동 닫힘
- [x] 검증: 콘솔 에러 0건
- [ ] **학습 규칙 2**: `localStorage.setItem` 줄을 지우고 새로고침 → 무엇이 사라지는가 → **Phase 6 이연**

### Phase 2 남긴 것 (Phase 3·4에서 처리)

- `AppState.repoState` / `formValues` / `formErrors` 는 뼈대만. 값은 아직 안 쓴다
- F-28 네 이벤트 중 `click` `scroll` 완료. `submit` `input` 은 Phase 4
- F-26 `innerHTML` 은 Phase 3 카드 생성에서 사용

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

## ✅ Phase 3 · API 연동 + 4상태 렌더링 (완료 2026-09-16) ★ 채점 중심

- [x] `repoState = { status, data, error }` 사용
- [x] `fetchRepos()` -- `fetch` + `async/await` + `try/catch` (F-48, F-54)
- [x] 엔드포인트 `https://api.github.com/users/MylovelyCatMori/repos?sort=updated&per_page=100` (F-49)
- [x] `response.ok` 검사 → 403 / 404 / 기타 분기 (F-55)
- [x] `renderProjects()` -- **하나의 함수가 status로 4갈래 분기** ← 흐름 2 (F-57b)
  - [x] loading (F-50) / success (F-51) / error+재시도 (F-52) / empty (F-53)
- [x] 템플릿 리터럴로 카드 생성 (F-43) + 구조분해 할당 (F-44) + `map` (F-45)
- [x] `description` / `language` **null 기본값 처리** (설명 없음 / `Unknown`)
- [x] `escapeHtml()` -- 저장소 이름·설명의 HTML 무력화 (XSS 차단)
- [x] `UserFacingError` -- 우리가 던진 문구만 화면에 내보낸다
- [x] 재시도 버튼 → 부모에 이벤트 위임 (버튼이 다시 그려져도 살아남음)
- [x] 검증: 네트워크 실패 → "프로젝트를 불러올 수 없습니다. 연결 상태를 확인해 주세요." + 재시도 버튼
- [x] 검증: 403 → "요청 한도를 초과했습니다" / 404 → "해당 GitHub 사용자를 찾을 수 없습니다"
- [x] 검증: 빈 배열 → **빈 상태**(재시도 버튼 없음, 에러 아님)
- [x] 검증: 화면에 `null` / `undefined` 미표시
- [x] 검증: `<img src=x onerror=...>` 이름 주입 → 실행 안 됨, 글자로만 표시
- [x] 검증: 실제 API 응답 2건 카드 렌더링 확인
- [x] Phase 1 더미 카드 **완전 제거** 확인
- [ ] **학습 규칙 2 (최우선)**: `await` / `response.ok` / `try-catch` 각각 지우고 실행 → **Phase 6 이연**

### Phase 3 결정 사항 (미결 항목 해소)

| 항목 | 결정 | 사유 |
|---|---|---|
| 표시 개수 | 상위 **9개** (`MAX_VISIBLE_REPOS`) | Grid 3열 기준 3줄. 원본 배열은 그대로 두고 `slice`로 잘라 쓴다 |
| 정렬 | `sort=updated` 최신순 | 별 개수는 학습용 저장소에서 대부분 0이라 변별력이 없다 |
| 포크 제외 | **제외하지 않음** | 지금 저장소가 2개뿐이라 제외하면 빈 화면이 된다 |

---

## ✅ Phase 4 · 폼 유효성 검사 (완료 2026-09-16)

- [x] `formValues` / `formErrors` 객체 (F-37) + `formSuccess` 추가 (PRD 대비 확장 1건)
- [x] `submit`에 `preventDefault()` (F-29, F-41)
- [x] 필수값 검증 -- `trim()` 후 빈 값 차단 (F-38)
- [x] 이메일 형식 검증 -- **빈 값 검사를 먼저** (F-39)
- [x] 에러 메시지를 **해당 필드 바로 아래** 표시 ← 흐름 3 (F-40, F-57c)
- [x] `input` 이벤트로 입력 중 에러 해제, 이미 에러 난 칸만 재검사 (F-28)
- [x] 성공 메시지 + `form.reset()` + 상태 초기화 (F-41)
- [x] 첫 번째 문제 칸으로 `focus()` 이동
- [x] `aria-invalid` 갱신 (화면 낭독기 대응)
- [x] Formspree 미채택 (감점 없음)
- [x] 검증: 빈 칸 제출 → 에러 3건 + 첫 칸 포커스
- [x] 검증: 공백만 입력 → 동일하게 차단
- [x] 검증: `abc` 입력 → **형식 에러만** 1건 (빈 값 검사 우선순위 확인)
- [x] 검증: 고치는 중 에러 자동 해제
- [x] 검증: 정상 제출 → 성공 문구 + 입력칸 비워짐, **새로고침 안 됨** (`defaultPrevented: true`)
- [ ] **주간 5분 점검 3회차** → **Phase 6 이연**

### Phase 4 결정 사항

| 항목 | 결정 | 사유 |
|---|---|---|
| 이메일 정규식 | `/^[^\s@]+@[^\s@]+\.[^\s@]+$/` | RFC 규격을 그대로 옮기면 수백 자가 되고 그래도 완벽하지 않다. 오타 차단이 목적이며 진짜 유효성은 메일 도착 여부로만 알 수 있다 |
| 에러 표시 시점 | 제출 시 전체 검사, 이후 **에러 난 칸만** 입력 중 재검사 | 건드리지도 않은 칸에 빨간 글씨를 미리 띄우면 사용자를 재촉하는 꼴이 된다 |

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
- [x] 저장소 표시 개수 제한 → **상위 9개** (2026-09-16)
- [x] 정렬 기준 → **`updated` 최신순** (2026-09-16)
- [x] 포크한 저장소 제외 여부 → **제외 안 함** (2026-09-16)
- [x] 이메일 검증 정규식 엄격도 → **오타 차단 수준** (2026-09-16)

### 검증 방법
- [ ] 403 레이트 리밋을 개발 중 어떻게 강제 유발할 것인가

---

## 변경 이력

| 날짜 | 내용 |
|---|---|
| 2026-09-09 | 최초 생성. 설계 + 용어 훑기 + Phase 0 완료 반영 |
| 2026-09-11 | A1·A2 실습 파일 생성(관찰 보류), **A3 박스 모델 완료**. 관찰 보류 백로그 신설 |
| 2026-09-15 | **A4 CSS 변수** 예측·해설 완료(오답 3건 교정, 관찰 보류). A5 Flexbox 실습 파일 생성 + 예측 질문 제시 |
| 2026-09-16 | **Phase 4 완료** -- 폼 검증(빈 값 우선 → 형식), 에러 필드별 표시, 입력 중 해제, 성공 후 초기화. **흐름 3 확보로 F-56·F-57 충족.** F-37~F-41 등 9건 ✅ |
| 2026-09-16 | **Phase 3 완료** -- `fetchRepos` + 4상태 `renderProjects` + 템플릿리터럴/구조분해/map. XSS 차단과 에러 문구 누출 차단 추가. 흐름 2 확보. F-43~F-55 중 12건 ✅ |
| 2026-09-16 | **Phase 2 완료** -- AppState + 임계값 3종 + 햄버거/부드러운스크롤/스크롤탑/nav배경/다크모드+localStorage/Observer. 흐름 1 확보. F-25~F-36 중 11건 ✅ |
| 2026-09-16 | **규칙 5 구현 우선 도입.** 개념 A 인라인 전환, A5 5줄 요약 마무리. **Phase 1 완료** -- 시맨틱 구조 + CSS 변수 2종 + Flex nav + Grid 카드 + 768/1024 반응형 + 햄버거 CSS. F-01~F-24 중 23건 ✅ |
