# 백엔드 프레임워크 가이드

## Node.js / TypeScript

### 익스프레스.js

#### 빠른 시작
```bash
npm init -y
npm install express cors helmet dotenv
npm install -D typescript @types/node @types/express
npx tsc --init
```
#### 기본 응용 프로그램
```typescript
import express, { Application, Request, Response } from 'express';

const app: Application = express();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.get('/', (req: Request, res: Response) => {
  res.json({ message: 'Hello World' });
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
```
#### 미들웨어 스택
```typescript
import helmet from 'helmet';
import cors from 'cors';
import compression from 'compression';

app.use(helmet());
app.use(cors());
app.use(compression());
app.use(express.json());
app.use(morgan('combined'));
```
#### 파일 구조
```
src/
├── index.ts              # Entry point
├── config/               # Configuration
├── controllers/          # Request handlers
├── services/             # Business logic
├── repositories/         # Data access
├── middleware/           # Express middleware
├── models/               # Data models
├── routes/               # Route definitions
├── utils/                # Utilities
└── types/                # TypeScript types
```
### NestJS

#### 빠른 시작
```bash
npm i -g @nestjs/cli
nest new project-name
cd project-name
npm run start:dev
```
#### 모듈 구조
```typescript
@Module({
  imports: [TypeOrmModule.forFeature([User])],
  controllers: [UserController],
  providers: [UserService],
  exports: [UserService]
})
export class UserModule {}
```
#### 의존성 주입
```typescript
@Injectable()
export class UserService {
  constructor(
    @InjectRepository(User)
    private userRepository: Repository<User>,
    private emailService: EmailService
  ) {}

  async findAll(): Promise<User[]> {
    return this.userRepository.find();
  }
}
```
## 파이썬 / FastAPI

### 빠른 시작
```bash
pip install fastapi uvicorn
uvicorn main:app --reload
```
### 기본 응용 프로그램
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```
### 프로젝트 구조
```
app/
├── __init__.py
├── main.py              # Application entry
├── api/                 # API routes
│   ├── __init__.py
│   └── v1/
│       ├── __init__.py
│       └── endpoints/
├── core/                # Core functionality
│   ├── config.py
│   ├── security.py
│   └── deps.py
├── models/              # SQLAlchemy models
├── schemas/             # Pydantic schemas
├── services/            # Business logic
├── crud/                # Database operations
└── utils/               # Utilities
```
### 의존성 주입
```python
from fastapi import Depends
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/")
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return crud.create_user(db, user)
```
### Pydantic 모델
```python
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserResponse(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
```
## 파이썬/장고

### 빠른 시작
```bash
pip install django djangorestframework
django-admin startproject project
cd project
python manage.py startapp api
```
### 프로젝트 구조
```
project/
├── manage.py
├── config/              # Configuration
│   ├── __init__.py
│   ├── settings/
│   ├── urls.py
│   └── wsgi.py
└── api/                 # Apps
    ├── __init__.py
    ├── models.py
    ├── serializers.py
    ├── views.py
    └── urls.py
```
### Django REST 프레임워크
```python
# serializers.py
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']

# views.py
from rest_framework import viewsets

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# urls.py
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet)
```
### 설정 구성
```python
# settings/base.py
class Base:
    SECRET_KEY = env('SECRET_KEY')
    DEBUG = False

# settings/development.py
from .base import Base

class Development(Base):
    DEBUG = True
    DATABASES = {...}

# settings/production.py
from .base import Base

class Production(Base):
    DEBUG = False
    ALLOWED_HOSTS = ['example.com']
```
## 자바/스프링부트

### 빠른 시작
```bash
# Using Spring Initializr
curl https://start.spring.io/starter.zip \
  -d dependencies=web,data-jpa,postgresql \
  -d type=maven-project \
  -d bootVersion=3.1.5 \
  -o project.zip

unzip project.zip
cd project
./mvnw spring-boot:run
```
### 프로젝트 구조
```
src/main/java/com/example/
├── Application.java     # Main class
├── config/              # Configuration
├── controller/          # Controllers
├── service/             # Services
├── repository/          # Repositories
├── model/               # Entities
└── dto/                 # DTOs

src/main/resources/
├── application.properties
└── db/migration/        # Liquibase migrations
```
### 컨트롤러
```java
@RestController
@RequestMapping("/api/v1/users")
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping
    public List<UserDTO> getAllUsers() {
        return userService.findAll();
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public UserDTO createUser(@Valid @RequestBody UserCreateDTO dto) {
        return userService.create(dto);
    }
}
```
### 서비스 계층
```java
@Service
@Transactional
public class UserService {

    private final UserRepository userRepository;

    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public List<UserDTO> findAll() {
        return userRepository.findAll()
            .stream()
            .map(this::toDTO)
            .collect(Collectors.toList());
    }

