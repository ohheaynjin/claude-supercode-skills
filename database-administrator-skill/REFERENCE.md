# 데이터베이스 관리자 - 기술 참조

## 워크플로: 고가용성을 갖춘 PostgreSQL 프로덕션 설정

### 1단계: 아키텍처 설계

```yaml
# Architecture: Primary-Replica with Patroni + etcd
Components:
  - 3-node PostgreSQL cluster (1 primary + 2 replicas)
  - 3-node etcd cluster (distributed consensus)
  - Patroni (automatic failover orchestration)
  - HAProxy or PgBouncer (connection pooling + load balancing)
  - Continuous WAL archiving to S3

Expected Performance:
  - Automatic failover: <30 seconds
  - Zero data loss (synchronous replication)
  - Read scaling via replicas
  - Connection pooling: 10K connections → 100 database connections
```

### 2단계: PostgreSQL 구성(postgresql.conf)

```ini
# /etc/postgresql/15/main/postgresql.conf

# --- CONNECTIONS AND AUTHENTICATION ---
max_connections = 200
superuser_reserved_connections = 3

# --- RESOURCE USAGE (8GB RAM, 4 CPU server) ---
shared_buffers = 2GB                    # 25% of RAM
effective_cache_size = 6GB              # 75% of RAM
maintenance_work_mem = 512MB
work_mem = 10MB                         # Per operation

# --- WRITE AHEAD LOG (WAL) ---
wal_level = replica
max_wal_senders = 5
wal_keep_size = 1GB
archive_mode = on
archive_command = 'aws s3 cp %p s3://company-db-backups/wal/%f'
archive_timeout = 300

# --- REPLICATION ---
hot_standby = on
max_replication_slots = 5
hot_standby_feedback = on
wal_receiver_timeout = 60s

# --- QUERY TUNING ---
random_page_cost = 1.1                  # SSD storage
effective_io_concurrency = 200          # SSD concurrent I/O
default_statistics_target = 100

# --- AUTOVACUUM ---
autovacuum = on
autovacuum_max_workers = 4
autovacuum_naptime = 10s
autovacuum_vacuum_scale_factor = 0.05
autovacuum_analyze_scale_factor = 0.02

# --- LOGGING ---
log_destination = 'csvlog'
logging_collector = on
log_directory = '/var/log/postgresql'
log_min_duration_statement = 1000       # Log queries >1 second
log_checkpoints = on
log_connections = on
log_disconnections = on
log_lock_waits = on
```

### 3단계: Patroni 구성(patroni.yml)

```yaml
# /etc/patroni/patroni.yml
scope: postgres-cluster
namespace: /db/
name: postgres-node-1

restapi:
  listen: 0.0.0.0:8008
  connect_address: 10.0.1.10:8008

etcd:
  hosts: 10.0.1.20:2379,10.0.1.21:2379,10.0.1.22:2379

bootstrap:
  dcs:
    ttl: 30
    loop_wait: 10
    retry_timeout: 10
    maximum_lag_on_failover: 1048576
    postgresql:
      use_pg_rewind: true
      use_slots: true
      parameters:
        max_connections: 200
        shared_buffers: 2GB
        wal_level: replica
        hot_standby: on

  initdb:
    - encoding: UTF8
    - data-checksums

  pg_hba:
    - host replication replicator 10.0.1.0/24 md5
    - host all all 10.0.0.0/16 md5

postgresql:
  listen: 0.0.0.0:5432
  connect_address: 10.0.1.10:5432
  data_dir: /var/lib/postgresql/15/main
  bin_dir: /usr/lib/postgresql/15/bin
  authentication:
    replication:
      username: replicator
      password: CHANGE_ME
    superuser:
      username: postgres
      password: CHANGE_ME

tags:
  nofailover: false
  noloadbalance: false
  clonefrom: false
```

### 4단계: HAProxy 로드 밸런서(haproxy.cfg)

```conf
# /etc/haproxy/haproxy.cfg

global
    maxconn 4000
    log /dev/log local0

defaults
    log global
    mode tcp
    option tcplog
    timeout connect 5s
    timeout client 30m
    timeout server 30m

listen stats
    mode http
    bind *:7000
    stats enable
    stats uri /

# Primary (read-write)
listen postgres-primary
    bind *:5432
    mode tcp
    option httpchk
    http-check expect status 200
    default-server inter 3s fall 3 rise 2
    server postgres-node-1 10.0.1.10:5432 maxconn 100 check port 8008
    server postgres-node-2 10.0.1.11:5432 maxconn 100 check port 8008 backup
    server postgres-node-3 10.0.1.12:5432 maxconn 100 check port 8008 backup

# Replicas (read-only)
listen postgres-replicas
    bind *:5433
    mode tcp
    option httpchk GET /replica
    http-check expect status 200
    default-server inter 3s fall 3 rise 2
    server postgres-node-2 10.0.1.11:5432 maxconn 100 check port 8008
    server postgres-node-3 10.0.1.12:5432 maxconn 100 check port 8008
```

