# ML/AI 기술 전환 프로젝트

## 개요

이 프로젝트는 모범 사례, 오류 처리 및 구성 관리와 함께 프로덕션용으로 설계된 11가지 ML/AI 관련 기술에 대한 포괄적인 스크립트와 참조를 제공합니다.

## 프로젝트 구조
```
claude-skills-conversion/
├── ai-engineer-skill/          # AI service integration, RAG, prompts
├── llm-architect-skill/        # LLM design, fine-tuning, serving
├── ml-engineer-skill/           # ML pipelines, scikit-learn
├── mlops-engineer-skill/        # MLflow, deployment, monitoring
├── machine-learning-engineer-skill/  # Jupyter, feature engineering
├── data-engineer-skill/         # ETL pipelines, data lakes
├── data-scientist-skill/        # Statistical analysis, visualization
├── data-analyst-skill/          # Data analysis, dashboards
├── prompt-engineer-skill/       # Prompt optimization, A/B testing
├── postgres-pro-skill/          # PostgreSQL administration
├── devops-incident-responder-skill/  # Incident response automation
└── incident-responder-skill/     # Alert handling and triage
```
## 스킬 생성

### 1. AI 엔지니어
**스크립트:**
-`integrate_openai.py`- 재시도 로직과 OpenAI API 통합
-`integrate_anthropic.py`- 클로드 API 통합
-`setup_rag.py`- 벡터 데이터베이스를 갖춘 RAG 시스템
-`manage_prompts.py`- 프롬프트 템플릿 관리
-`monitor_ai_service.py`- AI 서비스 상태 모니터링
-`optimize_tokens.py`- 토큰 사용량 및 비용 추적

**참고자료:**
- 빠른 시작이 가능한 AI 통합 가이드
- RAG 패턴 및 모범 사례
- 프롬프트 템플릿 라이브러리
- 비용 최적화 전략

**사용 사례:**
- LLM API 통합
- RAG 구현
- 신속한 관리
- 비용 모니터링 및 최적화

### 2. LLM 설계자
**스크립트:**
-`benchmark_models.py`- 모델 비교 및 선택
-`finetune_model.py`- LoRA/PEFT를 이용한 미세 조정
-`setup_rag_pipeline.py`- 엔드투엔드 RAG 파이프라인
-`serve_model.py`- 모델 서비스 인프라
-`engineer_prompts.py`- 신속한 최적화
-`evaluate_model.py`- 모델 평가 프레임워크

**참고자료:**
- 모델 선택 가이드
- LoRA를 이용한 미세 조정 가이드
- 서비스 인프라(vLLM, Docker, K8s)
- 평가 지표 및 프레임워크

**사용 사례:**
- 모델 벤치마킹 및 선정
- PEFT/LoRA를 이용한 미세 조정
- RAG 파이프라인 아키텍처
- 프로덕션 모델 서빙

### 3. ML 엔지니어
**스크립트:**
-`train_sklearn.py`- Scikit-learn 교육 파이프라인
-`tune_hyperparameters.py`- Optuna 하이퍼파라미터 최적화

**참고자료:**
- Scikit-learn 모범 사례
- 모델 버전 관리 전략
- 실험 추적

**사용 사례:**
- 기존 ML 모델 학습
- 하이퍼파라미터 최적화
- 모델 배포 준비

### 4. MLOps 엔지니어
**스크립트:**
-`track_mlflow.py`- MLflow 실험 추적 및 모델 등록

**사용 사례:**
- 실험 추적
- 모델 레지스트리 관리
- MLOps 파이프라인 오케스트레이션

### 5. 포스트그레SQL 프로
**스크립트:**
-`backup_pg.py`- PostgreSQL 백업 및 복원

**사용 사례:**
- 데이터베이스 백업 전략
- 자동 백업 예약
- 재해 복구

### 6. 데이터 엔지니어
**스크립트:**
-`run_etl_pipeline.py`- 스케줄링을 통한 ETL 자동화

