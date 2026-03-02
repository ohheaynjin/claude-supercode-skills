---
name: sql-pro
description: 사용자가 PostgreSQL, MySQL, SQL Server 및 Oracle 플랫폼 전반에서 SQL 개발, 데이터베이스 설계, 쿼리 최적화, 성능 조정 또는 데이터베이스 관리가 필요한 경우에 사용합니다.
---
# SQL 프로

## 목적

복잡한 쿼리 설계, 성능 최적화 및 데이터베이스 아키텍처를 전문으로 하는 주요 데이터베이스 플랫폼(PostgreSQL, MySQL, SQL Server, Oracle) 전반에 걸쳐 전문적인 SQL 개발 기능을 제공합니다. 효율성과 확장성에 중점을 두고 ANSI SQL 표준, 플랫폼별 최적화 및 최신 데이터 패턴을 마스터합니다.

## 사용 시기

- 조인, CTE, 창 함수 또는 재귀 쿼리를 사용하여 복잡한 SQL 쿼리 작성
- 신규 애플리케이션을 위한 데이터베이스 스키마 설계 또는 기존 스키마 리팩토링
- 실행 계획 분석을 통한 느린 SQL 쿼리 최적화
- 서로 다른 데이터베이스 플랫폼 간 데이터 마이그레이션(MySQL → PostgreSQL)
- 저장 프로시저, 함수 또는 트리거 구현
- 고급 집계 및 창 기능을 갖춘 분석 보고서 작성
- 비즈니스 요구사항을 SQL 쿼리 로직으로 변환
- 플랫폼 간 SQL 호환성 문제(다른 방언)

## 빠른 시작

**다음과 같은 경우에 이 스킬을 호출하세요:**
- CTE, 창 함수 또는 재귀 패턴을 사용하여 복잡한 쿼리 작성
- 데이터베이스 스키마 설계 또는 리팩터링
- 실행 계획 분석을 통한 느린 쿼리 최적화
- 서로 다른 데이터베이스 플랫폼 간 데이터 마이그레이션
- 저장 프로시저, 함수 또는 트리거 구현
- 고급 집계로 분석 보고서 작성

**다음과 같은 경우에는 호출하지 마세요.**
- PostgreSQL 전용 기능 필요 → postgres-pro 사용
- MySQL 전용 관리 → 데이터베이스 관리자 사용
- 간단한 CRUD 작업 → 백엔드 개발자 사용
- ORM 쿼리 패턴 → 적절한 언어 스킬 사용

## 의사결정 프레임워크

### CTE 및 하위 쿼리 및 JOIN 결정 트리
```
Query Requirement Analysis
│
├─ Need to reference result multiple times?
│  └─ YES → Use CTE (avoids duplicate subquery evaluation)
│     WITH user_totals AS (SELECT ...)
│     SELECT * FROM user_totals WHERE ...
│     UNION ALL
│     SELECT * FROM user_totals WHERE ...
│
├─ Recursive data traversal (hierarchy, graph)?
│  └─ YES → Use Recursive CTE (ONLY option for recursion)
│     WITH RECURSIVE tree AS (
│       SELECT ... -- anchor
│       UNION ALL
│       SELECT ... FROM tree ... -- recursive
│     )
│
├─ Simple lookup or filter?
│  └─ Use JOIN (most optimizable by query planner)
│     SELECT u.*, o.total
│     FROM users u
│     JOIN orders o ON u.id = o.user_id
│
├─ Correlated subquery in WHERE clause?
│  ├─ Checking existence → Use EXISTS (stops at first match)
│  │  WHERE EXISTS (SELECT 1 FROM orders WHERE user_id = u.id)
│  │
│  └─ Value comparison → Use JOIN instead
│     -- BAD: WHERE (SELECT COUNT(*) FROM orders WHERE user_id = users.id) > 5
│     -- GOOD: JOIN (SELECT user_id, COUNT(*) as cnt FROM orders GROUP BY user_id)
│
└─ Readability vs Performance trade-off?
   ├─ Complex logic, readability critical → CTE
   │  (Easier to understand, debug, maintain)
   │
   └─ Performance critical, simple logic → Subquery or JOIN
      (Query planner can inline and optimize)
```

### 창 함수와 GROUP BY 결정 행렬 비교

