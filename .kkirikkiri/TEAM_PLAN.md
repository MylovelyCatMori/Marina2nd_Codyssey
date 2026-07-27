# 팀 작업 계획

- 팀명: kkirikkiri-development-codyssey-structure
- 목표: Codyssey with Claude 프로젝트 18개월 운영 구조 조직화
- 생성 시각: 2026-07-28

## 팀 구성
| 이름 | 역할 | 모델 | 담당 업무 |
|------|------|------|----------|
| Lead | 팀장 | Opus | 계획/배분/검증/통합 |
| Architect | 아키텍트 | Opus | 폴더구조 + 거버넌스 파일 생성 |
| Writer | 문서작가 | Opus | 학습템플릿 + grill 체크포인트 문서화 |

## 태스크 목록
- [ ] [Architect] 18개월 폴더 뼈대 생성 (phase1~4, archive)
- [ ] [Architect] .governance/ 파일 3종 생성 (PROTECTED_ASSETS, OPERATING_RULES, LEARNING_CYCLE)
- [ ] [Writer] knowledge/ SSOT 구조 + 미션 개념 템플릿
- [ ] [Writer] decision-log/ 결정 레지스트리 구조 + 템플릿
- [ ] [Writer] grill-me/grill-with-docs 체크포인트 템플릿
- [ ] [Lead] 전체 통합 검증 + README 업데이트

## 설계 원칙 (Standard Project Structure 기반)
1. SSOT: knowledge/ 가 유일한 개념 기록 채널
2. 거버넌스: .governance/ 파일은 승인 없이 변경 금지 (보호자산)
3. 피드백 루프: 미션 완료 전 grill-me 3문항 PASS 필수
4. 결정 레지스트리: decision-log/ 에 append-only 기록
5. 아카이빙: 단계(phase) 완료 시 archive/로 이관
6. 크로스플랫폼: 모든 파일 LF 줄바꿈, 경로 슬래시(/)

## 주요 결정사항
- week1-mission1/ 기존 구조 유지 (이동하지 않음)
- phase1-admission/ 에 week별 서브폴더 구조 신설
- grill-with-docs 전용 체크포인트 파일 포함
