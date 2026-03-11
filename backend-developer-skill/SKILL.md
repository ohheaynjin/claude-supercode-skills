---
name: backend-developer
description: 여러 프레임워크, 데이터베이스 및 배포 전략을 사용하여 프로덕션에 즉시 사용 가능한 서버 측 애플리케이션을 구축하기 위한 포괄적인 백엔드 개발입니다. API, 서비스, 데이터베이스 또는 서버 인프라를 구축할 때 사용합니다.
---
# 백엔드 개발자 스킬

## 목적

여러 프레임워크, 언어 및 배포 전략에 걸쳐 서버 측 애플리케이션 개발에 대한 포괄적인 전문 지식을 제공합니다. 확장 가능한 API, 데이터베이스 설계, 인증 시스템 및 프로덕션 지원 백엔드 인프라 구축을 전문으로 합니다.

## 사용 시기

- REST 또는 GraphQL API 구축
- 데이터베이스 스키마 및 모델 설계
- 인증 및 승인 구현
- 서버 인프라 구축
- 마이크로서비스 또는 모놀리식 백엔드 생성
- 백엔드 성능 최적화
- 서버 애플리케이션을 프로덕션에 배포
- 멀티 프레임워크 백엔드 지침 필요(Express, FastAPI, Django, Spring)

## 빠른 시작

**다음과 같은 경우에 이 스킬을 호출하세요:**
- Node.js, Python, Java 또는 Go에서 서버 측 API(REST, GraphQL) 구축
- 인증/권한 부여 구현 (JWT, OAuth2, 세션 기반)
- 데이터베이스 스키마 설계 및 ORM 통합
- 백엔드 테스트 설정(단위, 통합, E2E)
- 미들웨어 구현(로깅, 검증, 오류 처리)
- Kubernetes, AWS, GCP 또는 Azure에 백엔드 서비스 배포
- 백엔드 성능 최적화(캐싱, 쿼리 최적화, 속도 제한)

**다음과 같은 경우에는 호출하지 마세요.**
- 프론트엔드 개발만 필요 → frontend-developer 또는 nextjs-developer 사용
- 데이터베이스별 최적화 필요 → 데이터베이스 최적화 프로그램 또는 postgres-pro 사용
- 구현 없이 API 디자인 → api-designer 사용
- GraphQL 전용 아키텍처 → graphql-architect 사용
- DevOps/인프라 전용 → devops-engineer 또는 cloud-architect 사용

## 프레임워크 지원

### Node.js/TypeScript
- Express.js, NestJS, Koa.js, Fastify

### 파이썬
- FastAPI, Django, 플라스크, 토네이도

### 자바
- 스프링 부트, Quarkus, Micronaut

### 이동
- 진, 에코, 파이버

## 의사결정 프레임워크

### 백엔드 프레임워크 선택

```
Backend Framework Selection
├─ JavaScript/TypeScript
│   ├─ Need rapid development + type safety → NestJS
│   ├─ Need lightweight/fast performance → Fastify
│   └─ Need simplicity + ecosystem → Express.js
│
├─ Python
│   ├─ Need async + high performance → FastAPI
│   └─ Need batteries-included → Django (+ DRF)
│
├─ Java
│   └─ Enterprise-ready → Spring Boot
│
└─ Go
    └─ High-performance services → Gin or Fiber
```

### 인증 전략 매트릭스

| 대본 | 전략 | 복잡성 | 보안 |
|----------|----------|------------|----------|
| 무상태 API(모바일, SPA) | JWT | 낮은 | 중간 |
| 타사 로그인 | OAuth 2.0 | 중간 | 높은 |
| 기존 웹 앱 | 세션 기반 | 낮은 | 높은 |
| 마이크로서비스 | JWT + API 게이트웨이 | 높은 | 높은 |
| 엔터프라이즈 SSO | SAML 2.0 | 높은 | 매우 높음 |

### 데이터베이스 및 ORM 선택

