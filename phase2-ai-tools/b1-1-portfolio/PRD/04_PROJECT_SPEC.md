# B1-1 나를 소개하는 웹페이지 -- 프로젝트 스펙

> AI에게 코드를 시킬 때 **이 문서를 항상 함께 공유한다.**
> 이 미션은 "무엇을 쓰느냐"보다 **"무엇을 쓰지 않느냐"가 채점 기준**이다.

---

## 기술 스택

| 영역 | 선택 | 이유 |
|---|---|---|
| 마크업 | HTML5 (시맨틱 태그) | 과제 강제. `div` 남용 대신 `header`/`nav`/`main`/`section`/`article`/`footer` |
| 스타일 | 순수 CSS3 (CSS 변수 + Flexbox + Grid) | 과제 강제. 전처리기 사용 시 컴파일 단계가 생겨 "브라우저가 읽는 언어" 전제가 깨짐 |
| 스크립트 | 순수 JavaScript ES6+ (모듈 없이 단일 파일) | 과제 강제. `import`/`export`는 로컬 `file://` 프로토콜에서 CORS로 막히므로 Live Server 전제에서도 위험 |
| 데이터 소스 | GitHub REST API v3 (미인증) | 과제 지정 엔드포인트. 토큰 사용 금지(아래 참조) |
| 배포 | GitHub Pages | 과제 강제. 무료, 정적 호스팅, 저장소와 직결 |
| 아이콘 | Font Awesome (CDN) | 과제가 명시적으로 허용한 유일한 외부 자산 |
| 폰트 | Google Fonts | 과제가 명시적으로 허용 |
| 인증 | **없음** | 요구사항에 없음. 정적 사이트라 서버가 없음 |
| 빌드 도구 | **없음** | `index.html`을 브라우저가 직접 읽는다. `package.json` 자체를 만들지 않는다 |

---

## 프로젝트 구조

```
b1-1-portfolio/
├── index.html              # 유일한 페이지
├── css/
│   └── style.css           # 변수 → 리셋 → 레이아웃 → 컴포넌트 → 미디어쿼리 순
├── js/
│   └── main.js             # 상수 → 상태 → 렌더 함수 → 이벤트 바인딩 순
├── images/
│   └── profile.*           # 프로필 이미지 등
├── screenshots/            # 제출용 캡처 (데스크톱/모바일/다크모드)
├── PRD/                    # 이 문서들
├── REQUIREMENTS.md         # 요구사항 전수 추적표
├── STEPS.md                # 커밋 단위 실행 기록
└── README.md               # 동료평가 인터뷰 문서
```

### `js/main.js` 내부 순서 (고정)
```
1. 상수        -- 임계값(300/60/0.2), API URL, 셀렉터
2. 상태        -- AppState 객체
3. 순수 함수   -- 검증, 데이터 가공 (DOM을 만지지 않음)
4. 렌더 함수   -- 상태를 받아 DOM을 갱신
5. 이벤트 핸들러 -- 상태를 바꾸고 렌더 함수를 호출
6. 초기화      -- 테마 복원, 이벤트 바인딩, fetch 시작
```
> **왜 이 순서인가** -- 위에서 아래로 읽으면 "데이터가 어디서 와서 어떻게 화면이 되는가"가 그대로 읽힌다. 동료평가에서 코드를 스크롤하며 설명할 때 순서 자체가 설명이 된다.

---

## 절대 하지 마 (DO NOT)

> 1~6번은 **위반 시 과제 무효 또는 직접 감점**이다.

