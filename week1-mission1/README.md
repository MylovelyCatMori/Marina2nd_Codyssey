# Week1 Mission1 - 개발 워크스테이션 구축

## 1) 실행 환경

| 항목 | 내용 |
|------|------|
| OS | macOS (평가 환경) / Windows 11 (작업 환경) |
| Shell | bash |
| Terminal | - |
| Docker | - |
| Git | - |

> 실습 완료 후 실제 버전 정보로 업데이트

---

## 2) 수행 체크리스트

- [ ] 터미널 기본 조작 및 폴더 구성
- [ ] 권한 변경 실습 (chmod)
- [ ] Docker 설치/점검 (docker --version, docker info)
- [ ] hello-world 컨테이너 실행
- [ ] ubuntu 컨테이너 진입 및 명령 실행
- [ ] Dockerfile 빌드 및 컨테이너 실행
- [ ] 포트 매핑 접속 확인 (브라우저 스크린샷)
- [ ] 바인드 마운트 반영 확인
- [ ] Docker 볼륨 영속성 검증
- [ ] Git 사용자 설정 (git config --list)
- [ ] GitHub 저장소 연동

---

## 3) 크로스 플랫폼 호환성 처리 (Windows -> Mac)

이 프로젝트는 **Windows 11에서 작업하고, Mac(OrbStack 환경)에서 평가**받는다.
두 OS 간 차이로 인한 오류를 사전에 차단하기 위해 다음 처리를 적용했다.

### 핵심 문제: 줄바꿈 문자 차이

| OS | 줄바꿈 문자 | 표기 |
|----|-----------|------|
| Windows | CR + LF | `\r\n` |
| Mac / Linux | LF | `\n` |

Windows에서 작성한 파일을 Mac에서 실행하면 `\r` 문자가 남아 스크립트 오류, Dockerfile 파싱 오류 등이 발생할 수 있다.

### 해결: `.gitattributes`로 LF 강제

```
# .gitattributes
* text=auto eol=lf
*.sh text eol=lf
Dockerfile text eol=lf
```

Git이 커밋 시점에 모든 텍스트 파일을 LF로 정규화한다. Mac에서 clone하면 LF 파일만 받는다.

### Git 설정

```bash
git config core.autocrlf false
```

Windows Git이 자동으로 CRLF 변환하는 것을 막는다. `.gitattributes`가 유일한 기준이 된다.

### 적용된 호환성 원칙

| 항목 | Windows 주의사항 | 적용 처리 |
|------|----------------|----------|
| 줄바꿈 | CRLF 자동 삽입 | `.gitattributes eol=lf` |
| 경로 구분자 | 백슬래시 `\` | Dockerfile/스크립트 내부는 `/` 사용 |
| 쉘 스크립트 | bash 없음 | Git Bash 또는 WSL 사용 |
| chmod | Windows에서 효과 없음 | README는 Mac 기준으로 기록 |
| Docker | WSL2 백엔드 사용 | 명령어는 동일, 동작 차이 없음 |

---

## 4) 터미널 조작 로그

### 3-1. 기본 조작

```bash
# 현재 위치 확인
$ pwd

# 숨김 파일 포함 목록
$ ls -la

# 디렉토리 생성
$ mkdir -p ~/codyssey/practice

# 파일 생성 및 내용 확인
$ touch test.txt
$ echo "hello codyssey" > test.txt
$ cat test.txt

# 복사 / 이름변경 / 삭제
$ cp test.txt test_copy.txt
$ mv test_copy.txt renamed.txt
$ rm renamed.txt
```

> 실습 후 실제 출력 결과 여기에 추가

### 3-2. 권한 실습

```bash
# 파일 권한 확인
$ ls -l test.txt

# 권한 변경 (644: 소유자 읽기/쓰기, 그 외 읽기만)
$ chmod 644 test.txt
$ ls -l test.txt

# 디렉토리 권한 변경 (755: 소유자 모든 권한, 그 외 읽기/실행)
$ chmod 755 practice/
$ ls -ld practice/
```

**권한 표기법 해석:**
```
755 = rwxr-xr-x
      ^^^ ^^^ ^^^
      소유자 그룹 others

