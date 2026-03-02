# STRIDE 위협 모델링 방법론

## 개요
STRIDE는 시스템 설계에서 보안 위협을 식별하기 위해 Microsoft에서 개발한 위협 모델링 프레임워크입니다.

## 스트라이드 카테고리

### 스푸핑(S)

**정의:** 사물 또는 누군가의 명의를 도용하는 행위

**예:**
- 스푸핑된 사용자 인증
- 가짜 API 엔드포인트
- 이메일 스푸핑
- 중간자 공격

**탐지:**
```python
# Check for weak authentication
def check_spoofing_risks(auth_mechanism):
    risks = []
    
    if not auth_mechanism.get('mfa_enabled'):
        risks.append('No multi-factor authentication')
    
    if auth_mechanism.get('type') == 'basic':
        risks.append('Basic authentication (use HTTPS with strong auth)')
    
    return risks
```
**완화:**
- 강력한 인증(비밀번호, 인증서, 생체인식)
- 다단계 인증(MFA)
- 인증서 고정
- 유효한 인증서가 있는 HTTPS/TLS
- 세션 관리 모범 사례

### 탬퍼링(T)

**정의:** 데이터 또는 코드 수정

**예:**
- 데이터 주입 공격
- 중간자 수정
- 코드 주입
- 매개변수 변조

**탐지:**
```python
# Check for integrity protection
def check_tampering_protection(data_handling):
    risks = []
    
    if not data_handling.get('digital_signatures'):
        risks.append('No digital signatures for data integrity')
    
    if not data_handling.get('hash_verification'):
        risks.append('No hash verification for data integrity')
    
    return risks
```
**완화:**
- 디지털 서명
- 해시 검증(SHA-256, SHA-3)
- 체크섬
- 데이터에 대한 접근 통제
- 보안 통신 채널(TLS)
- 코드 서명

### 부인(R)

**정의:** 사용자가 작업 수행을 거부합니다.

**예:**
- 거래 거부
- 감사 로그 변조
- 부인방지 실패

**탐지:**
```python
# Check for audit logging
def check_repudiation_prevention(logging_config):
    risks = []
    
    if not logging_config.get('audit_trail'):
        risks.append('No audit trail implemented')
    
    if not logging_config.get('immutable_logs'):
        risks.append('Audit logs can be modified')
    
    return risks
```
**완화:**
- 종합적인 감사 로깅
- 불변의 감사 로그
- 로그의 디지털 서명
- 부인방지 서비스
- 사용자 활동 추적
- 시간 동기화

### 정보 공개(I)

**정의:** 승인되지 않은 당사자에게 정보 노출

**예:**
- 데이터 유출
- 암호화되지 않은 민감한 데이터
- 노출된 API
- 보안되지 않은 데이터베이스

**탐지:**
```python
# Check for data protection
def check_information_disclosure_risks(data_protection):
    risks = []
    
    if not data_protection.get('encryption_at_rest'):
        risks.append('Data not encrypted at rest')
    
    if not data_protection.get('encryption_in_transit'):
        risks.append('Data not encrypted in transit')
    
    return risks
```
**완화:**
- 암호화(휴식은 AES-256, 전송은 TLS)
- 접근 제어 및 최소 권한
- 데이터 마스킹/익명화
- 안전한 API 설계
- 데이터 분류
- 안전한 폐기

### 서비스 거부(D)

**정의:** 서비스 또는 액세스 거부

**예:**
- DDoS 공격
- 자원 고갈
- 애플리케이션 충돌
- 네트워크 플러딩

**탐지:**
```python
# Check for DoS protections
def check_dos_protections(infra_config):
    risks = []
    
    if not infra_config.get('rate_limiting'):
        risks.append('No rate limiting configured')
    
    if not infra_config.get('load_balancing'):
        risks.append('No load balancing for high availability')
    
    return risks
```
**완화:**
- 속도 제한
- 스로틀링
- 로드 밸런싱
- 중복성(다중 AZ, 다중 지역)
- 자동 크기 조정
- DDoS 보호 서비스
- 회로 차단기

### 권한 승격(E)

**정의:** 승인된 것보다 더 높은 권한을 얻습니다.

**예:**
- 권한 상승 공격
- 수평적/수직적 권한 상승
- 손상된 액세스 제어
- 관리자 인터페이스 노출

