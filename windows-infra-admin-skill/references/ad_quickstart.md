# Windows 인프라 관리자 - 빠른 시작 가이드

이 가이드는 Windows 인프라 관리 기술의 스크립트 및 도구를 시작하는 데 도움이 됩니다.

## 전제 조건

- 윈도우 서버 2016 이상
- RSAT(원격 서버 관리 도구) 설치
- 대부분의 작업에 대한 도메인 관리자 권한
- 파워셸 5.1 이상
- AD 작업을 위한 Active Directory 모듈

## 필수 모듈 설치
```powershell
# Install RSAT features (if not already installed)
Install-WindowsFeature RSAT-AD-PowerShell
Install-WindowsFeature RSAT-DNS-Server
Install-WindowsFeature RSAT-Group-Policy-Management

# Import modules
Import-Module ActiveDirectory
Import-Module DnsServer
Import-Module GroupPolicy
```
## 인증

스크립트에는 적절한 권한이 필요합니다.

- **Active Directory 작업**: 도메인 관리자 또는 위임된 권한
- **DNS 관리**: DNS 관리자 또는 도메인 관리자
- **그룹 정책**: 그룹 정책 작성자 소유자 또는 도메인 관리자

## 빠른 예

### Active Directory 사용자 관리
```powershell
# Create a new user
.\manage_ad_users.ps1 -Action Create `
  -Username "jdoe" `
  -FirstName "John" `
  -LastName "Doe" `
  -Email "jdoe@example.com" `
  -OU "OU=Users,DC=example,DC=com" `
  -Enabled $true

# List all users
.\manage_ad_users.ps1 -Action List

# Disable a user account
.\manage_ad_users.ps1 -Action Disable -Username "jdoe"

# Enable a user account
.\manage_ad_users.ps1 -Action Enable -Username "jdoe"

# Update user information
.\manage_ad_users.ps1 -Action Update `
  -Username "jdoe" `
  -Email "john.doe@newdomain.com" `
  -FirstName "Jonathan"
```
### DNS 구성
```powershell
# Create a new DNS zone
.\configure_dns.ps1 -Action CreateZone -ZoneName "example.com"

# Create an A record
.\configure_dns.ps1 -Action CreateRecord `
  -ZoneName "example.com" `
  -RecordName "www" `
  -RecordType "A" `
  -RecordData "192.168.1.10"

# Create an MX record
.\configure_dns.ps1 -Action CreateRecord `
  -ZoneName "example.com" `
  -RecordName "@" `
  -RecordType "MX" `
  -RecordData "mail.example.com" `
  -Priority 10

# Query DNS
.\configure_dns.ps1 -Action QueryDNS -ZoneName "www.example.com" -RecordType "A"

# Test DNS health
.\configure_dns.ps1 -Action TestDNS -ZoneName "example.com"
```
### 그룹 정책 관리
```powershell
# Create a new GPO
.\setup_gpo.ps1 -Action CreateGPO `
  -GPOName "Workstation Security" `
  -Description "Security policies for workstations"

# Link GPO to OU
.\setup_gpo.ps1 -Action LinkGPO `
  -GPOName "Workstation Security" `
  -TargetOU "OU=Workstations,DC=example,DC=com"

# List all GPOs
.\setup_gpo.ps1 -Action ListGPOs

# Backup a GPO
.\setup_gpo.ps1 -Action BackupGPO `
  -GPOName "Workstation Security" `
  -BackupPath ".\GPOBackups"

# Generate GPO report
.\setup_gpo.ps1 -Action ReportGPO -GPOName "Workstation Security"
```
## 일반적인 패턴

### 일괄 사용자 생성
```powershell
$users = @(
    @{Username="user1"; FirstName="User"; LastName="One"; Email="user1@example.com"},
    @{Username="user2"; FirstName="User"; LastName="Two"; Email="user2@example.com"}
)

foreach ($user in $users) {
    .\manage_ad_users.ps1 -Action Create `
        -Username $user.Username `
        -FirstName $user.FirstName `
        -LastName $user.LastName `
        -Email $user.Email
}
```
### 대량 DNS 레코드 생성
```powershell
$records = @(
    @{Name="www"; Type="A"; Data="192.168.1.10"},
    @{Name="mail"; Type="A"; Data="192.168.1.20"},
    @{Name="ftp"; Type="A"; Data="192.168.1.30"}
)

foreach ($record in $records) {
    .\configure_dns.ps1 -Action CreateRecord `
        -ZoneName "example.com" `
        -RecordName $record.Name `
        -RecordType $record.Type `
        -RecordData $record.Data
}
```
### GPO 보안 설정
```powershell
$settings = @{
    PasswordPolicy = @{
        MinLength = 12
        History = 12
        MaxAgeDays = 60
    }
    AuditPolicy = @{
        "Logon" = @{Success = $true; Failure = $true}
        "Privilege Use" = @{Success = $true; Failure = $true}
        "Process Tracking" = @{Success = $false; Failure = $false}
    }
}

.\setup_gpo.ps1 -Action ApplySettings `
  -GPOName "Security Baseline" `
  -GPOSettings $settings
```
## 모범 사례

