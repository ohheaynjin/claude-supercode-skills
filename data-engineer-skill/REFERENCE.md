# 데이터 엔지니어 - 기술 참조

## 워크플로: Airflow + dbt를 사용하여 일괄 ETL 파이프라인 구축

**사용 사례:** PostgreSQL에서 일일 데이터 동기화 → 분석용 Snowflake

### 1단계: 소스 시스템 분석
```python
# scripts/analyze_source.py
import pandas as pd
from sqlalchemy import create_engine

# Connect to source database
engine = create_engine('postgresql://user:pass@prod-db:5432/appdb')

# Analyze table sizes and row counts
tables_query = """
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size,
    (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = tablename) AS columns
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
LIMIT 20;
"""

tables_df = pd.read_sql(tables_query, engine)
print(tables_df)

# Identify incremental load candidates (tables with updated_at column)
incremental_tables = pd.read_sql("""
SELECT table_name
FROM information_schema.columns
WHERE column_name IN ('updated_at', 'modified_at', 'last_modified')
GROUP BY table_name
HAVING COUNT(*) >= 1;
""", engine)

print(f"\nIncremental load candidates: {len(incremental_tables)} tables")
```
### 2단계: 오케스트레이션을 위한 Airflow DAG
```python
# dags/daily_etl.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from datetime import datetime, timedelta
import pandas as pd

default_args = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'email': ['data-alerts@company.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'retry_exponential_backoff': True,
    'max_retry_delay': timedelta(minutes=30),
}

dag = DAG(
    'daily_etl_postgres_to_snowflake',
    default_args=default_args,
    description='Daily ETL from PostgreSQL to Snowflake',
    schedule_interval='0 2 * * *',  # 2 AM daily
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['etl', 'snowflake', 'production'],
)

def extract_and_load(table_name, incremental=False):
    """Extract from PostgreSQL and load to Snowflake"""
    
    pg_hook = PostgresHook(postgres_conn_id='postgres_prod')
    
    if incremental:
        sf_hook = SnowflakeHook(snowflake_conn_id='snowflake_warehouse')
        last_sync = sf_hook.get_first(f"""
            SELECT MAX(updated_at) 
            FROM ANALYTICS.RAW.{table_name.upper()}_SYNC_METADATA
        """)[0]
        
        query = f"""
            SELECT * FROM {table_name}
            WHERE updated_at > '{last_sync}'
        """
        print(f"Incremental load from {last_sync}")
    else:
        query = f"SELECT * FROM {table_name}"
        print(f"Full refresh of {table_name}")
    
    # Extract (stream in chunks for large tables)
    chunk_size = 100000
    df_iter = pg_hook.get_pandas_df_by_chunks(query, chunksize=chunk_size)
    
    sf_hook = SnowflakeHook(snowflake_conn_id='snowflake_warehouse')
    
    total_rows = 0
    for chunk_num, df_chunk in enumerate(df_iter):
        # Data quality checks
        assert df_chunk.isnull().sum().sum() < len(df_chunk) * 0.1, \
            f"Too many nulls in {table_name} chunk {chunk_num}"
        
        sf_hook.insert_rows(
            table=f'RAW.STG_{table_name.upper()}',
            rows=df_chunk.values.tolist(),
            target_fields=df_chunk.columns.tolist(),
        )
        
        total_rows += len(df_chunk)
        print(f"Loaded chunk {chunk_num}: {len(df_chunk)} rows")
    
    print(f"Total rows loaded: {total_rows}")
    return total_rows

# Create tasks dynamically for each table
tables_config = [
    {'name': 'users', 'incremental': False},
    {'name': 'orders', 'incremental': True},
    {'name': 'transactions', 'incremental': True},
    {'name': 'products', 'incremental': False},
]

extract_tasks = []
for table in tables_config:
    task = PythonOperator(
        task_id=f'extract_load_{table["name"]}',
        python_callable=extract_and_load,
        op_kwargs={
            'table_name': table['name'],
            'incremental': table['incremental']
        },
        dag=dag,
    )
    extract_tasks.append(task)

# dbt transformation task
dbt_run = SnowflakeOperator(
    task_id='dbt_transform',
    snowflake_conn_id='snowflake_warehouse',
    sql='CALL ANALYTICS.DBT.RUN_TRANSFORMATIONS()',
    dag=dag,
)

# Data quality checks
quality_checks = SnowflakeOperator(
    task_id='data_quality_checks',
    snowflake_conn_id='snowflake_warehouse',
    sql="""
        SELECT 'orders' AS table_name,
            COUNT(*) - COUNT(DISTINCT order_id) AS duplicates
        FROM ANALYTICS.MART.ORDERS
        HAVING duplicates > 0
        
        UNION ALL
        
        SELECT 'orders' AS table_name,
            COUNT(*) AS null_customer_ids
        FROM ANALYTICS.MART.ORDERS
        WHERE customer_id IS NULL
        HAVING null_customer_ids > 0
    """,
    dag=dag,
)

# DAG dependencies
extract_tasks >> dbt_run >> quality_checks
```
### 3단계: DBT 변환
```sql
-- models/staging/stg_orders.sql
{{
    config(
        materialized='incremental',
        unique_key='order_id',
        on_schema_change='append_new_columns',
        cluster_by=['order_date']
    )
}}

WITH source AS (
    SELECT *
    FROM {{ source('raw', 'orders') }}
    
    {% if is_incremental() %}
        WHERE updated_at > (SELECT MAX(updated_at) FROM {{ this }})
    {% endif %}
),

cleaned AS (
    SELECT
        order_id,
        customer_id,
        order_date,
        total_amount,
        currency,
        status,
        
        CASE 
            WHEN total_amount < 0 THEN 0
            ELSE total_amount
        END AS cleaned_total_amount,
        
        UPPER(TRIM(status)) AS standardized_status,
        DATE_TRUNC('month', order_date) AS order_month,
        updated_at,
        CURRENT_TIMESTAMP() AS dbt_loaded_at
    
    FROM source
    WHERE order_id IS NOT NULL
)

SELECT * FROM cleaned
```
### 실행 결과
```bash
# Run Airflow DAG
airflow dags trigger daily_etl_postgres_to_snowflake

# Expected output:
# [2024-01-15 02:00:00] extract_load_users: Loaded 10,000,000 rows (full refresh)
# [2024-01-15 02:15:00] extract_load_orders: Loaded 150,000 rows (incremental)
# [2024-01-15 02:20:00] extract_load_transactions: Loaded 500,000 rows (incremental)
# [2024-01-15 02:25:00] dbt_transform: 25 models run successfully
# [2024-01-15 02:30:00] data_quality_checks: PASSED (no issues detected)

# Cost analysis:
# - Snowflake compute: $45 (warehouse running 30 minutes)
# - Snowflake storage: $23/month (1TB compressed)
# - Total monthly cost: ~$2,000
```
## 세부 패턴

