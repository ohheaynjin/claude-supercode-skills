# GraphQL 아키텍트 - 예제 및 패턴

## 안티 패턴

### 안티 패턴: N+1 쿼리를 처리하지 않음

**모습:**
```typescript
// Resolver without DataLoader
const resolvers = {
  Post: {
    author: async (post, _, { db }) => {
      // Executed once per post (N+1 problem!)
      return db.User.findByPk(post.userId);
    }
  }
};

// Query for 100 posts triggers 101 DB queries:
// 1 query for posts + 100 queries for authors
```
**실패하는 이유:**
- **성능**: 선형 확장(게시물 100개 = 쿼리 101개, 게시물 1000개 = 쿼리 1001개)
- **데이터베이스 부하**: 작은 쿼리로 DB를 압도함
- **지연**: 일괄 처리 대신 순차적 쿼리

**올바른 접근 방식:**
```typescript
// Use DataLoader for batching
import DataLoader from 'dataloader';

// Create per-request loader
const createLoaders = (db) => ({
  userLoader: new DataLoader(async (userIds) => {
    const users = await db.User.findAll({
      where: { id: userIds }
    });
    const userMap = new Map(users.map(u => [u.id, u]));
    return userIds.map(id => userMap.get(id));
  })
});

const resolvers = {
  Post: {
    author: (post, _, { loaders }) => {
      // DataLoader batches all author requests
      return loaders.userLoader.load(post.userId);
    }
  }
};

// Same query now triggers 2 queries:
// 1 query for posts + 1 batched query for all authors
```
---

### 안티 패턴: 쿼리 깊이/복잡성 제한 없음

**모습:**
```graphql
# Malicious query - no limits
query DeepNested {
  users {
    posts {
      comments {
        author {
          posts {
            comments {
              author {
                # ... infinitely deep
              }
            }
          }
        }
      }
    }
  }
}
```
**실패하는 이유:**
- DoS 취약점
- 기억력 고갈
- 데이터베이스 과부하

**올바른 접근 방식:**
```typescript
import depthLimit from 'graphql-depth-limit';
import { createComplexityLimitRule } from 'graphql-validation-complexity';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [
    depthLimit(10),  // Max 10 levels deep
    createComplexityLimitRule(1000)  // Max complexity score
  ]
});
```
---

### 안티 패턴: 내부 ID 노출

**모습:**
```graphql
type User {
  id: Int!  # Database auto-increment ID exposed
  email: String!
}
```
**실패하는 이유:**
- 데이터베이스 구조를 드러냅니다.
- 열거 공격 가능
- 데이터베이스 마이그레이션 시 중단

**올바른 접근 방식:**
```graphql
type User {
  id: ID!  # Opaque identifier (base64 encoded or UUID)
  email: String!
}
```


```typescript
// Encode/decode IDs
const toGlobalId = (type: string, id: number) => 
  Buffer.from(`${type}:${id}`).toString('base64');

const fromGlobalId = (globalId: string) => {
  const decoded = Buffer.from(globalId, 'base64').toString();
  const [type, id] = decoded.split(':');
  return { type, id: parseInt(id) };
};
```
---

### 안티 패턴: 모두 Null 가능

**모습:**
```graphql
type User {
  id: ID
  email: String
  name: String
  posts: [Post]
}
```
**실패하는 이유:**
- 클라이언트가 모든 곳에서 null을 처리하도록 강제합니다.
- 필수 필드를 숨깁니다.
- 코드 생성에 스키마를 덜 유용하게 만듭니다.

**올바른 접근 방식:**
```graphql
type User {
  id: ID!                    # Always present
  email: String!             # Required field
  name: String               # Optional (nullable is intentional)
  posts: [Post!]!            # Non-null list with non-null items
}
```
---

## 통합 패턴

### 백엔드 개발자
- **핸드오프**: 백엔드에서 비즈니스 로직 구현 → GraphQL 설계자가 스키마를 통해 노출
- **협업**: 공유 리졸버 구현, 인증/권한 부여
- **도구**: TypeScript, Node.js, ORM(Prisma, TypeORM), DataLoader
- **예**: 백엔드가 사용자 서비스 제공 → GraphQL은 DataLoader를 사용하여 사용자 유형을 생성합니다.

### API 디자이너
- **핸드오프**: API 디자이너가 REST 끝점을 정의 → GraphQL이 래퍼 또는 마이그레이션 계획을 생성합니다.
- **협업**: API 버전 관리 전략, REST→GraphQL 마이그레이션
- **도구**: OpenAPI 사양, GraphQL 스키마, 게이트웨이 패턴
- **예**: 제품용 REST API → GraphQL은 통합 스키마를 생성합니다.

