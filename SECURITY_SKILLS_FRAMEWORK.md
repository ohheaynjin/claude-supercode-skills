# 보안 기술 자동화 프레임워크 - 완료

## 개요
OpenCode 프로젝트의 4가지 보안 관련 기술을 위해 만들어진 포괄적인 보안 자동화 프레임워크입니다.

## 스킬 생성

### 1. 보안 감사자 기술
**위치:**`claude-skills-conversion/security-auditor-skill/`

**스크립트(Python 파일 8개):**
-`scripts/scan_vulnerabilities.py`- 보안 취약점 스캐닝(Bandit, Safety)
-`scripts/detect_secrets.py`- 비밀 감지(API 키, 비밀번호, 토큰)
-`scripts/audit_dependencies.py`- 종속성 취약점 점검(pip-audit, npm audit)
-`scripts/scan_containers.py`- 컨테이너 보안 스캐닝(Docker, Kubernetes, Trivy)
-`scripts/audit_infrastructure.py`- 인프라 보안 감사(Terraform, CloudFormation)
-`scripts/review_config.py`- 구성 검토(하드코딩된 자격 증명, 취약한 비밀번호)
-`scripts/sast_scan.py`- SAST 자동화(SonarQube, Semgrep, CodeQL)
-`scripts/dast_scan.py`- DAST 자동화(OWASP ZAP, Głoso, SQLMap)

**참조(마크다운 파일 4개):**
-`references/owasp_top10.md`- 패턴 및 교정을 통한 OWASP 상위 10대 보안 위험
-`references/security_frameworks.md`- 보안 프레임워크(OWASP, NIST, CIS, ISO, PCI DSS, HIPAA, GDPR, SOC 2)
-`references/remediation_guide.md`- 보안 취약점 개선 절차
-`references/report_templates.md`- 보안 보고서 템플릿(경영 요약, 기술, 규정 준수)

### 2. 침투 테스터 스킬
**위치:**`claude-skills-conversion/penetration-tester-skill/`

**스크립트(7개 Python 파일):**
-`scripts/recon_scan.py`- 자동 정찰(DNS, 하위 도메인 열거, 포트 스캐닝)
-`scripts/vuln_scan.py`- 취약점 스캐닝(Nessus, OpenVAS, Nmap)
-`scripts/web_app_test.py`- 웹 애플리케이션 보안 테스트(OWASP ZAP, Burp Suite, XSSer)
-`scripts/sql_injection_test.py`- SQL 주입 테스트(SQLMap)
-`scripts/xss_test.py`- XSS/CSRF 감지(XSSer, XSStrike)
-`scripts/auth_test.py`- 인증 및 승인 테스트(Hydra, 세션 관리)
-`scripts/generate_report.py`- CVSS 채점을 통한 침투 테스트 보고서 생성

**참조(마크다운 파일 3개):**
-`references/attack_vectors.md`- 일반적인 공격 벡터 및 악용 기법
-`references/cvss_scoring.md`- 계산기가 포함된 CVSS v3.1 채점 가이드
-`references/testing_methodology.md`- PTES 및 OSSTMM 테스트 방법론
-`references/tool_setup.md`- 침투 테스트 도구 설정 가이드 (Kali, Ubuntu, macOS, Windows, Cloud)

### 3. 건축가 리뷰어 스킬
**위치:**`claude-skills-conversion/architect-reviewer-skill/`

**스크립트(4개의 Python 파일):**
-`scripts/analyze_patterns.py`- 아키텍처 패턴 분석(마이크로서비스, 모놀리스, 이벤트 중심)
-`scripts/security_design_review.py`- 보안 설계 검토(인증, 암호화, 입력 검증)
-`scripts/threat_model.py`- STRIDE 방법론을 이용한 위협 모델링
-`scripts/identify_spof.py`- 단일 장애점 식별

