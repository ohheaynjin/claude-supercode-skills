# PowerShell 보안 기준

## 개요

이 가이드에서는 실행 정책, 제한된 언어 모드 및 로깅을 포함하여 PowerShell 환경에 대한 보안 기준을 설정합니다.

## 보안 체크리스트

### 실행 정책

- [ ] 적절한 실행 정책 설정(RemoteSigned 권장)
- [ ] 모든 범위에 걸쳐 실행 정책 시행
- [ ] 실행 정책 준수 여부를 정기적으로 감사합니다.
- [ ] 전사적 시행을 위해 그룹 정책을 사용합니다.

### 제한된 언어 모드

- [ ] 프로덕션을 위해 제한된 언어 모드를 활성화합니다.
- [ ] 먼저 비프로덕션 환경에서 테스트
- [ ] 문서 제한 작업
- [ ] 우회 시도 모니터링

### 스크립트 블록 로깅

- [ ] 스크립트 블록 로깅 활성화
- [ ] 호출 헤더 로깅 활성화
- [ ] 로그 보존 정책 구성
- [ ] 스크립트 블록 로그를 정기적으로 검토합니다.

### 모듈 로깅

- [ ] 모듈 로깅 활성화
- [ ] 기록할 모듈 지정
- [ ] 모니터 모듈 사용량
- [ ] 의심스러운 모듈 활동에 대한 경고

### 전사

- [ ] PowerShell 기록 활성화
- [ ] 적절한 전사 경로 설정
- [ ] 성적 증명서를 위한 보안 저장소 구성
- [ ] 성적표 보존 정책 구현

## 실행 정책 구성

### 권장 설정

```powershell
# Set RemoteSigned for LocalMachine scope
Set-ExecutionPolicy -Scope LocalMachine -ExecutionPolicy RemoteSigned

# Set Restricted for Process scope
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Restricted

# Verify settings
Get-ExecutionPolicy -List
```

### 그룹 정책 시행

```
Computer Configuration → Administrative Templates →
Windows Components → Windows PowerShell

Turn on Script Execution:
- Enabled
- Execution Policy: Allow only signed scripts

```

## 제한된 언어 모드

### 제한 모드 활성화

```powershell
# Set constrained language mode
$ExecutionContext.SessionState.LanguageMode = "ConstrainedLanguage"

# Verify
$ExecutionContext.SessionState.LanguageMode
```

### 시스템 전체 시행

```powershell
# Set system-wide constrained mode
$registryPath = "HKLM:\SOFTWARE\Microsoft\PowerShell\1\ShellIds"
Set-ItemProperty -Path $registryPath -Name "ConsoleSessionConfigurationName" -Value "ConstrainedLanguage"
```

### 제한 모드 테스트

```powershell
# Test restricted operations
try {
    Add-Type -TypeDefinition 'public class Test { }'
    Write-Host "✗ Type creation allowed (NOT SECURE)" -ForegroundColor Red
}
catch {
    Write-Host "✓ Type creation blocked (SECURE)" -ForegroundColor Green
}

try {
    New-Object System.Net.WebClient
    Write-Host "✗ Object creation allowed (NOT SECURE)" -ForegroundColor Red
}
catch {
    Write-Host "✓ Object creation blocked (SECURE)" -ForegroundColor Green
}
```

## 스크립트 블록 로깅

### 스크립트 블록 로깅 활성화

```powershell
# Enable script block logging
$registryPath = "HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging"

if (-not (Test-Path $registryPath)) {
    New-Item -Path $registryPath -Force
}

Set-ItemProperty -Path $registryPath -Name "EnableScriptBlockLogging" -Value 1 -Force
Set-ItemProperty -Path $registryPath -Name "EnableScriptBlockInvocationLogging" -Value 1 -Force
```

### 스크립트 블록 로그 분석

```powershell
# Query script block events
$events = Get-WinEvent -LogName "Microsoft-Windows-PowerShell/Operational" `
                      -FilterXPath "*[System[(EventID=4104)]]" `
                      -MaxEvents 100

# Analyze patterns
foreach ($event in $events) {
    $message = $event.Message
    
    if ($message -match "ScriptBlock ID: ([0-9a-f-]+)") {
        $scriptBlockId = $matches[1]
        Write-Host "Script Block ID: $scriptBlockId"
    }
}
```

### 의심스러운 활동 감지

