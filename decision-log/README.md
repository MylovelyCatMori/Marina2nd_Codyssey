# Decision Log - 결정 레지스트리

> Standard Project Structure §B 결정 레지스트리 원칙 적용.
> append-only. 기록 삭제/수정 금지. 추가만 허용.
> 목적: 이미 해소된 결정을 재논쟁하지 않는다.

## 기록 채널 통일 원칙
- 트러블슈팅 결정 → 이 파일에만 기록
- 개념 보정 → knowledge/에만 기록
- 운영 규칙 변경 → .governance/에 기록 후 여기에도 링크

## 파일 구조
| 파일 | 내용 |
|------|------|
| phase1-decisions.md | 입학연수 결정 기록 |
| _template-decision.md | 결정 기록 템플릿 |

## 아카이빙 규칙
20건 초과 시 → decision-log/archive/phase1-YYYYMM.md 로 이관
