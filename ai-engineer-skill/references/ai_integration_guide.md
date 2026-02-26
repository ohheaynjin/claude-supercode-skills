# AI 통합 가이드

## 빠른 시작

### 설치
```bash
pip install openai anthropic chromadb sentence-transformers
```
### 환경 변수
```bash
export OPENAI_API_KEY="your-key"
export ANTHROPIC_API_KEY="your-key"
```
## OpenAI 통합

### 기본 사용법
```python
from integrate_openai import OpenAIIntegration, OpenAIConfig

config = OpenAIConfig(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4"
)

integration = OpenAIIntegration(config)

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
]

response = integration.chat_completion(messages)
print(response['content'])
```
### 구성 옵션
-`max_retries`: 재시도 횟수 (기본값: 3)
-`retry_delay`: 재시도 간 지연 시간(초)(기본값: 1.0)
-`timeout`: 요청 시간 초과(기본값: 120)
-`rate_limit_delay`: 속도 제한을 피하기 위한 지연 (기본값: 0.5)

## 인류 통합

### 기본 사용법
```python
from integrate_anthropic import AnthropicIntegration, AnthropicConfig

config = AnthropicConfig(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    model="claude-3-5-sonnet-20241022"
)

integration = AnthropicIntegration(config)

messages = [{"role": "user", "content": "Explain AI"}]
response = integration.messages(messages)
```
## RAG 설정

### 빠른 시작
```python
from setup_rag import RAGSystem, RAGConfig

config = RAGConfig(
    collection_name="my_docs",
    embedding_model="all-MiniLM-L6-v2"
)

rag = RAGSystem(config)

# Add documents
documents = [
    {
        'id': 'doc1',
        'text': 'Your document text here',
        'metadata': {'source': 'doc.txt'}
    }
]
rag.add_documents(documents)

# Query
results = rag.query("What is machine learning?")
for result in results:
    print(result['text'])
```
## 신속한 관리
```python
from manage_prompts import PromptManager, PromptTemplate

manager = PromptManager()

template = PromptTemplate(
    name="summary",
    template="Summarize: {text}",
    variables=["text"],
    description="Text summarization"
)

manager.add_template(template)

# Render
rendered = template.render(text="Your text here")
```
## 모니터링
```python
from monitor_ai_service import AIMonitor

monitor = AIMonitor(window_size=1000)

monitor.record_request(
    success=True,
    response_time=1.5,
    token_usage=1000
)

status = monitor.get_health_status()
print(f"Healthy: {status.is_healthy}")
```
## 비용 최적화
```python
from optimize_tokens import TokenTracker

tracker = TokenTracker()
tracker.record_usage(
    model="gpt-4",
    usage={'prompt_tokens': 100, 'completion_tokens': 50, 'total_tokens': 150}
)

cost = tracker.get_total_cost()
print(f"Total cost: ${cost:.4f}")
```
## 모범 사례

1. **속도 제한**: API 제한을 방지하려면 항상 속도 제한을 구현하세요.
2. **오류 처리**: 지수 백오프와 함께 재시도 로직을 사용합니다.
3. **토큰 추적**: 사용량을 모니터링하여 비용을 제어합니다.
4. **폴백 시스템**: 대체 모델로 폴백 구현
5. **모니터링**: 상태 지표 및 응답 시간 추적
6. **보안**: 버전 관리에 API 키를 커밋하지 마세요.

## 가격 참조

| 모델 | 입력(1K당) | 출력(1K당) |
|-------|---------------|---|
| GPT-4 | $0.03 | $0.06 |
| GPT-4 터보 | $0.01 | $0.03 |
| GPT-3.5 터보 | $0.0005 | $0.0015 |
| 클로드 3.5 소네트 | $0.003 | $0.015 |
| 클로드 3 작품 | $0.015 | $0.075 |