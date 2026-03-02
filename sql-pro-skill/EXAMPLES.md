# SQL Pro - 코드 예제 및 패턴

## 계층적 데이터를 위한 재귀적 CTE

**시나리오**: 조직 계층 - 관리자 아래의 모든 직원 찾기
```sql
-- Create employees table
CREATE TABLE employees (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100),
  manager_id INTEGER REFERENCES employees(id),
  title VARCHAR(100),
  salary DECIMAL(10,2)
);

-- Find all employees under VP Bob (id=2), including indirect reports
WITH RECURSIVE org_tree AS (
  -- Anchor: Starting point (VP Bob himself)
  SELECT 
    id,
    name,
    manager_id,
    title,
    salary,
    0 as depth,  -- Track hierarchy depth
    ARRAY[id] as path,  -- Track path from root (prevents cycles)
    name::TEXT as hierarchy  -- Visual representation
  FROM employees
  WHERE id = 2  -- Starting point: VP Bob
  
  UNION ALL
  
  -- Recursive: Find direct reports of current level
  SELECT 
    e.id,
    e.name,
    e.manager_id,
    e.title,
    e.salary,
    ot.depth + 1,
    ot.path || e.id,  -- Append to path
    ot.hierarchy || ' > ' || e.name  -- Build visual hierarchy
  FROM employees e
  INNER JOIN org_tree ot ON e.manager_id = ot.id
  WHERE NOT (e.id = ANY(ot.path))  -- Prevent infinite loops (cycle detection)
)

SELECT 
  id,
  REPEAT('  ', depth) || name as indented_name,  -- Visual indentation
  title,
  salary,
  depth,
  hierarchy
FROM org_tree
ORDER BY path;  -- Depth-first traversal
```
## 총 개수를 사용한 페이지 매김
```sql
-- Template: Window function for pagination + total count in single query
WITH paginated_users AS (
  SELECT 
    id,
    name,
    email,
    created_at,
    COUNT(*) OVER () as total_count  -- Total count without separate query
  FROM users
  WHERE status = 'active'
  ORDER BY created_at DESC
  LIMIT 20 OFFSET 40  -- Page 3 (20 per page)
)
SELECT * FROM paginated_users;

/*
Output includes total_count in every row (no separate COUNT query needed):
id  | name  | email       | created_at | total_count
----|-------|-------------|------------|------------
123 | Alice | a@email.com | 2024-03-15 | 5432
124 | Bob   | b@email.com | 2024-03-14 | 5432
*/
```
## 조건부 집계(피벗 테이블)
```sql
-- Pivot without PIVOT syntax (works across all databases)
SELECT 
  EXTRACT(YEAR FROM sale_date) as year,
  SUM(CASE WHEN EXTRACT(QUARTER FROM sale_date) = 1 THEN amount ELSE 0 END) as q1_sales,
  SUM(CASE WHEN EXTRACT(QUARTER FROM sale_date) = 2 THEN amount ELSE 0 END) as q2_sales,
  SUM(CASE WHEN EXTRACT(QUARTER FROM sale_date) = 3 THEN amount ELSE 0 END) as q3_sales,
  SUM(CASE WHEN EXTRACT(QUARTER FROM sale_date) = 4 THEN amount ELSE 0 END) as q4_sales,
  SUM(amount) as total_sales
FROM sales
WHERE sale_date >= '2024-01-01'
GROUP BY EXTRACT(YEAR FROM sale_date);

/*
Output:
year | q1_sales | q2_sales | q3_sales | q4_sales | total_sales
-----|----------|----------|----------|----------|------------
2024 | 125000   | 145000   | 167000   | 189000   | 626000
*/
```
## 인덱스 커버리지 확인
```sql
-- Template: Check if query can use index-only scan
-- 1. Identify columns in WHERE, JOIN, ORDER BY
-- 2. Identify columns in SELECT
-- 3. Create covering index

-- Example query:
SELECT user_id, created_at, total 
FROM orders 
WHERE status = 'completed' AND created_at >= '2024-01-01'
ORDER BY created_at DESC;

-- Covering index design:
CREATE INDEX idx_orders_status_created_covering
  ON orders (status, created_at DESC)  -- Filter + sort columns
  INCLUDE (user_id, total);  -- SELECT columns (PostgreSQL)

-- MySQL equivalent:
CREATE INDEX idx_orders_status_created_covering
  ON orders (status, created_at DESC, user_id, total);

-- Verify with EXPLAIN: look for "Index Only Scan" (PostgreSQL) or "Using index" (MySQL)
```
## 안티 패턴 및 수정 사항

