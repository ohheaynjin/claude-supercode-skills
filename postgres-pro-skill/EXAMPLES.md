# PostgreSQL Professional - 코드 예제 및 패턴

## JSONB 인덱싱 및 쿼리

### JSONB 스키마 설계
```sql
-- Create table with JSONB column
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255),
  metadata JSONB NOT NULL DEFAULT '{}',
  created_at TIMESTAMP DEFAULT NOW()
);

-- Sample JSONB data structure
INSERT INTO users (email, name, metadata) VALUES
  ('alice@example.com', 'Alice', '{
    "preferences": {
      "theme": "dark",
      "language": "en",
      "notifications": {
        "email": true,
        "push": false
      }
    },
    "profile": {
      "age": 28,
      "city": "San Francisco",
      "interests": ["tech", "hiking", "photography"]
    },
    "subscription": {
      "plan": "premium",
      "expires_at": "2025-12-31"
    }
  }');
```
### GIN 인덱스 생성
```sql
-- Default GIN index (supports all JSONB operators)
CREATE INDEX idx_users_metadata_gin ON users USING GIN (metadata);

-- GIN index with jsonb_path_ops (faster, containment only)
CREATE INDEX idx_users_metadata_path_ops ON users USING GIN (metadata jsonb_path_ops);

-- Partial GIN index (for specific keys)
CREATE INDEX idx_users_subscription ON users USING GIN ((metadata->'subscription'))
  WHERE metadata ? 'subscription';

-- Expression index for frequently queried path
CREATE INDEX idx_users_theme ON users ((metadata->'preferences'->>'theme'))
  WHERE metadata->'preferences' ? 'theme';
```
### 최적의 인덱스 사용을 위한 쿼리 패턴
```sql
-- Containment query (uses GIN index)
SELECT * FROM users
WHERE metadata @> '{"preferences": {"theme": "dark"}}';

-- Key existence check
SELECT * FROM users
WHERE metadata ? 'subscription';

-- Path extraction (uses expression index if exists)
SELECT email, metadata->'preferences'->>'theme' as theme
FROM users
WHERE metadata->'preferences'->>'theme' = 'dark';

-- Array containment
SELECT * FROM users
WHERE metadata->'profile'->'interests' @> '["tech"]';

-- Complex nested query
SELECT email, metadata
FROM users
WHERE metadata->'subscription'->>'plan' = 'premium'
  AND (metadata->'subscription'->>'expires_at')::DATE > CURRENT_DATE;

-- Aggregation on JSONB field
SELECT 
  metadata->'preferences'->>'theme' as theme,
  COUNT(*) as user_count
FROM users
WHERE metadata->'preferences' ? 'theme'
GROUP BY metadata->'preferences'->>'theme'
ORDER BY user_count DESC;
```
### 인덱스 사용량 확인
```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM users
WHERE metadata @> '{"preferences": {"theme": "dark"}}';

/*
Expected output with GIN index:
Bitmap Heap Scan on users  (cost=... actual time=0.234..1.456 rows=234 loops=1)
  Recheck Cond: (metadata @> '{"preferences": {"theme": "dark"}}'::jsonb)
  Heap Blocks: exact=123
  Buffers: shared hit=126
  ->  Bitmap Index Scan on idx_users_metadata_gin  (cost=... actual time=0.123 rows=234 loops=1)
        Index Cond: (metadata @> '{"preferences": {"theme": "dark"}}'::jsonb)
        Buffers: shared hit=3
*/
```
## 동시 새로 고침을 통한 구체화된 뷰
```sql
-- Create materialized view
CREATE MATERIALIZED VIEW mv_daily_sales AS
SELECT 
  DATE(created_at) as sale_date,
  product_id,
  COUNT(*) as order_count,
  SUM(total) as total_revenue,
  AVG(total) as avg_order_value
FROM orders
WHERE status = 'completed'
GROUP BY DATE(created_at), product_id
WITH DATA;

-- Unique index required for REFRESH CONCURRENTLY
CREATE UNIQUE INDEX mv_daily_sales_pkey ON mv_daily_sales (sale_date, product_id);

-- Refresh without blocking reads
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_daily_sales;

-- Schedule refresh with pg_cron
CREATE EXTENSION IF NOT EXISTS pg_cron;

SELECT cron.schedule(
  'refresh-daily-sales',
  '0 2 * * *',  -- Every day at 2 AM
  'REFRESH MATERIALIZED VIEW CONCURRENTLY mv_daily_sales'
);
```
## 안티 패턴 및 수정 사항

### 안티 패턴: 연결 풀링을 사용하지 않음

