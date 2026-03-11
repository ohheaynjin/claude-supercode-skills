# 확장된 하위 상담원 기술 카탈로그

이 문서에는 상담원 기술 형식으로 전환할 가능성이 있는 것으로 식별된 300개 이상의 추가 하위 상담원이 범주 및 우선순위별로 정리되어 있습니다.

## 개요

**현재 변환됨:** 9개 핵심 하위 에이전트
**변환할 남은 수:** 여러 컬렉션에 걸쳐 300개 이상의 하위 에이전트

## 전환 우선순위 매트릭스

### 우선순위 1: 핵심 유틸리티(높은 가치)

이러한 에이전트는 대부분의 개발 워크플로에서 사용되는 기본 기능을 제공합니다.

| 대리인 | 설명 | 도구 | 이론적 해석 |
|-------|-------------|-------|------------|
| **코드 검토자** | 보안에 초점을 맞춘 품질 중심의 코드 검토 | 읽기, Grep, Glob | 모든 개발에 중요 |
| **디버거** | 고급 디버깅 및 근본 원인 분석 | 읽기, Grep, Glob | 워크플로의 일반적인 병목 현상 |
| **리팩토링 전문가** | 코드 리팩토링 및 디자인 패턴 | 읽기, 쓰기, 편집, Bash, Glob, Grep | 코드베이스 품질 향상 |
| **종속성 관리자** | 패키지 관리 및 공급망 보안 | 읽기, 쓰기, 편집, Bash, Glob, Grep | 현대 프로젝트에 매우 중요 |

### 우선 순위 2: 언어 전문가(빈도가 높음)

주요 프레임워크와 기술을 다루는 23개의 언어별 에이전트.

#### JavaScript/TypeScript 생태계
| 에이전트 | 전문성 | 사용 사례 |
|-------|------------|------------|
| **자바스크립트-프로** | 최신 ES2023+, Node.js, Bun, 비동기 패턴 | 바닐라 JS, Node.js 백엔드 |
| **typescript-pro** | TypeScript 5+ 패턴, 제네릭, 유틸리티 유형 | 유형이 안전한 JS 프로젝트 |
| **반응 전문가** | React 18+, Next.js, Zustand, TanStack 쿼리 | React 앱과 라이브러리 |
| **nextjs-개발자** | Next.js 14+, 앱 라우터, 서버 작업 | 풀스택 React 앱 |
| **vue 전문가** | Vue 3 구성 API, Pinia, Nuxt | Vue.js 애플리케이션 |

#### 백엔드 언어
| 에이전트 | 전문성 | 사용 사례 |
|-------|------------|------------|
| **파이썬 프로** | Python 3.11+, 유형 힌트, 비동기, FastAPI | Python 백엔드, 데이터 과학 |
| **골랑프로** | Go 1.21+, 고루틴, 채널, stdlib | 고성능 서비스 |
| **자바 건축가** | Java 21, 스프링 부트 3, 자카르타 EE | 엔터프라이즈 Java 애플리케이션 |
| **스프링 부트 엔지니어** | 스프링 부트 3+, 스프링 클라우드, Kubernetes | Spring 기반 마이크로서비스 |
| **dotnet-코어 전문가** | .NET 8 크로스 플랫폼, MAUI, EF Core | C#/.NET 애플리케이션 |
| **녹슨 엔지니어** | Rust 비동기, 소유권, FFI, WebAssembly | 시스템 프로그래밍, WASM |

#### 모바일 및 전문화
| 에이전트 | 전문성 | 사용 사례 |
|-------|------------|------------|
| **플러터 전문가** | Flutter 3+, Dart, Firebase, 플랫폼 채널 | 크로스 플랫폼 모바일 |
| **kotlin 전문가** | Kotlin 2.0, KMP, 코루틴, Ktor | 안드로이드 개발 |
| **스위프트 전문가** | iOS/macOS, SwiftUI, 결합, 동시성 | 애플 플랫폼 |

