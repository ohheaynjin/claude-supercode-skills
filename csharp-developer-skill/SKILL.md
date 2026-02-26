---
name: csharp-developer
description: ASP.NET Core, EF Core 및 최신 엔터프라이즈 개발에 대한 전문 지식을 갖춘 .NET 8 및 C# 12 전문가입니다. C# 애플리케이션 빌드, .NET 작업, ASP.NET Core API 구현 또는 Entity Framework 사용 시 사용합니다.
---
# C# 개발자

## 목적
ASP.NET Core 웹 애플리케이션, Entity Framework Core 데이터 액세스, 엔터프라이즈 애플리케이션 패턴을 포함한 최신 C# 및 .NET 개발에 대한 전문 지식을 제공합니다. C# 12 기능과 .NET 8 모범 사례를 다룹니다.

## 사용 시기
- .NET 8을 사용하여 C# 애플리케이션 구축
- ASP.NET Core 웹 API 개발
- Entity Framework Core 데이터 액세스 구현
- 최신 C# 기능(레코드, 패턴 등) 사용
- 엔터프라이즈 .NET 애플리케이션 구축
- xUnit/NUnit을 사용하여 단위 테스트 작성
- 의존성 주입 패턴 구현

## 빠른 시작
**다음과 같은 경우에 이 스킬을 호출하세요:**
- .NET 8을 사용하여 C# 애플리케이션 구축
- ASP.NET Core 웹 API 개발
- Entity Framework Core 데이터 액세스 구현
- 최신 C# 기능 사용
- 엔터프라이즈 .NET 애플리케이션 구축

**다음과 같은 경우에는 호출하지 마세요.**
- 크로스 플랫폼 .NET MAUI 앱 빌드(dotnet-core-expert 사용)
- .NET Framework 4.8로 작업(dotnet-framework-4.8-expert 사용)
- Windows 데스크톱 앱 빌드(windows-app-developer 사용)
- Azure 관련 인프라(azure-infra-engineer 사용)

## 의사결정 프레임워크
```
Project Type:
├── Web API → ASP.NET Core Minimal API or Controllers
├── Web App → Blazor or Razor Pages
├── Background service → Worker Service
├── Desktop → WPF, WinUI, or MAUI
└── Library → .NET Standard or .NET 8

Data Access:
├── SQL with ORM → Entity Framework Core
├── SQL with control → Dapper
├── NoSQL → MongoDB driver or Cosmos SDK
└── Multiple DBs → Repository pattern
```
## 핵심 워크플로

### 1. ASP.NET Core API 개발
1. 적절한 템플릿으로 프로젝트 생성
2. 종속성 주입 구성
3. 도메인 모델 구현
4. 마이그레이션을 통해 EF Core 설정
5. 컨트롤러 또는 최소 API 엔드포인트 생성
6. 유효성 검사 및 오류 처리 추가
7. 인증/권한 부여 구현
8. OpenAPI 문서 추가

### 2. Entity Framework 핵심 설정
1. 엔터티 모델 정의
2. DbContext 구성
3. 관계 및 제약 조건 설정
4. 초기 마이그레이션 생성
5. 필요한 경우 저장소 패턴 구현
6. 쿼리 최적화 추가
7. 연결 복원력 구성

### 3. 테스트 전략
1. xUnit 또는 NUnit 프로젝트 설정
2. 모의 테스트로 단위 테스트 만들기
3. 통합 테스트 구현
4. API 테스트에 WebApplicationFactory 사용
5. 테스트 데이터베이스 고정 장치 추가
6. CI 테스트 파이프라인 구성

## 모범 사례
- DTO 및 불변 데이터에 대한 레코드 사용
- 더욱 깔끔한 코드를 위해 패턴 매칭 활용
- nullable 참조 유형을 사용하세요.
- 비동기 정리를 위해 IAsyncDisposable 구현
- C# 12에서 기본 생성자를 사용합니다.
- 포함에 대한 EF Core 쿼리 분할 구성

## 안티 패턴
| 안티 패턴 | 문제 | 올바른 접근 |
|---------------|---------|------|
| 서비스 찾기 | 숨겨진 종속성 | 생성자 주입 |
| 비동기 무효 | 처리되지 않은 예외 | 어디서나 비동기 작업 |
| N+1 쿼리 | 성능 문제 | 포함() 또는 프로젝션 |
| 생성자에서 던지기 | 다루기 힘든 | 팩토리 메소드 사용 |
| 문자열 기반 구성 | 런타임 오류 | 강력한 유형의 옵션 |