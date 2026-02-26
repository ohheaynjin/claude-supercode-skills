# 미세 조정 가이드

## 개요

미세 조정은 사전 훈련된 모델을 특정 작업이나 영역에 맞게 조정하여 특화된 데이터의 성능을 향상시킵니다.

## 방법

### 1. 전체 미세 조정

모든 모델 매개변수를 업데이트합니다.

**장점:**
- 최대 성능 향상
- 아키텍처 변경 없음
- 모든 모델에서 작동

**단점:**
- 높은 계산 비용
- 대용량 저장 요구 사항
- 치명적인 망각의 위험

**사용 사례:**
- 최대의 정확성이 요구되는 중요한 작업
- 충분한 컴퓨팅 리소스
- 도메인별 모델

### 2. LoRA(낮은 순위 적응)

훈련 가능한 순위 분해 행렬을 추가합니다.

**장점:**
- 100-1000배 더 빠른 훈련
- 작은 저장 공간(1-100MB)
- 성능저하 없음
- 어댑터 간 전환이 용이함

**단점:**
- Full Fine-tuning에 비해 약간 낮은 성능
- LoRA를 지원하는 코드베이스가 필요합니다.

**사용 사례:**
- 대부분의 프로덕션 사용 사례
- 다중 작업 어댑터
- 자원이 제한된 환경

**구성:**
```python
lora_config = LoraConfig(
    r=8,  # Rank (4-16 typical)
    lora_alpha=32,  # Scaling factor
    target_modules=["q_proj", "v_proj"],  # Target layers
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)
```
### 3. 접두사 튜닝

연속 프롬프트 임베딩을 학습합니다.

**장점:**
- 모델을 통한 그라데이션 없음
- 매우 효율적

**단점:**
- 구현이 더 복잡함
- LoRA에 비해 성능이 낮음

### 4. P-Tuning(즉시튜닝)

부드러운 프롬프트를 배웁니다.

**장점:**
- 간단한 구현
- 매개변수 효율성

**단점:**
- 프롬프트 기반 학습으로 제한

## 데이터 준비

### 데이터세트 형식
```json
[
    {
        "text": "The capital of France is Paris."
    },
    {
        "text": "Machine learning enables computers to learn from data."
    }
]
```
### 데이터 품질 요구사항

1. **관련성**: 데이터가 대상 작업과 일치해야 합니다.
2. **다양성**: 극단적인 경우와 변형을 다루세요.
3. **크기**: 작업에 따라 100~10,000개 이상의 예시
4. **균형**: 분류를 위한 균형 클래스
5. **청결함**: 중복 및 오류 제거

### 데이터 증대
```python
def augment_data(text):
    variations = []

    # Paraphrasing
    variations.append(paraphrase(text))

    # Back-translation
    variations.append(back_translate(text))

    # Synonym replacement
    variations.append(replace_synonyms(text))

    return variations
```
## 훈련 과정

### 1단계: 데이터 준비
```python
from finetune_model import ModelFinetuner, FinetuningConfig

config = FinetuningConfig(
    model_name="gpt2",
    output_dir="./finetuned_model",
    train_file="train_data.json",
    validation_file="validation_data.json",
    use_lora=True,
    num_train_epochs=3,
    per_device_train_batch_size=4,
    learning_rate=2e-4
)

finetuner = ModelFinetuner(config)
finetuner.load_model()
```
### 2단계: 훈련
```python
finetuner.train()
```
### 3단계: 평가
```python
# Use validation set
validation_loss = finetuner.evaluate()

# Or test on held-out examples
test_results = finetuner.test(test_data)
```
### 4단계: 모델 저장
```python
finetuner.save_model()
```
## 하이퍼파라미터 튜닝

### 주요 매개변수