#### 기타 언어
- **cpp-pro** - C++20, 최신 기능, 성능 최적화
- **csharp-개발자** - .NET 8, C# 12, ASP.NET Core, EF Core
- **php-pro** - PHP 8.2+, 최신 패턴, Composer
- **ruby-on-rails** - Ruby on Rails, Hotwire, Turbo, Stimulus
- **laravel 전문가** - Laravel 10+, PHP 8.2, Eloquent, Livewire

### 우선순위 3: 인프라 및 DevOps(중요 기반)

클라우드, 데이터베이스, 운영을 담당하는 에이전트 11개.

| 대리인 | 집중하다 | 도구 | 이론적 해석 |
|-------|-------|-------|------------|
| **클라우드 설계자** | AWS/Azure/GCP, 멀티 클라우드, 비용 최적화 | 읽기, 쓰기, 편집, Bash, Glob, Grep | 클라우드 배포 전략 |
| **쿠버네티스 전문가** | K8s 오케스트레이션, Helm, 오퍼레이터 | 읽기, 쓰기, 편집, Bash, Glob, Grep | 컨테이너 오케스트레이션 |
| **배포 엔지니어** | CI/CD, 도커, 쿠버네티스, GitOps | 읽기, 쓰기, 편집, Bash, Glob, Grep | 배포 자동화 |
| **데이터베이스 관리자** | PostgreSQL/MySQL, HA, 백업, 모니터링 | 읽기, 쓰기, 편집, Bash, Glob, Grep | 데이터베이스 관리 |
| **재엔지니어** | 사이트 안정성, SLO, 오류 예산 | 읽기, 쓰기, 편집, Bash, Glob, Grep | 생산 신뢰성 |
| **데브옵스 엔지니어** | CI/CD 자동화, IaC, 모니터링, SRE | 읽기, 쓰기, 편집, Bash, Glob, Grep | DevOps 워크플로 |

### 우선순위 4: 품질 및 보안(규정 준수 중요)

코드 품질, 보안 및 규정 준수에 중점을 둔 13명의 에이전트.

| 대리인 | 전문 | 도구 | 이론적 해석 |
|-------|-----------|-------|------------|
| **보안 감사자** | 보안 취약점, OWASP | 읽기, Grep, Glob | 보안 검토 |
| **접근성 테스터** | WCAG 2.1 AA 규정 준수, A11y 감사 | 읽기, Grep, Glob | 접근성 준수 |
| **침투 테스터** | 윤리적 해킹, 취약점 평가 | 읽기, Grep, Glob | 보안 테스트 |
| **성능 엔지니어** | 성능 최적화, 프로파일링 | 읽기, Grep, Glob | 성과 검토 |
| **규정 준수 감사자** | SOC2, HIPAA, GDPR 준수 | 읽기, Grep, Glob | 규제 준수 |
| **코드 검토자** | 코드 품질, 보안, 모범 사례 | 읽기, Grep, Glob | 품질 게이트 |

### 우선순위 5: 아키텍처 및 디자인(전략적)

시스템 아키텍처 및 API 설계에 중점을 둔 여러 에이전트.

| 대리인 | 집중하다 | 도구 | 이론적 해석 |
|-------|-------|-------|------------|
| **API 디자이너** | OpenAPI 3.1을 사용하는 REST/GraphQL API 설계자 | 읽기, 쓰기, 편집, Bash, Glob, Grep | API 디자인 |
| **마이크로서비스 설계자** | 분산 시스템, 서비스 분해 | 읽기, 쓰기, 편집, Bash, Glob, Grep | 마이크로서비스 |
| **백엔드 개발자** | 확장 가능한 API, 데이터베이스 설계, 인증 | 읽기, 쓰기, 편집, Bash, Glob, Grep | 백엔드 아키텍처 |
| **프론트엔드 개발자** | React/Vue/Angular UI/UX, 접근성 | 읽기, 쓰기, 편집, Bash, Glob, Grep | 프런트엔드 아키텍처 |
| **UI 디자이너** | 시각 디자인, 디자인 시스템, 상호 작용 패턴 | 읽기, 쓰기, 편집, Bash, Glob, Grep | UI/UX 디자인 |

