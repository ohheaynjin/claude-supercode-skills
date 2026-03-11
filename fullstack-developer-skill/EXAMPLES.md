# 풀스택 개발자 - 코드 예제 및 패턴

이 문서에는 전체 스택 개발을 위한 실제 예제, 일반적인 패턴 및 안티 패턴이 포함되어 있습니다.

## 예시 1: 전자상거래 플랫폼 개발

**시나리오:** 장바구니, 결제, 사용자 계정을 갖춘 모든 기능을 갖춘 전자상거래 플랫폼을 구축합니다.

**기술 스택:**
- **프런트엔드**: TypeScript, Redux 툴킷, Material-UI로 반응
- **백엔드**: Express, PostgreSQL, Redis 캐싱이 포함된 Node.js
- **인프라**: Docker 컨테이너, AWS 기반 Kubernetes

**주요 구현:**
1. **쇼핑 카트**: 낙관적인 업데이트가 포함된 영구 카트
2. **결제 흐름**: 결제 통합이 포함된 다단계 마법사
3. **사용자 계정**: 새로 고침 토큰을 사용한 JWT 인증
4. **관리 대시보드**: 분석을 통한 역할 기반 액세스 제어

**결과:**
- 페이지 로드 시간: < 2초
- API 응답 시간: 평균 < 100ms
- 자동 확장으로 99.9% 가동 시간
- 모바일 반응형 디자인

---

## 예시 2: 실시간 협업 도구

**시나리오:** 실시간 업데이트가 포함된 공동 문서 편집기를 개발합니다.

**기술적 아키텍처:**
1. **실시간 동기화**: 운영 혁신을 통한 WebSocket 연결
2. **문서 편집기**: 협업 커서가 포함된 서식 있는 텍스트 편집기
3. **현재 상태**: 실시간 사용자 상태 및 활동 피드
4. **댓글**: 실시간 업데이트가 포함된 스레드 댓글

**구현 하이라이트:**
- 협업을 위한 충돌 없는 복제 데이터 유형(CRDT)
- 반응형 경험을 위한 낙관적인 UI 업데이트
- 연결 풀링을 갖춘 WebSocket 서버
- 게시/구독 및 세션 관리를 위한 Redis

---

## 예시 3: SaaS 대시보드 애플리케이션

**시나리오:** 멀티 테넌트 SaaS 분석 대시보드 구축.

**다중 테넌트 아키텍처:**
1. **데이터베이스**: PostgreSQL을 사용한 행 수준 보안
2. **API**: 테넌트 인식 라우팅 및 인증
3. **프런트엔드**: 구성 가능한 위젯이 포함된 대시보드
4. **청구**: 구독 관리와 스트라이프 통합

**엔터프라이즈 기능:**
- 역할 기반 액세스 제어(RBAC)
- 감사 로깅 및 규정 준수 보고
- SAML/OIDC와 SSO 통합
- 맞춤형 브랜딩 및 화이트 라벨링

---

## 일반적인 패턴

### 패턴 1: 인증이 포함된 API 게이트웨이

```javascript
// API Gateway Setup
import express from 'express';
import { createProxyMiddleware } from 'http-proxy-middleware';
import jwt from 'jsonwebtoken';

const app = express();

// Authentication middleware
const authMiddleware = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  
  if (!token) {
    return res.status(401).json({ error: 'No token provided' });
  }
  
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    return res.status(401).json({ error: 'Invalid token' });
  }
};

// Route to user service
app.use('/api/users', authMiddleware, createProxyMiddleware({
  target: 'http://user-service:3001',
  changeOrigin: true,
  pathRewrite: { '^/api/users': '' }
}));

// Route to product service
app.use('/api/products', authMiddleware, createProxyMiddleware({
  target: 'http://product-service:3002',
  changeOrigin: true,
  pathRewrite: { '^/api/products': '' }
}));
```

### 패턴 2: TypeScript를 사용한 저장소 패턴

```typescript
// Repository Interface
interface IRepository<T> {
  findAll(): Promise<T[]>;
  findById(id: string): Promise<T | null>;
  create(entity: Partial<T>): Promise<T>;
  update(id: string, entity: Partial<T>): Promise<T>;
  delete(id: string): Promise<boolean>;
}

// User Repository Implementation
class UserRepository implements IRepository<User> {
  constructor(private db: Database) {}

  async findAll(): Promise<User[]> {
    return this.db.query('SELECT * FROM users');
  }

  async findById(id: string): Promise<User | null> {
    const [user] = await this.db.query('SELECT * FROM users WHERE id = ?', [id]);
    return user || null;
  }

  async create(userData: Partial<User>): Promise<User> {
    const result = await this.db.query(
      'INSERT INTO users (email, name) VALUES (?, ?)',
      [userData.email, userData.name]
    );
    return this.findById(result.insertId);
  }

  async update(id: string, userData: Partial<User>): Promise<User> {
    await this.db.query(
      'UPDATE users SET email = ?, name = ? WHERE id = ?',
      [userData.email, userData.name, id]
    );
    return this.findById(id);
  }

  async delete(id: string): Promise<boolean> {
    const result = await this.db.query('DELETE FROM users WHERE id = ?', [id]);
    return result.affectedRows > 0;
  }
}
```

### 패턴 3: API 호출을 위한 사용자 정의 React Hook

