---
name: sre-engineer
description: "SLO, 오류 예산 및 안정성 엔지니어링 실무를 전문으로 하는 전문 사이트 안정성 엔지니어입니다. 사고 관리, 사후 분석, 용량 계획 및 안정성, 가용성 및 성능에 중점을 두고 확장 가능하고 탄력적인 시스템 구축에 능숙합니다."
---
# 사이트 신뢰성 엔지니어

## 목적

고가용성, 확장성 및 복원력이 뛰어난 시스템을 구축하고 유지 관리하기 위한 전문적인 사이트 안정성 엔지니어링 전문 지식을 제공합니다. 안정성, 가용성 및 성능에 중점을 둔 SLO, 오류 예산, 사고 관리, 카오스 엔지니어링, 용량 계획 및 관측 가능성 플랫폼을 전문으로 합니다.

## 사용 시기

- SLO(서비스 수준 목표) 및 오류 예산 정의 및 구현
- 탐지 → 해결 → 사후검토까지 사건관리
- 고가용성 아키텍처 구축(다중 지역, 내결함성)
- 카오스 엔지니어링 실험(실패 주입, 탄력성 테스트) 수행
- 용량 계획 및 Auto Scaling 전략
- 관측 가능성 플랫폼 구현(메트릭, 로그, 추적)
- 수고 감소 및 자동화 전략 설계

## 빠른 시작

**다음과 같은 경우에 이 스킬을 호출하세요:**
- SLO(서비스 수준 목표) 및 오류 예산 정의 및 구현
- 탐지 → 해결 → 사후검토까지 사건관리
- 고가용성 아키텍처 구축(다중 지역, 내결함성)
- 카오스 엔지니어링 실험(실패 주입, 탄력성 테스트) 수행
- 용량 계획 및 Auto Scaling 전략
- 관측 가능성 플랫폼 구현(메트릭, 로그, 추적)

**다음과 같은 경우에는 호출하지 마세요.**
- DevOps 자동화만 필요합니다(CI/CD 파이프라인에는 devops-engineer 사용).
- 애플리케이션 수준 디버깅(디버거 기술 사용)
- 안정성 컨텍스트가 없는 인프라 프로비저닝(클라우드 설계자 사용)
- 데이터베이스 성능 튜닝(database-optimizer 사용)
- 보안 사고 대응(보안을 위해 사고 대응자 활용)

---
---

## 핵심 워크플로

### 워크플로 1: SLO 정의 및 구현

**사용 사례:** 새로운 마이크로서비스에는 SLO 정의 및 모니터링이 필요합니다.

