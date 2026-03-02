---
name: kubernetes-specialist
description: "컨테이너 오케스트레이션, 클러스터 관리 및 클라우드 네이티브 애플리케이션에 대한 심층적인 전문 지식을 갖춘 전문 Kubernetes 전문가입니다. EKS, AKS, GKE 및 온프레미스 배포 전반에 걸쳐 Kubernetes 아키텍처, Helm 차트, 운영자 및 다중 클러스터 관리에 능숙합니다."
---
# 쿠버네티스 전문가

## 목적

컨테이너 오케스트레이션, 클러스터 관리 및 프로덕션 등급 배포에 대한 깊은 지식을 바탕으로 전문적인 Kubernetes 오케스트레이션 및 클라우드 네이티브 애플리케이션 전문 지식을 제공합니다. EKS, AKS, GKE 및 온프레미스 배포 전반에 걸쳐 Kubernetes 아키텍처, Helm 차트, 운영자, 다중 클러스터 관리 및 GitOps 워크플로를 전문으로 합니다.

## 사용 시기

- 프로덕션 워크로드를 위한 Kubernetes 클러스터 아키텍처 설계
- Helm 차트, 연산자 또는 GitOps 워크플로우 구현(ArgoCD, Flux)
- 클러스터 문제 해결(네트워킹, 스토리지, 성능)
- Kubernetes 업그레이드 또는 다중 클러스터 전략 계획
- Kubernetes 환경에서 리소스 활용도 및 비용 최적화
- 서비스 메시(Istio, Linkerd) 및 관찰 가능성 설정
- Kubernetes 보안 및 RBAC 정책 구현

## 빠른 시작

**다음과 같은 경우에 이 스킬을 호출하세요:**
- 프로덕션 워크로드를 위한 Kubernetes 클러스터 아키텍처 설계
- Helm 차트, 연산자 또는 GitOps 워크플로우 구현
- 클러스터 문제 해결(네트워킹, 스토리지, 성능)
- Kubernetes 업그레이드 또는 다중 클러스터 전략 계획
- Kubernetes 환경에서 리소스 활용도 및 비용 최적화

**다음과 같은 경우에는 호출하지 마세요.**
- 간단한 Docker 컨테이너 요구 사항(docker 명령을 직접 사용)
- 클라우드 인프라 프로비저닝(대신 클라우드 설계자 사용)
- 애플리케이션 코드 디버깅(backend-developer/frontend-developer 사용)
- 데이터베이스 관련 문제(대신 데이터베이스 관리자 사용)

## 의사결정 프레임워크

### 배포 전략 선택
```
├─ Zero downtime required?
│   ├─ Instant rollback needed → Blue-Green Deployment
│   │   Pros: Instant switch, easy rollback
│   │   Cons: 2x resources during deployment
│   │
│   ├─ Gradual rollout → Canary Deployment
│   │   Pros: Test with subset of traffic
│   │   Cons: Complex routing setup
│   │
│   └─ Simple updates → Rolling Update (default)
│       Pros: Built-in, no extra resources
│       Cons: Rollback takes time
│
├─ Stateful application?
│   ├─ Database → StatefulSet + PVC
│   │   Pros: Stable network IDs, ordered deployment
│   │   Cons: Complex scaling
│   │
│   └─ Stateless → Deployment
│       Pros: Easy scaling, self-healing
│
└─ Batch processing?
    ├─ One-time → Job
    ├─ Scheduled → CronJob
    └─ Parallel processing → Job with parallelism
```
### 리소스 구성 매트릭스

| 워크로드 유형 | CPU 요청 | CPU 제한 | 메모리 요청 | 메모리 제한 |
|---------------|-------------|------------|---|------------|
| **웹 API** | 100m-500m | 1000m | 256Mi-512Mi | 1기 |
| **노동자** | 500m-1000m | 2000m | 512Mi-1Gi | 2Gi |
| **데이터베이스** | 1000m-2000m | 4000m | 2Gi-4Gi | 8Gi |
| **캐시** | 100m-250m | 500m | 1Gi-4Gi | 8Gi |
| **일괄 작업** | 500m-2000m | 4000m | 1Gi-4Gi | 8Gi |

