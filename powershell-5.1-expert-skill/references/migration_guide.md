# PowerShell 마이그레이션 가이드(5.1 → 7)

## 개요

이 가이드는 Windows PowerShell 5.1에서 PowerShell 7+로 스크립트와 모듈을 마이그레이션하는 데 도움이 됩니다.

## 주요 차이점

### 플랫폼 지원

| 특징 | 파워셸 5.1 | 파워셸 7 |
|---------|----------------|---------------|
| 윈도우 지원 | 가득한 | 가득한 |
| 리눅스 지원 | No | 예 |
| macOS 지원 | No | 예 |
| ARM64 지원 | 제한된 | 예 |
| 패키지 관리자 | MSI, MSIx | MSI, MSIx, ZIP, Linux 패키지 |

### 명령 변경 사항

| 파워셸 5.1 | 파워셸 7 | 메모 |
|-----------------|---------------|-------|
| `Get-WmiObject` | `Get-CimInstance` | CIM 선호 |
| `Invoke-WmiMethod` | `Invoke-CimMethod` | CIM 선호 |
| `Register-WmiEvent` | `Register-CimIndicationEvent` | CIM 선호 |
| `Remove-WmiObject` | `Remove-CimInstance` | CIM 선호 |

## 단계별 마이그레이션

### 1. 업데이트 구문

#### 배열 하위 표현식

**파워셸 5.1:**```powershell
$array = @()
$array += "Item1"
$array += "Item2"
```

**파워셸 7:**```powershell
$array = @("Item1", "Item2")
# Or use pipeline
$array = @("Item1", "Item2")
```

#### Null 병합

**파워셸 5.1:**```powershell
if ($null -eq $value) {
    $value = "default"
}
```

**파워셸 7:**```powershell
$value = $value ?? "default"
```

#### Null 조건부 할당

**파워셸 5.1:**```powershell
if ($object -ne $null) {
    $object.Property = "value"
}
```

**파워셸 7:**```powershell
$object?.Property = "value"
```

### 2. WMI를 CIM으로 교체

**파워셸 5.1:**```powershell
$process = Get-WmiObject -Class Win32_Process -Filter "Name='notepad.exe'"
```

**파워셸 7:**```powershell
$process = Get-CimInstance -ClassName Win32_Process -Filter "Name='notepad.exe'"
```

**파워셸 5.1:**```powershell
$wmi = Get-WmiObject -Class Win32_OperatingSystem
Invoke-WmiMethod -InputObject $wmi -Name "Win32Shutdown" -ArgumentList @()
```

**파워셸 7:**```powershell
$cim = Get-CimInstance -ClassName Win32_OperatingSystem
Invoke-CimMethod -InputObject $cim -MethodName "Win32Shutdown" -Arguments @{}
```

### 3. 플랫폼별 코드 업데이트

**PowerShell 5.1(Windows 전용):**```powershell
# Use Windows-specific APIs
Add-Type -AssemblyName System.Windows.Forms
```

**PowerShell 7(크로스 플랫폼):**```powershell
# Check platform first
if ($IsWindows) {
    Add-Type -AssemblyName System.Windows.Forms
} elseif ($IsLinux) {
    # Use Linux-specific APIs
} elseif ($IsMacOS) {
    # Use macOS-specific APIs
}
```

### 4. 오류 처리 현대화

**파워셸 5.1:**```powershell
try {
    Get-Item "nonexistent"
}
catch {
    Write-Error $_
}
```

**파워셸 7:**```powershell
try {
    Get-Item "nonexistent"
}
catch [System.Management.Automation.ItemNotFoundException] {
    Write-Warning "Item not found"
}
catch {
    Write-Error $_
}
```

### 5. 매개변수 유효성 검사 업데이트

**파워셸 5.1:**```powershell
param(
    [Parameter(Mandatory=$true)]
    [string]$Path
)
```

**파워셸 7:**```powershell
param(
    [Parameter(Mandatory=$true)]
    [ValidateScript({
        if (-not (Test-Path $_)) {
            throw "Path does not exist: $_"
        }
        $true
    })]
    [string]$Path
)
```