```typescript
// useApi Hook with Error Handling and Caching
function useApi<T>(
  endpoint: string,
  options: { immediate?: boolean; cache?: boolean } = {}
) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(options.immediate !== false);
  const [error, setError] = useState<Error | null>(null);

  const fetchData = useCallback(async (params?: Record<string, any>) => {
    setLoading(true);
    setError(null);

    try {
      const queryString = params 
        ? '?' + new URLSearchParams(params).toString() 
        : '';
      const response = await fetch(`/api${endpoint}${queryString}`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const result = await response.json();
      setData(result);
      return result;
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Unknown error'));
      throw err;
    } finally {
      setLoading(false);
    }
  }, [endpoint]);

  useEffect(() => {
    if (options.immediate !== false) {
      fetchData();
    }
  }, [fetchData, options.immediate]);

  return { data, loading, error, refetch: fetchData };
}

// Usage
function ProductList() {
  const { data: products, loading, error, refetch } = useApi<Product[]>('/products');
  
  if (loading) return <Spinner />;
  if (error) return <ErrorMessage error={error} retry={refetch} />;
  
  return <ProductGrid products={products} />;
}
```

### 패턴 4: 대체 UI의 오류 경계

```typescript
// Error Boundary Component
class ErrorBoundary extends React.Component<
  { children: React.ReactNode; fallback?: React.ReactNode },
  { hasError: boolean; error?: Error }
> {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
    // Send to error tracking service
    trackError(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div className="error-container">
          <h2>Something went wrong</h2>
          <p>{this.state.error?.message}</p>
          <button onClick={() => window.location.reload()}>
            Refresh Page
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}
```

---

## 안티 패턴 및 수정 사항

### 안티 패턴 1: N+1 쿼리 문제

**문제:**```javascript
// BAD: N+1 queries
async function getOrdersWithItems() {
  const orders = await Order.findAll();
  
  // This creates N additional queries!
  for (const order of orders) {
    order.items = await OrderItem.findAll({ 
      where: { orderId: order.id } 
    });
  }
  
  return orders;
}
```

**해결책:**```javascript
// GOOD: Single query with join/include
async function getOrdersWithItems() {
  return Order.findAll({
    include: [{
      model: OrderItem,
      as: 'items'
    }]
  });
}
```

### 안티 패턴 2: 소품 드릴링

**문제:**```jsx
// BAD: Passing props through many levels
function App({ user }) {
  return <Layout user={user} />;
}

function Layout({ user }) {
  return <Sidebar user={user} />;
}

function Sidebar({ user }) {
  return <UserInfo user={user} />;
}

function UserInfo({ user }) {
  return <span>{user.name}</span>;
}
```

**해결책:**```jsx
// GOOD: Use Context for deeply nested data
const UserContext = createContext(null);

function App({ user }) {
  return (
    <UserContext.Provider value={user}>
      <Layout />
    </UserContext.Provider>
  );
}

function UserInfo() {
  const user = useContext(UserContext);
  return <span>{user.name}</span>;
}
```

### 안티 패턴 3: API 호출에서 오류 처리 누락

**문제:**```javascript
// BAD: No error handling
async function fetchUser(id) {
  const response = await fetch(`/api/users/${id}`);
  return response.json();
}
```

**해결책:**```javascript
// GOOD: Comprehensive error handling
async function fetchUser(id) {
  try {
    const response = await fetch(`/api/users/${id}`);
    
    if (!response.ok) {
      if (response.status === 404) {
        throw new NotFoundError(`User ${id} not found`);
      }
      if (response.status === 401) {
        throw new UnauthorizedError('Authentication required');
      }
      throw new ApiError(`API error: ${response.status}`);
    }
    
    return response.json();
  } catch (error) {
    if (error instanceof TypeError) {
      throw new NetworkError('Network connection failed');
    }
    throw error;
  }
}
```

### 안티 패턴 4: 하드코딩된 구성

**문제:**```javascript
// BAD: Hardcoded values
const API_URL = 'http://localhost:3000/api';
const DB_HOST = 'localhost';
const JWT_SECRET = 'mysecret123';
```

**해결책:**```javascript
// GOOD: Environment variables with validation
const config = {
  apiUrl: process.env.API_URL || 'http://localhost:3000/api',
  database: {
    host: process.env.DB_HOST,
    port: parseInt(process.env.DB_PORT || '5432'),
    name: process.env.DB_NAME,
  },
  jwt: {
    secret: process.env.JWT_SECRET,
    expiresIn: process.env.JWT_EXPIRES_IN || '1d',
  }
};

// Validate required config
const required = ['DB_HOST', 'DB_NAME', 'JWT_SECRET'];
for (const key of required) {
  if (!process.env[key]) {
    throw new Error(`Missing required environment variable: ${key}`);
  }
}

export default config;
```

---

## 통합 체크리스트

### 전체 스택 기능을 배포하기 전

- [ ] 프런트엔드 및 백엔드 API 계약이 일치합니다.
- [ ] 오류 처리에는 모든 극단적인 경우가 포함됩니다.
- [ ] 인증/승인 테스트됨
- [ ] 데이터베이스 마이그레이션이 적용되었습니다.
- [ ] 환경 변수가 구성됨
- [ ] CORS 설정이 확인되었습니다.
- [ ] 비율 제한이 적용됨
- [ ] 로깅 및 모니터링 활성화됨
- [ ] 단위 및 통합 테스트 통과
- [ ] 부하 상태에서 성능 테스트