# 백엔드 개발자 - 기술 참조

## 워크플로 1: JWT 인증을 사용하여 Production-Ready Express + TypeScript API 설정

**목표:** TypeScript, Prisma ORM, JWT 인증, 검증, 오류 처리 기능을 갖춘 부트스트랩 보안 REST API를 1시간 이내에 완료하세요.

### 1단계: TypeScript를 사용하여 프로젝트 초기화

```bash
mkdir my-backend-api && cd my-backend-api
npm init -y
npm install express cors helmet dotenv
npm install -D typescript @types/node @types/express ts-node-dev
npx tsc --init
```

### 2단계: Prisma ORM 설정

```bash
npm install prisma @prisma/client
npm install -D prisma
npx prisma init
```

```prisma
# prisma/schema.prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

model User {
  id        String   @id @default(uuid())
  email     String   @unique
  password  String
  name      String?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}
```

```bash
# Run migrations
npx prisma migrate dev --name init
npx prisma generate
```

### 3단계: JWT 인증 구현

```typescript
// src/auth/jwt.ts
import jwt from 'jsonwebtoken';
import { Request, Response, NextFunction } from 'express';

const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key';
const JWT_EXPIRES_IN = '15m';
const REFRESH_TOKEN_EXPIRES_IN = '7d';

export function generateTokens(userId: string) {
  const accessToken = jwt.sign({ userId }, JWT_SECRET, { 
    expiresIn: JWT_EXPIRES_IN 
  });
  
  const refreshToken = jwt.sign({ userId }, JWT_SECRET, { 
    expiresIn: REFRESH_TOKEN_EXPIRES_IN 
  });
  
  return { accessToken, refreshToken };
}

export function verifyToken(token: string) {
  try {
    return jwt.verify(token, JWT_SECRET) as { userId: string };
  } catch (error) {
    throw new Error('Invalid token');
  }
}

// Middleware
export function authMiddleware(req: Request, res: Response, next: NextFunction) {
  const authHeader = req.headers.authorization;
  
  if (!authHeader?.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'No token provided' });
  }
  
  const token = authHeader.substring(7);
  
  try {
    const payload = verifyToken(token);
    req.userId = payload.userId; // Attach to request
    next();
  } catch (error) {
    return res.status(401).json({ error: 'Invalid token' });
  }
}
```

### 4단계: Zod를 사용하여 입력 유효성 검사 설정

```bash
npm install zod
```

```typescript
// src/validators/user.validator.ts
import { z } from 'zod';

export const registerSchema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  name: z.string().optional(),
});

export const loginSchema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(1, 'Password required'),
});

// Middleware
export function validate(schema: z.ZodSchema) {
  return (req: Request, res: Response, next: NextFunction) => {
    try {
      schema.parse(req.body);
      next();
    } catch (error) {
      if (error instanceof z.ZodError) {
        return res.status(400).json({ 
          error: 'Validation failed', 
          details: error.errors 
        });
      }
      next(error);
    }
  };
}
```

### 5단계: 인증 경로 구현

```typescript
// src/routes/auth.routes.ts
import { Router } from 'express';
import bcrypt from 'bcrypt';
import { PrismaClient } from '@prisma/client';
import { validate } from '../validators/user.validator';
import { registerSchema, loginSchema } from '../validators/user.validator';
import { generateTokens } from '../auth/jwt';

const router = Router();
const prisma = new PrismaClient();

// Register
router.post('/register', validate(registerSchema), async (req, res, next) => {
  try {
    const { email, password, name } = req.body;
    
    // Check if user exists
    const existingUser = await prisma.user.findUnique({ where: { email } });
    if (existingUser) {
      return res.status(409).json({ error: 'User already exists' });
    }
    
    // Hash password
    const hashedPassword = await bcrypt.hash(password, 10);
    
    // Create user
    const user = await prisma.user.create({
      data: { email, password: hashedPassword, name },
    });
    
    // Generate tokens
    const { accessToken, refreshToken } = generateTokens(user.id);
    
    res.status(201).json({
      user: { id: user.id, email: user.email, name: user.name },
      accessToken,
      refreshToken,
    });
  } catch (error) {
    next(error);
  }
});

// Login
router.post('/login', validate(loginSchema), async (req, res, next) => {
  try {
    const { email, password } = req.body;
    
    // Find user
    const user = await prisma.user.findUnique({ where: { email } });
    if (!user) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }
    
    // Verify password
    const isValid = await bcrypt.compare(password, user.password);
    if (!isValid) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }
    
    // Generate tokens
    const { accessToken, refreshToken } = generateTokens(user.id);
    
    res.json({
      user: { id: user.id, email: user.email, name: user.name },
      accessToken,
      refreshToken,
    });
  } catch (error) {
    next(error);
  }
});

export default router;
```

### 6단계: 전역 오류 처리기

```typescript
// src/middleware/error.middleware.ts
import { Request, Response, NextFunction } from 'express';

export function errorHandler(
  error: Error,
  req: Request,
  res: Response,
  next: NextFunction
) {
  console.error('Error:', error);
  
  res.status(500).json({
    error: 'Internal server error',
    message: process.env.NODE_ENV === 'development' ? error.message : undefined,
  });
}
```

### 7단계: 주 서버 설정