    public UserDTO create(UserCreateDTO dto) {
        User user = new User();
        user.setEmail(dto.getEmail());
        user.setName(dto.getName());
        return toDTO(userRepository.save(user));
    }
}
```
### 저장소
```java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByEmail(String email);

    @Query("SELECT u FROM User u WHERE u.active = true")
    List<User> findActiveUsers();
}
```
### 구성
```java
@Configuration
public class DatabaseConfig {

    @Bean
    public DataSource dataSource(
        @Value("${spring.datasource.url}") String url,
        @Value("${spring.datasource.username}") String username,
        @Value("${spring.datasource.password}") String password
    ) {
        HikariConfig config = new HikariConfig();
        config.setJdbcUrl(url);
        config.setUsername(username);
        config.setPassword(password);
        return new HikariDataSource(config);
    }
}
```
## 고/진

### 빠른 시작
```bash
go mod init project-name
go get -u github.com/gin-gonic/gin
go run main.go
```
### 기본 응용 프로그램
```go
package main

import (
    "github.com/gin-gonic/gin"
)

type User struct {
    ID    uint   `json:"id"`
    Email string `json:"email"`
    Name  string `json:"name"`
}

func main() {
    r := gin.Default()

    r.GET("/users", getUsers)
    r.POST("/users", createUser)

    r.Run(":8080")
}

func getUsers(c *gin.Context) {
    users := []User{...}
    c.JSON(200, users)
}
```
## 프레임워크 비교

| 기능 | 익스프레스 | FastAPI | 장고 | 스프링 부트 | 진 |
|---------|---------|---------|---------|------------|------|
| 언어 | 타입스크립트 | 파이썬 | 파이썬 | 자바 | 이동 |
| 성과 | 높음 | 높음 | 중간 | 중간 | 매우 높음 |
| 학습 곡선 | 낮음 | 낮음 | 중간 | 높음 | 낮음 |
| 내장 기능 | 최소 | 좋음 | 우수 | 우수 | 최소 |
| ORM 지원 | 다중 | SQLAlchemy | 장고 ORM | JPA | 다중 |
| 타입스크립트 지원 | 네이티브 | 아니요 | 아니요 | 롬복 | 아니요 |
| 비동기 지원 | 네이티브 | 네이티브 | 한정 | 반응성 | 네이티브 |

## 모범 사례

### 구성 관리
```typescript
// config/index.ts
export const config = {
  port: parseInt(process.env.PORT || '3000', 10),
  database: {
    host: process.env.DB_HOST || 'localhost',
    port: parseInt(process.env.DB_PORT || '5432', 10),
    name: process.env.DB_NAME || 'mydb',
  },
  jwt: {
    secret: process.env.JWT_SECRET || 'secret',
    expiresIn: process.env.JWT_EXPIRES_IN || '7d',
  },
};
```
### 환경 변수
```bash
# .env.example
PORT=3000
NODE_ENV=development
DATABASE_URL=postgresql://localhost:5432/mydb
JWT_SECRET=your-secret-key
```
### 로깅
```typescript
import winston from 'winston';

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'app.log' }),
  ],
});
```
## 테스트

### 익스프레스(예)
```typescript
import request from 'supertest';
import app from '../app';

describe('User API', () => {
  it('should create user', async () => {
    const res = await request(app)
      .post('/api/v1/users')
      .send({
        email: 'test@example.com',
        name: 'Test User',
      })
      .expect(201);

    expect(res.body.data.email).toBe('test@example.com');
  });
});
```
### FastAPI(pytest)
```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    response = client.post(
        "/api/v1/users/",
        json={
            "email": "test@example.com",
            "name": "Test User"
        }
    )
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"
```
## 배포

### 도커(Node.js)
```dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --production
COPY --from=builder /app/dist ./dist
EXPOSE 3000
CMD ["node", "dist/index.js"]
```
### 도커(파이썬)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```
### 도커(자바)
```dockerfile
FROM maven:3.9-eclipse-temurin-17 AS build
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline
COPY src ./src
RUN mvn clean package -DskipTests

FROM eclipse-temurin:17-jre
WORKDIR /app
COPY --from=build /app/target/*.jar app.jar
EXPOSE 8080
CMD ["java", "-jar", "app.jar"]
```
## 문제 해결

### 메모리 문제
- 메모리 사용량 모니터링
- 연결 풀링 구현
- 대용량 데이터 전송에는 스트리밍 사용

### 성능
- 내장된 프로파일러가 있는 프로파일
- 적절한 곳에 캐싱을 추가하세요.
- 데이터베이스 쿼리 최적화
- 비동기 작업 사용

### 데이터베이스 문제
- 연결 풀 구성을 확인하세요.
- 재시도 로직 구현
- 적절한 인덱스를 추가하세요.
- 쿼리 성능 모니터링