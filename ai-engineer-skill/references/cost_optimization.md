# 비용 최적화 전략

## 토큰 비용 이해하기

### 토큰 가격(1,000개 토큰당)

| 모델 | 입력 | 산출 | 문맥 |
|-------|-------|--------|---------|
| GPT-4 | $0.03 | $0.06 | 8K |
| GPT-4 터보 | $0.01 | $0.03 | 128K |
| GPT-3.5 터보 | $0.0005 | $0.0015 | 16K |
| 클로드 3.5 소네트 | $0.003 | $0.015 | 200K |
| 직장 3개 닫기 | $0.015 | $0.075 | 200K |

### 비용 추정

**대략적인 토큰:**```python
def estimate_tokens(text):
    # Rough estimate: 1 token ≈ 0.75 words
    return len(text.split()) * 1.3
```

**전체 요청 비용:**```python
def calculate_cost(model, input_tokens, output_tokens):
    pricing = {
        'gpt-4': {'input': 0.03, 'output': 0.06},
        'gpt-4-turbo': {'input': 0.01, 'output': 0.03},
    }

    input_cost = (input_tokens / 1000) * pricing[model]['input']
    output_cost = (output_tokens / 1000) * pricing[model]['output']

    return input_cost + output_cost
```

## 최적화 기술

### 1. 모델 선정

**작업에 적합한 모델을 사용하세요.**

```python
def select_model(task_complexity, budget):
    if task_complexity == 'simple' and budget < 0.01:
        return 'gpt-3.5-turbo'
    elif task_complexity == 'medium' and budget < 0.10:
        return 'gpt-4-turbo'
    elif task_complexity == 'complex':
        return 'gpt-4'
    else:
        return 'gpt-3.5-turbo'  # Default cheapest
```

**계층형 접근 방식:**
1. 가장 작은 모델부터 시작하세요
2. 품질이 부족한 경우 에스컬레이션하세요.
3. 반복 통화를 피하기 위해 결과를 캐시합니다.

### 2. 프롬프트 최적화

**메시지 길이 줄이기:**```python
def optimize_prompt(prompt, target_length=500):
    while estimate_tokens(prompt) > target_length:
        # Remove redundancies
        prompt = remove_redundancies(prompt)
        # Use abbreviations
        prompt = abbreviate_common_terms(prompt)
        # Simplify language
        prompt = simplify_language(prompt)

    return prompt
```

**시스템 프롬프트 사용:**```python
# Bad: Repeats context in every prompt
prompt = "You are a helpful assistant. Be concise. " + user_message

# Good: Set once, then use minimal prompts
client.chat.completions.create(
    messages=[
        {"role": "system", "content": "You are a helpful, concise assistant."},
        {"role": "user", "content": user_message}
    ]
)
```

### 3. 캐싱 전략

**응답 캐싱:**```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=1000)
def cached_llm_call(prompt_hash):
    return client.generate(original_prompt)

def generate_with_cache(prompt):
    prompt_hash = hashlib.md5(prompt.encode()).hexdigest()
    return cached_llm_call(prompt_hash)
```

**캐싱 삽입:**```python
embedding_cache = {}

def get_embeddings(texts):
    uncached = [t for t in texts if t not in embedding_cache]

    if uncached:
        new_embeddings = client.embeddings.create(uncached)
        for text, emb in zip(uncached, new_embeddings):
            embedding_cache[text] = emb

    return [embedding_cache[t] for t in texts]
```

### 4. 일괄 처리

**일괄 요청:**```python
def batch_generate(prompts, batch_size=10):
    results = []

    for i in range(0, len(prompts), batch_size):
        batch = prompts[i:i+batch_size]
        # Use batch API if available
        batch_results = client.batch.generate(batch)
        results.extend(batch_results)

    return results
```

### 5. 긴 출력을 위한 스트리밍

```python
def generate_streaming(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )

    full_content = ""
    for chunk in response:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            full_content += content
            # Process chunk as it arrives
            process_chunk(content)

    return full_content
```

