# PowerShell 5.1 레거시 패턴

## 개요

이 가이드에서는 PowerShell 5.1 및 Windows 전용 환경과 관련된 패턴과 기술을 다룹니다.

## Windows 관련 패턴

### Windows Forms 통합

```powershell
Add-Type -AssemblyName System.Windows.Forms

$form = New-Object System.Windows.Forms.Form
$form.Text = "PowerShell 5.1 Form"
$form.Width = 400
$form.Height = 300

$button = New-Object System.Windows.Forms.Button
$button.Text = "Click Me"
$button.Location = New-Object System.Drawing.Point(100, 100)
$button.Add_Click({
    [System.Windows.Forms.MessageBox]::Show("Hello from PS 5.1!")
})

$form.Controls.Add($button)
$form.ShowDialog()
```

### WMI 쿼리(레거시)

```powershell
# Query using Get-WmiObject
$os = Get-WmiObject -Class Win32_OperatingSystem
Write-Host "OS: $($os.Caption)"
Write-Host "Version: $($os.Version)"
Write-Host "Service Pack: $($os.ServicePackMajorVersion)"

# Query with WQL filter
$services = Get-WmiObject -Class Win32_Service -Filter "State='Running'"
```

### Active Directory 자동화

```powershell
# Create user with properties
New-ADUser -SamAccountName "jdoe" `
            -UserPrincipalName "jdoe@corp.local" `
            -Name "John Doe" `
            -DisplayName "John Doe" `
            -Path "OU=Users,DC=corp,DC=local" `
            -Enabled $true `
            -ChangePasswordAtLogon $true `
            -AccountPassword (ConvertTo-SecureString "TempPass123!" -AsPlainText -Force)

# Query with filter
Get-ADUser -Filter * -Properties * | Where-Object { $_.Enabled -eq $false }

# Batch operations
$users = Import-Csv -Path "users.csv"
foreach ($user in $users) {
    New-ADUser @user
}
```

## 레거시 프로토콜 관리

### WinRM을 사용한 원격

```powershell
# Enable WinRM
Enable-PSRemoting -Force

# Test remoting connection
Test-WSMan -ComputerName "server01"

# Invoke command remotely
Invoke-Command -ComputerName "server01" -ScriptBlock {
    Get-Service | Where-Object { $_.Status -eq 'Running' }
}

# Enter remote session
Enter-PSSession -ComputerName "server01"
```

### 레거시 COM 개체

```powershell
# Create COM object
$excel = New-Object -ComObject Excel.Application
$excel.Visible = $true

$workbook = $excel.Workbooks.Add()
$worksheet = $workbook.Worksheets.Item(1)
$worksheet.Cells.Item(1,1).Value = "Hello"

# Clean up
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($worksheet) | Out-Null
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($workbook) | Out-Null
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null
```

## 레지스트리 작업

### 레지스트리 조작

```powershell
# Create registry key
New-Item -Path "HKLM:\Software\MyApp" -Force

# Set registry value
Set-ItemProperty -Path "HKLM:\Software\MyApp" -Name "Version" -Value "1.0.0"

# Read registry value
Get-ItemProperty -Path "HKLM:\Software\MyApp" -Name "Version"

# Remove registry value
Remove-ItemProperty -Path "HKLM:\Software\MyApp" -Name "Version"

# Check if key exists
if (Test-Path "HKLM:\Software\MyApp") {
    Write-Host "Registry key exists"
}
```

### 레지스트리 권한

```powershell
# Get ACL
$acl = Get-Acl "HKLM:\Software\MyApp"

# Add access rule
$rule = New-Object System.Security.AccessControl.RegistryAccessRule(
    "DOMAIN\User",
    "FullControl",
    "Allow"
)

$acl.SetAccessRule($rule)
Set-Acl "HKLM:\Software\MyApp" $acl
```

## Windows 서비스 관리

### 서비스 제어

```powershell
# Get service status
Get-Service -Name "wuauserv"

# Start service
Start-Service -Name "wuauserv"

# Stop service
Stop-Service -Name "wuauserv" -Force

# Restart service
Restart-Service -Name "wuauserv"

# Set service startup type
Set-Service -Name "wuauserv" -StartupType Automatic
```

### 서비스 종속성

```powershell
# Get service dependencies
Get-Service -Name "spooler" -RequiredServices

# Get dependent services
Get-Service -Name "Spooler" -DependentServices
```

## 이벤트 로그 통합

### 이벤트 로그 읽기

```powershell
# Get recent events
Get-EventLog -LogName System -Newest 10

# Filter by event ID
Get-EventLog -LogName Security -InstanceId 4624 -Newest 100

# Get specific time range
$startTime = (Get-Date).AddHours(-24)
Get-WinEvent -FilterHashtable @{
    LogName = 'Security'
    ID = 4624
    StartTime = $startTime
}
```

### 이벤트 로그에 쓰기

```powershell
# Create custom event source
New-EventLog -LogName "Application" -Source "MyScript"

# Write event
Write-EventLog -LogName "Application" `
               -Source "MyScript" `
               -EntryType Information `
               -EventId 1000 `
               -Message "Script completed successfully"
```

## Windows Server 2012/2016/2019 특정

### 서버 관리자 통합

```powershell
# Import Server Manager module
Import-Module ServerManager

# Get Windows features
Get-WindowsFeature

# Install feature
Install-WindowsFeature -Name Web-Server -IncludeManagementTools

# Remove feature
Remove-WindowsFeature -Name Web-Server
```

### IIS 관리

```powershell
# Import IIS module
Import-Module WebAdministration

# Get websites
Get-Website

# Create website
New-Website -Name "MySite" `
             -PhysicalPath "C:\inetpub\wwwroot\mysite" `
             -Port 80

# Get application pools
Get-WebApplicationPool

# Start website
Start-Website -Name "MySite"
```

## 성능 카운터

### 성능 모니터링

```powershell
# Get available counters
Get-Counter -ListSet "Processor"

# Get counter data
Get-Counter -Counter "\Processor(_Total)\% Processor Time"

# Continuous monitoring
while ($true) {
    $cpu = Get-Counter -Counter "\Processor(_Total)\% Processor Time"
    Write-Host "CPU: $($cpu.CounterSamples.CookedValue)%"
    Start-Sleep -Seconds 1
}
```

## 모범 사례

1. 사용하기 전에 항상 Windows 관련 기능을 확인하십시오.
2. WMI/COM 작업에는 `try/catch`을 사용하세요.
3. COM 개체를 올바르게 해제합니다.
4. 안전한 환경에서 레지스트리 작업 테스트
5. 문제 해결을 위해 자세한 로깅을 사용하십시오.
6. 실행 전 사용자 입력 유효성 검사
7. 권한을 적절하게 처리하세요.

## 마이그레이션 참고 사항

PowerShell 7로 마이그레이션하는 경우:

- `Get-WmiObject`을(를) `Get-CimInstance`(으)로 바꿉니다.
- 크로스 플랫폼 대안으로 Windows 관련 API 업데이트
- 해당되는 경우 PowerShell 7 특정 기능을 사용합니다.
- PS 7 환경에서 모든 스크립트 테스트
- PS 7 호환성을 위한 업데이트 모듈 가져오기

## 자원

- [PowerShell 5.1 문서](https://docs.microsoft.com/en-us/powershell/scripting/whats-new/what-s-new-in-windows-powershell-50)
- [WMI 클래스](https://docs.microsoft.com/en-us/windows/win32/wmisdk/wmi-classes)
- [Active Directory 모듈](https://docs.microsoft.com/en-us/powershell/module/activedirectory/)