```
Database & ORM Decision
├─ Relational (SQL)
│   ├─ Node.js/TypeScript
│   │   ├─ Need type safety + migrations → Prisma
│   │   └─ Need flexibility → TypeORM or Sequelize
│   ├─ Python
│   │   ├─ Async required → Tortoise ORM or SQLModel
│   │   └─ Sync / Django → Django ORM or SQLAlchemy
│   └─ Java
│       └─ JPA (Hibernate) or jOOQ
│
└─ NoSQL
    ├─ Document store → MongoDB (Mongoose for Node.js)
    └─ Key-value → Redis (caching, sessions)
```

## 모범 사례

1. **항상 입력 유효성 검사** - 제공된 유효성 검사 미들웨어 사용
2. **정상적으로 오류 처리** - 생성된 오류 핸들러 사용
3. **테스트 작성** - 일관성을 위해 테스트 템플릿을 사용하세요.
4. **환경 변수 사용** - 비밀을 하드코딩하지 마세요.
5. **로깅 구현** - 제공된 로깅 구성 사용
6. **성능 모니터링** - 측정항목 및 알림 설정
7. **보안 우선** - 제공된 인증 설정 사용
8. **API 버전 관리** - 버전 관리 패턴 따르기
9. **코드 문서화** - 자동으로 API 문서 생성
10. **안전한 배포** - 제공된 배포 스크립트 사용

## 일반적인 패턴

### 저장소 패턴
- 우려의 분리
- 쉬운 테스트
- 교체 가능한 구현

### 서비스 계층
- 중앙 집중식 비즈니스 규칙
- 거래 관리
- 오류 처리

### 미들웨어 스택
- 인증
- 승인
- 검증
- 로깅
- 오류 처리

## 문제 해결

### 일반적인 문제

**데이터베이스 연결 오류**
- 연결 문자열 확인
- 데이터베이스가 실행 중인지 확인
- 네트워크 연결을 확인하세요
- 연결 풀 설정 검토

**인증 실패**
- JWT 비밀 확인
- 토큰 만료 확인
- 토큰 형식 검증
- 미들웨어 주문 검토

**빌드 실패**
- TypeScript 구성 확인
- 종속성이 설치되어 있는지 확인
- 오류 메시지 검토
- 구문 오류를 확인하세요.

**배포 문제**
- Docker 이미지 빌드 확인
- Kubernetes 포드 확인
- 로그 검토
- 환경변수 확인

## 품질 체크리스트

### 보안
- [ ] 모든 엔드포인트(Zod/Joi)에 대한 입력 검증
- [ ] 비밀번호 해싱(bcrypt 비용 10+ 또는 Argon2)
- [ ] SQL 주입 방지(매개변수화된 쿼리)
- [ ] 인증 엔드포인트의 속도 제한
- [ ] 보안 헤더(Helmet.js)
- [ ] 비밀에 대한 환경 변수

### 인증 및 승인
- [ ] 강력한 JWT 비밀(256비트)
- [ ] 단기 액세스 토큰(15분)
- [ ] 새로 고침 토큰 교체
- [ ] 보호된 경로에 대한 인증 확인

### 오류 처리
- [ ] 전역 오류 처리기
- [ ] 비동기 오류 처리(express-async-errors)
- [ ] 검증 오류 메시지 지우기
- [ ] 알 수 없는 끝점에 대한 404 처리

### 성능
- [ ] 데이터베이스 연결 풀링
- [ ] 쿼리 최적화(N+1 없음)
- [ ] 캐싱(세션용 Redis, 속도 제한)
- [ ] 응답 압축(gzip/brotli)

### 테스트
- [ ] 서비스/저장소에 대한 단위 테스트
- [ ] API 엔드포인트에 대한 통합 테스트
- [ ] 중요한 경로에 대한 적용 범위가 >80%입니다.
- [ ] 별도의 테스트 데이터베이스

## 추가 리소스

- **자세한 기술 참조**: [REFERENCE.md](REFERENCE.md) 참조
- **코드 예제 및 패턴**: [EXAMPLES.md](EXAMPLES.md) 참조