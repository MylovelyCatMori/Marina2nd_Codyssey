/* ===================================================================
   B1-1 포트폴리오 · main.js

   구조
     1. 상수      -- 매직 넘버를 여기 한곳에 모은다
     2. AppState  -- 화면을 결정하는 값 전부
     3. 요소 참조 -- querySelector 결과를 한 번만 담아둔다
     4. 렌더 함수 -- 상태를 읽어 화면에 반영한다
     5. 이벤트    -- 상태를 바꾸고 렌더 함수를 부른다

   원칙: 단방향. 이벤트 -> 상태 변경 -> 화면 갱신.
   이벤트 처리기가 화면을 직접 고치지 않는다. 상태만 바꾸고 렌더를 부른다.
   =================================================================== */

/* -------------------------------------------------------------------
   1. 상수 (README 명시 대상 -- F-32, F-33, F-36)
   ------------------------------------------------------------------- */

const SCROLL_TOP_THRESHOLD = 300;   // F-32: 스크롤탑 버튼이 나타나는 높이(px)
const NAV_SCROLL_THRESHOLD = 60;    // F-33: nav 배경이 바뀌는 높이(px)
const OBSERVER_THRESHOLD = 0.2;     // F-36: 요소가 20% 보이면 등장 처리
const THEME_STORAGE_KEY = 'theme';  // localStorage 키

/* -------------------------------------------------------------------
   2. AppState -- PRD/02_DATA_MODEL.md 의 구조를 그대로 따른다
   ------------------------------------------------------------------- */

const AppState = {
  theme: 'light',

  // Phase 3에서 채운다. status: 'loading' | 'success' | 'error' | 'empty'
  repoState: { status: 'loading', data: [], error: null },

  activeLanguage: 'all',              // Phase 5
  formValues: { name: '', email: '', message: '' },   // Phase 4
  formErrors: { name: '', email: '', message: '' },   // Phase 4

  uiState: {
    isMenuOpen: false,
    isScrolled: false,
    showTopButton: false
  }
};

/* -------------------------------------------------------------------
   3. 요소 참조
   querySelector 는 호출할 때마다 문서를 뒤진다. 스크롤처럼 자주 도는
   코드 안에서 부르면 낭비다. 시작할 때 한 번만 찾아 담아둔다.
   ------------------------------------------------------------------- */

const els = {
  header: document.querySelector('#site-header'),
  navMenu: document.querySelector('#nav-menu'),
  navLinks: document.querySelectorAll('#nav-menu a'),
  hamburger: document.querySelector('#hamburger'),
  themeToggle: document.querySelector('#theme-toggle'),
  themeIcon: document.querySelector('#theme-icon'),
  scrollTopBtn: document.querySelector('#scroll-top'),
  sections: document.querySelectorAll('main section')
};

/* -------------------------------------------------------------------
   localStorage 안전 래퍼
   시크릿 창이나 저장소 차단 설정에서는 접근 자체가 예외를 던진다.
   여기서 막지 않으면 스크립트 전체가 그 자리에서 멈춘다.
   ------------------------------------------------------------------- */

const storage = {
  get(key) {
    try {
      return localStorage.getItem(key);
    } catch (error) {
      console.warn('[storage] 읽기 실패:', error);
      return null;
    }
  },
  set(key, value) {
    try {
      localStorage.setItem(key, value);
    } catch (error) {
      console.warn('[storage] 쓰기 실패:', error);
    }
  }
};

/* -------------------------------------------------------------------
   4. 렌더 함수 -- 상태를 읽어 화면에 반영한다
   ------------------------------------------------------------------- */

/* 흐름 1: 테마 상태 -> 문서 전체 스타일 (F-34, F-35, F-57a)
   CSS 변수 세트를 통째로 갈아끼우므로 여기서 색을 직접 지정하지 않는다. */
const renderTheme = () => {
  const isDark = AppState.theme === 'dark';

  // data-theme 속성 하나로 [data-theme="dark"] 규칙 전체가 켜지고 꺼진다.
  document.documentElement.setAttribute('data-theme', AppState.theme);

  els.themeIcon.textContent = isDark ? '☀' : '☾';
  els.themeToggle.setAttribute(
    'aria-label',
    isDark ? '라이트 모드로 전환' : '다크 모드로 전환'
  );
};

