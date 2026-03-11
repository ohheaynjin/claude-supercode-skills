---
name: typescript-pro
description: 고급 유형 시스템 기능, 일반 프로그래밍 및 유형 안전 애플리케이션 아키텍처를 전문으로 하는 전문 TypeScript 개발자입니다. 이 에이전트는 TypeScript 5+ 기능을 활용하여 포괄적인 유형 안전성과 우수한 개발자 경험을 갖춘 강력하고 유지 관리 가능한 애플리케이션을 구축하는 데 탁월합니다.
---
# TypeScript Pro 전문가

## 목적

고급 유형 시스템 기능, 일반 프로그래밍 패턴 및 유형이 안전한 애플리케이션 아키텍처를 갖춘 전문적인 TypeScript 개발 기능을 제공합니다. 포괄적인 유형 안전성을 갖춘 강력하고 유지 관리 가능한 애플리케이션을 구축하기 위해 TypeScript 5+를 활용하는 데 특화되어 있습니다.

## 사용 시기

- 고급 제네릭 및 매핑된 유형을 사용하여 복잡한 유형 시스템 설계
- 프런트엔드-백엔드 경계를 넘어 유형이 안전한 API 구현
- JavaScript 코드베이스를 TypeScript로 점진적으로 마이그레이션
- 복잡한 유형 오류 또는 추론 문제 해결
- 유형이 안전한 라이브러리, SDK 또는 프레임워크 통합 구축
- 대규모 프로젝트에서 TypeScript 빌드 성능 최적화
- 브랜드형, 차별적 조합, 유틸리티형 만들기

## 빠른 시작

**다음과 같은 경우에 이 스킬을 호출하세요:**
- 고급 제네릭 및 매핑된 유형을 사용하여 복잡한 유형 시스템 설계
- 프런트엔드-백엔드 경계를 넘어 유형이 안전한 API 구현
- JavaScript 코드베이스를 TypeScript로 점진적으로 마이그레이션
- 복잡한 유형 오류 또는 추론 문제 해결
- 유형이 안전한 라이브러리, SDK 또는 프레임워크 통합 구축

**다음과 같은 경우에는 호출하지 마세요.**
- 간단한 JavaScript 작업(유형 주석이 필요하지 않음)
- 런타임 로직 버그(대신 디버거 사용)
- 빌드 구성만(대신 빌드 엔지니어 사용)
- React/Vue 특정 패턴(react-specialist/vue-expert 사용)

---
---

## 핵심 워크플로우

### 작업 흐름 1: 유형 안전 API 클라이언트 설계

**사용 사례:** 자동 완성 기능을 사용하여 완전히 유형이 안전한 REST API 클라이언트 생성

**단계:**

**1. API 스키마 정의(계약 우선)**```typescript
// api-schema.ts - Single source of truth for API contract
export const apiSchema = {
  '/users': {
    GET: {
      query: {} as { page?: number; limit?: number },
      response: {} as { users: User[]; total: number }
    },
    POST: {
      body: {} as { email: string; name: string },
      response: {} as { id: string; email: string; name: string }
    }
  },
  '/users/{id}': {
    GET: {
      params: {} as { id: string },
      response: {} as User
    },
    PUT: {
      params: {} as { id: string },
      body: {} as Partial<User>,
      response: {} as User
    },
    DELETE: {
      params: {} as { id: string },
      response: {} as { success: boolean }
    }
  },
  '/posts': {
    GET: {
      query: {} as { author_id?: string; tags?: string[] },
      response: {} as { posts: Post[]; next_cursor?: string }
    }
  }
} as const;

// Extract types from schema
type ApiSchema = typeof apiSchema;
type ApiPaths = keyof ApiSchema;
type ApiMethods<Path extends ApiPaths> = keyof ApiSchema[Path];

// Helper types for type-safe request/response
type RequestParams<
  Path extends ApiPaths,
  Method extends ApiMethods<Path>
> = ApiSchema[Path][Method] extends { params: infer P } ? P : never;

type RequestQuery<
  Path extends ApiPaths,
  Method extends ApiMethods<Path>
> = ApiSchema[Path][Method] extends { query: infer Q } ? Q : never;

type RequestBody<
  Path extends ApiPaths,
  Method extends ApiMethods<Path>
> = ApiSchema[Path][Method] extends { body: infer B } ? B : never;

type ResponseData<
  Path extends ApiPaths,
  Method extends ApiMethods<Path>
> = ApiSchema[Path][Method] extends { response: infer R } ? R : never;
```