```typescript
// src/server.ts
import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import dotenv from 'dotenv';
import authRoutes from './routes/auth.routes';
import { errorHandler } from './middleware/error.middleware';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json());

// Routes
app.use('/api/auth', authRoutes);

// Error handling
app.use(errorHandler);

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
```

## 워크플로 2: Bull Queue를 사용하여 백그라운드 작업 구현

**목표:** 장기 실행 작업(이메일 전송, 이미지 처리)을 비동기식으로 처리합니다.

### 1단계: 종속성 설치

```bash
npm install bull @types/bull
```

### 2단계: 대기열 설정

```typescript
// src/queues/email.queue.ts
import Queue from 'bull';
import { sendEmail } from '../services/email.service';

const emailQueue = new Queue('email', {
  redis: {
    host: process.env.REDIS_HOST || 'localhost',
    port: parseInt(process.env.REDIS_PORT || '6379'),
  },
});

// Process jobs
emailQueue.process(async (job) => {
  const { to, subject, body } = job.data;
  console.log(`Sending email to ${to}...`);
  
  await sendEmail(to, subject, body);
  
  console.log(`Email sent to ${to}`);
});

// Add job to queue
export function queueEmail(to: string, subject: string, body: string) {
  return emailQueue.add({
    to,
    subject,
    body,
  }, {
    attempts: 3, // Retry 3 times on failure
    backoff: {
      type: 'exponential',
      delay: 2000, // 2s, 4s, 8s
    },
  });
}

export { emailQueue };
```

### 3단계: API 경로에서 사용

```typescript
// src/routes/user.routes.ts
import { queueEmail } from '../queues/email.queue';

router.post('/send-welcome-email', authMiddleware, async (req, res) => {
  const user = await prisma.user.findUnique({ where: { id: req.userId } });
  
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }
  
  // Queue email (non-blocking)
  await queueEmail(
    user.email,
    'Welcome!',
    `Hello ${user.name}, welcome to our platform!`
  );
  
  res.json({ message: 'Welcome email queued' });
});
```

## 통합 패턴

### API 디자이너
- **핸드오프:** 백엔드 개발자가 API 경로를 구현 → API 디자이너가 OpenAPI 사양 준수 여부를 확인합니다.
- **협업:** 백엔드 개발자가 엔드포인트 생성 → API 디자이너가 RESTful 규칙, HTTP 상태 코드 보장
- **도구:** 백엔드 개발자는 Express/FastAPI를 사용합니다. api-designer는 Swagger/Postman으로 유효성을 검사합니다.

### 데이터베이스 관리자
- **핸드오프:** 백엔드 개발자가 ORM 모델 구현 → 데이터베이스 관리자가 데이터베이스 스키마, 인덱스 최적화
- **협업:** 백엔드 개발자가 쿼리 작성 → 데이터베이스 관리자가 쿼리 성능 조정
- **도구:** 백엔드 개발자는 Prisma/TypeORM을 사용합니다. 데이터베이스 관리자는 EXPLAIN ANALYZE, pg_stat_statements를 사용합니다.

### 프론트엔드 개발자
- **Handoff:** 백엔드 개발자가 API 엔드포인트 생성 → 프런트엔드 개발자가 Axios/Fetch를 통해 소비
- **협업:** 백엔드 개발자가 API 계약 정의 → 프런트엔드 개발자가 TypeScript 유형 구현
- **도구:** 둘 다 TypeScript를 사용합니다. backend-developer는 프런트엔드 코드 생성을 위한 OpenAPI 사양을 제공합니다.

### 데브옵스 엔지니어
- **Handoff:** backend-developer가 Dockerfile을 생성 → devops-engineer가 CI/CD 파이프라인 설정
- **협업:** 백엔드 개발자가 상태 확인을 구현 → devops-엔지니어가 Kubernetes 프로브 구성
- **도구:** 백엔드 개발자는 Docker를 사용합니다. devops-engineer는 Kubernetes, GitHub Actions를 사용합니다.

### 보안 감사자
- **인계:** 백엔드 개발자가 인증 구현 → 보안 감사자 취약점 감사(SQL 주입, XSS)
- **협업:** 백엔드 개발자가 입력 유효성 검사를 추가 → 보안 감사자가 보안 코딩 방식을 확인합니다.
- **도구:** 백엔드 개발자는 Zod/Joi를 사용합니다. 보안 감사자는 OWASP ZAP, Burp Suite를 사용합니다.

## 스크립트 참조

### API 스캐폴딩```bash
python scripts/scaffold_api.py <framework> <project_name>
# Frameworks: express, fastapi, django, spring
```

### 데이터베이스 모델 생성```bash
python scripts/generate_model.py <orm> --schema <schema_file> --output <output_dir>
# ORMs: sequelize, typeorm, sqlalchemy, django, jpa
```

### 인증 설정```bash
python scripts/setup_auth.py <framework> <auth_type>
# Auth types: jwt, oauth2, session
```

### 미들웨어 세대```bash
python scripts/create_middleware.py <framework> --output <output_dir>
```

### 오류 처리기 설정```bash
python scripts/error_handler.py <framework> --output <output_dir>
```

### 배포 스크립트```bash
./scripts/deploy.sh [OPTIONS]
# Options:
# --skip-tests: Skip test execution
# --platform <kubernetes|aws|gcp>: Deployment platform
# --rollback: Rollback deployment
# --health-check: Run health check only
```
