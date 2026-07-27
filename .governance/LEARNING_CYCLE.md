# 학습 사이클 가이드 (Learning Cycle Guide)

> 단순히 따라하는 것이 아니라, 설명할 수 있는 수준으로 체득한다.

## 미션별 학습 사이클 상세

### 단계 1: 개념 학습 (Claude와 함께)
- Claude에게 "왜?"를 포함한 설명 요청
- 현장(제약 생산) 연결 관점은 AI-tutor 스킬 활용
- 심화 이해 필요 시 deep-research 스킬 활용

### 단계 2: 직접 실습
- 모든 명령어는 직접 입력 (복붙 지양)
- 출력 결과 직접 읽기
- 이해 안 되는 출력은 바로 Claude에게 질문

### 단계 3: grill-me 검증 (필수 게이트)
- knowledge/_template-checkpoint.md 체크포인트 파일 복사
- grill-me 스킬로 핵심 개념 3문항 이상 검증
- PASS 기준: 답을 "왜?"까지 포함해서 설명 가능

### 단계 4: grill-with-docs 기록화 (권장)
- grill-me와 동일한 검증 과정을 수행하되 결과를 MD 파일로 저장
- knowledge/ 폴더에 체크포인트 파일로 남김
- 다음 세션에서 재설명 없이 바로 이어서 작업 가능 (세션 간 지식 지속)

### 단계 5: 현장 연결 (AI-tutor)
- "이 개념이 제약 생산 현장에서 어떻게 쓰일까?" 질문
- Physical AI 연결 관점 기록
- knowledge/pharma-ai-insights.md에 누적

### 단계 6: 제출 준비
- 미션 README 빈칸 채우기
- 스크린샷/로그 첨부
- 민감정보 마스킹 확인

### grill-me vs grill-with-docs 차이

| 도구 | 목적 | 사용 시점 |
|------|------|----------|
| grill-me | 이해도 검증 (세션 내 휘발) | 실습 직후 즉각 확인 |
| grill-with-docs | 이해도 검증 + MD 저장 (세션 간 지속) | 미션 완료 전, 다음 세션 인수인계 |
| AI-tutor | 현장 연결 관점 | 개념 이해 후 |