**나쁜:**
```python
# Opening new connection for every request (NO connection pool)
def handle_request():
    conn = psycopg2.connect("dbname=mydb user=postgres")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    result = cur.fetchall()
    conn.close()  # Close connection after each request
    return result
```
**실패하는 이유:**
- **연결 오버헤드**: 연결 생성에 20~50ms가 소요됩니다(풀에서는 1ms 미만).
- **리소스 소진**: PostgreSQL max_connections 제한(일반적으로 200-400)
- **성능 저하**: 연결 설정 오버헤드가 쿼리 시간을 지배합니다.

**좋음:**
```python
# Use connection pool
from psycopg2 import pool

# Create connection pool (application startup)
connection_pool = pool.SimpleConnectionPool(
    minconn=10,
    maxconn=50,
    dbname="mydb",
    user="postgres",
    host="localhost"
)

def handle_request():
    conn = connection_pool.getconn()  # Get from pool (reuse existing)
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        result = cur.fetchall()
        return result
    finally:
        connection_pool.putconn(conn)  # Return to pool (don't close)
```
**성능 개선**: 20-50ms → 요청당 <1ms(50배 더 ​​빠름).

### 안티 패턴: 열거된 값에 TEXT 사용

**나쁜:**
```sql
-- Storing status as unbounded TEXT
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  status TEXT,  -- Could be anything: 'pending', 'Pending', 'PENDING', 'pnding' (typo)
  total DECIMAL(10,2)
);
```
**실패하는 이유:**
- **데이터 무결성**: 데이터베이스 수준 유효성 검사 없음(오타, 잘못된 값)
- **저장 낭비**: TEXT는 ENUM 또는 SMALLINT보다 더 많은 공간을 사용합니다.
- **쿼리 성능**: CHECK 제약 조건 또는 ENUM으로 최적화할 수 없습니다.

**좋음:**
```sql
-- Option 1: ENUM type (PostgreSQL-specific, best for few values)
CREATE TYPE order_status AS ENUM ('pending', 'processing', 'completed', 'canceled');

CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  status order_status NOT NULL DEFAULT 'pending',  -- Type-safe!
  total DECIMAL(10,2)
);

-- Typos are caught at database level
INSERT INTO orders (status, total) VALUES ('complted', 100.00);
-- ERROR: invalid input value for enum order_status: "complted"

-- Option 2: CHECK constraint (portable across databases)
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  status VARCHAR(20) NOT NULL DEFAULT 'pending'
    CHECK (status IN ('pending', 'processing', 'completed', 'canceled')),
  total DECIMAL(10,2)
);

-- Option 3: Foreign key to lookup table (best for many values)
CREATE TABLE order_statuses (
  id SMALLINT PRIMARY KEY,
  name VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  status_id SMALLINT NOT NULL REFERENCES order_statuses(id) DEFAULT 1,
  total DECIMAL(10,2)
);
```
## 스트리밍 복제 설정

### 기본 서버 구성
```bash
# Edit postgresql.conf on PRIMARY
sudo vim /etc/postgresql/14/main/postgresql.conf

# Replication settings
wal_level = replica
max_wal_senders = 10
max_replication_slots = 10
wal_keep_size = 1GB
hot_standby = on
archive_mode = on
archive_command = 'test ! -f /mnt/wal_archive/%f && cp %p /mnt/wal_archive/%f'
```
### 복제 사용자 및 슬롯 생성
```sql
-- On PRIMARY, create replication user
CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD 'secure_password';

-- Create replication slot (prevents WAL deletion)
SELECT * FROM pg_create_physical_replication_slot('replica_1_slot');

-- Verify slots created
SELECT slot_name, slot_type, active FROM pg_replication_slots;
```
### 복제 서버 설정
```bash
# Stop PostgreSQL on replica
sudo systemctl stop postgresql

# Remove existing data directory
sudo rm -rf /var/lib/postgresql/14/main/*

# Base backup from primary
sudo -u postgres pg_basebackup -h primary_host -D /var/lib/postgresql/14/main -U replicator -P -v -R -X stream -C -S replica_1_slot

# Start replica
sudo systemctl start postgresql

# Verify replication status
sudo -u postgres psql -c "SELECT pg_is_in_recovery();"  -- Should return 't'
```
### 복제 지연 모니터링
```sql
-- On PRIMARY: Check connected replicas
SELECT 
  client_addr,
  state,
  sync_state,
  pg_wal_lsn_diff(sent_lsn, replay_lsn) AS replication_lag_bytes
FROM pg_stat_replication;

-- On REPLICA: Check lag in seconds
SELECT 
  NOW() - pg_last_xact_replay_timestamp() AS replication_lag_seconds;
```
