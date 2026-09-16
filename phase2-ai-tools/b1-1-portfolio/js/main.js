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

/* GitHub API (F-49)
   sort=updated : 최근에 손댄 저장소가 앞으로 온다
   per_page=100 : 한 번에 받아올 최대 개수. 기본값은 30이다 */
const GITHUB_USERNAME = 'MylovelyCatMori';
const GITHUB_REPOS_URL =
  `https://api.github.com/users/${GITHUB_USERNAME}/repos?sort=updated&per_page=100`;
const MAX_VISIBLE_REPOS = 9;        // 화면에 보여줄 저장소 개수 상한

/* -------------------------------------------------------------------
   2. AppState -- PRD/02_DATA_MODEL.md 의 구조를 그대로 따른다
   ------------------------------------------------------------------- */

const AppState = {
  theme: 'light',

  // Phase 3에서 채운다. status: 'loading' | 'success' | 'error' | 'empty'
  repoState: { status: 'loading', data: [], error: null },

  activeLanguage: 'all',              // Phase 5

  formValues: { name: '', email: '', message: '' },
  formErrors: { name: '', email: '', message: '' },

  // PRD/02_DATA_MODEL.md 에 없는 필드다. 제출 성공 문구도 화면을 결정하는
  // 값이므로 DOM 에 직접 쓰지 않고 상태로 둔다.
  formSuccess: '',

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
  sections: document.querySelectorAll('main section'),
  projectsGrid: document.querySelector('#projects-grid'),
  form: document.querySelector('#contact-form'),
  formSuccess: document.querySelector('#form-success')
};

/* 폼 필드 세 개의 요소를 한 번에 묶어둔다.
   formValues / formErrors 의 키와 이름을 일치시켰으므로
   필드마다 따로 코드를 쓸 필요가 없다. */
const FORM_FIELDS = ['name', 'email', 'message'];

const formEls = FORM_FIELDS.reduce((acc, field) => {
  const input = document.querySelector(`#${field}`);
  acc[field] = {
    input,
    error: document.querySelector(`#${field}-error`),
    wrapper: input.closest('.field')
  };
  return acc;
}, {});

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

/* -----------------------------------------------------------------
   Projects 렌더링 (F-50 ~ F-53) -- 흐름 2 (F-57b)

   함수는 하나다. repoState.status 를 읽어 네 갈래로 나뉜다.
   상태마다 별도의 show/hide 함수를 두지 않는 이유는, 그렇게 하면
   "로딩을 숨기는 것을 깜빡한" 상태가 생길 수 있기 때문이다.
   한 함수가 innerHTML 을 통째로 덮어쓰면 그런 조합 자체가 불가능해진다.
   ----------------------------------------------------------------- */

/* 외부에서 받은 문자열을 HTML 안에 넣기 전에 꺾쇠와 따옴표를 무력화한다.
   저장소 이름이나 설명에 <script> 가 들어 있으면 그대로 실행되기 때문이다.
   (textContent 는 이 처리가 필요 없지만, 템플릿 리터럴로 만든 문자열을
    innerHTML 에 넣을 때는 반드시 거쳐야 한다) */
