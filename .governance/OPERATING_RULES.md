# 운영 규칙 (Operating Rules)

> 이 파일은 보호 자산입니다. 변경 시 decision-log에 기록하세요.

## 1. 미션 학습 사이클 (필수 순서)

```
미션 수령
  -> Claude와 개념 학습 (왜? 포함)
  -> 직접 실습 수행  <-- 각 명령 전 반드시 "왜 이 명령인가?" 설명 포함
  -> grill-me 3문항 이상 PASS (knowledge/_template-checkpoint.md 사용)
  -> grill-with-docs로 검증 결과 MD 저장 (knowledge/에 체크포인트 기록)
  -> 제출용 별도 GitHub repo 생성 (아래 규칙 참고)
  -> 미션 README 작성 및 증거 수집 -> 제출 repo에 push
  -> 동료 평가 신청 (제출 repo URL로)
  -> decision-log에 트러블슈팅 기록
  -> 동료 평가 3회 PASS
  -> 다음 미션
```

## 1-1. 실습 중 Claude 가이드 규칙 (필수)

실습 진행 시 매 명령 블록마다 아래 5가지를 반드시 포함한다:

```
[왜 필요한가]   이 명령/작업이 존재하는 이유. 없으면 어떤 문제가 생기는가.
[무엇을 하는가] 한 줄 요약
[코드 해설]     각 옵션/인자가 무엇을 의미하는지 분해 설명
[명령]
[기대 결과]     실행 후 무엇이 출력/변경되어야 정상인가
```

**금지 사항:**
- 명령만 주고 "실행해줘" 금지
- 개념 설명 없이 다음 단계로 넘어가기 금지
- 사용자가 "왜?"를 물어봐야 설명하는 방식 금지

**목표:** 사용자가 명령 실행 전에 이미 결과를 예측할 수 있는 상태여야 한다.

## 1-2. 제출용 GitHub repo 규칙 (Week2 Mission2부터 적용)

**2가지 repo 구분:**

| repo | 목적 | 예시 |
|------|------|------|
| `Marina2nd_Codyssey` | 프로젝트 관리 전용 (학습 기록, 거버넌스, knowledge) | 제출 금지 |
| 미션별 제출 repo | 동료평가 제출 전용. Default branch 루트에 README.md | 미션마다 새로 생성 |

**제출 repo 생성 규칙:**
- 이름: `codyssey-{phase}-mission{N}` (예: `codyssey-p1-mission2`)
- 공개(Public) 설정
- 루트에 README.md 바로 위치 (폴더 안에 넣지 않음)
- `.gitattributes` 포함 (eol=lf, Mac 평가 환경 대응)
- 민감정보 없음 확인 후 push

**Marina2nd_Codyssey에도 미션 폴더 유지:**
- `week{N}-mission{N}/` 폴더에 동일 내용 보존 (학습 이력용)
- 두 곳 모두 최신 상태 유지

> Week1 Mission1은 예외 적용 (기존 구조 유지).

## 2. 기록 채널 규칙 (SSOT 원칙)

| 기록 유형 | 저장 위치 | 규칙 |
|-----------|-----------|------|
| 미션별 핵심 개념 | knowledge/ | 단일 파일, 덮어쓰기 금지 |
| 트러블슈팅 / 의사결정 | decision-log/ | append-only, 삭제 금지 |
| 미션 수행 증거 | 제출 repo 루트 README.md + week{N}-mission{N}/README.md | 완료 후 수정 금지 |
| 현장 연결 인사이트 | knowledge/pharma-ai-insights.md | 누적 기록 |

## 3. 크로스플랫폼 규칙 (Windows->Mac)

- 모든 텍스트 파일: LF 줄바꿈
- Dockerfile/쉘스크립트: `text eol=lf` 명시
- 경로: 슬래시(/) 사용
- git config core.autocrlf false 유지

## 4. 아카이빙 임계치

- Phase 완료 시 -> archive/phase{N}/ 이관
- 미션 완료 후 logs/ 폴더 -> 미션 폴더 내 보존
- decision-log가 20건 초과 시 -> decision-log/archive/ 이관

## 5. 보호 자산 변경 절차

1. decision-log/에 변경 이유 기록
2. 변경 수행
3. decision-log/에 변경 결과 기록