**참조(마크다운 파일 3개):**
-`references/stride_methodology.md`- STRIDE 위협 모델링 종합 가이드
-`references/architecture_principles.md`- 소프트웨어 아키텍처 모범 사례 및 원칙
-`references/security_checklist.md`- 아키텍처 보안 체크리스트

### 4. 규정 준수 감사자 기술
**위치:**`claude-skills-conversion/compliance-auditor-skill/`

**스크립트(7개 Python 파일):**
-`scripts/check_gdpr.py`- GDPR 준수 확인(데이터 최소화, 동의, 삭제 권한)
-`scripts/validate_hipaa.py`- HIPAA 검증(PHI 보호, 감사 통제)
-`scripts/collect_soc2_evidence.py`- SOC 2 증거 수집(보안, 가용성, 처리 무결성, 기밀성, 개인 정보 보호)
-`scripts/scan_pci_dss.py`- PCI DSS 스캐닝(카드 소지자 데이터, 암호화 표준)
-`scripts/validate_nist.py`- NIST 제어 검증(CSF, SP 800-53)
-`scripts/assess_iso27001.py`- ISO 27001 평가(ISMS 제어)
-`scripts/generate_report.py`- 규정 준수 보고서 생성

**참조(마크다운 파일 5개):**
-`references/gdpr_requirements.md`- GDPR 요구 사항 및 규정 준수 확인
-`references/hipaa_guidelines.md`- HIPAA 지침 및 통제
-`references/soc2_controls.md`- SOC 2 Type 2 심사 기준 및 제어
-`references/pci_dss_standard.md`- PCI DSS v4.0 요구 사항 및 규정 준수 체크리스트
-`references/nist_controls.md`- NIST 사이버 보안 프레임워크 및 SP 800-53 제어

## 주요 기능

### 스크립트 기능
- **오류 처리:** 강력한 오류 처리를 위한 블록 시도/제외
- **입력 검증:** 처리 전 입력 검증
- **로깅:** 디버깅 및 감사 추적을 위한 로깅 지우기
- **구성 지원:** YAML/JSON 구성 파일 지원
- **명령줄 인터페이스:** 유연한 사용을 위한 Argparse
- **출력 형식:** JSON 및 텍스트 출력 옵션
- **파일 출력:** 지정된 파일에 보고서 저장

### 보안 기능
- **안전한 작업:** 기본적으로 읽기 전용 작업
- **비밀 로깅 없음:** 민감한 데이터에 대한 마스킹된 출력
- **프로덕션 경고:** 프로덕션에서 실행하기 전에 경고 지우기
- **책임 공개:** 책임 공개 관행에 대한 언급
- **권한 확인:** 승인된 대상만 테스트하라는 경고

### 참조 기능
- **포괄적인 범위:** 보안 주제에 대한 광범위한 범위
- **모범 사례:** 업계 표준 보안 사례
- **수정 지침:** 문제 해결을 위한 명확한 단계
- **규정 준수 매핑:** 주요 규정 준수 프레임워크에 대한 매핑
- **도구 참조:** 공식 도구 및 문서 링크
- **빠른 시작 가이드:** 각 도구/프레임워크에 대한 시작 가이드

## 사용 예

### 보안 감사관```bash
# Vulnerability scanning
python3 scripts/scan_vulnerabilities.py . --format json --output vulnerability_report.json

# Secret detection
python3 scripts/detect_secrets.py . --config config/security.yaml --output secrets.json

# Dependency audit
python3 scripts/audit_dependencies.py . --format text

# Container security scan
python3 scripts/scan_containers.py --dockerfile Dockerfile

# Infrastructure audit
python3 scripts/audit_infrastructure.py terraform/

# Configuration review
python3 scripts/review_config.py src/

# SAST scan
python3 scripts/sast_scan.py . --language python

