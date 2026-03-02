---
name: postgres-pro
description: 사용자에게 PostgreSQL 데이터베이스 관리, 성능 최적화, 고가용성 설정, 백업/복구 또는 고급 PostgreSQL 기능 구현이 필요할 때 사용합니다.
---
# 포스트그레SQL 프로페셔널

## 목적

데이터베이스 관리, 성능 최적화 및 고급 기능 구현을 전문으로 하는 포괄적인 PostgreSQL 전문 지식을 제공합니다. 고가용성 및 고급 확장 기능을 통해 PostgreSQL 배포에 대한 최대 안정성, 성능 및 확장성을 달성하는 데 탁월합니다.

## 사용 시기

- 필요한 PostgreSQL 관련 기능(JSONB, 전체 텍스트 검색, PostGIS, pgVector)
- 스트리밍 또는 논리적 복제 설정
- PostgreSQL 확장 구현
- PostgreSQL 관련 문제 해결
- PostgreSQL 구성 최적화
- 파티셔닝 및 고가용성 구현

## 빠른 시작

**다음과 같은 경우에 이 스킬을 호출하세요:**
- 필요한 PostgreSQL 관련 기능(JSONB 인덱싱, 전체 텍스트 검색, PostGIS, pgVector)
- PostgreSQL에 대한 스트리밍 복제 또는 논리적 복제 설정
- PostgreSQL 확장 구현(pg_trgm, PostGIS, timescaledb, pg_partman)
- PostgreSQL 관련 문제 해결(autovacuum, bloat, WAL 아카이빙)
- PostgreSQL 구성 최적화(shared_buffers, work_mem, Vacuum 설정)
- PostgreSQL 파티셔닝 구현(선언적 파티셔닝, 제약 조건 제외)
- PostgreSQL 고가용성 설정(Patroni, repmgr, pgpool-II)
- GIN 인덱스를 이용한 JSONB 스키마 및 쿼리 최적화 설계

**다음과 같은 경우에는 호출하지 마세요.**
- 일반 SQL 쿼리 작성(ANSI SQL 쿼리에는 sql-pro 사용)
- 크로스 플랫폼 데이터베이스 최적화(일반 튜닝에는 데이터베이스 최적화 도구 사용)
- MySQL 또는 SQL Server 특정 기능(플랫폼 특정 기술 사용)
- 데이터베이스 관리 기본(사용자, 권한 - 데이터베이스 관리자 사용)
- PostgreSQL 관련 기능 없이 간단한 쿼리 최적화
- ORM 쿼리 패턴(ORM 전문 지식을 갖춘 백엔드 개발자 사용)

## 핵심 기능

### PostgreSQL 아키텍처
- 프로세스 아키텍처 및 메모리 구성
- WAL 메커니즘 및 MVCC 구현
- 스토리지 레이아웃 및 버퍼 관리
- 잠금 관리 및 백그라운드 작업자

### 고급 기능
- GIN 인덱스를 사용한 JSONB 최적화
- tsVector 및 GIN 인덱스를 사용한 전체 텍스트 검색
- PostGIS 공간 쿼리 및 인덱싱
- 시계열 데이터 처리 및 파티셔닝
- 외부 데이터 래퍼 및 데이터베이스 간 쿼리
- 병렬 쿼리 및 JIT 컴파일

### 성능 튜닝
- 구성 최적화(메모리, 연결, 체크포인트)
- 쿼리 최적화 및 실행 계획 분석
- 인덱스 전략 및 인덱스 사용량 모니터링
- 진공 튜닝 및 Autovacuum 구성
- 연결 풀링 및 병렬 실행

### 복제 전략
- 스트리밍 복제 및 논리적 복제
- 동기식 설정 및 계단식 복제본
- 지연된 복제본 및 장애 조치 자동화
- 로드 밸런싱 및 충돌 해결

### 백업 및 복구
- pg_dump 전략 및 물리적 백업
- WAL 보관 및 PITR 설정
- 백업 검증 및 복구 테스트
- 자동화 스크립트 및 보존 정책

## 의사결정 프레임워크

