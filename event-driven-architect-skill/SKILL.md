---
name: event-driven-architect
description: EDA(Event-Driven Architecture)를 사용하여 비동기식 분리 시스템을 설계하는 전문가입니다. AsyncAPI, Event Mesh 및 CloudEvents 표준을 전문으로 합니다. 이벤트 기반 시스템을 설계하거나, 메시지 대기열을 구현하거나, 비동기식 마이크로서비스를 구축할 때 사용합니다.
---
# 이벤트 중심 아키텍트

## 목적
이벤트 중심 아키텍처 설계 및 구현에 대한 전문 지식을 제공합니다. 확장 가능하고 분리된 시스템을 구축하기 위한 메시지 브로커, 이벤트 소싱, CQRS 및 CloudEvents 및 AsyncAPI와 같은 표준을 다룹니다.

## 사용 시기
- 이벤트 기반 아키텍처 설계
- 메시지 큐 및 브로커 구현
- 이벤트 소싱 시스템 구축
- CQRS 패턴 구현
- AsyncAPI 사양 생성
- 이벤트 메시 토폴로지 설계
- 비동기식 마이크로서비스 구축

## 빠른 시작
**다음과 같은 경우에 이 스킬을 호출하세요:**
- 이벤트 기반 아키텍처 설계
- 메시지 큐 및 브로커 구현
- 이벤트 소싱 시스템 구축
- CQRS 패턴 구현
- AsyncAPI 사양 생성

**다음과 같은 경우에는 호출하지 마세요.**
- 동기식 REST API 구축(api-designer 사용)
- Kafka 인프라 설정(데이터 엔지니어 사용)
- 워크플로 오케스트레이션 구축(워크플로 오케스트레이터 사용)
- GraphQL API 설계(graphql-architect 사용)

## 의사결정 프레임워크
```
Message Broker Selection:
├── High throughput, streaming → Kafka
├── Flexible routing → RabbitMQ
├── Cloud-native, serverless → EventBridge, Pub/Sub
├── Simple queuing → SQS, Redis Streams
└── Enterprise integration → Azure Service Bus

Pattern Selection:
├── Audit/replay needed → Event Sourcing
├── Read/write separation → CQRS
├── Simple async → Pub/Sub
├── Guaranteed delivery → Transactional outbox
└── Complex routing → Message router
```
## 핵심 워크플로

### 1. 이벤트 중심 시스템 설계
1. 도메인 이벤트 식별
2. 이벤트 스키마 정의(CloudEvents)
3. 메시지 브로커 선택
4. 디자인 주제/대기열 구조
5. 소비자 그룹 정의
6. 배달 못한 편지 처리 계획
7. AsyncAPI를 사용한 문서화

### 2. 이벤트 소싱 구현
1. 집계 경계 정의
2. 디자인 이벤트 유형
3. 이벤트 스토어 구현
4. 프로젝션 핸들러 구축
5. 읽기 모델 생성
6. 스키마 진화 처리
7. 스냅샷 전략 계획

### 3. AsyncAPI 사양
1. 서버 및 프로토콜 정의
2. 채널 설명(주제/대기열)
3. 메시지 스키마 정의
4. 문서 작업(pub/sub)
5. 보안 체계 추가
6. 문서 생성
7. 코드 생성 활성화

## 모범 사례
- 상호 운용성을 위해 CloudEvents 형식을 사용합니다.
- 멱등성 소비자 설계
- 배달 못한 편지 대기열 구현
- 이벤트 스키마를 신중하게 버전 관리하세요.
- 소비자 지연 모니터링
- 최소 1회 배송 계획

## 안티 패턴
| 안티 패턴 | 문제 | 올바른 접근 |
|---------------|---------|------|
| 비동기에 비해 동기 | 목적을 무너뜨린다 | 적절한 패턴 사용 |
| 멱등성 없음 | 중복 처리 | 멱등성 처리기 설계 |
| 순서를 무시하다 | 데이터 일관성 문제 | 필요한 경우 키로 파티션하기 |
| 대규모 이벤트 | 네트워크 오버헤드 | 소규모 이벤트, 세부정보 가져오기 |
| 스키마 진화 없음 | 주요 변경 사항 | 버전 관리 전략 |