1. **랩 환경에서 먼저 테스트** - 항상 비프로덕션 환경에서 스크립트를 테스트하세요.
2. **설명적인 OU 구조 사용** - 기능, 위치 또는 부서별로 OU를 구성합니다.
3. **GPO 변경 사항 문서화** - GPO 수정 사항 및 목적을 기록해 둡니다.
4. **변경 전 백업** - 수정하기 전에 항상 GPO를 백업하세요.
5. **최소 권한 사용** - 스크립트에 필요한 권한만 부여합니다.
6. **로깅 활성화** - LogPath 매개변수를 사용하여 작업을 추적합니다.
7. **입력 유효성 검사** - 모든 스크립트에는 내장된 유효성 검사가 포함됩니다.
8. **DNS 변경 계획** - DNS 레코드 변경 사항을 문서화하고 DNS 인벤토리를 유지합니다.

## 문제 해결

### AD 모듈을 찾을 수 없습니다
```
Error: Active Directory module not available
```
**해결책**:
```powershell
Install-WindowsFeature RSAT-AD-PowerShell -IncludeManagementTools
Import-Module ActiveDirectory
```
### 권한 거부 오류
```
Error: Access denied
```
**해결책**:
1. 관리자 권한으로 PowerShell을 실행하세요.
2. 도메인 관리자 권한이 있는지 확인하세요.
3. 계정에 필요한 위임 권한이 있는지 확인하세요.

### GPO 링크 실패
```
Error: Failed to link GPO
```
**해결책**:
1. OU 경로가 올바른지 확인하세요.
2. GPO가 존재하는지 확인하세요.
3. 대상 OU에 대한 권한이 있는지 확인하십시오.

### DNS 레코드가 확인되지 않음
```
Error: DNS query failed
```
**해결책**:
1. DNS 서버 서비스가 실행 중인지 확인하세요.
2. 기록이 존재하는지 확인하세요.
3. DNS 서버 복제 확인
4. 테스트`nslookup`명령

### 사용자 생성 실패
```
Error: Failed to create user
```
**해결책**:
1. 사용자 이름이 이미 존재하는지 확인하십시오.
2. OU 경로가 유효한지 확인하세요.
3. 비밀번호 정책이 임시 비밀번호를 허용하는지 확인하세요.
4. 계정에 OU의 사용자 생성 권한이 있는지 확인하세요.

## 유용한 PowerShell 명령
```powershell
# Find a user
Get-ADUser -Filter {Name -like "*John*"}

# Check user groups
Get-ADUser -Identity "jdoe" -Properties MemberOf | Select-Object -ExpandProperty MemberOf

# Get GPO links
Get-GPLink -Target "OU=Users,DC=example,DC=com"

# Test DNS resolution
Resolve-DnsName -Name "www.example.com"

# Check DNS server status
Get-Service -Name DNS

# Get DNS zones
Get-DnsServerZone

# View GPO inheritance
gpresult /r
```
## 보안 고려 사항

1. **보안 자격 증명** - 스크립트에 비밀번호를 하드코딩하지 마세요.
2. **관리형 서비스 계정 사용** - 자동화된 작업용
3. **권한 있는 작업 감사** - 관리자 작업에 대한 로깅 활성화
4. **계층형 관리 구현** - 관리자 계정과 일반 사용자 계정을 분리합니다.
5. **정기적인 비밀번호 순환** - 자동 비밀번호 순환 기능이 있는 관리형 서비스 계정을 사용하세요.
6. **AD 변경 모니터링** - 중요한 AD 수정에 대한 알림 설정

## 추가 리소스

- [Active Directory 설명서](https://docs.microsoft.com/active-directory)
- [DNS 서버 설명서](https://docs.microsoft.com/windows-server/networking/dns)
- [그룹 정책 문서](https://docs.microsoft.com/windows-server/group-policy)
- [PowerShell 설명서](https://docs.microsoft.com/powershell)
- [서버 관리 도구](https://docs.microsoft.com/windows-server/administration/server-manager)