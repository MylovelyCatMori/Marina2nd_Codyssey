# General Concepts - 프로젝트 전반 보충 학습

> 특정 미션에 국한되지 않는 일반 개념 학습 기록.
> 동료평가 피드백, 자기주도 학습, 현장 연결 공부 등에서 발생한 개념 누적.
> 덮어쓰기 금지. 추가(append)만 허용.

---

## 네트워크 기초

### 포트(Port) 개념

**개념:** IP 주소 = 건물 주소. 포트 = 호수 번호. 하나의 IP에서 여러 서비스를 구분하는 번호.

**범위: 0 ~ 65535 (총 65,536개)**

| 구역 | 범위 | 특징 | 주요 예시 |
|------|------|------|----------|
| Well-known Ports | 0 ~ 1023 | IANA 전 세계 표준 지정 | 80(HTTP), 443(HTTPS), 22(SSH), 53(DNS), 25(SMTP) |
| Registered Ports | 1024 ~ 49151 | 소프트웨어 관례적 사용 | 3306(MySQL), 5432(PostgreSQL), 8080(개발 웹), 6379(Redis) |
| Dynamic/Private Ports | 49152 ~ 65535 | OS가 클라이언트 측 임시 자동 배정 | 브라우저가 서버 접속 시 사용. 연결 끊으면 반환 |

**IANA:** Internet Assigned Numbers Authority. 인터넷 할당 번호 관리기관.

**[Physical AI 연계] 직접 연계:**
- SSH(22): 엔지니어가 원격으로 로봇 컨트롤러 접속
- 8080: 로봇 상태 모니터링 웹 대시보드
- 502 Modbus TCP: 산업용 센서/액추에이터 제어
- 4840 OPC UA (OPC Unified Architecture): 스마트팩토리 표준 통신. 설비 → MES 데이터 전달
- 1883 MQTT (Message Queuing Telemetry Transport): IoT 센서 데이터 수집 경량 프로토콜
- ROS 2 DDS: Dynamic Ports 구역 자동 사용 (노드 간 통신)

---

## OS / 시스템 기초

### 듀얼부팅 (Dual Booting)

**개념:**
하나의 컴퓨터에 OS를 두 개 설치하여 부팅 시 선택하는 구성.

**부팅 흐름:**
```
전원 ON → BIOS/UEFI (하드웨어 점검) → GRUB (OS 선택) → 선택한 OS 로드
```

**핵심 용어:**
| 용어 | 풀이 | 설명 |
|------|------|------|
| BIOS | Basic Input/Output System | 구형 펌웨어. 하드웨어 점검 후 부트로더 실행 |
| UEFI | Unified Extensible Firmware Interface | 신형 펌웨어. Secure Boot 포함. 현재 주류 |
| GRUB | GRand Unified Bootloader | Ubuntu 설치 시 자동 설치되는 부트로더 |
| Partition | - | 하나의 물리 디스크를 논리적으로 나눈 구역 |
| ISO | International Organization for Standardization | CD/DVD 이미지를 파일로 만든 형식. 설치 디스크 대체 |

**위험 요소:**
- 파티션 잘못 선택 시 Windows 데이터 삭제 가능 → 설치 전 전체 백업 필수
- Secure Boot 충돌 시 부팅 불가 → UEFI 설정 확인 필요

**[Physical AI 연계] 간접 연계:**
- 듀얼부팅 원리("하나의 하드웨어에서 OS 분리")는 산업용 로봇 컨트롤러에서 동일하게 활용
- 로봇 컨트롤러: Ubuntu(ROS 2) + RTOS(실시간 제어) 병존 구성이 일반적

---

### Ubuntu

**개념:**
Linux 커널 위에 Canonical사가 도구와 패키지를 얹어 만든 Linux 배포판(Distribution).

**계층 구조:**
```
Linux 커널 (Linus Torvalds, 1991) - 하드웨어 직접 제어하는 핵심 엔진
    └── Ubuntu = 커널 + apt 패키지 매니저 + 각종 도구 묶음 (Canonical, 영국)
```

**버전 체계:**
```
번호 규칙: 연도.월  (예: 24.04 = 2024년 4월)
LTS (Long Term Support): 5년 보안 지원 보장. 개발/서버 환경 필수.
권장: Ubuntu 24.04 LTS (ROS 2 Jazzy 매칭)
```

**핵심 명령어:**
```bash
sudo apt update          # 패키지 목록 최신화 (설치 안 함)
# sudo = superuser do (관리자 권한 실행)
# apt = Advanced Packaging Tool (패키지 관리자)
# update = 패키지 인덱스 갱신

sudo apt install <이름>  # 패키지 설치
apt list --installed     # 설치된 패키지 목록 확인
```

**[Physical AI 연계] 직접 연계:**
- ROS 2 공식 지원 OS = Ubuntu. 버전 1:1 매칭 필수
  - Ubuntu 22.04 LTS ↔ ROS 2 Humble
  - Ubuntu 24.04 LTS ↔ ROS 2 Jazzy
- 스마트팩토리 로봇 셀 구성: Ubuntu + ROS 2 노드(카메라/로봇팔/PLC 통신) 분리 실행
- Docker + Ubuntu 조합 = 로봇 소프트웨어 개발 환경 구성 실제 방법과 동일

---

### 사용자 계정 / 드라이브 분리 / 듀얼부팅 비교

세 개념은 작동하는 **층(Layer)**이 다르다.

```
[스토리지 층] 파티션
[OS 층]      운영체제
[사용자 층]  사용자 계정
```

| 구분 | 분리 층 | OS 개수 | 분리 범위 |
|------|---------|---------|----------|
| 사용자 계정 | 사용자 층 | 1개 | 사용자 파일/설정만 |
| C: D: E: 드라이브 | 스토리지 층 | 1개 | 저장 공간만 |
| 듀얼부팅 | 스토리지+OS 층 | 2개 | OS 전체 완전 분리 |

**비유:**
- 사용자 계정 = 같은 집, 다른 방
- 드라이브 분리 = 같은 방, 다른 서랍
- 듀얼부팅 = 같은 땅, 다른 건물

**핵심:** 파티션(디스크 나누기)은 세 경우 모두의 기반 기술. 차이는 파티션 위에 무엇을 올리느냐. 데이터 → D: 드라이브. 다른 OS → 듀얼부팅.

**[Physical AI 연계] 참고:**
- 사용자 계정 분리: 로봇 OS에서 운영자/개발자/서비스 계정 분리 (보안)
- 파티션 분리: 펌웨어 파티션(읽기전용) + 데이터 파티션(쓰기가능) 분리. OTA(Over-The-Air, 무선 업데이트) 시 OS 파티션만 교체
- 듀얼부팅 개념: A/B 파티션 스킴. 업데이트 실패 시 이전 OS로 롤백. Tesla/Android 동일 방식.

---