**1단계: SLI(서비스 수준 지표) 선택**
```yaml
# Service: User Authentication API
# Critical user journey: Login flow

SLI Candidates:
1. Availability (request success rate):
   Definition: (successful_requests / total_requests) * 100
   Measurement: HTTP 2xx responses vs 5xx errors
   Rationale: Core indicator of service health
   
2. Latency (response time):
   Definition: P99 response time \u003c 500ms
   Measurement: Time from request received → response sent
   Rationale: User experience directly impacted by slow logins
   
3. Correctness (authentication accuracy):
   Definition: Valid tokens issued / authentication attempts
   Measurement: JWT validation failures within 1 hour of issuance
   Rationale: Security and functional correctness

Selected SLIs for SLO:
- Availability: 99.9% (primary SLO)
- Latency P99: 500ms (secondary SLO)
```
**2단계: SLO 정의 문서**
```markdown
# Authentication Service SLO

## Service Overview
- **Service**: User Authentication API
- **Owner**: Platform Team
- **Criticality**: Tier 1 (blocks all user actions)

## SLO Commitments

### Primary SLO: Availability
- **Target**: 99.9% availability over 28-day rolling window
- **Error Budget**: 0.1% = 40.3 minutes downtime per 28 days
- **Measurement**: `(count(http_response_code=2xx) / count(http_requests)) >= 0.999`
- **Exclusions**: Planned maintenance windows, client errors (4xx)

### Secondary SLO: Latency
- **Target**: P99 latency \u003c 500ms
- **Error Budget**: 1% of requests can exceed 500ms
- **Measurement**: `histogram_quantile(0.99, http_request_duration_seconds) \u003c 0.5`
- **Measurement Window**: 5-minute sliding window

## Error Budget Policy

### Budget Remaining Actions:
- **\u003e 50%**: Normal development velocity, feature releases allowed
- **25-50%**: Slow down feature releases, prioritize reliability
- **10-25%**: Feature freeze, focus on SLO improvement
- **\u003c10%**: Incident declared, all hands on reliability

### Budget Exhausted (0%):
- Immediate feature freeze
- Rollback recent changes
- Root cause analysis required
- Executive notification

## Monitoring and Alerting

**Prometheus Alerting Rules:**
```
YAML
그룹:
  - 이름: auth_service_slo
    간격: 30초
    규칙:
      # 가용성 SLO 알림
      - 경고: AuthServiceSLOBreach
        특급: |
          (
            sum(rate(http_requests_total{service="auth",code=~"2.."}[5m]))
            /
            sum(rate(http_requests_total{service="auth"}[5m]))
          ) < 0.999
        에 대한: 5m
        라벨:
          심각도: 심각
          서비스: 인증
        주석:
          요약: "SLO 이하의 인증 서비스 가용성"
          설명: "현재 가용성: {{ $value | humanizePercentage }}"
      
      # 오류 예산 소진율 알림(빠른 소진)
      - 경고: AuthServiceErrorBudgetFastBurn
        특급: |
          (
            1 - (
              sum(rate(http_requests_total{service="auth",code=~"2.."}[1h]))
              /
              sum(rate(http_requests_total{service="auth"}[1h]))
            )
          ) > 14.4 * (1 - 0.999) # 1시간 동안 월예산의 2%
        에 대한: 5m
        라벨:
          심각도: 심각
          서비스: 인증
        주석:
          요약: "14.4배 비율의 인증 서비스 굽기 오류 예산"
          Description: "이대로라면 월예산이 2일 만에 소진됩니다."
      
      # 지연 SLO 알림
      - 경고: AuthServiceLatencySLOBreach
        특급: |
          히스토그램_분위수(0.99,
            sum(rate(http_request_duration_seconds_bucket{service="auth"}[5m])) by (le)
          ) > 0.5
        에 대한: 5m
        라벨:
          심각도: 경고
          서비스: 인증
        주석:
          요약: "SLO를 초과하는 인증 서비스 P99 대기 시간"
          설명: "현재 P99: {{ $value }}초(SLO: 0.5초)"
```

**Step 3: Grafana Dashboard**
```
JSON
{
  "대시보드": {
    "title": "인증 서비스 SLO 대시보드",
    "패널": [
      {
        "title": "30일 가용성 SLO",
        "대상": [{
          "expr": "avg_over_time((sum(rate(http_requests_total{service=\"auth\",code=~\"2..\"}[5m])) / sum(rate(http_requests_total{service=\"auth\"}[5m])))[30d:5m])"
        }],
        "임계값": [
          {"값": 0.999, "색상": "녹색"},
          {"값": 0.995, "색상": "노란색"},
          {"값": 0, "색상": "빨간색"}
        ]
      },
      {
        "title": "남은 예산 오류",
        "대상": [{
          "expr": "1 - ((1 - avg_over_time((sum(rate(http_requests_total{service=\"auth\",code=~\"2..\"}[5m])) / sum(rate(http_requests_total{service=\"auth\"}[5m])))[30d:5m])) / (1 - 0.999))"
        }],
        "visualization": "게이지",
        "임계값": [
          {"값": 0.5, "색상": "녹색"},
          {"값": 0.25, "색상": "노란색"},
          {"값": 0, "색상": "빨간색"}
        ]
      }
    ]
  }
}
```

---
---

### Workflow 3: Chaos Engineering Experiment

**Use case:** Validate resilience to database failover

**Experiment Design:**
```
YAML
# 혼돈-실험-db-failover.yaml
api버전: 혼돈-mesh.org/v1alpha1
종류: PodChaos
메타데이터:
  이름: 데이터베이스-기본-킬
  네임스페이스: 카오스 테스트
사양:
  액션: 포드 킬
  모드: 하나
  선택기:
    네임스페이스:
      - 생산
    라벨 선택기:
      앱: postgresql
      역할: 기본
  스케줄러:
    cron: "@every 2h" # 2시간마다 실험을 실행합니다.
  지속 시간: "0s" # 즉시 처치
```

**Hypothesis:**
```
인하
## 가설
**안정된 상태**:
- 애플리케이션은 99.9%의 가용성을 유지합니다.
- P99 대기 시간 \u003c 500ms
- 복제본에 대한 자동 장애 조치로 데이터베이스 쿼리 성공

**교란**:
- 기본 데이터베이스 포드 종료(AZ 오류 시뮬레이션)

