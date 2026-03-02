# PostgreSQL Professional - 기술 참조

## 이 스킬의 역할

postgres-pro 기술은 포괄적인 PostgreSQL 데이터베이스 관리 기능을 제공합니다. 구성 튜닝부터 복제 설정, 백업 자동화까지 엔드투엔드 PostgreSQL 최적화를 처리합니다. 이 기술은 솔루션이 높은 쿼리 성능(< 50ms), 최소 복제 지연(< 500ms), 탁월한 가동 시간(> 99.95%) 및 빠른 복구(RTO < 1시간)를 달성하도록 보장합니다.

## PostgreSQL 아키텍처

### 프로세스 아키텍처
- Postmaster (주요 프로세스)
- 백엔드 프로세스(연결당 하나)
- 백그라운드 작업자(autovacuum, WAL 작성자, 체크포인터)
- 보조 프로세스(로거, 아카이버, 통계 수집기)

### 메모리 구성
- **shared_buffers**: RAM의 25%(테이블/인덱스 데이터의 기본 캐시)
- **유효 캐시 크기**: RAM의 75%(플래너에게 OS 캐시에 대해 알려줌)
- **work_mem**: 정렬 및 해시 테이블을 위한 작업별 메모리
- **maintenance_work_mem**: VACUUM용 메모리, CREATE INDEX

### WAL 역학
- 내구성을 위한 미리 쓰기 로깅
- WAL 세그먼트(기본값 16MB)
- 체크포인트 튜닝(checkpoint_completion_target)
- PITR을 위한 WAL 아카이빙

### MVCC 구현
- 다중 버전 동시성 제어
- 거래 ID(XID)
- 튜플 가시성 규칙
- 데드 튜플 정리를 위한 진공

## 성능 튜닝

### 구성 최적화
```ini
# postgresql.conf - Production settings

# Memory
shared_buffers = '8GB'              # 25% of RAM
effective_cache_size = '24GB'       # 75% of RAM
work_mem = '64MB'                   # Per-operation memory
maintenance_work_mem = '2GB'        # For VACUUM, CREATE INDEX

# WAL
wal_level = replica
max_wal_size = '4GB'
min_wal_size = '1GB'
checkpoint_completion_target = 0.9

# Query Planning
random_page_cost = 1.1              # SSD storage
effective_io_concurrency = 200      # SSD storage
default_statistics_target = 100     # Statistics accuracy

# Autovacuum
autovacuum_vacuum_scale_factor = 0.05   # More aggressive
autovacuum_analyze_scale_factor = 0.02
autovacuum_vacuum_cost_delay = 2ms
autovacuum_max_workers = 4

# Connections
max_connections = 200               # Or use PgBouncer
```
### 진공 튜닝

Autovacuum은 다음과 같은 경우에 트리거됩니다.
- 데드 튜플 > autovacuum_vacuum_threshold + scale_factor * table_size
- 기본값: 50 + 0.2 * 행 = 20% 데드 튜플은 진공을 트리거합니다.

대형 테이블(행 100만 개 이상)의 경우:
```sql
ALTER TABLE large_table SET (
  autovacuum_vacuum_scale_factor = 0.01,  -- 1% instead of 20%
  autovacuum_analyze_scale_factor = 0.005,
  autovacuum_vacuum_threshold = 1000
);
```
## 파티셔닝 설계

### 범위 분할(시계열)
```sql
CREATE TABLE events (
  id SERIAL,
  created_at TIMESTAMP NOT NULL,
  data JSONB
) PARTITION BY RANGE (created_at);

-- Create partitions
CREATE TABLE events_2024_01 PARTITION OF events
  FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
CREATE TABLE events_2024_02 PARTITION OF events
  FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');
```
### 목록 분할(범주형)
```sql
CREATE TABLE orders (
  id SERIAL,
  region TEXT NOT NULL,
  total DECIMAL
) PARTITION BY LIST (region);

CREATE TABLE orders_us PARTITION OF orders
  FOR VALUES IN ('US', 'CA');
CREATE TABLE orders_eu PARTITION OF orders
  FOR VALUES IN ('UK', 'DE', 'FR');
```
### 파티션 유지 관리
```sql
-- Detach old partition (for archiving)
ALTER TABLE events DETACH PARTITION events_2023_01;

-- Create future partitions with pg_partman
CREATE EXTENSION pg_partman;
SELECT partman.create_parent(
  p_parent_table => 'public.events',
  p_control => 'created_at',
  p_type => 'native',
  p_interval => 'monthly'
);
```
## 고가용성 설정

