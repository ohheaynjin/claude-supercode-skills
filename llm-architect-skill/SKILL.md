---
name: llm-architect
description: 사용자에게 LLM 시스템 아키텍처, 모델 배포, 최적화 전략 및 프로덕션 서비스 인프라가 필요할 때 사용합니다. 성능, 비용 효율성 및 안전성에 중점을 두고 확장 가능한 대규모 언어 모델 애플리케이션을 설계합니다.
---
# LLM 건축가

## 목적

대규모로 LLM 애플리케이션을 설계, 배포 및 최적화하기 위한 전문적인 대규모 언어 모델 시스템 아키텍처를 제공합니다. 모델 선택, RAG(Retrieval Augmented Generation) 파이프라인, 전략 미세 조정, 서비스 인프라, 비용 최적화 및 생산 LLM 시스템을 위한 안전 가드레일을 전문으로 합니다.

## 사용 시기

- 요구사항부터 생산까지 엔드투엔드 LLM 시스템 설계
- 특정 사용 사례에 맞는 모델 및 서비스 인프라 선택
- RAG(Retrieval Augmented Generation) 파이프라인 구현
- 품질 임계값을 유지하면서 LLM 비용 최적화
- 안전 가드레일 및 규정 준수 메커니즘 구축
- 미세 조정 계획 vs RAG vs 신속한 엔지니어링 전략 계획
- 처리량이 많은 애플리케이션을 위한 LLM 추론 확장

## 빠른 시작

**다음과 같은 경우에 이 스킬을 호출하세요:**
- 요구사항부터 생산까지 엔드투엔드 LLM 시스템 설계
- 특정 사용 사례에 맞는 모델 및 서비스 인프라 선택
- RAG(Retrieval Augmented Generation) 파이프라인 구현
- 품질 임계값을 유지하면서 LLM 비용 최적화
- 안전 가드레일 및 규정 준수 메커니즘 구축

**다음과 같은 경우에는 호출하지 마세요.**
- 간단한 API 통합이 존재합니다(대신 백엔드 개발자 사용).
- 아키텍처 결정 없이 신속한 엔지니어링만 필요
- 처음부터 기초 모델 교육(거의 항상 잘못된 접근 방식)
- 언어 모델과 관련되지 않은 일반 ML 작업(ml-engine 사용)

## 의사결정 프레임워크

### 모델 선택 퀵 가이드

| 요구사항 | 권장 접근 방식 |
|-------------|---------|
| 지연 시간 <100ms | 소형 미세 조정 모델(7B 양자화) |
| 지연 시간 2초 미만, 예산 무제한 | 클로드 3 Opus / GPT-4 |
| 지연 시간 <2초, 도메인별 | 클로드 3번 소네트 미세 조정 |
| 지연 시간은 2초 미만, 비용에 민감함 | 클로드 3 하이쿠 |
| 일괄/비동기 허용 | 배치 API, 가장 저렴한 계층 |

### RAG 대 미세 조정 결정 트리
```
Need to customize LLM behavior?
│
├─ Need domain-specific knowledge?
│  ├─ Knowledge changes frequently?
│  │  └─ RAG (Retrieval Augmented Generation)
│  └─ Knowledge is static?
│     └─ Fine-tuning OR RAG (test both)
│
├─ Need specific output format/style?
│  ├─ Can describe in prompt?
│  │  └─ Prompt engineering (try first)
│  └─ Format too complex for prompt?
│     └─ Fine-tuning
│
└─ Need latency <100ms?
   └─ Fine-tuned small model (7B-13B)
```
### 아키텍처 패턴
```
[Client] → [API Gateway + Rate Limiting]
              ↓
         [Request Router]
          (Route by intent/complexity)
              ↓
    ┌────────┴────────┐
    ↓                 ↓
[Fast Model]    [Powerful Model]
(Haiku/Small)   (Sonnet/Large)
    ↓                 ↓
[Cache Layer] ← [Response Aggregator]
    ↓
[Logging & Monitoring]
    ↓
[Response to Client]
```
## 핵심 작업 흐름: LLM 시스템 설계

### 1. 요구 사항 수집

다음 질문을 해보세요:
- **대기 시간**: P95 응답 시간 요구 사항은 무엇입니까?
- **규모**: 예상 요청/일 및 성장 궤적은 무엇입니까?
- **정확도**: 허용 가능한 최소 품질은 얼마입니까? (측정 가능한 측정항목)
- **비용**: 예산 제약이 있나요? ($/요청 또는 $/월)
- **데이터**: 평가를 위한 기존 데이터세트가 있나요? 민감도 수준?
- **규정 준수**: 규제 요건? (HIPAA, GDPR, SOC2 등)

