# LLM 설계자 - 기술 참조

## RAG 시스템 구현

**사용 사례:** 문서 Q&A를 위한 검색 증강 생성 구축

### 1. 문서 처리 파이프라인
```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
from datetime import datetime

# Step 1: Load documents
documents = load_documents("./knowledge_base/")  # PDFs, HTML, MD, etc.

# Step 2: Chunking strategy (critical for retrieval quality)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # Tokens, not characters
    chunk_overlap=200,  # Overlap to preserve context
    separators=["\n\n", "\n", ". ", " ", ""]  # Preserve semantic boundaries
)
chunks = text_splitter.split_documents(documents)

# Step 3: Add metadata (enables filtering)
for chunk in chunks:
    chunk.metadata["source_file"] = chunk.metadata.get("source")
    chunk.metadata["chunk_index"] = chunks.index(chunk)
    chunk.metadata["created_at"] = datetime.now().isoformat()
```
### 2. 임베딩 및 벡터 스토어
```python
from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI

# Initialize Pinecone
pc = Pinecone(api_key="YOUR_API_KEY")
index = pc.Index("llm-rag-demo")

# Embedding model options:
# - OpenAI text-embedding-3-small: $0.02/1M tokens, 1536 dims, fast
# - Cohere embed-english-v3.0: $0.10/1M tokens, 1024 dims, high quality
# - Local BAAI/bge-large-en-v1.5: Free, 1024 dims, self-hosted

client = OpenAI()

def embed_chunks(chunks, batch_size=100):
    embeddings = []
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i+batch_size]
        texts = [chunk.page_content for chunk in batch]
        
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=texts
        )
        embeddings.extend([r.embedding for r in response.data])
    
    return embeddings

# Upload to vector store
embeddings = embed_chunks(chunks)
index.upsert(vectors=zip(ids, embeddings, metadatas))
```
### 3. 하이브리드 검색을 통한 검색
```python
from sentence_transformers import CrossEncoder

def retrieve_context(query, top_k=5):
    # Step 1: Dense retrieval (semantic similarity)
    query_embedding = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    ).data[0].embedding
    
    dense_results = index.query(
        vector=query_embedding,
        top_k=top_k * 2,  # Get more candidates
        include_metadata=True
    )
    
    # Step 2: Rerank with cross-encoder (optional, +50% relevance)
    reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    
    candidates = [(r.metadata['text'], r.score) for r in dense_results.matches]
    reranked = reranker.rank(query, [c[0] for c in candidates])
    
    # Return top-k after reranking
    return reranked[:top_k]
```
### 4. 검색된 컨텍스트를 사용한 생성
```python
import anthropic

anthropic_client = anthropic.Anthropic()

def generate_answer(query, context_chunks):
    # Build prompt with retrieved context
    context = "\n\n".join([
        f"[Source {i+1}]: {chunk['text']}"
        for i, chunk in enumerate(context_chunks)
    ])
    
    prompt = f"""Answer the question using ONLY the provided sources.
If the sources don't contain enough information, say "I don't have enough information to answer this."

Sources:
{context}

Question: {query}

Answer:"""
    
    # Generate with Claude
    response = anthropic_client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.content[0].text


# Full RAG pipeline
def rag_query(query):
    context_chunks = retrieve_context(query, top_k=5)
    answer = generate_answer(query, context_chunks)
    return {
        "answer": answer,
        "sources": context_chunks,  # Return for citation
        "confidence": calculate_confidence(context_chunks)
    }
```
### 5. 평가 및 반복
```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy

results = evaluate(
    dataset=eval_dataset,
    metrics=[faithfulness, answer_relevancy]
)

# Expected baselines:
# - Faithfulness (answer matches sources): >90%
# - Answer relevancy: >85%
# - Retrieval precision@5: >70%
```
---

## 시맨틱 캐싱 레이어

**사용 시기:** 반복되거나 유사한 쿼리(60% 이상의 적중률 달성 가능)
```python
import hashlib
import time
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

class SemanticCache:
    def __init__(self, embedding_model):
        self.client = QdrantClient(":memory:")
        self.client.create_collection(
            collection_name="llm_cache",
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
        )
        self.embedding_model = embedding_model
        self.ttl_seconds = 86400  # 24 hours
    
    async def get(self, query, similarity_threshold=0.95):
        # Embed query
        query_vec = self.embedding_model.encode(query)
        
        # Search for similar cached queries
        results = self.client.search(
            collection_name="llm_cache",
            query_vector=query_vec,
            limit=1
        )
        
        if results and results[0].score >= similarity_threshold:
            # Check TTL
            cached_time = results[0].payload["timestamp"]
            if time.time() - cached_time < self.ttl_seconds:
                return results[0].payload["response"]  # CACHE HIT
        
        return None  # Cache miss
    
    async def set(self, query, response):
        query_vec = self.embedding_model.encode(query)
        cache_id = hashlib.md5(query.encode()).hexdigest()
        
        self.client.upsert(
            collection_name="llm_cache",
            points=[{
                "id": cache_id,
                "vector": query_vec,
                "payload": {
                    "query": query,
                    "response": response,
                    "timestamp": time.time()
                }
            }]
        )
```
**예상 절감액:** 60% 이상의 쿼리를 캐시할 수 있는 경우 40-80% 비용 절감