### 프론트엔드 개발자
- **Handoff**: 프런트엔드에 데이터가 필요함 → GraphQL은 형식화된 스키마와 쿼리를 제공합니다.
- **협업**: 조각 코로케이션, Apollo 클라이언트 캐시 구성
- **도구**: GraphQL 코드 생성기, Apollo 클라이언트, 릴레이
- **예**: 프런트엔드에는 사용자 프로필이 필요합니다. → GraphQL은 입력된 쿼리를 제공합니다.

### 데이터베이스 최적화 프로그램
- **핸드오프**: GraphQL은 느린 해석기를 식별 → 데이터베이스 최적화 프로그램이 인덱스를 생성합니다.
- **협업**: 쿼리 최적화, 연결 풀링
- **도구**: EXPLAIN ANALYZE, DataLoader 일괄 처리, pg_stat_statements
- **예**: DataLoader 일괄 처리 100명의 사용자 → 커버링 인덱스 생성

### 데브옵스 엔지니어
- **핸드오프**: GraphQL은 게이트웨이 아키텍처를 정의 → DevOps는 연합 서비스를 배포합니다.
- **협업**: 서비스 메시, 로드 밸런싱, 모니터링
- **도구**: Kubernetes, Istio, Apollo Router, Grafana
- **예**: 5개의 하위 그래프가 있는 Apollo Federation → 서비스 검색을 통한 배포

---

## 전체 리졸버 예제
```typescript
import { GraphQLResolveInfo } from 'graphql';
import DataLoader from 'dataloader';

interface Context {
  user: User | null;
  db: Database;
  loaders: {
    userLoader: DataLoader<string, User>;
    postLoader: DataLoader<string, Post>;
    commentCountLoader: DataLoader<string, number>;
  };
}

export const resolvers = {
  Query: {
    me: (_, __, { user }: Context) => user,
    
    user: async (_, { id }, { loaders }: Context) => {
      return loaders.userLoader.load(id);
    },
    
    posts: async (_, { first, after }, { db }: Context) => {
      const cursor = after ? decodeCursor(after) : null;
      const posts = await db.Post.findAll({
        where: cursor ? { id: { [Op.gt]: cursor } } : {},
        limit: first + 1,
        order: [['id', 'ASC']]
      });
      
      const hasNextPage = posts.length > first;
      const edges = posts.slice(0, first).map(post => ({
        node: post,
        cursor: encodeCursor(post.id)
      }));
      
      return {
        edges,
        pageInfo: {
          hasNextPage,
          hasPreviousPage: !!after,
          startCursor: edges[0]?.cursor,
          endCursor: edges[edges.length - 1]?.cursor
        }
      };
    }
  },
  
  User: {
    posts: async (user, { first = 10 }, { db }: Context) => {
      return db.Post.findAll({
        where: { authorId: user.id },
        limit: first
      });
    },
    
    postCount: (user, _, { loaders }: Context) => {
      return loaders.postCountLoader.load(user.id);
    }
  },
  
  Post: {
    author: (post, _, { loaders }: Context) => {
      return loaders.userLoader.load(post.authorId);
    },
    
    commentCount: (post, _, { loaders }: Context) => {
      return loaders.commentCountLoader.load(post.id);
    }
  },
  
  Mutation: {
    createPost: async (_, { input }, { user, db }: Context) => {
      if (!user) {
        throw new Error('Authentication required');
      }
      
      const post = await db.Post.create({
        title: input.title,
        content: input.content,
        authorId: user.id
      });
      
      return {
        post,
        errors: []
      };
    }
  }
};
```
---

## 데이터로더 팩토리
```typescript
// loaders.ts

import DataLoader from 'dataloader';
import { Database } from './db';

export function createLoaders(db: Database) {
  return {
    userLoader: new DataLoader<string, User>(async (ids) => {
      const users = await db.User.findAll({ where: { id: ids } });
      const userMap = new Map(users.map(u => [u.id, u]));
      return ids.map(id => userMap.get(id) || null);
    }),
    
    postLoader: new DataLoader<string, Post>(async (ids) => {
      const posts = await db.Post.findAll({ where: { id: ids } });
      const postMap = new Map(posts.map(p => [p.id, p]));
      return ids.map(id => postMap.get(id) || null);
    }),
    
    postCountLoader: new DataLoader<string, number>(async (userIds) => {
      const counts = await db.Post.findAll({
        attributes: ['authorId', [db.fn('COUNT', '*'), 'count']],
        where: { authorId: userIds },
        group: ['authorId']
      });
      const countMap = new Map(counts.map(c => [c.authorId, c.get('count')]));
      return userIds.map(id => countMap.get(id) || 0);
    }),
    
    commentCountLoader: new DataLoader<string, number>(async (postIds) => {
      const counts = await db.Comment.findAll({
        attributes: ['postId', [db.fn('COUNT', '*'), 'count']],
        where: { postId: postIds },
        group: ['postId']
      });
      const countMap = new Map(counts.map(c => [c.postId, c.get('count')]));
      return postIds.map(id => countMap.get(id) || 0);
    })
  };
}
```
