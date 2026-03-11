# RAG 패턴

## 핵심 구성 요소

### 1. 문서 청킹

**고정 크기 청크:**```python
chunk_size = 512
chunk_overlap = 50
```

**의미적 덩어리:**
- 문장 경계를 사용하세요
- 단락 구조 유지
- 상황 일관성 유지

### 2. 모델 삽입

**빠름/소형:**
-`all-MiniLM-L6-v2`(384 어둡게, 빠르게)
-`all-mpnet-base-v2`(768 밝기, 균형)

**대형/정확함:**
-`text-embedding-3-large`(오픈AI)
-`text-embedding-3-small`(오픈AI)

### 3. 검색 전략

**단순한:**```python
results = rag.query(query_text, n_results=5)
```

**거르는:**```python
results = rag.query(
    query_text,
    n_results=5,
    where={'category': 'technical'}
)
```

**하이브리드 검색:**
- 의미 검색과 키워드 검색 결합
- 크로스 인코더로 결과 순위 재지정

## 고급 패턴

### 멀티홉 RAG

여러 단계에 걸쳐 정보를 검색합니다.```python
def multi_hop_query(initial_query):
    # First hop
    results1 = rag.query(initial_query)
    context1 = " ".join(r['text'] for r in results1)

    # Second hop based on first results
    followup = f"Based on: {context1}\nQuery: {followup_question}"
    results2 = rag.query(followup)

    return results1 + results2
```

### 에이전트 RAG

에이전트가 검색할 항목을 결정하도록 합니다.```python
def agentic_rag(query):
    # Agent decides retrieval strategy
    strategy = agent.analyze_query(query)

    if strategy['needs_retrieval']:
        results = rag.query(query, **strategy['params'])
    else:
        results = []

    # Generate answer with retrieved context
    return agent.generate_answer(query, results)
```

###재순위

검색 품질 향상:```python
def rerank(query, results, top_k=5):
    from sentence_transformers import CrossEncoder

    reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

    pairs = [[query, r['text']] for r in results]
    scores = reranker.predict(pairs)

    ranked = sorted(zip(results, scores), key=lambda x: x[1], reverse=True)
    return [r for r, s in ranked[:top_k]]
```

### 인용 관리

트랙 소스 정보:```python
def generate_with_citations(query):
    results = rag.query(query)

    response = llm.generate(
        f"Answer: {query}\n\nContext: {[r['text'] for r in results]}"
    )

    citations = [
        {'source': r['metadata']['source'], 'chunk_id': r['metadata']['chunk_id']}
        for r in results
    ]

    return {'answer': response, 'citations': citations}
```

## 평가

### RAGAS 프레임워크```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy

metrics = [faithfulness, answer_relevancy]
results = evaluate(dataset, metrics)
```

### 맞춤 측정항목```python
def retrieval_accuracy(expected_docs, retrieved_docs):
    expected_ids = set(d['id'] for d in expected_docs)
    retrieved_ids = set(d['id'] for d in retrieved_docs)

    recall = len(expected_ids & retrieved_ids) / len(expected_ids)
    precision = len(expected_ids & retrieved_ids) / len(retrieved_ids)

    return {'recall': recall, 'precision': precision}
```

## Performance Optimization

### Vector Index Tuning
```python
# Use IVF for large collections
index_params = {
    "index_type": "IVF_FLAT",
    "nlist": 100,
    "metric_type": "IP"
}
```

### Cache Frequently Asked Questions
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_query(query_hash):
    return rag.query(query_hash)
```

## Best Practices

1. **Chunk size**: 500-1000 tokens usually works well
2. **Overlap**: 10-20% overlap maintains context
3. **Embeddings**: Choose based on speed vs accuracy needs
4. **Reranking**: Always rerank top 20-50 results
5. **Evaluation**: Regularly test retrieval quality
6. **Update strategy**: Implement incremental updates