### 2. 모델 선정
```python
def select_model(requirements):
    if requirements.latency_p95 < 100:  # milliseconds
        if requirements.task_complexity == "simple":
            return "llama2-7b-finetune"
        else:
            return "mistral-7b-quantized"
    
    elif requirements.latency_p95 < 2000:
        if requirements.budget == "unlimited":
            return "claude-3-opus"
        elif requirements.domain_specific:
            return "claude-3-sonnet-finetuned"
        else:
            return "claude-3-haiku"
    
    else:  # Batch/async acceptable
        if requirements.accuracy_critical:
            return "gpt-4-with-ensemble"
        else:
            return "batch-api-cheapest-tier"
```
### 3. 프로토타입 제작 및 평가
```bash
# Run benchmark on eval dataset
python scripts/evaluate_model.py \
  --model claude-3-sonnet \
  --dataset data/eval_1000_examples.jsonl \
  --metrics accuracy,latency,cost

# Expected output:
# Accuracy: 94.3%
# P95 Latency: 1,245ms
# Cost per 1K requests: $2.15
```
### 4. 반복 체크리스트

- [ ] 대기 시간 P95가 요구 사항을 충족합니까? 그렇지 않은 경우 → 서비스 최적화(양자화, 캐싱)
- [ ] 정확도가 임계값을 충족합니까? 그렇지 않은 경우 → 프롬프트 개선, 미세 조정 또는 모델 업그레이드
- [ ] 예산 범위 내에서 비용이 발생합니까? 그렇지 않은 경우 → 공격적인 캐싱, 더 작은 모델 라우팅, 일괄 처리
- [ ] 안전 가드레일이 테스트되었습니까? 그렇지 않은 경우 → 콘텐츠 필터 추가, PII 감지
- [ ] 대시보드를 실시간으로 모니터링합니까? 그렇지 않은 경우 → Prometheus + Grafana 설정
- [ ] Runbook이 문서화되었습니까? 그렇지 않은 경우 → 일반적인 오류 및 수정 사항을 문서화합니다.

## 비용 최적화 전략

| 전략 | 저축 | 사용 시기 |
|------------|---------|-------------|
| 시맨틱 캐싱 | 40-80% | 60%+ 유사한 검색어 |
| 다중 모델 라우팅 | 30-50% | 복합적인 복잡성 쿼리 |
| 신속한 압축 | 10-20% | 긴 컨텍스트 입력 |
| 일괄 처리 | 20-40% | 비동기 허용 워크로드 |
| 더 작은 모델 캐스케이드 | 40-60% | 간단한 쿼리 먼저 |

## 안전 체크리스트

- [ ] 적대적인 예시에 대해 테스트된 콘텐츠 필터링
- [ ] PII 감지 및 수정 검증됨
- [ ] 즉각적인 주입 방어가 확립되어 있습니다.
- [ ] 출력 유효성 검사 규칙이 구현되었습니다.
- [ ] 모든 요청에 대해 감사 로깅이 구성되었습니다.
- [ ] 규정 준수 요구 사항이 문서화되고 검증되었습니다.

## 위험 신호 - 에스컬레이션해야 하는 경우

| 관찰 | 액션 |
|-------------|---------|
| 프롬프트 반복 후 정확도 <80% | 미세 조정 고려 |
| 지연 시간 2배 요구 사항 | 인프라 검토 |
| 비용 >예산의 2배 | 적극적인 캐싱/라우팅 |
| 환각률 >5% | RAG 또는 더 강한 가드레일 추가 |
| 안전 우회 감지됨 | 즉각적인 보안 검토 |

## 빠른 참조: 실적 목표

| 미터법 | 대상 | 심각 |
|---------|---------|----------|
| P95 대기 시간 | <2x 요구 사항 | <3x 요구사항 |
| 정확도 | >90% | >80% |
| 캐시 적중률 | >60% | >40% |
| 오류율 | <1% | <5% |
| 비용/요청 1,000개 | 예산 내에서 | 예산 150% 미만 |

## 추가 리소스

- **자세한 기술 참조**: [REFERENCE.md](REFERENCE.md) 참조
  - RAG 구현 워크플로우
  - 의미론적 캐싱 패턴
  - 배포 구성
  
- **코드 예제 및 패턴**: [EXAMPLES.md](EXAMPLES.md) 참조
  - 안티 패턴(충분한 메시지가 표시될 때 미세 조정, 대체 없음)
  - LLM 시스템 품질 체크리스트
  - 탄력적인 LLM 통화 패턴