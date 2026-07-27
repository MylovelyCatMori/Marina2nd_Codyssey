# 트러블슈팅 패턴 (반복 오류 방지)

> Standard Project Structure §E 근본원인 피드백 루프 적용.
> 오류 1건 = 부류 전체 재검토. 가드 추가 필수.

## 패턴 기록 형식
```
## [날짜] [오류 제목]
- 증상: 어떤 오류 메시지/현상
- 근본원인: 왜 발생했는가
- 해결: 어떻게 해결했는가
- 가드: 재발 방지 확인 방법
- 관련 개념: knowledge/phase*.md 링크
```

---

## Windows→Mac 크로스플랫폼 패턴

### CRLF 줄바꿈 오류
- 증상: Mac에서 쉘스크립트 실행 시 `\r: command not found`
- 근본원인: Windows CRLF 줄바꿈이 Mac에서 오류
- 해결: `.gitattributes`에 `* text=auto eol=lf` + `git config core.autocrlf false`
- 가드: 새 파일 생성 시 `.gitattributes` 적용 여부 확인

---