---

## 쿠버네티스 배포
```yaml
# kubernetes/llm-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-service
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: vllm-server
        image: vllm/vllm-openai:latest
        resources:
          limits:
            nvidia.com/gpu: 1
        env:
        - name: MODEL_NAME
          value: "mistralai/Mistral-7B-Instruct-v0.2"
        - name: TENSOR_PARALLEL_SIZE
          value: "1"
        - name: MAX_MODEL_LEN
          value: "4096"
        ports:
        - containerPort: 8000
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 60
          periodSeconds: 10
```
---

## 다중 모델 라우팅
```python
from enum import Enum
from typing import Literal

class ModelTier(Enum):
    FAST = "haiku"      # Simple queries, <500ms
    BALANCED = "sonnet"  # Medium complexity
    POWERFUL = "opus"    # Complex reasoning

def classify_query_complexity(query: str) -> ModelTier:
    """Route queries to appropriate model tier"""
    
    # Simple heuristics (replace with classifier in production)
    word_count = len(query.split())
    
    if word_count < 20 and "?" in query:
        return ModelTier.FAST
    
    complex_indicators = [
        "explain", "analyze", "compare", "evaluate",
        "step by step", "reasoning", "implications"
    ]
    
    if any(indicator in query.lower() for indicator in complex_indicators):
        return ModelTier.POWERFUL
    
    return ModelTier.BALANCED


async def route_and_call(query: str) -> str:
    tier = classify_query_complexity(query)
    
    model_map = {
        ModelTier.FAST: "claude-3-haiku-20240307",
        ModelTier.BALANCED: "claude-3-sonnet-20240229",
        ModelTier.POWERFUL: "claude-3-opus-20240229"
    }
    
    response = await anthropic_client.messages.create(
        model=model_map[tier],
        max_tokens=1024,
        messages=[{"role": "user", "content": query}]
    )
    
    return response.content[0].text
```
---

## 안전 가드레일

### 콘텐츠 필터링
```python
from typing import Tuple

async def check_safety(content: str) -> Tuple[bool, str]:
    """Check content for safety issues"""
    
    # PII detection
    pii_patterns = [
        r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
        r'\b\d{16}\b',             # Credit card
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'  # Email
    ]
    
    import re
    for pattern in pii_patterns:
        if re.search(pattern, content):
            return False, "PII detected"
    
    # Prompt injection detection
    injection_patterns = [
        "ignore previous instructions",
        "disregard all prior",
        "you are now",
        "new instructions:"
    ]
    
    content_lower = content.lower()
    for pattern in injection_patterns:
        if pattern in content_lower:
            return False, "Potential prompt injection"
    
    return True, "OK"


async def safe_llm_call(query: str) -> str:
    # Check input
    is_safe, reason = await check_safety(query)
    if not is_safe:
        return f"Request blocked: {reason}"
    
    # Get response
    response = await call_llm(query)
    
    # Check output
    is_safe, reason = await check_safety(response)
    if not is_safe:
        return "Response filtered for safety reasons"
    
    return response
```
---

## 모니터링 설정

### 추적할 주요 지표
```python
import prometheus_client as prom

# Define metrics
llm_request_latency = prom.Histogram(
    'llm_request_latency_seconds',
    'LLM request latency',
    ['model', 'endpoint'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
)

llm_request_tokens = prom.Counter(
    'llm_request_tokens_total',
    'Total tokens processed',
    ['model', 'type']  # type: input/output
)

llm_cache_hits = prom.Counter(
    'llm_cache_hits_total',
    'Cache hit count',
    ['cache_type']  # exact/semantic
)

llm_errors = prom.Counter(
    'llm_errors_total',
    'LLM error count',
    ['model', 'error_type']
)


# Usage in request handler
async def handle_llm_request(query: str):
    with llm_request_latency.labels(model='sonnet', endpoint='/chat').time():
        response = await call_llm(query)
    
    llm_request_tokens.labels(model='sonnet', type='input').inc(len(query.split()))
    llm_request_tokens.labels(model='sonnet', type='output').inc(len(response.split()))
    
    return response
```