### 안티 패턴: 프로덕션 코드에서 SELECT *

**나쁜:**
```sql
-- Selecting all columns (even if only need 3)
SELECT * FROM users WHERE id = 123;

-- Joining with SELECT *
SELECT * FROM orders o
JOIN users u ON o.user_id = u.id
WHERE o.status = 'pending';
```
**실패하는 이유:**
- **성능**: 불필요한 데이터를 가져옵니다(네트워크 전송, 메모리 오버헤드).
- **인덱스 적용 범위**: 인덱스 전용 스캔을 사용할 수 없습니다(힙에 액세스해야 함).
- **주요 변경 사항**: 스키마 변경으로 인해 애플리케이션 코드가 중단됩니다.
- **모호성**: 조인 시 열 이름이 충돌합니다(어떤 'ID' 열이요?).

**좋음:**
```sql
-- Select only needed columns
SELECT id, email, name, created_at 
FROM users 
WHERE id = 123;

-- Explicit columns in joins (qualify with table alias)
SELECT 
  o.id as order_id,
  o.total,
  o.status,
  u.email,
  u.name
FROM orders o
JOIN users u ON o.user_id = u.id
WHERE o.status = 'pending';

-- Bonus: Can use covering index
CREATE INDEX idx_users_id_covering 
  ON users (id) 
  INCLUDE (email, name, created_at);  -- Index-only scan possible
```
### 안티 패턴: WHERE 절의 암시적 유형 변환

**나쁜:**
```sql
-- user_id is INTEGER, but comparing with string
SELECT * FROM orders WHERE user_id = '12345';

-- created_at is TIMESTAMP, but comparing with string
SELECT * FROM orders WHERE created_at = '2024-03-15';

-- phone_number is VARCHAR, but comparing with number
SELECT * FROM users WHERE phone_number = 1234567890;
```
**실패하는 이유:**
- **인덱스가 사용되지 않음**: 유형 불일치로 인해 인덱스 사용이 불가능함(전체 테이블 스캔)
- **암시적 변환 오버헤드**: 데이터베이스가 모든 행의 값을 변환합니다(느림).
- **일관되지 않은 동작**: 서로 다른 데이터베이스는 변환을 다르게 처리합니다.

**좋음:**
```sql
-- Use correct data types
SELECT * FROM orders WHERE user_id = 12345;  -- INTEGER

-- Explicit type casting when necessary
SELECT * FROM orders WHERE created_at = '2024-03-15'::DATE;

-- Or use proper timestamp
SELECT * FROM orders WHERE created_at >= '2024-03-15 00:00:00'::TIMESTAMP
  AND created_at < '2024-03-16 00:00:00'::TIMESTAMP;

-- String comparison for VARCHAR
SELECT * FROM users WHERE phone_number = '1234567890';

-- Verify index usage with EXPLAIN
EXPLAIN SELECT * FROM orders WHERE user_id = 12345;
-- Should show "Index Scan" or "Index Seek", NOT "Seq Scan"
```
## 쿼리 최적화 예
```sql
-- Before: Multiple scans, inefficient joins
SELECT o.order_id, c.customer_name, SUM(oi.quantity * oi.price) as total
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_date >= '2024-01-01'
GROUP BY o.order_id, c.customer_name;

-- After: Optimized with covering index and CTE
WITH recent_orders AS (
  SELECT order_id, customer_id, order_date
  FROM orders
  WHERE order_date >= '2024-01-01'
)
SELECT ro.order_id, c.customer_name, SUM(oi.quantity * oi.price) as total
FROM recent_orders ro
JOIN customers c ON ro.customer_id = c.customer_id
JOIN order_items oi ON ro.order_id = oi.order_id
GROUP BY ro.order_id, c.customer_name;

-- Covering index
CREATE INDEX idx_orders_date_customer ON orders(order_date, customer_id) INCLUDE (order_id);
```