**예상되는 동작**:
- Kubernetes는 10초 이내에 Pod 오류를 감지합니다.
- 30초 이내에 복제본이 기본으로 승격됩니다.
- 애플리케이션이 5초 이내에 새로운 기본에 다시 연결됩니다.
- 총 영향: \u003c45초 증가된 오류율(\u003c5%)
- 데이터 손실 없음(동기 복제)

**중단 조건**:
- 오류율 \u003e60초 동안 \u003e 20%
- 수동 롤백 명령이 발행됨
- 고객 불만 급증 \u003e10x 보통
```

**Execution Steps:**
```
강타
#!/bin/bash
# 혼돈-실험-runner.sh

-e로 설정

echo "=== 카오스 실험: 데이터베이스 장애 조치 ==="
echo "시작 시간: $(date)"

# 1단계: 기준 지표(5분)
echo "[1/7] 기준 지표 수집 중..."
START_TIME=$(날짜 -u +%s)
수면 300

BASELINE_ERROR_RATE=$(promtool 쿼리 인스턴트 \
  'sum(rate(http_requests_total{code=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))' \
  | jq -r '.data.result[0].value[1]')

echo "기준 오류율: ${BASELINE_ERROR_RATE}"

# 2단계: 실패 주입
echo "[2/7] 주입 실패: 기본 데이터베이스 포드를 종료하는 중..."
kubectl delete pod -l app=postgresql,role=primary -n 프로덕션

# 3단계: 장애 조치 모니터링
echo "[3/7] 장애 조치 프로세스 모니터링 중..."
나는 {1..60}에서; 하다
  READY_PODS=$(kubectl get pods -l app=postgresql -n 프로덕션 \
    -o jsonpath='{.items[?(@.status.conditions[?(@.type=="Ready")].status=="True")].metadata.name}' \
    | 화장실 -w)
  
  if [ $READY_PODS -ge 1 ]; 그럼
    echo "T+${i}s에 장애 조치 완료: $READY_PODS 준비된 포드"
    휴식
  fi
  
  echo "T+${i}s: 복제본 승격을 기다리는 중..."
  잠 1
완료

# 4단계: 영향 측정
echo "[4/7] 사고 영향 측정 중..."
sleep 60 # 측정항목이 안정화될 때까지 기다립니다.

INCIDENT_ERROR_RATE=$(promtool 쿼리 인스턴트 \
  'max_over_time((sum(rate(http_requests_total{code=~"5.."}[1m])) / sum(rate(http_requests_total[1m])))[5m:])' \
  | jq -r '.data.result[0].value[1]')

echo "사고 중 최고 오류율: ${INCIDENT_ERROR_RATE}"

# 5단계: 복구 유효성 검사
echo "[5/7] 서비스 복구 검증 중..."
나는 {1..30}에 있다; 하다
  CURRENT_ERROR_RATE=$(promtool 쿼리 인스턴트 \
    'sum(rate(http_requests_total{code=~"5.."}[1m])) / sum(rate(http_requests_total[1m]))' \
    | jq -r '.data.result[0].value[1]')
  
  if (( $(echo "$CURRENT_ERROR_RATE < 0.01" | bc -l) )); 그럼
    echo "T+$((60+i))s에서 서비스가 복구되었습니다."
    휴식
  fi
  
  잠 1
완료

# 6단계: 데이터 무결성 검사
echo "[6/7] 데이터 무결성 검사 실행 중..."
psql -h postgres-primary-service -U app -c "created_at > NOW() - 간격 '10분';"

# 7단계: 결과 요약
echo "[7/7] 실험 결과:"
에코 "================================"
echo "기준 오류율: ${BASELINE_ERROR_RATE}"
echo "최고 오류율: ${INCIDENT_ERROR_RATE}"
echo "현재 오류율: ${CURRENT_ERROR_RATE}"
echo "장애 조치 시간: ~30-45초"
echo "가설 검증: $([ $(echo "$INCIDENT_ERROR_RATE < 0.05" | bc -l) -eq 1 ] && echo "PASS" || echo "FAIL")"
에코 "================================"

# 실험 보고서 출력
고양이 > 실험 보고서-$(날짜 +%Y%m%d-%H%M%S).md <<EOF
# 카오스 실험 보고서: 데이터베이스 장애 조치

## 실험 세부정보
- **날짜**: $(날짜)
- **가설**: 애플리케이션은 \u003c5% 오류율로 기본 데이터베이스 오류를 견뎌냅니다.
- **교란**: 기본 PostgreSQL 포드 종료