**탐지:**
```python
# Check for privilege controls
def check_privilege_controls(auth_config):
    risks = []
    
    if not auth_config.get('least_privilege'):
        risks.append('Least privilege principle not enforced')
    
    if not auth_config.get('role_based_access'):
        risks.append('No role-based access control')
    
    return risks
```
**완화:**
- 최소 권한의 원칙
- 역할 기반 액세스 제어(RBAC)
- 권한 분리
- 안전한 세션 관리
- 정기 권한 감사
- 입력 검증

## 위협 모델링 프로세스

### 1단계: 시스템 분해

**요소 식별:**
- 데이터 저장소(데이터베이스, 파일 시스템)
- 데이터 흐름(API 호출, 메시지 대기열)
- 프로세스(서비스, 기능)
- 외부 엔터티(사용자, 제3자 서비스)

**다이어그램 요소:**
```
[User] --(HTTP)--> [Load Balancer] --(HTTP)--> [Web Server]
Web Server --(SQL)--> [Database]
Web Server --(gRPC)--> [Microservice A]
Microservice A --(Kafka)--> [Microservice B]
```
### 2단계: STRIDE 적용

**각 요소에 대해:**
1. 스푸핑될 수 있나요?
2. 변조가 가능한가요?
3. 부인할 수 있나요?
4. 정보를 공개할 수 있나요?
5. 서비스가 거부될 수 있나요?
6. 권한을 높일 수 있나요?

**예제 테이블:**

| 요소 | 스푸핑 | 조작 | 부인 | 정보 공개 | DoS | 고도 |
|---------|------------|------------|---------------|------|------|------------|
| 로그인 양식 | 예 | 아니요 | 예 | 예 | 예 | 예 |
| 데이터베이스 | 예 | 예 | 아니요 | 예 | 예 | 예 |
| API 게이트웨이 | 예 | 예 | 예 | 예 | 예 | 예 |

### 3단계: 위협 분석

**위협 분석 프레임워크:**
```python
def analyze_threat(threat, likelihood, impact):
    """
    likelihood: low, medium, high
    impact: low, medium, high
    """
    risk_matrix = {
        ('low', 'low'): 'low',
        ('low', 'medium'): 'medium',
        ('low', 'high'): 'high',
        ('medium', 'low'): 'medium',
        ('medium', 'medium'): 'high',
        ('medium', 'high'): 'critical',
        ('high', 'low'): 'high',
        ('high', 'medium'): 'critical',
        ('high', 'high'): 'critical'
    }
    
    return risk_matrix[(likelihood, impact)]
```
### 4단계: 문서 조사 결과

**위협 문서 템플릿:**
```markdown
## Threat: [Title]

**STRIDE Category:** [Spoofing/Tampering/etc]
**Target:** [Element/Component]
**Likelihood:** [Low/Medium/High]
**Impact:** [Low/Medium/High]
**Risk:** [Calculated Risk]

### Description
[Detailed description of the threat]

### Scenario
[Attack scenario description]

### Mitigation
[Recommended mitigations]

### Verification
[How to verify the mitigation works]
```
## 실제 예

### 웹 애플리케이션 STRIDE 분석

**시스템 구성요소:**
1. 사용자 브라우저
2. 웹 서버(NGINX)
3. 애플리케이션 서버(Node.js)
4. 데이터베이스(PostgreSQL)
5. 레디스 캐시

**위협 분석:**

#### 사용자 브라우저
- **스푸핑:** 피싱 공격
- **조작:** 브라우저 확장
- **부인:** 사용자 조치
- **정보 공개:** 저장된 자격 증명
- **DoS:** 브라우저 정지
- **고도:** 해당 없음

#### 웹 서버
- **스푸핑:** DNS 스푸핑
- **조작:** 구성 변조
- **부인:** 액세스 로그
- **정보 공개:** 헤더 유출
- **DoS:** 리소스 고갈
- **고도:** 해당 없음

#### 애플리케이션 서버
- **스푸핑:** 세션 하이재킹
- **조작:** 변조 요청
- **부인:** 작업 로그
- **정보 공개:** 오류 메시지
- **DoS:** 메모리 고갈
- **승격:** 권한 에스컬레이션

#### 데이터베이스
- **스푸핑:** SQL 주입
- **조작:** 데이터 손상
- **부인:** 거래 로그
- **정보 공개:** 데이터 유출
- **DoS:** 쿼리 과부하
- **승격:** 관리자 에스컬레이션