| 요구사항 | 솔루션 | 예 |
|------------|----------|---------|
| 집계 + 행 수준 세부정보 필요 | 창 기능 |`SELECT name, salary, AVG(salary) OVER () as avg_salary FROM employees`|
| 집계된 결과만 필요 | 그룹 기준 |`SELECT dept, AVG(salary) FROM employees GROUP BY dept`|
| 순위/행 번호 매기기 | 윈도우 함수(ROW_NUMBER, RANK, DENSE_RANK) |`ROW_NUMBER() OVER (ORDER BY sales DESC)`|
| 누적 합계/이동 평균 | 프레임이 있는 창 기능 |`SUM(amount) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`|
| LAG/LEAD(이전/다음 행에 액세스) | 창 기능 |`LAG(price, 1) OVER (ORDER BY date) as prev_price`|
| 백분위수 / NTILE | 창 기능 |`NTILE(4) OVER (ORDER BY score) as quartile`|
| 그룹별 단순 개수/합계/평균 | GROUP BY(보다 효율적) |`SELECT category, COUNT(*) FROM products GROUP BY category`|

### 위험 신호 → Oracle에 에스컬레이션

| 관찰 | 에스컬레이션하는 이유 | 예 |
|------------|---------------|---------|
| 실행 계획의 데카르트 곱 | 의도하지 않은 교차 ​​조인으로 인해 지수 행이 발생함 | "수백만 개의 행을 반환하는 쿼리" |
| 복잡한 다단계 재귀 CTE 성능 | 고급 최적화가 필요함 | "100,000개 노드로 10개 이상의 레벨을 탐색하는 재귀 CTE" |
| 호환되지 않는 기능을 사용한 플랫폼 간 마이그레이션 | 플랫폼별 기능 매핑 | "Oracle CONNECT BY를 PostgreSQL 재귀 CTE로 마이그레이션" |
| 10개 이상의 조인과 복잡한 논리를 사용한 쿼리 | 건축 냄새, 잠재적인 재설계 | "15개 테이블을 조인하는 단일 쿼리" |
| 복잡한 시계열 논리를 사용한 시간 쿼리 | 고급 분석 패턴 | "기록 스냅샷이 포함된 SCD 유형 2" |

## 핵심 기능

### 고급 쿼리 패턴
- 공통 테이블 표현식(CTE) 및 재귀 쿼리
- 창 기능: ROW_NUMBER, RANK, LEAD, LAG, 집계 창
- 데이터 변환을 위한 PIVOT/UNPIVOT 작업
- 트리/그래프 구조에 대한 계층적 쿼리
- 시간 기반 분석을 위한 시간 쿼리

### 쿼리 최적화
- 실행계획 분석 및 해석
- 지수 선정 전략 및 커버링 지수
- 통계관리 및 유지관리
- 쿼리 힌트 및 계획 안내(필요한 경우)
- 병렬 쿼리 실행 튜닝

### 인덱스 디자인 패턴
- 클러스터형 인덱스와 비클러스터형 인덱스
- 쿼리 최적화를 위한 커버링 인덱스
- 선택적 쿼리를 위한 필터링된/부분 인덱스
- 표현식에 대한 함수 기반/인덱스
- 복합 인덱스 열 순서

## 품질 체크리스트

**쿼리 성능:**
- [ ] 실행 시간이 요구 사항을 충족합니다(OLTP: <100ms, 분석: <5s)
- [ ] 모든 복잡한 쿼리에 대해 EXPLAIN ANALYZE가 검토되었습니다.
- [ ] 대형 테이블에서는 순차적 스캔이 수행되지 않습니다(의도한 경우 제외).
- [ ] 효율적으로 활용되는 인덱스 (실행 계획 확인)
- [ ] N+1 쿼리 패턴 없음(상관 하위 쿼리 제거)

**SQL 품질:**
- [ ] SELECT에 필요한 열만(SELECT 없음 *)
- [ ] 다중 테이블 쿼리에 사용되는 명시적 테이블 별칭
- [ ] 적절한 NULL 처리(COALESCE, IS NULL 대 = NULL)
- [ ] 비교 시 데이터 유형이 일치합니다(암시적 변환 없음).
- [ ] 매개변수화된 쿼리 사용(SQL 주입 방지)

**최적화:**
- [ ] 해당되는 경우 자체 조인 대신 사용되는 창 기능
- 더 나은 NULL 처리를 위해 NOT IN 대신 [ ] EXISTS가 사용됨
- [ ] 빈번한 쿼리에 대해 제안된 커버링 인덱스
- [ ] 상관된 하위 쿼리를 제거하기 위해 쿼리를 다시 작성했습니다.

**문서:**
- [ ] 설명에 설명된 복잡한 쿼리 논리
- [ ] CTE 이름 설명 및 자체 문서화
- [ ] 예상 출력 형식이 문서화되었습니다.
- [ ] 성능 특성이 문서화됨

## 추가 리소스

- **자세한 기술 참조**: [REFERENCE.md](REFERENCE.md) 참조
- **코드 예제 및 패턴**: [EXAMPLES.md](EXAMPLES.md) 참조