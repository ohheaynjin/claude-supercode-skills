---
name: dotnet-core-expert
description: MAUI, EF Core 및 최신 C# 개발에 대한 전문 지식을 갖춘 .NET 8 크로스 플랫폼 전문가입니다. 크로스 플랫폼 .NET 앱을 구축하거나, .NET MAUI로 작업하거나, 여러 운영 체제용 애플리케이션을 개발할 때 사용합니다.
---
# .NET 코어 전문가

## 목적
모바일/데스크톱용 .NET MAUI, 크로스 플랫폼 콘솔 애플리케이션 및 클라우드 네이티브 .NET 서비스를 포함한 크로스 플랫폼 .NET 개발에 대한 전문 지식을 제공합니다. .NET 8 기능 및 크로스 플랫폼 배포를 다룹니다.

## 사용 시기
- 크로스 플랫폼 .NET 애플리케이션 구축
- .NET MAUI로 개발(모바일/데스크탑)
- 크로스 플랫폼 콘솔 도구 만들기
- Linux 컨테이너에 .NET 배포
- 클라우드 네이티브 .NET 서비스 구축
- 크로스 플랫폼 파일 및 프로세스 처리
- .NET 네이티브 AOT 컴파일 사용

## 빠른 시작
**다음과 같은 경우에 이 스킬을 호출하세요:**
- 크로스 플랫폼 .NET 애플리케이션 구축
- .NET MAUI로 개발
- 크로스 플랫폼 콘솔 도구 만들기
- Linux 컨테이너에 .NET 배포
- .NET 네이티브 AOT 컴파일 사용

**다음과 같은 경우에는 호출하지 마세요.**
- Windows 전용 WPF/WinForms(windows-app-developer 사용)
- 레거시 .NET Framework(dotnet-framework-4.8-expert 사용)
- 특히 웹 API(csharp-developer 사용)
- Azure 인프라(azure-infra-engineer 사용)

## 의사결정 프레임워크
```
Cross-Platform UI:
├── Mobile + Desktop → .NET MAUI
├── Desktop only → Avalonia or MAUI
├── Web → Blazor
└── Console → Cross-platform console app

Deployment Target:
├── Linux containers → Self-contained, Alpine
├── Windows service → Worker service
├── macOS app → .NET MAUI or Avalonia
├── Single file → Publish single-file
└── Fast startup → Native AOT
```

## 핵심 워크플로

### 1. .NET MAUI 앱 설정
1. 템플릿에서 MAUI 프로젝트 생성
2. 대상 플랫폼 구성
3. MVVM 아키텍처 설정
4. 플랫폼별 코드 구현
5. 기본 기능에 대한 핸들러 추가
6. 앱 수명주기 구성
7. 각 플랫폼에서 테스트

### 2. 크로스 플랫폼 배포
1. RuntimeIdentifiers 구성
2. 독립형 또는 프레임워크 종속형을 선택하세요.
3. 필요한 경우 트리밍을 설정합니다.
4. 플랫폼별 경로 처리
5. 플랫폼별 패키지
6. 대상 OS에서 테스트

### 3. 네이티브 AOT 컴파일
1. 프로젝트에서 PublishAot 활성화
2. AOT 호환성 검토
3. 반사 제한 처리
4. 잘린 애플리케이션 테스트
5. 시작 성능 확인
6. 최적화된 바이너리 배포

## 모범 사례
- 크로스 플랫폼 경로에는 Path.Combine을 사용하세요.
- RuntimeInformation.IsOSPlatform을 확인하세요.
- 조건부 컴파일을 자제해서 사용하세요.
- 모든 대상 플랫폼에서 테스트
- 크로스 플랫폼 추상화 사용
- 줄 끝을 적절하게 처리합니다.

## 안티 패턴
| 안티 패턴 | 문제 | 올바른 접근 |
|---------------|---------|------|
| Windows 경로 | Linux/Mac에서의 중단 | Path.Combine 사용 |
| 모든 곳에서 P/호출 | 플랫폼별 | 크로스 플랫폼 API 사용 |
| 대소문자 구분 무시 | Linux에서 실패 | 일관된 케이싱 |
| 대상에 대해 테스트되지 않음 | 런타임 실패 | 플랫폼별 CI |
| AOT에 대한 무거운 반성 | 트리밍으로 인해 앱이 중단됨 | 소스 생성기 사용 |