# B1-1 나를 소개하는 웹페이지 -- 디자인 문서

> Show Me The PRD로 생성됨 (2026-09-09)
> 미션: Codyssey Step 2 · B1-1 (필수, 160h)

---

## 한 줄 요약

외부 라이브러리 없이 순수 HTML/CSS/JS로 만드는 반응형 포트폴리오. GitHub API를 연동해 저장소를 실시간 렌더링한다. **채점 기준은 UI 완성도가 아니라 "이벤트 → 상태 → 렌더링" 흐름의 설명 가능성이다.**

---

## 문서 구성

| 문서 | 내용 | 언제 읽나 |
|---|---|---|
| [../REQUIREMENTS.md](../REQUIREMENTS.md) | 과제 원문 요구사항 전수 추적표 (필수 86개) | **구현 중 항상**. 구현 완료 시 상태 갱신 |
| [01_PRD.md](./01_PRD.md) | 뭘 만드는지, 누가 쓰는지, 상태흐름 4종 | 프로젝트 시작 전 |
| [02_DATA_MODEL.md](./02_DATA_MODEL.md) | 상태 객체 구조, API 응답 모양, localStorage | JS 상태 설계할 때 |
| [03_PHASES.md](./03_PHASES.md) | Phase 0~6 단계 계획 + 검증 기준 | 개발 순서 정할 때 |
| [04_PROJECT_SPEC.md](./04_PROJECT_SPEC.md) | 금지 사항 13개 + 필수 사항 + 테스트 방법 | **AI에게 코드 시킬 때마다** |

---

## 이 문서들에 나오는 약어 (공통 LEARNING_RULES "약어 풀기")

| 약어 | 원말 | 뜻 |
|---|---|---|
| DOM | Document Object Model | 문서 객체 모델. 브라우저가 HTML을 자바스크립트로 조작 가능한 객체 구조로 바꿔놓은 것 |
| API | Application Programming Interface | 프로그램끼리 정해진 형식으로 데이터를 주고받는 창구 |
| CTA | Call To Action | 행동 유도 버튼. "프로젝트 보기" 같은 것 |
| CSS | Cascading Style Sheets | 계단식 스타일 시트. 위에서 아래로 규칙이 흘러내리며 적용된다는 뜻 |
| HTML | HyperText Markup Language | 하이퍼텍스트 마크업 언어 |
| SPA | Single Page Application | 단일 페이지 애플리케이션. **이번 미션에서는 만들지 않음** |
| ERD | Entity Relationship Diagram | 개체 관계도. 데이터끼리의 관계를 그린 그림 |
| CORS | Cross-Origin Resource Sharing | 교차 출처 리소스 공유. 다른 주소의 자원을 가져올 때의 브라우저 보안 규칙 |
| XSS | Cross-Site Scripting | 교차 사이트 스크립팅. 남의 입력이 내 페이지에서 코드로 실행되는 공격 |
| MVP | Minimum Viable Product | 최소 기능 제품. 일단 돌아가는 최소 버전 |
| PRD | Product Requirements Document | 제품 요구사항 문서 |
| UI | User Interface | 사용자 인터페이스. 사람이 보고 만지는 화면 |
| UX | User Experience | 사용자 경험 |
| CDN | Content Delivery Network | 콘텐츠 전송망. 외부 파일을 빠르게 받아오는 서버망 |

---

## 절대 잊으면 안 되는 것 3가지

1. **외부 라이브러리 전면 금지** -- React/Vue/jQuery/Bootstrap/Tailwind 전부. 위반 시 과제 무효. 허용은 Font Awesome, Google Fonts뿐
2. **`var` / `onclick=` / `style="..."` 사용 금지** -- 직접 감점 대상
3. **임계값 3종(300px, 60px, 0.2)을 README에 명시** -- 요구사항 자체

---

## 다음 단계

Phase 1을 시작하려면 [03_PHASES.md](./03_PHASES.md) 맨 아래 "Phase 1 시작 프롬프트"를 복사해 쓴다.

**단, 그 전에** `knowledge/glossary.md`의 B1-1 백로그를 훑는다 (`LEARNING_RULES.md` 규칙 1).

> **"훑는다"의 정확한 의미**: 15분 이내, **정의 없이 이름만** 눈으로 지나간다. 외우는 것이 아니다.
> 목적은 코드에서 그 단어를 만났을 때 "처음 본다"는 당황을 없애 **흐름이 끊기지 않게** 하는 것이다.
> 정의를 채우는 것(🔴→🟡)은 미션 **종료 전**에 몰아서 한다.

**학습 규칙 상시 적용 사항**은 [03_PHASES.md](./03_PHASES.md) 맨 위 "모든 Phase에 상시 적용되는 학습 규칙" 표를 먼저 읽는다. 구현 진도보다 우선한다.

---

## 미결 사항 종합 [NEEDS CLARIFICATION]

### 콘텐츠 (내가 정해야 하는 것)
- [ ] About 프로필 이미지 -- 사진 / 일러스트 / 이니셜 도형
- [ ] Skills 섹션에 넣을 기술과 수준 표기 (과장 금지. 인터뷰에서 되치기당한다)
- [ ] Hero 인사말 문구 (타이핑 효과에 들어감)
- [ ] Footer 소셜 링크 목록 (GitHub 외)

### 기술 결정
- [ ] GitHub Pages 배포 방식 -- `gh-pages` 브랜치 vs `/docs` 폴더 (04_PROJECT_SPEC 배포 섹션 참조)
- [ ] `.gitignore` 웹 프로젝트용으로 교체 (현재 M3의 Python용)
- [ ] Font Awesome 사용 여부 (인라인 SVG로 대체하면 외부 의존 0)
- [ ] Formspree 채택 최종 결정 (미채택해도 감점 없음)

### 데이터 표시 정책
- [ ] 저장소 표시 개수 제한 (전부 vs 상위 6~9개)
- [ ] 정렬 기준 (`updated_at` 최신순 vs `stargazers_count` 많은순)
- [ ] 포크한 저장소 제외 여부
- [ ] 이메일 검증 정규식 엄격도

### 검증 방법
- [ ] 403 레이트 리밋 상태를 개발 중 어떻게 강제 유발할 것인가

---

## 이 미션이 남기는 것

| 지금 손으로 만드는 것 | 다음 미션에서 배울 대응물 |
|---|---|
| `AppState` 객체 | React `useState` |
| `renderProjects(state)` 하나의 함수 | React 컴포넌트 렌더링 |
| `addEventListener` + 상태 변경 + 렌더 호출 | React 이벤트 핸들러 + 자동 리렌더 |
| `status: 'loading'\|'success'\|'error'\|'empty'` | 데이터 페칭 라이브러리의 상태 관리 |

React가 자동으로 해주는 일을 **직접 해봐야** React가 무엇을 대신해주는지 알 수 있다. 이것이 이 미션이 B1-2 이후의 필수 선행인 이유다.