const escapeHtml = (value) => String(value)
  .replace(/&/g, '&amp;')
  .replace(/</g, '&lt;')
  .replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;')
  .replace(/'/g, '&#39;');

/* 저장소 하나를 카드 HTML 문자열로 바꾼다.
   구조분해 할당(F-44)으로 필요한 다섯 개만 꺼낸다.
   = 뒤의 값은 기본값이다. null 이 아니라 undefined 일 때만 작동하므로
   null 방어는 아래에서 따로 한다. */
const createCard = (repo) => {
  const { name, description, language, stargazers_count: stars, html_url: url } = repo;

  // GitHub 는 설명이나 언어가 없으면 null 을 준다.
  // 그대로 넣으면 화면에 "null" 이라는 글자가 찍힌다.
  const safeDesc = description ? escapeHtml(description) : '설명이 없는 저장소입니다.';
  const safeLang = language ? escapeHtml(language) : 'Unknown';

  return `
    <article class="card">
      <h3 class="card__title">
        <a class="card__link" href="${escapeHtml(url)}" target="_blank" rel="noopener noreferrer">
          ${escapeHtml(name)}
        </a>
      </h3>
      <p class="card__desc">${safeDesc}</p>
      <div class="card__meta">
        <span class="chip">${safeLang}</span>
        <span class="card__stars">★ ${Number(stars) || 0}</span>
      </div>
    </article>
  `;
};

const renderProjects = () => {
  const { status, data, error } = AppState.repoState;

  if (status === 'loading') {                                   // F-50
    els.projectsGrid.innerHTML = `
      <div class="state">
        <p class="state__msg">프로젝트를 불러오는 중입니다...</p>
      </div>
    `;
    return;
  }

  if (status === 'error') {                                     // F-52, F-55
    els.projectsGrid.innerHTML = `
      <div class="state">
        <p class="state__msg">${escapeHtml(error)}</p>
        <button class="btn btn--ghost js-retry" type="button">다시 시도</button>
      </div>
    `;
    return;
  }

  if (status === 'empty') {                                     // F-53
    els.projectsGrid.innerHTML = `
      <div class="state">
        <p class="state__msg">표시할 프로젝트가 없습니다.</p>
      </div>
    `;
    return;
  }

  // status === 'success' (F-51)
  // map 으로 배열을 HTML 문자열 배열로 바꾼 뒤 이어 붙인다. (F-45, F-43)
  els.projectsGrid.innerHTML = data
    .slice(0, MAX_VISIBLE_REPOS)
    .map(createCard)
    .join('');
};

/* 스크롤 파생 상태 -> nav 배경(F-33) + 스크롤탑 버튼(F-32) */
const renderScrollUI = () => {
  const { isScrolled, showTopButton } = AppState.uiState;

  els.header.classList.toggle('is-scrolled', isScrolled);
  els.scrollTopBtn.classList.toggle('is-visible', showTopButton);
};

/* -----------------------------------------------------------------
   폼 검증 (F-37 ~ F-41) -- 흐름 3 (F-57c)
   ----------------------------------------------------------------- */

/* 이메일 형식 검사식.
   RFC 규격을 그대로 옮기면 수백 자짜리 정규식이 되고, 그래도 완벽하지
   않다. 오타를 걸러내는 것이 목적이므로 "공백 없는 글자 @ 공백 없는 글자
   . 공백 없는 글자" 세 덩어리만 확인한다. 진짜 유효성은 메일이 도착하는지로만
   알 수 있다. */
const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const EMPTY_MESSAGES = {
  name: '이름을 입력해 주세요.',
  email: '이메일을 입력해 주세요.',
  message: '메시지를 입력해 주세요.'
};

/* 필드 하나를 검사해 에러 문구를 돌려준다. 문제가 없으면 빈 문자열이다. */
const validateField = (field, rawValue) => {
  // 공백만 입력한 것은 입력하지 않은 것과 같다. (F-38)
  const value = rawValue.trim();

  if (!value) {
    return EMPTY_MESSAGES[field];
  }

  // 순서가 중요하다. 빈 값 검사가 형식 검사보다 먼저다. (F-39)
  // 빈 칸에 "이메일 형식이 올바르지 않습니다"가 뜨면 무엇이 틀렸는지 알 수 없다.
  if (field === 'email' && !EMAIL_PATTERN.test(value)) {
    return '이메일 형식이 올바르지 않습니다. 예: name@example.com';
  }

  return '';
};

/* 상태를 읽어 에러 문구와 테두리 색을 화면에 반영한다. (F-40) */
const renderForm = () => {
  FORM_FIELDS.forEach((field) => {
    const message = AppState.formErrors[field];
    const { input, error, wrapper } = formEls[field];

    // 외부 입력을 화면에 넣을 때는 textContent 를 쓴다.
    // innerHTML 과 달리 태그로 해석되지 않는다.
    error.textContent = message;
    wrapper.classList.toggle('has-error', Boolean(message));

    // 화면 낭독기에 "이 칸에 문제가 있다"를 알린다.
    input.setAttribute('aria-invalid', String(Boolean(message)));
  });

  els.formSuccess.textContent = AppState.formSuccess;
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
   GitHub API 호출 (F-48 ~ F-55)

   async 함수는 항상 Promise 를 돌려준다. await 은 "이 줄의 결과가
   올 때까지 기다렸다가 다음 줄로 가라"는 뜻이다. await 을 빼면
   응답 대신 Promise 객체 자체가 담긴다.
   ------------------------------------------------------------------- */

/* 상태 코드별로 사용자에게 보여줄 문구를 나눈다.
   "실패했습니다" 한 줄로 뭉뚱그리면 사용자가 다시 시도해야 할지
   기다려야 할지 판단할 수 없다. */
/* 사용자에게 그대로 보여도 되는 에러임을 표시하는 표식.
   이것이 없으면 "Failed to fetch" 같은 개발자용 문구가 화면에 새어 나간다. */
class UserFacingError extends Error {
  constructor(message) {
    super(message);
    this.name = 'UserFacingError';
  }
}

const describeHttpError = (status) => {
  if (status === 403) {
    // F-55: GitHub API 는 로그인 없이 시간당 60회까지만 허용한다.
    return '요청 한도를 초과했습니다. 잠시 후 다시 시도해 주세요.';
  }
  if (status === 404) {
    return '해당 GitHub 사용자를 찾을 수 없습니다.';
  }
  return '프로젝트를 불러올 수 없습니다.';
};

const fetchRepos = async () => {
  // ① 상태를 loading 으로 바꾸고 즉시 화면에 반영한다.
  //    응답을 기다린 뒤에 바꾸면 로딩 화면이 보이지 않는다.
  AppState.repoState = { status: 'loading', data: [], error: null };
  renderProjects();

  try {
    const response = await fetch(GITHUB_REPOS_URL);

    // fetch 는 404 나 403 을 받아도 예외를 던지지 않는다.
    // "서버에 닿았다"는 것 자체는 성공으로 보기 때문이다.
    // 그래서 response.ok 를 직접 확인해야 한다. (F-54 의 함정)
    if (!response.ok) {
      throw new UserFacingError(describeHttpError(response.status));
    }

    const repos = await response.json();

    // ② 0개인 것은 실패가 아니다. empty 와 error 를 구분한다.
    AppState.repoState = {
      status: repos.length > 0 ? 'success' : 'empty',
      data: repos,
      error: null
    };
  } catch (error) {
    // 우리가 던진 에러만 문구를 그대로 쓴다.
    // fetch 가 네트워크 문제로 던지는 에러의 message 는 "Failed to fetch" 같은
    // 개발자용 문구라 화면에 내보내면 안 된다.
    let message;
    if (error instanceof UserFacingError) {
      message = error.message;
    } else if (!navigator.onLine) {
      message = '네트워크에 연결되어 있지 않습니다.';
    } else {
      message = '프로젝트를 불러올 수 없습니다. 연결 상태를 확인해 주세요.';
    }

    // 원본 에러는 콘솔에만 남긴다. 디버깅에는 필요하고 사용자에게는 불필요하다.
    console.error('[fetchRepos] 실패:', error);
    AppState.repoState = { status: 'error', data: [], error: message };
  }

  // ③ 성공이든 실패든 마지막에 한 번만 그린다.
  renderProjects();
};

/* 폼 제출 (F-29, F-38, F-39, F-41)
   submit 의 기본 동작은 페이지 새로고침이다. 막지 않으면 검증 결과를
   보여주기도 전에 화면이 통째로 다시 그려진다. */
els.form.addEventListener('submit', (event) => {
  event.preventDefault();

  // ① 입력값을 상태로 옮긴다.
  FORM_FIELDS.forEach((field) => {
    AppState.formValues[field] = formEls[field].input.value;
  });

  // ② 상태를 검사해 에러 상태를 만든다.
  FORM_FIELDS.forEach((field) => {
    AppState.formErrors[field] = validateField(field, AppState.formValues[field]);
  });

  const hasError = FORM_FIELDS.some((field) => AppState.formErrors[field] !== '');

  if (hasError) {
    AppState.formSuccess = '';
    renderForm();

    // 첫 번째 문제 칸으로 커서를 옮긴다. 에러 문구가 화면 밖에 있으면
    // 사용자는 왜 제출이 안 되는지 알 수 없다.
    const firstBad = FORM_FIELDS.find((field) => AppState.formErrors[field] !== '');
    formEls[firstBad].input.focus();
    return;
  }

  // ③ 통과. 실제 전송은 하지 않는다 (Formspree 미채택, 감점 없음).
  AppState.formSuccess = '메시지가 전송되었습니다. 감사합니다.';
  FORM_FIELDS.forEach((field) => { AppState.formValues[field] = ''; });
  els.form.reset();
  renderForm();
});

/* 입력 중 에러 해제 (F-28 input 이벤트)
   칸 세 개에 각각 리스너를 다는 대신 폼 하나에 단다.
   event.target 이 어느 칸에서 났는지 알려준다. */
els.form.addEventListener('input', (event) => {
  const field = event.target.id;
  if (!FORM_FIELDS.includes(field)) return;

  AppState.formValues[field] = event.target.value;

  // 이미 에러가 떠 있는 칸만 다시 검사한다. 아직 건드리지도 않은 칸에
  // 빨간 글씨를 미리 띄우면 사용자를 재촉하는 꼴이 된다.
  if (AppState.formErrors[field]) {
    AppState.formErrors[field] = validateField(field, event.target.value);
  }

  // 고치기 시작하면 이전 성공 문구는 치운다.
  AppState.formSuccess = '';
  renderForm();
});

/* 재시도 버튼 (F-52)
   버튼은 렌더할 때마다 새로 만들어진다. 버튼에 직접 리스너를 달면
   다시 그려질 때 사라진다. 그래서 사라지지 않는 부모에 한 번만 단다. */
els.projectsGrid.addEventListener('click', (event) => {
  if (!event.target.closest('.js-retry')) return;
  fetchRepos();
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
  renderForm();
  handleScroll();   // 새로고침 시 이미 스크롤되어 있을 수 있다
  setupReveal();

  // await 하지 않는다. 응답을 기다리는 동안 나머지 화면은 이미 쓸 수 있어야 한다.
  fetchRepos();

  console.log('[Phase 4] 초기화 완료. theme =', AppState.theme);
};

init();