| 매개변수 | 일반적인 범위 | 영향 |
|------------|---------------|---------|
| 학습률 | 1e-5에서 5e-4 | 큰 영향 |
| 배치 크기 | 1-16 | 보통 영향 |
| 시대 | 1-10 | 데이터 크기에 따라 다름 |
| LoRA 순위(r) | 4-32 | 낮음-보통 영향 |
| LoRA 알파 | 16-128 | 낮은 영향 |
| 워밍업 단계 | 100-1000 | 보통 영향 |

### 튜닝 전략
```python
# Grid search
learning_rates = [1e-5, 5e-5, 1e-4]
batch_sizes = [4, 8]

for lr in learning_rates:
    for bs in batch_sizes:
        config.learning_rate = lr
        config.per_device_train_batch_size = bs
        finetuner.train()
        results.append(evaluate())
```
## 평가

### 측정항목

**언어 생성:**
- 당혹감
- BLEU 점수
- 루즈 점수
- 인간 평가

**분류:**
- 정확성
- F1 점수
- 정밀도/재현율
- 혼란 매트릭스

**질문 답변:**
- 정확한 일치
- F1 점수(토큰 수준)
- 의미적 유사성

### 평가 프레임워크
```python
from evaluate_model import ModelEvaluator

evaluator = ModelEvaluator()

# Add metrics
evaluator.add_metric(EvaluationMetric(
    name="perplexity",
    metric_type=MetricType.CUSTOM,
    description="Model perplexity"
))

# Run evaluation
report = evaluator.evaluate_model(
    model_name="finetuned_model",
    generate_func=generate_with_model,
    dataset=test_dataset
)
```
## 배포

### 미세 조정된 모델 로드
```python
finetuner.load_finetuned_model("path/to/model")

# Generate
response = finetuner.generate(
    prompt="Your prompt here",
    max_new_tokens=100,
    temperature=0.7
)
```
### 미세 조정된 모델 제공
```python
from serve_model import ModelServer

server = ModelServer(config)
server.load_model("finetuned_model", "path/to/model")
server.start()
```
### 다중 어댑터 배포
```python
# Switch between adapters
model.set_adapter("adapter_1")
output_1 = model.generate(prompt)

model.set_adapter("adapter_2")
output_2 = model.generate(prompt)
```
## 고급 기술

### 명령어 튜닝
```python
# Format: instruction + input + output
data = [
    {
        "instruction": "Summarize the following text.",
        "input": "Long text here...",
        "output": "Summary here..."
    }
]
```
### 다중 작업 학습
```python
# Train on multiple tasks simultaneously
tasks = ["summarization", "translation", "qa"]

for task in tasks:
    task_data = load_task_data(task)
    finetuner.train(task_data)
```
### 지속적인 학습
```python
# Learn new tasks without forgetting
for task in new_tasks:
    finetuner.train(task_data, replay_buffer=old_data)
```
## 일반적인 문제

### 치명적인 망각
- **증상**: 이전 작업의 성능이 저하됩니다.
- **해결책**: 재생 버퍼 사용, 탄력적 가중치 통합

### 과적합
- **증상**: 훈련 손실이 감소하고 검증 손실이 증가합니다.
- **해결책**: 에포크 감소, 드롭아웃 증가, 정규화 추가

### 과소적합
- **증상**: 학습 및 검증 손실이 모두 높음
- **해결책**: 모델 용량을 늘리고 학습 시간을 연장하세요.

### 열악한 융합
- **증상**: 손실이 진동하거나 감소하지 않음
- **해결책**: 학습률 조정, 데이터 품질 확인

## 모범 사례

1. **LoRA로 시작**: 대부분의 경우 완전한 미세 조정이 필요하지 않습니다.
2. **검증 손실 모니터링**: 과적합 전에 중지
3. **체크포인트 사용**: 최고 성능 모델 저장
4. **보존 데이터에 대한 평가**: 학습 측정항목만 신뢰하지 마세요.
5. **특정 사례에 대한 테스트**: 모델 견고성 검증
6. **문서 하이퍼파라미터**: 재현성 지원
7. **버전 관리 모델**: 모델 반복 추적