# DAST scan
python3 scripts/dast_scan.py https://example.com --format text --output dast_report.txt
```

### 침투 테스터```bash
# Reconnaissance scan
python3 scripts/recon_scan.py target.com --format json --output recon_data.json

# Vulnerability scanning
python3 scripts/vuln_scan.py 192.168.1.0/24 --format text

# Web application testing
python3 scripts/web_app_test.py https://example.com --config config/pentest.yaml

# SQL injection testing
python3 scripts/sql_injection_test.py http://example.com/login --format json

# XSS testing
python3 scripts/xss_test.py http://example.com --output xss_report.txt

# Authentication testing
python3 scripts/auth_test.py http://example.com --brute-force --output auth_test.json

# Generate penetration test report
python3 scripts/generate_report.py --findings pentest_findings.json --output final_report.md
```

### 건축가 검토자```bash
# Architecture pattern analysis
python3 scripts/analyze_patterns.py . --format json --output architecture_analysis.json

# Security design review
python3 scripts/security_design_review.py . --check-auth --check-encryption

# Threat modeling
python3 scripts/threat_model.py . --methodology STRIDE --output threat_model.json

# Single Point of Failure identification
python3 scripts/identify_spof.py . --check-dependencies --check-infrastructure
```

### 규정 준수 감사관```bash
# GDPR compliance check
python3 scripts/check_gdpr.py . --config config/compliance.yaml --output gdpr_report.json

# HIPAA validation
python3 scripts/validate_hipaa.py . --format text

# SOC 2 evidence collection
python3 scripts/collect_soc2_evidence.py . --framework SOC2_Type2 --output soc2_evidence/

# PCI DSS scanning
python3 scripts/scan_pci_dss.py . --scan_level full

# NIST controls validation
python3 scripts/validate_nist.py . --framework CSF

# ISO 27001 assessment
python3 scripts/assess_iso27001.py . --controls annex_a --output iso_report.md

# Generate compliance report
python3 scripts/generate_report.py --evidence evidence/ --compliance SOC2 --output compliance_report.md
```

## 구성 템플릿

### 보안 감사자 구성```yaml
# config/security.yaml
security:
  scan_paths: ['.']
  severity_threshold: 'medium'
  exclude_patterns: ['venv', '__pycache__', '.git', 'node_modules']
  
  scan_vulnerabilities:
    language: 'auto'
    
  detect_secrets:
    file_extensions: ['.py', '.js', '.ts', '.java', '.go']
    max_file_size_mb: 10
```

### 침투 테스터 구성```yaml
# config/pentest.yaml
penetration_testing:
  target_domains: []
  wordlist: /usr/share/wordlists/dirb/common.txt
  max_threads: 50
  scan_depth: 3
```

### 규정 준수 감사자 구성```yaml
# config/compliance.yaml
compliance_auditing:
  audit_scope: '.'
  frameworks: ['SOC2', 'GDPR', 'HIPAA', 'PCI_DSS', 'ISO27001', 'NIST']