```powershell
function Find-SuspiciousScripts {
    $suspiciousPatterns = @(
        'System.Reflection.Assembly',
        'System.Net.WebClient',
        'Invoke-Expression',
        'DownloadString',
        'IEX'
    )
    
    $events = Get-WinEvent -LogName "Microsoft-Windows-PowerShell/Operational" `
                          -FilterXPath "*[System[(EventID=4104)]]"
    
    foreach ($event in $events) {
        $message = $event.Message
        
        foreach ($pattern in $suspiciousPatterns) {
            if ($message -match $pattern) {
                Write-Host "Suspicious pattern detected: $pattern" -ForegroundColor Red
                Write-Host "Time: $($event.TimeCreated)"
                Write-Host "User: $($event.Properties[4].Value)"
                Write-Host "Message: $($message -split "`n")[0]"
                Write-Host ""
            }
        }
    }
}
```

## 모듈 로깅

### 모듈 로깅 활성화

```powershell
# Enable module logging
$registryPath = "HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\ModuleLogging"

if (-not (Test-Path $registryPath)) {
    New-Item -Path $registryPath -Force
}

Set-ItemProperty -Path $registryPath -Name "EnableModuleLogging" -Value 1 -Force

# Specify modules to log
$moduleNamesPath = Join-Path $registryPath "ModuleNames"
if (-not (Test-Path $moduleNamesPath)) {
    New-Item -Path $moduleNamesPath -Force
}

Set-ItemProperty -Path $moduleNamesPath -Name "*" -Value "*" -Force
```

### 모듈 사용량 모니터링

```powershell
function Get-ModuleUsage {
    $events = Get-WinEvent -LogName "Microsoft-Windows-PowerShell/Operational" `
                          -FilterXPath "*[System[(EventID=4103)]]"
    
    $moduleUsage = @{}
    
    foreach ($event in $events) {
        $moduleName = $event.Properties[0].Value
        
        if ($moduleUsage.ContainsKey($moduleName)) {
            $moduleUsage[$moduleName]++
        }
        else {
            $moduleUsage[$moduleName] = 1
        }
    }
    
    $moduleUsage.GetEnumerator() | 
        Sort-Object -Property Value -Descending | 
        Format-Table -AutoSize
}
```

## 전사

### 전사 활성화

```powershell
# Enable transcription
$registryPath = "HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\Transcription"

if (-not (Test-Path $registryPath)) {
    New-Item -Path $registryPath -Force
}

$transcriptionPath = "C:\Logs\PowerShellTranscripts"
if (-not (Test-Path $transcriptionPath)) {
    New-Item -Path $transcriptionPath -ItemType Directory -Force
}

Set-ItemProperty -Path $registryPath -Name "EnableTranscripting" -Value 1 -Force
Set-ItemProperty -Path $registryPath -Name "EnableInvocationHeader" -Value 1 -Force
Set-ItemProperty -Path $registryPath -Name "OutputDirectory" -Value $transcriptionPath -Force
```

### 전사 구성

```powershell
# Start transcription manually
Start-Transcript -Path "C:\Logs\transcript_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"

# Stop transcription
Stop-Transcript

# Enable transcription for all sessions
$PSDefaultParameterValues['Start-Transcript:IncludeInvocationHeader'] = $true
```

## 충분한 행정(JEA)

### JEA 세션 구성 생성

```powershell
# Create role capability file
$roleParams = @{
    Path = ".\AdminRole.psrc"
    VisibleCmdlets = "Get-Service", "Restart-Service"
    VisibleFunctions = "Get-SystemInfo"
    VisibleExternalCommands = "C:\Windows\System32\whoami.exe"
}

New-PSRoleCapabilityFile @roleParams

# Create session configuration file
$sessionParams = @{
    Path = ".\JEAConfig.pssc"
    SessionType = "RestrictedRemoteServer"
    RunAsVirtualAccount = $true
    RoleDefinitions = @{
        "CONTOSO\\JEA_Admins" = @{
            RoleCapabilityFiles = @(".\\AdminRole.psrc")
        }
    }
    TranscriptDirectory = "C:\\Transcripts"
}

New-PSSessionConfigurationFile @sessionParams

# Register session configuration
Register-PSSessionConfiguration -Path ".\JEAConfig.pssc" -Name "JEA" -Force
```

## 코드 서명

### 서명 스크립트

```powershell
# Get code signing certificate
$cert = Get-ChildItem -Path Cert:\CurrentUser\My -CodeSigningCert | Select-Object -First 1

# Sign script
Set-AuthenticodeSignature -FilePath ".\script.ps1" -Certificate $cert -TimestampServer "http://timestamp.digicert.com"

# Verify signature
Get-AuthenticodeSignature -FilePath ".\script.ps1"
```

### 서명된 스크립트 시행

```powershell
# Require signed scripts only
Set-ExecutionPolicy -Scope LocalMachine -ExecutionPolicy AllSigned

# Test compliance
Get-AuthenticodeSignature -FilePath ".\script.ps1" | Select-Object Status
```

## 모니터링 및 경고

### PowerShell 보안 이벤트

```powershell
# Key event IDs to monitor
$securityEventIds = @{
    ScriptBlockExecution = 4104
    ModuleInvocation = 4103
    ModuleLogging = 4103
    PipelineExecution = 4104
    ScriptBlockLogging = 4104
}

# Query events
foreach ($eventId in $securityEventIds.Values) {
    $events = Get-WinEvent -LogName "Microsoft-Windows-PowerShell/Operational" `
                          -FilterXPath "*[System[(EventID=$eventId)]]" `
                          -MaxEvents 50
    
    Write-Host "Event ID $eventId: $($events.Count) events"
}
```

### 경고 구성

```powershell
# Create scheduled task for monitoring
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-File C:\Scripts\Monitor-PowerShell.ps1"
$trigger = New-ScheduledTaskTrigger -Daily -At "3:00 AM"

Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "PowerShell Security Monitor" -Description "Monitor PowerShell security events"
```

## 규정 준수 검사

### 보안 준수 확인

```powershell
function Test-PowerShellSecurityCompliance {
    $compliance = @{
        ExecutionPolicy = $false
        ScriptBlockLogging = $false
        ModuleLogging = $false
        Transcription = $false
        ConstrainedMode = $false
    }
    
    # Check execution policy
    $policy = Get-ExecutionPolicy -Scope LocalMachine
    if ($policy -in @('RemoteSigned', 'AllSigned')) {
        $compliance.ExecutionPolicy = $true
    }
    
    # Check script block logging
    $sbLogging = (Get-ItemProperty "HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging" -ErrorAction SilentlyContinue).EnableScriptBlockLogging
    if ($sbLogging -eq 1) {
        $compliance.ScriptBlockLogging = $true
    }
    
    # Check module logging
    $modLogging = (Get-ItemProperty "HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\ModuleLogging" -ErrorAction SilentlyContinue).EnableModuleLogging
    if ($modLogging -eq 1) {
        $compliance.ModuleLogging = $true
    }
    
    # Check transcription
    $transcription = (Get-ItemProperty "HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\Transcription" -ErrorAction SilentlyContinue).EnableTranscripting
    if ($transcription -eq 1) {
        $compliance.Transcription = $true
    }
    
    # Check constrained mode
    $mode = $ExecutionContext.SessionState.LanguageMode
    if ($mode -eq 'ConstrainedLanguage') {
        $compliance.ConstrainedMode = $true
    }
    
    # Display results
    $compliance.GetEnumerator() | ForEach-Object {
        $status = if ($_.Value) { "✓" } else { "✗" }
        $color = if ($_.Value) { "Green" } else { "Red" }
        Write-Host "$status $($_.Name)" -ForegroundColor $color
    }
    
    return $compliance
}
```

## 모범 사례

1. **심층 방어**: 여러 보안 제어 계층화
2. **정기 감사**: 보안 로그를 정기적으로 검토합니다.
3. **변경 사항 테스트**: 비프로덕션에서 보안 변경 사항을 테스트합니다.
4. **문서화**: 모든 보안 구성을 문서화합니다.
5. **모니터링**: 지속적인 모니터링 구현
6. **알림**: 의심스러운 활동에 대한 알림을 설정합니다.
7. **업데이트**: PowerShell과 시스템을 최신 상태로 유지하세요.
8. **교육**: PowerShell 보안에 대해 직원 교육

## 자원

- [PowerShell 보안 문서](https://docs.microsoft.com/en-us/powershell/scripting/learn/remoting/wsman-credentials-in-security-descriptions)
- [스크립트 블록 로깅](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_script_block_logging)
- [JEA 문서](https://docs.microsoft.com/en-us/powershell/scripting/learn/remoting/jea/overview)