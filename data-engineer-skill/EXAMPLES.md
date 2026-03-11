# 데이터 엔지니어 - 코드 예제 및 패턴

## 안티 패턴: 데이터 파이프라인에 멱등성이 없습니다.

### 외관(나쁨):```python
def daily_etl():
    # Extract new data
    new_data = extract_from_api()
    
    # Transform
    transformed_data = transform(new_data)
    
    # Load (append mode)
    transformed_data.to_sql('fact_orders', engine, if_exists='append')

# Problem: If pipeline fails halfway and restarts → duplicates!
```

### 실패 이유:
- 파이프라인 실패로 인해 중복 레코드가 생성됨
- 실패한 실행을 안전하게 재시도할 수 있는 방법이 없습니다.
- 데이터 무결성이 손상됨
- 개수 및 집계가 올바르지 않게 됩니다.

### 올바른 접근 방식:```python
import uuid
from datetime import datetime

def daily_etl(run_date=None, run_id=None):
    # Generate unique run ID
    if run_id is None:
        run_id = str(uuid.uuid4())
    
    if run_date is None:
        run_date = datetime.now().date()
    
    print(f"ETL Run ID: {run_id}, Date: {run_date}")
    
    # Check if this run already completed
    existing_run = engine.execute(f"""
        SELECT status FROM etl_runs 
        WHERE run_id = '{run_id}' AND run_date = '{run_date}'
    """).fetchone()
    
    if existing_run and existing_run[0] == 'completed':
        print(f"Run {run_id} already completed, skipping")
        return
    
    # Record run start
    engine.execute(f"""
        INSERT INTO etl_runs (run_id, run_date, status, started_at)
        VALUES ('{run_id}', '{run_date}', 'running', NOW())
        ON CONFLICT (run_id, run_date) DO UPDATE SET started_at = NOW()
    """)
    
    try:
        # Extract
        data = extract_from_api(run_date)
        
        # Transform (add run_id to each record)
        data['etl_run_id'] = run_id
        data['etl_loaded_at'] = datetime.now()
        
        # Load with merge (upsert)
        # Option 1: Delete + Insert (for small datasets)
        engine.execute(f"""
            DELETE FROM fact_orders WHERE order_date = '{run_date}'
        """)
        data.to_sql('fact_orders', engine, if_exists='append', index=False)
        
        # Record completion
        engine.execute(f"""
            UPDATE etl_runs 
            SET status = 'completed', completed_at = NOW(), rows_processed = {len(data)}
            WHERE run_id = '{run_id}' AND run_date = '{run_date}'
        """)
        
        print(f"ETL completed: {len(data)} rows processed")
        
    except Exception as e:
        # Record failure
        engine.execute(f"""
            UPDATE etl_runs 
            SET status = 'failed', error_message = '{str(e)}'
            WHERE run_id = '{run_id}' AND run_date = '{run_date}'
        """)
        raise

# Safe to retry with same run_id
daily_etl(run_date='2024-01-15', run_id='specific-run-id-123')
```

## dbt Mart 모델 예시

```sql
-- models/marts/fact_orders.sql
{{
    config(
        materialized='table',
        cluster_by=['order_month', 'customer_id']
    )
}}

WITH orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),

customers AS (
    SELECT * FROM {{ ref('stg_customers') }}
),

order_items AS (
    SELECT 
        order_id,
        COUNT(*) AS item_count,
        SUM(quantity) AS total_quantity
    FROM {{ ref('stg_order_items') }}
    GROUP BY order_id
)

SELECT
    o.order_id,
    o.customer_id,
    c.customer_name,
    c.customer_segment,
    o.order_date,
    o.order_month,
    o.cleaned_total_amount AS total_amount,
    o.currency,
    o.standardized_status AS status,
    i.item_count,
    i.total_quantity,
    
    -- Business metrics
    CASE 
        WHEN o.cleaned_total_amount >= 1000 THEN 'High Value'
        WHEN o.cleaned_total_amount >= 100 THEN 'Medium Value'
        ELSE 'Low Value'
    END AS order_value_tier,
    
    o.dbt_loaded_at

FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id
LEFT JOIN order_items i ON o.order_id = i.order_id
```

## SCD 유형 2 구현

```sql
-- dbt snapshot for SCD2
{% snapshot users_snapshot %}

{{
    config(
      target_schema='snapshots',
      unique_key='user_id',
      strategy='check',
      check_cols=['address', 'email', 'status'],
    )
}}

SELECT * FROM {{ source('raw', 'users') }}

{% endsnapshot %}
```

## 오류 처리 기능이 있는 Kafka 소비자

```python
from kafka import KafkaConsumer, KafkaProducer
import json

consumer = KafkaConsumer(
    'orders',
    bootstrap_servers=['kafka:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=False,
    group_id='order-processor'
)

dlq_producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda m: json.dumps(m).encode('utf-8')
)

def process_message(message):
    try:
        order = message.value
        
        # Validate required fields
        required_fields = ['order_id', 'customer_id', 'amount']
        for field in required_fields:
            if field not in order:
                raise ValueError(f"Missing required field: {field}")
        
        # Process the order
        result = transform_and_load(order)
        return result
        
    except Exception as e:
        # Send to Dead Letter Queue
        dlq_message = {
            'original_message': message.value,
            'error': str(e),
            'topic': message.topic,
            'partition': message.partition,
            'offset': message.offset,
            'timestamp': datetime.now().isoformat()
        }
        dlq_producer.send('orders-dlq', dlq_message)
        print(f"Sent to DLQ: {e}")
        return None

for message in consumer:
    result = process_message(message)
    if result:
        consumer.commit()
```

## 워터마크를 사용한 Spark 스트리밍

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import window, col, from_json
from pyspark.sql.types import StructType, StringType, TimestampType, DoubleType

spark = SparkSession.builder \
    .appName("OrderStreaming") \
    .getOrCreate()

schema = StructType() \
    .add("order_id", StringType()) \
    .add("customer_id", StringType()) \
    .add("amount", DoubleType()) \
    .add("event_time", TimestampType())

# Read from Kafka
orders_stream = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "orders") \
    .load() \
    .select(from_json(col("value").cast("string"), schema).alias("data")) \
    .select("data.*")

# Aggregate with watermark for late data handling
order_aggregates = orders_stream \
    .withWatermark("event_time", "10 minutes") \
    .groupBy(
        window(col("event_time"), "5 minutes"),
        col("customer_id")
    ) \
    .agg(
        {"amount": "sum", "order_id": "count"}
    )

# Write to console (or sink to database)
query = order_aggregates \
    .writeStream \
    .outputMode("update") \
    .format("console") \
    .start()

query.awaitTermination()
```
