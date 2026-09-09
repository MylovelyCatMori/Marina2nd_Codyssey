/* ===================================================================
   Phase 0 · 연결 확인용 임시 스크립트
   Phase 2에서 전면 교체된다. 지금은 두 가지만 확인한다.
     ① JavaScript 파일이 연결되었는가
     ② defer 덕분에 HTML 요소를 찾을 수 있는가
   =================================================================== */

/* console.log: 브라우저 개발자도구(F12) > Console 탭에 값을 찍는다.
   화면에는 보이지 않는다. 개발자만 보는 확인용 출력이다. */
console.log('[Phase 0] JavaScript 연결 성공');

/* querySelector: CSS 선택자로 요소를 하나 찾아온다.
   '#js-check' 의 # 은 "id 가 js-check 인 것"이라는 뜻이다.
   찾지 못하면 에러가 아니라 null 을 돌려준다. */
const checkTarget = document.querySelector('#js-check');

/* defer 가 동작했는지 확인하는 지점.
   defer 가 없었다면 이 시점에 <p> 가 아직 존재하지 않아 null 이 담긴다. */
console.log('[Phase 0] 요소를 찾았는가:', checkTarget);

/* textContent: 요소 안의 글자를 바꾼다.
   화면의 문장이 아래 내용으로 바뀌면 ①②가 모두 성공한 것이다. */
checkTarget.textContent = 'JavaScript 연결 성공. defer 덕분에 요소를 찾았습니다.';