- [ ] **1. 외부 라이브러리를 쓰지 마** -- React, Vue, jQuery, Bootstrap, Tailwind, Alpine, Lodash 전부 금지. npm 설치도, CDN `<script>` 링크도 금지. 허용은 Font Awesome과 Google Fonts **뿐** (C-01, C-02)
- [ ] **2. `var`를 쓰지 마** -- `const` 우선, 재할당이 필요할 때만 `let` (C-04)
- [ ] **3. HTML에 `onclick=` 같은 이벤트 속성을 쓰지 마** -- 전부 `addEventListener` (C-05)
- [ ] **4. 인라인 `style="..."`을 쓰지 마** -- 스타일 변경은 `classList` 조작 또는 CSS 변수로 (C-06)
- [ ] **5. 하드코딩 더미 데이터로 완성이라고 하지 마** -- Projects는 반드시 실제 GitHub API 응답이어야 한다. Phase 1의 더미 카드는 Phase 3에서 **완전히 제거**한다
- [ ] **6. 임계값을 코드에만 두고 README에 안 쓰지 마** -- 300px / 60px / 0.2 세 값은 README 명시가 **요구사항**이다 (F-32, F-33, F-36)
- [ ] **7. GitHub 개인 액세스 토큰을 코드에 넣지 마** -- 정적 사이트의 JS는 누구나 읽는다. 토큰을 넣는 순간 공개된다. 레이트 리밋은 **에러 UI로 처리하는 것이 과제 요구**(F-55)이지 회피 대상이 아니다
- [ ] **8. `repoState.data` 원본 배열을 변형하지 마** -- `splice`/`sort`/`reverse`는 원본을 바꾼다. 필터·정렬은 `filter`/`map`/`[...arr].sort()`로 **새 배열**을 만든다
- [ ] **9. 빈 결과(0개)를 에러로 처리하지 마** -- `empty`와 `error`는 다른 상태다. 합치면 재시도 버튼이 영원히 의미 없어진다
- [ ] **10. 절대경로 `/images/...`를 쓰지 마** -- GitHub Pages는 저장소명 하위 경로에 배포된다. 상대경로 `./images/...`를 쓴다
- [ ] **11. 사용자 입력을 `innerHTML`에 그대로 넣지 마** -- 폼 입력값을 화면에 되비출 때는 `textContent`를 쓴다 (XSS 방지)
- [ ] **12. 매직 넘버를 코드 중간에 흩뿌리지 마** -- 임계값은 파일 상단 상수로 모은다
- [ ] **13. 내가 설명 못 하는 코드를 남기지 마** -- 동료평가 규정상 설명하지 못하면 **부정행위로 간주될 수 있다** (OT p.17). 이해 안 되는 줄은 지우고 다시 쓴다

---

## 항상 해 (ALWAYS DO)

- [ ] **변경 전에 계획을 먼저 보여줘** -- 어떤 파일의 어디를 왜 고칠 것인지
- [ ] **요구사항 ID를 주석으로 남겨** -- `/* F-18: Grid auto-fit 반응형 */` 형태. README 작성 시 근거 추적이 가능해진다
- [ ] **모바일 퍼스트로 작성해** -- 기본 스타일이 모바일, `min-width` 미디어쿼리로 확장 (F-19)
- [ ] **에러는 사용자 언어로 표시해** -- `TypeError: Failed to fetch`가 아니라 "프로젝트를 불러올 수 없습니다"
- [ ] **null 가능 필드는 기본값을 줘** -- `description`, `language`는 자주 null이다. 화면에 `null`이 찍히면 안 된다
- [ ] **상태를 바꾼 뒤엔 반드시 렌더 함수를 호출해** -- 상태만 바꾸고 화면을 안 그리면 아무 일도 일어나지 않는다. 이것이 이 미션에서 가장 흔한 버그다
- [ ] **한 Phase가 끝나면 브라우저에서 눈으로 확인하고 커밋해** -- Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`)
- [ ] **접근성 기본을 지켜** -- 모든 이미지에 의미있는 `alt`(F-12), 폼 `label` for-id 매칭(F-13), 다크모드에서도 색 대비 확보

---

## 테스트 방법

빌드 도구가 없으므로 **브라우저 확인 + 금지패턴 검사**가 테스트다.

```bash
# 로컬 실행 -- VS Code에서 index.html 우클릭 > "Open with Live Server"
# (file:// 직접 열기는 API 호출 시 CORS 문제 가능. 반드시 Live Server 사용)

# 금지 패턴 검사 (전부 결과 0건이어야 함)
grep -rn "var "        js/ index.html   # C-04 위반
grep -rn "onclick="    index.html       # C-05 위반
grep -rn 'style="'     index.html       # C-06 위반
grep -rn "cdn\|unpkg\|jsdelivr" index.html   # C-01 위반 (Font Awesome/Google Fonts 제외 확인)

