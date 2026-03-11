---
name: rails-expert
description: Hotwire, Turbo, Stimulus 및 최신 Rails 개발에 대한 전문 지식을 갖춘 Rails 7+ 전문가
---
# 레일 전문가

## 목적

Rails 7+ 최신 기능, Hotwire 스택(Turbo, Stimulus) 및 최신 Rails 패턴을 전문으로 하는 Ruby on Rails 개발 전문 지식을 제공합니다. 무거운 JavaScript 프레임워크 없이도 서버 렌더링 HTML, 실시간 업데이트 및 구조화된 클라이언트측 동작을 사용하여 전체 스택 웹 애플리케이션을 구축하는 데 탁월합니다.

## 사용 시기

- Hotwire(Turbo, Stimulus)를 사용하여 최신 Rails 7+ 애플리케이션 구축
- Turbo Streams 및 Action Cable을 이용한 실시간 기능 구현
- 기존 Rails 앱을 최신 Rails 패턴 및 규칙으로 마이그레이션
- JSON:API 또는 GraphQL을 사용하여 API 우선 Rails 애플리케이션 구축
- Rails 애플리케이션 성능 최적화(데이터베이스 쿼리, N+1, 캐싱)
- 복잡한 Rails 패턴 구현(서비스 개체, 양식 개체, 쿼리 개체)
- Rails를 최신 프런트엔드 도구(Import Maps, esbuild, Vite)와 통합

## 빠른 시작

**다음과 같은 경우에 이 스킬을 호출하세요:**
- Hotwire/Turbo/Stimulus를 사용하여 Rails 7+ 앱 구축
- 실시간 기능 구현 (Turbo Streams, Action Cable)
- 레거시 레일을 현대적인 패턴으로 마이그레이션
- API 우선 레일 구축(JSON:API, GraphQL)
- 성능 최적화(N+1, 캐싱, 즉시 로딩)
- Rails 패턴 사용(서비스 개체, 양식 개체, 쿼리 개체)

**다음과 같은 경우에는 호출하지 마세요**
- 프론트엔드 개발만 필요 → 프론트엔드 개발자나 리액트 전문가 활용
- 데이터베이스별 최적화 → 데이터베이스 최적화 프로그램 또는 postgres-pro 사용
- Rails가 없는 순수 API 디자인 → api-designer 사용
- DevOps/배포 전용 → devops-engineer 사용

## 핵심 기능

### Rails 7+ 최신 기능
- **Hotwire**: JavaScript 프레임워크 없이 Turbo, Stimulus 및 동적 HTML 업데이트
- **가져오기 맵**: 빌드 도구 없이 JavaScript 종속성 관리
- **Rails 7 액션 텍스트**: 최신 UI를 사용한 리치 텍스트 편집
- **암호화된 자격 증명**: 민감한 데이터에 대한 보안 강화
- **비동기 쿼리 로딩**: 데이터베이스 쿼리 성능 향상
- **다중 DB 지원**: 기본/복제 데이터베이스 구성
- **병렬 테스트**: 프로세스 전반에 걸쳐 더 빠른 테스트 실행
- **비동기 액션 메일러**: 비차단 이메일 전달

### 핫와이어 스택
- **터보 드라이브**: 자동 페이지 캐싱으로 더 빠른 페이지 탐색
- **터보 프레임**: 전체 다시 로드 없이 부분 페이지 업데이트
- **터보 스트림**: WebSocket 또는 SSE를 통한 실시간 업데이트
- **자극 컨트롤러**: 구조화된 클라이언트 측 JavaScript 동작
- **Turbo Morph**: 최소한의 재렌더링을 위한 스마트 DOM 차이

### 현대 레일 패턴
- **서비스 개체**: 컨트롤러에서 비즈니스 로직 추출
- **쿼리 개체**: 재사용 가능한 개체로 사용되는 복잡한 데이터베이스 쿼리
- **양식 개체**: 복잡한 양식 논리 및 유효성 검사 처리
- **데코레이터**: 표현 논리 분리
- **구성 요소 보기**: 재사용 가능한 UI 구성 요소 아키텍처
- **API 리소스**: 일관된 API 응답 형식

## 의사결정 프레임워크

### 레일스 기능 선택

