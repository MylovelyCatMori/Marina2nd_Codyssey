# Week1 Mission1 - 개발 워크스테이션 구축

## 0) 프로젝트 개요

### 미션 목표
"코드가 내 컴퓨터에서만 돌아가는 문제"를 없애기 위한 개발 워크스테이션을 직접 구축한다.

터미널(CLI), Docker(컨테이너), Git/GitHub(버전관리)를 직접 손으로 세팅하고, 각 도구가 왜 필요한지 설명할 수 있는 수준으로 체득하는 것이 목표다.

### 핵심 학습 내용
- **터미널**: 절대/상대 경로, 파일 조작, 권한(r/w/x) 이해
- **Docker**: 이미지-컨테이너 분리 개념, 포트매핑, 바인드마운트, 볼륨
- **Git/GitHub**: 로컬 버전관리(Git) vs 원격 협업 플랫폼(GitHub) 역할 차이

### 작업 환경
Windows 11에서 작업 후 GitHub에 push. 동료평가는 Mac(OrbStack 환경)에서 수행됨.
크로스플랫폼 호환성을 위해 `.gitattributes`로 LF 줄바꿈 강제 적용.

---

## 1) 실행 환경

| 항목 | 내용 |
|------|------|
| OS | macOS (평가 환경) / Windows 11 Home (작업 환경) |
| Shell | bash (Git Bash / PowerShell) |
| Terminal | Antigravity Terminal (Windows), PowerShell |
| Docker | 29.6.2 (docker:desktop-linux) |
| Git | 2.53.0.windows.2 |

---

## 2) 수행 체크리스트

- [x] 터미널 기본 조작 및 폴더 구성
- [x] 권한 변경 실습 (chmod) - ubuntu 컨테이너 내부에서 수행
- [x] Docker 설치/점검 (docker --version, docker info)
- [x] hello-world 컨테이너 실행
- [x] ubuntu 컨테이너 진입 및 명령 실행
- [x] Dockerfile 빌드 및 컨테이너 실행
- [x] 포트 매핑 접속 확인 (브라우저 스크린샷)
- [x] 바인드 마운트 반영 확인
- [x] Docker 볼륨 영속성 검증
- [x] Git 사용자 설정 (git config --list)
- [ ] GitHub 저장소 연동 (스크린샷 첨부 예정)

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

ubuntu 컨테이너(`vol-test2`) 내부에서 수행.

```bash
root@a80b52f7c295:/# pwd
/
root@a80b52f7c295:/# mkdir -p ~/practice/docs
root@a80b52f7c295:/# cd ~/practice
root@a80b52f7c295:~/practice# ls -la
total 12
drwxr-xr-x 3 root root 4096 Jul 28 13:00 .
drwx------ 1 root root 4096 Jul 28 13:00 ..
drwxr-xr-x 2 root root 4096 Jul 28 13:00 docs
root@a80b52f7c295:~/practice# touch hello.txt
root@a80b52f7c295:~/practice# cp hello.txt docs/hello-copy.txt
root@a80b52f7c295:~/practice# mv hello.txt renamed.txt
root@a80b52f7c295:~/practice# ls -la
total 12
drwxr-xr-x 3 root root 4096 Jul 28 13:00 .
drwx------ 1 root root 4096 Jul 28 13:00 ..
drwxr-xr-x 2 root root 4096 Jul 28 13:00 docs
-rw-r--r-- 1 root root    0 Jul 28 13:00 renamed.txt
root@a80b52f7c295:~/practice# rm renamed.txt
root@a80b52f7c295:~/practice# ls -la
total 12
drwxr-xr-x 3 root root 4096 Jul 28 13:03 .
drwx------ 1 root root 4096 Jul 28 13:00 ..
drw-r--r-- 2 root root 4096 Jul 28 13:00 docs
```

### 3-2. 권한 실습

