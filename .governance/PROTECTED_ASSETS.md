# 보호 자산 목록 (Protected Assets)

> Standard Project Structure SS-F 거버넌스 원칙 적용.
> 이 파일에 등록된 자산은 승인 없이 삭제/덮어쓰기 금지.

## 보호 대상

| 자산 | 경로 | 보호 이유 | 변경 시 절차 |
|------|------|-----------|-------------|
| 미션 제출 README | week{N}-mission{N}/README.md | 동료 평가 증거 | 동료 평가 완료 후 변경 금지 |
| 핵심 개념 기록 | knowledge/*.md | SSOT 단일 소스 | decision-log에 변경 이유 기록 필수 |
| 운영 규칙 파일 | .governance/*.md | 프로젝트 거버넌스 | 학습자 본인 승인 + decision-log 기록 |
| 결정 레지스트리 | decision-log/*.md | append-only 이력 | 수정 금지, 추가만 가능 |
| .gitattributes | week*/.gitattributes | Mac 호환성 | 변경 시 크로스플랫폼 검증 필수 |

## 보호 원칙
1. 보호 자산을 변경하려면 decision-log/에 이유를 먼저 기록한다
2. 미션 제출 후 해당 미션 README는 수정하지 않는다 (증거 보존)
3. knowledge/의 개념 기록은 덮어쓰지 않고 버전을 누적한다