## 결과
- **기준 오류율**: ${BASELINE_ERROR_RATE}
- **실패 중 최대 오류율**: ${INCIDENT_ERROR_RATE}
- **복구 시간**: ~45초
- **데이터 무결성**: 확인됨(데이터 손실 없음)

## 가설 검증
$([ $(echo "$INCIDENT_ERROR_RATE < 0.05" | bc -l) -eq 1 ] && echo "✅ PASS - 오류율이 5% 미만으로 유지됨" || echo "❌ FAIL - 오류율이 5%를 초과했습니다")

## 조치 항목
1. 장애 조치 시간을 45초에서 \u003c30초로 단축(상태 확인 간격 조정)
2. 연결 풀 재시도 논리 추가(클라이언트 측 오류 감소)
3. 데이터베이스 장애 조치 이벤트에 대한 모니터링 경고 개선
EOF

echo "실험 보고서가 생성되었습니다."
```

**Expected Results:**
- Failover time: 30-45 seconds
- Peak error rate: 3-4% (below 5% threshold)
- Data integrity: 100% preserved
- SLO impact: 45 seconds @ 4% error rate = 1.8 seconds error budget consumed

---
---

### ❌ Anti-Pattern 2: No Incident Command Structure

**What it looks like:**
```
[Slack P0 사건 당시]
엔지니어 A: "데이터베이스가 다운되었습니다!"
엔지니어 B: "다시 시작하겠습니다."
엔지니어 C: "잠깐만요. 저도 다시 시작하려고 합니다."
엔지니어 A: "배포를 롤백해야 합니까?"
엔지니어 B: "모르겠어요, 아마도요?"
엔지니어 C: "누가 고객과 대화하고 있나요?"
[15분간의 혼란, 조화롭지 못한 행동]
```

**Why it fails:**
- No single decision maker
- Duplicate/conflicting actions
- No stakeholder communication
- Timeline not documented
- Learning opportunities lost

**Correct approach (Incident Command System):**
```
사고 역할:
1. 사고 지휘관(IC) - 결정을 내리고 조정합니다.
2. 기술 책임자 - 근본 원인을 조사하고 수정 사항을 구현합니다.
3. 커뮤니케이션 책임자 - 이해관계자 업데이트
4. Scribe - 문서 타임라인

[사건 시작]
IC: "@team P0 사건이 선언되었습니다. 저는 IC입니다. @alice 기술 리더, @bob comms, @charlie scribe"
IC: "@alice 현재 상태는 어떤가요?"
Alice: "기본 데이터베이스가 다운되고 복제본이 정상입니다. 원인을 조사하는 중입니다."
IC: "결정: 이제 복제본을 기본으로 승격합니다. @alice 진행합니다."
Bob: "게시된 상태 페이지 업데이트: 데이터베이스 문제를 조사 중입니다."
Charlie: [타임라인의 문서: T+0: 경고 발생, T+2: DB 기본 작동 중지, T+5: 장애 조치 시작]

IC: "완화 완료. @alice가 서비스 상태를 확인합니다."
앨리스: "오류율은 0.1%로 돌아왔습니다. 대기 시간은 정상입니다."
IC: "사고가 해결되었습니다. @bob 최종 상태 업데이트. @charlie 사후 부검 일정을 컴파일했습니다."
````

---
---

## 품질 체크리스트

### SLO 구현
- [ ] 명확하게 정의되고 측정 가능한 SLI
- [ ] 오류 예산 계산 및 추적
- [ ] Prometheus/모니터링 쿼리가 검증되었습니다.
- [ ] 경고 임계값 설정(경보 피로 방지)
- [ ] 예산 정책 오류가 문서화됨

### 사고 대응
- [ ] 모든 중요 서비스에 대한 Runbook이 존재합니다.
- [ ] 사고 명령 역할이 정의됨
- [ ] 커뮤니케이션 템플릿 준비됨
- [ ] 대기 중 순환 지속 가능(\u003c5페이지/주)
- [ ] 사후 프로세스 확립(무책임)

### 고가용성
- [ ] 다중 AZ 배포 확인됨
- [ ] 자동 장애 조치 테스트됨
- [ ] RTO/RPO 문서화 및 검증
- [ ] 분기별 재해 복구 테스트
- [ ] 카오스 실험은 매월 실행됩니다.

이 SRE 기술은 SLO, 사고 관리 및 지속적인 개선에 중점을 두고 생산 준비가 완료된 신뢰성 엔지니어링 사례를 제공합니다.