**2. 유형 안전 API 클라이언트 구현**```typescript
// api-client.ts
class ApiClient {
  constructor(private baseUrl: string) {}

  async request<
    Path extends ApiPaths,
    Method extends ApiMethods<Path>
  >(
    path: Path,
    method: Method,
    options?: {
      params?: RequestParams<Path, Method>;
      query?: RequestQuery<Path, Method>;
      body?: RequestBody<Path, Method>;
    }
  ): Promise<ResponseData<Path, Method>> {
    // Replace path parameters: /users/{id} → /users/123
    let url = path as string;
    if (options?.params) {
      Object.entries(options.params).forEach(([key, value]) => {
        url = url.replace(`{${key}}`, String(value));
      });
    }

    // Append query parameters
    if (options?.query) {
      const queryString = new URLSearchParams(
        options.query as Record<string, string>
      ).toString();
      url += `?${queryString}`;
    }

    // Make request
    const response = await fetch(`${this.baseUrl}${url}`, {
      method: method as string,
      headers: {
        'Content-Type': 'application/json',
      },
      body: options?.body ? JSON.stringify(options.body) : undefined,
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }

    return response.json();
  }
}

// Usage with full type safety and auto-completion
const api = new ApiClient('https://api.example.com');

// GET /users?page=1&limit=10
const usersResponse = await api.request('/users', 'GET', {
  query: { page: 1, limit: 10 }  // Type-checked!
});
usersResponse.users[0].email;  // ✅ Auto-complete works!

// POST /users
const newUser = await api.request('/users', 'POST', {
  body: { email: 'test@example.com', name: 'Test' }  // Type-checked!
});
newUser.id;  // ✅ Type: string

// PUT /users/{id}
const updatedUser = await api.request('/users/{id}', 'PUT', {
  params: { id: '123' },  // Type-checked!
  body: { name: 'Updated Name' }  // Partial<User> type-checked!
});

// TypeScript errors for invalid usage:
api.request('/users', 'GET', {
  query: { invalid: true }  // ❌ Error: Object literal may only specify known properties
});

api.request('/users/{id}', 'PUT', {
  // ❌ Error: params required for this path
  body: { name: 'Test' }
});
```

**3. Zod로 런타임 검증 추가**```typescript
import { z } from 'zod';

// Define Zod schemas for runtime validation
const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  name: z.string().min(1).max(100),
  created_at: z.string().datetime()
});

type User = z.infer<typeof UserSchema>;  // TypeScript type from Zod schema

// Enhanced API client with runtime validation
class ValidatedApiClient extends ApiClient {
  async request<
    Path extends ApiPaths,
    Method extends ApiMethods<Path>
  >(
    path: Path,
    method: Method,
    options?: {
      params?: RequestParams<Path, Method>;
      query?: RequestQuery<Path, Method>;
      body?: RequestBody<Path, Method>;
      responseSchema?: z.ZodSchema<ResponseData<Path, Method>>;
    }
  ): Promise<ResponseData<Path, Method>> {
    const response = await super.request(path, method, options);

    // Runtime validation if schema provided
    if (options?.responseSchema) {
      return options.responseSchema.parse(response);
    }

    return response;
  }
}

// Usage with runtime validation
const validatedApi = new ValidatedApiClient('https://api.example.com');

const user = await validatedApi.request('/users/{id}', 'GET', {
  params: { id: '123' },
  responseSchema: UserSchema  // Runtime validation!
});
// If API returns invalid data, Zod throws detailed error
```

---
---

### 작업 흐름 3: 점진적 TypeScript 마이그레이션

**사용 사례:** 대규모 JavaScript 코드베이스를 점진적으로 마이그레이션

**1단계: 변경 사항 없이 TypeScript 활성화(1주차)**```json
// tsconfig.json - Initial configuration
{
  "compilerOptions": {
    "allowJs": true,          // Allow .js files
    "checkJs": false,         // Don't check .js files yet
    "noEmit": true,           // Don't output files (just check)
    "skipLibCheck": true,     // Skip type checking of .d.ts files
    "esModuleInterop": true,
    "moduleResolution": "node",
    "target": "ES2017",
    "module": "commonjs"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

**2단계: JSDoc 유형 힌트 추가(2~4주)**```javascript
// user.js - Add JSDoc comments for type checking
/**
 * @typedef {Object} User
 * @property {string} id
 * @property {string} email
 * @property {string} name
 */

/**
 * Fetch user by ID
 * @param {string} userId
 * @returns {Promise<User>}
 */
async function getUserById(userId) {
  const response = await fetch(`/api/users/${userId}`);
  return response.json();
}

/**
 * @param {User[]} users
 * @param {string} searchTerm
 * @returns {User[]}
 */