## 모듈 마이그레이션

### 업데이트 모듈 매니페스트

**파워셸 5.1:**```powershell
@{
    ModuleVersion = '1.0.0'
    PowerShellVersion = '5.1'
    CompatiblePSEditions = @('Desktop')
    # ...
}
```

**파워셸 7:**```powershell
@{
    ModuleVersion = '1.0.0'
    PowerShellVersion = '5.1'
    CompatiblePSEditions = @('Desktop', 'Core')
    # ...
}
```

### 업데이트 #문이 필요합니다.

**파워셸 5.1:**```powershell
#Requires -Version 5.1
#Requires -Modules ActiveDirectory
```

**파워셸 7:**```powershell
#Requires -Version 7.0
#Requires -Modules @{ ModuleName='ActiveDirectory'; ModuleVersion='1.0.0.0' }
```

## 주요 변경 사항

### 제거된 기능

1. **PowerShell 워크플로** - PowerShell 7에서는 사용할 수 없습니다.
2. **PowerShell Snap-in** - 대신 모듈 사용
3. **일부 Windows 관련 API** - Linux/macOS에서는 작동하지 않을 수 있습니다.

### 행동 변화

1. **대소문자 구분** - Linux의 PowerShell 7은 대소문자를 구분합니다.
2. **파일 경로** - 플랫폼 간 호환성을 위해 슬래시 `/`를 사용하세요.
3. **문화 설정** - 기본값은 en-US이며 OS에 따라 다를 수 있습니다.

## 테스트 체크리스트

PowerShell 7 스크립트를 배포하기 전에:

- [ ] Windows에서 테스트
- [ ] Linux에서 테스트(해당되는 경우)
- [ ] macOS에서 테스트(해당하는 경우)
- [ ] CIM으로 변환된 모든 WMI 호출을 확인합니다.
- [ ] Windows 관련 API 확인
- [ ] 테스트 파일 경로 처리
- [ ] 모듈 호환성 확인
- [ ] 테스트 오류 처리
- [ ] 매개변수 유형 검증

## 마이그레이션 예시

### 이전(PowerShell 5.1)

```powershell
# Get-Service.ps1
[CmdletBinding()]
param(
    [string]$ComputerName = $env:COMPUTERNAME
)

$services = Get-WmiObject -Class Win32_Service -ComputerName $ComputerName

foreach ($service in $services) {
    $status = switch ($service.State) {
        'Running' { [System.ConsoleColor]::Green }
        'Stopped' { [System.ConsoleColor]::Red }
        default { [System.ConsoleColor]::Yellow }
    }
    
    Write-Host "$($service.Name) - $($service.State)" -ForegroundColor $status
}
```

### 이후(PowerShell 7)

```powershell
# Get-Service.ps1
#Requires -Version 7.0

[CmdletBinding()]
param(
    [string]$ComputerName = $env:COMPUTERNAME
)

$services = Get-CimInstance -ClassName Win32_Service -ComputerName $ComputerName

foreach ($service in $services) {
    $status = switch ($service.State) {
        'Running' { 'Green' }
        'Stopped' { 'Red' }
        default { 'Yellow' }
    }
    
    Write-Host "$($service.Name) - $($service.State)" -ForegroundColor $status
}
```

## 문제 해결

### 일반적인 문제

**문제:** Linux에서 대소문자 구분 오류로 인해 스크립트가 실패합니다.

**해결책:** 변수 및 함수 이름에 일관된 대소문자 사용

**문제:** WMI cmdlet을 찾을 수 없습니다.

**해결책:** CIM cmdlet으로 교체

**문제:** Windows 관련 API를 사용할 수 없음

**해결책:** 플랫폼 검사를 추가하거나 크로스 플랫폼 대안을 사용하세요.

## 추가 리소스

- [PowerShell 7 릴리스 노트](https://docs.microsoft.com/en-us/powershell/scripting/whats-new/what-s-new-in-powershell-70)
- [PowerShell 7 호환성](https://docs.microsoft.com/en-us/powershell/scripting/whats-new/differences-from-windows-powershell)
- [_PS_ISE 정보](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_ps_ise)