### 5단계: 자동 백업 스크립트

```bash
#!/bin/bash
# /usr/local/bin/postgres-backup.sh

set -e

BACKUP_DIR="/var/backups/postgresql"
S3_BUCKET="s3://company-db-backups"
RETENTION_DAYS=30
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

echo "Starting PostgreSQL backup at $TIMESTAMP"

# Base backup with compression
pg_basebackup -h localhost -U postgres \
  -D "${BACKUP_DIR}/base-${TIMESTAMP}" \
  -Ft -z -Xs -P \
  --checkpoint=fast \
  --label="automated-backup-${TIMESTAMP}"

# Upload to S3
aws s3 sync "${BACKUP_DIR}/base-${TIMESTAMP}" \
  "${S3_BUCKET}/base-backups/${TIMESTAMP}/" \
  --storage-class STANDARD_IA

# Cleanup local backups older than 7 days
find "${BACKUP_DIR}" -type d -mtime +7 -exec rm -rf {} +

echo "Backup completed successfully"
```

### 배포 단계

```bash
# 1. Install PostgreSQL 15 on all nodes
sudo apt update
sudo apt install -y postgresql-15 postgresql-contrib-15

# 2. Install Patroni
sudo apt install -y python3-pip python3-etcd
sudo pip3 install patroni[etcd]

# 3. Setup etcd cluster
sudo apt install -y etcd

# 4. Configure Patroni on each node
sudo cp patroni.yml /etc/patroni/
sudo systemctl enable patroni
sudo systemctl start patroni

# 5. Install HAProxy
sudo apt install -y haproxy
sudo cp haproxy.cfg /etc/haproxy/
sudo systemctl restart haproxy

# 6. Setup automated backups
sudo cp postgres-backup.sh /usr/local/bin/
sudo chmod +x /usr/local/bin/postgres-backup.sh
echo "0 2 * * * /usr/local/bin/postgres-backup.sh" | sudo crontab -

# 7. Verify cluster status
patronictl -c /etc/patroni/patroni.yml list

# Expected output:
# + Cluster: postgres-cluster ----+---------+---------+----+-----------+
# | Member          | Host        | Role    | State   | TL | Lag in MB |
# +-----------------+-------------+---------+---------+----+-----------+
# | postgres-node-1 | 10.0.1.10   | Leader  | running |  1 |           |
# | postgres-node-2 | 10.0.1.11   | Replica | running |  1 |         0 |
# | postgres-node-3 | 10.0.1.12   | Replica | running |  1 |         0 |
# +-----------------+-------------+---------+---------+----+-----------+
```

## 워크플로: MongoDB 샤딩 구현

### 샤드 키 선택

```javascript
// Bad shard key choices:
// - Auto-incrementing _id: All writes go to one shard (hotspot)
// - Country: Uneven distribution (US has 70% of data)
// - Timestamp: All recent writes go to one shard

// Good shard key choice: Hashed _id
// - Evenly distributes data
// - Random write distribution

// Alternative: Compound shard key for query optimization
// Shard key: { category_id: 1, product_id: 1 }

db.products.createIndex({ category_id: 1, product_id: 1 });
```

### 클러스터 아키텍처

```yaml
Config Servers (3 nodes):
  - config-1: 10.0.1.10:27019
  - config-2: 10.0.1.11:27019
  - config-3: 10.0.1.12:27019

Query Routers (mongos) (2 nodes):
  - mongos-1: 10.0.2.10:27017
  - mongos-2: 10.0.2.11:27017

Shards (3 replica sets):
  Shard 1 (shard1-rs): 10.0.3.10-12:27018
  Shard 2 (shard2-rs): 10.0.4.10-12:27018
  Shard 3 (shard3-rs): 10.0.5.10-12:27018
```

### 성능 결과

- 쿼리 지연 시간: 2.5초 → 0.4초(6배 개선)
- 쓰기 처리량: 5K ops/초 → 15K ops/초(3배 증가)
- 수평적 확장: 데이터가 증가함에 따라 더 많은 샤드를 추가할 수 있습니다.