---
name: powershell-security-hardening
description: Windows 보안 강화 및 PowerShell 보안 구성 전문가입니다. 자동화 보안, 최소 권한 적용, 엔터프라이즈 보안 기준 조정을 전문으로 합니다. PowerShell 환경 및 Windows 시스템을 보호하는 데 사용됩니다. 트리거에는 "PowerShell 보안", "제한된 언어 모드", "JEA", "실행 정책", "보안 기준", "PowerShell 로깅"이 포함됩니다.
---
# PowerShell 보안 강화

## 목적
Windows 보안 강화 및 PowerShell 보안 구성에 대한 전문 지식을 제공합니다. 자동화 스크립트 보안, JEA(Just Enough Administration) 구현, 최소 권한 적용 및 엔터프라이즈 보안 기준 조정을 전문으로 합니다.

## 사용 시기
- PowerShell 보안 정책 구성
- 제한된 언어 모드 구현
- JEA(Just Enough Administration) 설정
- PowerShell 로깅 및 감사 활성화
- 자동화 자격 증명 확보
- CIS/STIG 기준선 적용
- PowerShell 공격으로부터 보호
- 실행 정책 구현

## 빠른 시작
**다음과 같은 경우에 이 스킬을 호출하세요:**
- PowerShell 환경 강화
- JEA 또는 제한된 언어 모드 구현
- PowerShell 로깅 구성
- 자동화 자격 증명 확보
- 보안 기준 적용

**다음과 같은 경우에는 호출하지 마세요.**
- 일반 Windows 관리 → 사용`/windows-infra-admin`- PowerShell 개발 → 사용`/powershell-7-expert`- Active Directory 보안 → 사용`/ad-security-reviewer`- 네트워크 보안 → 사용`/network-engineer`## 의사결정 프레임워크
```
Security Requirement?
├── Script Execution Control
│   ├── Basic → Execution Policy
│   └── Strict → AppLocker/WDAC
├── Language Restriction
│   └── Constrained Language Mode
├── Privilege Reduction
│   └── JEA (Just Enough Administration)
└── Auditing
    └── Script Block Logging + Transcription
```
## 핵심 워크플로

### 1. PowerShell 로깅 설정
1. GPO를 통해 스크립트 블록 로깅 활성화
2. 주요 모듈에 대한 모듈 로깅 활성화
3. 안전한 위치로 전사 구성
4. 보호된 이벤트 로그 전달 설정
5. 의심스러운 패턴에 대한 알림 생성
6. 샘플 스크립트를 사용하여 로깅 테스트

### 2. JEA 구성
1. 역할 기능 파일 정의
2. 허용되는 cmdlet 및 매개변수 지정
3. 세션 구성 생성
4. JEA 엔드포인트 등록
5. 제한된 사용자 계정으로 테스트
6. 문서 역할 할당

### 3. 제한된 언어 모드
1. 지원 요건 평가
2. AppLocker/WDAC 정책 만들기
3. 신뢰할 수 없는 스크립트에 대해 CLM 활성화
4. 필수 스크립트를 화이트리스트에 추가하세요
5. 애플리케이션 기능 테스트
6. 우회 시도 모니터링

## 모범 사례
- 모든 시스템에서 스크립트 블록 로깅 활성화
- 전체 관리자 권한 대신 JEA 사용
- 보안 저장소에 자격 증명 저장(스크립트 아님)
- 악성 코드 탐지를 위해 AMSI 적용
- AllSigned 정책과 함께 서명된 스크립트 사용
- PowerShell 사용 로그를 정기적으로 감사합니다.

## 안티 패턴
| 안티 패턴 | 문제 | 올바른 접근 |
|---------------|---------|------|
| 스크립트의 자격 증명 | 노출 위험 | SecretManagement 볼트 |
| 비활성화된 로깅 | 가시성 없음 | 모든 로깅 활성화 |
| 실행 정책 우회 | 보안 극장 | 앱락커/WDAC |
| 자동화를 위한 전체 관리자 | 과도한 특권 | 최소한의 권리를 가진 JEA |
| AMSI 무시 | 악성코드 사각지대 | AMSI 활성화 유지 |