```bash
# 변경 전 확인
root@a80b52f7c295:~/practice# ls -la renamed.txt
-rw-r--r-- 1 root root 0 Jul 28 13:00 renamed.txt

# 644 -> 755 (실행권한 추가)
root@a80b52f7c295:~/practice# chmod 755 renamed.txt
root@a80b52f7c295:~/practice# ls -la renamed.txt
-rwxr-xr-x 1 root root 0 Jul 28 13:00 renamed.txt

# 디렉토리 755 -> 644 (실행권한 제거)
root@a80b52f7c295:~/practice# chmod 644 docs/
root@a80b52f7c295:~/practice# ls -la
total 12
drwxr-xr-x 3 root root 4096 Jul 28 13:00 .
drwx------ 1 root root 4096 Jul 28 13:00 ..
drw-r--r-- 2 root root 4096 Jul 28 13:00 docs
-rwxr-xr-x 1 root root    0 Jul 28 13:00 renamed.txt
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
Docker version 29.6.2, build dfc4efb

$ docker info
Client:
 Version:    29.6.2
 Context:    desktop-linux
 Debug Mode: false

Server:
 Containers: 5
  Running: 3
  Paused: 0
  Stopped: 2
 Images: 3
 Server Version: 29.6.2
 Storage Driver: overlayfs
 Logging Driver: json-file
 Cgroup Driver: cgroupfs
 Kernel Version: 6.18.33.2-microsoft-standard-WSL2
 Operating System: Docker Desktop
 OSType: linux
 Architecture: x86_64
 CPUs: 12
 Total Memory: 3.241GiB
 Debug Mode: false
 Live Restore Enabled: false
```

> Docker 데몬 정상 동작 확인. Server 섹션이 출력되면 daemon이 실행 중임을 의미함.

---

## 5) Docker 기본 운영

```bash
$ docker run hello-world
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
4f55086f7dd0: Pull complete
Digest: sha256:c3cbe1cc1aa588a64951ac6286e0df7b27fe2e6324b1001c619bb358770c0178
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

$ docker run -it ubuntu bash
root@e4f96ac758ff:/# ls
bin   dev  home  lib64  mnt  proc  run   srv  tmp  var
boot  etc  lib   media  opt  root  sbin  sys  usr
root@e4f96ac758ff:/# echo "hello from ubuntu"
hello from ubuntu
root@e4f96ac758ff:/# exit

**컨테이너 종료/유지 방식 차이 관찰:**

| 방식 | 명령 | 컨테이너 상태 | 특징 |
|------|------|--------------|------|
| `exit` | 셸에서 exit 입력 | 종료(Exited) | 컨테이너가 완전히 멈춤 |
| `Ctrl+P, Q` | 키보드 단축키 | 실행 유지(Up) | 컨테이너는 살아있고 셸만 분리 |
| `docker exec` | 실행 중 컨테이너에 명령 추가 | 실행 유지 | 이미 떠 있는 컨테이너에 접속. 볼륨 실습에서 `docker exec vol-test2 bash -c "..."` 방식으로 사용 |

> `docker run -it`는 새 컨테이너를 만들며 진입. `docker exec -it`는 이미 실행 중인 컨테이너에 추가로 진입. exit해도 컨테이너는 계속 실행됨.

$ docker images
IMAGE                ID             DISK USAGE
hello-world:latest   c3cbe1cc1aa5   25.9kB
ubuntu:latest        3131b4cc82a7   161MB

$ docker ps -a
CONTAINER ID   IMAGE         COMMAND    CREATED   STATUS                    NAMES
e4f96ac758ff   ubuntu        "bash"     ...        Exited (0)               keen_banach
3721937481ee   hello-world   "/hello"   ...        Exited (0)               friendly_gagarin

$ docker logs e4f96ac758ff
root@e4f96ac758ff:/# ls
bin   dev  home  lib64  mnt  proc  run   srv  tmp  var
boot  etc  lib   media  opt  root  sbin  sys  usr
root@e4f96ac758ff:/# echo "hello from ubuntu"
hello from ubuntu

$ docker stats --no-stream
CONTAINER ID   NAME      CPU %     MEM USAGE / LIMIT   MEM %     NET I/O   BLOCK I/O   PIDS
(실행 중인 컨테이너 없음 - 빈 표 출력)
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
$ docker build -t my-web:1.0 .
[+] Building 1.6s (7/7) FINISHED                       docker:desktop-linux
 => [internal] load build definition from Dockerfile   0.1s
 => [internal] load metadata for docker.io/library/nginx:alpine   1.0s
 => [1/2] FROM docker.io/library/nginx:alpine@sha256:4a73...      0.1s
 => [2/2] COPY site/ /usr/share/nginx/html/                       0.0s
 => exporting to image                                             0.3s
 => naming to docker.io/library/my-web:1.0                        0.0s

$ docker run -d -p 8080:80 --name my-web-8080 my-web:1.0
723c77f9dd5a...

$ docker run -d -p 8081:80 --name my-web-bind \
  -v "d:/Projects/Codyssey with Claude/week1-mission1/site:/usr/share/nginx/html" \
  my-web:1.0
```