```

## 다른 기술과의 통합

보안 기술은 다음과 통합되도록 설계되었습니다.
- **백엔드 개발자** - 보안 제어 구현용
- **devops-engineer** - 인프라 보안 구현용
- **플랫폼 엔지니어** - 클라우드 보안 구현을 위해
- **cloud-architect** - 보안 아키텍처 설계용
- **코드 검토자** - 보안 코드 검토용

## 모범 사례

### 스크립트 실행 전
1. **검토 범위:** 대상을 테스트할 권한이 있는지 확인하세요.
2. **데이터 백업:** 보안 검사를 실행하기 전에 항상 백업하세요.
3. **스테이징에서 테스트:** 먼저 비프로덕션 환경에서 보안 도구를 테스트합니다.
4. **구성 확인:** 실행 전 구성 파일을 검토합니다.

### 스크립트 실행 중
1. **진행 상황 모니터링:** 예상치 못한 동작을 관찰하세요.
2. **로그 확인:** 로그에서 오류 또는 경고를 검토합니다.
3. **결과 검증:** 가능하면 결과를 수동으로 교차 확인합니다.
4. **문제가 있는 경우 중지:** 예상치 못한 동작이 감지되면 종료합니다.

### 스크립트 실행 후
1. **결과 검토:** 모든 결과를 주의 깊게 검토합니다.
2. **해결 우선순위 지정:** 중요하고 심각도가 높은 문제에 집중
3. **문서화 작업:** 문제 해결 단계 기록 유지
4. **재테스트:** 해결 방법이 효과적인지 확인합니다.

## 법적, 윤리적 고려 사항

**중요한 경고:**
- 귀하가 소유하거나 서면으로 테스트 승인을 받은 시스템만 테스트하십시오.
- 테스트 전 서면 승인을 받으세요.
- 책임 있는 공개 관행을 따르십시오.
- 현지 법률 및 규정을 준수합니다.
- 안전한 테스트 환경을 사용하세요
- 절대 실제 피해를 입히지 마세요.
- 결과를 공개하기 전에 공급업체에 책임 있게 보고합니다.

## 지원되는 규정 준수 프레임워크

| 뼈대 | 적용 범위 |
|-----------|----------|
| OWASP 상위 10위 | 웹 애플리케이션 보안 위험 |
| OWASP ASVS | 애플리케이션 보안 검증 표준 |
| NIST SP 800-53 | 연방 정보 시스템 통제 |
| NIST CSF | 사이버보안 프레임워크 |
| CIS 제어 | 우선순위 보안 제어 |
| ISO 27001 | 정보보안 관리 |
| ISO 27701 | 개인정보 관리 |
| PCI DSS v4.0 | 결제 카드 산업 보안 |
| HIPAA | 의료정보 개인정보 보호 |
| GDPR | EU 데이터 보호 규정 |
| SOC 2 유형 2 | 보안, 가용성, 처리 무결성, 기밀성, 개인 정보 보호 |
| 보폭 | 위협 모델링 방법론 |

## 유지 관리 및 업데이트

### 정기 업데이트
- 정기적으로 종속성 패키지 업데이트
- 보안 프레임워크 업데이트 검토
- 새로운 표준으로 참조 문서 업데이트
- 사용자 피드백을 기반으로 스크립트 개선

### 지속적인 개선
- 스크립트 실행 결과 모니터링
- 사용자 피드백 수집
- 개선할 부분 파악
- 개선 및 최적화 구현

## 지원 및 문서

### 문서
- 포괄적인 인라인 코드 주석
- 스크립트 도움말의 사용 예
- 구성 파일 예시
- 통합 가이드

### 문제 해결
- 명확한 안내가 포함된 오류 메시지
- 디버깅을 위한 로깅
- 참조 문서의 FAQ 섹션
- 도구 설치 가이드

## 요약

이 보안 자동화 프레임워크는 다음을 제공합니다.

4가지 기술에 걸친 **27개의 Python 스크립트**
주요 보안 프레임워크를 다루는 **15개 참조 문서**
보안, 침투 테스트, 아키텍처 검토 및 규정 준수에 대한 **포괄적인 범위**
오류 처리 및 검증 기능이 포함된 **프로덕션용 스크립트**
모범 사례와 예시가 포함된 **광범위한 문서**

모든 스크립트의 우선순위는 다음과 같습니다.
- 안전하고 비파괴적인 작업
- 실제 비밀은 기록되지 않습니다(마스킹된 출력만 해당).
- 테스트를 위한 읽기 전용 작업(승인된 환경이 아닌 경우)
- 프로덕션 실행에 대한 명확한 경고
- 책임 있는 공개 관행
- 공식 보안 프레임워크 및 표준 참조

프레임워크는 보안 평가, 침투 테스트, 아키텍처 검토 및 규정 준수 감사에 즉시 사용할 수 있습니다.