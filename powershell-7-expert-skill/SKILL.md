---
name: powershell-7-expert
description: 최신 크로스 플랫폼 PowerShell Core 전문가입니다. Linux/macOS 자동화, 병렬 처리, REST API 통합 및 최신 스크립팅 패턴을 전문으로 합니다. 크로스 플랫폼 자동화 및 최신 PowerShell 기능에 사용합니다. 트리거에는 "PowerShell 7", "PowerShell Core", "pwsh", "ForEach-Object -Parallel", "크로스 플랫폼 PowerShell"이 포함됩니다.
---
# 파워셸 7 전문가

## 목적
플랫폼 간 자동화를 위한 최신 PowerShell 7+(PowerShell Core)에 대한 전문 지식을 제공합니다. 병렬 처리, REST API 통합, 최신 스크립팅 패턴 및 새로운 언어 기능 활용을 전문으로 합니다.

## 사용 시기
- 크로스 플랫폼 자동화(Windows, Linux, macOS)
- ForEach-Object -Parallel을 사용한 병렬 처리
- REST API 통합
- 최신 PowerShell 스크립팅 패턴
- 파이프라인 체인 연산자(&& ||)
- 삼항 표현식 및 Null 병합
- SSH 기반 원격
- JSON/YAML 데이터 조작

## 빠른 시작
**다음과 같은 경우에 이 스킬을 호출하세요:**
- 크로스 플랫폼 PowerShell 스크립트 작성
- PowerShell 7+ 특정 기능 사용
- 병렬 처리 구현
- REST API 통합 구축
- 5.1의 스크립트 현대화

**다음과 같은 경우에는 호출하지 마세요.**
- 레거시 Windows 전용 시스템 → 사용`/powershell-5.1-expert`- GUI 개발 → 활용`/powershell-ui-architect`- 보안설정 → 사용`/powershell-security-hardening`- 모듈 설계 → 사용`/powershell-module-architect`## 의사결정 프레임워크
```
PowerShell 7 Feature Selection?
├── Parallel Processing
│   ├── Simple iteration → ForEach-Object -Parallel
│   └── Complex workflows → Start-ThreadJob
├── API Integration
│   └── Invoke-RestMethod with modern options
├── Null Handling
│   ├── Default value → ?? operator
│   └── Conditional access → ?. operator
└── Pipeline Control
    └── && and || chain operators
```
## 핵심 워크플로

### 1. 병렬 처리
1. 병렬화 가능한 워크로드 식별
2. ForEach-Object -Parallel을 사용하세요.
3. -ThrottleLimit을 적절하게 설정하십시오.
4. 스레드로부터 안전한 데이터 액세스 처리
5. 집계 결과
6. 병렬 실행으로 인한 오류 처리

### 2. REST API 통합
1. 요청 매개변수 구성
2. 인증 처리(Bearer, OAuth)
3. Invoke-RestMethod 사용
4. JSON 응답 구문 분석
5. 페이지 매김 구현
6. 실패에 대한 재시도 논리 추가

### 3. 크로스 플랫폼 스크립트
1. Windows 관련 경로를 피하세요
2. $PSVersionTable 및 $IsLinux/$IsWindows를 사용하세요.
3. 경로 구분 기호를 올바르게 처리하십시오.
4. 모든 대상 플랫폼에서 테스트
5. 호환 가능한 모듈을 사용하세요
6. 문서 플랫폼 요구 사항

## 모범 사례
- 간결한 조건문을 위해 삼항 연산자를 사용하세요.
- 기본값에 대해 널 병합 활용
- CPU 바인딩 작업에는 ForEach-Object -Parallel을 사용하세요.
- 크로스 플랫폼의 경우 WinRM보다 SSH 원격을 선호합니다.
- 크로스 플랫폼 경로에 Join-Path 사용
- 모든 대상 운영 체제에서 테스트

## 안티 패턴
| 안티 패턴 | 문제 | 올바른 접근 |
|---------------|---------|------|
| 하드코딩된 백슬래시 | Linux/macOS에서 중단 | 조인 경로 또는 / |
| Windows 전용 cmdlet | 플랫폼 간 오류 | 이용 가능 여부 확인 |
| 과잉 병렬화 | 스레드 오버헤드 | ThrottleLimit 조정 |
| $Error 무시 | 조용한 실패 | 적절한 오류 처리 |
| WinRM 가정 | 크로스 플랫폼이 아님 | SSH 원격 |