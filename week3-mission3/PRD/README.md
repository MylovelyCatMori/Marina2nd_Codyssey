# Mini NPU Simulator -- 디자인 문서

> Show Me The PRD로 생성됨 (2026-08-12)
> 대상: S01-codyssey Week3 Mission3
> 요구사항 원본: `D:\Projects\S01-codyssey\Week3_Mission3.txt`

## 문서 구성

| 문서 | 내용 | 언제 읽나 |
|------|------|----------|
| [01_PRD.md](./01_PRD.md) | 뭘 만드는지, 누가 쓰는지, 성공 기준, 안 만드는 것 | 프로젝트 시작 전 |
| [02_DATA_MODEL.md](./02_DATA_MODEL.md) | data.json 실측 스키마, Matrix 구조, 라벨 정규화 매핑 | 데이터 로드 코드 짤 때 |
| [03_PHASES.md](./03_PHASES.md) | Phase 1~4 구현 순서와 Phase별 검증 방법 | 개발 순서 정할 때 |
| [04_PROJECT_SPEC.md](./04_PROJECT_SPEC.md) | **요구사항 추적표 전수**, 금지사항, 예상 결과 정답표 | AI에게 코드 시킬 때마다 / 제출 전 대조 |

> 구현 단계별 커밋 가이드는 상위 폴더의 [../STEPS.md](../STEPS.md).

## 확정된 결정사항

| 항목 | 결정 | 근거 |
|------|------|------|
| 보너스 과제 | 제외 (1D 최적화, 패턴 생성기 둘 다) | 사용자 결정. 필수 요구사항 완성도 우선 |
| 레포 전략 | 기존 단일 레포 `Marina2nd_Codyssey`의 `week3-mission3/` 하위 | `D:\Projects\CLAUDE.md` 5항 단일 레포 원칙 |
| 산출물 | PRD 4종 + STEPS.md + main.py + README.md | 사용자 결정 |
| 3x3 데이터 | `main.py`에 고정 상수로 내장 | data.json에 size_3 없음. 요구사항은 3x3 성능 측정을 요구 |
| epsilon | `1e-9` 상수 | 요구사항 8절 출력 예시가 `|A-B| < 1e-9` 명시 |
| 예상 결과 | 총 6 / 통과 3 / 실패 3 | 데이터가 3건을 수학적 동점으로 설계 (Fraction 정확 연산 확인) |

## 다음 단계

Phase 1을 시작하려면 [03_PHASES.md](./03_PHASES.md)의 "Phase 1 시작 프롬프트"를 복사해서 사용한다.

## 미결 사항 (종합)

- [ ] 동료평가 제출 시 레포 URL + `week3-mission3/` 경로 병기 (단일 레포이므로 경로 명시 필수)
- [ ] 스크린샷 캡처 항목 최종 확정 -- 최소 5장 (모드1 정상 / 모드1 오류 / 모드2 판정 / 성능표 / 결과 요약)

> 나머지 [NEEDS CLARIFICATION] 항목은 각 문서 안에서 근거와 함께 결정 완료(`[x]`) 상태다.