**브라우저 접속 증거:**

포트 매핑(8080) 및 바인드 마운트(8081) 브라우저 스크린샷 참고.

바인드 마운트 검증: `index.html`에서 "Running" -> "Running [Bind Mount Test]" 수정 후 브라우저 새로고침으로 즉시 반영 확인.

---

## 7) Docker 볼륨 영속성 검증

```bash
$ docker volume create mydata
mydata

$ docker run -d --name vol-test -v mydata:/data ubuntu sleep infinity
43bc9e5b8241...

$ docker exec -it vol-test bash -c "echo 'codyssey-test' > /data/hello.txt && cat /data/hello.txt"
codyssey-test

$ docker rm -f vol-test
vol-test

$ docker run -d --name vol-test2 -v mydata:/data ubuntu sleep infinity
a80b52f7c295...

$ docker exec vol-test2 bash -c "cat /data/hello.txt"
codyssey-test
```

**검증 결과:** `vol-test` 삭제 후 `vol-test2`에서 동일 데이터(`codyssey-test`) 유지 확인. 볼륨이 컨테이너 생명주기와 독립적으로 존재함을 증명.

---

## 8) Git 설정 및 GitHub 연동

```bash
$ git config --list
diff.astextplain.textconv=astextplain
filter.lfs.clean=git-lfs clean -- %f
filter.lfs.smudge=git-lfs smudge -- %f
filter.lfs.process=git-lfs filter-process
filter.lfs.required=true
http.sslbackend=schannel
core.autocrlf=true          # 전역(global) 기본값
core.fscache=true
core.symlinks=false
pull.rebase=false
credential.helper=manager
init.defaultbranch=master
user.email=kimyhwdcp@gmail.com
user.name=MylovelyCatMori
core.repositoryformatversion=0
core.filemode=false
core.bare=false
core.logallrefupdates=true
core.ignorecase=true
core.autocrlf=false         # 로컬(이 저장소) 설정 - 전역 덮어씀
user.name=MylovelyCatMori
user.email=kimyhwdcp@gmail.com
remote.origin.url=https://github.com/MylovelyCatMori/Marina2nd_Codyssey.git
remote.origin.fetch=+refs/heads/*:refs/remotes/origin/*
branch.master.remote=origin
branch.master.merge=refs/heads/master
```

> 민감정보(토큰, 비밀번호) 미포함 확인

**GitHub 저장소:** https://github.com/MylovelyCatMori/Marina2nd_Codyssey

**커밋 내역:** https://github.com/MylovelyCatMori/Marina2nd_Codyssey/commits/master

**GitHub 연동 증거 (스크린샷):**
> 저장소 메인 페이지 스크린샷 첨부

---