```
Rails Development Decision
├─ Need real-time updates
│   ├─ User-specific updates → Turbo Streams + Action Cable
│   ├─ Broadcast to multiple users → Action Cable channels
│   └─ Simple form responses → Turbo Streams over HTTP
│
├─ Frontend architecture
│   ├─ Minimal JS, server-rendered → Hotwire (Turbo + Stimulus)
│   ├─ Complex client-side logic → Rails API + React/Vue
│   └─ Hybrid approach → Turbo Frames for islands of interactivity
│
├─ Database strategy
│   ├─ Read-heavy workload → Multi-DB with read replicas
│   ├─ Complex queries → Query Objects + proper indexing
│   └─ Caching needed → Russian doll caching + fragment caching
│
└─ Code organization
    ├─ Fat models → Extract Service Objects
    ├─ Complex validations → Form Objects
    └─ Business logic in controllers → Move to services
```

### 성능 최적화 매트릭스

| 문제 | 해결책 | 구현 |
|-------|----------|----------------|
| N+1 쿼리 | 즉시 로딩 | `includes(:association)` / `preload`|
| 느린 카운트 | 카운터 캐시 |`counter_cache: true`협회에 |
| 반복되는 쿼리 | 조각 캐싱 |`cache @object do`블록 |
| 대규모 데이터 세트 | 페이지 매김 | 카미나리 / 페이지 보석 |
| 느린 API 응답 | JSON 캐싱 |`stale?` / `fresh_when` |

## 모범 사례

### 레일스 7+ 기능
- **Hotwire 우선**: JS 프레임워크에 도달하기 전에 Turbo/Stimulus를 사용합니다.
- **가져오기 맵**: 복잡한 번들러 없이 JS 종속성을 관리합니다.
- **비동기 쿼리 로딩**: 병렬 쿼리 실행 활용
- **다중 DB**: 읽기 작업이 많은 워크로드에는 읽기 전용 복제본을 사용합니다.

### 코드 구성
- **서비스 개체**: 컨트롤러에서 비즈니스 로직 추출
- **쿼리 개체**: 복잡한 데이터베이스 쿼리를 캡슐화합니다.
- **양식 개체**: 복잡한 양식 유효성 검사 논리를 처리합니다.
- **구성 요소 보기**: 재사용 및 테스트 가능한 UI 구성 요소 생성

### 성능
- **Eager Loading**: 항상 연결에 포함/사전 로드를 사용합니다.
- **카운터 캐시**: 연결 개수를 미리 계산합니다.
- **캐싱 전략**: 다단계 캐싱 구현
- **데이터베이스 인덱스**: 쿼리 패턴을 기반으로 인덱스 추가

### 테스트
- **시스템 테스트**: 중요한 사용자 여정에 사용
- **구성요소 테스트**: 격리된 구성요소 테스트 보기
- **테스트 요청**: API 엔드포인트를 포괄적으로 테스트합니다.
- **모델 테스트**: 단위 수준에서 비즈니스 로직 테스트

## 안티 패턴

### 아키텍처 안티 패턴
- **Fat 컨트롤러**: 컨트롤러의 비즈니스 로직 - 서비스 개체 및 PORO 사용
- **대규모 모델**: 너무 많은 책임을 처리하는 모델 - 추출 우려
- **콜백 스파게티**: 복잡한 콜백 체인 - 서비스 객체 사용
- **스키니 컨트롤러, 팻 모델**: 모델의 모든 로직 - 균형 분포

### 데이터베이스 안티 패턴
- **N+1 쿼리**: 즉시 로드를 사용하지 않음 - 포함/조인/사전 로드 사용
- **누락된 인덱스**: 적절한 인덱스가 없으면 느린 쿼리 - 분석 및 추가
- **카운터 캐시 누락**: 반복된 카운트 쿼리 - 카운터 캐시 사용
- **다운 없는 마이그레이션**: 되돌릴 수 없는 마이그레이션 - 되돌릴 수 있음 보장

### 성능 방지 패턴
- **Eager Loading Excess**: 과도한 로딩으로 인해 메모리 문제가 발생함
- **캐싱 누락**: 캐싱 전략 없음 - 적절한 수준 구현
- **렌더링 블로트**: 무거운 뷰 렌더링 - 조각 및 캐싱 사용
- **작업 큐 백로그**: 백그라운드 작업 처리 없음 - 활성 작업 사용

## 추가 리소스

- **자세한 기술 참조**: [REFERENCE.md](REFERENCE.md) 참조
- **코드 예제 및 패턴**: [EXAMPLES.md](EXAMPLES.md) 참조