### API 게이트웨이 STRIDE 분석

**구성요소:**
1. API 게이트웨이
2. 마이크로서비스
3. 메시지 큐
4. 이벤트 버스

**주요 위협:**

#### API 게이트웨이
| 위협 | 설명 | 완화 |
|---------|-------------|------------|
| 스푸핑 | 가짜 API 토큰 | JWT 검증, OAuth 2.0 |
| 조작 | 수정요청 | 메시지 서명 |
| 부인 | 요청 거부 | 로깅 요청 |
| 정보 공개 | API 키 유출 | 안전한 저장 |
| DoS | 비율 제한 우회 | 제한, WAF |
| 고도 | 토큰 권한 상승 | 토큰 범위 |

#### 마이크로서비스 커뮤니케이션
| 위협 | 설명 | 완화 |
|---------|-------------|------------|
| 스푸핑 | 서비스 사칭 | mTLS |
| 조작 | 메시지 변조 | 암호화 |
| 부인 | 메시지 거부 | 감사 로깅 |
| 정보 공개 | 데이터 유출 | 암호화 |
| DoS | 대기열 오버플로 | 배압 |
| 고도 | 서비스 인수 | 최소 권한 |

## 도구 및 자동화

### Microsoft 위협 모델링 도구
- GUI 기반 위협 모델링
- STRIDE 자동 적용
- 다이어그램 시각화
- 다양한 형식으로 내보내기

### OWASP 위협 드래곤
- 웹 기반 위협 모델링
- 협업 모델링
- STRIDE 및 DREAD 모델
- 다른 도구와의 통합

### PyTM(Python 위협 모델링)
```python
#!/usr/bin/env python3
from pytm import TM, Actor, Server, Datastore, Dataflow

tm = TM("Threat Model")
tm.description = "Simple Web App"

user = Actor("User", tm)
webapp = Server("Web Application", tm)
db = Datastore("Database", tm)

user_to_webapp = Dataflow(user, webapp, "User Input")
webapp_to_db = Dataflow(webapp, db, "SQL Query")

tm.process()
```
### 사용자 정의 STRIDE 스크립트
```python
#!/usr/bin/env python3
import yaml
import json

class STRIDEThreatModeler:
    def __init__(self, system_design):
        self.design = system_design
        self.threats = []
    
    def model_threats(self):
        for component in self.design.get('components', []):
            self._check_spoofing(component)
            self._check_tampering(component)
            self._check_repudiation(component)
            self._check_info_disclosure(component)
            self._check_dos(component)
            self._check_elevation(component)
        
        return self.threats
    
    def _check_spoofing(self, component):
        if not component.get('auth_required'):
            self.threats.append({
                'component': component['name'],
                'category': 'Spoofing',
                'severity': 'high',
                'description': 'No authentication required'
            })
    
    # ... other methods ...

if __name__ == '__main__':
    design = {
        'components': [
            {'name': 'API', 'auth_required': True},
            {'name': 'Database', 'auth_required': False}
        ]
    }
    
    modeler = STRIDEThreatModeler(design)
    threats = modeler.model_threats()
    print(json.dumps(threats, indent=2))
```
## 모범 사례

1. **조기 시작:** 구현 후가 아닌 설계 중 위협 모델
2. **반복:** 시스템이 발전함에 따라 위협 모델을 정기적으로 업데이트합니다.
3. **우선순위:** 고위험, 고영향 위협에 집중
4. **문서화:** 자세한 위협 문서를 보관하세요.
5. **확인:** 완화 기능을 테스트하여 제대로 작동하는지 확인하세요.
6. **팀 참여:** 보안, 개발, 운영팀 포함

## 흔히 저지르는 실수

1. **위협 모델링만 구현:** 설계 중 모델링
2. **비즈니스 로직 무시:** 비기술적 위협 고려
3. **업데이트되지 않음:** 시스템 변경으로 모델을 최신 상태로 유지합니다.
4. **구성요소 누락:** 모든 요소가 포함되어 있는지 확인하세요.
5. **외부 종속성 간과:** 타사 서비스 포함

## 참고자료

- [Microsoft STRIDE](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling)
- [OWASP 위협 모델링](https://owasp.org/www-community/threat_modeling)
- [위협 모델링 치트 시트](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html)