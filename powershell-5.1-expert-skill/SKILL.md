---
name: powershell-5.1-expert
description: 레거시 Windows PowerShell 5.1 전문가입니다. WMI, ADSI, COM 자동화 및 Windows Server 환경과의 이전 버전과의 호환성 유지를 전문으로 합니다. 레거시 시스템에서 Windows 관련 자동화에 사용합니다. 트리거에는 "PowerShell 5.1", "Windows PowerShell", "WMI", "ADSI", "COM 개체", "레거시 PowerShell"이 포함됩니다.
---
# 파워셸 5.1 전문가

## 목적
레거시 Windows 환경을 위한 Windows PowerShell 5.1에 대한 전문 지식을 제공합니다. WMI 쿼리, ADSI 작업, COM 자동화 및 이전 Windows Server 시스템과 호환되는 스크립트 유지 관리를 전문으로 합니다.

## 사용 시기
- Windows Server 2012/2016/2019용 스크립팅
- 시스템 관리를 위해 WMI를 사용합니다.
- ADSI를 통한 Active Directory 작업
- COM 자동화(Office, 레거시 앱)
- 이전 버전과의 호환성 유지
- DSC(원하는 상태 구성)
- Windows 전용 자동화
- 레거시 스크립트 유지 관리

## 빠른 시작
**다음과 같은 경우에 이 스킬을 호출하세요:**
- 특히 Windows PowerShell 5.1을 사용하여 작업
- 시스템 쿼리에 WMI 사용
- ADSI 또는 COM 개체를 사용한 자동화
- 레거시 PowerShell 스크립트 유지 관리
- DSC 구성 관리

**다음과 같은 경우에는 호출하지 마세요.**
- 크로스 플랫폼 PowerShell → 사용`/powershell-7-expert`- GUI/TUI 개발 → 활용`/powershell-ui-architect`- 보안강화 → 활용`/powershell-security-hardening`- 모듈 아키텍처 → 사용`/powershell-module-architect`## 의사결정 프레임워크
```
PowerShell Version Context?
├── Must run on older Windows
│   └── Use 5.1 with WMI/ADSI
├── Cross-platform needed
│   └── Use PowerShell 7+ instead
├── AD Management
│   ├── Simple → ADSI
│   └── Complex → AD Module
└── System Info
    ├── Legacy → WMI
    └── Modern → CIM (also works in 5.1)
```
## 핵심 워크플로

### 1. WMI 시스템 쿼리
1. WMI 클래스 식별(Win32_*)
2. WMI 쿼리 구성
3. Get-WmiObject 또는 Get-CimInstance를 사용하세요.
4. 결과를 적절하게 필터링하세요.
5. 포맷 출력
6. 원격 시스템의 오류 처리

### 2. ADSI 작업
1. DirectoryEntry 객체 생성
2. LDAP 경로 탐색
3. 속성 쿼리 또는 수정
4. 수정하는 경우 변경 사항을 커밋합니다.
5. 인증 처리
6. 리소스 정리

### 3. COM 자동화
1. New-Object -ComObject를 사용하여 COM 개체 생성
2. 객체 모델에 액세스
3. 작업 수행
4. COM 오류 처리
5. COM 개체를 적절하게 해제하세요.
6. [System.Runtime.InteropServices.Marshal]을 사용하여 정리합니다.

## 모범 사례
- 가능하면 WMI를 통해 CIM cmdlet을 사용합니다(더 나은 원격 기능).
- 원격 작업에 대한 오류 처리를 항상 포함합니다.
- 메모리 누수를 방지하기 위해 COM 개체를 명시적으로 해제합니다.
- 대상 Windows 버전에서 테스트
- 필요한 PowerShell 모듈 문서화
- 기능에 승인된 동사를 사용하세요.

## 안티 패턴
| 안티 패턴 | 문제 | 올바른 접근 |
|---------------|---------|------|
| COM을 출시하지 않음 | 메모리 누수 | 명시적 정리 |
| 느린 네트워크를 통한 WMI | 성능 문제 | 세션에 CIM 사용 |
| 오류 처리 없음 | 조용한 실패 | 로깅을 통한 시도/캐치 |
| 하드코딩된 경로 | 이식성 문제 | 환경 변수 사용 |
| 출력용 쓰기 호스트 | 캡처할 수 없습니다 | 쓰기 출력 또는 반환 |