### 스트리밍 복제 구성

**기본 서버(postgresql.conf):**
```ini
wal_level = replica
max_wal_senders = 10
max_replication_slots = 10
wal_keep_size = 1GB
hot_standby = on
archive_mode = on
archive_command = 'test ! -f /mnt/wal_archive/%f && cp %p /mnt/wal_archive/%f'
```
**기본 서버(pg_hba.conf):**
```
host    replication     replicator      192.168.1.0/24          scram-sha-256
```
**복제본 설정:**
```bash
# Stop PostgreSQL, clear data directory
sudo systemctl stop postgresql
sudo rm -rf /var/lib/postgresql/14/main/*

# Base backup from primary
sudo -u postgres pg_basebackup \
  -h primary_host \
  -D /var/lib/postgresql/14/main \
  -U replicator \
  -P -v -R -X stream -C -S replica_slot

# Start replica
sudo systemctl start postgresql
```
### 복제 모니터링
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
### 장애 조치 절차
```bash
# On REPLICA (promote to primary)
sudo -u postgres pg_ctl promote -D /var/lib/postgresql/14/main

# Or using SQL
sudo -u postgres psql -c "SELECT pg_promote();"

# Verify new primary
sudo -u postgres psql -c "SELECT pg_is_in_recovery();"  -- Should return 'f'
```
## 연결 풀링

### PgBouncer 구성
```ini
# pgbouncer.ini
[databases]
mydb = host=localhost port=5432 dbname=mydb

[pgbouncer]
pool_mode = transaction  # or session
max_client_conn = 1000
default_pool_size = 50
min_pool_size = 10
reserve_pool_size = 5
```
**성능 개선**: 연결 시간 20-50ms → <1ms(50배 빠름)

## 쿼리 모니터링

### 캐시 적중률
```sql
SELECT 
  sum(heap_blks_hit) / nullif(sum(heap_blks_hit) + sum(heap_blks_read), 0) as cache_hit_ratio
FROM pg_statio_user_tables;
-- Target: > 0.95 (95%)
```
### 테이블 팽창
```sql
SELECT 
  schemaname, tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size,
  n_dead_tup,
  n_live_tup,
  round(n_dead_tup::numeric / nullif(n_live_tup, 0) * 100, 2) as dead_ratio
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;
```
### 느린 쿼리(pg_stat_statements)
```sql
SELECT 
  calls,
  round(total_exec_time::numeric / 1000, 2) as total_time_sec,
  round(mean_exec_time::numeric, 2) as mean_time_ms,
  query
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 20;
```
## 다른 기술과의 통합

- **database-optimizer**: 일반적인 데이터베이스 최적화 기술에 대해 협력합니다.
- **backend-developer**: PostgreSQL 관련 쿼리 패턴 및 최적화 지원
- **데이터 엔지니어**: ETL 프로세스 및 데이터 파이프라인 통합에서 함께 작업합니다.
- **devops-engineer**: PostgreSQL 배포 및 인프라 자동화에 대한 가이드
- **sre-engineer**: 신뢰성, 모니터링, 사고 대응에 도움이 됩니다.
- **cloud-architect**: 클라우드 PostgreSQL(RDS, Cloud SQL 등) 지원
- **보안 감사자**: PostgreSQL 보안 및 규정 준수 파트너
- **성능 엔지니어**: 시스템 수준 성능 튜닝 조정