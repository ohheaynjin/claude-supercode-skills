---
name: windows-app-developer
description: WinUI 3, WPF 및 Windows App SDK를 사용하여 최신 Windows 애플리케이션을 구축하는 전문가입니다. MSIX 패키징, XAML 스타일 지정 및 MVVM 아키텍처를 전문으로 합니다.
---
# 윈도우 앱 개발자

## 목적
WinUI 3, WPF 및 Windows App SDK를 사용하여 최신 Windows 데스크톱 애플리케이션을 구축하는 데 필요한 전문 지식을 제공합니다. XAML 기반 UI 개발, MVVM 아키텍처, 기본 Windows 통합 및 MSIX를 사용한 최신 패키징을 전문으로 합니다.

## 사용 시기
- WinUI 3 또는 WPF를 사용하여 Windows 데스크톱 애플리케이션 구축
- Windows 앱용 MVVM 아키텍처 구현
- XAML 레이아웃 및 사용자 지정 컨트롤 만들기
- MSIX를 사용하여 애플리케이션 패키징
- Windows 기능(알림, 작업 표시줄, 시스템 트레이)과 통합
- WPF 애플리케이션을 WinUI 3으로 마이그레이션
- Windows 관련 기능 구현(점프 목록, 라이브 타일)
- Microsoft Store 지원 애플리케이션 구축

## 빠른 시작
**다음과 같은 경우에 이 스킬을 호출하세요:**
- WinUI 3 또는 WPF를 사용하여 Windows 데스크톱 애플리케이션 구축
- Windows 앱용 MVVM 아키텍처 구현
- XAML 레이아웃 및 사용자 지정 컨트롤 만들기
- MSIX를 사용하여 애플리케이션 패키징
- Windows 기능(알림, 작업 표시줄)과 통합

**다음과 같은 경우에는 호출하지 마세요.**
- 크로스 플랫폼 앱 구축 → mobile-developer 또는 Electron-pro 사용
- 콘솔 애플리케이션 → 적절한 언어 능력 사용
- PowerShell GUI → powershell-ui-architect 사용
- 웹 애플리케이션 → 적절한 웹 스킬 사용

## 의사결정 프레임워크
```
Windows App Task?
├── New Modern App → WinUI 3 with Windows App SDK
├── Existing WPF App → Maintain or migrate to WinUI 3
├── Cross-Platform Priority → Consider .NET MAUI
├── Enterprise Internal → WPF with proven patterns
├── Store Distribution → MSIX packaging required
└── System Integration → P/Invoke or Windows SDK APIs
```

## 핵심 워크플로

### 1. WinUI 3 애플리케이션 설정
1. Windows App SDK 템플릿을 사용하여 프로젝트 생성
2. 기능에 대한 Package.appxmanifest 구성
3. MVVM 인프라 설정(CommunityToolkit.Mvvm)
4. 탐색 및 셸 구조 구현
5. 재사용 가능한 컨트롤 라이브러리 생성
6. MSIX 패키징 구성
7. 스토어 또는 사이드로드 배포를 위한 CI/CD 설정

### 2. MVVM 구현
1. 관찰 가능한 속성으로 ViewModel 정의
2. 사용자 작업에 대한 명령 구현
3. 데이터 및 비즈니스 로직을 위한 서비스 생성
4. 종속성 주입 컨테이너 설정
5. XAML의 ViewModel에 뷰 바인딩
6. 내비게이션 서비스 구현
7. XAML 미리 보기를 위한 디자인 타임 데이터 추가

### 3. MSIX 패키징
1. Package.appxmanifest 구성
2. 애플리케이션 ID 및 기능 정의
3. 시각적 자산(아이콘, 스플래시) 설정
4. 설치 동작 구성
5. 인증서로 패키지 서명
6. 테스트 설치 및 업데이트
7. Microsoft Store에 제출하거나 내부적으로 배포

## 모범 사례
- 새로운 개발에는 WinUI 3를 사용하고 레거시 유지 관리에는 WPF를 사용합니다.
- 테스트 가능성과 분리를 위해 MVVM을 엄격하게 구현합니다.
- 컴파일 타임 바인딩 유효성 검사를 위해 x:Bind 사용
- 공통 패턴에 대한 커뮤니티 툴킷 활용
- 최신 설치 환경을 위한 MSIX 포함 패키지
- 일관된 UX를 위해 Fluent 디자인 시스템을 따릅니다.

## 안티 패턴
- **코드 숨김 로직** → ViewModels로 이동
- **동기식 UI 작업** → I/O에 async/await 사용
- **View에서 직접 서비스 호출** → ViewModel을 통해 이동
- **DPI 인식 무시** → 여러 척도에서 테스트
- **기능 누락** → 매니페스트에 필수 기능 선언