### 우선순위 6: 데이터 및 AI(새로운 중요성)

데이터 엔지니어링, ML, AI 시스템을 담당하는 에이전트 13개.

| 대리인 | 집중하다 | 도구 | 이론적 해석 |
|-------|-------|-------|------------|
| **데이터 엔지니어** | ETL/ELT, 데이터 레이크, 스트리밍(Spark, Kafka) | 읽기, 쓰기, 편집, Bash, Glob, Grep | 데이터 파이프라인 |
| **머신러닝 엔지니어** | ML 시스템, TensorFlow, PyTorch | 읽기, 쓰기, 편집, Bash, Glob, Grep | ML 인프라 |
| **mlops-엔지니어** | MLOps, 모델 배포, 모니터링 | 읽기, 쓰기, 편집, Bash, Glob, Grep | ML 작업 |
| **llm-건축가** | LLM 아키텍처, RAG, 미세 조정 | 읽기, 쓰기, 편집, Bash, Glob, Grep | LLM 통합 |
| **데이터 과학자** | 분석, ML 모델, 통계 분석 | 읽기, 쓰기, 편집, Bash, Glob, Grep | 데이터 분석 |
| **데이터베이스 최적화 프로그램** | 쿼리 최적화, 인덱싱, 성능 | 읽기, 쓰기, 편집, Bash, Glob, Grep | DB 성능 |

### 우선순위 7: 개발자 경험(생산성)

개발자 워크플로우와 도구를 개선하는 9명의 에이전트.

| 대리인 | 전문 | 도구 | 이론적 해석 |
|-------|-----------|-------|------------|
| **git-워크플로-관리자** | Git 워크플로, 분기 전략 | 읽기, 쓰기, 편집, Bash, Glob, Grep | Git 프로세스 |
| **툴링 엔지니어** | 개발자 도구, 플러그인, 확장 | 읽기, 쓰기, 편집, Bash, Glob, Grep | 맞춤형 도구 |
| **cli 개발자** | CLI 도구, 클릭, argparse, UX | 읽기, 쓰기, 편집, Bash, Glob, Grep | CLI 개발 |
| **레거시 현대화** | 레거시 코드 현대화, 리팩토링 | 읽기, 쓰기, 편집, Bash, Glob, Grep | 기술 부채 감소 |

### 우선순위 8: 비즈니스 및 제품(교차 도메인)

제품 관리, 비즈니스 분석 및 문서화를 위한 10명의 에이전트.

| 대리인 | 집중하다 | 도구 | 이론적 해석 |
|-------|-------|-------|------------|
| **제품 관리자** | 제품 전략, 로드맵, 우선순위 | 읽기, 쓰기, 편집, Glob, Grep, WebFetch, WebSearch | 상품기획 |
| **비즈니스 분석가** | 요구 사항, 비즈니스 분석 | 읽기, 쓰기, 편집, Glob, Grep | 요구사항 수집 |
| **프로젝트 관리자** | 프로젝트 관리, 납품 | 읽기, 쓰기, 편집, Glob, Grep | 프로젝트 조정 |
| **기술 작가** | 기술 문서, 문서 | 읽기, 쓰기, 편집, Glob, Grep, WebFetch, WebSearch | 선적 서류 비치 |
| **ux-연구원** | UX 연구, 사용자 테스트 | 읽기, 쓰기, 편집, Glob, Grep, WebFetch, WebSearch | UX 검증 |

### 우선순위 9: 전문 도메인(틈새이지만 중요함)

특수한 요구 사항을 충족하는 10개의 도메인별 에이전트.

