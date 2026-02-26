# 서비스 인프라 가이드

## 개요

프로덕션 모델을 제공하려면 성능, 확장성, 안정성을 신중하게 고려해야 합니다.

## 제공 옵션

### 1. API 기반 서비스

공급자 API(OpenAI, Anthropic 등) 사용

**장점:**
- 인프라 제로
- 자동 스케일링
- 모니터링 내장
- 정기 업데이트

**단점:**
- 지속적인 비용
- 데이터 개인 정보 보호 문제
- 비율 제한
- 외부 서비스에 대한 의존성

**최적의 용도:**
- 개념 증명
- 낮거나 중간 정도의 트래픽
- ML 인프라팀 없음
- 신속한 프로토타이핑

### 2. 자체 호스팅 서비스

자체 인프라에 모델 배포

**장점:**
- 모든 권한
- 데이터 개인정보 보호
- 예측 가능한 비용
- 맞춤 최적화

**단점:**
- 인프라 구축
- 유지관리 간접비
- 확장 복잡성
- 초기비용이 높다

**최적의 용도:**
- 대량 생산
- 민감한 데이터
- 맞춤형 모델
- 규모에 따른 비용 최적화

## 서빙 프레임워크

### vLLM

PagedAttention을 통한 높은 처리량 제공.

**설치:**
```bash
pip install vllm
```
**용법:**
```bash
python -m vllm.entrypoints.api_server \
    --model meta-llama/Llama-2-7b-hf \
    --port 8000 \
    --tensor-parallel-size 4
```
**장점:**
- 10~20배 더 높은 처리량
- 낮은 대기 시간
- 지속적인 일괄 처리
- OpenAI 호환 API

**단점:**
- 최신, 덜 전투 테스트됨
- 제한된 모델 지원

### 텍스트 생성 WebUI(Oobabooga)

모델 제공을 위한 기능이 풍부한 웹 인터페이스입니다.

**특징:**
- 웹 UI
- 다중 모델 지원
- 확장 생태계
- API 액세스

**설정:**
```bash
git clone https://github.com/oobabooga/text-generation-webui
cd text-generation-webui
python server.py --model-path /path/to/model --listen
```
### 로컬AI

로컬 모델을 위한 OpenAI 호환 API입니다.

**설정:**
```bash
docker run -p 8080:8080 \
    -v /models:/models \
    localai/localai \
    --models-path /models
```
**OpenAI 클라이언트 사용:**
```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="not-needed"
)
```
## 배포 전략

### 도커 배포

**도커파일:**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

RUN pip install fastapi uvicorn transformers accelerate torch

COPY model.py .
COPY ./models ./models

CMD ["uvicorn", "model:app", "--host", "0.0.0.0", "--port", "8000"]
```
**빌드 및 실행:**
```bash
docker build -t model-server .
docker run -p 8000:8000 --gpus all model-server
```
### 쿠버네티스 배포

**배포 YAML:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: model-server
spec:
  replicas: 3
  selector:
    matchLabels:
      app: model-server
  template:
    metadata:
      labels:
        app: model-server
    spec:
      containers:
      - name: model-server
        image: model-server:latest
        ports:
        - containerPort: 8000
        resources:
          limits:
            nvidia.com/gpu: 1
```
**서비스:**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: model-server
spec:
  selector:
    app: model-server
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```
### 서버리스 배포

**AWS 람다:**
```python
import json

def lambda_handler(event, context):
    prompt = event['prompt']
    response = generate_with_model(prompt)
    return {
        'statusCode': 200,
        'body': json.dumps({'output': response})
    }
```
## 성능 최적화

### 일괄 처리
```python
@app.post("/batch_generate")
async def batch_generate(requests: List[GenerationRequest]):
    outputs = []
    for request in requests:
        output = generate(request)
        outputs.append(output)
    return outputs
```
### 캐싱
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_generate(prompt_hash):
    return generate(original_prompt)
```
### 양자화
```python
from transformers import BitsAndBytesConfig

quantization_config = BitsAndBytesConfig(
    load_in_8bit=True
)

model = AutoModelForCausalLM.from_pretrained(
    model_path,
    quantization_config=quantization_config
)
```
### 스트림 응답
```python
async def stream_generate(prompt):
    for token in model.generate_stream(prompt):
        yield token
```
## 모니터링

### 주요 지표

1. **처리량**: 초당 요청
2. **지연 시간**: P50, P95, P99 응답 시간
3. **오류율**: 요청 실패
4. **GPU 활용률**: 컴퓨팅 효율성
5. **메모리 사용량**: VRAM 소비

### 프로메테우스 통합
```python
from prometheus_client import Counter, Histogram

request_counter = Counter('model_requests_total', 'Total requests')
latency_histogram = Histogram('model_latency_seconds', 'Request latency')

@app.post("/generate")
async def generate(request: GenerationRequest):
    with latency_histogram.time():
        output = generate_with_model(request)
        request_counter.inc()
        return output
```
### 상태 점검
```python
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "gpu_available": torch.cuda.is_available(),
        "memory_used": torch.cuda.memory_allocated()
    }
```
## 스케일링

### 수평 확장

증가된 로드를 처리하려면 인스턴스를 더 추가하세요.

**쿠버네티스 HPA:**
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: model-server-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: model-server
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 80
```
### 수직 확장

인스턴스당 리소스를 늘립니다.

**GPU 유형:**
- A100(40GB/80GB): 최고의 성능
- V100(16GB/32GB): 밸런스 좋음
- T4(16GB): 가성비
- L4(24GB): 최신 옵션

### 로드 밸런싱
```nginx
upstream model_servers {
    least_conn;
    server server1:8000;
    server server2:8000;
    server server3:8000;
}

server {
    listen 80;
    location / {
        proxy_pass http://model_servers;
    }
}
```
## 모범 사례

1. **FastAPI 사용**: 비동기, 유형 안전, 자동 문서
2. **비율 제한 구현**: 남용 방지
3. **인증 추가**: 보안 엔드포인트
4. **모든 것을 기록**: 디버깅 및 모니터링
5. **버전 모델**: 간편한 롤백
6. **우아한 종료**: 연결을 적절하게 처리합니다.
7. **상태 확인**: Kubernetes 준비
8. **리소스 제한**: 메모리 누수 방지
9. **검증 요청**: Pydantic 모델 사용
10. **지속적으로 모니터링**: 문제를 조기에 감지