### 6. 토큰 한도 관리

**스마트 잘림:**```python
def smart_truncate(text, max_tokens, preserve_intro=True):
    if estimate_tokens(text) <= max_tokens:
        return text

    if preserve_intro:
        # Keep first and last parts
        intro_tokens = max_tokens * 0.3
        outro_tokens = max_tokens * 0.7
        return truncate_ends(text, intro_tokens, outro_tokens)
    else:
        return truncate_from_start(text, max_tokens)
```

**컨텍스트 창 최적화:**```python
def optimize_context_window(query, context, max_tokens):
    query_tokens = estimate_tokens(query)
    available_tokens = max_tokens - query_tokens - 100  # Buffer

    # Select most relevant context
    ranked_contexts = rank_relevance(query, context)
    selected_contexts = []

    for ctx in ranked_contexts:
        ctx_tokens = estimate_tokens(ctx)
        if sum(estimate_tokens(c) for c in selected_contexts) + ctx_tokens <= available_tokens:
            selected_contexts.append(ctx)
        else:
            break

    return "\n\n".join(selected_contexts)
```

## 모니터링 및 경고

### 비용 추적

```python
class CostMonitor:
    def __init__(self, budget_limit):
        self.total_cost = 0
        self.budget_limit = budget_limit
        self.alerts = []

    def track_usage(self, model, input_tokens, output_tokens):
        cost = calculate_cost(model, input_tokens, output_tokens)
        self.total_cost += cost

        if self.total_cost > self.budget_limit * 0.8:
            self.alerts.append(f"Budget warning: {self.total_cost:.2f}")

        if self.total_cost > self.budget_limit:
            self.alerts.append(f"Budget exceeded: {self.total_cost:.2f}")

    def get_report(self):
        return {
            'total_cost': self.total_cost,
            'budget_limit': self.budget_limit,
            'utilization': self.total_cost / self.budget_limit,
            'alerts': self.alerts
        }
```

### 최적화 권장 사항

```python
def analyze_usage(usage_data):
    recommendations = []

    # High cost per request
    avg_cost = usage_data['total_cost'] / usage_data['request_count']
    if avg_cost > 0.10:
        recommendations.append("Consider using smaller models")

    # High error rate leads to retries
    if usage_data['error_rate'] > 0.05:
        recommendations.append("Improve error handling to reduce retries")

    # Low cache hit rate
    if usage_data['cache_hit_rate'] < 0.30:
        recommendations.append("Implement response caching")

    return recommendations
```

## 비용 절감 패턴

### 1. 계층형 LLM 전략```
Level 1: Small model for simple tasks (gpt-3.5-turbo)
Level 2: Medium model for complex tasks (gpt-4-turbo)
Level 3: Large model for critical tasks (gpt-4)
```

### 2. 하이브리드 접근 방식
- 간단한 작업에는 로컬 모델을 사용하세요.
- 복잡한 추론을 위해 API 모델을 사용하세요.
- 가능한 모든 것을 캐시하세요

### 3. 대체 패턴```python
def generate_with_fallbacks(prompt, models=['gpt-4', 'gpt-3.5-turbo']):
    for model in models:
        try:
            return generate(model, prompt)
        except RateLimitError:
            continue

    raise Exception("All models failed")
```

## 모범 사례

1. **지속적으로 모니터링**: 실시간으로 비용을 추적합니다.
2. **예산 설정**: 사용자/프로젝트당 한도 적용
3. **프롬프트 최적화**: 불필요한 컨텍스트 제거
4. **적극적으로 캐시**: 반복 계산 방지
5. **올바른 모델 선택**: 작업 복잡성에 따라 모델 연결
6. **스트리밍 사용**: 긴 출력에 대한 대기 시간 줄이기
7. **일괄 요청**: API가 지원하는 경우
8. **작은 모델로 테스트**: 값비싼 모델로 확장하기 전