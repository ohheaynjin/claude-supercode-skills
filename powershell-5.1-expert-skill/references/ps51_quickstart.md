# PowerShell 5.1 전문가 - 빠른 시작 가이드

## 개요

이 기술은 Windows 시스템에 설치된 레거시 PowerShell 버전인 Windows PowerShell 5.1에 대한 전문 지식을 제공합니다. Windows Server 2012/2016/2019 환경 관리에 적합합니다.

## 전제 조건

- PowerShell 5.1이 설치된 Windows 운영 체제
- 시스템 수준 작업을 위한 관리 권한
- AD 작업을 위한 Active Directory 모듈(RSAT 도구)

## 시작하기

### 1. 필수 모듈 설치
```powershell
# Check PowerShell version
$PSVersionTable.PSVersion

# Install RSAT tools (if needed)
Install-WindowsFeature -Name RSAT-AD-PowerShell

# Import modules
Import-Module ActiveDirectory
Import-Module PSDesiredStateConfiguration
```
### 2. 기본 AD 사용자 관리
```powershell
# Create a user
.\scripts\manage_legacy_ad.ps1 -Username "jdoe" -Action Create -OU "OU=Users,DC=corp,DC=local"

# Enable a user
.\scripts\manage_legacy_ad.ps1 -Username "jdoe" -Action Enable

# Disable a user
.\scripts\manage_legacy_ad.ps1 -Username "jdoe" -Action Disable
```
### 3. WMI/CIM 쿼리
```powershell
# Query system information
.\scripts\query_wmi.ps1 -QueryClass "Win32_OperatingSystem" -UseCIM

# Query with filter
.\scripts\query_wmi.ps1 -QueryClass "Win32_Processor" -PropertyFilter "Name"

# Query remote computer
.\scripts\query_wmi.ps1 -QueryClass "Win32_Service" -ComputerName "server01"
```
### 4. DSC 구성 배포
```powershell
# Compile and apply DSC
.\scripts\deploy_dsc.ps1 -ConfigurationName "WebServerConfig" -TargetNodes "web01","web02" -Mode Apply

# Test DSC compliance
.\scripts\deploy_dsc.ps1 -ConfigurationName "WebServerConfig" -TargetNodes "web01" -Mode Test
```
## 주요 개념

### 실행 정책

PowerShell 5.1은 실행 정책을 사용하여 스크립트 실행을 제어합니다.
```powershell
# View current policy
Get-ExecutionPolicy -List

# Set execution policy
Set-ExecutionPolicy -Scope LocalMachine -ExecutionPolicy RemoteSigned
```
### 모듈 관리
```powershell
# List available modules
Get-Module -ListAvailable

# Import a module
Import-Module ActiveDirectory

# Get module commands
Get-Command -Module ActiveDirectory
```
## 일반적인 패턴

### 오류 처리
```powershell
try {
    # Your code here
    Get-ADUser -Identity "jdoe"
}
catch {
    Write-Error "Failed to retrieve user: $_"
}
finally {
    # Cleanup code
}
```
### 매개변수 검증
```powershell
param(
    [Parameter(Mandatory=$true)]
    [ValidateNotNullOrEmpty()]
    [string]$Username,
    
    [Parameter(Mandatory=$false)]
    [ValidateSet('Enable', 'Disable', 'Delete')]
    [string]$Action
)
```
### 자세한 출력
```powershell
[CmdletBinding()]
param()

begin {
    Write-Verbose "Starting operation"
}

process {
    Write-Verbose "Processing item: $_"
}

end {
    Write-Verbose "Operation complete"
}
```
## 타입스크립트 통합
```typescript
import PowerShell51Manager from './scripts/legacy_wrapper';

const ps51 = new PowerShell51Manager('./scripts');

// Manage AD users
await ps51.manageLegacyAD({
  username: 'jdoe',
  action: 'Create',
  ou: 'OU=Users,DC=corp,DC=local',
  groups: ['Developers', 'PowerUsers']
});

// Query WMI
await ps51.queryWMI({
  queryClass: 'Win32_Processor',
  useCIM: true
});
```
## 문제 해결

### AD 모듈을 찾을 수 없습니다
```
Error: The term 'Get-ADUser' is not recognized
```
**해결책:** RSAT 도구를 설치합니다.
```powershell
Install-WindowsFeature -Name RSAT-AD-PowerShell
```
### WMI 액세스가 거부되었습니다.
```
Error: Access denied
```
**해결책:** 관리자로 PowerShell을 실행하거나 적절한 자격 증명을 사용하십시오.

### DSC 컴파일 오류
```
Error: The term 'Configuration' is not recognized
```
**해결책:** DSC 모듈 가져오기:
```powershell
Import-Module PSDesiredStateConfiguration
```
## 모범 사례

1. 항상 사용하세요`#Requires -Version 5.1`스크립트 상단에
2. 오류 처리를 위한 try/catch/finally 블록 구현
3. 사용`Write-Verbose`디버깅 정보용
4. 검증 속성으로 입력 매개변수 검증
5. 사용`ShouldProcess`파괴적인 작업을 위해
6. 먼저 비프로덕션 환경에서 스크립트를 테스트하세요.

## 다음 단계

- 탐색`references/`고급 패턴 디렉토리
- 검토`legacy_patterns.md`PowerShell 5.1 특정 기술용
- 확인`migration_guide.md`PowerShell 7로 업그레이드하기 위해

## 지원

문제나 질문이 있는 경우 다음을 참조하세요.
- Microsoft PowerShell 5.1 설명서
- Windows 서버 문서
- Active Directory PowerShell 모듈 참조