### 패턴: 멱등성 파티션 덮어쓰기
```python
# PySpark example: Overwrite partition based on execution date
def write_daily_partition(df, target_table, execution_date):
    """
    Writes data to a specific partition, overwriting existing data for that day.
    Safe to re-run multiple times.
    """
    (df
     .write
     .mode("overwrite")
     .partitionBy("process_date")
     .option("partitionOverwriteMode", "dynamic")
     .format("parquet")
     .saveAsTable(target_table))

# SQL Equivalent (Snowflake/BigQuery)
"""
MERGE INTO target t
USING source s
ON t.id = s.id AND t.process_date = s.process_date
WHEN MATCHED THEN
  UPDATE SET ...
WHEN NOT MATCHED THEN
  INSERT ...
"""
```
### 패턴: 데이터 품질 회로 차단기
```python
def check_data_quality(df, thresholds):
    """
    Returns True if data quality is acceptable, False otherwise.
    """
    total_rows = df.count()
    null_count = df.filter(col("critical_column").isNull()).count()
    null_ratio = null_count / total_rows
    
    if null_ratio > thresholds['max_null_ratio']:
        raise DataQualityException(
            f"Null ratio {null_ratio:.2%} exceeds limit {thresholds['max_null_ratio']:.2%}"
        )
        
    unique_count = df.select("id").distinct().count()
    if unique_count != total_rows:
        raise DataQualityException(
            f"Duplicate IDs found: {total_rows - unique_count} duplicates"
        )
        
    return True

# Usage in Airflow
check_task = PythonOperator(
    task_id='dq_check',
    python_callable=check_data_quality,
    op_kwargs={'thresholds': {'max_null_ratio': 0.01}}
)
```
### 패턴: 스트리밍을 위한 DLQ(배달 못한 편지 대기열)
```python
# Flink Side Output for DLQ
process_stream = stream.process(ProcessFunction())
valid_data = process_stream.get_side_output("valid")
bad_data = process_stream.get_side_output("dlq")

# Sink bad data to S3/GCS for manual inspection
bad_data.add_sink(
    FileSink.for_row_format(
        BasePath("s3://data-lake/dlq/"),
        Encoder()
    ).build()
)
```
