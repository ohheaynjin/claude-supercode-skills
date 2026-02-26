# LLM 건축가 - 예제 및 패턴

## 안티 패턴

### 안티 패턴: 프롬프트가 표시될 때 미세 조정하면 충분합니다.

**모습:**
```python
# User wants to change response format or style
# Jumps straight to fine-tuning a custom model
train_model(
    base_model="llama2-7b",
    dataset="responses_formatted_nicely.jsonl",
    epochs=3
)
```
**실패하는 이유:**
- 좋은 메시지를 전달하려면 컴퓨팅 비용이 수천 달러가 소요됩니다.
- 유지관리 부담(업데이트에 대한 재교육 필요)
- 느린 반복 주기(일 대 분)

**올바른 접근 방식:**
```python
# Try prompt engineering first (90% of cases this works)
prompt = """Output JSON in this exact format:
{
  "answer": "your response here",
  "confidence": 0.95,
  "sources": ["source1", "source2"]
}"""

# Only fine-tune if:
# - Prompting fails after extensive iteration
# - Need <50ms latency (fine-tuned model smaller/faster)
# - Highly domain-specific behavior required
```
---

### 안티 패턴: 대체 전략 없음

**모습:**
```python
# Single model, no error handling
response = claude.messages.create(
    model="claude-3-opus",
    messages=[{"role": "user", "content": prompt}]
)
# If Claude API is down → your app is down
```
**실패하는 이유:**
- API 중단 발생(99.9% 가동 시간 = 월 43분 가동 중지 시간)
- 예기치 않게 비율 제한에 도달할 수 있습니다.
- 단일 실패 지점

**올바른 접근 방식:**
```python
import asyncio

async def resilient_llm_call(prompt):
    # Strategy 1: Retry with exponential backoff
    for attempt in range(3):
        try:
            return await call_primary_llm(prompt)
        except RateLimitError:
            await asyncio.sleep(2 ** attempt)  # 1s, 2s, 4s
        except APIError as e:
            logger.warning(f"Attempt {attempt+1} failed: {e}")
    
    # Strategy 2: Fallback to alternative model
    try:
        return await call_fallback_llm(prompt)
    except Exception:
        pass
    
    # Strategy 3: Degrade gracefully
    return {
        "response": "Service temporarily unavailable, queued for processing",
        "queued": True
    }
```
---

### 안티 패턴: 컨텍스트 창 제한 무시

**모습:**
```python
# Stuffing entire document into prompt
prompt = f"Summarize this: {entire_100k_document}"
# API error: context length exceeded
```
**실패하는 이유:**
- 모델에는 토큰 제한이 있습니다(모델에 따라 4K-200K).
- 입력 크기에 따라 비용이 선형적으로 증가합니다.
- 컨텍스트가 매우 길면 품질이 저하됩니다.

**올바른 접근 방식:**
```python
def chunk_and_summarize(document: str, max_chunk_tokens: int = 4000) -> str:
    chunks = split_into_chunks(document, max_chunk_tokens)
    
    # Map: Summarize each chunk
    summaries = []
    for chunk in chunks:
        summary = await call_llm(f"Summarize this section:\n{chunk}")
        summaries.append(summary)
    
    # Reduce: Combine summaries
    if len(summaries) == 1:
        return summaries[0]
    
    combined = "\n\n".join(summaries)
    return await call_llm(f"Combine these summaries into one:\n{combined}")
```
---

### 안티 패턴: LLM을 데이터베이스로 취급

**모습:**
```python
# Asking model to recall specific facts from training
prompt = "What is customer ID 12345's current order status?"
```
**실패하는 이유:**
- 모델에는 결정론적 메모리가 없습니다.
- 그럴듯하게 들리지만 잘못된 정보를 환각시킨다.
- 훈련 데이터가 오래되었습니다(몇 개월에서 몇 년까지).

**올바른 접근 방식:**
```python
# Fetch from database, use LLM for synthesis/presentation
order_data = database.query("SELECT * FROM orders WHERE customer_id = 12345")
prompt = f"Summarize this order status for customer: {order_data}"

# LLM transforms data → user-friendly response
# Database provides facts (deterministic, accurate, up-to-date)
# LLM provides presentation (natural language, helpful)
```
---

### 안티 패턴: 출력 유효성 검사 없음