| 대리인 | 도메인 | 도구 | 이론적 해석 |
|-------|---------|-------|------------|
| **API-다큐멘터리** | API 문서(OpenAPI, Swagger) | 읽기, 쓰기, 편집, Glob, Grep | API 문서 |
| **블록체인 개발자** | Web3, 스마트 계약, DeFi | 읽기, 쓰기, 편집, Bash, Glob, Grep | Web3/블록체인 |
| **임베디드 시스템** | 임베디드, 실시간, RTOS | 읽기, 쓰기, 편집, Bash, Glob, Grep | 임베디드/IoT |
| **핀테크 엔지니어** | 금융 기술, 거래, 규정 준수 | 읽기, 쓰기, 편집, Bash, Glob, Grep | 핀테크 |
| **게임 개발자** | 게임 개발, 유니티, 언리얼 | 읽기, 쓰기, 편집, Bash, Glob, Grep | 게임 개발 |
| **IoT 엔지니어** | IoT, 엣지 컴퓨팅, 센서 | 읽기, 쓰기, 편집, Bash, Glob, Grep | IoT 솔루션 |
| **결제 통합** | 결제 시스템(Stripe, PayPal) | 읽기, 쓰기, 편집, Bash, Glob, Grep | 결제 처리 |
| **양적 분석가** | 정량분석, 금융 | 읽기, 쓰기, 편집, Bash, Glob, Grep | 금융에 대하여 |
| **위험 관리자** | 위험 평가, 관리 | 읽기, 쓰기, 편집, Bash, Glob, Grep | 위험 분석 |
| **서구 전문가** | SEO, 최적화, 분석 | 읽기, 쓰기, 편집, Bash, Glob, Grep | SEO/최적화 |

### 우선순위 10: 메타 및 오케스트레이션(워크플로)

업무를 조정하고 대리인을 관리하는 8명의 대리인.

| 대리인 | 목적 | 도구 | 이론적 해석 |
|-------|---------|-------|------------|
| **대리인-주최자** | 다중 에이전트 코디네이터, 팀 조립 | 읽기, 쓰기, 편집, Glob, Grep | 상담원 조정 |
| **워크플로 조정자** | 복잡한 작업 흐름 자동화 | 읽기, 쓰기, 편집, Glob, Grep | 워크플로우 자동화 |
| **작업 배포자** | 작업 할당, 로드 밸런싱 | 읽기, 쓰기, 편집, Glob, Grep | 업무분배 |
| **지식 합성기** | 지식 집합, 종합 | 읽기, 쓰기, 편집, Glob, Grep | 지식경영 |

### 우선순위 11: 연구 및 분석(정보)

포괄적인 연구 및 분석을 위한 6가지 에이전트.

| 대리인 | 전문 | 도구 | 이론적 해석 |
|-------|-----------|-------|------------|
| **연구-분석가** | 종합적인 연구, 합성 | 읽기, Grep, Glob, WebFetch, WebSearch | 심층 연구 |
| **검색 전문가** | 고급 정보 검색 | 읽기, Grep, Glob, WebFetch, WebSearch | 연구 쿼리 |
| **트렌드 분석가** | 추세 분석, 예측 | 읽기, Grep, Glob, WebFetch, WebSearch | 시장 동향 |
| **경쟁 분석가** | 경쟁력 있는 정보 | 읽기, Grep, Glob, WebFetch, WebSearch | 경쟁 분석 |
| **시장 조사자** | 시장분석, 소비자 인사이트 | 읽기, Grep, Glob, WebFetch, WebSearch | 시장 조사 |
| **데이터 연구원** | 데이터 발견, 분석 | 읽기, Grep, Glob, WebFetch, WebSearch | 데이터 연구 |

## 체계적인 전환 전략

### 1단계: 영향력이 큰 에이전트(즉시)

영향력이 가장 큰 상담원 20명을 먼저 전환하세요.

**핵심 유틸리티**(에이전트 4개):
- 코드 검토자
- 디버거
- 리팩토링 전문가
- 종속성 관리자

**최고의 언어 전문가**(상담사 8명):
- 자바스크립트 프로
- typescript-pro
- 반응 전문가
- 파이썬 프로
- 골랑프로
- 자바 건축가
- nextjs 개발자
- vue 전문가

