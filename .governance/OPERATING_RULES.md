# 운영 규칙 (Operating Rules)

> 이 파일은 보호 자산입니다. 변경 시 decision-log에 기록하세요.

## 1. 미션 학습 사이클 (필수 순서)

```
미션 수령
  -> Claude와 개념 학습 (왜? 포함)
  -> 직접 실습 수행
  -> grill-me 3문항 이상 PASS (knowledge/_template-checkpoint.md 사용)
  -> grill-with-docs로 검증 결과 MD 저장 (knowledge/에 체크포인트 기록)
  -> 미션 README 작성 및 증거 수집
  -> 동료 평가 신청
  -> decision-log에 트러블슈팅 기록
  -> 동료 평가 3회 PASS
  -> 다음 미션
```

## 2. 기록 채널 규칙 (SSOT 원칙)

| 기록 유형 | 저장 위치 | 규칙 |
|-----------|-----------|------|
| 미션별 핵심 개념 | knowledge/ | 단일 파일, 덮어쓰기 금지 |
| 트러블슈팅 / 의사결정 | decision-log/ | append-only, 삭제 금지 |
| 미션 수행 증거 | week{N}-mission{N}/README.md | 완료 후 수정 금지 |
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
