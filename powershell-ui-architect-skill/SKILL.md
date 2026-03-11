---
name: powershell-ui-architect
description: WinForms, WPF 및 콘솔/TUI 프레임워크를 사용하여 PowerShell로 GUI 및 TUI를 구축하는 전문가입니다. 그래픽 또는 터미널 인터페이스로 PowerShell 도구를 만들 때 사용합니다. 트리거에는 "PowerShell GUI", "WinForms", "WPF PowerShell", "PowerShell TUI", "터미널 UI", "PowerShell 인터페이스"가 포함됩니다.
---
# PowerShell UI 설계자

## 목적
PowerShell을 사용하여 그래픽 사용자 인터페이스(GUI) 및 터미널 사용자 인터페이스(TUI) 구축에 대한 전문 지식을 제공합니다. 사용자 친화적인 PowerShell 도구를 만들기 위한 WinForms, WPF 및 콘솔 기반 TUI 프레임워크를 전문으로 합니다.

## 사용 시기
- GUI를 사용하여 PowerShell 도구 구축
- WinForms 애플리케이션 만들기
- 스크립트용 WPF 인터페이스 개발
- 터미널 사용자 인터페이스(TUI) 구축
- 자동화 스크립트에 대화 상자 추가
- 대화형 관리 도구 만들기
- 구성 마법사 구축
- 진행상황 표시 구현

## 빠른 시작
**다음과 같은 경우에 이 스킬을 호출하세요:**
- PowerShell 스크립트용 GUI 생성
- WinForms 또는 WPF 인터페이스 구축
- 터미널 기반 UI 개발
- 도구에 대화형 대화 상자 추가
- 관리 도구 인터페이스 생성

**다음과 같은 경우에는 호출하지 마세요**
- 크로스 플랫폼 CLI 도구 → 사용`/cli-developer`- PowerShell 모듈 설계 → 사용`/powershell-module-architect`- 웹 인터페이스 → 사용`/frontend-design`- Windows 앱 개발(PS ​​이외) → 사용`/windows-app-developer`

## 의사결정 프레임워크```
UI Type Needed?
├── Simple Dialog
│   └── WinForms MessageBox / InputBox
├── Full Windows App
│   ├── Simple layout → WinForms
│   └── Rich UI → WPF with XAML
├── Console/Terminal
│   ├── Simple menu → Write-Host + Read-Host
│   └── Rich TUI → Terminal.Gui / PSReadLine
└── Cross-Platform
    └── Terminal-based only
```

## 핵심 워크플로우

### 1. WinForms 애플리케이션
1. System.Windows.Forms 어셈블리 추가
2. 양식 객체 생성
3. 컨트롤 추가(버튼, 텍스트 상자)
4. 이벤트 핸들러 연결
5. 레이아웃 구성
6. ShowDialog()를 사용하여 양식 표시

### 2. WPF 인터페이스
1. XAML 레이아웃 정의
2. PowerShell에서 XAML 로드
3. 제어 참조 얻기
4. 이벤트 핸들러 추가
5. 로직 구현
6. 디스플레이 창

### 3. Terminal.Gui를 사용한 TUI
1. Terminal.Gui 모듈 설치
2. 애플리케이션 초기화
3. 창 및 뷰 생성
4. 컨트롤 추가(버튼, 목록, 텍스트)
5. 이벤트 처리
6. 메인 루프 실행

## 모범 사례
- UI 코드를 로직과 별도로 유지
- 복잡한 WPF 레이아웃에 XAML 사용
- 사용자 피드백을 통해 오류를 적절하게 처리
- 장시간 작업에 대한 진행률 표시 제공
- 대상 Windows 버전에서 테스트
- 대상에 적합한 UI 사용(GUI vs TUI)

## 안티 패턴
| 안티 패턴 | 문제 | 올바른 접근 |
|---------------|---------|------|
| 비즈니스 로직과 혼합된 UI 로직 | 유지 관리가 어려움 | 별도의 우려 사항 |
| UI 스레드 차단 | 고정된 인터페이스 | 런타임/작업 사용 |
| 입력 유효성 검사 없음 | 충돌, 잘못된 데이터 | 사용 전 확인 |
| 하드코딩된 크기 | 확장 문제 | 앵커링/도킹 사용 |
| 오류 메시지 없음 | 혼란스러운 사용자 | 친숙한 오류 대화 상자 |