**중요 인프라**(에이전트 8명):
- 클라우드 설계자
- kubernetes 전문가
- 배포 엔지니어
- 데이터베이스 관리자
- SRE 엔지니어
- 데브옵스 엔지니어
- 보안 감사관
- 성능 엔지니어

### 2단계: 언어 지원(단기)

나머지 언어 전문가 변환(에이전트 15명):

- 백엔드 언어: spring-boot-engineer, dotnet-core-expert, Rust-engineer, cpp-pro
- 모바일: flutter 전문가, kotlin 전문가, Swift 전문가
- 웹 프레임워크: Angle-architect, vue-expert, laravel-specialist
- 기타: php-pro, 레일스 전문가

### 3단계: 도메인 전문가(중기)

우선순위에 따라 도메인별 에이전트를 변환합니다.

**품질 및 보안**(에이전트 8명):
- 접근성 테스터
- 침투 테스터
- 규정 준수 감사관
- 코드 검토자
- qa 전문가
- 테스트 자동화
- 오류 탐지
- 테라폼 엔지니어

**데이터 및 AI**(에이전트 10개):
- 데이터 엔지니어
- 머신러닝 엔지니어
- mlops 엔지니어
- LLM 건축가
- 데이터 과학자
- 데이터베이스 최적화 프로그램
- nlp 엔지니어
- AI 엔지니어
- ml-엔지니어
- 신속한 엔지니어

**건축 및 디자인**(에이전트 4명):
- API 디자이너
- 마이크로서비스 아키텍트
-graphql-건축가
- 풀스택 개발자

### 4단계: 비즈니스 및 전문 분야(장기)

비즈니스 및 전문 에이전트 전환:

**비즈니스 및 제품**(에이전트 8명):
- 제품 관리자
- 비즈니스 분석가
- 프로젝트 관리자
- 기술 작가
- ux-연구원
- 스크럼 마스터
- 고객-성공-관리자
- 영업 엔지니어

**특수 도메인**(에이전트 8명):
- API 문서
- 블록체인 개발자
- 임베디드 시스템
- 핀테크 엔지니어
- 게임 개발자
- IoT 엔지니어
- 결제 통합
- SEO 전문가

**개발자 경험**(에이전트 5명):
-git-워크플로-관리자
- 툴링 엔지니어
- CLI 개발자
- 레거시 현대화
- dx-옵티마이저

### 5단계: 메타 및 오케스트레이션(장기)

조정 및 연구 에이전트 변환:

**메타 및 오케스트레이션**(에이전트 5명):
- 대리인-주최자
- 작업 흐름 조정자
- 작업 분배자
- 지식 합성기
- 성능 모니터

**연구 및 분석**(에이전트 6명):
- 연구 분석가
- 검색 전문가
- 트렌드 분석가
- 경쟁 분석가
- 시장 조사원
- 데이터 연구원

## 변환 템플릿

### 언어 전문가 템플릿

언어별 에이전트를 변환하려면 다음 구조를 사용하십시오.

```markdown
---
name: [language]-development
description: Expert [language] developer with mastery of [version features], [frameworks], and [ecosystem patterns]. Use when developing [language] applications, working with [common libraries], or needing [language]-specific guidance.
---

# [Language] Development Skill

You are an expert [language] developer with deep knowledge of [version] features, modern patterns, and the [language] ecosystem.

## Core Expertise

### Language Features
- [version] capabilities and syntax
- Type system features
- Standard library usage
- Performance characteristics

### Frameworks & Libraries
- [framework1] - when to use
- [framework2] - use cases
- [library patterns] - common libraries
- Ecosystem best practices

### Development Patterns
- Code organization
- Error handling
- Testing approaches
- Performance optimization
```

### 인프라 전문가 템플릿

인프라/DevOps 에이전트 변환의 ​​경우:

```markdown
---
name: [domain]-infrastructure
description: [domain] specialist with expertise in [cloud platforms], [technologies], and [operational patterns]. Use when designing [domain] architecture, deploying to [platforms], or managing [domain] operations.
---

# [Domain] Infrastructure Skill

You are an expert [domain] engineer with comprehensive knowledge of [platforms], [tools], and operational excellence.

## Core Capabilities

### Platform Expertise
- AWS/Azure/GCP services
- Multi-cloud strategies
- Cost optimization
- Security best practices

### Technologies
- [tool1] patterns and best practices
- [tool2] integration strategies
- [tool3] optimization techniques

### Operational Excellence
- Monitoring and observability
- Incident response
- Capacity planning
- Reliability engineering
```

## 추정

### 노력 필요

- **1단계**(에이전트 20개): ~4시간
- **2단계**(에이전트 15명): ~3시간
- **3단계**(에이전트 22개): ~4.5시간
- **4단계**(에이전트 21개): ~4.5시간
- **5단계**(에이전트 11개): ~2.5시간

**총 예상 시간**: 우선 순위가 높은 상담원 89명의 경우 최대 18.5시간

### 전체 카탈로그 변환

300개 이상의 에이전트를 모두 변환하려면 대략 다음이 필요합니다.
- **시간**: ~60시간 이상
- **스킬 파일**: 300개 이상의 SKILL.md 파일
- **검증**: 모든 기술에 대한 광범위한 테스트
- **문서**: 지원 가이드 및 템플릿

## 추천

### 옵션 1: 타겟 전환(권장)

영향력이 가장 큰 상담원 50~100명을 먼저 전환하세요.
- 가장 일반적으로 사용되는 기능에 중점을 둡니다.
- 인프라, 보안, 언어 전문가 우선순위
- 틈새시장/전문 에이전트를 나중 단계로 연기
- **투자 시간**: 20~25시간
- **적용 범위**: 일반적인 사용 사례의 80-90%

### 옵션 2: 전체 체계적 변환

설정된 템플릿을 사용하여 모든 에이전트를 변환합니다.
- 카테고리별 상담사별 템플릿 생성
- 유사한 에이전트에 대해서는 일괄 처리를 사용합니다.
- 복잡한 기술에 대한 점진적 공개 구현
- **시간 투자**: 60시간 이상
- **적용 범위**: 문서화된 에이전트 100%

### 옵션 3: 주문형 전환

사용자 요청에 따라 필요에 따라 에이전트를 변환합니다.
- 우선순위가 가장 높은 에이전트부터 시작하세요.
- 사용자가 요청하면 특정 에이전트를 변환합니다.
- **시간 투자**: 가변적, 최소한의 초기 투자
- **커버리지**: 필요에 따라 유기적으로 확장

## 다음 단계

1. **접근 방식 선택**: 타겟 전환, 전체 전환, 주문형 전환 중에서 결정
2. **우선순위 정의**: 먼저 변환할 상담원/카테고리를 선택하세요.
3. **템플릿 생성**: 상담원 카테고리별 템플릿 개발
4. **변환 실행**: 선택한 상담원을 체계적으로 변환합니다.
5. **철저하게 검증**: 마무리하기 전에 각 기술을 테스트하세요.
6. **문서화 프로세스**: 학습 내용으로 변환 가이드 업데이트

## 자원

모든 기술은 다음을 참조해야 합니다.
- 공식 인류학 기술 문서
- 인류학/기술 저장소 예시
- SKILL-VALIDATION-GUIDE.md의 모범 사례 가이드
- CONVERSION-GUIDE.md의 변환 프로세스

## 요약

- **9개 스킬 완료**: 핵심 유틸리티(탐색, 오라클, 라이브러리언 등)
- **남은 스킬 300개 이상**: 우선순위 및 카테고리별로 정리
- **명확한 전환 전략**: 예상 시간이 포함된 5단계
- **제공되는 템플릿**: 언어, 인프라 및 전문 에이전트용
- **다양한 옵션**: 타겟(25시간), 전체(60시간) 또는 주문형 변환

귀하의 우선순위와 시간적 제약에 따라 체계적인 전환을 진행할 준비가 되어 있습니다.