---
name: graphql-architect
description: 리졸버 최적화, 구독, API 게이트웨이 패턴을 전문으로 하는 GraphQL 스키마 및 페더레이션 전문가
---
# GraphQL 아키텍트 스킬

## 목적

스키마 설계, 연합 패턴, 확인자 최적화 및 실시간 구독을 전문으로 하는 전문적인 GraphQL 아키텍처 전문 지식을 제공합니다. 분산 시스템 전반에 걸쳐 N+1 방지, 효율적인 캐싱 및 확장 가능한 API 게이트웨이 패턴을 통해 성능이 뛰어나고 유형이 안전한 GraphQL API를 구축합니다.

## 사용 시기

- 새로운 API를 위해 처음부터 GraphQL 스키마 설계
- 여러 서비스에 걸쳐 GraphQL 페더레이션 구현
- N+1 쿼리를 방지하기 위한 리졸버 최적화(DataLoader 구현)
- GraphQL 구독을 통해 실시간 기능 구축
- REST에서 GraphQL로 마이그레이션 또는 하이브리드 REST+GraphQL API 설계
- GraphQL API 게이트웨이 패턴 구현

## 빠른 시작

**다음과 같은 경우에 이 스킬을 호출하세요:**
- 새로운 GraphQL 스키마 또는 연합 아키텍처 설계
- N+1 쿼리 성능 문제 해결
- 실시간 구독 구현
- REST API를 GraphQL로 마이그레이션

**다음과 같은 경우에는 호출하지 마세요.**
- 간단한 REST API로 충분합니다. (api-designer 사용)
- API 레이어가 없는 데이터베이스 스키마 설계(데이터베이스 관리자 사용)
- 프론트엔드 데이터 가져오기만 가능(프런트엔드 개발자 사용)

## 핵심 기능

### 스키마 디자인
- 모범 사례를 사용하여 유형이 안전한 GraphQL 스키마 생성
- 페이지네이션 패턴 구현 (릴레이, 오프셋 기반)
- 입력 검증 및 오류 처리를 통해 돌연변이 설계
- 스키마 진화 및 이전 버전과의 호환성 관리

### 페더레이션 아키텍처
- 마이크로서비스를 위한 Apollo Federation 구현
- 서비스 구성을 위한 스키마 스티칭 구성
- 서비스 간 쿼리 및 변형 관리
- 스키마 구성을 위한 API 게이트웨이 설정

### 리졸버 최적화
- N+1 방지를 위한 DataLoader 구현
- 리졸버 및 필드 수준의 캐싱 전략
- 쿼리 복잡성 분석 및 깊이 제한
- 생산 최적화를 위한 지속적인 쿼리

### 실시간 구독
- WebSocket 기반 구독 구현
- 구독 수명주기 및 정리 관리
- 이벤트 중심 백엔드와 통합
- 가입 인증 및 승인 처리

## 의사결정 프레임워크

### GraphQL과 REST 결정 매트릭스 비교

| 요인 | GraphQL 사용 | REST 사용 |
|---------|-------------|----------|
| **클라이언트 유형** | 다양한 요구 사항을 가진 여러 클라이언트 | 요구 사항이 예측 가능한 단일 클라이언트 |
| **데이터 관계** | 고도로 중첩되고 상호 연결된 데이터 | 관계가 거의 없는 평면 리소스 |
| **과잉** | 클라이언트에는 다른 하위 집합이 필요합니다 | 클라이언트는 일반적으로 모든 필드가 필요합니다 |
| **과소평가** | 여러 번의 왕복 여행을 피하세요 | 단일 엔드포인트가 충분함 |
| **스키마 발전** | 빈번한 변경, 이전 버전과의 호환성 | 안정적인 API, 버전 관리 가능 |
| **실시간** | 구독이 필요합니다 | 폴링 또는 웹후크가 충분함 |

### 스키마 설계 결정 트리
```
Schema Design Requirements
│
├─ Single service (monolith)?
│  └─ Schema-first design with single schema
│
├─ Multiple microservices?
│  ├─ Services owned by different teams?
│  │  └─ Apollo Federation
│  └─ Services owned by same team?
│     └─ Schema stitching (simpler)
│
├─ Existing REST APIs to wrap?
│  └─ GraphQL wrapper layer
│
└─ Need backward compatibility?
   └─ Hybrid REST + GraphQL
```
### N+1 예방 전략
```
Resolver Implementation
│
├─ Field resolves to single related entity?
│  └─ DataLoader with batching
│
├─ Field resolves to list of related entities?
│  ├─ List size always small (<10)?
│  │  └─ Direct query acceptable
│  └─ List size unbounded?
│     └─ DataLoader with batching + pagination
│
├─ Nested resolvers (users → posts → comments)?
│  └─ Multi-level DataLoaders
│
└─ Aggregations or counts?
   └─ Separate DataLoader for counts
```
## 핵심 작업 흐름: DataLoader 구현

**문제**: N+1 쿼리로 인해 성능이 저하됩니다.
```typescript
// WITHOUT DataLoader - N+1 problem
const resolvers = {
  Post: {
    author: async (post, _, { db }) => {
      // Executed once per post (N+1 problem!)
      return db.User.findByPk(post.userId);
    }
  }
};
// Query for 100 posts triggers 101 DB queries
```
**해결책**: DataLoader를 사용한 일괄 처리
```typescript
import DataLoader from 'dataloader';

// Create loader per request (important!)
function createLoaders(db) {
  return {
    userLoader: new DataLoader(async (userIds) => {
      const users = await db.User.findAll({
        where: { id: userIds }
      });
      // Return in same order as requested IDs
      const userMap = new Map(users.map(u => [u.id, u]));
      return userIds.map(id => userMap.get(id));
    })
  };
}

// Resolver using DataLoader
const resolvers = {
  Post: {
    author: (post, _, { loaders }) => {
      return loaders.userLoader.load(post.userId);
    }
  }
};
// Same query now triggers 2 queries total!
```
## 빠른 참조: 스키마 모범 사례

### 페이지 매김 패턴(릴레이 스타일)
```graphql
type Query {
  users(first: Int, after: String, last: Int, before: String): UserConnection!
}

type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type UserEdge {
  node: User!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}
```
### 오류 처리 패턴
```graphql
type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
}

type CreateUserPayload {
  user: User
  errors: [UserError!]!
}

type UserError {
  field: String
  message: String!
  code: ErrorCode!
}

enum ErrorCode {
  VALIDATION_ERROR
  NOT_FOUND
  UNAUTHORIZED
  CONFLICT
}
```
## 위험 신호 - 에스컬레이션해야 하는 경우

| 관찰 | 에스컬레이션하는 이유 |
|-------------|---------------|
| 쿼리 복잡성 폭발 | DoS를 유발하는 무제한 중첩 쿼리 |
| 페더레이션 순환 종속성 | 스키마 디자인 문제 |
| 10,000개 이상의 동시 구독 | 인프라 아키텍처 |
| 50개 이상의 필드에 대한 스키마 버전 관리 | 획기적인 변화 관리 |
| 서비스 간 트랜잭션 요구 | 분산 시스템 패턴 |

## 추가 리소스

- **자세한 기술 참조**: [REFERENCE.md](REFERENCE.md) 참조
  - Apollo Federation 설정 워크플로
  - 필드 수준 인증 지시어
  - 쿼리 복잡성 제한
  
- **코드 예제 및 패턴**: [EXAMPLES.md](EXAMPLES.md) 참조
  - 안티 패턴(N+1 쿼리, 복잡성 제한 없음)
  - 다른 스킬과의 통합 패턴
  - 완전한 리졸버 구현