**모습:**
```python
# Trusting LLM output blindly
response = await call_llm("Generate a JSON config")
config = json.loads(response)  # Crashes if invalid JSON
```
**올바른 접근 방식:**
```python
import json
from pydantic import BaseModel, ValidationError

class ConfigOutput(BaseModel):
    setting_a: str
    setting_b: int
    enabled: bool

async def get_validated_config(prompt: str) -> ConfigOutput:
    for attempt in range(3):
        response = await call_llm(prompt)
        
        try:
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return ConfigOutput(**data)
        except (json.JSONDecodeError, ValidationError) as e:
            # Retry with error feedback
            prompt = f"{prompt}\n\nPrevious attempt failed: {e}. Please fix."
    
    raise ValueError("Failed to get valid output after 3 attempts")
```
---

## 품질 체크리스트

LLM 시스템 구현 완료를 표시하기 전에 이 체크리스트를 사용하십시오.

### 건축 및 디자인
- [ ] 지연 요구 사항이 문서화되고 검증되었습니다(P50, P95, P99).
- [ ] 예상 트래픽에 대해 계산된 비용 예측($/1,000개 요청)
- [ ] 절충 분석을 통해 정당화된 모델 선택
- [ ] 대체 전략 구현 및 테스트됨
- [ ] 확장 전략 정의됨(수평/수직, 트리거)

### 성능
- [ ] 대표 데이터 세트에 대한 벤치마크 결과(>1000개 예시)
- [ ] 정확도/품질 지표가 최소 기준을 충족합니다.
- [ ] P95 전반에 걸쳐 지연 시간 <2x 요구 사항
- [ ] 예상 최대 로드의 2배에서 테스트된 처리량
- [ ] 캐시 적중률 측정됨(캐싱이 구현된 경우)

### 비용 최적화
- [ ] 캐싱 전략 구현 및 검증
- [ ] 프롬프트 최적화 적용(압축, 템플릿)
- [ ] 다중 모델 라우팅 구성됨(해당하는 경우)
- [ ] 비용 모니터링 대시보드 생성
- [ ] 예산 알림이 구성됨(>110% 예상 지출)

### 안전 및 규정 준수
- [ ] 적대적인 예시에 대해 테스트된 콘텐츠 필터링
- [ ] PII 감지 및 수정 검증됨
- [ ] 즉각적인 주입 방어가 확립되어 있습니다.
- [ ] 출력 유효성 검사 규칙이 구현되었습니다.
- [ ] 모든 요청에 대해 감사 로깅이 구성되었습니다.
- [ ] 규정 준수 요구 사항이 문서화되고 검증되었습니다.

### 모니터링 및 관찰 가능성
- [ ] 추적된 지연 시간 지표(P50, P95, P99)
- [ ] 추적된 비용 지표($/일, $/1,000개 요청)
- [ ] 추적된 품질 지표(정확도, 사용자 평가)
- [ ] 오류율 추적 및 경고(>5% 오류율)
- [ ] 이해관계자를 위해 생성된 대시보드

### 운영 준비 상태
- [ ] 일반적인 오류 시나리오가 문서화된 Runbook
- [ ] 대기 중 에스컬레이션 경로가 정의됨
- [ ] 롤백 절차 테스트됨
- [ ] A/B 테스트 프레임워크 구성(필요한 경우)
- [ ] 모델 버전 관리 전략 구현

### 문서
- [ ] 아키텍처 다이어그램 작성 및 검토
- [ ] API 문서 게시됨(API를 노출하는 경우)
- [ ] 구성 문서가 완료되었습니다.
- [ ] 의사결정 로그 유지(이 모델이 필요한 이유, 이 접근 방식이 필요한 이유)
- [ ] 알려진 제한 사항이 문서화되었습니다.

---

## 신속한 엔지니어링 패턴

### 생각의 사슬
```python
prompt = """Solve this step by step:

Question: If a train travels at 60 mph for 2.5 hours, how far does it travel?

Let me think through this:
1. First, I'll identify the formula: distance = speed × time
2. Speed = 60 mph
3. Time = 2.5 hours
4. Distance = 60 × 2.5 = 150 miles

The train travels 150 miles.

Now solve this:
Question: {user_question}

Let me think through this:"""
```
### 몇 가지 예시
```python
prompt = """Classify the sentiment of these reviews:

Review: "The product arrived broken and customer service was unhelpful."
Sentiment: Negative

Review: "Exactly what I needed! Fast shipping too."
Sentiment: Positive

Review: "It works okay, nothing special but does the job."
Sentiment: Neutral

Review: "{user_review}"
Sentiment:"""
```
### 구조화된 출력
```python
prompt = """Extract information from this text and return as JSON:

Text: "John Smith, CEO of Acme Corp, announced Q3 revenue of $5.2M"

Output the following JSON structure:
{
  "person": "name of the person mentioned",
  "role": "their job title",
  "company": "company name",
  "metric": "any financial figures mentioned"
}

JSON:"""
```