## 9) 트러블슈팅

### Case 1: gh 설치 후 `command not found` 오류

| 항목 | 내용 |
|------|------|
| 문제 | `winget install --id GitHub.cli`로 gh 설치 완료했으나 터미널에서 `gh: command not found` 오류 발생 |
| 원인 가설 | 설치 시점에 열려 있던 터미널 세션은 PATH 환경변수를 설치 전 상태로 유지함. 새로 추가된 경로를 인식하지 못함 |
| 확인 방법 | 새 터미널(PowerShell) 창을 열고 `gh --version` 실행 |
| 해결/대안 | 새 터미널에서 `gh --version` 정상 출력 확인. 기존 터미널 세션은 재시작 전까지 새 PATH 미반영 |

```bash
# 기존 터미널 (오류)
$ gh --version
command not found: gh

# 새 터미널에서 확인
$ gh --version
gh version 2.96.0 (2026-07-02)
```

---

### Case 2: 바인드 마운트 `docker run` 명령 미실행

| 항목 | 내용 |
|------|------|
| 문제 | `docker run -d -p 8081:80 ... my-web:1.0` 실행했으나 컨테이너가 생성되지 않음. `docker ps -a`에서 해당 컨테이너 없음 |
| 원인 가설 | 긴 명령어를 여러 줄로 나눠 입력하는 과정에서 줄바꿈 처리가 되지 않아 명령이 실제로 실행되지 않음 |
| 확인 방법 | `docker logs my-web-bind` 실행 시 `Error response from daemon: No such container` 응답으로 미생성 확인 |
| 해결/대안 | 명령을 한 줄로 붙여서 재입력. 컨테이너 ID 해시가 출력되며 정상 생성 확인 |

```bash
# 실패: 명령 미실행
$ docker run -d -p 8081:80 --name my-web-bind \
  -v "d:/Projects/..." my-web:1.0
# (아무 출력 없음)

$ docker logs my-web-bind
Error response from daemon: No such container: my-web-bind

# 해결: 한 줄로 재실행
$ docker run -d -p 8081:80 --name my-web-bind -v "d:/Projects/Codyssey with Claude/week1-mission1/site:/usr/share/nginx/html" my-web:1.0
7672a7f7f6cd...  # 컨테이너 ID 출력 = 정상 생성
```

### Case 3: 포트 충돌 진단 절차

| 항목 | 내용 |
|------|------|
| 문제 | `docker run -p 8080:80` 실행 시 "port is already allocated" 또는 브라우저 연결 거부 발생 |
| 원인 가설 | 호스트 8080번 포트를 다른 프로세스(또는 이전 컨테이너)가 이미 점유 중 |
| 확인 방법 | 포트 점유 프로세스 확인 후 종료 또는 다른 포트로 변경 |
| 해결/대안 | 점유 프로세스 종료 또는 `-p 8082:80`처럼 다른 호스트 포트 사용 |

```bash
# 1단계: 어떤 컨테이너가 포트 점유 중인지 확인
$ docker ps
CONTAINER ID   IMAGE        PORTS                  NAMES
723c77f9dd5a   my-web:1.0   0.0.0.0:8080->80/tcp   my-web-8080

# 2단계: 컨테이너가 아닌 일반 프로세스 확인 (Linux/Mac)
$ ss -tulnp | grep 8080
# 또는
$ netstat -ano | findstr 8080   # Windows

# 3단계: 해결 - 기존 컨테이너 중지 후 재실행
$ docker stop my-web-8080
$ docker run -d -p 8080:80 --name my-web-new my-web:1.0

# 또는 다른 포트로 우회
$ docker run -d -p 8082:80 --name my-web-8082 my-web:1.0
```

> 포트는 한 번에 하나의 프로세스만 점유 가능. 충돌 시 먼저 `docker ps`로 컨테이너 점유 여부 확인, 없으면 OS 프로세스 확인 순으로 진단한다.

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