### JSONB 지수 전략
```
JSONB Query Pattern Analysis
│
├─ Containment queries (@> operator)?
│   └─ Use GIN with jsonb_path_ops
│       CREATE INDEX idx ON table USING GIN (column jsonb_path_ops);
│       • 2-3x smaller than default GIN
│       • Faster for @> containment checks
│       • Does NOT support key existence (?)
│
├─ Key existence queries (? or ?| or ?& operators)?
│   └─ Use default GIN operator class
│       CREATE INDEX idx ON table USING GIN (column);
│       • Supports all JSONB operators
│       • Larger index size
│
├─ Specific path frequently queried?
│   └─ Use expression index
│       CREATE INDEX idx ON table ((column->>'key'));
│       • Most efficient for specific path
│       • B-tree allows range queries
│
└─ Full document search needed?
    └─ Combine GIN + expression indexes
        • GIN for flexible queries
        • Expression for hot paths
```
### 복제 전략 선택

| 요구사항 | 전략 | 구성 |
|------------|----------|---------------|
| 스케일링 읽기 | 스트리밍(비동기) | 다중 읽기 복제본 |
| 데이터 손실 없음 | 스트리밍(동기화) | synchronous_commit = 켜짐 |
| 테이블 수준 복제 | 논리적 | 출판/구독 작성 |
| 버전 간 업그레이드 | 논리적 | 새 버전으로 복제 |
| 재해 복구 | 스트리밍 + WAL 아카이브 | PITR 기능 |
| 지연된 회복 | 지연된 복제 | Recovery_min_apply_delay |

## 품질 체크리스트

**성능:**
- [ ] 쿼리 성능 목표 충족(OLTP <50ms, Analytics <2s)
- [ ] 모든 중요한 쿼리에 대해 EXPLAIN ANALYZE를 검토했습니다.
- [ ] JSONB, 배열, 전체 텍스트 쿼리에 사용되는 GIN/GiST 인덱스
- [ ] 시계열 데이터가 포함된 10GB가 넘는 테이블에 대해 분할 구현
- [ ] 캐시 적중률 >95%(shared_buffers + OS 캐시)
- [ ] 연결 풀링 구현됨(PgBouncer 또는 응용 프로그램 풀)

**구성:**
- [ ] shared_buffers = RAM의 25%
- [ ] Effective_cache_size = RAM의 75%
- [ ] work_mem이 워크로드에 맞춰 조정되었습니다(EXPLAIN에 임시 파일 유출이 없음).
- [ ] Autovacuum 구성(대형 테이블의 경우 scale_factor ≤0.05)
- [ ] max_connections 적절함(또는 PgBouncer 사용)
- [ ] PITR에 대해 WAL 보관이 활성화되었습니다.

**복제(해당되는 경우):**
- [ ] 복제 슬롯 생성(WAL 삭제 방지)
- [ ] 복제 지연 <500ms(P95)
- [ ] pg_stat_replication 모니터링됨(sync_state, replay_lag)
- [ ] 페일오버 테스트됨(복제본을 기본으로 승격)
- [ ] 복제 액세스용으로 구성된 pg_hba.conf

**확장:**
- [ ] 필수 확장 설치됨(pg_trgm, PostGIS, pgVector 등)
- [ ] PostgreSQL 버전과 호환되는 확장 버전
- [ ] JSONB, tsVector, 트라이그램용으로 생성된 GIN 인덱스
- [ ] 적절한 언어 사전으로 구성된 전체 텍스트 검색

**JSONB(사용된 경우):**
- [ ] GIN 인덱스 생성됨(포함 쿼리의 경우 jsonb_path_ops)
- [ ] 자주 쿼리되는 경로에 대한 표현식 인덱스
- [ ] 애플리케이션의 JSONB 검증(jsonschema 또는 사용자 정의)
- [ ] 깊게 중첩된 JSONB 없음(>3 수준 → 정규화 고려)

**모니터링:**
- [ ] 느린 쿼리 로그 구성(log_min_duration_statement = 200ms)
- [ ] pg_stat_statements 설치 및 모니터링
- [ ] Autovacuum 진행 상황 모니터링(pg_stat_progress_vacuum)
- [ ] 테이블 팽창이 모니터링됨(<15% 데드 튜플)
- [ ] 복제 지연 경고가 구성되었습니다(<1초 임계값).

## 추가 리소스

- **자세한 기술 참조**: [REFERENCE.md](REFERENCE.md) 참조
- **코드 예제 및 패턴**: [EXAMPLES.md](EXAMPLES.md) 참조