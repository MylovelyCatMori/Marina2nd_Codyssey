# Phase 1 - 결정 레지스트리

> append-only. 수정 금지. 새 결정은 맨 아래에 추가.

---

## [2026-07-28] D-001: 프로젝트 구조 설계

**상황**: Codyssey 교육 시작, 18개월 학습 공간 필요
**결정**: Standard Project Structure 원칙 기반 4-phase 구조 채택
**근거**:
- SSOT 원칙: knowledge/ 단일 채널
- 거버넌스: .governance/ 보호 자산
- 피드백 루프: grill-me 게이트
- 아카이빙: phase 완료 시 archive/ 이관
**영향 범위**: 전체 프로젝트 구조

---

## [2026-07-28] D-002: Windows→Mac 크로스플랫폼 대응

**상황**: 작업 Windows, 평가 Mac(OrbStack)
**결정**: .gitattributes eol=lf + git config core.autocrlf false
**근거**: CRLF 차이로 인한 Dockerfile/쉘스크립트 오류 예방
**영향 범위**: 모든 미션 폴더의 .gitattributes

---

## [2026-07-28] D-003: week1-mission1 폴더 이동 불가 결정

**상황**: phase1-admission/ 구조 신설 시 week1-mission1 이동 고려
**결정**: week1-mission1/ 현재 위치 유지 (이동하지 않음)
**근거**: 이미 설정된 .gitattributes, Dockerfile 경로 유지 필요. 동료 평가 링크 보존.
**영향 범위**: phase1-admission/week1/에는 README로 참조만

---