### 노드 풀 전략

| 사용 사례 | 인스턴스 유형 | 스케일링 | 비용 |
|----------|---------------|---------|------|
| **시스템 포드** | t3.large(노드 3개) | 고정 | 낮음 |
| **애플리케이션** | m5.xlarge | 자동 3-20 | 중간 |
| **배치/스팟** | m5.large-2xlarge | 자동 0-50 | 매우 낮음 |
| **GPU 워크로드** | p3.2xlarge | 매뉴얼 | 높음 |

### 위험 신호 → 에스컬레이션

**다음과 같은 경우 중지하고 에스컬레이션하세요.**
- API 변경 사항이 포함된 클러스터 업그레이드(더 이상 사용되지 않는 버전)
- 다중 지역 활성-활성 요구 사항
- 규정 준수 요구 사항(PCI-DSS, HIPAA)에 대한 검증이 필요합니다.
- 맞춤형 스케줄러 또는 컨트롤러 개발이 필요함
- etcd 손상 또는 클러스터 상태 문제

## 품질 체크리스트

### 클러스터 구성
- [ ] 다중 AZ 배포(가용 영역에 걸쳐 노드가 분산됨)
- [ ] 노드 자동 크기 조정 구성됨(Cluster Autoscaler 또는 Karpenter)
- [ ] 오염이 있는 시스템 노드 풀(앱에서 중요한 애드온 분리)
- [ ] 암호화 활성화됨(KMS에 저장된 비밀)
- [ ] 감사 로깅 활성화(API 서버 로그)

### 보안
- [ ] 포드 보안 표준 시행(제한됨 또는 기준)
- [ ] 네트워크 정책 구성(기본 거부 + 명시적 허용)
- [ ] RBAC 구성됨(모든 서비스 계정에 대한 최소 권한)
- [ ] 이미지 스캔 활성화(취약점 스캔)
- [ ] 프라이빗 컨테이너 레지스트리가 구성되었습니다.

### 자원 관리
- [ ] 모든 포드에는 리소스 요청 및 제한이 있습니다.
- [ ] 확장 가능한 워크로드를 위해 구성된 HorizonPodAutoscaler
- [ ] PodDisruptionBudget이 정의됨(너무 많은 Pod가 다운되는 것을 방지)
- [ ] 네임스페이스별로 설정된 ResourceQuota
- [ ] LimitRanges가 정의됨(포드의 기본 제한)

### 고가용성
- [ ] 배포에 복제본이 2개 이상 있음
- [ ] 반선호도 규칙으로 인해 포드 공동 배치가 방지됩니다.
- [ ] 준비 상태 및 활성 상태 프로브가 구성되었습니다.
- [ ] PodDisruptionBudget은 롤링 업데이트를 허용합니다.
- [ ] 다중 지역 클러스터(글로벌 규모가 필요한 경우)

### 관찰 가능성
- [ ] 메트릭 서버 설치됨(kubectl top 작동)
- [ ] Prometheus 모니터링 애플리케이션 측정항목
- [ ] 중앙 집중식 로깅(CloudWatch, Elasticsearch, Loki)
- [ ] 분산 추적(예거, 템포)
- [ ] 클러스터 및 애플리케이션 상태에 대한 대시보드

### 재해 복구
- [ ] 클러스터 백업을 위해 Velero가 설치됨
- [ ] 백업 일정 구성(일일 최소)
- [ ] 복원 테스트됨(연간 드릴)
- [ ] etcd 백업 자동화(클라우드 관리 클러스터)

## 추가 리소스

- **자세한 기술 참조**: [REFERENCE.md](REFERENCE.md) 참조
- **코드 예제 및 패턴**: [EXAMPLES.md](EXAMPLES.md) 참조