# 빌드 산물이 없는지 확인 (있으면 안 됨)
ls package.json node_modules 2>/dev/null   # 아무것도 안 나와야 정상
```

### 수동 검증 체크리스트 (Phase 6에서 일괄 수행)

| 항목 | 방법 | 요구사항 |
|---|---|---|
| 반응형 | DevTools 반응형 모드 375 / 768 / 1440px | R-02 |
| 다크모드 영속 | 토글 후 새로고침 | R-08 |
| 시스템 테마 | localStorage 비우고 OS 다크 설정 | B-04 |
| API 성공 | 정상 로딩 | F-51 |
| API 에러 | DevTools Network를 **Offline**으로 전환 후 새로고침 | F-52 |
| API 빈 상태 | 엔드포인트를 저장소 0개 계정으로 임시 변경 | F-53 |
| 재시도 | 에러 상태에서 버튼 클릭 → Network 탭에 새 요청 확인 | F-52 |
| 폼 필수값 | 빈 칸 제출 | F-38 |
| 폼 형식 | 이메일에 `abc` 입력 | F-39 |
| 폼 제출 | 정상 입력 → 새로고침 안 됨 + 성공 메시지 | F-41 |
| 햄버거 | 375px 폭에서 열기/닫기 | F-30 |
| 스크롤 임계값 | 300px / 60px 경계 부근에서 확인 | F-32, F-33 |

---

## 배포 방법 (GitHub Pages)

레포 전략은 `D:\Projects\CLAUDE.md` 5항에 따라 **단일 레포 `Marina2nd_Codyssey` + 하위 폴더**다. GitHub Pages는 저장소 루트 또는 `/docs`만 배포 대상으로 잡을 수 있으므로 아래 중 하나를 택한다.

| 방식 | 방법 | 장점 | 단점 |
|---|---|---|---|
| A. `gh-pages` 브랜치 (권장) | 미션 폴더 내용만 `gh-pages` 브랜치 루트로 push | 단일 레포 원칙 유지, URL이 깔끔 | 브랜치 동기화를 수동으로 해야 함 |
| B. `/docs` 폴더 | 빌드 결과를 레포 루트 `/docs`에 복사 | 설정이 가장 단순 | 파일이 두 곳에 중복 존재 |
| C. 별도 레포 | 포트폴리오만 새 레포로 | 설정 불필요 | **`CLAUDE.md` 5항 "별도 레포 금지" 위반** |

> **C는 선택하지 않는다.** A/B 중 결정 필요 → `[NEEDS CLARIFICATION]`

**배포 절차 (A 기준)**
```
1. Settings > Pages > Source: Deploy from a branch
2. Branch: gh-pages / (root) 선택 후 Save
3. 1~2분 후 https://MylovelyCatMori.github.io/Marina2nd_Codyssey/ 접속
4. 배포 URL에서 전 기능 재검증 (F-59) -- 로컬에서 됐다고 배포에서도 되는 것이 아니다
```

---

## 환경변수

**이 프로젝트에는 환경변수가 없다.**

| 항목 | 값 | 비고 |
|---|---|---|
| GitHub 사용자명 | `MylovelyCatMori` | `js/main.js` 상단 상수. 공개 정보이므로 코드에 있어도 무방 |
| API 엔드포인트 | `https://api.github.com/users/MylovelyCatMori/repos` | 미인증 호출, 시간당 60회 제한 |
| Formspree 폼 ID | (보너스 채택 시) | **공개되어도 무방한 값이지만, 스팸 위험이 있으므로 채택 시 재검토** |

> **`.env` 파일을 만들지 않는다.** 정적 사이트에는 서버가 없어 환경변수를 숨길 방법 자체가 없다. "숨긴 것처럼 보이는" 구조를 만드는 것이 더 위험하다.

---

## [NEEDS CLARIFICATION]

- [ ] **GitHub Pages 배포 방식** -- 위 표의 A(`gh-pages` 브랜치) vs B(`/docs` 폴더) 결정 필요
- [ ] **`.gitignore` 교체** -- 현재 M3에서 복사한 Python용 파일이다. `__pycache__` 등을 지우고 웹 프로젝트용(`.DS_Store`, `.vscode/` 등)으로 교체 필요
- [ ] **Font Awesome 사용 여부** -- 허용되지만 필수는 아니다. 아이콘을 유니코드 문자나 인라인 SVG로 대체하면 외부 의존이 0이 되어 더 안전하다
- [ ] **Formspree 채택 최종 결정** -- 가입 필요. 미채택 시 감점 없음 (과제 요구는 성공 메시지 표시까지)
