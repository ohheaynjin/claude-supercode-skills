---
name: spring-boot-engineer
description: Spring Boot 3+, 마이크로서비스 및 클라우드 네이티브 Java 전문가입니다. 가상 스레드, Spring Cloud 및 Reactive Stack을 전문으로 합니다.
---
# 스프링부트 엔지니어

## 목적
Spring Boot 3+를 사용하여 프로덕션급 Java 애플리케이션 구축에 대한 전문 지식을 제공합니다. 마이크로서비스 아키텍처, 클라우드 네이티브 패턴, 반응형 프로그래밍, 가상 스레드를 포함한 최신 Java 기능 활용을 전문으로 합니다.

## 사용 시기
- Spring Boot 애플리케이션 및 마이크로서비스 구축
- Spring Web 또는 WebFlux를 사용하여 REST API 구현
- 인증/권한 부여를 위한 Spring Security 구성
- Spring Data JPA, MongoDB 또는 R2DBC 설정
- Spring Cloud 패턴 구현(Config, Gateway, Circuit Breaker)
- Spring Boot 3.2+에서 가상 스레드 사용
- Project Reactor를 사용하여 반응형 애플리케이션 구축
- Spring Kafka 또는 RabbitMQ와 메시징 통합

## 빠른 시작
**다음과 같은 경우에 이 스킬을 호출하세요:**
- Spring Boot 애플리케이션 및 마이크로서비스 구축
- Spring Web 또는 WebFlux를 사용하여 REST API 구현
- 인증/권한 부여를 위한 Spring Security 구성
- 스프링 데이터 저장소 설정
- Spring Cloud 패턴 구현

**다음과 같은 경우에는 호출하지 마세요.**
- Spring이 없는 일반적인 Java 질문 → java-architect 사용
- Kubernetes 배포 → kubernetes-specialist 사용
- 데이터베이스 설계 → 데이터베이스 관리자 사용
- 프론트엔드 개발 → 적절한 프론트엔드 스킬 사용

## 의사결정 프레임워크
```
Spring Boot Task?
├── API Development → Spring Web (blocking) vs WebFlux (reactive)
├── Data Access → JPA (relational) vs MongoDB (document) vs R2DBC (reactive)
├── Security → OAuth2/OIDC vs JWT vs Basic Auth
├── Messaging → Kafka (high throughput) vs RabbitMQ (routing)
├── Service Communication → REST vs gRPC vs messaging
└── Configuration → Spring Cloud Config vs Kubernetes ConfigMaps
```

## 핵심 워크플로

### 1. 마이크로서비스 개발
1. Spring 초기화 및 필수 스타터를 사용하여 프로젝트 초기화
2. 도메인 모델 및 DTO 정의
3. Spring Data로 저장소 계층 구현
4. 비즈니스 로직으로 서비스 레이어 생성
5. 적절한 오류 처리 기능을 갖춘 REST 컨트롤러 구축
6. 검증, 보안, 관찰 가능성 추가
7. 단위, 통합 및 계약 수준에서 테스트 작성
8. 클라우드 배포를 위한 구성(상태, 지표, 구성)

### 2. 스프링 보안 설정
1. spring-boot-starter-security 종속성 추가
2. 보안 필터 체인 구성 정의
3. 인증 공급자(JWT, OAuth2, LDAP) 구성
4. 엔드포인트에 대한 인증 규칙 설정
5. 필요한 경우 사용자 정의 UserDetailsService 구현
6. CORS 및 CSRF 구성 추가
7. 보안 구성을 철저히 테스트하세요.

### 3. 반응형 애플리케이션 개발
1. Spring Web 대신 WebFlux를 사용하라
2. 반응형 데이터베이스 액세스를 위해 R2DBC 구성
3. 컨트롤러 및 서비스에서 Mono/Flux 반환
4. 비차단 HTTP 호출에 WebClient를 사용하세요.
5. 배압 처리 구현
6. StepVerifier로 테스트
7. 반응 인식 관찰 가능성으로 모니터링

## 모범 사례
- 필드 주입보다 생성자 주입을 사용합니다.
- 프로필 및 ConfigMap을 사용하여 구성을 외부화합니다.
- @ControllerAdvice를 사용하여 적절한 예외 처리 구현
- 상태 및 지표에 대한 액추에이터 엔드포인트 활성화
- 통합 테스트를 위해 Testcontainers를 사용하세요.
- I/O 바인딩 작업 부하에 가상 스레드 활용(Spring Boot 3.2+)

## 안티 패턴
- **필드 주입** → 테스트 가능성을 위해 생성자 주입 사용
- **반응 체인의 차단** → 반응 파이프라인을 비차단 상태로 유지
- **일반 예외 잡기** → 특정 예외를 적절하게 처리
- **하드코딩된 구성** → 환경 변수로 외부화
- **상태 확인 누락** → 항상 Actuator 상태 엔드포인트 노출