r=4, w=2, x=1
7 = 4+2+1 = rwx (읽기+쓰기+실행)
5 = 4+0+1 = r-x (읽기+실행)
4 = 4+0+0 = r-- (읽기만)
```

---

## 4) Docker 설치 및 점검

```bash
$ docker --version
# Docker version X.X.X, build XXXXXXX

$ docker info
# 실제 출력 결과 추가
```

---

## 5) Docker 기본 운영

```bash
# 이미지 목록
$ docker images

# hello-world 실행
$ docker run hello-world

# ubuntu 컨테이너 진입
$ docker run -it ubuntu bash
root@<id>:/# ls
root@<id>:/# echo "hello from ubuntu container"
root@<id>:/# exit

# 컨테이너 목록 (실행중 + 종료된 것 포함)
$ docker ps -a

# 로그 확인
$ docker logs <container_id>

# 리소스 확인
$ docker stats --no-stream
```

---

## 6) Dockerfile 기반 커스텀 이미지

### 선택 방식: (A) nginx:alpine 베이스 + 정적 콘텐츠 교체

**커스텀 포인트:**
| 항목 | 목적 |
|------|------|
| `FROM nginx:alpine` | 경량 alpine 기반으로 이미지 크기 최소화 |
| `LABEL` | 이미지 메타데이터 명시 (관리 용이) |
| `ENV APP_ENV=development` | 환경 변수로 실행 모드 명시 |
| `COPY site/` | 커스텀 HTML 페이지로 기본 nginx 페이지 교체 |

```bash
# 빌드
$ docker build -t my-web:1.0 .

# 실행 (포트 매핑: 호스트 8080 -> 컨테이너 80)
$ docker run -d -p 8080:80 --name my-web-8080 my-web:1.0

# 접속 확인
$ curl http://localhost:8080
```

**브라우저 접속 증거:**
> http://localhost:8080 접속 스크린샷 추가

---

## 7) Docker 볼륨 영속성 검증

```bash
# 볼륨 생성
$ docker volume create mydata

# 컨테이너에 볼륨 연결 후 데이터 기록
$ docker run -d --name vol-test -v mydata:/data ubuntu sleep infinity
$ docker exec -it vol-test bash -c "echo 'persistent data' > /data/hello.txt && cat /data/hello.txt"

# 컨테이너 삭제
$ docker rm -f vol-test

# 새 컨테이너에서 동일 볼륨 연결 -> 데이터 유지 확인
$ docker run -d --name vol-test2 -v mydata:/data ubuntu sleep infinity
$ docker exec -it vol-test2 bash -c "cat /data/hello.txt"
# 출력: persistent data
```

**검증 결과:** 컨테이너 삭제 후에도 볼륨 데이터 유지됨

---

## 8) Git 설정 및 GitHub 연동

```bash
$ git config --list
# 실제 출력 결과 추가 (토큰/비밀번호 절대 포함 금지)
```

**VSCode GitHub 연동 증거:**
> 스크린샷 추가

---

## 9) 트러블슈팅

### Case 1: (제목)
| 항목 | 내용 |
|------|------|
| 문제 | |
| 원인 가설 | |
| 확인 방법 | |
| 해결/대안 | |

### Case 2: (제목)
| 항목 | 내용 |
|------|------|
| 문제 | |
| 원인 가설 | |
| 확인 방법 | |
| 해결/대안 | |

---

## 10) 핵심 개념 정리

### 절대 경로 vs 상대 경로
- **절대 경로**: 루트(`/`)부터 시작. 예) `/home/user/documents/file.txt`
- **상대 경로**: 현재 위치 기준. 예) `./documents/file.txt`, `../other/`

### 포트 매핑이 필요한 이유
컨테이너는 격리된 네트워크 공간에서 실행된다. 호스트에서 컨테이너 내부 포트에 접근하려면 `-p <호스트포트>:<컨테이너포트>`로 명시적 연결이 필요하다.

### Docker 볼륨이란?
컨테이너는 삭제되면 내부 데이터도 함께 사라진다. 볼륨은 컨테이너 생명주기와 독립적으로 데이터를 유지하는 저장소다.

### Git vs GitHub
- **Git**: 로컬 버전관리 도구. 변경 이력 추적
- **GitHub**: 원격 협업 플랫폼. Git 저장소 호스팅 + 코드 리뷰 + 이슈 관리
