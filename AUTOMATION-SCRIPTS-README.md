# 자동화 스크립트 읽어보기

이 문서는 Claude Skills Conversion 프로젝트를 위해 생성된 모든 자동화 스크립트에 대한 포괄적인 가이드를 제공합니다. 이러한 스크립트는 일반적인 작업에 대해 실행 가능한 자동화를 제공하여 다양한 기술의 기능을 향상시킵니다.

## 목차

- [디렉토리 구조](#디렉토리-구조)
- [기술별 스크립트](#scripts-by-skill)
- [사용 예](#usage-examples)
- [모범 사례](#best-practices)
- [확장 및 유지 관리](#extension-and-maintenance)
- [문제 해결](#troubleshooting)

## 디렉토리 구조

```
claude-skills-conversion/
├── incident-responder-skill/
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── incident_triage.py
│   │   ├── incident_analysis.py
│   │   ├── incident_response.py
│   │   ├── runbook_generator.py
│   │   ├── maintenance_automation.py
│   │   └── handle_alerts.py (existing)
│   └── references/
│       ├── troubleshooting.md
│       └── best_practices.md
│
├── chaos-engineer-skill/
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── chaos_experiment.py
│   │   └── resilience_assessment.py
│   └── references/
│       ├── troubleshooting.md
│       └── best_practices.md
│
├── error-detective-skill/
│   ├── SKILL.md
│   ├── scripts/
│   │   └── error_detection_automation.py
│   └── references/
│       ├── troubleshooting.md
│       └── best_practices.md
│
├── backend-developer-skill/
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── scaffold_api.py (existing)
│   │   ├── generate_model.py (existing)
│   │   ├── setup_auth.py (existing)
│   │   ├── create_middleware.py (existing)
│   │   ├── error_handler.py (existing)
│   │   ├── setup_logging.py (existing)
│   │   ├── generate_docs.py (existing)
│   │   ├── create_tests.py (existing)
│   │   └── deploy.sh (existing)
│   └── references/
│       ├── troubleshooting.md
│       └── best_practices.md
│
└── build-engineer-skill/
    ├── SKILL.md
    ├── scripts/
    │   ├── config_webpack.py (existing)
    │   ├── config_vite.py (existing)
    │   ├── optimize_cache.py (existing)
    │   ├── code_splitting.py (existing)
    │   ├── dev_server.py (existing)
    │   └── optimize_production.py (existing)
    └── references/
        ├── troubleshooting.md
        └── best_practices.md
```

## 스킬별 스크립트

### 사고 대응 기술

#### `incident_triage.py`

**목적**: 심각도를 분류하고, 팀에 전달하고, 초기 증거를 수집하여 초기 사고 분류를 자동화합니다.

**용법**:```bash
python scripts/incident_triage.py --incident INC-001 --description "Service outage" \
  --impact service_outage --urgency immediate --affected-users 500 \
  --service api-service --output triage_report.json
```

**주요 기능**:
- 자동 심각도 분류(CRITICAL, HIGH, MEDIUM, LOW)
- 사건 유형 및 심각도에 따른 팀 라우팅
- 초기 지표 및 증거 수집
- 종합적인 분류 보고서 생성

**출력**: 분류, 할당된 팀, 측정항목, 권장 조치가 포함된 JSON 분류 보고서입니다.

---

#### `incident_analysis.py`

**목적**: 로그/측정항목의 상관관계를 파악하고 근본 원인을 식별하며 비즈니스 영향을 측정하여 심층적인 사고 분석을 수행합니다.

**용법**:```bash
python scripts/incident_analysis.py --incident INC-001 \
  --start-time "2024-01-12T10:00:00Z" \
  --end-time "2024-01-12T11:30:00Z" \
  --affected-users 500 --downtime 90 \
  --service api-service --output analysis_report.json
```

**주요 기능**:
- 여러 서비스에 걸친 로그 상관관계
- 이상 징후 및 추세에 대한 지표 분석
- 비즈니스 영향 계산(수익, SLA, 사용자)
- 근본 원인 패턴 분석

**출력**: 상관 관계, 지표, 영향, 근본 원인 및 권장 사항이 포함된 JSON 분석 보고서입니다.

---

#### `incident_response.py`

**목적**: 봉쇄, 완화, 팀 조정, 진행 상황 추적을 포함한 사고 대응 조치를 자동화합니다.

**용법**:```bash
# Containment action
python scripts/incident_response.py --incident INC-001 --severity critical \
  --action-type containment --action isolate_service --target api-service

# Team notification
python scripts/incident_response.py --incident INC-001 --severity critical \
  --action-type notify --teams security-engineer devops-incident-responder

# Status update
python scripts/incident_response.py --incident INC-001 --severity critical \
  --action-type status --status investigating --details "Root cause identified"
```

**주요 기능**:
- 사전 정의된 봉쇄 및 완화 조치
- 자동화된 팀 알림
- 상태 업데이트 추적
- 대응 일정 및 감사 추적

**출력**: 실행된 작업, 팀 알림, 현재 상태가 포함된 JSON 응답 보고서입니다.

---

#### `runbook_generator.py`

**목적**: 절차, 팀 연락처 및 커뮤니케이션 템플릿이 포함된 포괄적인 사고 대응 실행서를 생성합니다.

**용법**:```bash
# Generate JSON runbook
python scripts/runbook_generator.py --incident-type service_outage \
  --title "Service Outage Response Runbook" \
  --output service_outage_runbook.json

# Generate Markdown runbook
python scripts/runbook_generator.py --incident-type data_breach \
  --format both --markdown data_breach_runbook.md \
  --output data_breach_runbook.json
```

**주요 기능**:
- 5가지 사고 유형: data_breach, service_outage, security_violation, Database_failure, network_incident
- 각 단계별 대응 절차를 완료하세요.
- 팀 연락처 및 에스컬레이션 경로
- 커뮤니케이션 템플릿(내부, 고객, 임원)
- JSON 및 Markdown 출력 형식

**출력**: JSON 및/또는 Markdown 형식의 포괄적인 런북입니다.

---

#### `maintenance_automation.py`

**목적**: 예약, 백업, 알림, 상태 확인을 포함한 시스템 유지 관리 작업을 자동화합니다.

**용법**:```bash
python scripts/maintenance_automation.py --task system_update \
  --system api-service --start-time "2024-01-20T02:00:00Z" \
  --duration 120 --priority medium --backup-type full \
  --affected-users 0 --output maintenance_report.json
```

**주요 기능**:
- 유지 관리 기간 예약
- 백업 계획 생성(전체, 증분, 차등)
- 이해관계자 알림 생성
- 유지보수 작업 실행
- 유지보수 후 상태 검증

**출력**: 기간, 실행, 검증 및 권장 사항이 포함된 JSON 유지 관리 보고서입니다.

---

### 카오스 엔지니어 스킬

#### `chaos_experiment.py`

**목적**: 가설 설계, 실패 주입, 자동화된 롤백을 통해 카오스 엔지니어링 실험을 자동화합니다.

**용법**:```bash
python scripts/chaos_experiment.py --experiment database-failure-test \
  --target database-service --failure-type pod_kill \
  --blast-radius 5 --duration 15 \
  --output chaos_experiment_report.json
```

**주요 기능**:
- 8가지 오류 유형: pod_kill, network_latency, packet_loss, network_partition, cpu_stress, memory_stress, disk_failure, dns_failure
- 가설 기반 실험 설계
- 폭발 반경 제어(트래픽/사용자 비율)
- 30초 목표로 자동 롤백
- 지표 수집(전, 중, 후)
- 검증 및 교훈을 담은 실험 보고서

**출력**: 설계, 주입, 지표, 가설 검증 및 권장 사항이 포함된 JSON 실험 보고서입니다.

---

#### `resilience_assessment.py`

**목적**: 패턴 분석, SPOF 식별, 장애 조치 테스트, 용량 평가를 통해 시스템 복원력을 평가합니다.

**용법**:```bash
python scripts/resilience_assessment.py --target api-service \
  --component database --output resilience_report.json
```

**주요 기능**:
- 복원력 패턴 분석(회로 차단기, 재시도, 격벽, 시간 초과, 대체)
- SPOF(단일 실패 지점) 식별
- 장애 조치 기능 테스트
- 용량 분석 및 헤드룸 계산
- 전체 탄력성 점수(0~100%)
- 우선순위 개선 로드맵

**출력**: 패턴, SPOF, 장애 조치, 용량, 점수 및 개선 사항이 포함된 JSON 평가 보고서입니다.

---

### 오류탐지 스킬

#### `error_detection_automation.py`

**목적**: 로그를 스캔하고, 서비스 간 상관 관계를 분석하고, 이상 현상을 감지하여 오류 감지 및 분석을 자동화합니다.

**용법**:```bash
# Scan logs for errors
python scripts/error_detection_automation.py --scan \
  --services api-service database-service auth-service \
  --output error_detection_report.json

# Use sample logs for testing
python scripts/error_detection_automation.py --scan \
  --sample-logs --error-count 50 --output test_report.json

# Correlate errors
python scripts/error_detection_automation.py --correlate \
  --services api-service database-service

# Detect anomalies
python scripts/error_detection_automation.py --detect-anomalies \
  --service api-service --output anomaly_report.json
```

**주요 기능**:
- 오류 패턴 일치(심각, 높음, 중간 심각도)를 통한 로그 검사
- 여러 서비스 간의 오류 상관 관계
- 통계분석을 이용한 이상 징후 탐지(평균 ± 2 표준편차)
- 상위 오류 패턴 식별
- 오류 계단식 감지
- 종합적인 오류 감지 보고서

**출력**: 스캔한 서비스, 상관된 사건, 감지된 이상 항목 및 권장 사항이 포함된 JSON 보고서입니다.

---

## 사용 예

### 사고 대응 워크플로

완전한 사고 관리 워크플로우:

```bash
# 1. Triage the incident
python scripts/incident_triage.py \
  --incident INC-001 \
  --description "API service experiencing 503 errors" \
  --impact service_outage \
  --urgency immediate \
  --affected-users 1000 \
  --service api-service \
  --output triage.json

# 2. Contain the issue
python scripts/incident_response.py \
  --incident INC-001 \
  --severity critical \
  --action-type containment \
  --action enable_circuit_breaker \
  --target upstream-service

# 3. Analyze root cause
python scripts/incident_analysis.py \
  --incident INC-001 \
  --start-time "2024-01-12T10:00:00Z" \
  --end-time "2024-01-12T11:00:00Z" \
  --affected-users 1000 \
  --downtime 60 \
  --service api-service \
  --output analysis.json

# 4. Notify teams
python scripts/incident_response.py \
  --incident INC-001 \
  --severity critical \
  --action-type notify \
  --teams security-engineer devops-incident-responder backend-developer

# 5. Update status
python scripts/incident_response.py \
  --incident INC-001 \
  --severity critical \
  --action-type status \
  --status resolved \
  --details "Root cause fixed and service restored"
```

### 카오스 엔지니어링 작업 흐름

완전한 카오스 엔지니어링 워크플로:

```bash
# 1. Assess current resilience
python scripts/resilience_assessment.py \
  --target api-service \
  --component database \
  --output baseline_resilience.json

# 2. Design and run chaos experiment
python scripts/chaos_experiment.py \
  --experiment database-failure-resilience \
  --target database-service \
  --failure-type pod_kill \
  --blast-radius 5 \
  --output experiment.json

# 3. Analyze experiment results
# Review experiment.json for hypothesis validation
# Check lessons learned and recommendations

# 4. Re-assess resilience after improvements
python scripts/resilience_assessment.py \
  --target api-service \
  --output post_experiment_resilience.json

# 5. Compare scores
# baseline_resilience.json vs post_experiment_resilience.json
# Measure improvement in resilience score
```

### 오류 감지 작업 흐름

완전한 오류 감지 작업 흐름:

```bash
# 1. Scan logs across services
python scripts/error_detection_automation.py --scan \
  --services api-service database-service auth-service cache-service \
  --output error_scan.json

# 2. Correlate errors
python scripts/error_detection_automation.py --correlate \
  --services api-service database-service \
  --output correlation.json

# 3. Detect anomalies
python scripts/error_detection_automation.py --detect-anomalies \
  --service api-service \
  --output anomalies.json

# 4. Review findings
# Check error_scan.json for top error patterns
# Check correlation.json for cascades
# Check anomalies.json for unexpected behavior
```

## 모범 사례

### 일반 스크립트 사용법

1. **항상 먼저 테스트**: 프로덕션 사용 전에 샘플 데이터로 스크립트를 실행합니다.
2. **버전 관리 사용**: 스크립트 및 구성에 대한 변경 사항 추적
3. **출력 확인**: 생성된 파일에 예상 데이터가 포함되어 있는지 확인
4. **오류 처리**: 오류 메시지 검토 및 문제 해결 가이드 확인
5. **문서 사용자 정의**: 수정 사항을 기록으로 유지하세요.

### 사고 대응

- **신속한 대응**: 감지 즉시 분류 스크립트 사용
- **Contain First**: 전체 분석 전에 격리 조치를 실행합니다.
- **증거 보존**: 증거를 수집하기 전에 시스템을 수정하지 마십시오.
- **정기적으로 소통**: 사건 전반에 걸쳐 이해관계자를 업데이트합니다.
- **모든 것을 문서화**: 모든 조치와 결정의 일정을 유지합니다.
- **지속적으로 학습**: 모든 사건을 기반으로 런북 업데이트

### 카오스 엔지니어링

- **가설 우선**: 항상 명확하고 테스트 가능한 가설로 시작합니다.
- **작게 시작**: 낮은 폭발 반경으로 시작합니다(생산 시 1~5%).
- **지속적으로 모니터링**: 실험 중에 측정항목을 실시간으로 관찰하세요.
- **롤백 준비됨**: 시작하기 전에 자동 롤백 테스트를 거칩니다.
- **모두로부터 배우기**: 실패한 실험이라도 통찰력을 제공합니다.
- **점진적으로 반복**: 자신감이 쌓일 때만 복잡성이 증가합니다.

### 오류 감지

- **서비스 간 상관관계**: 단독으로 분석하지 마세요.
- **기준 설정**: 이상 탐지를 위해 기록 데이터를 사용합니다.
- **임계값 조정**: 오탐지를 줄이기 위해 환경에 맞게 조정
- **패턴 추적**: 일반적인 오류 패턴에 대한 지식 기반 구축
- **경고 자동화**: PagerDuty, Slack 등과 통합됩니다.
- **정기 검토**: 주간/월간 오류 동향 분석

### 빌드 엔지니어링

- **속도 최적화**: 캐싱 및 병렬 처리 활성화
- **번들 크기 분석**: 최적화 기회를 정기적으로 확인
- **로컬에서 먼저 테스트**: CI/CD 전에 빌드 구성 확인
- **빌드 시간 모니터링**: 빌드 시간 회귀에 대한 경고
- **업데이트 유지**: 빌드 도구를 정기적으로 업데이트합니다.

## 확장 및 유지 관리

### 새 스크립트 추가

1. **기존 패턴 따르기**: 유사한 구조와 명명 규칙을 사용합니다.
2. **도움말 문서 포함**: 추가`--help`지원하다
3. **오류 처리**: 명확한 오류 메시지와 함께 try/제외 블록을 포함합니다.
4. **로깅**: 적절한 수준의 로깅 모듈을 사용합니다.
5. **유형 힌트**: 코드 명확성을 높이기 위해 유형 힌트를 추가합니다.
6. **Docstrings**: 문서 기능 목적 및 매개변수

### 스크립트 템플릿

```python
#!/usr/bin/env python3
"""
[Script Description]

Automates [what this script does].

Usage:
    python scripts/script_name.py [OPTIONS]
    python scripts/script_name.py --help
"""

import argparse
import json
import logging
from typing import Dict, List

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='[Script description]')
    parser.add_argument('--option', help='Option description')
    parser.add_argument('--output', help='Output file path')
    
    args = parser.parse_args()
    
    # Script logic here
    logger.info("Executing script...")
    
    # Generate output
    result = {"status": "success", "data": "output"}
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)
        logger.info(f"Output saved to {args.output}")
    else:
        print(json.dumps(result, indent=2))
    
    logger.info("Script completed")

if __name__ == '__main__':
    main()
```

### 기존 스크립트 업데이트

1. **현재 구현 검토**: 기존 논리 및 패턴 이해
2. **변경 사항 테스트**: 스크립트를 수정하고 철저하게 테스트합니다.
3. **문서 업데이트**: SKILL.md 및 참조를 동기화 상태로 유지
4. **버전 관리**: 명확한 메시지로 변경 사항 커밋
5. **팀에 알림**: 중요한 변경 사항을 팀과 공유

### 참조 문서 유지

- **문제 해결 업데이트**: 발견된 새로운 문제와 솔루션을 추가합니다.
- **모범 사례 업데이트**: 사용을 통해 얻은 교훈을 통합합니다.
- **동기화 유지**: SKILL.md 섹션이 실제 스크립트와 일치하는지 확인하세요.
- **정기 검토**: 모든 문서를 월별로 검토합니다.

## 문제 해결

### 일반적인 문제

#### 스크립트 실행 실패

**증상**:`No such file or directory`, `Permission denied`또는 가져오기 오류

**해결책**:
- 올바른 스킬 디렉토리에 있는지 확인하세요.
- 스크립트 디렉터리가 존재하는지 확인하세요.
- Python 3.7 이상이 설치되어 있는지 확인하십시오.`python --version`- 스크립트를 실행 가능하게 만듭니다.`chmod +x scripts/*.py`- 출력 디렉터리에 대한 쓰기 권한을 확인하세요.

#### 출력 파일이 생성되지 않음

**증상**: 출력 파일이 생성되지 않거나 파일이 비어 있습니다.

**해결책**:
- 출력 디렉터리가 존재하고 쓰기 가능한지 확인하세요.
- 스크립트 출력에서 오류 메시지를 확인하세요.
- 출력에 절대 경로를 사용합니다.`--output /full/path/to/output.json`- 사용 가능한 디스크 공간 확인
- 가능한 경우 자세한 플래그를 사용하여 실행합니다.

#### JSON 구문 분석 오류

**증상**:`JSONDecodeError`출력 파일을 읽을 때

**해결책**:
- 스크립트가 성공적으로 완료되었는지 확인
- 실행 중 쓰기 오류 확인
- 온라인 유효성 검사기로 JSON 출력 유효성 검사
- 출력시 특수문자 확인

### 도움 받기

#### 스크립트 도움말

```bash
# Get help for any script
python scripts/script_name.py --help
```

#### 문서

- SKILL.md: 각 스킬에 대한 개요 및 기능
- reference/troubleshooting.md: 자세한 문제 해결 가이드
- reference/best_practices.md: 모범 사례 및 권장 사항

#### 디버그 모드

```bash
# Enable debug logging
export DEBUG=true

# Or modify script
logging.basicConfig(level=logging.DEBUG)
```

## 기여

새로운 스크립트나 개선 사항에 기여할 때:

1. 기존 코드 패턴과 스타일을 따릅니다.
2. 포괄적인 문서와 예시를 포함하세요.
3. 여러 시나리오에 걸쳐 철저하게 테스트
4. 관련 SKILL.md 파일 업데이트
5. 필요에 따라 문제 해결 및 모범 사례에 추가
6. 변경사항에 대한 명확한 설명과 함께 제출

## 라이센스

이러한 자동화 스크립트는 Claude Skills Conversion 프로젝트의 일부입니다. 자세한 내용은 메인 프로젝트 LICENSE 파일을 참고하세요.

## 지원하다

문제, 질문 또는 기여의 경우:
- 사용 지침은 이 README를 검토하세요.
- 스킬별 문제 해결.md 파일 확인
- 기능 설명은 SKILL.md 파일을 참조하세요.
- 권장 접근 방식은 best_practices.md를 검토하세요.