/* 햄버거 메뉴 (F-30) */
const renderMenu = () => {
  const { isMenuOpen } = AppState.uiState;

  els.navMenu.classList.toggle('is-open', isMenuOpen);
  els.hamburger.classList.toggle('is-active', isMenuOpen);

  // 화면 낭독기에 열림/닫힘을 알린다. 시각적 변화만으로는 전달되지 않는다.
  els.hamburger.setAttribute('aria-expanded', String(isMenuOpen));
  els.hamburger.setAttribute('aria-label', isMenuOpen ? '메뉴 닫기' : '메뉴 열기');
};

/* 스크롤 파생 상태 -> nav 배경(F-33) + 스크롤탑 버튼(F-32) */
const renderScrollUI = () => {
  const { isScrolled, showTopButton } = AppState.uiState;

  els.header.classList.toggle('is-scrolled', isScrolled);
  els.scrollTopBtn.classList.toggle('is-visible', showTopButton);
};

/* -------------------------------------------------------------------
   5. 이벤트 -> 상태 변경 -> 렌더
   ------------------------------------------------------------------- */

/* 테마 토글 (F-34, F-35) */
els.themeToggle.addEventListener('click', () => {
  AppState.theme = AppState.theme === 'dark' ? 'light' : 'dark';  // ① 상태 변경
  storage.set(THEME_STORAGE_KEY, AppState.theme);                 // ② 저장
  renderTheme();                                                  // ③ 화면 갱신
});

/* 햄버거 토글 (F-30) */
els.hamburger.addEventListener('click', () => {
  AppState.uiState.isMenuOpen = !AppState.uiState.isMenuOpen;
  renderMenu();
});

/* 부드러운 스크롤 (F-31, F-29)
   기본 동작(주소창에 #about 이 붙으며 순간 이동)을 막고 직접 이동시킨다. */
els.navLinks.forEach((link) => {
  link.addEventListener('click', (event) => {
    const targetId = link.getAttribute('href');
    const target = document.querySelector(targetId);
    if (!target) return;

    event.preventDefault();

    // 움직임을 줄이도록 설정한 사용자에게는 애니메이션 없이 이동시킨다.
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    target.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth' });

    // 모바일에서 메뉴를 누르면 메뉴가 열린 채로 남지 않게 닫는다.
    if (AppState.uiState.isMenuOpen) {
      AppState.uiState.isMenuOpen = false;
      renderMenu();
    }
  });
});

/* 스크롤 (F-32, F-33)
   scroll 이벤트는 1초에 수십 번 터진다. 매번 클래스를 만지면 낭비이므로
   다음 화면 갱신 직전에 한 번만 처리하도록 묶는다. */
let scrollTicking = false;

const handleScroll = () => {
  const y = window.scrollY;

  AppState.uiState.isScrolled = y > NAV_SCROLL_THRESHOLD;
  AppState.uiState.showTopButton = y > SCROLL_TOP_THRESHOLD;

  renderScrollUI();
  scrollTicking = false;
};

window.addEventListener('scroll', () => {
  if (scrollTicking) return;
  scrollTicking = true;
  window.requestAnimationFrame(handleScroll);
});

/* 스크롤탑 버튼 (F-32) */
els.scrollTopBtn.addEventListener('click', () => {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  window.scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' });
});

/* -------------------------------------------------------------------
   스크롤 등장 애니메이션 (F-36)
   IntersectionObserver = "이 요소가 화면에 들어왔는가"를 브라우저가
   대신 감시해주는 도구. scroll 이벤트로 위치를 계산하는 것보다 싸다.
   ------------------------------------------------------------------- */

const setupReveal = () => {
  // JS가 죽었을 때 내용이 영원히 안 보이는 사고를 막기 위해
  // 숨기는 클래스는 JS가 직접 붙인다.
  els.sections.forEach((section) => section.classList.add('reveal'));

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;

      entry.target.classList.add('is-visible');

      // 한 번 나타난 요소는 더 볼 필요가 없다. 감시를 끊는다.
      observer.unobserve(entry.target);
    });
  }, { threshold: OBSERVER_THRESHOLD });

  els.sections.forEach((section) => observer.observe(section));
};

/* -------------------------------------------------------------------
   초기화
   테마 결정 우선순위: ① localStorage ② 시스템 설정(B-04) ③ light
   ------------------------------------------------------------------- */

const init = () => {
  const saved = storage.get(THEME_STORAGE_KEY);

  if (saved === 'dark' || saved === 'light') {
    AppState.theme = saved;
  } else {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    AppState.theme = prefersDark ? 'dark' : 'light';
  }

  renderTheme();
  renderMenu();
  handleScroll();   // 새로고침 시 이미 스크롤되어 있을 수 있다
  setupReveal();

  console.log('[Phase 2] 초기화 완료. theme =', AppState.theme);
};

init();