function filterUsers(users, searchTerm) {
  return users.filter(u => u.name.includes(searchTerm));
}
```

**3단계: 점차적으로 checkJ 활성화(5~8주)**```json
// tsconfig.json - Start checking JavaScript
{
  "compilerOptions": {
    "allowJs": true,
    "checkJs": true,  // ✅ Enable type checking for .js files
    "noEmit": true
  }
}
```

**디렉터리별 오류 디렉터리 수정:**```bash
# Disable checkJs for specific files with errors
// @ts-nocheck at top of file

# Or suppress specific errors
// @ts-ignore
const result = unsafeOperation();
```

**4단계: 파일 이름을 TypeScript로 바꾸기(9~12주)**```bash
# Rename .js → .ts one directory at a time
mv src/utils/user.js src/utils/user.ts

# Update imports (no file extensions in TypeScript)
- import { getUserById } from './user.js'
+ import { getUserById } from './user'
```

**명시적 유형 추가:**```typescript
// user.ts - Full TypeScript with explicit types
interface User {
  id: string;
  email: string;
  name: string;
  created_at: Date;
}

async function getUserById(userId: string): Promise<User> {
  const response = await fetch(`/api/users/${userId}`);
  return response.json();
}

function filterUsers(users: User[], searchTerm: string): User[] {
  return users.filter(u => u.name.includes(searchTerm));
}
```

**5단계: 엄격 모드 활성화(13~16주)**```json
// tsconfig.json - Enable strict mode progressively
{
  "compilerOptions": {
    "strict": true,  // Enable all strict checks
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictPropertyInitialization": true
  }
}
```

**엄격 모드 오류 수정:**```typescript
// Before (implicit any)
function processData(data) {  // ❌ Parameter 'data' implicitly has 'any' type
  return data.map(item => item.value);
}

// After (explicit types)
function processData(data: Array<{ value: number }>): number[] {
  return data.map(item => item.value);
}

// Before (null not handled)
function getUserName(user: User) {  // ❌ User might be null
  return user.name;
}

// After (null handled)
function getUserName(user: User | null): string {
  return user?.name ?? 'Unknown';
}
```

---
---

### 패턴 2: 문자열 검증을 위한 템플릿 리터럴 유형

**사용 시기:** CSS 클래스 이름, API 경로, 환경 변수

```typescript
// Type-safe CSS class names
type Size = 'sm' | 'md' | 'lg';
type Color = 'red' | 'blue' | 'green';
type ClassName = `btn-${Size}-${Color}`;

function createButton(className: ClassName) {
  return `<button class="${className}"></button>`;
}

createButton('btn-md-blue');  // ✅ Valid
createButton('btn-xl-yellow');  // ❌ Error: Not assignable to ClassName

// Type-safe environment variables
type Stage = 'dev' | 'staging' | 'prod';
type Region = 'us' | 'eu' | 'asia';
type Environment = `${Stage}_${Region}`;

const env: Environment = 'prod_us';  // ✅ Valid
const invalid: Environment = 'production_us';  // ❌ Error
```

---
---

### ❌ 안티 패턴 2: 반환 유형을 정의하지 않음

**모습:**```typescript
function getUser(id: string) {  // ❌ No return type
  return fetch(`/api/users/${id}`).then(r => r.json());
}
// Return type inferred as Promise<any>
```

**실패하는 이유:**
- 구현이 변경되면 반환 유형이 자동으로 변경됩니다.
- 어떤 함수가 반환되는지 보장하지 않음
- 주요 변경 사항을 파악하기가 더 어렵습니다.

**올바른 접근 방식:**```typescript
interface User {
  id: string;
  email: string;
  name: string;
}

function getUser(id: string): Promise<User> {  // ✅ Explicit return type
  return fetch(`/api/users/${id}`).then(r => r.json());
}
```

---
---

## 통합 패턴

### typescript-pro ⇔ 반응 전문가
- **Handoff**: TypeScript pro는 유형을 정의하고 → React 전문가는 구성 요소에서 사용합니다.
- **협업**: props, state, API 계약에 대한 공유 유형 정의
- **도구**: 유형용 TypeScript, UI 로직용 React

### typescript-pro ← 백엔드-개발자
- **Handoff**: TypeScript pro는 API 유형을 설계 → 백엔드는 일치하는 유형을 구현합니다.
- **협업**: 공유 스키마 정의(OpenAPI, tRPC, GraphQL)
- **공동 책임**: 엔드투엔드형 안전

### typescript-pro ← nextjs-developer
- **Handoff**: TypeScript 유형 → Next.js 앱 라우터 서버/클라이언트 구성 요소
- **협업**: 서버 액션 유형, API 경로 유형
- **종속성**: Next.js는 TypeScript의 큰 이점을 얻습니다.

---
