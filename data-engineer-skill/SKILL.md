---
name: data-engineer
description: 사용자에게 확장 가능한 데이터 파이프라인 개발, ETL/ELT 구현 또는 데이터 인프라 설계가 필요한 경우 사용합니다.
---
# 데이터 엔지니어

## 목적

확장 가능한 데이터 파이프라인, ETL/ELT 워크플로우, 데이터 레이크 및 데이터 웨어하우스를 구축하기 위한 전문적인 데이터 엔지니어링 기능을 제공합니다. 안정성과 비용 최적화에 중점을 둔 분산 데이터 처리, 스트림 처리, 데이터 품질 및 최신 데이터 스택 기술(Airflow, dbt, Spark, Kafka)을 전문으로 합니다.

## 사용 시기

- 소스부터 소비 계층까지 엔드투엔드 데이터 파이프라인 설계
- 오류 처리 및 데이터 품질 검사를 통해 ETL/ELT 워크플로우 구현
- 최적의 저장 및 쿼리 기능을 갖춘 데이터 레이크 또는 데이터 웨어하우스 구축
- 실시간 스트림 처리 설정(Kafka, Flink, Kinesis)
- 데이터 인프라 비용 최적화(스토리지 계층화, 컴퓨팅 효율성)
- 데이터 거버넌스 및 규정 준수 구현(GDPR, 데이터 계보)
- 레거시 데이터 시스템을 최신 데이터 플랫폼으로 마이그레이션

## 빠른 시작

**다음과 같은 경우에 이 스킬을 호출하세요:**
- 소스부터 소비 계층까지 엔드투엔드 데이터 파이프라인 설계
- 오류 처리 및 데이터 품질 검사를 통해 ETL/ELT 워크플로우 구현
- 최적의 저장 및 쿼리 기능을 갖춘 데이터 레이크 또는 데이터 웨어하우스 구축
- 실시간 스트림 처리 설정(Kafka, Flink, Kinesis)
- 데이터 인프라 비용 최적화(스토리지 계층화, 컴퓨팅 효율성)
- 데이터 거버넌스 및 규정 준수 구현(GDPR, 데이터 계보)

**다음과 같은 경우에는 호출하지 마세요.**
- SQL 쿼리 최적화만 필요함(대신 데이터베이스 최적화 프로그램 사용)
- 기계 학습 모델 개발(ML-엔지니어 또는 데이터 과학자 사용)
- 간단한 데이터 분석 또는 시각화(데이터 분석가 사용)
- 데이터베이스 관리 작업(데이터베이스 관리자 사용)
- 데이터 변환 없이 API 통합(백엔드 개발자 사용)

## 의사결정 프레임워크

### 파이프라인 아키텍처 선택
```
├─ Batch Processing?
│   ├─ Daily/hourly schedules → Airflow + dbt
│   │   Pros: Mature ecosystem, SQL-based transforms
│   │   Cost: Low-medium
│   │
│   ├─ Large-scale (TB+) → Spark (EMR/Databricks)
│   │   Pros: Distributed processing, handles scale
│   │   Cost: Medium-high (compute-intensive)
│   │
│   └─ Simple transforms → dbt Cloud or Fivetran
│       Pros: Managed, low maintenance
│       Cost: Medium (SaaS pricing)
│
├─ Stream Processing?
│   ├─ Event streaming → Kafka + Flink
│   │   Pros: Low latency, exactly-once semantics
│   │   Cost: High (always-on infrastructure)
│   │
│   ├─ AWS native → Kinesis + Lambda
│   │   Pros: Serverless, auto-scaling
│   │   Cost: Variable (pay per use)
│   │
│   └─ Simple CDC → Debezium + Kafka Connect
│       Pros: Database change capture
│       Cost: Medium
│
└─ Hybrid (Batch + Stream)?
    └─ Lambda Architecture or Kappa Architecture
        Lambda: Separate batch/speed layers
        Kappa: Single stream-first approach
```
### 데이터 저장소 선택

| 사용 사례 | 기술 | 장점 | 단점 |
|------------|------------|------|------|
| **구조적 분석** | 눈송이/BigQuery | SQL, 빠른 쿼리 | 대규모 비용 |
| **반구조적** | 삼각주/빙산 | ACID, 스키마 진화 | 복잡성 |
| **원시 스토리지** | S3/GCS | 저렴하고 내구성 | 쿼리 엔진 없음 |
| **실시간** | Redis/다이나모DB | 낮은 대기 시간 | 제한된 분석 |
| **시계열** | 타임스케일DB/인플럭스DB | 시간 데이터에 최적화 | 특정 사용 사례 |

### ETL 대 ELT 결정

| 요인 | ETL(변환 우선) | ELT(먼저 로드) |
|---------|---------|------|
| **데이터 볼륨** | 중소 | 대형(TB+) |
| **변환** | 복합, 예압 | SQL 기반, 창고 내 |
| **지연 시간** | 더 높은 | 낮은 |
| **비용** | 로드 전 계산 | 창고 컴퓨팅 |
| **최고의 대상** | 레거시 시스템 | 최신 클라우드 DW |

## 핵심 패턴

### 패턴 1: 멱등성 파티션 덮어쓰기
**사용 사례:** 중복을 생성하지 않고 일괄 작업을 안전하게 다시 실행합니다.
```python
# PySpark example: Overwrite partition based on execution date
def write_daily_partition(df, target_table, execution_date):
    (df
     .write
     .mode("overwrite")
     .partitionBy("process_date")
     .option("partitionOverwriteMode", "dynamic")
     .format("parquet")
     .saveAsTable(target_table))
```
### 패턴 2: 느리게 변경되는 차원 유형 2(SCD2)
**사용 사례:** 과거 상태를 잃지 않고 변경 내역을 추적합니다.
```sql
-- dbt implementation of SCD2
{{ config(materialized='incremental', unique_key='user_id') }}

SELECT 
    user_id, address, email, status, updated_at,
    LEAD(updated_at, 1, '9999-12-31') OVER (
        PARTITION BY user_id ORDER BY updated_at
    ) as valid_to
FROM {{ source('raw', 'users') }}
```
### 패턴 3: 스트리밍용 DLQ(배달 못한 편지 대기열)
**사용 사례:** 파이프라인을 중지하지 않고 잘못된 형식의 메시지를 처리합니다.

### 패턴 4: 데이터 품질 회로 차단기
**사용 사례:** 데이터 품질이 임계값 아래로 떨어지면 파이프라인 실행을 중지합니다.

## 품질 체크리스트

### 데이터 파이프라인
- [ ] 멱등성(재시도해도 안전함)
- [ ] 스키마 유효성 검사가 시행되었습니다.
- [ ] 재시도를 통한 오류 처리
- [ ] 데이터 품질 검사 자동화
- [ ] 모니터링 및 경고 구성
- [ ] 혈통이 문서화됨

### 성능
- [ ] 파이프라인이 SLA 내에 완료됩니다(예: 1시간 미만).
- [ ] 해당되는 경우 증분 로딩
- [ ] 파티셔닝 전략 최적화
- [ ] 쿼리 성능 <30초 (P95)

### 비용 최적화
- [ ] 스토리지 계층화 구현(핫/웜/콜드)
- [ ] 컴퓨팅 자동 확장이 구성됨
- [ ] 쿼리 비용 모니터링 활성
- [ ] 압축 활성화됨(Parquet/ORC)

## 추가 리소스

- **자세한 기술 참조**: [REFERENCE.md](REFERENCE.md) 참조
- **코드 예제 및 패턴**: [EXAMPLES.md](EXAMPLES.md) 참조