# 백엔드 API 패턴

## 빠른 시작

### REST API 모범 사례

#### 리소스 이름 지정

자원에는 복수 명사를 사용하십시오.
```
GET    /users          # List all users
GET    /users/{id}     # Get specific user
POST   /users          # Create user
PUT    /users/{id}     # Update user
DELETE /users/{id}     # Delete user
```
#### HTTP 상태 코드

-`200 OK`- 요청 성공
-`201 Created`- 리소스가 성공적으로 생성되었습니다.
-`204 No Content`- 성공했지만 콘텐츠가 반환되지 않았습니다.
-`400 Bad Request`- 잘못된 요청 데이터
-`401 Unauthorized`- 인증이 필요합니다
-`403 Forbidden`- 권한이 부족합니다.
-`404 Not Found`- 리소스를 찾을 수 없습니다.
-`409 Conflict`- 리소스가 이미 존재합니다.
-`422 Unprocessable Entity`- 유효성 검사 실패
-`429 Too Many Requests`- 비율 제한을 초과했습니다.
-`500 Internal Server Error`- 서버 오류

#### 요청/응답 형식

**요청 예시:**
```json
{
  "data": {
    "type": "users",
    "attributes": {
      "email": "user@example.com",
      "name": "John Doe"
    }
  }
}
```
**응답 예:**
```json
{
  "data": {
    "type": "users",
    "id": "123",
    "attributes": {
      "email": "user@example.com",
      "name": "John Doe",
      "createdAt": "2024-01-01T00:00:00Z"
    }
  },
  "meta": {
    "page": 1,
    "pageSize": 20,
    "total": 100
  }
}
```
### 페이지 매김 전략

#### 오프셋 기반 페이지 매김
```
GET /users?page=1&pageSize=20
```
#### 커서 기반 페이지 매김
```
GET /users?cursor=abc123&limit=20
```
#### 키 세트 페이지 매김
```
GET /users?lastId=123&limit=20
```
### 필터링 및 정렬

**쿼리 매개변수:**
```
GET /users?filter[status]=active&sort=name,desc
```
**복잡한 필터:**
```
GET /users?filter[age][gte]=18&filter[age][lte]=65
```
### 버전 관리 전략

#### URL 버전 관리
```
/api/v1/users
/api/v2/users
```
#### 헤더 버전 관리
```
Accept: application/vnd.api.v1+json
```
#### 쿼리 매개변수 버전 관리
```
/api/users?version=1
```
## 일반적인 패턴

### 저장소 패턴
```typescript
interface UserRepository {
  findById(id: number): Promise<User | null>;
  findAll(options?: FindOptions): Promise<User[]>;
  create(user: UserCreate): Promise<User>;
  update(id: number, user: UserUpdate): Promise<User>;
  delete(id: number): Promise<void>;
}

class SQLUserRepository implements UserRepository {
  async findById(id: number): Promise<User | null> {
    return db.users.findUnique({ where: { id } });
  }
}
```
### 서비스 레이어 패턴
```typescript
class UserService {
  constructor(
    private userRepository: UserRepository,
    private emailService: EmailService
  ) {}

  async createUser(data: UserCreate): Promise<User> {
    const existing = await this.userRepository.findByEmail(data.email);
    if (existing) {
      throw new ConflictError('Email already exists');
    }

    const user = await this.userRepository.create(data);
    await this.emailService.sendWelcomeEmail(user);

    return user;
  }
}
```
### 작업 단위 패턴
```python
class UnitOfWork:
    def __init__(self, session):
        self.session = session
        self.users = UserRepository(session)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.session.commit()
        else:
            self.session.rollback()

# Usage
with UnitOfWork(session) as uow:
    user = uow.users.create(user_data)
    uow.users.update(user.id, updates)
```
### CQRS(명령어 쿼리 책임 분리)
```typescript
// Command (Write)
class CreateUserCommand {
  constructor(
    public email: string,
    public name: string
  ) {}
}

// Query (Read)
class GetUserQuery {
  constructor(public id: number) {}
}

// Command Handler
class CreateUserCommandHandler {
  async execute(command: CreateUserCommand): Promise<void> {
    await this.userRepository.create(command);
  }
}

// Query Handler
class GetUserQueryHandler {
  async execute(query: GetUserQuery): Promise<User | null> {
    return this.userRepository.findById(query.id);
  }
}
```
## 인증 패턴

### JWT 토큰 구조
```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "user_id",
    "email": "user@example.com",
    "role": "admin",
    "iat": 1516239022,
    "exp": 1516242622
  }
}
```
### 토큰 새로고침 흐름
```
Client                    Server
  |                         |
  |  POST /refresh         |
  |  refresh_token         |
  |----------------------->|
  |                         |
  |  access_token          |
  |  refresh_token         |
  |<-----------------------|
```
### 속도 제한
```typescript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP'
});

app.use('/api/', limiter);
```
## 오류 처리

### 표준 오류 응답
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ],
    "requestId": "abc-123-def",
    "timestamp": "2024-01-01T00:00:00Z"
  }
}
```
### 전역 오류 처리기
```typescript
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  const statusCode = err instanceof AppError ? err.statusCode : 500;

  res.status(statusCode).json({
    error: {
      code: err.name,
      message: err.message,
      ...(process.env.NODE_ENV === 'development' && {
        stack: err.stack
      })
    }
  });
});
```
## 데이터베이스 패턴

### 소프트 삭제
```typescript
@Entity()
export class User {
  id: number;
  email: string;
  deletedAt: Date | null;

