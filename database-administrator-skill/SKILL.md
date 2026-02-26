---
name: database-administrator
description: "PostgreSQL, MySQL, MongoDB 및 엔터프라이즈 데이터베이스 시스템에 대한 전문 지식을 갖춘 수석 데이터베이스 관리자입니다. 프로덕션 환경을 위한 고가용성 아키텍처, 성능 조정, 백업 전략 및 데이터베이스 보안을 전문으로 합니다."
---
# 데이터베이스 관리자

## 목적

PostgreSQL, MySQL, MongoDB 및 엔터프라이즈 데이터베이스를 포함한 프로덕션 데이터베이스 시스템에 대한 고위급 데이터베이스 관리 전문 지식을 제공합니다. 미션 크리티컬 환경을 위한 고가용성 아키텍처, 성능 튜닝, 백업 전략, 재해 복구 및 데이터베이스 보안을 전문으로 합니다.

## 사용 시기

- 고가용성 및 재해 복구 기능을 갖춘 프로덕션 데이터베이스 설정
- 데이터베이스 성능 최적화(느린 쿼리, 인덱싱, 구성 튜닝)
- 백업 및 복구 전략 구현(PITR, 교차 지역 백업)
- 데이터베이스(PostgreSQL, MySQL, MongoDB)를 클라우드로 또는 버전 간 마이그레이션
- 데이터베이스 보안 강화(암호화, 접근통제, 감사로깅)
- 데이터베이스 문제 해결(잠금, 복제 지연, 손상)
- 확장성과 신뢰성을 위한 데이터베이스 아키텍처 설계

## 빠른 시작

**다음과 같은 경우에 이 스킬을 호출하세요:**
- 고가용성 및 재해 복구 기능을 갖춘 프로덕션 데이터베이스 설정
- 데이터베이스 성능 최적화(느린 쿼리, 인덱싱, 구성 튜닝)
- 백업 및 복구 전략 구현(PITR, 교차 지역 백업)
- 데이터베이스(PostgreSQL, MySQL, MongoDB)를 클라우드로 또는 버전 간 마이그레이션
- 데이터베이스 보안 강화(암호화, 접근통제, 감사로깅)
- 데이터베이스 문제 해결(잠금, 복제 지연, 손상)

**다음과 같은 경우에는 호출하지 마세요.**
- 애플리케이션 수준 ORM 쿼리에만 최적화가 필요합니다(백엔드 개발자 사용).
- 데이터 파이프라인 개발(ETL/ELT용 데이터 엔지니어 사용)
- 분석을 위한 데이터 모델링 및 스키마 설계(데이터 엔지니어 활용)
- 신규 프로젝트를 위한 데이터베이스 선택(전략을 위해 클라우드 아키텍트 사용)
- 간단한 SQL 쿼리 또는 데이터 분석(data-analyst 사용)

## 의사결정 프레임워크

### 데이터베이스 선택

| 사용 사례 | 데이터베이스 | 왜 |
|----------|----------|-----|
| **트랜잭션(OLTP)** | 포스트그레SQL | ACID, 확장, JSON 지원 |
| **읽기량이 많은 웹 앱** | MySQL/마리아DB | 빠른 읽기, 성숙한 복제 |
| **유연한 스키마** | 몽고DB | 문서 모델, 수평 규모 |
| **키-값 캐시** | 레디스 | 밀리초 미만의 대기 시간, 데이터 구조 |
| **시계열 데이터** | 타임스케일DB/인플럭스DB | 시간 기반 쿼리에 최적화됨 |
| **분석(OLAP)** | 눈송이/BigQuery | 기둥형, 대규모 |

### 고가용성 아키텍처
```
├─ Single Region HA?
│   ├─ Managed service → RDS Multi-AZ / Cloud SQL HA
│   │   Pros: Automatic failover, managed backups
│   │   Cost: 2x compute (standby instance)
│   │
│   └─ Self-managed → Patroni + etcd (PostgreSQL)
│       Pros: Full control, no vendor lock-in
│       Cost: Operational overhead
│
├─ Multi-Region HA?
│   ├─ Active-Passive → Cross-region read replicas
│   │   Pros: Simple, low cost
│   │   Cons: Manual failover, data lag
│   │
│   └─ Active-Active → CockroachDB / Spanner
│       Pros: True global distribution
│       Cons: Complexity, cost
│
└─ Horizontal Scaling?
    ├─ Read scaling → Read replicas
    ├─ Write scaling → Sharding (MongoDB, Vitess)
    └─ Both → Distributed SQL (CockroachDB, TiDB)
```
### 백업 전략 매트릭스

| RPO 요구 사항 | 전략 | 구현 |
|----|----------|---|
| **< 1분** | 동기식 복제 | Patroni 동기화 모드 |
| **< 5분** | 지속적인 WAL 아카이빙 | pg_basebackup + WAL-G |
| **< 1시간** | 자동 스냅샷 | RDS 자동 백업 |
| **< 24시간** | 일일 백업 | pg_dump + S3 |

### 성능 조정 우선순위

1. **쿼리 최적화**(가장 큰 영향, 최저 비용)
2. **인덱싱 전략**(보통의 노력, 높은 영향력)
3. **구성 튜닝**(일회성, 중간 정도의 영향)
4. **하드웨어 업그레이드**(높은 비용, 최후의 수단)

## 품질 체크리스트

### 생산 준비
- [ ] 고가용성 구성(다중 AZ 또는 다중 지역)
- [ ] 자동 백업 활성화됨(일일 + 연속 WAL)
- [ ] 백업 복원 테스트(월간 재해 복구 훈련)
- [ ] 연결 풀링 구성됨(PgBouncer/ProxySQL)
- [ ] 모니터링 및 경고 활성화(느린 쿼리, 복제 지연)

### 성능
- [ ] 모든 쿼리 패턴에 대해 생성된 인덱스
- [ ] 최신 테이블 통계(autovacuum 조정됨)
- [ ] 쿼리 계획 검토됨(대형 테이블에서는 전체 테이블 스캔 없음)
- [ ] 연결 풀링 최적화(최소/최대 풀 크기)
- [ ] 데이터베이스 구성 조정(shared_buffers, work_mem)

### 보안
- [ ] 미사용 암호화 활성화됨
- [ ] 전송 중 암호화(SSL/TLS) 시행
- [ ] 최소 권한 액세스(응용 프로그램에 대한 수퍼유저 없음)
- [ ] 감사 로깅 활성화(로그인 실패, DDL 변경)
- [ ] 정기 보안 패치 예정

### 재해 복구
- [ ] RTO/RPO 문서화 및 테스트 완료
- [ ] 지역 간 백업이 활성화되었습니다.
- [ ] 장애 조치 절차가 문서화되고 테스트되었습니다.
- [ ] 데이터 보존 정책 시행
- [ ] 특정 시점 복구 검증됨

## 추가 리소스

- **자세한 기술 참조**: [REFERENCE.md](REFERENCE.md) 참조
- **코드 예제 및 패턴**: [EXAMPLES.md](EXAMPLES.md) 참조