**사용 사례:**
- 데이터 파이프라인 자동화
- 변환 및 검증
- 예약된 데이터 처리

### 7. 사고 대응자
**스크립트:**
-`handle_alerts.py`- 사건 분류 및 분류

**사용 사례:**
- 경고 라우팅 및 분류
- 이해관계자 알림
- 사고 수명주기 관리

## 설치

### 전제 조건
```bash
# Python dependencies
pip install scikit-learn pandas numpy
pip install transformers peft datasets
pip install chromadb sentence-transformers
pip install mlflow optuna
pip install openai anthropic
pip install fastapi uvicorn

# Optional: GPU support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```
### 환경 설정
```bash
# Set API keys
export OPENAI_API_KEY="your-openai-key"
export ANTHROPIC_API_KEY="your-anthropic-key"

# PostgreSQL
export PGPASSWORD="your-db-password"
```
## 빠른 시작 예

### AI 엔지니어 - OpenAI 통합
```python
from ai_engineer_skill.scripts.integrate_openai import OpenAIIntegration, OpenAIConfig

config = OpenAIConfig(api_key=os.getenv("OPENAI_API_KEY"))
integration = OpenAIIntegration(config)

messages = [{"role": "user", "content": "Hello!"}]
response = integration.chat_completion(messages)
print(response['content'])
```
### LLM 설계자 - 모델 벤치마킹
```python
from llm_architect_skill.scripts.benchmark_models import ModelBenchmarker

benchmarker = ModelBenchmarker(models)
benchmarker.benchmark_task("summarization", task_func, test_data)
best = benchmarker.get_best_model_for_task("summarization")
```
### ML 엔지니어 - 교육 파이프라인
```python
from ml_engineer_skill.scripts.train_sklearn import MLModelTrainer, ModelConfig

trainer = MLModelTrainer(ModelConfig())
X_train, X_test = trainer.preprocess_features(X_train, X_test)
trainer.train_model(X_train, y_train)
metrics = trainer.evaluate_model(X_test, y_test)
```
### MLOps - MLflow 추적
```python
from mlops_engineer_skill.scripts.track_mlflow import MLflowTracker

tracker = MLflowTracker(experiment_name="my_experiment")
run_id = tracker.start_run("run_1")
tracker.log_params({"lr": 0.01, "epochs": 10})
tracker.log_metrics({"accuracy": 0.95})
tracker.log_model(model, "my_model")
tracker.end_run()
```
## 모범 사례

### 오류 처리
모든 스크립트에는 다음이 포함됩니다.
- 로깅이 포함된 Try-Exception 블록
- 우아한 저하
- 오류 메시지 지우기

### 구성
- YAML/JSON 구성 파일 지원
- 환경변수 지원
- 재정의가 포함된 기본값

### 로깅
- 구조화된 로깅
- 여러 로그 수준
- 타임스탬프 및 컨텍스트

### 문서
- 복잡한 논리에 대한 인라인 주석
- 함수/클래스에 대한 Docstring
- README 및 참조 가이드

## 기여

각 기술은 일관된 패턴을 따릅니다.
1. 생성`scripts/`실행 가능한 코드를 위한 디렉토리
2. 생성`references/`문서용 디렉토리
3. 구성을 위해 데이터 클래스를 사용하세요
4. 오류 처리 및 로깅 포함
5. 예시 사용법을 제공하세요.`main()`기능

## 라이선스

프로덕션 준비가 완료된 교육 코드입니다. 귀하의 요구에 적응하십시오.

## 다음 단계

다음 기술에는 구현할 준비가 된 자리 표시자 구조가 있습니다.
- 머신러닝-엔지니어-기술
- 데이터 과학자 기술
- 데이터 분석가 기술
- 신속한 엔지니어 기술
- devops-incident-responder-skill

이러한 기술을 구현하려면 기존 패턴을 따르세요.