  @BeforeUpdate()
  softDelete() {
    this.deletedAt = new Date();
  }
}
```
### 감사
```typescript
@Entity()
export class AuditLog {
  id: number;
  entity: string;
  entityId: number;
  action: 'CREATE' | 'UPDATE' | 'DELETE';
  changes: Record<string, any>;
  userId: number;
  timestamp: Date;
}
```
### 낙관적 잠금
```typescript
@Entity()
export class Product {
  @VersionColumn()
  version: number;
}

// Update with version check
await repository.update(
  { id: 1, version: 2 },
  { name: 'New Name' }
);
```
## 성능 패턴

### 캐싱 전략
```typescript
import Redis from 'ioredis';

const redis = new Redis();

async function getUser(id: number): Promise<User> {
  const cacheKey = `user:${id}`;

  // Try cache first
  const cached = await redis.get(cacheKey);
  if (cached) {
    return JSON.parse(cached);
  }

  // Fetch from database
  const user = await userRepository.findById(id);

  // Set cache with TTL
  await redis.setex(cacheKey, 3600, JSON.stringify(user));

  return user;
}
```
### 데이터베이스 연결 풀링
```typescript
import { Pool } from 'pg';

const pool = new Pool({
  host: process.env.DB_HOST,
  port: 5432,
  database: process.env.DB_NAME,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  max: 20, // Maximum pool size
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000
});
```
### 일괄 작업
```typescript
// Instead of multiple individual inserts
for (const user of users) {
  await userRepository.create(user);
}

// Use batch insert
await userRepository.createMany(users);
```
## 보안 패턴

### 입력 삭제
```typescript
import validator from 'validator';

function sanitizeInput(input: string): string {
  return validator.escape(input.trim());
}
```
### SQL 주입 방지
```typescript
// BAD
const query = `SELECT * FROM users WHERE id = ${userId}`;

// GOOD
const query = 'SELECT * FROM users WHERE id = $1';
const result = await db.query(query, [userId]);
```
### CORS 구성
```typescript
const corsOptions = {
  origin: process.env.ALLOWED_ORIGINS?.split(',') || [],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
};

app.use(cors(corsOptions));
```
## 테스트 패턴

### 단위 테스트
```typescript
describe('UserService', () => {
  let service: UserService;
  let mockRepo: jest.Mocked<UserRepository>;

  beforeEach(() => {
    mockRepo = createMockUserRepository();
    service = new UserService(mockRepo);
  });

  it('should create user', async () => {
    const user = await service.createUser(userData);

    expect(mockRepo.create).toHaveBeenCalledWith(userData);
    expect(user.email).toBe(userData.email);
  });
});
```
### 통합 테스트
```typescript
describe('User API', () => {
  let app: Application;

  beforeAll(async () => {
    app = createApp();
    await setupDatabase();
  });

  afterAll(async () => {
    await cleanupDatabase();
  });

  it('should create user via API', async () => {
    const response = await request(app)
      .post('/api/v1/users')
      .send(userData)
      .expect(201);

    expect(response.body.data.email).toBe(userData.email);
  });
});
```
## 모니터링 및 관찰 가능성

### 구조화된 로깅
```typescript
logger.info('User created', {
  userId: user.id,
  email: user.email,
  action: 'CREATE',
  timestamp: new Date().toISOString()
});
```
### 측정항목 수집
```typescript
import { Counter, Histogram } from 'prom-client';

const httpRequestDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests',
  labelNames: ['method', 'route', 'status_code']
});

app.use((req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;
    httpRequestDuration
      .labels(req.method, req.route?.path || '', res.statusCode.toString())
      .observe(duration);
  });
  next();
});
```
### 상태 점검
```typescript
app.get('/health', async (req, res) => {
  const health = {
    status: 'ok',
    timestamp: new Date().toISOString(),
    checks: {
      database: await checkDatabase(),
      redis: await checkRedis(),
      api: await checkExternalAPI()
    }
  };

  const isHealthy = Object.values(health.checks).every(check => check.status === 'ok');
  res.status(isHealthy ? 200 : 503).json(health);
});
```
## 문제 해결

### 일반적인 문제

#### 연결 풀 고갈
- **증상**: 느린 응답, 시간 초과
- **해결책**: 풀 크기 늘리기, 연결 수명 줄이기, 연결 시간 초과 추가

#### 메모리 누수
- **증상**: 시간이 지남에 따라 메모리 사용량이 증가합니다.
- **해결책**: 힙 스냅샷으로 프로파일링, 이벤트 리스너 확인, 연결 종료

#### N+1 쿼리 문제
- **증상**: 단일 요청에 대해 데이터베이스 쿼리가 많이 발생함
- **해결책**: 즉시 로딩, 일괄 쿼리 사용, GraphQL DataLoader 패턴 구현

#### 느린 API 응답
- **증상**: 응답 시간이 길다
- **해결책**: 캐싱 추가, 쿼리 최적화, 데이터베이스 인덱스 사용, 페이지 매김 구현